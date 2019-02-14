[![Travis-CI status](https://travis-ci.org/scivision/findssh.svg?branch=master)](https://travis-ci.org/scivision/findssh)
[![Coverage percent](https://coveralls.io/repos/github/scivision/findssh/badge.svg?branch=master)](https://coveralls.io/github/scivision/findssh?branch=master)
[![AppVeyor-CI status](https://ci.appveyor.com/api/projects/status/pk5ebkekh0u4q90t?svg=true)](https://ci.appveyor.com/project/scivision/findssh)
[![PyPi versions](https://img.shields.io/pypi/pyversions/findssh.svg)](https://pypi.python.org/pypi/findssh)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7409d3c78d12c3df14b/maintainability)](https://codeclimate.com/github/scivision/findssh/maintainability)
[![PyPi Download stats](http://pepy.tech/badge/findssh)](http://pepy.tech/project/findssh)

# Find SSH servers (without NMAP)

Platform-independently find SSH servers (or other services with open ports) on an IPv4 subnet, WITHOUT NMAP.
Scans entire IPv4 subnet in less than 1 second using 100 threads via Python standard library
[concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html).

Although speed advantages weren't seen in our testing, `findssh` works with PyPy as well.

Matlab `findssh.m` works similarly.

## Install

Just run `findssh.py` directly.
To allow use from other programs, you can install by:

    pip install findssh

or from this repo:

    pip install -e .


## Usage

    findssh

or from within Python

```python
import findssh

findssh.run()
```

### Command line options

* `-s`  check the string from the server to attempt to verify the correct service has been found
* `-t` timeout per server (seconds)  useful for high latency connection
* `-b` baseip (check other subnet besides your own) 
* `-p` network port to scan (default 22)
