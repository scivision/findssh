#!/usr/bin/env python3
"""
scans IPv4 subnet for SSH servers on Port 22 or other server ports.
Useful for machines that don't/can't have NMAP installed (e.g. Windows),
  and device does not have Avahi server.
I wanted to make it as cross-platform as possible,
  where the user would have only basic Python installed (Windows)

Note:
timeout value bare minimum is 0.15 seconds for LAN,
suggest using higher values say 0.25 or 0.35 to allow for network / CPU delays
Wifi timeout should be 1 second or more
"""

import asyncio
import logging
import ipaddress as ip
from argparse import ArgumentParser

from . import get_lan_ip, address2net
from . import coro
from . import threadpool

PORT = 22
TIMEOUT = 1.0


def main():
    p = ArgumentParser("scan for hosts with open port, without NMAP")
    p.add_argument("-p", "--port", help="single port to try", default=PORT, type=int)
    p.add_argument(
        "-s", "--service", default="", help="string to match to qualify detections"
    )
    p.add_argument(
        "-t",
        "--timeout",
        help="timeout to wait for server. Must be finite or will hang.",
        type=float,
        default=TIMEOUT,
    )
    p.add_argument("-b", "--baseip", help="set a specific subnet to scan")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument(
        "-threadpool", help="use threadpool instead of asyncio", action="store_true"
    )
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if not P.baseip:
        ownip = get_lan_ip()
        print("own address", ownip)
    else:
        ownip = ip.ip_address(P.baseip)

    net = address2net(ownip)
    print("searching", net)

    if P.threadpool:
        for host in threadpool.get_hosts(
            net,
            P.port,
            P.timeout,
            P.service,
        ):
            print(host)
    else:
        asyncio.run(coro.get_hosts(net, P.port, P.timeout, P.service))


if __name__ == "__main__":
    main()
