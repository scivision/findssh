#!/usr/bin/env python
import pytest
import subprocess
import findssh


def test_script():
    subprocess.check_call(['findssh'])
    

def test_mod():
    findssh.run()
    


if __name__ == '__main__':
    pytest.main(['-xv', __file__])
