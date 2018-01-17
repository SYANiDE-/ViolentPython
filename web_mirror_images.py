#!/usr/bin/env python2
import argparse, os
from web_AnonBrowserClass import *
from BeautifulSoup import BeautifulSoup


def scrape_IMGs(u, d):
    ab = anonBrowser()
    ab.debug(True)
    ab.anonymize()
    html = ab.open(u)
    chowder = BeautifulSoup(html)
    img_tags = chowder.findAll('img')
    for img in img_tags:
        fname = img['src'].lstrip('http://').lstrip("https://")
        fname = os.path.join(d, fname.replace('/', '_'))
        print("[+] Saving %s" % fname)
        data = ab.open(img['src']).read()
        ab.back()
        fd = open(fname, 'wb')
        fd.write(data)
        fd.close()

def getargs():
    ap = argparse.ArgumentParser(description="Scrape images from web location")
    ap.add_argument('-u', '--url', type=str, default=None, help="URL to scrape from")
    ap.add_argument('-d', '--dir', type=str, default=None, help="DIR to save pictures to")
    args, leftover = ap.parse_known_args()
    if args.url == None or args.dir == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    args = getargs()
    scrape_IMGs(args.url, args.dir)


if __name__=="__main__":
    main()

