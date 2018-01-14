#!/usr/bin/env python2
import mechanize, sys, datetime, argparse

def get_source(url):
    try:
        br = mechanize.Browser()
        pg = br.open(url)
        src = pg.read()
        print(src)
    except KeyboardInterrupt:
        sys.exit()

def getargs():
    ap = argparse.ArgumentParser(description="Retrieve sourcd code (client-side available)")
    ap.add_argument('-u', '--url', type=str, default=None, help="Url of web resource to retrieve.")
    args, l = ap.parse_known_args()
    if args.url == None:
        ap.print_help()
        sys.exit()
    else:
        return args

def main():
    args = getargs()
    get_source(args.url)

if __name__=="__main__":
    main()
