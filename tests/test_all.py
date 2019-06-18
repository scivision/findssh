#!/usr/bin/env python
import pytest
import subprocess
import findssh
import findssh.threadpool
import ipaddress as ip

PORT = 22
SERVICE = ''
TIMEOUT = 1.0


def test_script():
    subprocess.check_call(['findssh'])


@pytest.mark.asyncio
async def test_coroutine():
    net = findssh.netfromaddress(findssh.getLANip())
    hosts = [host async for host in findssh.main(net, PORT, SERVICE, TIMEOUT)]
    if len(hosts) > 0:
        assert isinstance(hosts[0], ip.IPv4Address)


def test_threadpool():
    servers = findssh.threadpool.main(None, PORT, SERVICE, TIMEOUT)
    try:
        assert isinstance(servers[0], ip.IPv4Address)
    except IndexError:
        pytest.xfail('no servers found')


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
