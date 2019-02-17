#!/usr/bin/env python
import pytest
import subprocess
import findssh
import findssh.threadpool
import ipaddress as ip


def test_script():
    try:
        subprocess.check_call(['findssh'])
    except FileNotFoundError:
        pytest.skip('script not installed in PATH')


def test_coroutine():
    servers = findssh.main()
    try:
        assert isinstance(servers[0], ip.IPv4Address)
    except IndexError:
        pytest.xfail('no servers found')


def test_threadpool():
    servers = findssh.threadpool.main()
    try:
        assert isinstance(servers[0], ip.IPv4Address)
    except IndexError:
        pytest.xfail('no servers found')


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
