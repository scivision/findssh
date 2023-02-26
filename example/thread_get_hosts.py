#!/usr/bin/env python3
"""
example of using findssh from a Python script.

Threads are MUCH slower than using asyncio as in asyncio_get_hosts.py
"""

import findssh
import findssh.threadpool

PORT = 22  # default SSH port
TIMEOUT = 1.0  # seconds
# timeout needs to be finite otherwise non-existant hosts are waited for forever

ownIP = findssh.get_lan_ip()
print("own address", ownIP)
net = findssh.address2net(ownIP)
print("searching", net)

for host in findssh.threadpool.get_hosts(net, PORT, TIMEOUT):
    print(host)
