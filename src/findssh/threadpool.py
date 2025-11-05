"""
threadpool.py launches one thread per IPv4Address and is
significantly slower and uses more resources
than the recommended asyncio coroutines in coro.py
"""

from __future__ import annotations
import concurrent.futures
import logging
import ipaddress as ip
from collections.abc import Iterable

from .base import is_port_open

__all__ = ["get_hosts"]


def get_hosts(
    net: ip.IPv4Network,
    port: int,
    timeout: float,
    service: str | None = None,
) -> Iterable[tuple[ip.IPv4Address, str]]:
    """
    loops over hosts in network, one thread per address.
    This is MUCH slower than asyncio coroutines in coro.py

    Timeout must be finite otherwise non-existant hosts are waited for forever
    """

    with concurrent.futures.ThreadPoolExecutor() as exc:
        try:
            futures = (
                exc.submit(is_port_open, host, port, timeout, service)
                for host in net.hosts()
            )
            for future in concurrent.futures.as_completed(futures):
                if res := future.result():
                    yield res
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt")
            # the shutdown() is necessary to immediately halt threads, otherwise the
            # futures are still waited on
            exc.shutdown(wait=True, cancel_futures=True)
