"""
scans own LAN subnet for SSH servers on Port 22.
Useful for machines that don't/can't have NMAP installed (e.g. Windows)
Yes this can be done simply via Linux shell, but I wanted to make it as cross-platform as possible
where the user would have only basic Python installed (Windows)

Michael Hirsch
"""
from __future__ import division
import socket
#
PORT=22
TIMEOUT=0.15 #seconds
#%% (1) get LAN IP of laptop
# ref: http://stackoverflow.com/a/23822431
def getLANip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

laptopIP = getLANip()
print('detected laptop IPv4 ' + str(laptopIP)) #str() in case of None
#%% (2) scan own subnet for SSH servers
def isportopen(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT) #seconds
    try:
        s.connect((host,port))
        s.close()
    except socket.timeout:
        return
    except ConnectionRefusedError:
        return True

base = laptopIP.rsplit('.',1)[0]
tail = range(1,255)
servers = []
print('searching {}.*'.format(base))
for t in tail:
    host = '.'.join((base,str(t)))
    if isportopen(host,PORT):
        servers.append(host)
        print('found {} on port {}'.format(host,PORT))
    if not t % 10:
        print('{:.1f} % done, {} servers detected on port {}'.format(t/255*100.,len(servers),PORT))

print('found SSH server IPs: \n'+str(servers))