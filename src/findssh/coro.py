"""
this method uses Python asyncio coroutines and is significantly faster and leaner,
here using only ONE thread total, instead of the slower one-thread-per-address
threadpool.py method
"""

import logging
import ipaddress as ip
import asyncio
from collections.abc import Mapping

from .base import HostResult, get_service
from .http import is_http_response, get_http_service

__all__ = ["get_hosts", "discover_services"]


async def get_hosts(
    net: ip.IPv4Network,
    port: int,
    timeout: float,
    service: str | None = None,
    max_concurrent: int = 100,
) -> list[HostResult]:
    """
    Timeout must be finite otherwise non-existant hosts are waited for forever

    use of Semaphore limits number of concurrent connections to avoid
    overloading system with large nets
    100 is a reasonable default for most systems
    """

    if max_concurrent < 1:
        raise ValueError(f"max_concurrent must be >= 1, got {max_concurrent}")

    hosts: list[HostResult] = []
    host_queue: asyncio.Queue[ip.IPv4Address] = asyncio.Queue()
    for host in net.hosts():
        host_queue.put_nowait(host)

    async def worker() -> None:
        while True:
            try:
                host = host_queue.get_nowait()
            except asyncio.QueueEmpty:
                return

            if result := await waiter(host, port, service, timeout):
                logging.info("Found host: %s", result)
                hosts.append(result)

    worker_count = min(max_concurrent, max(1, host_queue.qsize()))
    async with asyncio.TaskGroup() as tg:
        for _ in range(worker_count):
            tg.create_task(worker())

    return hosts


async def waiter(
    host: ip.IPv4Address, port: int, service: str | None, timeout: float
) -> HostResult | None:
    try:
        async with asyncio.timeout(timeout):
            return await is_port_open(host, port, service)
    except TimeoutError:
        return None


async def is_port_open(
    host: ip.IPv4Address, port: int, service: str | None
) -> HostResult | None:
    """
    https://docs.python.org/3/library/asyncio-stream.html#asyncio.open_connection
    """
    host_str = host.exploded

    try:
        reader, writer = await asyncio.open_connection(host_str, port)
        if not (b := await reader.read(32)):
            return None
    except OSError as err:  # to avoid flake8 error OSError has ConnectionError
        logging.debug("Error connecting to %s:%s - %s", host_str, port, err)
        return None
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except (NameError, OSError):
            pass

    if svc_txt := get_service(b, service):
        return host, svc_txt

    return None


async def discover_services(
    net: ip.IPv4Network,
    service_ports: Mapping[str, int | list[int]],
    timeout: float,
    max_concurrent: int = 100,
) -> dict[str, list[HostResult]]:
    """
    Discover multiple services (e.g., SSH, HTTP) across a network in a single pass.

    Scans a subnet for multiple services simultaneously, using a worker pool pattern
    with asyncio.TaskGroup to efficiently parallelize connections across all hosts
    and ports.

    Args:
        net: IPv4Network to scan (e.g., IPv4Network('192.168.1.0/24'))
        service_ports: Mapping of service names to port(s)
                      Examples:
                        - {"ssh": 22, "http": 80}
                        - {"ssh": 22, "http": [80, 443]}
                        - {"dns": 53, "ssh": 22}
        timeout: Connection timeout in seconds (must be finite)
        max_concurrent: Maximum number of concurrent connections (default: 100)

    Returns:
        Dictionary mapping service names to lists of (IPv4Address, banner_text) tuples
        Example: {
            "ssh": [(IPv4Address('192.168.1.1'), 'OpenSSH_8.0...'), ...],
            "http": [(IPv4Address('192.168.1.3'), 'HTTP/1.1 200 OK'), ...]
        }

    Raises:
        ValueError: If max_concurrent < 1
    """
    if max_concurrent < 1:
        raise ValueError(f"max_concurrent must be >= 1, got {max_concurrent}")

    # Normalize service_ports to dict[service_name, list[int]]
    normalized_ports: dict[str, list[int]] = {}
    for service_name, ports in service_ports.items():
        if isinstance(ports, int):
            normalized_ports[service_name] = [ports]
        elif isinstance(ports, list):
            normalized_ports[service_name] = ports
        else:
            raise TypeError(
                f"Port for service '{service_name}' must be int or list[int], "
                f"got {type(ports).__name__}"
            )

    # Build work queue: (host, port, service_name) tuples
    work_queue: asyncio.Queue[tuple[ip.IPv4Address, int, str]] = asyncio.Queue()
    for host in net.hosts():
        for service_name, ports in normalized_ports.items():
            for port in ports:
                work_queue.put_nowait((host, port, service_name))

    # Results dict
    results: dict[str, list[HostResult]] = {svc: [] for svc in normalized_ports}

    async def worker() -> None:
        """Worker coroutine: process work queue items until empty."""
        while True:
            try:
                host, port, service_name = work_queue.get_nowait()
            except asyncio.QueueEmpty:
                return

            if result := await discover_waiter(host, port, service_name, timeout):
                logging.info("Found %s host: %s", service_name, result)
                results[service_name].append(result)

    # Calculate worker count based on queue size and max_concurrent
    worker_count = min(max_concurrent, max(1, work_queue.qsize()))

    # Run workers concurrently
    async with asyncio.TaskGroup() as tg:
        for _ in range(worker_count):
            tg.create_task(worker())

    return results


async def discover_waiter(
    host: ip.IPv4Address, port: int, service_name: str, timeout: float
) -> HostResult | None:
    """
    Attempt to connect to a service on a host with timeout.

    Routes service validation based on service type.
    """
    try:
        async with asyncio.timeout(timeout):
            return await discover_is_port_open(host, port, service_name)
    except TimeoutError:
        return None


async def discover_is_port_open(
    host: ip.IPv4Address, port: int, service_name: str
) -> HostResult | None:
    """
    Check if a port is open and identify the service.

    Routes to service-specific validators:
    - "http": sends HTTP GET request, then validates response headers
    - "ssh": expects SSH banner (service name validation)
    - others: accepts any response as valid (generic port detection)
    """
    host_str = host.exploded

    try:
        reader, writer = await asyncio.open_connection(host_str, port)

        # For HTTP, send a GET request; for others, just read the banner
        if service_name.lower() == "http":
            # Send minimal HTTP request to trigger server response
            http_request = b"GET / HTTP/1.0\r\n\r\n"
            writer.write(http_request)
            await writer.drain()

        if not (b := await reader.read(32)):
            return None
    except OSError as err:
        logging.debug("Error connecting to %s:%s - %s", host_str, port, err)
        return None
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except (NameError, OSError):
            pass

    # Route to service-specific validation
    match service_name.lower():
        case "http":
            if is_http_response(b):
                if svc_txt := get_http_service(b):
                    return host, svc_txt
        case "ssh":
            # SSH service: validate "SSH-" banner
            if svc_txt := get_service(b, "ssh"):
                return host, svc_txt
        case _:
            # Generic service: accept any response
            if b and len(b) > 0:
                try:
                    svc_txt = b.decode("utf-8", errors="ignore").splitlines()[0].strip()
                    if svc_txt:
                        return host, svc_txt
                except Exception:
                    pass

    return None
