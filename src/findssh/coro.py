"""
this method uses Python asyncio coroutines and is significantly faster and leaner,
here using only ONE thread total, instead of the slower one-thread-per-address
threadpool.py method
"""

from __future__ import annotations
import logging
import ipaddress as ip
import asyncio

from .base import validateservice


async def get_hosts(
    net: ip.IPv4Network, port: int, service: str, timeout: float
) -> list[tuple[ip.IPv4Address, str]]:

    hosts = []
    for h in asyncio.as_completed(
        [waiter(host, port, service, timeout) for host in net.hosts()]
    ):
        if host := await h:
            print(host)
            hosts.append(host)

    return hosts


async def waiter(
    host: ip.IPv4Address, port: int, service: str, timeout: float
) -> tuple[ip.IPv4Address, str]:
    try:
        res = await asyncio.wait_for(isportopen(host, port, service), timeout=timeout)
    except asyncio.TimeoutError:
        res = None
    return res


async def isportopen(
    host: ip.IPv4Address, port: int, service: str
) -> tuple[ip.IPv4Address, str]:
    """
    https://docs.python.org/3/library/asyncio-stream.html#asyncio.open_connection
    """
    host_str = host.exploded

    try:
        reader, _ = await asyncio.open_connection(host_str, port)
        b = await reader.read(32)  # arbitrary number of bytes
    except OSError as err:  # to avoid flake8 error OSError has ConnectionError
        logging.debug(err)
        return None
    # %% service decode (optional)
    if svc_txt := validateservice(service, host_str, b):
        return host, svc_txt
    return None
