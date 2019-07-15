"""
this method uses Python asyncio coroutines and is significantly faster and leaner,
here using only ONE thread total, instead of the slower one-thread-per-address
threadpool.py method
"""
import logging
import ipaddress as ip
import typing
import asyncio

from .base import validateservice, getLANip, netfromaddress


async def get_hosts(net: ip.IPv4Network,
                    port: int,
                    service: str,
                    timeout: float) -> typing.List[typing.Tuple[ip.IPv4Address, str]]:

    if not net:
        ownip = getLANip()
        print('own address', ownip)
    elif isinstance(net, str):
        ownip = ip.ip_address(net)

    if not isinstance(net, ip.IPv4Network):
        net = netfromaddress(ownip)

    # print(list(net.hosts()))  # all the addresses to be pinged
    hosts = await as_completed(net, port, service, timeout)

    # futures = [isportopen(host, port, service) for host in net.hosts()]
    # host_results = await asyncio.gather(*futures)
    # hosts = list(filter(None, host_results))
    return hosts


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


async def isportopen(host: ip.IPv4Address,
                     port: int,
                     service: str) -> typing.Tuple[ip.IPv4Address, str]:
    """
    https://docs.python.org/3/library/asyncio-stream.html#asyncio.open_connection
    """
    host_str = host.exploded

    try:
        reader, _ = await asyncio.open_connection(host_str, port)
        b = await reader.read(32)  # arbitrary number of bytes
    except (OSError, ConnectionError) as err:
        logging.debug(err)
        return None
# %% service decode (optional)
    svc_txt = validateservice(service, host_str, b)
    if svc_txt:
        return host, svc_txt
    return None
