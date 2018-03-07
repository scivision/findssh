.. image:: https://travis-ci.org/scivision/findssh.svg?branch=master
    :target: https://travis-ci.org/scivision/findssh

.. image:: https://coveralls.io/repos/github/scivision/findssh/badge.svg?branch=master
    :target: https://coveralls.io/github/scivision/findssh?branch=master

.. image:: https://ci.appveyor.com/api/projects/status/pk5ebkekh0u4q90t?svg=true
    :target: https://ci.appveyor.com/project/scivision/findssh

.. image:: https://api.codeclimate.com/v1/badges/c7409d3c78d12c3df14b/maintainability
   :target: https://codeclimate.com/github/scivision/findssh/maintainability
   :alt: Maintainability

=======
findssh
=======
Platform-independent Python >= 3.5 script that finds SSH servers (or other services with open ports) on an IPv4 subnet, WITHOUT NMAP.

:author: Michael Hirsch, Ph.D.

.. contents::

Install
=======
You can just run ``findssh.py`` directly, but to allow use from other programs, you can install by::

    pip install findssh
    
or from this repo::

    pip install -e .
    

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


    

Future
======
consider non-blocking/threading


Notes
=====
Python <= 3.2 is that ``socket`` doesn't have a context manager.
