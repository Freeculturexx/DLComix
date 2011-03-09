#!/usr/bin/python
# *-* coding: utf-8 *-*

"""
This file is part of DLComix.

    DLComix is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    DLComix is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DLComix.  If not, see <http://www.gnu.org/licenses/>.

"""

from setuptools import setup
import sys

requires = []
if sys.version_info < (2,7):
    requires.append('argparse')

setup(
     name = "dlcomix",
     version = '0.3',
     url = 'http://freeculture.homelinux.com/pages/documentation-de-dlcomix.html',
     author = "Guillaume LAME",
     description = "A small application to download comix on the web",
     include_package_data = True,
     packages = ['dlcomix', 'Gui'],
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
