.. image:: https://travis-ci.org/scivision/findssh.svg?branch=master
    :target: https://travis-ci.org/scivision/findssh

.. image:: https://coveralls.io/repos/github/scivision/findssh/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/findssh?branch=master

.. image:: https://ci.appveyor.com/api/projects/status/pk5ebkekh0u4q90t?svg=true
    :target: https://ci.appveyor.com/project/scivision/findssh

.. image:: https://img.shields.io/pypi/pyversions/findssh.svg
  :target: https://pypi.python.org/pypi/findssh
  :alt: Python versions (PyPI)

.. image::  https://img.shields.io/pypi/format/findssh.svg
  :target: https://pypi.python.org/pypi/findssh
  :alt: Distribution format (PyPI)

.. image:: https://api.codeclimate.com/v1/badges/c7409d3c78d12c3df14b/maintainability
   :target: https://codeclimate.com/github/scivision/findssh/maintainability
   :alt: Maintainability
   
.. image:: http://pepy.tech/badge/findssh
   :target: http://pepy.tech/project/findssh
   :alt: PyPi Download stats

=======
findssh
=======
Platform-independent **Python >= 3.6** script that finds SSH servers (or other services with open ports) on an IPv4 subnet, WITHOUT NMAP.
Scans entire IPv4 subnet in less than 1 second using 100 threads via Python standard library
`concurrent.futures <https://docs.python.org/3/library/concurrent.futures.html>`_.

:author: Michael Hirsch, Ph.D.


.. contents::

Install
=======
You can just run ``findssh.py`` directly, but to allow use from other programs, you can install by::

    pip install findssh

or from this repo::

    pip install -e .
    
It is expected that your default `python` version is at least 3.5, which was released in 2015.


Usage
=======
Takes about 40 seconds to scan an IPv4 subnet.

from Terminal::

  python findssh.py

or from within Python

.. code:: python

    import findssh

    findssh.run()


Command line options
---------------------

-s  checks the string from the server to attempt to verify the correct service has been found.
-t  timeout
-b  baseip (check other subnet besides your own)
-p  port

