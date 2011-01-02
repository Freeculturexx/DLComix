#!/usr/bin/python
import sys
import os
from time import *
import datetime
import urllib
import re
from PIL import Image
import settings
import ConfigParser


gocomics_base = {'2_cows_and_a_chicken' : ['http://www.gocomics.com/features/290-2cowsandachicken',
    'http://www.gocomics.com/2cowsandachicken', '2008/06/30'],
    '9_to_5' : ['http://www.gocomics.com/features/2-9to5',
        'http://www.gocomics.com/9to5', '2001/04/13','9to5'],
    'the_academia_waltz' : ['http://www.gocomics.com/features/3-academiawaltz',
        'http://www.gocomics.com/academiawaltz', '2003/12/08'],
    'adam_at_home' : ['http://www.gocomics.com/features/4-adamathome',
        'http://www.gocomics.com/adamathome', '1995/06/20'],
    'agnes' : ['http://www.gocomics.com/features/5-agnes',
        'http://www.gocomics.com/agnes', '2002/01/01'],
    'andy_capp' : ['http://www.gocomics.com/features/6-andycapp',
        'http://www.gocomics.com/andycapp', '2002/01/01'],
    'animal_crackers' : ['http://www.gocomics.com/features/7-animalcrackers',
        'http://www.gocomics.com/animalcrackers', '2001/04/08'],
    'the_argyle_sweater' : ['http://www.gocomics.com/features/9-theargylesweater',
        'http://www.gocomics.com/theargylesweater', '2006/11/29'],
    'ask_shagg' : ['http://www.gocomics.com/features/10-askshagg',
        'http://www.gocomics.com/askshagg', '2002/08/12'],
    'bc' : ['http://www.gocomics.com/features/11-bc',
        'http://www.gocomics.com/bc', '2002/01/01'],
    'back_in_the_day' : ['http://www.gocomics.com/features/492-backintheday',
        'http://www.gocomics.com/backintheday', '2010/03/08'],
    'bad_reporter' : ['http://www.gocomics.com/features/12-badreporter',
        'http://www.gocomics.com/badreporter', '2005/08/12'],
    'baldo' : ['http://www.gocomics.com/features/13-baldo',
        'http://www.gocomics.com/baldo', '1998/11/22'],
    'ballard_street' : ['http://www.gocomics.com/features/14-ballardstreet',
        'http://www.gocomics.com/ballardstreet', '2002/01/01'],
    'the_barn' : ['http://www.gocomics.com/features/291-thebarn',
        'http://www.gocomics.com/thebarn', '2009/02/02'],
    'barney_and_clyde' : ['http://www.gocomics.com/features/515-barneyandclyde',
        'http://www.gocomics.com/barneyandclyde', '2010/06/07'],
    'basic_instructions' : ['http://www.gocomics.com/features/255-basicinstructions',
        'http://www.gocomics.com/basicinstructions', '2003/02/25'],
    'bewley' : ['http://www.gocomics.com/features/306-bewley',
        'http://www.gocomics.com/bewley', '2009/11/09'],
    'the big_picture' : ['http://www.gocomics.com/features/16-thebigpicture',
        'http://www.gocomics.com/thebigpicture', '2010/11/29'],
    'big_top' : ['http://www.gocomics.com/features/17-bigtop',
        'http://www.gocomics.com/bigtop', '2001/04/22'],
    'bird_brains' : ['http://www.gocomics.com/features/251-birdbrains',
        'http://www.gocomics.com/birdbrains', '2007/01/01'],
    'bleeker' : ['http://www.gocomics.com/features/19-bleeker',
        'http://www.gocomics.com/bleeker', '2006/07/27'],
    'bliss' : ['http://www.gocomics.com/features/281-bliss',
        'http://www.gocomics.com/bliss', '2008/07/28'],
    'bloomcounty' : ['http://www.gocomics.com/features/20-bloomcounty',
        'http://www.gocomics.com/bloomcounty',  '1980/12/04'],
    'calvin_and_hobbes'   : ['http://www.gocomics.com/features/32-calvinandhobbes',
        'http://www.gocomics.com/calvinandhobbes','1984/08/14',],
    'for_better_or_for_worse' : ['http://www.gocomics.com/features/64-forbetterorforworse',
        'http://www.gocomics.com/forbetterorforworse', '1981/11/23'],
    'foxtrot' : ['http://www.gocomics.com/features/66-foxtrot',
        'http://www.gocomics.com/foxtrot',  '1996/03/11'],
    'garfield' : ['http://www.gocomics.com/features/72-garfield',
        'http://www.gocomics.com/garfield','1978/06/19'],
    'non_sequitur'     : ['http://www.gocomics.com/features/112-nonsequitur',
        'http://www.gocomics.com/nonsequitur','1992/02/16']
	}


