[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1431634.svg)](https://doi.org/10.5281/zenodo.1431634)
[![Travis-CI status](https://travis-ci.org/scivision/findssh.svg?branch=master)](https://travis-ci.org/scivision/findssh)
[![Coverage percent](https://coveralls.io/repos/github/scivision/findssh/badge.svg?branch=master)](https://coveralls.io/github/scivision/findssh?branch=master)
[![AppVeyor-CI status](https://ci.appveyor.com/api/projects/status/pk5ebkekh0u4q90t?svg=true)](https://ci.appveyor.com/project/scivision/findssh)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/scivision/findssh.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/scivision/findssh/context:python)
[![PyPi versions](https://img.shields.io/pypi/pyversions/findssh.svg)](https://pypi.python.org/pypi/findssh)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7409d3c78d12c3df14b/maintainability)](https://codeclimate.com/github/scivision/findssh/maintainability)
[![PyPi Download stats](http://pepy.tech/badge/findssh)](http://pepy.tech/project/findssh)

# Find SSH servers (without NMAP)

Platform-independently find SSH servers (or other services with open ports) on an IPv4 subnet, WITHOUT NMAP.
Scan entire IPv4 subnet in less than 1 second using Python standard library `asyncio`  coroutines and a single thread.

The `asyncio` coroutine method uses ONE thread and is significantly *faster* than `concurrent.futures.ThreadPoolExecutor`, even (perhaps especially) with hundreds of threads in the ThreadPool.

Although speed advantages weren't seen in our testing, `findssh` works with PyPy as well.

Matlab `findssh.m` works similarly.

## Install

Just run `FindSSH.py` directly.
To allow use from other programs, you can install by:

    pip install findssh

or from this repo:

    pip install -e .


## Usage

from command line:
```sh
findssh
```


### Command line options

* `-s`  check the string from the server to attempt to verify the correct service has been found
* `-t` timeout per server (seconds)  useful for high latency connection
* `-b` baseip (check other subnet besides your own)
* `-p` network port to scan (default 22)

## Benchmark

These tests used 500 ms timeout on WiFi.

Coroutine (single thread, fast, lean, recommended):

```ipython
%timeit findssh.main()

522 ms ± 1.26 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

Thread pool (100 thread max, slow, heavy):

```ipython
%timeit findssh.threadpool.main()

1.39 s ± 213 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```
