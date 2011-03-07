#!/usr/bin/python
# *-* coding: utf-8 *-*

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import dlcomix, sys

def main(args):
    a = QApplication(args)
    locale = QLocale.system().name()
    qtTranslator = QTranslator()
    if  qtTranslator.load("qt_"+locale):
        app.installTranslator(qtTranslator)
    appTranslator = QTranslator()
    if appTranslator.load("LOCALE/DLComix_"+locale):
        app.installTranslator(appTranslator)

    fenetre = dlcomix.DLComix()
    fenetre.show()
    r=a.exec_()
    return r

if __name__ == "__main__":
    main(sys.argv)
