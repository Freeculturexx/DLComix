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

import apropos
import preferences
from sqlite import Sqlite
from gocomics import Gocomics
from manga import Manga
import os, re, sys, sqlite3

from dlcomix_ui import Ui_DLComix

"""
Fenetre principale de l'application
"""
class DLComix(QMainWindow, Ui_DLComix):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_DLComix.__init__(self)


        self.sqlite = Sqlite()
        self.setupUi(self)
        self.init_options()
        self.statusbar.showMessage(self.trUtf8("Prêt"))

        self.connect(self.pushButton, SIGNAL("clicked()"),
                     self.update_database)
        self.connect(self.actionQuitter, SIGNAL("triggered()"), qApp,
                     SLOT("quit()"))
        self.connect(self.actionPreferences, SIGNAL("triggered()"),
                     self.preferences)
        self.connect(self.actionA_Propos, SIGNAL("triggered()"),
                     self.apropos)
        self.connect(self.radioButton, SIGNAL("clicked()"), self.combo_comic)
        self.connect(self.radioButton_2, SIGNAL("clicked()"), self.combo_manga)
        self.connect(self.pushButton_2,  SIGNAL("clicked()"),  self.telecharger_prefs)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.telecharger)
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.init_options)

    """Appel SLOT"""
    def init_options(self):
        self.check_preferences()
        if self.full == "True":
            self.checkBox.setChecked(True)
        if self.archive == "True":
            self.checkBox_2.setChecked(True)
        if self.optimise == "True":
            self.checkBox_3.setChecked(True)

    def update_database(self):
        self.initialise_comic()
        self.initialise_manga()
        self.sqlite.c.close()

    def telecharger(self):
        if self.checkBox.isChecked():
            self.full = "True"
        else:
            self.full = "False"
        if self.checkBox_2.isChecked():
            self.archive = "True"
        else:
            self.archive = "False"
        if self.checkBox_3.isChecked():
            self.optimise = "True"
        else:
            self.optimise = "False"
        self.limit = self.spinBox.value()
        if self.radioButton_2.isChecked():
            self.sqlite.c.execute("select * from mangas where name='%s'" %
                                  self.comboBox.currentText())
            for row in self.sqlite.c:
                manga = Manga(row[0], self.path, self.archive, self.full,
                              self.optimise, row[1], self.limit)
        elif self.radioButton.isChecked():
            self.sqlite.c.execute("select * from comics where name='%s'" %
                                  self.comboBox.currentText())
            for row in self.sqlite.c:
                comic = Gocomics(row[0], self.path, self.archive, self.full,
                              self.optimise, row[1])

    def telecharger_prefs(self):
        i = 0
        self.check_preferences()
        self.limit = self.spinBox.value()
        self.sqlite.connect()
        self.sqlite.c.execute('''select * from preferences''')
        row = self.sqlite.c.fetchall()
        lenght = len(row) -1
        while i <= lenght:
            if row[i][0] == "mangas":
                self.sqlite.c.execute("select * from mangas where name='%s'" %
                                      row[i][1])
                row_2 = self.sqlite.c.fetchall()
                manga = Manga(row_2[0][0],  self.path,  self.archive,  self.full,
                              self.optimise, row_2[0][1],  self.limit )
            if row[i][0] == "comics":
                self.sqlite.c.execute("select * from comics where name='%s'" %
                                      row[i][1])
                row_2 = self.sqlite.c.fetchall()
                comic = Gocomics(row_2[0][0],  self.path,  self.archive,  self.full,
                                 self.optimise,  row_2[0][1])
            i += 1

    def combo_comic(self):
        i= 0
        self.spinBox.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        self.label.setEnabled(False)
        self.comboBox.clear()
        self.sqlite.connect()
        self.sqlite.c.execute('''select name from comics order by name''')
        row = self.sqlite.c.fetchall()
        lenght = len(row)-1
        while i <= lenght:
            self.comboBox.addItem(row[i][0])
            i += 1
        self.sqlite.c.close()

    def combo_manga(self):
        i = 0
        self.spinBox.setEnabled(True)
        self.checkBox_3.setEnabled(True)
        self.label.setEnabled(True)
        self.comboBox.clear()
        self.sqlite.connect()
        self.sqlite.c.execute('''select name from mangas order by name''')
        row = self.sqlite.c.fetchall()
        lenght = len(row)-1
        while i <= lenght:
            self.comboBox.addItem(row[i][0])
            i += 1
        self.sqlite.c.close()

    """ Fonctions tierces"""

    def check_preferences(self):
        sqliteFile = os.path.expanduser ('~')+'/.dlcomix/dlcomix.sqlite'
        if not os.path.exists(sqliteFile):
            QMessageBox.information(None,
                self.trUtf8("Information"),
                self.trUtf8("""DLComix effectue une mise a jour necessaire de la base \
                de données avant de démarrer.

Cela peut prendre un peu de temps"""))
            self.sqlite.initialise_sqlite()
            self.update_database()
        self.sqlite.connect()
        self.sqlite.c.execute('''select * from glob_prefs''')
        row = self.sqlite.c.fetchall()
        if not row:
            QMessageBox.information(None,
                self.trUtf8("Information"),
                self.trUtf8("""DLComix effectue une mise a jour necessaire de la base \
                de données avant de démarrer.

Cela peut prendre un peu de temps"""))
            self.update_database()
            self.check_preferences()
        else:
            self.full = row[0][1]
            self.archive = row[1][1]
            self.optimise = row[2][1]
            self.path = row[3][1]

    def initialise_manga(self):
        i = 0
        self.sqlite.connect()
        sys.stdout.write("Initialisation de la liste de manga")
        print "Cela peu prendre un peu de temps"
        print "Connection au serveur"
        os.system("wget -q http://99.198.113.68/manga -O /tmp/manga.html")
        files = open("/tmp/manga.html","rb")
        source = files.read()
        link = re.findall('<li><a href="(.*?)">',source)
        link.remove(link[0])
        mangaList = re.findall('"> (.*?)/</a></li>',source)
        n = len(mangaList)-1
        self.sqlite.c.execute('delete from mangas')
        while i <= n:
            if mangaList[i].count('_') > 0:
                mangaList[i] = mangaList[i].replace('_',' ')
            tmpManga = str(mangaList[i])
            linkManga = "http://99.198.113.68/manga/"+link[i]
            self.sqlite.c.execute("""insert into mangas values(?,?)""", (tmpManga,linkManga))
            i += 1
        self.sqlite.c.execute('delete from mangas where name like "Chapter-%"')
        self.sqlite.conn.commit()
        self.sqlite.c.close()
        print "Fin de l'initialisation de la liste de manga"

    def initialise_comic(self):
        i = 0
        self.sqlite.connect()
        self.sqlite.c.execute('delete from comics')
        print "Initialisation de la liste de comic"
        print "Connection au serveur"
        os.system("wget -q -O /tmp/initComic http://www.gocomics.com/features")
        self.comicList = self.parse_comic()
        self.comic_db()
        os.system("wget -q -O /tmp/initComic http://www.gocomics.com/explore/editorial_lists")
        self.comicList = self.parse_comic()
        self.comic_db()
        os.system("wget -q -O /tmp/initComic http://www.gocomics.com/explore/sherpa_list")
        self.comicList = self.parse_comic()
        self.comic_db()
        self.sqlite.c.close()
        print "Fin de l'initialisation de la liste de comic"

    def parse_comic(self):
        f = open("/tmp/initComic","rb")
        source = f.read()
        link = re.findall('<li><a href="/(.*?)" class=', source)
        name = re.findall('title="(.*?)" width="60" />', source)
        n = len(name)-1
        i =0
        while i <= n:
            name[i] = name[i].capitalize()
            name[i] = name[i].replace('é','e')
            name[i] = name[i].replace('&amp;','&')
            link[i] = ("http://www.gocomics.com/"+link[i]).decode('utf-8')
            i += 1
        os.remove("/tmp/initComic")
        return name, link

    def comic_db(self):
        n = len(self.comicList[0])-1
        i = 0
        while i <= n:
            self.sqlite.c.execute("""insert into comics values(?,?)""",
                           (self.comicList[0][i],self.comicList[1][i]))
            i += 1
        self.sqlite.conn.commit()

    """Appel de fenetres"""

    def apropos(self):
       apropos.Apropos()

    def preferences(self):
        preferences.Preferences()
