#!/usr/bin/python
# *-* coding: utf-8 *-*

from PyQt4.QtGui import *
import dlcomix, sys

def main(args):
    a = QApplication(args)

    fenetre = dlcomix.DLComix()
    fenetre.show()
    r=a.exec_()
    return r

if __name__ == "__main__":
    main(sys.argv)
