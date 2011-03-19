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

import os,  re
import sqlite3

class Sqlite(object):

    def __init__(self, path=None):
        if not os.path.isdir(os.path.expanduser ('~')+'/.dlcomix'):
            os.mkdir(os.path.expanduser ('~')+'/.dlcomix')
        self.sqliteFile = os.path.expanduser ('~')+'/.dlcomix/dlcomix.sqlite'


    def initialise_sqlite(self):
        """ Initialise database. Create it if not exists"""
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
            self.c.execute('''insert into glob_prefs values (?,?)''', ("full", "False"))
            self.c.execute('''insert into glob_prefs values (?,?)''', ("archive","False"))
            self.c.execute('''insert into glob_prefs values (?,?)''', ("optimise", "False"))
            self.c.execute('''insert into glob_prefs values (?,?)''', ("path", path))
            self.c.execute('''insert into glob_prefs values (?,?)''',  ("pdf", "False"))
            self.conn.commit()
        self.c.close()
        print "Tables créées avec succès"




    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.sqliteFile)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

