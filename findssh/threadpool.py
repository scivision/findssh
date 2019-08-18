"""
threadpool.py launches one thread per IPv4Address and is significantly slower and uses more resources
than the recommended asyncio coroutines in coro.py
"""
import concurrent.futures
import ipaddress as ip
import typing
import itertools
import logging
import socket

from .base import validateservice


def isportopen(
    host: ip.IPv4Address, port: int, service: str, timeout: float
) -> typing.Tuple[ip.IPv4Address, str]:
    h = host.exploded

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)  # seconds
        if s.connect_ex((h, port)):
            return None
        # %% service decode (optional)
        svc_txt = validateservice(service, h, s.recv(32))
    if svc_txt:
        return host, svc_txt
    return None


def get_hosts(
    net: ip.IPv4Network, port: int, service: str, timeout: float, debug: bool = False
) -> typing.List[typing.Tuple[ip.IPv4Address, str]]:
    """
    loops over xxx.xxx.xxx.1-254
    IPv4 only. One thread per address.
    """

    hosts = net.hosts()

    if debug:
        servers = []
        for host in hosts:
            logging.debug(host)
            result = isportopen(host, port, service, timeout)
            if result is not None:
                servers.append(result)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exc:
            res = exc.map(
                isportopen,
                hosts,
                itertools.repeat(port),
                itertools.repeat(service),
                itertools.repeat(timeout),
            )

    servers = list(filter(None, res))

    return servers
