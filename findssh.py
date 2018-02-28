#!/usr/bin/env python
"""
scans IPv4 subnet for SSH servers on Port 22 or other server ports.
Useful for machines that don't/can't have NMAP installed (e.g. Windows), and device does not have Avahi server.
Yes this can be done simply via Linux shell, but I wanted to make it as cross-platform as possible
where the user would have only basic Python installed (Windows)

Michael Hirsch, Ph.D.

Note: timeout value bare minimum is 0.15 seconds for LAN, suggest using higher values say 0.25 or 0.35 if you can stand the wait 254*0.35 seconds

"""
from time import time
import logging
import socket
from ipaddress import ip_address,ip_network,IPv4Network

TIMEOUT = 0.3
PORT=22

def run(port:int=PORT, service:str='', timeout:float=TIMEOUT, baseip:str=None):
    tic = time()
    if not baseip:
        ownip = getLANip()
        print('own address',ownip)
    else:
        ownip = baseip

    servers = scanhosts(ownip, port, service, timeout)
    print('\n*** RESULTS ***')
    print('found',len(servers), service,'server IPs in {:.1f} seconds:'.format(time()-tic))
    print('\n'.join([str(i) for i in servers]))


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

    return ip_address(name)

#%% (2) scan subnet for SSH servers
def isportopen(host:ip_address, port:int, service:str, timeout:float=TIMEOUT):
    h = host.exploded
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout) #seconds
        try:
            s.connect((h,port))
            b=s.recv(32) #arbitrary number of bytes
#%% service decode (optional)
            return validateservice(service,h,b)

        except (ConnectionRefusedError,socket.timeout,socket.error):
            logging.info('no connection to {} {}'.format(h,port))
            return

def validateservice(service:str, h:bytes, b:bytes):
    if not b: #empty reply
        return
#%% non-empty reply
    try:
        u = b.splitlines()[0].decode('utf-8') #splitlines is in case the ASCII/UTF8 response is less than 32 bytes, hoping server sends a \r\n
    except UnicodeDecodeError: # must not have been utf8 encoding..., maybe latin1 or something else..
        u = b

    print('\n',u)
#%% optional service validation
    if service:
        try:
            if service in u.lower():
                return True
        except UnicodeDecodeError:
            logging.error('unable to decode response'.format(h))
            return
    else:
        return True

def netfromaddress(addr:ip_address):
    addr = ip_address(addr) #in case it's string
    if addr.version == 4:
        return ip_network(addr.exploded.rsplit('.',1)[0]+'.0/24')
    else: #addr.version ==6
        raise NotImplementedError('https://www.6net.org/publications/standards/draft-chown-v6ops-port-scanning-implications-00.txt')

#%% main loop
def scanhosts(net:ip_network, port:int, service:str, timeout:float):
    """
    loops over xxx.xxx.xxx.1-254
    IPv4 only.
    """
    if not isinstance(net,IPv4Network):
        net = netfromaddress(net)

    if net.version != 4:
        raise NotImplementedError('https://www.6net.org/publications/standards/draft-chown-v6ops-port-scanning-implications-00.txt')


    servers = []
    print('searching',net)
    for t,a in enumerate(net.hosts()):
        if isportopen(a,port,service):
            servers.append(a)
            print('found',service,'on',a,'port',port)

        if not t % 20:
            print('{:.1f} % done'.format(t/255*100), len(servers), service,
                  'servers detected on port',port,'\r',end="",flush=True)

    return servers


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser('scan for hosts with open port, without NMAP')
    p.add_argument('-p','--port',help='single port to try',default=PORT, type=int)
    p.add_argument('-s','--service',help='string to match to qualify detections',default='')
    p.add_argument('-t','--timeout',help='timeout to wait for server',default=TIMEOUT,type=float)
    p.add_argument('-b','--baseip',help='instead of using own IP, set a specific subnet to scan')
    P = p.parse_args()

    run(p.port, p.service, p.timeout, p.baseip)
