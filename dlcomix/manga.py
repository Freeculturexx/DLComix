#!/usr/bin/python
# *-* coding: utf-8 *-*

"""
This file is part of DLComix.

    DLComix is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    DLComix is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DLComix.  If not, see <http://www.gnu.org/licenses/>.

"""

import os,  re,  urllib2
import ConfigParser
from threading import Thread
from sqlite import Sqlite



class Manga(object):

    def __init__(self, manga=None, path=None, archive=None, full=None, useComix=None, url=None, limit=None):
        """ Init variables"""
        self.manga = manga.replace(' ', '_')
        self.path = path
        self.archive = archive
        self.full = full
        self.useComix = useComix
        self.url = url
        self.limit = limit


        self.headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)' }


        if self.limit == "":
            self.limit = 10
        else:
            if int(self.limit) <= 0:
                self.limit = 1
            elif int(self.limit) > 10:
                self.limit = 10

        if self.archive == "True":
            self.control_path(self.path+"/archives/"+self.manga)
        self.parseManga = self.parse_manga()

        """ Look if manga folder contains Chapters"""
        if not self.parseManga[1]:
            print "Le manga ne contient aucun chapitre"
            print "Téléchargement arrêté"
        else:
            self.sqlite = Sqlite()

            if self.full == "False":
                self.prepare_download()
                self.single_dl()
            else:
                self.prepare_download()
                self.full_dl()

    def init_dl_rule(self):
        """ Look for last chapter downloaded in database"""
        self.sqlite.connect()
        self.sqlite.c.execute("select * from dl_rule where comic='%s'" % self.manga)
        row = self.sqlite.c.fetchall()
        if not row:
            self.sqlite.c.execute("insert into dl_rule values(?,?)",(self.manga, '0'))
            self.sqlite.conn.commit()
            self.start_i = 0
            self.start = self.parseManga[1][0]
            return True
        else:
            self.start_i = int(row[0][1])
            nbr_l = len(self.parseManga[1]) - 1
            if self.start_i <= nbr_l :
                self.start = self.parseManga[1][self.start_i]
                return True
            else:
                return False
        self.sqlite.c.close

    def prepare_download(self):
        """ define local paths for download"""
        test_dl = self.init_dl_rule()
        if test_dl is not False :
            self.normalize_chapter()
            self.urlDl = self.url+self.chapter+"/"
            self.pathDl = self.path+"/download/"+self.manga+"/"+self.chapter
            self.control_path(self.pathDl)


    def single_dl(self):
        """ Single chapter download"""
        self.download()
        self.start_i += 1
        self.sqlite.connect()
        self.sqlite.c.execute("update dl_rule set data=(?) where comic=(?)", (self.start_i, self.manga))
        self.sqlite.conn.commit()
        self.sqlite.c.close()
        if self.archive == "True":
            self.make_archive()


    def full_dl(self):
        """All chapter dowload """
        while self.start_i <= self.parseManga[0] - 1:
            self.single_dl()
            self.prepare_download()

    def control_path(self, path):
        """ Check if download path exists"""
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename

    def download(self):
        """ Download Chapters"""
        if self.start_i >= self.parseManga[0]:
            pass
        else:
            print ("Téléchargement de "+str(self.manga)+" "+str(self.chapter)).decode('utf-8')
            req = urllib2.Request(self.urlDl, headers = self.headers)
            response = urllib2.urlopen(req)
            images = response.read()
            images = re.findall('<li><a href="(.*?)">',images)
            images.remove(images[0])
            n = 0
            dd = ()
            while n <= len(images)-1:
                dl_image = str(images[n])
                locals()[n]= Thread(target=self.multi_download,args=(dl_image,) )
                locals()[n].start()
                n += 1
            n = 0
            while n <= len(images)-1:
                locals()[n].join()
                n += 1

    def multi_download(self,  images):
        """ Make parallel downloads"""
        req = urllib2.Request(self.urlDl+images,  headers = self.headers)
        response = urllib2.urlopen(req)
        image = response.read()

        i_file = open(self.pathDl+"/"+images,  'w')
        i_file.write(image)
        i_file.close()

    def parse_manga(self):
        """ Define number of chapters and chapter list"""
        v = (0, "", 100, 0)
        (i, album, mini, maxi) = v
        print ("Préparation du téléchargement").decode('utf-8')
        req = urllib2.Request(self.url,  headers = self.headers)
        response = urllib2.urlopen(req)
        htmlSource = response.read()
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

            else:
                n -= 1
                tmpLink.remove(tmpLink[i])
        nManga = len(tmpLink)
        tmpLink.sort()
        return nManga, tmpLink

    def normalize_chapter(self):
        """ Change chapter name to be compatible with Comix sofware library"""
        x = len(self.start)
        if float(self.start) < 100:
            y = self.start[1:x]
        else:
            y = self.start
        if float(self.start) < 10:
            y = y[1:x]
        self.chapter = "Chapter-"+str(y)
        if self.useComix == "True":
            self.archive_chapter = "Chapter-"+self.start
        else:
            self.archive_chapter = "Chapter-"+str(y)
        self.archive_chapter = self.archive_chapter.replace('.','-')

    def make_archive(self):
        """ Create archive files"""
        os.system("cd "+self.path+"/download/"+self.manga+" && tar -cvzf "+self.archive_chapter+".tar.gz "
                  +self.chapter+"/ && rm -rf "+self.chapter+"/")
        os.system("ln -s "+self.path+"/download/"+self.manga+"/"+self.archive_chapter+".tar.gz "+self.path
                  +"/archives/"+self.manga+"/"+self.archive_chapter+".tar.gz")

