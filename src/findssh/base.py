from __future__ import annotations
import ipaddress as ip
import socket
import typing as T


def getLANip() -> ip.IPv4Address | ip.IPv6Address:
    """get IP of own interface
    ref: http://stackoverflow.com/a/23822431
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # don't use link local here (169.254.x.x) unless you have a specific need
        try:
            s.connect(("<broadcast>", 0))
        except OSError:
            s.connect(("8.8.8.8", 80))  # for BSD/Mac

        name = s.getsockname()[0]

    return ip.ip_address(name)


def validateservice(service: str, h: str, b: bytes) -> str:
    """
    splitlines is in case the ASCII/UTF8 response is less than 32 bytes,
    hoping server sends a \r\n
    """
    if not b:  # empty reply
        return None
    # %% non-empty reply
    svc_txt = b.splitlines()[0].decode("utf-8", "ignore")
    # %% optional service validation
    if service and service not in svc_txt.lower():
        return None

    return svc_txt


def netfromaddress(addr: ip.IPv4Address, mask: str = "24") -> ip.IPv4Network | ip.IPv6Network:

    if isinstance(addr, ip.IPv4Address):
        net = ip.ip_network(addr.exploded.rsplit(".", 1)[0] + f".0/{mask}")
    elif isinstance(addr, ip.IPv6Address):
        net = ip.ip_network(addr.exploded.rsplit(":", 1)[0] + f":0/{mask}")
    else:
        raise TypeError(addr)

    return net


def isportopen(
    host: ip.IPv4Address, port: int, service: str, timeout: float
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
        # %% service decode (optional)
        try:
            svc_txt = validateservice(service, h, s.recv(32))
        except (socket.timeout, ConnectionError):
            return None
    if svc_txt:
        return host, svc_txt
    return None


def get_hosts_seq(
    net: ip.IPv4Network, port: int, service: str, timeout: float
) -> T.Iterable[tuple[ip.IPv4Address, str]]:
    """
    find hosts sequentially (no parallelism or concurrency)
    """

    for host in net.hosts():
        res = isportopen(host, port, service, timeout)
        if res:
            yield res
