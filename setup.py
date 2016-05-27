#!/usr/bin/env python
from setuptools import setup

with open('README.rst','r') as f:
    long_description = f.read()

with open('requirements.txt','r') as f:
    req = f.read().splitlines()

setup(name='findssh',
      version='0.1',
	    description='find servers with open ports without nmap',
	    long_description=long_description,
	    author='Michael Hirsch',
	    url='https://github.com/scienceopen/findssh',
      dependency_links = [],
	  install_requires=[req],
      packages=[],
	  )
