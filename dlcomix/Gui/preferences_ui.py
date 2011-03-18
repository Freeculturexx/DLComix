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

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(700, 300)
        Dialog.setModal(False)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(360, 10, 311, 221))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.radioButton = QtGui.QRadioButton(self.tab)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 108, 22))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtGui.QRadioButton(self.tab)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 50, 108, 22))
        self.radioButton_2.setObjectName("radioButton_2")
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setGeometry(QtCore.QRect(10, 80, 291, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.pushButton_3 = QtGui.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 130, 101, 27))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setEnabled(True)
        self.tab_2.setObjectName("tab_2")
        self.radioButton_3 = QtGui.QRadioButton(self.tab_2)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 20, 108, 22))
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtGui.QRadioButton(self.tab_2)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 50, 108, 22))
        self.radioButton_4.setObjectName("radioButton_4")
        self.comboBox_2 = QtGui.QComboBox(self.tab_2)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 80, 291, 27))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton_4 = QtGui.QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(110, 130, 101, 27))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 311, 251))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_5 = QtGui.QPushButton(self.groupBox)
        self.pushButton_5.setGeometry(QtCore.QRect(70, 220, 92, 27))
        self.pushButton_5.setObjectName("pushButton_5")
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(0, 40, 191, 22))
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(0, 70, 191, 22))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(0, 100, 231, 22))
        self.checkBox_3.setObjectName("checkBox_3")
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(0, 130, 291, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(580, 260, 92, 27))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Préférences", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("Dialog", "Comic", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("Dialog", "Manga", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Dialog", "Ajouter", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Ajouter", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_3.setText(QtGui.QApplication.translate("Dialog", "Comic", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_4.setText(QtGui.QApplication.translate("Dialog", "Manga", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Dialog", "Supprimer", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Supprimer", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Paramètres globaux", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("Dialog", "Mettre à jour", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Dialog", "Téléchargement intégral", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("Dialog", "Créer des archives", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("Dialog", "Optimiser le nom des archives", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Choisir le répertoire de téléchargement", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))

