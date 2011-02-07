#!/usr/bin/python
import os
from time import *
from datetime import datetime, timedelta
import re
from PIL import Image
import ConfigParser
import gocomics, manga, gocomics_list, manga_list

gocomics_base = gocomics_list.base
manga_base = manga_list.base

def define_host(comic, path=None, archive=None, full=None):
    if comic :
        if gocomics_base.has_key(comic):
            control_path(path+"download/"+comic)
            if full is False:
                gocomics.single(comic,path, archive)
            else :
                gocomics.full(comic, path, archive)
        else :
            for name in comic :
                if gocomics_base.has_key(name):
                    control_path(path+"download/"+name)
                    if full is False :
                        gocomics.single(name,path, archive)
                    else :
                        gocomics.full(name, path, archive)
        if manga_base.has_key(comic):
            control_path(path+"download/"+comic)
            if full is False:
                manga.single(comic, path, archive)
            else:
                manga.full(comic, path, archive)
        else:
            for name in comic :
                if manga_base.has_key(name):
                    control_path(path+"download/"+name)
                    if full is False:
                        manga.single(name, path, archive)
                    else:
                        manga.full(name, path, archive)
                else:
                    print "La valeur "+name+" est erronee"





def control_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path, mode=0755)
        except OSError, e:
            print e.errno, e.strerror, e.filename
