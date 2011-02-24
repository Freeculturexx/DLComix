#!/usr/bin/python
# *-* coding: utf-8 *-*

import os
import re
import sqlite3
import settings

class Sqlite(object):

    def __init__(self, path=None):
        self.sqliteFile = os.path.expanduser ('~')+'/.dlcomix/dlcomix.sqlite'
        if not os.path.exists(self.sqliteFile):
            self.initialise_sqlite()

    def initialise_sqlite(self):
        print "Initialisation de la base de données"
        self.connect()
        self.c.execute('''create table if not exists dl_rule(comic text, data text)''')
        self.c.execute('''create table if not exists mangas(name text, url text)''')
        self.c.execute('''create table if not exists comics(id text, name text, url text)''')
        self.c.close()
        print "Tables créées avec succès"
        self.initialise_manga()
        self.initialise_comic()

    def initialise_manga(self):
        i = 0
        self.connect()
        print "Initialisation de la liste de manga"
        print "Cela peu prendre un peu de temps"
        print "Connection au serveur"
        os.system("wget -q http://99.198.113.68/manga -O /tmp/manga.html")
        files = open("/tmp/manga.html","rb")
        source = files.read()
        link = re.findall('<li><a href="(.*?)">',source)
        link.remove(link[0])
        mangaList = re.findall('"> (.*?)/</a></li>',source)
        n = len(mangaList)-1
        self.c.execute('delete from mangas')
        while i <= n:
            if mangaList[i].count('_') > 0:
                mangaList[i] = mangaList[i].replace('_','-')
            tmpManga = str(mangaList[i].lower())
            linkManga = "http://99.198.113.68/manga/"+link[i]
            self.c.execute("""insert into mangas values(?,?)""", (tmpManga,linkManga))
            i += 1
        self.c.execute('delete from mangas where name like "Chapter-%"')
        self.conn.commit()
        self.c.close
        print "Fin de l'initialisation de la liste de manga"

    def initialise_comic(self):
        i = 0
        self.connect()
        self.c.execute('delete from comics')
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
        self.c.close
        print "Fin de l'initialisation de la liste de comic"

    def parse_comic(self):
        f = open("/tmp/initComic","rb")
        source = f.read()
        link = re.findall('<li><a href="/(.*?)" class=', source)
        name = re.findall('title="(.*?)" width="60" />', source)
        n = len(name)-1
        i =0
        while i <= n:
            name[i] = link[i]
            link[i] = "http://www.gocomics.com/"+link[i]
            i += 1
     	os.remove("/tmp/initComic")
      	return name, link
 
    def comic_db(self):
        n = len(self.comicList[0])-1
        i = 0
        while i <= n:
            self.c.execute("""insert into comics values(?,?)""", 
				(self.comicList[0][i],self.comicList[1][i]))
            i += 1
        self.conn.commit()

    def connect(self):
        self.conn = sqlite3.connect(self.sqliteFile)
	self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

