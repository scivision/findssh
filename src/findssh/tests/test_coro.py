import ipaddress
import asyncio

import findssh
import findssh.coro

PORT = 22
TIMEOUT = 0.5


def test_coroutine():
    net = findssh.address2net(findssh.get_lan_ip())
    hosts = asyncio.run(findssh.coro.get_hosts(net, PORT, TIMEOUT))
    for host, svc in hosts:
        assert isinstance(host, ipaddress.IPv4Address)
        assert isinstance(svc, str)
        break
