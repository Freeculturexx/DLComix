#!/usr/bin/python
import os
from time import *
from datetime import datetime, timedelta
import re
from PIL import Image
import ConfigParser
import gocomics, manga

gocomics_base = gocomics.base
manga_base = manga.base

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
        if manga_base.has_key(comic):
            control_path(path+"download/"+comic)
            if full is False:
                single_manga(comic, path, archive)
            else:
                full_manga(comic, path, archive)
        else:
            for name in comic :
                if manga_base.has_key(name):
                    control_path(path+"download/"+name)
                    if full is False:
                        single_manga(name, path, archive)
                    else:
                        full_manga(name, path, archive)
                else:
                    print "La valeur "+name+" est erronee"

def single_manga(manga, path, archive):
    range_manga = parse_manga(manga)
    number = int(dl_rule_manga(manga, path, range_manga)) +1
    chapter = "Chapter-"+str(number)
    url = manga_base[manga][0]+chapter+"/"
    path2 = path+"download/"+manga+"/"+chapter
    control_path(path2)
    print "Téléchargement de "+manga+" "+chapter
    os.system("cd "+path2+" && wget -q -c -i "+url+" -A .jpg,.jpeg,.png,.gif  "+url)
    os.system("cd "+path2+" && rm *.html* && rm *.db")
    dl_rule = path+".dl_rule"
    dl_rules = ConfigParser.ConfigParser()
    dl_rules.readfp(open(dl_rule,'r'))
    if dl_rules.has_section(manga):
        dl_rules_number = int(dl_rules.get(manga,'number'))
        dl_rules_number += 1
        dl_rules.set(manga,'number', dl_rules_number)
        dl_rules.write(open(dl_rule,'w'))
    if archive is not False:
        create_archive_manga(manga, path, chapter)

def full_manga(manga,path,archive):
    range_manga = parse_manga(manga)
    number = int(dl_rule_manga(manga, path, range_manga)) +1
    while number <= range_manga[1]:
        single_manga(manga,path,archive)
        number += 1
    

def dl_rule_manga(manga, path, range_manga):
    dl_rule = path+".dl_rule"
    if not os.path.isfile(dl_rule):
        file(dl_rule,'w')
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.add_section(manga)
        dl_rules.set(comic, 'number',range_manga[0]-1)
        dl_rules.write(open(dl_rule,'w'))
    else:
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.readfp(open(dl_rule,'r'))
        if dl_rules.has_section(manga):
            dl_rules_number = dl_rules.get(manga,'number')
        else:
            dl_rules.add_section(manga)
            dl_rules_number=range_manga[0]-1
            dl_rules.set(manga,'number', dl_rules_number)
            dl_rules.write(open(dl_rule,'w'))
        return dl_rules_number


def parse_manga(manga):
    url = manga_base[manga][0]
    os.system("wget -q -O /tmp/" +manga+" "+url)
    file = open("/tmp/"+manga,"rb")
    htmlSource = file.read()
    link = re.findall('<li><a href="(.*?)">',htmlSource)
    n = len(link)-1
    i= 0
    album=""
    mini = 100
    maxi = 0
    while i<= n:
        if link[i].startswith('Chapter-'):
            link[i]= link[i].replace('Chapter-','')
            link[i] = link[i].replace('/','')
            if not link[i] == '':
                album = int(link[i])
                if album < mini :
                    mini = album	
                if album > maxi :
                    maxi = album
        i += 1
    range_manga=(mini,maxi)
    return range_manga

        
def create_archive_manga(manga,path,chapter):
    print manga,path,chapter
    os.system("cd "+path+"download/"+manga+" && tar -cvzf "+chapter+".tar.gz "+chapter+"/")
    control_path(path+"archives/"+manga)
    os.system("ln -s "+path+"download/"+manga+"/"+chapter+".tar.gz "+path+"/archives/"+manga+"/"+chapter+".tar.gz")


def single_gocomics(comic,path, archive):
    comic_file = gocomics_base[comic][1].replace('http://www.gocomics.com/','')
    gocomics(comic, path, comic_file)
    if archive is not False :
        create_archive(comic, path)

