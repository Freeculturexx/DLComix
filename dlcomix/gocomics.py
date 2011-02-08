#!/usr/bin/python
import os
from time import *
from datetime import datetime, timedelta
import re
from PIL import Image
import ConfigParser
import gocomics_list
import dlcomixbase

def single(comic,path, archive):
    comic_file = gocomics_list.base[comic][1].replace('http://www.gocomics.com/','')
    gocomics(comic, path, comic_file)
    if archive is not False :
        create_archive(comic, path)

def full(comic, path, archive):
    date = gocomics_list.base[comic][2]
    date = dl_rule(path, comic,date)
    if date <= datetime.today():
        url = gocomics_list.base[comic][1]
        g_all(comic, url, path, date, archive)
        single(comic,path, archive)





def g_all(comic, url, path, first, archive):
    comic_name = gocomics_list.base[comic][1].replace('http://www.gocomics.com/','')
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
                    crop_image(path+"download/"+comic+"/"+file)
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
    url =  "%s/" % gocomics_list.base[comic][0]
    os.system("wget -q -O /tmp/" +comic_file+" "+url)
    file = open("/tmp/"+comic,"rb")
    htmlSource = file.read()
    link = re.findall('<link rel="image_src" href="(.*?)" />',htmlSource)
    file = re.findall('<h1 (.*?)><a href="/(.*?)/">', htmlSource)
    file = file[0][1].replace('/','_')+".gif"
    os.system("wget -q -O " +path+"download/"+comic+"/"+file +" "+link[0])
    print "Téléchargement de "+file
    crop_image(path+"download/"+comic+"/"+file)

def crop_image(image):
    im = Image.open(image)
    largeur, hauteur = im.size[0], im.size[1]-25
    im = im.crop((0,0,largeur,hauteur))
    im.save(image)

def create_archive(name, path):
    first = gocomics_list.base[name][2]
    first = re.findall('(.*)/(.*)/(.*)', first)[0][0]
    first_year = int(first)
    last = datetime.today()
    last_year = int(datetime.strftime(last, "%Y"))
    archives = path+"archives/"
    dl_path = path+"download/"
    comic_path = dl_path+name+"/"
    dlcomixbase.control_path(archives)
    while first_year <= last_year :
        os.system("cd "+dl_path+name+" && find  -name '*"+first+"*.gif' | xargs tar -cvzf  "+comic_path+name+"_"+first+".tar.gz")
        if not os.path.exists(archives+name+"/"+name+"_"+first+".tar.gz"):
            dlcomixbase.control_path(archives+name)
            os.system("ln -s "+comic_path+name+"_"+first+".tar.gz "+archives+name+"/"+name+"_"+first+".tar.gz")
        first_year += 1
        first = str(first_year)
    os.system("rm "+comic_path+"*.gif")

