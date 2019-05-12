"""
threadpool.py launches one thread per IPv4Address and is significantly slower and uses more resources
than the recommended asyncio coroutines in coro.py
"""
import concurrent.futures
import ipaddress as ip
from typing import List
import itertools
import socket

from .base import PORT, TIMEOUT, validateservice, getLANip, netfromaddress


def isportopen(host: ip.IPv4Address, port: int, service: str,
               timeout: float = TIMEOUT,
               verbose: bool = True) -> bool:
    h = host.exploded

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)  # seconds
        ret = s.connect_ex((h, port))

        if ret:
            return False

        b = s.recv(32)  # arbitrary number of bytes
# %% service decode (optional)
    ok = validateservice(service, h, b)
    if ok and verbose:
        print('found', service, 'on', host, 'port', port)

    return ok


def arbiter(net: ip.IPv4Network,
            port: int, service: str,
            timeout: float, debug: bool = False) -> List[ip.IPv4Address]:
    """
    loops over xxx.xxx.xxx.1-254
    IPv4 only. One thread per address.
    """

    assert isinstance(net, ip.IPv4Network)

    print('searching', net)

    hosts = list(net.hosts())

    if debug:
        servers = [h for h in hosts if isportopen(h, port, service, timeout)]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exc:
            portsopen = exc.map(isportopen, hosts,
                                itertools.repeat(port), itertools.repeat(service))
            servers = list(itertools.compress(hosts, portsopen))

    return servers


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

    return arbiter(net, port, service, timeout)
