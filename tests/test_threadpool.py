"""
normally we use coroutines, but for demo purposes we have threadpool too.
"""
import ipaddress
import pytest
import findssh.threadpool

PORT = 22
SERVICE = ""
TIMEOUT = 1.0


def test_threadpool():
    net = findssh.netfromaddress(findssh.getLANip())
    hosts = findssh.threadpool.get_hosts(net, PORT, SERVICE, TIMEOUT)
    if len(hosts) > 0:
        host = hosts[0]
        assert isinstance(host[0], ipaddress.IPv4Address)
        assert isinstance(host[1], str)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
