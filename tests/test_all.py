#!/usr/bin/env python
import pytest
import subprocess
import findssh
import ipaddress as ip


def test_script():
    try:
        subprocess.check_call(['findssh'])
    except FileNotFoundError:
        pytest.skip('script not installed in PATH')


def test_mod():
    servers = findssh.run()
    assert isinstance(servers[0], ip.IPv4Address)


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
