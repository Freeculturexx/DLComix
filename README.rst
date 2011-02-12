Description of the application
##############################

The application DLComix is an application like Dailystrips to download online comics from the web. 

The first step will be to have the last picture of the day.

Then I will start script to download the whole directory of different comics

But the most important will be to support the largest number of comics !! 

Install  DLComix
################

You will need git-core package. For a Debian based distribution, make a
apt-get install git-core
as root

Go on the folder you want to put DLComix, and make
git clone git://github.com/Freeculture/DLComix.git
 
To install it, go in DLComix folder and make a 
python setup.py install 
as root

That's all

Download your first comic
#########################

With dlcomix, you have five options
-c or --comic 
	where you put the comic name. All supported comics are in List_of_Comics file
	Put the name on the second column
-p or --path (optional)
	Path where you want to download comic. If none, DLComix will create the
	~/.dlcomix/download folder
-a or --archive (optional)
	Use if you want DLComix create archives for you
-f or --full (optional)
	Use if you want to all images of a comic
-u or --usecomix (optional)
        This option renames archive to have better integration with Comix sofware.
        By defaut archives names are Chapter-9.tar.gz, Chapter-10.tar.gz, and
        Comix put the Chapter-10 before Chapter-9. With this option, Chapter-9.tar.gz
        becomes Chapter-09.tar.gz

The exemple
-----------

Imagine you want to download the last Garfield comic

Do a
dlcomix -c garfield

I hope you will enjoy it
 
Use of config file
###################

You can use a config file that will be stored in ~/.dlcomix and named config.py

For the moment, you can config the path where you want to download files and choose the comics you want to download 

Config.py
---------

PATH = "/home/username/Images/comix"

COMICS = ('garfield',
		'bloom_county',)

ARCHIVE = True
FULL = True
USE_COMIX = True

So by typing only 

dlcomix

you download full garfield and bloom_county and create archives optimized for Comix !!

