.. image:: https://travis-ci.org/scivision/findssh.svg?branch=master
    :target: https://travis-ci.org/scivision/findssh

.. image:: https://coveralls.io/repos/github/scivision/findssh/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/findssh?branch=master

.. image:: https://api.codeclimate.com/v1/badges/c7409d3c78d12c3df14b/maintainability
   :target: https://codeclimate.com/github/scivision/findssh/maintainability
   :alt: Maintainability

=======
findssh
=======
Platform-independent Python &ge; 3.3 script that finds SSH servers (or other services with open ports) on an IPv4 subnet, WITHOUT NMAP.

:author: Michael Hirsch, Ph.D.

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
Blocker for Python &lt; 3.3 is that ``pip install ipaddress`` doesn't currently have a context manager.
