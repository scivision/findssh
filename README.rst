=======
findssh
=======
Python script that finds SSH servers (or other services with open ports) on the local subnet, WITHOUT NMAP

Checks the string from the server to attempt to verify the correct service has been found.

Takes about 40 seconds on Linux or Windows. Tested with Python 2.7 & 3.5

Example
=======
::

  python findssh.py

Future
======
consider non-blocking/threading
