#!/usr/bin/python
# *-* coding: utf-8 *-*

import os,  re
import sqlite3

class Sqlite(object):

    def __init__(self, path=None):
        self.sqliteFile = os.path.expanduser ('~')+'/.dlcomix/dlcomix.sqlite'


    def initialise_sqlite(self):
        print "Initialisation de la base de données"
        self.connect()
        self.c.execute('''create table if not exists dl_rule(comic text, data text)''')
        self.c.execute('''create table if not exists mangas(name text, url text)''')
        self.c.execute('''create table if not exists comics(name text, url text)''')
        self.c.execute('''create table if not exists preferences(table_ref text, name text)''')
        self.c.execute('''create table if not exists glob_prefs(param text, value text)''')
        self.c.execute('''select * from glob_prefs where param="full"''')
        row = self.c.fetchall()
        if not row:
            path = os.path.expanduser ('~')+'/.dlcomix'
            self.c.execute('''insert into glob_prefs values (?,?)''', ("full", "false"))
            self.c.execute('''insert into glob_prefs values (?,?)''', ("archive","false"))
            self.c.execute('''insert into glob_prefs values (?,?)''', ("optimise", "false"))
            self.c.execute('''insert into glob_prefs values (?,?)''', ("path", path))
            self.conn.commit()
        self.c.close()
        print "Tables créées avec succès"




    def connect(self):
        self.conn = sqlite3.connect(self.sqliteFile)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

