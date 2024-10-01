# Find SSH servers (without NMAP)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3336467.svg)](https://doi.org/10.5281/zenodo.3336467)
[![ci](https://github.com/scivision/findssh/actions/workflows/ci.yml/badge.svg)](https://github.com/scivision/findssh/actions/workflows/ci.yml)
[![PyPI Download stats](http://pepy.tech/badge/findssh)](http://pepy.tech/project/findssh)

Platform-independently find SSH servers (or other services with open ports) on an IPv4 subnet in pure Python WITHOUT NMAP.
Scan entire IPv4 subnet in less than 1 second using Python standard library `asyncio`  coroutines and a single thread.

The default
[asyncio coroutine](https://docs.python.org/3/library/asyncio.html)
uses a single thread and is more than 10x faster than
[concurrent.futures.ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html).

Although speed advantages weren't seen in our testing, `findssh` works with PyPy as well.

```sh
pip install findssh
```

or from this repo:

```sh
git clone https://github.com/scivision/findssh

pip install -e findssh
```

## Usage

A canonical way to use FindSSH from other Python scripts is [asyncio](example/asyncio_get_hosts.py).

---

from command line:

```sh
python -m findssh
```

or use project script e.g. from [pipx](https://github.com/pypa/pipx):

```sh
findssh
```

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

Trying to open too many threads via ThreadPoolExecutor can cause a system error like

```
OSError: [Errno 24] Too many open files
```

Thus in practical terms, using coroutines can be significantly faster than threads while using less system resources.
