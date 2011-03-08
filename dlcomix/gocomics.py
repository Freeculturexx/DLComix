#!/usr/bin/python
# *-* coding: utf-8 *-*

import os,  re,  time
from PIL import Image
from sqlite import Sqlite

class Gocomics(object):

    def __init__(self, comic=None, path=None, archive=None, full=None, useComix=None,
                 url=None):
        self.comic = comic.replace(' ',  '_')
        self.path = path
        self.archive = archive
        self.full = full
        self.useComix = useComix
        self.url = url
        self.comic_url = self.url.replace('http://www.gocomics.com/', '')

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
        if not os.path.exists(path):
            try:
                os.makedirs(path, mode=0755)
            except OSError, e:
                print e.errno, e.strerror, e.filename

    def parse_comic(self):
        os.system("wget -nv -O /tmp/"+self.comic+" "+self.url)
        f = open("/tmp/"+self.comic, "rb")
        source = f.read()
        self.last = re.findall("<h1 class='too_big'><a href="+'"/'+self.comic_url+
                               "/(.*?)/"+'">'"", source)
        if not self.last:
            self.last = re.findall('<h1 ><a href="/'+self.comic_url+'/(.*?)/">', source)
        self.first = re.findall('<li><a href="/'+self.comic_url+'/(.*?)/" class="beginning">', source)
        self.lastItem = re.findall('<link rel="image_src" href="(.*?)" />', source)
        self.nextItem = re.findall('<li><a href="/'+self.comic_url+'/(.*?)/" class="next">',source)


    def single_dl(self):
        last = self.last[0].replace('/','_')
        year = last[:4]
        self.control_path(self.path+"/download/"+self.comic+"/"+year)
        image = self.path+"/download/"+self.comic+"/"+self.comic+"_"+last+".gif"
        os.system("wget  -nv -O "+image+" "+self.lastItem[0])

    def full_dl(self):
        self.sqlite.connect()
        self.url = "http://www.gocomics.com/"+self.comic+"/"+self.start
        first = self.start.replace('/','')
        last = self.last[0].replace('/','')
        while first <= last:
            self.parse_comic()
            year = first[:4]
            self.control_path(self.path+"/download/"+self.comic+"/"+year)
            lastI = self.last[0].replace('/','_')
            image = self.path+"/download/"+self.comic+"/"+year+"/"+self.comic+"_"+lastI+".gif"
            os.system("wget  -nv -c -t 5 -O "+image+" "+self.lastItem[0])
            self.crop_image(image)
            self.sqlite.c.execute("update dl_rule set data=(?) where comic=(?)",
                                  (self.last[0], self.comic))
            self.sqlite.conn.commit()
            if self.nextItem:
                first = self.nextItem[0].replace('/','')
                self.url = "http://www.gocomics.com/"+self.comic+"/"+self.nextItem[0]
            else:
                first = int(first) +1
                first = str(first)
        self.sqlite.c.close()

    def crop_image(self, image):
        im = Image.open(image)
        largeur, hauteur = im.size[0], im.size[1]-25
        im = im.crop((0,0,largeur,hauteur))
        im.save(image)

    def create_archive(self):
        firstY = self.start[0:4]
        lastY = self.last[0][0:4]
        while firstY <= lastY:
            os.system("cd "+self.path+"/download/"+self.comic+"/"+firstY+
                      " && find -name '*"+str(firstY)+"*.gif' | xargs tar -cvzf ../"
                      +self.comic+"_"+str(firstY)+".tar.gz")
            os.system("cd "+self.path+"/download/"+self.comic+"/"+firstY+
                      " && rm -rf "+str(firstY)+"/")
            if not os.path.exists(self.path+"/archives/"+self.comic+"/"+self.comic+"_"
                           +str(firstY)+".tar.gz"):
                os.system("ln -s "+self.path+"/download/"+self.comic+"/"+self.comic+"_"
                      +str(firstY)+".tar.gz "+self.path+"/archives/"+self.comic+"/"+self.comic+"_"
                      +str(firstY)+".tar.gz")
            firstY = int(firstY) + 1
            firstY = str(firstY)

    def unpack_archive(self, start):
        start = int(start[:4])
        thisYear = int(time.strftime('%Y', time.localtime()))
        while start <= thisYear:
            if os.path.exists(self.path+"/download/"+self.comic+"/"+self.comic+"_"
                          +str(start)+".tar.gz"):
                try:
                    os.system("tar -xvzf"+self.path+"/download/"+self.comic+"/"+self.comic+"_"
                      +str(start)+".tar.gz "+self.path+"/download/"+self.comic)
                except OSError, e:
                    print e.errno, e.strerror, e.filename
            start +=1



