#!/usr/bin/env python3
"""
example of using findssh from a Python script.

Sequential non-parallel host discovery is impractically slow
"""

import findssh
from findssh.base import get_hosts_seq

PORT = 22  # default SSH port
TIMEOUT = 1.0  # seconds
# timeout needs to be finite otherwise non-existant hosts are waited for forever

ownIP = findssh.get_lan_ip()
print("own address", ownIP)
net = findssh.address2net(ownIP)
print("searching", net)

for host in get_hosts_seq(net, PORT, TIMEOUT):
    print(host)
