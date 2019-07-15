import ipaddress as ip
import typing
import asyncio

from findssh.coro import isportopen


async def as_completed(net: ip.IPv4Network,
                       port: int,
                       service: str,
                       timeout: float) -> typing.List[typing.Tuple[ip.IPv4Address, str]]:
    futures = [isportopen(host, port, service) for host in net.hosts()]
    hosts = []
    for future in asyncio.as_completed(futures, timeout=timeout):
        try:
            res = await future
        except asyncio.TimeoutError:
            continue

        if res is not None:
            print(*res)
            hosts.append(res)
    return hosts
