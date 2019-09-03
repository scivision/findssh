#!/usr/bin/env python
"""
scans IPv4 subnet for SSH servers on Port 22 or other server ports.
Useful for machines that don't/can't have NMAP installed (e.g. Windows),
  and device does not have Avahi server.
I wanted to make it as cross-platform as possible,
  where the user would have only basic Python installed (Windows)

Michael Hirsch, Ph.D.

Note:
timeout value bare minimum is 0.15 seconds for LAN,
suggest using higher values say 0.25 or 0.35 to allow for network / CPU delays
Wifi timeout should be 1 second or more

"""
import logging
import ipaddress as ip
from argparse import ArgumentParser

from findssh.base import getLANip, netfromaddress
from findssh.runner import runner
import findssh.coro as coro
import findssh.threadpool as threadpool

PORT = 22
TIMEOUT = 1.0


def main():
    p = ArgumentParser("scan for hosts with open port, without NMAP")
    p.add_argument("-p", "--port", help="single port to try", default=PORT, type=int)
    p.add_argument("-s", "--service", default="", help="string to match to qualify detections")
    p.add_argument(
        "-t", "--timeout", help="timeout to wait for server", type=float, default=TIMEOUT
    )
    p.add_argument("-b", "--baseip", help="set a specific subnet to scan")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-threadpool", help="use threadpool instead of asyncio", action="store_true")
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if not P.baseip:
        ownip = getLANip()
        print("own address", ownip)
    else:
        ownip = ip.ip_address(P.baseip)

    net = netfromaddress(ownip)
    print("searching", net)

    if P.threadpool:
        hosts = threadpool.get_hosts(net, P.port, P.service, P.timeout)
    else:
        hosts = runner(coro.get_hosts, net, P.port, P.service, P.timeout)

    for host, svc in hosts:
        print(host, svc)


if __name__ == "__main__":
    main()
