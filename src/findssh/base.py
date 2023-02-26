from __future__ import annotations
import ipaddress as ip
import socket
import typing as T


def get_service(b: bytes, service: str | None = None) -> str:
    """
    splitlines is in case the ASCII/UTF8 response is less than 32 bytes,
    hoping server sends a \r\n
    """

    svc_txt = b.splitlines()[0].decode("utf-8", errors="ignore")
    # %% optional service validation
    if service and service not in svc_txt.lower():
        return None

    return svc_txt


def is_port_open(
    host: ip.IPv4Address, port: int, timeout: float, service: str | None = None
) -> tuple[ip.IPv4Address, str]:
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
            if not (resp := s.recv(32)):
                return None
        except (socket.timeout, ConnectionError):
            return None

    if svc_txt := get_service(resp, service):
        return host, svc_txt

    return None


def get_hosts_seq(
    net: ip.IPv4Network, port: int, timeout: float, service: str | None = None
) -> T.Iterable[tuple[ip.IPv4Address, str]]:
    """
    find hosts sequentially (no parallelism or concurrency)
    """

    for host in net.hosts():
        if res := is_port_open(host, port, timeout, service):
            yield res
