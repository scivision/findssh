import ipaddress
import asyncio

import findssh

PORT = 22
SERVICE = ""
TIMEOUT = 1.0


def test_coroutine():
    net = findssh.netfromaddress(findssh.getLANip())
    hosts = asyncio.run(findssh.get_hosts(net, PORT, SERVICE, TIMEOUT))
    for host, svc in hosts:
        assert isinstance(host, ipaddress.IPv4Address)
        assert isinstance(svc, str)
        break
