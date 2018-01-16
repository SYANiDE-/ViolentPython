#!/usr/bin/env python2
from web_AnonBrowserClass import anonBrowser as aB
import os, argparse, sys, datetime, re 
from BeautifulSoup import BeautifulSoup as BS


def scrape(url):
    ab = aB()
    ab.debug(1)
    ab.anonymize()
    pg = ab.open(url)
    src = pg.read()
    try:
        print("[%s] Printing links via REGEX" % (datetime.datetime.now()))
        lf = re.compile('href="(.*?)"')
        links = lf.findall(src)
        for LINK in links:
            print(LINK)
    except:
        pass
    try:
        print("[%s] Printing links via BeautifulSoup" % (datetime.datetime.now()))
        chowder = BS(src)
        links = chowder.findAll(name='a')
        for LINK in links:
            if LINK.has_key('href'):
                print(LINK['href'])
    except Exception, X:
        print(str(X))
    except:
        pass


def getargs():
    ap = argparse.ArgumentParser(description="Exercises two different methods for parsing through web content")
    ap.add_argument('-u', '--url', type=str, default=None, help="URL to parse")
    args, l = ap.parse_known_args()
    if args.url == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    args = getargs()
    scrape(args.url)


if __name__=="__main__":
    main()

