#!/usr/bin/python
import sys
import os
from time import strftime
from datetime import datetime
import urllib
import re


gocomics_base = {'2_cows_and_a_chicken' : ['http://www.gocomics.com/features/290-2cowsandachicken',
    'http://www.gocomics.com/2cowsandachicken', '2 Cows and a Chicken', '2008-06-30'],
        'bloom_county' : ['http://www.gocomics.com/features/20-bloomcounty',
            'http://www.gocomics.com/bloomcounty', 'Bloom County', '1980-12-04'],
        'calvin_and_hobbes'   : ['http://www.gocomics.com/features/32-calvinandhobbes',
            'http://www.gocomics.com/calvinandhobbes','Calvin and Hobbes', '1984-08-14',],
        'for_better_or_for_worse' : ['http://www.gocomics.com/features/64-forbetterorforworse',
            'http://www.gocomics.com/forbetterorforworse','For Better or For Worse', '1981-11-23'],
        'foxtrot' : ['http://www.gocomics.com/features/66-foxtrot',
            'http://www.gocomics.com/foxtrot', 'FoxTrot', '1996-03-11'],
        'garfield' : ['http://www.gocomics.com/features/72-garfield',
            'http://www.gocomics.com/garfield','Garfield','1978-06-19'],
        'non_sequitur'     : ['http://www.gocomics.com/features/112-nonsequitur',
            'http://www.gocomics.com/nonsequitur','Non Sequitur','1992-02-16']
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
    today_url =  "%s/" % gocomics_base[comic][0]
    os.system("wget -O " +comic+" "+today_url)

    file = open(comic,"rb")
    htmlSource = file.read()
    link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
    file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
    file = file[0][1].replace('/','_')+".gif"
    os.system("wget -O " +path+file +" "+link[0])
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