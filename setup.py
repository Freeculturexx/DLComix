#!/usr/bin/python
# *-* coding: utf-8 *-*

from setuptools import setup
import sys
import sqlite3
from dlcomix import settings

requires = ['docutils']
if sys.version_info < (2,7):
    requires.append('argparse')

setup(
     name = "dlcomix",
     version = '0.2.1',
     url = 'http://freeculture.homelinux.com/pages/Comix',
     author = "Guillaume LAME",
     description = "A small application to download comix on the web",
     include_package_data = True,
     packages = ['dlcomix'],
     install_requires = requires,
     scripts = ['bin/dlcomix'],
     classifiers = ['Development Status :: 1 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
     )

