# Find SSH servers (without NMAP)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3336467.svg)](https://doi.org/10.5281/zenodo.3336467)
[![Actions Status](https://github.com/scivision/findssh/workflows/ci_python/badge.svg)](https://github.com/scivision/findssh/actions)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/scivision/findssh.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/scivision/findssh/context:python)
[![PyPi versions](https://img.shields.io/pypi/pyversions/findssh.svg)](https://pypi.python.org/pypi/findssh)
[![PyPi Download stats](http://pepy.tech/badge/findssh)](http://pepy.tech/project/findssh)

Platform-independently find SSH servers (or other services with open ports) on an IPv4 subnet in pure Python WITHOUT NMAP.
Scan entire IPv4 subnet in less than 1 second using Python standard library `asyncio`  coroutines and a single thread.

The `asyncio` coroutine method uses ONE thread and is significantly *faster* than `concurrent.futures.ThreadPoolExecutor`, even (perhaps especially) with hundreds of threads in the ThreadPool.

Although speed advantages weren't seen in our testing, `findssh` works with PyPy as well.

## Install

```sh
pip install findssh
```

or from this repo:

```sh
git clone https://github.com/scivision/findssh

pip install -e findssh
```

## Usage

from command line:

```sh
findssh
```

or

```sh
python -m findssh
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
