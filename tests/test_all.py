#!/usr/bin/env python
import pytest
import subprocess


def test_all():
    subprocess.check_call(['findssh'])


if __name__ == '__main__':
    pytest.main()
