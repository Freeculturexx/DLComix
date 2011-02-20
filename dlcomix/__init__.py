#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import settings
import sqlite3
from gocomics import Gocomics
from manga import Manga
from sqlite import Sqlite

class Dlcomix(object):

    def __init__(self, comic=None, path=None, archive=None, full=None,
                 use_comix=None, limit=None, update=None):
        
        """Define default settings"""
        if update:
            self.sqlite = Sqlite()
            self.sqlite.initialise_manga()
            self.sqlite.initialise_comic()
        else:
            config = settings._DEFAULT_CONFIG
        
            if os.path.isfile(os.path.expanduser ("~")+'/.dlcomix/config.py'):
                config = settings.read_settings(os.path.expanduser ("~"+'/.dlcomix/config.py'))

            self.path = path or config['PATH']
            if self.path.endswith('/'):
                self.path = self.path[:-1]
            self.archive = archive or config['ARCHIVE']
            self.full = full or config['FULL']
            self.use_comix = use_comix or config['USE_COMIX']
            if not comic:
                self.comic =  config['COMIC']
            else:
                self.comic = [comic]
            self.limit = limit or config['LIMIT']
            self.sqlite = Sqlite()
            self.define_host()

    def control_path(self):
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path, mode=0755)
            except OSError, e:
                print e.errno. e.strerror, e.filename

    def define_host(self):
        """
        Define if --comic argument is a manga or comic
        """
        for name in self.comic:
            self.sqlite.connect()
            self.sqlite.c.execute("select * from mangas where name='%s'" % name)
            for row in self.sqlite.c:
                manga = Manga(row[0], self.path, self.archive, self.full, self.use_comix, row[1], self.limit) 
            self.sqlite.c.execute("select * from comics where name='%s'" % name)
            for row in self.sqlite.c:
                comic = Gocomics(row[0], self.path, self.archive, self.full, self.use_comix, row[1], self.limit)

def main():
    parser = argparse.ArgumentParser(description="""Script to download
    comics and mangas.""")

    parser.add_argument('-c', '--comic', dest='comic',
                        help='Comic or manga you want to download')
    parser.add_argument('-p', '--path', dest='path',
                        help='Path where you want to download files')
    parser.add_argument('-a', '--archive', action='store_true',
                        help='To create comic archives')
    parser.add_argument('-f', '--full', action='store_true',
                        help='To download all items')
    parser.add_argument('-u', '--use-comix', action='store_true',
                        help='Improve archive format for Comix')
    parser.add_argument('-l', '--limit', dest='limit',
                        help="Put a transfert Limit")
    parser.add_argument('--update-comic-list', dest='update', action='store_true',
                        help="Update Comic and Manga list in database")

    args = parser.parse_args()
    dlcomix = Dlcomix(args.comic, args.path, args.archive, args.full,
                      args.use_comix, args.limit, args.update)
        
    


if __name__ == '__main__':
    main()


