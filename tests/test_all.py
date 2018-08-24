#!/usr/bin/env python
import pytest
import subprocess
import findssh


def test_script():
    try:
        subprocess.check_call(['findssh'])
    except FileNotFoundError:
        pytest.skip('script not installed in PATH')


def test_mod():
    findssh.run()


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
