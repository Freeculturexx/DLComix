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

import os,  re,  time,  urllib2
from PIL import Image
from sqlite import Sqlite

class Gocomics(object):

    def __init__(self, comic=None, path=None, archive=None, full=None, useComix=None,
                 url=None):
        """ Init variables"""
        self.comic = comic.replace(' ',  '_')
        self.path = path
        self.archive = archive
        self.full = full
        self.useComix = useComix
        self.url = url
        self.comic_url = self.url.replace('http://www.gocomics.com/', '')

        self.headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)' }

        """ Look for the comic html page and get informations"""
        self.parse_comic()


        if self.full == "False":
            self.single_dl()
        else:
            self.sqlite = Sqlite()
            self.init_dl_rule()
            self.full_dl()

        if self.archive == "True":
            self.control_path(self.path+"/archives/"+self.comic)
            self.create_archive()

    def init_dl_rule(self):
        """ Look for last comic downloaded"""
        self.sqlite.connect()
        self.sqlite.c.execute("select * from dl_rule where comic='%s'"
                              % self.comic)
        row = self.sqlite.c.fetchall()
        if not row:
            self.sqlite.c.execute("insert into dl_rule values(?,?)",
                                  (self.comic, self.first[0]))
            self.sqlite.conn.commit()
            self.start = self.first[0]
        else:
            self.start = row[0][1]
            self.unpack_archive(self.start)
        self.sqlite.c.close

    def control_path(self, path):
        """ Check if download path exists"""
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename

    def parse_comic(self):
        """ Get information from comic html page"""
        req = urllib2.Request(self.url,  headers = self.headers)
        response = urllib2.urlopen(req)
        source = response.read()
        self.last = re.findall("<h1 class='too_big'><a href="+'"/'+self.comic_url+
                               "/(.*?)/"+'">'"", source)
        if not self.last:
            self.last = re.findall('<h1 ><a href="/'+self.comic_url+'/(.*?)/">', source)
        self.first = re.findall('<li><a href="/'+self.comic_url+'/(.*?)/" class="beginning">', source)
        self.lastItem = re.findall('<link rel="image_src" href="(.*?)" />', source)
        self.nextItem = re.findall('<li><a href="/'+self.comic_url+'/(.*?)/" class="next">',source)


    def single_dl(self):
        """ Make a download of last comic"""
        last = self.last[0].replace('/','_')
        year = last[:4]
        self.control_path(self.path+"/download/"+self.comic_url+"/"+year)
        imageFile = self.path+"/download/"+self.comic_url+"/"+year+"/"+self.comic_url+"_"+last+".gif"
        self.download(imageFile)
        self.crop_image(imageFile)

    def full_dl(self):
        """ Download all images of a comic"""
        self.sqlite.connect()
        self.url = "http://www.gocomics.com/"+self.comic_url+"/"+self.start
        first = self.start.replace('/','')
        last = self.last[0].replace('/','')
        while first <= last:
            self.parse_comic()
            year = first[:4]
            self.control_path(self.path+"/download/"+self.comic_url+"/"+year)
            lastI = self.last[0].replace('/','_')
            imageFile = self.path+"/download/"+self.comic_url+"/"+year+"/"+self.comic_url+"_"+lastI+".gif"
            self.download(imageFile)
            self.crop_image(imageFile)
            self.sqlite.c.execute("update dl_rule set data=(?) where comic=(?)",
                                  (self.last[0], self.comic))
            self.sqlite.conn.commit()
            if self.nextItem:
                first = self.nextItem[0].replace('/','')
                self.url = "http://www.gocomics.com/"+self.comic_url+"/"+self.nextItem[0]
            else:
                first = int(first) +1
                first = str(first)
        self.sqlite.c.close()

    def download(self,  imageFile):
        """ Download image"""
        req = urllib2.Request(self.lastItem[0],  headers = self.headers)
        response = urllib2.urlopen(req)
        image = response.read()
        i_file = open(imageFile,  'w')
        i_file.write(image)
        i_file.close()

    def crop_image(self, image):
        """ Make a crop of the downloaded image to remove Gocomics Logo"""
        im = Image.open(image)
        largeur, hauteur = im.size[0], im.size[1]-25
        im = im.crop((0,0,largeur,hauteur))
        im.save(image)

    def create_archive(self):
        """ Create archives files"""
        firstY = self.start[0:4]
        lastY = self.last[0][0:4]
        while firstY <= lastY:
            os.system("cd "+self.path+"/download/"+self.comic_url+"/"+firstY+
                      " && find -name '*"+str(firstY)+"*.gif' | xargs tar -cvzf ../"
                      +self.comic+"_"+str(firstY)+".tar.gz")
            os.system("cd "+self.path+"/download/"+self.comic_url+"/"+firstY+
                      " && rm -rf "+str(firstY)+"/")
            if not os.path.exists(self.path+"/archives/"+self.comic_url+"/"+self.comic_url+"_"
                           +str(firstY)+".tar.gz"):
                os.system("ln -s "+self.path+"/download/"+self.comic_url+"/"+self.comic_url+"_"
                      +str(firstY)+".tar.gz "+self.path+"/archives/"+self.comic_url+"/"+self.comic_url+"_"
                      +str(firstY)+".tar.gz")
            firstY = int(firstY) + 1
            firstY = str(firstY)

    def unpack_archive(self, start):
        """ Uncompress archives before download treatment"""
        start = int(start[:4])
        thisYear = int(time.strftime('%Y', time.localtime()))
        while start <= thisYear:
            if os.path.exists(self.path+"/download/"+self.comic_url+"/"+self.comic_url+"_"
                          +str(start)+".tar.gz"):
                try:
                    os.system("tar -xvzf"+self.path+"/download/"+self.comic_url+"/"+self.comic_url+"_"
                      +str(start)+".tar.gz "+self.path+"/download/"+self.comic_url)
                except OSError, e:
                    print e.errno, e.strerror, e.filename
            start +=1



