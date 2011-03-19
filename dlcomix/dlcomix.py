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
import urllib2

import apropos
import preferences
from sqlite import Sqlite
from gocomics import Gocomics
from manga import Manga
import os, re, sys, sqlite3
from Gui import  dlcomix_ui


"""
Main Window of DLComix
"""
class DLComix(QMainWindow, dlcomix_ui.Ui_DLComix):

    def __init__(self):
        QMainWindow.__init__(self)
        dlcomix_ui.Ui_DLComix.__init__(self)

        self.headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)' }

        self.sqlite = Sqlite()
        self.setupUi(self)
        self.init_options()
        self.statusbar.showMessage(self.trUtf8("Prêt"))


        """ Configuration SLOT"""
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


    def init_options(self):
        """ Look for  preferences in database and check the checkBox with available options  """
        self.check_preferences()
        if self.full == "True":
            self.checkBox.setChecked(True)
        if self.archive == "True":
            self.checkBox_2.setChecked(True)
        if self.optimise == "True":
            self.checkBox_3.setChecked(True)
        if self.pdf == "True":
            self.checkBox_4.setChecked(True)

    def update_database(self):
        """ Update database with available comics and mangas"""
        self.initialise_comic()
        self.initialise_manga()
        self.sqlite.c.close()

    def telecharger(self):
        """ Make a download of the comic/manga selected in the main window """

        """ Define preferences"""
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
        if self.checkBox_4.isChecked():
            self.pdf = "True"

        self.sqlite.connect()
        """ Define if target is Manga or Comic and launch appropriate Class"""
        if self.radioButton_2.isChecked():
            self.sqlite.c.execute("select * from mangas where name='%s'" %
                                  self.comboBox.currentText())
            for row in self.sqlite.c:
                manga = Manga(row[0], self.path, self.archive, self.full,
                              self.optimise, row[1],  self.pdf)
        elif self.radioButton.isChecked():
            self.sqlite.c.execute("select * from comics where name='%s'" %
                                  self.comboBox.currentText())
            for row in self.sqlite.c:
                comic = Gocomics(row[0], self.path, self.archive, self.full,
                              self.optimise, row[1])
        elif not self.radioButton.isChecked() and not self.radioButton_2.isChecked():
            QMessageBox.warning(None,
                self.trUtf8("Téléchargement"),
                self.trUtf8("""Veuillez sélectionner un manga ou comic avant de lancer le téléchargement"""))
        self.sqlite.c.close()


    def telecharger_prefs(self):
        """ Launch download of manga/comic recorded in preferences"""
        i = 0
        self.check_preferences()
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
                              self.optimise, row_2[0][1],  self.pdf )
            if row[i][0] == "comics":
                self.sqlite.c.execute("select * from comics where name='%s'" %
                                      row[i][1])
                row_2 = self.sqlite.c.fetchall()
                comic = Gocomics(row_2[0][0],  self.path,  self.archive,  self.full,
                                 self.optimise,  row_2[0][1])
            i += 1
        if not row:
            msgPreferences = QMessageBox.question(None,
                self.trUtf8("Téléchargement"),
                self.trUtf8("""Vous n'avez par encore ajouté de comics ou mangas dans les préférences

Souhaitez vous le faire maintenant ?"""),
                QMessageBox.StandardButtons(\
                    QMessageBox.No | \
                    QMessageBox.Yes))
            if (msgPreferences == QMessageBox.Yes):
                self.preferences()
        self.sqlite.c.close()


    def combo_comic(self):
        """ Generate the Comic List in the comboBox"""
        i= 0
        self.checkBox_3.setEnabled(False)
        self.checkBox_4.setEnabled(False)
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
        """ Generate the Manga list in ComboBox"""
        i = 0
        self.checkBox_3.setEnabled(True)
        self.checkBox_4.setEnabled(True)
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
        """ Select Preferences in database"""

        """ Look if database exist. If not, initialise it"""
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
            if len(row)<5:
                self.sqlite.c.execute('''insert into glob_prefs values (?,?)''',
                                      ("pdf","false"))
                self.sqlite.conn.commit()
                self.pdf = "False"
            else:
                self.pdf = row[4][1]
        self.sqlite.c.close()

    def initialise_manga(self):
        """ Initialise the manga list in the database"""
        i = 0
        self.sqlite.connect()
        print ("Initialisation de la liste de manga").decode('utf-8')
        print ("Cela peu prendre un peu de temps").decode('utf-8')
        print ("Connection au serveur").decode('utf-8')
        req = urllib2.Request('http://99.198.113.68/manga', headers = self.headers)
        response = urllib2.urlopen(req)
        source = response.read()
        link = re.findall('<li><a href="(.*?)">',source)
        link.remove(link[0])
        n = len(link)-1
        while i <= n:
            if link[i].count('.jpg')>0:
                link.remove(link[i])
                n -= 1
                i -= 1
            i += 1
        mangaList = re.findall('"> (.*?)/</a></li>',source)
        n = len(mangaList)-1
        self.sqlite.c.execute('delete from mangas')
        i= 0
        while i <= n:
            if mangaList[i].count('_') > 0:
                mangaList[i] = mangaList[i].replace('_',' ')
            tmpManga = str(mangaList[i])
            linkManga = "http://99.198.113.68/manga/"+link[i]
            self.sqlite.c.execute("""insert into mangas values(?,?)""", (tmpManga,linkManga))
            i += 1
        """ TODO : make an update an not a complete insertion to purpose a new manga window"""
        self.sqlite.c.execute('delete from mangas where name like "Chapter-%"')
        self.sqlite.conn.commit()
        self.sqlite.c.close()
        print ("Fin de l'initialisation de la liste de manga").decode('utf-8')

    def initialise_comic(self):
        """ Initialise comic list in database"""
        i = 0
        self.sqlite.connect()
        """ TODO : make an update an not a complete insertion to purpose a new comic window"""
        self.sqlite.c.execute('delete from comics')
        print ("Initialisation de la liste de comic").decode('utf-8')
        print ("Connection au serveur").decode('utf-8')
        req = urllib2.Request('http://www.gocomics.com/features',  headers = self.headers)
        response = urllib2.urlopen(req)
        self.comicList = self.parse_comic(response)
        self.comic_db()
        req = urllib2.Request('http://www.gocomics.com/explore/editorial_lists',  headers = self.headers)
        response = urllib2.urlopen(req)
        self.comicList = self.parse_comic(response)
        self.comic_db()
        req = urllib2.Request('http://www.gocomics.com/explore/sherpa_list',  headers = self.headers)
        response = urllib2.urlopen(req)
        self.comicList = self.parse_comic(response)
        self.comic_db()
        self.sqlite.c.close()
        print ("Fin de l'initialisation de la liste de comic").decode('utf-8')

    def parse_comic(self,  response):
        """ Parse gocomics html page to get necessary informations"""
        source = response.read()
        test = re.findall('<a href="/(.*?)" class="alpha_list updated">(.*?)</a>', source)
        name = ['']*len(test)
        link = ['']*len(test)
        for i in range (0, len(test)):
            name[i] = test[i][1].decode('utf-8').capitalize()
            lk = (test[i][0]).replace(' ','')
            link[i] = ("http://www.gocomics.com/"+lk).decode('utf-8')
        return name, link

    def comic_db(self):
        """ Insert comic list in database"""
        n = len(self.comicList[0])-1
        i = 0
        while i <= n:
            self.sqlite.c.execute("""insert into comics values(?,?)""",
                           (self.comicList[0][i],self.comicList[1][i]))
            i += 1
        self.sqlite.conn.commit()

    """Appel de fenetres"""

    def apropos(self):
        """ Call About window"""
        apropos.Apropos()

    def preferences(self):
        """ Call preferences window"""
        preferences.Preferences()