def full_gocomics(comic, path, archive):
    date = gocomics_base[comic][2]
    date = dl_rule(path, comic,date)
    if date <= datetime.today():
        url = gocomics_base[comic][1]
        gocomics_all(comic, url, path, date, archive)
        single_gocomics(comic,path, archive)





def gocomics_all(comic, url, path, first, archive):
    comic_name = gocomics_base[comic][1].replace('http://www.gocomics.com/','')
    first2 = datetime.strftime(first, "%Y/%m/%d")
    first2 = re.findall('(.*)/(.*)/(.*)', first2)[0][0]
    first_year = int(first2)
    last = datetime.today()-timedelta(2)
    last_year = int(datetime.strftime(last, "%Y"))
    while first_year <= last_year :
        if archive == True:
            tarfile = comic+"_"+first2+".tar.gz"
            if os.path.isfile(path+"download/"+comic+"/"+tarfile):
                os.system("cd "+path+"download/"+comic+" && tar -xvzf "+tarfile)
                os.system("cd "+path+"download/"+comic+" && rm "+tarfile)
        first_year += 1
        first2 = str(first_year)
    while first <= last :
        iffile = path+"download/"+comic+"/"+comic_name+"_"+datetime.strftime(first, "%Y_%m_%d")+".gif"
        if os.path.exists(iffile):
            print comic_name+"_"+datetime.strftime(first, "%Y_%m_%d")+".gif"+" a déjà été téléchargé"
            first = first + timedelta(1)
        else:
            wget = url+"/"+datetime.strftime(first, "%Y/%m/%d")
            os.system("wget -q -O /tmp/" +comic+" "+wget)
            file = open("/tmp/"+comic,"rb")
            htmlSource = file.read()
            link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
            file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
            next = re.findall('<li><a href="(.*?)/" class="next">Next feature</a></li>',htmlSource)
            next = next[0].replace('/'+comic+'/','')
            next = datetime.strptime(next, "%Y/%m/%d")
            if file:
                file = file[0][1].replace('/','_')+".gif"
                if not os.path.isfile(path+"download/"+comic+"/"+file):
                    os.system("wget -q -O " +path+"download/"+comic+"/"+file +" "+link[0])
                    print "Téléchargement de "+file
                    gocomic_crop_image(path+"download/"+comic+"/"+file)
                first = next
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
        dl_rule_date = datetime.strptime(date, "%Y/%m/%d")
        dl_rules.set(comic, 'date', dl_rule_date)
        dl_rules.write(open(dl_rule,'w'))
    else :
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.readfp(open(dl_rule, 'r'))
        if dl_rules.has_section(comic):
            dl_rule_date = datetime.strptime(dl_rules.get(comic, 'date'), "%Y-%m-%d %H:%M:%S")
        else:
            dl_rules.add_section(comic)
            dl_rule_date = datetime.strptime(date, "%Y/%m/%d")
            dl_rules.set(comic, 'date', date)
            dl_rules.write(open(dl_rule,'w'))
    return dl_rule_date

def gocomics(comic,path=None, comic_file=None):
    url =  "%s/" % gocomics_base[comic][0]
    os.system("wget -q -O /tmp/" +comic_file+" "+url)
    file = open("/tmp/"+comic,"rb")
    htmlSource = file.read()
    link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
    file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
    file = file[0][1].replace('/','_')+".gif"
    os.system("wget -q -O " +path+"download/"+comic+"/"+file +" "+link[0])
    print "Téléchargement de "+file
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
    last = datetime.today()
    last_year = int(datetime.strftime(last, "%Y"))
    archives = path+"archives/"
    dl_path = path+"download/"
    comic_path = dl_path+name+"/"
    control_path(archives)
    while first_year <= last_year :
        os.system("cd "+dl_path+name+" && find  -name '*"+first+"*.gif' | xargs tar -cvzf  "+comic_path+name+"_"+first+".tar.gz")
        if not os.path.exists(archives+name+"/"+name+"_"+first+".tar.gz"):
            control_path(archives+name)
            os.system("ln -s "+comic_path+name+"_"+first+".tar.gz "+archives+name+"/"+name+"_"+first+".tar.gz")
        first_year += 1
        first = str(first_year)
    os.system("rm "+comic_path+"*.gif")


def control_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path, mode=0755)
        except OSError, e:
            print e.errno, e.strerror, e.filename
