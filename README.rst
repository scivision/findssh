.. image:: https://travis-ci.org/scienceopen/findssh.svg?branch=master
    :target: https://travis-ci.org/scienceopen/findssh

=======
findssh
=======
Platform-independent Python >= 3.3 script that finds SSH servers (or other services with open ports) on an IPv4 subnet, WITHOUT NMAP.

.. contents::


Options
=======

-s  checks the string from the server to attempt to verify the correct service has been found.
-t  timeout 
-b  baseip (check other subnet besides your own)
-p  port

Takes about 40 seconds to scan an IPv4 subnet.

Example
=======
::

  python findssh.py

Future
======
consider non-blocking/threading


Notes
=====
Blocker for Python < 3.3 is that ``pip install ipaddress`` doesn't currently have a context manager.
