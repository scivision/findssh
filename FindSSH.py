#!/usr/bin/env python
"""
scans IPv4 subnet for SSH servers on Port 22 or other server ports.
Useful for machines that don't/can't have NMAP installed (e.g. Windows),
  and device does not have Avahi server.
I wanted to make it as cross-platform as possible,
  where the user would have only basic Python installed (Windows)

Michael Hirsch, Ph.D.

Note: timeout value bare minimum is 0.15 seconds for LAN,
    suggest using higher values say 0.25 or 0.35.

"""
import ipaddress as ip
from argparse import ArgumentParser
from findssh.base import netfromaddress, getLANip
from findssh import main as comain

PORT = 22


def main():
    p = ArgumentParser('scan for hosts with open port, without NMAP')
    p.add_argument('-p', '--port', help='single port to try',
                   default=PORT, type=int)
    p.add_argument('-s', '--service', default='',
                   help='string to match to qualify detections')
    p.add_argument('-t', '--timeout', help='timeout to wait for server', type=float)
    p.add_argument('-b', '--baseip', help='set a specific subnet to scan')
    P = p.parse_args()

    if not P.baseip:
        ownip = getLANip()
        print('own address', ownip)
    else:
        ownip = ip.ip_address(P.baseip)

    net = netfromaddress(ownip)
    print('searching', net)

    comain(net, P.port, P.service, P.timeout)


if __name__ == '__main__':
    main()