def define_host(comic, path=None, archive=None, full=None):
    if comic :
        if gocomics_base.has_key(comic):
            control_path(path+"download/"+comic)
            if full is False:
                single_gocomics(comic,path, archive)
            else :
                full_gocomics(comic, path, archive)
        else :
            for name in comic :
                if gocomics_base.has_key(name):
                    control_path(path+"download/"+name)
                    if full is False :
                        single_gocomics(name,path, archive)
                    else :
                        full_gocomics(name, path, archive)
                else :
                    print "La valeur "+name+" est erronee"


def single_gocomics(comic,path, archive):
    comic_file = gocomics_base[comic][3]
    gocomics(comic, path, comic_file)
    if archive is not False :
        create_archive(comic, path)

def full_gocomics(comic, path, archive):
    date = gocomics_base[comic][2]
    date = dl_rule(path, comic,date)
    if date <= datetime.datetime.today():
        url = gocomics_base[comic][1]
        gocomics_all(comic, url, path, date, archive)
        if archive is not False :
            create_archive(comic, path)

def gocomics_all(comic, url, path, first, archive):
    first2 = datetime.datetime.strftime(first, "%Y/%m/%d")
    first2 = re.findall('(.*)/(.*)/(.*)', first2)[0][0]
    first_year = int(first2)
    last = datetime.datetime.today()
    last_year = int(datetime.datetime.strftime(last, "%Y"))
    while first_year <= last_year :
        if archive == True:
            tarfile = path+"download/"+comic+"/"+comic+"_"+first2+".tar"
            if os.path.isfile(tarfile):
                os.system("tar -xvf "+tarfile+" -C /")
                os.system("rm "+tarfile)
        first_year += 1
        first2 = str(first_year)
    while first <= last :
        iffile = path+"download/"+comic+"/"+comic+"_"+datetime.datetime.strftime(first, "%Y_%m_%d")+".gif"
        if not os.path.isfile(iffile):
            wget = url+"/"+datetime.datetime.strftime(first, "%Y/%m/%d")
            os.system("wget -O /tmp/" +comic+" "+wget)
            file = open("/tmp/"+comic,"rb")
            htmlSource = file.read()
            link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
            file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
            if file:
                file = file[0][1].replace('/','_')+".gif"
                if not os.path.isfile(path+"download/"+comic+"/"+file):
                    os.system("wget -O " +path+"download/"+comic+"/"+file +" "+link[0])
                    gocomic_crop_image(path+"download/"+comic+"/"+file)
        first = first + datetime.timedelta(1)
        dl_rule = path+".dl_rule"
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.readfp(open(dl_rule, 'r'))
        dl_rules.set(comic, 'date', first)
        dl_rules.write(open(dl_rule,'w'))


def dl_rule(path, comic, date):
    dl_rule = path+".dl_rule"
    if not os.path.isfile(dl_rule):
        file(dl_rule,'w')
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.add_section(comic)
        dl_rules.set(comic, 'date', date)
        dl_rules.write(open(dl_rule,'w'))
    else :
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.readfp(open(dl_rule, 'r'))
        if dl_rules.has_section(comic):
            dl_rule = dl_rules.get(comic, 'date')
        else:
            dl_rules.add_section(comic)
            dl_rules.set(comic, 'date', date)
            dl_rules.write(open(dl_rule,'w'))
    date = datetime.datetime.strptime(date, "%Y/%m/%d")
    return date

def gocomics(comic,path=None, comic_file=None):
    url =  "%s/" % gocomics_base[comic][0]
    os.system("wget -O /tmp/" +comic_file+" "+url)
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
    first = gocomics_base[name][2]
    first = re.findall('(.*)/(.*)/(.*)', first)[0][0]
    first_year = int(first)
    last = datetime.datetime.today()
    last_year = int(datetime.datetime.strftime(last, "%Y"))
    last_test = str(last_year)
    archives = path+"archives/"
    dl_path = path+"download/"
    comic_path = dl_path+name+"/"
    control_path(archives)
    while first_year <= last_year :
        os.system("find "+dl_path+name+"  -name '*"+first+"*' | xargs tar -cvf  "+comic_path+name+"_"+first+".tar ")
        if not os.path.exists(archives+name+"_"+first+".tar"):
            os.system("ln -s "+comic_path+name+"_"+first+".tar "+archives+name+"_"+first+".tar")
        first_year += 1
        first = str(first_year)
    os.system("rm "+comic_path+"*.gif")


def control_path(path):
    if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename