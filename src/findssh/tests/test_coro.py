#!/usr/bin/env python
import ipaddress

import findssh

PORT = 22
SERVICE = ""
TIMEOUT = 1.0


def test_coroutine():
    net = findssh.netfromaddress(findssh.getLANip())
    hosts = findssh.runner(findssh.get_hosts, net, PORT, SERVICE, TIMEOUT)
    if len(hosts) > 0:
        host = hosts[0]
        assert isinstance(host[0], ipaddress.IPv4Address)
        assert isinstance(host[1], str)
