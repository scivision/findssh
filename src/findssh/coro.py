"""
this method uses Python asyncio coroutines and is significantly faster and leaner,
here using only ONE thread total, instead of the slower one-thread-per-address
threadpool.py method
"""

import logging
import ipaddress as ip
import asyncio

from .base import HostResult, get_service

__all__ = ["get_hosts"]


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
        if "writer" in locals():
            writer.close()
            try:
                await writer.wait_closed()
            except OSError:
                pass

    if svc_txt := get_service(b, service):
        return host, svc_txt

    return None
