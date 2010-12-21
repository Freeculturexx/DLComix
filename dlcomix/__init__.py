import argparse
import os
import comicbase
import settings
import sys


def run_dlcomix(comic=None, path=None, archive=None, full=None):

    if os.path.isfile(os.path.expanduser ("~" )+'/.dlcomix/config.py'):
        config = settings.read_settings(os.path.expanduser ("~" )+'/.dlcomix/config.py')


    comic = comic or config["COMICS"]
    path = path or config["PATH"] or settings._DEFAULT_CONFIG["PATH"]
    archive = archive or config["ARCHIVE"] or settings._DEFAULT_CONFIG["ARCHIVE"]
    full = full or config["FULL"] or settings._DEFAULT_CONFIG["FULL"]
    comic = (comic)
    comicbase.define_host(comic,path, archive, full)




def main():
    parser = argparse.ArgumentParser(description="""A little software to download comics.
    To see the list of comics, see  the the ComicList file""")
    parser.add_argument('-p', '--path', dest='path', help='Path where you want to download comics')
    parser.add_argument('-c', '--comic', dest='comic', help='Comic you want to download')
    parser.add_argument('-a', '--archive', dest='archive', help='Put true to create an archive, false to not create any')
    parser.add_argument('-f', '--full', dest='full', help='Put true to download all the items of one comic')
    args = parser.parse_args()

    run_dlcomix(args.comic, args.path, args.archive, args.full)

if __name__ == '__main__':
    main()
