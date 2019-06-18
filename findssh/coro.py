"""
this method uses Python asyncio coroutines and is significantly faster and leaner,
here using only ONE thread total, instead of the slower one-thread-per-address
threadpool.py method
"""
import ipaddress as ip
from typing import AsyncGenerator, Tuple
import asyncio

from .base import validateservice, getLANip, netfromaddress


async def main(net: ip.IPv4Network,
               port: int, service: str,
               timeout: float, verbose: bool = False) -> AsyncGenerator[ip.IPv4Address, None]:

    if not net:
        ownip = getLANip()
        print('own address', ownip)
    elif isinstance(net, str):
        ownip = ip.ip_address(net)
    elif isinstance(net, (ip.IPv4Address, ip.IPv4Network)):
        pass
    else:
        raise TypeError('unexpected input type {}'.format(type(net)))

    if not isinstance(net, ip.IPv4Network):
        net = netfromaddress(ownip)

    # print(list(net.hosts()))
    futures = [isportopen(host, port, service) for host in net.hosts()]
    for future in asyncio.as_completed(futures, timeout=timeout):
        try:
            exists, host = await future
        except asyncio.TimeoutError:
            continue
        except ConnectionRefusedError as err:
            if verbose:
                print(err)
            continue

        if exists:
            yield host


async def isportopen(host: ip.IPv4Address,
                     port: int, service: str) -> Tuple[bool, ip.IPv4Address]:
    """
    https://docs.python.org/3/library/asyncio-stream.html#asyncio.open_connection
    """
    host_str = host.exploded

    r, w = await asyncio.open_connection(host_str, port)
    b = await r.read(32)  # arbitrary number of bytes
# %% service decode (optional)
    exists = validateservice(service, host_str, b)

    return exists, host
