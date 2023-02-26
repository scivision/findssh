"""
normally we use coroutines, but for demo purposes we have threadpool too.
"""
import ipaddress

import findssh.threadpool

PORT = 22
TIMEOUT = 0.5


def test_threadpool():
    net = findssh.address2net(findssh.get_lan_ip())
    hosts = findssh.threadpool.get_hosts(net, PORT, TIMEOUT)
    for host, svc in hosts:
        assert isinstance(host, ipaddress.IPv4Address)
        assert isinstance(svc, str)
        break
