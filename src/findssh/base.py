from __future__ import annotations
import ipaddress as ip
import socket
import logging
from collections.abc import Iterable


def get_service(b: bytes, service: str | None = None) -> str | None:
    """
    splitlines is in case the ASCII/UTF8 response is less than 32 bytes,
    hoping server sends a \r\n
    """

    if lines := b.splitlines():
        svc_txt = lines[0].decode("utf-8", errors="ignore")
    # %% optional service validation
        if service and service not in svc_txt.lower():
            return None

        return svc_txt

    return None


def is_port_open(
    host: ip.IPv4Address, port: int, timeout: float, service: str | None = None
) -> tuple[ip.IPv4Address, str] | None:
    """
    is a port open? Without coroutines.
    """

    h = host.exploded

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)  # seconds
        try:
            if s.connect_ex((h, port)):
                return None
        except socket.gaierror:
            return None

        try:
            # If recv returns empty bytes, the connection was closed by the remote host.
            # This does not necessarily mean the port is closed, but no service banner was received.
            if not (resp := s.recv(32)):
                return None
        except (socket.timeout, ConnectionError) as err:
            logging.debug("Socket error: %s", err)
            return None

    if svc_txt := get_service(resp, service):
        return host, svc_txt

    return None


def get_hosts_seq(
    net: ip.IPv4Network, port: int, timeout: float, service: str | None = None
) -> Iterable[tuple[ip.IPv4Address, str]]:
    """
    Yields hosts in the network that have the specified port open and
    match the service (if provided),
    sequentially (no parallelism or concurrency).
    """

    for host in net.hosts():
        if res := is_port_open(host, port, timeout, service):
            yield res
