#!/usr/bin/python
import sys
import os
from time import *
import datetime
import urllib
import re
from PIL import Image
import settings


gocomics_base = {'2_cows_and_a_chicken' : ['http://www.gocomics.com/features/290-2cowsandachicken',
    'http://www.gocomics.com/2cowsandachicken', '2 Cows and a Chicken', '2008/06/30'],
        'bloom_county' : ['http://www.gocomics.com/features/20-bloomcounty',
            'http://www.gocomics.com/bloomcounty', 'Bloom County', '1980/12/04'],
        'calvin_and_hobbes'   : ['http://www.gocomics.com/features/32-calvinandhobbes',
            'http://www.gocomics.com/calvinandhobbes','Calvin and Hobbes', '1984/08/14',],
        'for_better_or_for_worse' : ['http://www.gocomics.com/features/64-forbetterorforworse',
            'http://www.gocomics.com/forbetterorforworse','For Better or For Worse', '1981/11/23'],
        'foxtrot' : ['http://www.gocomics.com/features/66-foxtrot',
            'http://www.gocomics.com/foxtrot', 'FoxTrot', '1996/03/11'],
        'garfield' : ['http://www.gocomics.com/features/72-garfield',
            'http://www.gocomics.com/garfield','Garfield','1978/06/19'],
        'non_sequitur'     : ['http://www.gocomics.com/features/112-nonsequitur',
            'http://www.gocomics.com/nonsequitur','Non Sequitur','1992/02/16']
	}


def define_host(comic, path=None, archive=None, full=None):
    if comic :
        for name in comic :
            if gocomics_base.has_key(name):
                control_path(path)
                if full is False :
                    gocomics(name, path)
                    if archive is True :
                        create_archive(name, path)
                else :
                    date = gocomics_base[name][3]
                    date = datetime.datetime.strptime(date, "%Y/%m/%d")
                    url = gocomics_base[name][1]
                    gocomics_all(name, url, path, date)
                    if archive is True :
                        create_archive(name, path)
            else :
                print "La valeur "+e+" est erronee"



def gocomics_all(comic, url, path, first):
    last = datetime.datetime.today()
    while first < last :
        first = first + datetime.timedelta(1)
        iffile = path+"download/"+comic+"/"+comic+"_"+datetime.datetime.strftime(first, "%Y_%m_%d")+".gif"
        if not os.path.isfile(iffile):
            wget = url+"/"+datetime.datetime.strftime(first, "%Y/%m/%d")
            os.system("wget -O /tmp/" +comic+" "+wget)
            file = open("/tmp/"+comic,"rb")
            htmlSource = file.read()
            link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
            file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
            file = file[0][1].replace('/','_')+".gif"
            os.system("wget -O " +path+"download/"+comic+"/"+file +" "+link[0])
            gocomic_crop_image(path+"download/"+comic+"/"+file)




def gocomics(comic,path=None):
    url =  "%s/" % gocomics_base[comic][0]
    os.system("wget -O /tmp/" +comic+" "+url)
    file = open("/tmp/"+comic,"rb")
    htmlSource = file.read()
    link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
    file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
    file = file[0][1].replace('/','_')+".gif"
    os.system("wget -O " +path+"download/"+comic+"/"+file +" "+link[0])
    gocomic_crop_image(path+"download/"+comic+"/"+file)

def gocomic_crop_image(image):
    im = Image.open(image)
    largeur, hauteur = im.size[0], im.size[1]-25
    im = im.crop((0,0,largeur,hauteur))
    im.save(image)

def create_archive(name, path):
    archives = path+"archives/"
    dl_path = path+"download/"
    comic_path = dl_path+name+"/"
    control_path(archives)
    if os.path.isfile(dl_path+name+'/'+name+'.tar'):
        os.system("tar --delete -vf "+comic_path+name+".tar "+comic_path+"*.gif")
        os.system("tar -rvf  "+comic_path+name+".tar "+comic_path+"*.gif")
    else:
        os.system("tar -cvf  "+comic_path+name+".tar "+comic_path+"*.gif")
    os.system("rm "+comic_path+"*.gif")
    if not os.path.exists(archives+name+".tar"):
        os.system("ln -s "+comic_path+name+".tar "+archives+name+".tar")

def control_path(path):
    if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename