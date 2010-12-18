import argparse
import os
import comicbase
import settings
import sys

global _DEFAULT_CONFIG

def run_dlcomix(comic=None, path=None, archive=None):

    if os.path.isfile(os.path.expanduser ("~" )+'/.dlcomix/config.py'):
        config = settings.read_settings(os.path.expanduser ("~" )+'/.dlcomix/config.py')

        if path is None:
            if config.has_key("PATH"):
                path = config["PATH"]
            else:
                path = settings._DEFAULT_CONFIG["PATH"]

        if comic is None:
            if config.has_key("COMICS"):
                comic = config["COMICS"]
            else :
                sys.exit("No comic selected")
        else :
            comic = (comic)

        if archive is None:
            if config.has_key("ARCHIVE"):
                archive = config["ARCHIVE"]
            else:
                archive = settings._DEFAULT_CONFIG["ARCHIVE"]

    else :
        path = settings._DEFAULT_CONFIG["PATH"]
        archive = settings._DEFAULT_CONFIG["ARCHIVE"]
        if comic is None:
            sys.exit("No comic selected")
        else :
            comic = (comic)


    comicbase.define_host(comic, path, archive)


def main():
    parser = argparse.ArgumentParser(description="""A little software to download comics.
    To see the list of comics, see  the the ComicList file""")
    parser.add_argument('-p', '--path', dest='path', help='Path where you want to download comics')
    parser.add_argument('-c', '--comic', dest='comic', help='Comic you want to download')
    parser.add_argument('-a', '--archive', dest='archive', help='Put true to create an archive, false to not create any')
    args = parser.parse_args()

    run_dlcomix(args.comic, args.path, args.archive)

if __name__ == '__main__':
    main()
