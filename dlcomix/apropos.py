#/usr/bin/env python
# -*- coding: utf-8 -*-

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

"""
About Dialog window Class
Show the About DLComix Window
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys
from Gui import apropos_ui

class Apropos(QWidget, apropos_ui.Ui_Form):
     def __init__(self):
        QWidget.__init__(self)
        apropos_ui.Ui_Form.__init__(self)
        Dialog_Apropos = QDialog()
        self.setupUi(Dialog_Apropos)
        Dialog_Apropos.exec_()
