"""
threadpool.py launches one thread per IPv4Address and is significantly slower and uses more resources
than the recommended asyncio coroutines in coro.py
"""
import concurrent.futures
import ipaddress as ip
import typing
import socket
import logging
from .base import validateservice


def isportopen(host: ip.IPv4Address, port: int, service: str, timeout: float) -> typing.Tuple[ip.IPv4Address, str]:
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


def get_hosts(
    net: ip.IPv4Network, port: int, service: str, timeout: float, debug: bool = False
) -> typing.Iterable[typing.Tuple[ip.IPv4Address, str]]:
    """
    loops over hosts in network
    One thread per address.

    IPv6 is not well supported, it will overwhelm RAM except by a plain for loop.
    A different approach is needed to handle IPv6 scale, but it's fine for IPv4.
    """

    if debug or isinstance(net, ip.IPv6Network):
        for host in net.hosts():
            logging.debug(host)
            res = isportopen(host, port, service, timeout)
            if res:
                yield res
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exc:
            futures = (exc.submit(isportopen, host, port, service, timeout) for host in net.hosts())
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    yield res
