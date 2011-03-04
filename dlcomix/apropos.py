# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'apropos.ui'
#
# Created: Mon Feb 28 18:18:29 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from apropos_ui import Ui_Form

class Apropos(QWidget, Ui_Form):
     def __init__(self):
        QWidget.__init__(self)
        Ui_Form.__init__(self)
        Dialog_Apropos = QDialog()
        self.setupUi(Dialog_Apropos)
        Dialog_Apropos.exec_()
