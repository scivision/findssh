#!/usr/bin/env python
"""
scans own LAN subnet for SSH servers on Port 22.
Useful for machines that don't/can't have NMAP installed (e.g. Windows)
Yes this can be done simply via Linux shell, but I wanted to make it as cross-platform as possible
where the user would have only basic Python installed (Windows)

Michael Hirsch
"""
from __future__ import division
from time import time
import socket
SERVICE='ssh' #try to match this string in server response
#%% (1) get LAN IP of laptop
# ref: http://stackoverflow.com/a/23822431
def getLANip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]
#%% (2) scan own subnet for SSH servers
def isportopen(host,port,timeout=0.15):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout) #seconds
    try:
        s.connect((host,port))
        r=s.recv(32).decode('utf8') #arbitrary number of bytes
        print(r)
        s.close()
    except (OSError,socket.timeout,socket.error): #,ConnectionRefusedError
        return

    if SERVICE in r.lower():
        return True
#%% main loop
def scanhosts(ownip,port,timeout):
    """
    loops over xxx.xxx.xxx.1-254
    """
    base = ownip.rsplit('.',1)[0]
    tail = range(1,255)
    servers = []
    print('searching {}.*'.format(base))
    for t in tail:
        host = '.'.join((base,str(t)))
        if isportopen(host,port):
            servers.append(host)
            print('found {} on {} port {}'.format(SERVICE,host,port))
        if not t % 10:
            print('{:.1f} % done, {} servers detected on port {}'.format(t/255*100.,len(servers),port))
    return servers

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser('scan for hosts with open port, without NMAP')
    p.add_argument('-p','--port',help='single port to try',default=22,type=int)
    p.add_argument('-t','--timeout',help='timeout to wait for server',default=0.1,type=float)
    p.add_argument('-b','--baseip',help='instead of using own IP, set a specific subnet to scan')
    p = p.parse_args()

    tic = time()
    ownip = getLANip() if not p.baseip else p.baseip
    print('own IPv4 ' + str(ownip))
    servers = scanhosts(ownip,p.port,p.timeout)
    print('found {} {} server IPs in {:.1f} seconds: \n'.format(len(servers),SERVICE,time()-tic)+str(servers))
