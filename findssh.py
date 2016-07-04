#!/usr/bin/env python
"""
scans IPv4 subnet for SSH servers on Port 22 or other server ports.
Useful for machines that don't/can't have NMAP installed (e.g. Windows), and device does not have Avahi server.
Yes this can be done simply via Linux shell, but I wanted to make it as cross-platform as possible
where the user would have only basic Python installed (Windows)

Michael Hirsch

Note: timeout value bare minimum is 0.15 seconds for LAN, suggest using higher values say 0.25 or 0.35 if you can stand the wait 254*0.35 seconds

"""
from time import time
import socket
from ipaddress import ip_address,ip_network,IPv4Network

#%% (1) get LAN IP of laptop
def getLANip():
    """ get IP of own interface
     ref: http://stackoverflow.com/a/23822431
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # don't use link local here (169.254.x.x) unless you have a specific need
        try:
            s.connect(('<broadcast>', 0))
        except OSError:
            s.connect(('8.8.8.8',80)) # for BSD/Mac
        name = s.getsockname()[0]
    
    return ip_address(name.encode('utf-8').decode('utf-8')) #encode.decode is used for python2 and python3 compatibility

#%% (2) scan subnet for SSH servers
def isportopen(host,port,service,timeout=0.3):
    h = host.exploded
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout) #seconds
        try:
            s.connect((h,port))
            b=s.recv(32) #arbitrary number of bytes
#%% service decode (optional)
            return validateservice(service,h,b)

        except (ConnectionRefusedError,socket.timeout,socket.error):
            return

def validateservice(service,h,b):
    if not b: #empty reply
        return
#%% non-empty reply
    try:
        u = b.splitlines()[0].decode('utf-8') #splitlines is in case the ASCII/UTF8 response is less than 32 bytes, hoping server sends a \r\n
    except UnicodeDecodeError: # must not have been utf8 encoding..., maybe latin1 or something else..
        u = b

    print(u)
#%% optional service validation
    if service:
        try:
            if service in u.lower():
                return True
        except UnicodeDecodeError:
            print('unable to decode {} response'.format(h))
            return
    else:
        return True

def netfromaddress(addr):
    addr = ip_address(addr) #in case it's string
    if addr.version == 4:
        return ip_network(addr.exploded.rsplit('.',1)[0]+'.0/24')
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

    if net.version != 4:
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
    p.add_argument('-s','--service',help='string to match to qualify detections',default='')
    p.add_argument('-t','--timeout',help='timeout to wait for server',default=0.3,type=float)
    p.add_argument('-b','--baseip',help='instead of using own IP, set a specific subnet to scan')
    p = p.parse_args()

    tic = time()
    if not p.baseip:
        ownip = getLANip()
        print('own address ' + str(ownip))
    else:
        ownip = p.baseip

    servers = scanhosts(ownip,p.port,p.service,p.timeout)
    print('\n*** RESULTS ***\n')
    print('found {} {} server IPs in {:.1f} seconds: \n'.format(
                         len(servers),p.service,time()-tic)+str(servers))
