#!/usr/bin/python
# *-* coding: utf-8 *-*

import os
import re
import ConfigParser
from sqlite import Sqlite

class Manga(object):

    def __init__(self, manga=None, path=None, archive=None, full=None, useComix=None, url=None, limit=None):
        self.manga = manga
        self.path = path
        self.archive = archive
        self.full = full
        self.useComix = useComix
        self.url = url
        self.limit = limit
        
        if self.archive is not False:
            self.control_path(self.path+"/archives/"+self.manga)
        self.parseManga = self.parse_manga()
        self.sqlite = Sqlite()

        if self.full is False:
            self.prepare_download()
            self.single_dl()
        else:
            self.prepare_download()
            self.full_dl()

    def init_dl_rule(self):
        self.sqlite.connect()
        self.sqlite.c.execute("select * from dl_rule where comic='%s'" % self.manga)
        row = self.sqlite.c.fetchall()
        if not row: 
            self.sqlite.c.execute("insert into dl_rule values(?,?)",(self.manga, '0'))
            self.sqlite.conn.commit()
            self.start_i = 0
            self.start = self.parseManga[1][0]
        else:
            self.start_i = int(row[0][1])
            self.start = self.parseManga[1][self.start_i]
        self.sqlite.c.close

    def prepare_download(self):
        self.init_dl_rule()
        self.normalize_chapter()
        self.urlDl = self.url+self.chapter+"/"
        self.pathDl = self.path+"/download/"+self.manga+"/"+self.chapter
        self.control_path(self.pathDl)

    
    def single_dl(self):
        """
        Téléchargement d'un simple épisode
        """
        self.download()
        self.start_i += 1
        self.sqlite.connect()
        self.sqlite.c.execute("update dl_rule set data=(?) where comic=(?)", (self.start_i, self.manga))
        self.sqlite.conn.commit()
        self.sqlite.c.close()
        if self.archive is not False:
            self.make_archive()
        
    
    def full_dl(self):
        """
        Téléchargement de tout les épisodes
        """
        while self.start_i <= self.parseManga[0]:
            self.single_dl()
            self.prepare_download()
        
    def control_path(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename
        
    def download(self):
        if self.start_i >= self.parseManga[0]:
            pass
        else:
            print "Téléchargement de "+str(self.manga)+" "+str(self.chapter)
            os.system("wget "+self.urlDl+" -O /tmp/"+self.manga)
            f = open("/tmp/"+self.manga, "r")
            images = f.read()
            images = re.findall('<li><a href="(.*?)">',images)
            images.remove(images[0])
            os.remove("/tmp/"+self.manga)
            dl = open("/tmp/"+self.manga,'w')
            n = 0
            while n <= len(images)-1:
                dl.write(self.urlDl+images[n]+"\n")
                n += 1
            dl.close()
            os.system("cd "+self.pathDl+" && cat /tmp/"+self.manga+" | xargs -n 1 -P 10 wget -nv -c -t 5")
            os.system("cd "+self.pathDl+" && rm *.html && rm *.db")


    def parse_manga(self):
        """
        Défini les extrémités des chapitres
        """
        v = (0, "", 100, 0)
        (i, album, mini, maxi) = v
        os.system("wget -nv -O /tmp/"+self.manga+" "+self.url)
        tmpFile = open("/tmp/"+self.manga, "rb")
        htmlSource = tmpFile.read()
        tmpLink = re.findall('<li><a href="(.*?)">', htmlSource)
        n = len(tmpLink)-1
        while i <= n: 
            if tmpLink[i].startswith('Chapter-'):
                tmpLink[i] = tmpLink[i].replace('Chapter-','')
                tmpLink[i] = tmpLink[i].replace('/','')
                if tmpLink[i]:
                    if float(tmpLink[i]) < 100:
                        tmpLink[i] =  "0"+tmpLink[i]
                    if float(tmpLink[i]) < 10:
                        tmpLink[i] = "0"+tmpLink[i]
                    i += 1
                else:
                    tmpLink.remove(tmpLink[i])
                    n -= 1
                    print tmpLink
                
            else:
                n -= 1
                tmpLink.remove(tmpLink[i])
        nManga = len(tmpLink)
        tmpLink.sort()
        os.remove("/tmp/"+self.manga)
        return nManga, tmpLink

    def normalize_chapter(self):
        x = len(self.start)
        if float(self.start) < 100:
            y = self.start[1:x]
        else:
            y = self.start
        if float(self.start) < 10:
            y = y[1:x]
        self.chapter = "Chapter-"+str(y)
        if self.useComix is True:
            self.archive_chapter = "Chapter-"+self.start
        else:
            self.archive_chapter = "Chapter-"+str(y)
    
    def make_archive(self):
        os.system("cd "+self.path+"/download/"+self.manga+" && tar -cvzf "+self.archive_chapter+".tar.gz "
                  +self.chapter+"/ && rm -rf "+self.chapter+"/")
        os.system("ln -s "+self.path+"/download/"+self.manga+"/"+self.archive_chapter+".tar.gz "+self.path
                  +"/archives/"+self.manga+"/"+self.archive_chapter+".tar.gz")
