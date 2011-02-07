#!/usr/bin/python
import os
import re
import ConfigParser
import manga_list
import dlcomixbase

def single(manga, path, archive):
    range_manga = parse(manga)
    number = int(dlrule(manga, path, range_manga)) +1
    chapter = "Chapter-"+str(number)
    url = manga_list.base[manga][0]+chapter+"/"
    path2 = path+"download/"+manga+"/"+chapter
    dlcomixbase.control_path(path2)
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
        create_archive(manga, path, chapter)

def full(manga,path,archive):
    range_manga = parse(manga)
    number = int(dlrule(manga, path, range_manga)) +1
    while number <= range_manga[1]:
        single(manga,path,archive)
        number += 1
    

def dlrule(manga, path, range_manga):
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


def parse(manga):
    url = manga_list.base[manga][0]
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

        
def create_archive(manga,path,chapter):
    print manga,path,chapter
    os.system("cd "+path+"download/"+manga+" && tar -cvzf "+chapter+".tar.gz "+chapter+"/")
    dlcomixbase.control_path(path+"archives/"+manga)
    os.system("ln -s "+path+"download/"+manga+"/"+chapter+".tar.gz "+path+"/archives/"+manga+"/"+chapter+".tar.gz")

