"""
this method uses Python asyncio coroutines and is significantly faster and leaner,
here using only ONE thread total, instead of the slower one-thread-per-address
threadpool.py method
"""

from __future__ import annotations
import logging
import ipaddress as ip
import asyncio

from .base import get_service

__all__ = ["get_hosts"]


async def get_hosts(
    net: ip.IPv4Network,
    port: int,
    timeout: float,
    service: str | None = None,
) -> list[tuple[ip.IPv4Address, str]]:
    """
    Timeout must be finite otherwise non-existant hosts are waited for forever
    """

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
        res = await asyncio.wait_for(is_port_open(host, port, service), timeout=timeout)
    except asyncio.TimeoutError:
        res = None

    return res


async def is_port_open(
    host: ip.IPv4Address, port: int, service: str
) -> tuple[ip.IPv4Address, str]:
    """
    https://docs.python.org/3/library/asyncio-stream.html#asyncio.open_connection
    """
    host_str = host.exploded

    try:
        reader, _ = await asyncio.open_connection(host_str, port)
        if not (b := await reader.read(32)):
            return None
    except OSError as err:  # to avoid flake8 error OSError has ConnectionError
        logging.debug(err)
        return None

    if svc_txt := get_service(b, service):
        return host, svc_txt

    return None
