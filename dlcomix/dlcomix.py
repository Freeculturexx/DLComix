import argparse
import os
import comicbase

def run_dlcomix(comic, path=None):

    if comic is None:
        sys.exit("No comic selected")

    if path is None:
        path = os.path.expanduser ("~" )+'/.dlcomix/download/'+comic+'/'


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