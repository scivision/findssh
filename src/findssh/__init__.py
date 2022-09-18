import os
import typing as T
import asyncio
import ipaddress

from .coro import get_hosts as coro_get_hosts
from .threadpool import get_hosts as threadpool_get_hosts
from .base import get_hosts as get_hosts_seq
from .base import netfromaddress, getLANip

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore


def findssh(baseip: str = None, port: int = 22, timeout: float = 1.0) -> T.Iterable[tuple[ipaddress.IPv4Address, str]]:

    ownip = ipaddress.ip_address(baseip) if baseip else getLANip()

    net = netfromaddress(ownip)

    if isinstance(net, ipaddress.IPv6Network):
        return get_hosts_seq(net, port, None, timeout)

    return threadpool_get_hosts(net, port, None, timeout)
