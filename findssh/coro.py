"""
this method uses Python asyncio coroutines and is significantly faster and leaner,
here using only ONE thread total, instead of the slower one-thread-per-address
threadpool.py method
"""
import ipaddress as ip
import itertools
from typing import Tuple, List
import asyncio

from .base import PORT, TIMEOUT, validateservice, getLANip, netfromaddress


def main(net: ip.IPv4Network = None,
         port: int = PORT, service: str = '',
         timeout: float = TIMEOUT):
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
    print('searching', net)

    loop = asyncio.new_event_loop()
    servers = loop.run_until_complete(arbiter(net, port, service, timeout))
    return servers


async def run(host: ip.IPv4Address,
              port: int,
              service: str,
              timeout: float) -> Tuple[ip.IPv4Address, bool]:
    """
    loops over xxx.xxx.xxx.1-254
    IPv4 only.
    """
    if not timeout:
        timeout = TIMEOUT

    try:
        portopen = await asyncio.wait_for(isportopen(host, port, service), timeout=timeout)
        return host, portopen
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return host, False


async def isportopen(host: ip.IPv4Address, port: int, service: str,
                     verbose: bool = True) -> bool:
    """
    https://docs.python.org/3/library/asyncio-stream.html#asyncio.open_connection
    """
    h = host.exploded

    r, w = await asyncio.open_connection(h, port)
    b = await r.read(32)  # arbitrary number of bytes

# %% service decode (optional)
    ok = validateservice(service, h, b)

    if ok and verbose:
        print('found', service, 'on', host, 'port', port)

    return ok


async def arbiter(net: ip.IPv4Network, port: int, service: str, timeout: float) -> List[ip.IPv4Address]:
    assert isinstance(net, ip.IPv4Network), 'only IPv4'

    hosts = net.hosts()

    futures = [run(host, port, service, timeout) for host in hosts]

    portopen = await asyncio.gather(*futures)

    hosts, portopen = zip(*portopen)

    return list(itertools.compress(hosts, portopen))
