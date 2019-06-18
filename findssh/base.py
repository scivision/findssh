import ipaddress as ip
import socket


def getLANip() -> ip.IPv4Address:
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


def validateservice(service: str, h: str, b: bytes) -> bool:
    if not b:  # empty reply
        return False
# %% non-empty reply
    """
    splitlines is in case the ASCII/UTF8 response is less than 32 bytes,
    hoping server sends a \r\n
    """
    u = b.splitlines()[0].decode('utf-8', 'ignore')
    print('\n', u)


# %% optional service validation
    val = True
    if service and service not in u.lower():
        val = False

    return val


def netfromaddress(addr: ip.IPv4Address) -> ip.IPv4Network:

    return ip.ip_network(addr.exploded.rsplit('.', 1)[0]+'.0/24')
