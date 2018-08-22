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
from time import time
import logging
from typing import Union, List
import socket
import ipaddress as ip
import concurrent.futures
from itertools import repeat

TIMEOUT = 0.3
PORT = 22


def run(port: int=PORT, service: str='', timeout: float=TIMEOUT,
        baseip: Union[str, ip.IPv4Address]=None, debug: bool=False):
    tic = time()

    if not baseip:
        ownip = getLANip()
        print('own address', ownip)
    else:
        ownip = ip.ip_address(baseip)

    assert isinstance(ownip, ip.IPv4Address)

    net = netfromaddress(ownip)

    servers = scanhosts(net, port, service, timeout, debug)
    print('\n*** RESULTS ***')
    print('found', len(servers), service, 'servers on port', port,
          'in {:.1f} seconds:'.format(time()-tic))
    print('\n'.join(map(str, servers)))


# %% (1) get LAN IP of laptop
def getLANip() -> Union[ip.IPv4Address, ip.IPv6Address]:
    """ get IP of own interface
     ref: http://stackoverflow.com/a/23822431
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # don't use link local here (169.254.x.x) unless you have a specific need
        try:
            s.connect(('<broadcast>', 0))
        except OSError:
            s.connect(('8.8.8.8', 80))  # for BSD/Mac

        name = s.getsockname()[0]

    return ip.ip_address(name)


# %% (2) scan subnet for SSH servers
def isportopen(host: ip.IPv4Address, port: int, service: str,
               timeout: float=TIMEOUT,
               verbose: bool=True) -> bool:
    h = host.exploded

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)  # seconds
        try:
            s.connect((h, port))
            b = s.recv(32)  # arbitrary number of bytes
# %% service decode (optional)
            ok = validateservice(service, h, b)
            if ok and verbose:
                print('found', service, 'on', host, 'port', port)

            return ok

        except (ConnectionRefusedError, socket.timeout, socket.error):
            logging.info('no connection to {} {}'.format(h, port))
            return False


def validateservice(service: str, h: str, b: bytes) -> bool:
    if not b:  # empty reply
        return False
# %% non-empty reply
    try:
        """
        splitlines is in case the ASCII/UTF8 response is less than 32 bytes,
        hoping server sends a \r\n
        """
        u = b.splitlines()[0].decode('utf-8')
        print('\n', u)
    except UnicodeDecodeError:
        """
        must not have been utf8 encoding..., maybe latin1 or something else..
        """
        print('\n', b)
        return False

# %% optional service validation
    val = True
    if service and service not in u.lower():
        val = False

    return val


def netfromaddress(addr: ip.IPv4Address) -> ip.IPv4Network:

    assert isinstance(addr, ip.IPv4Address)

    net = ip.ip_network(addr.exploded.rsplit('.', 1)[0]+'.0/24')

    assert isinstance(net, ip.IPv4Network)

    return net


# %% main loop
def scanhosts(net: ip.IPv4Network,
              port: int, service: str,
              timeout: float, debug: bool) -> List[ip.IPv4Address]:
    """
    loops over xxx.xxx.xxx.1-254
    IPv4 only.
    """

    assert isinstance(net, ip.IPv4Network)

    print('searching', net)

    hosts = net.hosts()

    if debug:
        servers = [h for h in hosts if isportopen(h, port, service, timeout)]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as exc:
            servers = [h for h, s in zip(hosts,
                                         exc.map(isportopen, hosts,
                                                 repeat(port),
                                                 repeat(service))) if s]

    return servers


def main():
    from argparse import ArgumentParser
    p = ArgumentParser('scan for hosts with open port, without NMAP')
    p.add_argument('-p', '--port', help='single port to try',
                   default=PORT, type=int)
    p.add_argument('-s', '--service',
                   help='string to match to qualify detections', default='')
    p.add_argument('-t', '--timeout',
                   help='timeout to wait for server',
                   default=TIMEOUT, type=float)
    p.add_argument('-b', '--baseip',
                   help='set a specific subnet to scan')
    p.add_argument('--debug', help='run single-threaded for debugging',
                   action='store_true')
    P = p.parse_args()

    run(P.port, P.service, P.timeout, P.baseip, P.debug)


if __name__ == '__main__':
    main()
