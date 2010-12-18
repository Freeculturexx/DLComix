import argparse
import os
import comicbase
import settings


def run_dlcomix(comic, path=None):

    if os.path.isfile(os.path.expanduser ("~" )+'/.dlcomix/config.py'):
        config = settings.read_settings(os.path.expanduser ("~" )+'/.dlcomix/config.py')

        if path is None:
            if config.has_key("PATH"):
                path = config["PATH"]
            else:
                path = os.path.expanduser ("~" )+'/.dlcomix/download/'+comic+'/'

        if comic is None:
            if config.has_key("COMICS"):
                comic = config["COMICS"]
                print comic
            else :
                sys.exit("No comic selected")
        else :
            comic = (comic)



    comicbase.define_host(comic, path)


def main():
    parser = argparse.ArgumentParser(description="""A little software to download comics.
    To see the list of comics, see  the the ComicList file""")
    parser.add_argument('-p', '--path', dest='path', help='Path where you want to download comics')
    parser.add_argument('-c', '--comic', dest='comic', help='Comic you want to download')
    args = parser.parse_args()

    run_dlcomix(args.comic, args.path)

if __name__ == '__main__':
    main()
