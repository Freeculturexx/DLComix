#!/usr/bin/python
import sys
import os
from time import strftime
from datetime import datetime
import urllib
import re


gocomics_base = {	'calvin_and_hobbes'   : ['http://www.gocomics.com/calvinandhobbes',
'Calvin and Hobbes', '1984-08-14',],
		'non_sequitur'     : ['http://www.gocomics.com/nonsequitur','Non Sequitur'],
        'garfield' : ['http://www.gocomics.com/garfield','Garfield']
	}


def define_host(comic, path=None):
    if gocomics_base.has_key(comic):
        control_path(path)
        gocomics(comic, path)
    else :
        print "This comic name is incorrect"

def gocomics(comic,path=None):

    today = today_string()
    today_img = today_string_img()
    today_url =  "%s/%s" % (gocomics_base[comic][0], today)
    os.system("wget -O" +comic+" "+today_url)

    file = open(comic,"rb")
    htmlSource = file.read()
    linksList = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
    for link in linksList:
        os.system("wget -O " +path+comic+"_"+today_img+".gif "+link)
    os.system("rm " +comic)


def today_string():
    a=datetime.now()
    a=str(a.strftime("%Y/%m/%d"))
    return a

def today_string_img():
    a=datetime.now()
    a=str(a.strftime("%Y_%m_%d"))
    return a

def control_path(path):
    if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename