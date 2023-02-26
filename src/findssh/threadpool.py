"""
threadpool.py launches one thread per IPv4Address and is significantly slower and uses more resources
than the recommended asyncio coroutines in coro.py
"""

from __future__ import annotations
import concurrent.futures
import ipaddress as ip
import typing as T

from .base import isportopen


def get_hosts(
    net: ip.IPv4Network, port: int, service: str, timeout: float
) -> T.Iterable[tuple[ip.IPv4Address, str]]:
    """
    loops over hosts in network
    One thread per address.
    """

    with concurrent.futures.ThreadPoolExecutor() as exc:
        try:
            futures = (exc.submit(isportopen, host, port, service, timeout) for host in net.hosts())
            for future in concurrent.futures.as_completed(futures):
                if res := future.result():
                    yield res
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            exc.shutdown(wait=True, cancel_futures=True)
