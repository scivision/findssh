#!/usr/bin/env python3
"""
example of using findssh from a Python script
"""

import asyncio
import ipaddress

import findssh

PORT = 22  # default SSH port
TIMEOUT = 1.0  # seconds
# timeout needs to be finite otherwise non-existant hosts are waited for forever

ownIP = findssh.get_lan_ip()
print("own address", ownIP)
net = findssh.address2net(ownIP)
print("searching", net)

assert isinstance(net, ipaddress.IPv4Network), "only IPv4 networks are supported"

asyncio.run(findssh.get_hosts(net, PORT, TIMEOUT))
