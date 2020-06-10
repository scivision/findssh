#!/usr/bin/env python
import pytest
import subprocess
import shutil

matlab = shutil.which("matlab")


@pytest.mark.skipif(matlab is None, reason="Matlab not found")
def test_matlab():
    no_python = subprocess.run(
        [matlab, "-batch", "exit(isempty(pyversion))"], timeout=60
    ).returncode

    if no_python:
        pytest.skip("python not setup in Matlab")

    ret = subprocess.check_output(
        [matlab, "-batch", "findssh"], universal_newlines=True, timeout=60
    )
    print(ret)


if __name__ == "__main__":
    pytest.main(["-s", __file__])
