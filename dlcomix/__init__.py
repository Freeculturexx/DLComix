import argparse
import os
import comicbase
import settings



def run_dlcomix(comic=None, path=None, archive=None, full=None):

    config = settings._DEFAULT_CONFIG
    if os.path.isfile(os.path.expanduser ("~" )+'/.dlcomix/config.py'):
        config = settings.read_settings(os.path.expanduser ("~" )+'/.dlcomix/config.py')



    comics = comic or config["COMICS"]
    paths = path or config["PATH"] or settings._DEFAULT_CONFIG["PATH"]
    archives = archive or config["ARCHIVE"] or settings._DEFAULT_CONFIG["ARCHIVE"]
    fulls = full or config["FULL"] or settings._DEFAULT_CONFIG["FULL"]
    comics = (comics)
    comicbase.define_host(comics,paths, archives, fulls)




def main():
    parser = argparse.ArgumentParser(description="""A little software to download comics.
    To see the list of comics, see  the the ComicList file""")
    parser.add_argument('-p', '--path', dest='path', help='Path where you want to download comics')
    parser.add_argument('-c', '--comic', dest='comic', help='Comic you want to download')
    parser.add_argument('-a', '--archive', action="store_true", help='To create comic archives')
    parser.add_argument('-f', '--full', action="store_true", help='To download all the items of one comic')
    args = parser.parse_args()

    run_dlcomix(args.comic, args.path, args.archive, args.full)

if __name__ == '__main__':
    main()
