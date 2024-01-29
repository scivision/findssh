from __future__ import annotations
import socket
import ipaddress

from .coro import get_hosts

__all__ = ["get_hosts", "address2net", "get_lan_ip"]


def get_lan_ip() -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    """
    get IP address of currently used LAN interface
    ref: http://stackoverflow.com/a/23822431
    """

    name = socket.gethostname()
    host = socket.gethostbyname(name)
    return ipaddress.ip_address(host)


def address2net(
    addr: ipaddress.IPv4Address, mask: str = "24"
) -> ipaddress.IPv4Network | ipaddress.IPv6Network:

    if isinstance(addr, ipaddress.IPv4Address):
        net = ipaddress.ip_network(addr.exploded.rsplit(".", 1)[0] + f".0/{mask}")
    elif isinstance(addr, ipaddress.IPv6Address):
        net = ipaddress.ip_network(addr.exploded.rsplit(":", 1)[0] + f":0/{mask}")
    else:
        raise TypeError(addr)

    return net
