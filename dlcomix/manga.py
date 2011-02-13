#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import ConfigParser
import manga_list
import dlcomixbase

def single(manga, path, archive, comix_use,range_manga=None):
    if range_manga is None:
        print "Initialisation du téléchargement"
        range_manga = parse(manga)
    chapters = normalize_list(manga, path, range_manga, comix_use)
    chapter = chapters[0]
    archive_chapter = chapters[1]
    url = manga_list.base[manga][0]+chapter+"/"
    path2 = path+"download/"+manga+"/"+chapter
    dlcomixbase.control_path(path2)
    download(manga, chapter, url,path2) 
    dl_rule = path+".dl_rule"
    dl_rules = ConfigParser.ConfigParser()
    dl_rules.readfp(open(dl_rule,'r'))
    if dl_rules.has_section(manga):
        dl_rules_number = int(dl_rules.get(manga,'number'))
        dl_rules_number += 1
        dl_rules.set(manga,'number', dl_rules_number)
        dl_rules.write(open(dl_rule,'w'))
    if archive is not False:
        create_archive(manga, path, chapter, archive_chapter)

def full(manga,path,archive,comix_use):
    print "initialisation du téléchargement"
    range_manga = parse(manga)
    number = int(dlrule(manga, path, range_manga[1][0]))
    while number <= range_manga[0]-1:
        single(manga,path,archive,comix_use,range_manga)
        number += 1
    

def dlrule(manga, path, range_manga):
    dl_rule = path+".dl_rule"
    if not os.path.isfile(dl_rule):
        file(dl_rule,'w')
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.add_section(manga)
        dl_rules.set(comic, 'number',range_manga[1][0])
        dl_rules.write(open(dl_rule,'w'))
    else:
        dl_rules = ConfigParser.ConfigParser()
        dl_rules.readfp(open(dl_rule,'r'))
        if dl_rules.has_section(manga):
            dl_rules_number = dl_rules.get(manga,'number')
        else:
            dl_rules.add_section(manga)
            dl_rules_number=range_manga[1][0]
            dl_rules.set(manga,'number', dl_rules_number)
            dl_rules.write(open(dl_rule,'w'))
        return dl_rules_number


def parse(manga):
    url = manga_list.base[manga][0]
    os.system("wget -O /tmp/" +manga+" "+url)
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
            if link[i]:
                if float(link[i]) < 100:
                    link[i] = "0"+link[i]
                if float(link[i]) < 10:
                    link[i] = "0"+link[i]
            i += 1
        else:
            n -= 1
            link.remove(link[i])
    n_manga=len(link)
    link.sort()
    return n_manga, link

        
def create_archive(manga,path,chapter, archive_chapter):
    print manga,path,chapter
    os.system("cd "+path+"download/"+manga+" && tar -cvzf "+archive_chapter+".tar.gz "+chapter+"/ && rm -rvf "+chapter+"/")
    dlcomixbase.control_path(path+"archives/"+manga)
    os.system("ln -s "+path+"download/"+manga+"/"+archive_chapter+".tar.gz "+path+"/archives/"+manga+"/"+archive_chapter+".tar.gz")

def download(manga, chapter, url,path2):
    print "Téléchargement de "+manga+" "+chapter
    os.system("wget  "+url+" -O /tmp/"+manga)
    f = open('/tmp/'+manga, 'r')
    images = f.read()
    images = re.findall('<li><a href="(.*?)">',images) 
    images.remove(images[0])
    os.remove("/tmp/"+manga)
    dl = open("/tmp/"+manga,'w')
    n = 0
    while n <= len(images)-1:
        dl.write(url+images[n]+"\n")
        n += 1
    dl.close()
    os.system("cd "+path2+" && cat /tmp/"+manga+" | xargs -n 1 -P 10 wget  -c -t 5")
    os.system("cd "+path2+" && rm *.html* && rm *.db")

def normalize_list(manga, path, range_manga, comix_use):
    number = dlrule(manga, path, range_manga[1][0])
    number = range_manga[1][int(number)]
    x = len(number)
    if float(number) < 100:
        number_c = number[1:x]
    else:
        number_c = number
    if float(number) < 10:
        number_c = number_c[1:x]
    chapter = "Chapter-"+str(number_c)
    if comix_use is True:
        archive_chapter = "Chapter-"+str(number)
    else:
        archive_chapter = "Chapter-"+str(number_c)
    return (chapter, archive_chapter)
