.. image:: https://travis-ci.org/scienceopen/findssh.svg?branch=master
    :target: https://travis-ci.org/scienceopen/findssh

=======
findssh
=======
Platform-independent Python script that finds SSH servers (or other services with open ports) on an IPv4 subnet, WITHOUT NMAP

Checks the string from the server to attempt to verify the correct service has been found.

Takes about 40 seconds to scan an IPv4 subnet.

Example
=======
::

  python findssh.py

Future
======
consider non-blocking/threading
