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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlite import Sqlite
import sqlite3,  sys
from Gui import preferences_ui

"""
Preferences Window of DLComix
"""
class Preferences(QDialog, preferences_ui.Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        preferences_ui.Ui_Dialog.__init__(self)
        Dialog_Preferences = QDialog()
        self.setupUi(Dialog_Preferences)

        self.sqlite = Sqlite()
        self.initialise()

        """ Configuration SLOT"""
        self.connect(self.radioButton, SIGNAL("clicked()"), self.ajouter_comic)
        self.connect(self.radioButton_2, SIGNAL("clicked()"),
                     self.ajouter_manga)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),
                     self.ajouter_sqlite)
        self.connect(self.radioButton_3, SIGNAL("clicked()"),
                     self.supprimer_comic)
        self.connect(self.radioButton_4, SIGNAL("clicked()"),
                     self.supprimer_manga)
        self.connect(self.pushButton_4, SIGNAL("clicked()"),
                     self.supprimer_sqlite)
        self.connect(self.pushButton_5, SIGNAL("clicked()"), self.update_prefs)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.choix_path)
        self.connect(self.pushButton_2,  SIGNAL("clicked()"), Dialog_Preferences.accept)

        Dialog_Preferences.exec_()

    def initialise(self):
        """ Look for preferences in database, and check CheckBox with good options"""
        self.sqlite.connect()
        self.sqlite.c.execute('''select value from glob_prefs where \
                              param="full"''')
        row = self.sqlite.c.fetchall()
        if row:
            if row[0][0] == "True":
                self.checkBox.setChecked(True)
                self.full = 1
            else:
                self.full = 0
        self.sqlite.c.execute('''select value from glob_prefs where \
                              param="archive"''')
        row = self.sqlite.c.fetchall()
        if row:
            if row[0][0] == "True":
                self.checkBox_2.setChecked(True)
                self.archive = 1
            else:
                self.archive = 0
        self.sqlite.c.execute('''select value from glob_prefs where \
                              param="optimise"''')
        row = self.sqlite.c.fetchall()
        if row:
            if row[0][0] == "True":
                self.checkBox_3.setChecked(True)
                self.optimise = 1
            else:
                self.optimise = 0
        self.sqlite.c.execute('''select value from glob_prefs where \
                              param="pdf"''')
        row = self.sqlite.c.fetchall()
        if row:
            if row[0][0] == "True":
                self.checkBox_4.setChecked(True)
                self.pdf = 1
            else:
                self.pdf = 0
        self.sqlite.c.close()

    def ajouter_comic(self):
        """ Put prefered comics in comboBox"""
        i = 0
        self.ajout = "comics"
        self.comboBox.clear()
        self.sqlite.connect()
        self.sqlite.c.execute('''select name from comics order by name''')
        row = self.sqlite.c.fetchall()
        lenght = len(row)-1
        while i <= lenght:
            item =  row[i][0]
            self.sqlite.c.execute('''select name from preferences where
                                  name="%s"''' % item)
            row_2 = self.sqlite.c.fetchall()
            if not row_2:
                self.comboBox.addItem(row[i][0])
            i += 1
        self.sqlite.c.close()

    def ajouter_manga(self):
        """ Put prefered mangas in comboBox"""
        i= 0
        self.ajout = "mangas"
        self.comboBox.clear()
        self.sqlite.connect()
        self.sqlite.c.execute('''select name from mangas order by name''')
        row = self.sqlite.c.fetchall()
        lenght = len(row)-1
        while i <= lenght:
            self.sqlite.c.execute("""select name from preferences where
                                  name='%s'""" % (row[i][0]))
            row_2 = self.sqlite.c.fetchall()
            if not row_2:
                self.comboBox.addItem(row[i][0])
            i += 1
        self.sqlite.c.close()

    def ajouter_sqlite(self):
        """ Add a comic/manga in preferences table"""
        self.sqlite.connect()
        name = (self.comboBox.currentText())
        self.sqlite.c.execute("""insert into preferences values(?,?)""",
                              (self.ajout,str(name)))
        self.sqlite.conn.commit()
        self.sqlite.c.close()
        if self.ajout == "mangas":
            self.ajouter_manga()
        else:
            self.ajouter_comic()

    def supprimer_comic(self):
        """ Delete a comic in preferences table in database"""
        i = 0
        self.comboBox_2.clear()
        self.suppression = "comics"
        self.sqlite.connect()
        self.sqlite.c.execute("""select name from preferences where \
                              table_ref='comics'""")
        row = self.sqlite.c.fetchall()
        lenght = len(row) -1
        while i<= lenght:
            self.comboBox_2.addItem(row[i][0])
            i += 1
        self.sqlite.c.close()

    def supprimer_manga(self):
        """ Delete a manga in preferences table"""
        i = 0
        self.comboBox_2.clear()
        self.suppression = "mangas"
        self.sqlite.connect()
        self.sqlite.c.execute('''select name from preferences where \
                              table_ref="mangas"''')
        row = self.sqlite.c.fetchall()
        lenght = len(row) -1
        while i<= lenght:
            self.comboBox_2.addItem(row[i][0])
            i += 1
        self.sqlite.c.close()


    def supprimer_sqlite(self):
        """ Delete a comic/manga in preference table in database"""
        self.sqlite.connect()
        item = str(self.comboBox_2.currentText())
        self.sqlite.c.execute('''delete from preferences where name="%s"''' % item)
        self.sqlite.conn.commit()
        if self.suppression == "mangas":
            self.supprimer_manga()
        else:
            self.supprimer_comic()



    def update_prefs(self):
        """ Update preferences in database"""
        self.sqlite.connect()
        if self.checkBox.isChecked():
            if self.full == 0:
                self.sqlite.c.execute('''update glob_prefs set value="True" where \
                                      param="full"''')
                self.full = 1
        else:
            if self.full == 1:
                self.sqlite.c.execute('''update glob_prefs set value="False" where \
                                      param="full"''')
                self.full = 0
        if self.checkBox_2.isChecked():
            if self.archive == 0:
                self.sqlite.c.execute('''update glob_prefs set value="True" where \
                                      param="archive"''')
                self.archive = 1
        else:
            if self.archive == 1:
                self.sqlite.c.execute('''update glob_prefs set value="False" where \
                                      param="archive"''')
                self.archive = 0
        if self.checkBox_3.isChecked():
            if self.optimise == 0:
                self.sqlite.c.execute('''update glob_prefs set value="True" where \
                                      param="optimise"''')
                self.optimise = 1
        else:
            if self.optimise == 1:
                self.sqlite.c.execute('''update glob_prefs set value="False" where \
                                      param="optimise"''')
                self.optimise = 0
        if self.checkBox_4.isChecked():
            if self.pdf == 0:
                self.sqlite.c.execute('''update glob_prefs set value="True" where \
                                      param="pdf"''')
                self.pdf = 1
        else:
            if self.pdf == 1:
                self.sqlite.c.execute('''update glob_prefs set value="False" where \
                                      param="pdf"''')
                self.pdf = 0
        self.sqlite.conn.commit()
        self.sqlite.c.close()

    def choix_path(self):
        """ Choose download path"""
        self.sqlite.connect()
        self.sqlite.c.execute('''select value from glob_prefs where \
                              param="path"''')
        row = self.sqlite.c.fetchall()
        if row:
            path = row[0][0]
        choix_path = QFileDialog.getExistingDirectory(self)
        if row:
            print str(choix_path)
            self.sqlite.c.execute('''update glob_prefs set value="%s" \
                              where param="path"''' % choix_path)
        self.sqlite.conn.commit()
        self.sqlite.c.close()



