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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import dlcomix, sys

def main(args):
    a = QApplication(args)
    locale = QLocale.system().name()
    qtTranslator = QTranslator()
    if  qtTranslator.load("qt_"+locale):
        a.installTranslator(qtTranslator)
    appTranslator = QTranslator()
    if appTranslator.load("LOCALE/DLCOMIX_"+locale+".qm"):
        a.installTranslator(appTranslator)
    else:
        appTranslator.load("LOCALE/DLCOMIX_en_US")
        a.installTranslator(appTranslator)
    fenetre = dlcomix.DLComix()
    fenetre.show()
    r=a.exec_()
    return r

if __name__ == "__main__":
    main(sys.argv)
