#!/usr/bin/env python3
"""
scans own LAN subnet for SSH servers on Port 22.
Useful for machines that don't/can't have NMAP installed (e.g. Windows)
Yes this can be done simply via Linux shell, but I wanted to make it as cross-platform as possible
where the user would have only basic Python installed (Windows)

Michael Hirsch

Note: if using Python < 3.3, you will need
pip insall ipaddress
"""
from __future__ import division,unicode_literals
from six import PY2,string_types
from time import time
import socket
from ipaddress import ip_address,ip_network,IPv4Network
#
if PY2: ConnectionRefusedError = OSError
#%% (1) get LAN IP of laptop
def getLANip():
    """ get IP of own interface
     ref: http://stackoverflow.com/a/23822431
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    name= s.getsockname()[0]
    s.close()
    return ip_address(name)
#%% (2) scan subnet for SSH servers
def isportopen(host,port,service,timeout=0.15):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout) #seconds
    try:
        s.connect((host.exploded,port))
        r=s.recv(32).decode('utf8') #arbitrary number of bytes
        print(r)
        s.close()
    except (ConnectionRefusedError,socket.timeout,socket.error):
        return

    if service in r.lower():
        return True

def netfromaddress(addr):
    addr = ip_address(addr) #in case it's string
    if addr.version == 4:
        return ip_network(ownip.exploded.rsplit('.',1)[0]+'.0/24')
    else: #addr.version ==6
        raise NotImplementedError('https://www.6net.org/publications/standards/draft-chown-v6ops-port-scanning-implications-00.txt')
#%% main loop
def scanhosts(net,port,service,timeout):
    """
    loops over xxx.xxx.xxx.1-254
    IPv4 only.
    """
    if not isinstance(net,IPv4Network):
        net = netfromaddress(net)

    if net.version == 6:
        raise NotImplementedError('https://www.6net.org/publications/standards/draft-chown-v6ops-port-scanning-implications-00.txt')


    servers = []
    print('searching {}'.format(net))
    for t,a in enumerate(net.hosts()):
        if isportopen(a,port,service):
            servers.append(a)
            print('found {} on {} port {}'.format(service,a,port))
        if not t % 20:
            print('{:.1f} % done, {} {} servers detected on port {}'.format(t/255*100.,len(servers),service,port))
    return servers

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser('scan for hosts with open port, without NMAP')
    p.add_argument('-p','--port',help='single port to try',default=22,type=int)
    p.add_argument('-s','--service',help='string to match to qualify detections',default='ssh')
    p.add_argument('-t','--timeout',help='timeout to wait for server',default=0.1,type=float)
    p.add_argument('-b','--baseip',help='instead of using own IP, set a specific subnet to scan')
    p = p.parse_args()

    tic = time()
    ownip = getLANip() if not p.baseip else p.baseip
    print('own address ' + str(ownip))
    servers = scanhosts(ownip,p.port,p.service,p.timeout)
    print('found {} {} server IPs in {:.1f} seconds: \n'.format(
                         len(servers),p.service,time()-tic)+str(servers))
