# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlcomix_ui.ui'
#
# Created: Sat Mar 19 22:14:46 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DLComix(object):
    def setupUi(self, DLComix):
        DLComix.setObjectName(_fromUtf8("DLComix"))
        DLComix.resize(825, 468)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../../usr/share/pixmaps/dlcomix.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DLComix.setWindowIcon(icon)
        DLComix.setIconSize(QtCore.QSize(48, 48))
        self.centralwidget = QtGui.QWidget(DLComix)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 40, 231, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 80, 231, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(330, 0, 551, 421))
        self.groupBox.setAcceptDrops(False)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(60, 110, 301, 25))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.comboBox.setBaseSize(QtCore.QSize(0, 0))
        self.comboBox.setEditable(False)
        self.comboBox.setMaxCount(20000)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(50, 30, 104, 21))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(50, 60, 151, 21))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(50, 170, 271, 21))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(50, 200, 281, 21))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(50, 230, 251, 21))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 320, 88, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.line = QtGui.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(10, 140, 481, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(self.groupBox)
        self.line_2.setGeometry(QtCore.QRect(10, 290, 481, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(370, 210, 101, 31))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.checkBox_4 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(50, 260, 171, 22))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        DLComix.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DLComix)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 825, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFichier = QtGui.QMenu(self.menubar)
        self.menuFichier.setObjectName(_fromUtf8("menuFichier"))
        self.menuEdition = QtGui.QMenu(self.menubar)
        self.menuEdition.setObjectName(_fromUtf8("menuEdition"))
        self.menuAide = QtGui.QMenu(self.menubar)
        self.menuAide.setObjectName(_fromUtf8("menuAide"))
        DLComix.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DLComix)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DLComix.setStatusBar(self.statusbar)
        self.actionQuitter = QtGui.QAction(DLComix)
        self.actionQuitter.setObjectName(_fromUtf8("actionQuitter"))
        self.actionPreferences = QtGui.QAction(DLComix)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionA_Propos = QtGui.QAction(DLComix)
        self.actionA_Propos.setObjectName(_fromUtf8("actionA_Propos"))
        self.menuFichier.addAction(self.actionQuitter)
        self.menuEdition.addAction(self.actionPreferences)
        self.menuAide.addAction(self.actionA_Propos)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())

        self.retranslateUi(DLComix)
        QtCore.QMetaObject.connectSlotsByName(DLComix)

    def retranslateUi(self, DLComix):
        DLComix.setWindowTitle(QtGui.QApplication.translate("DLComix", "DLComix", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("DLComix", "Mettre à jour la base de données", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("DLComix", "Télécharger selon les préférences", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DLComix", "Choix du manga ou comic", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("DLComix", "Comic", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("DLComix", "Manga", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("DLComix", "Téléchargement intégral", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("DLComix", "Créer des archives", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("DLComix", "Optimiser le nom des archives", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("DLComix", "Télécharger", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("DLComix", "Réinitaliser", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_4.setText(QtGui.QApplication.translate("DLComix", "Créer des fichiers pdf", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFichier.setTitle(QtGui.QApplication.translate("DLComix", "Fichier", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdition.setTitle(QtGui.QApplication.translate("DLComix", "Edition", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAide.setTitle(QtGui.QApplication.translate("DLComix", "Aide", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuitter.setText(QtGui.QApplication.translate("DLComix", "Quitter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("DLComix", "Préférences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionA_Propos.setText(QtGui.QApplication.translate("DLComix", "A Propos", None, QtGui.QApplication.UnicodeUTF8))

