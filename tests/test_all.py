#!/usr/bin/env python
import pytest
import subprocess
import ipaddress as ip

import findssh
import findssh.threadpool
from findssh.runner import runner

PORT = 22
SERVICE = ''
TIMEOUT = 1.0


def test_script():
    subprocess.check_call(['findssh'])


def test_coroutine():
    net = findssh.netfromaddress(findssh.getLANip())
    hosts = runner(findssh.get_hosts, net, PORT, SERVICE, TIMEOUT)
    if len(hosts) > 0:
        host = hosts[0]
        assert isinstance(host[0], ip.IPv4Address)
        assert isinstance(host[1], str)


def test_threadpool():
    net = findssh.netfromaddress(findssh.getLANip())
    hosts = findssh.threadpool.get_hosts(net, PORT, SERVICE, TIMEOUT)
    if len(hosts) > 0:
        host = hosts[0]
        assert isinstance(host[0], ip.IPv4Address)
        assert isinstance(host[1], str)


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
