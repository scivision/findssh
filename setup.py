#!/usr/bin/env python
from setuptools import setup, find_packages
install_requires = []
tests_require = ['pytest', 'coveralls', 'flake8', 'mypy']
# %%

setup(name='findssh',
      packages=find_packages(),
      version='1.0.5',
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/findssh',
      long_description=open('README.rst').read(),
      description='find open servers on your IPv4 subnet, e.g. SSH.',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests': tests_require},
      python_requires='>=3.6',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: System :: Networking',
          'Topic :: Utilities',
      ],
      scripts=['findssh.py'],
      include_package_data=True,
      )
