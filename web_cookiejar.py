#!/usr/bin/env python2
import mechanize, cookielib, sys, argparse, datetime


# Good resource:  http://wiki.dreamrunner.org/public_html/Python/Python-Mechanize-Cheat-Sheet%20.html

def cookie_jar(url):
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    cj = cookielib.LWPCookieJar()
    browser.set_cookiejar(cj)
    pg = browser.open(url)
    # print(pg.read())
    for Cookie in cj:
        print("[%s]  Cookie: %s" % (datetime.datetime.now(), Cookie))


def getargs():
    ap = argparse.ArgumentParser(description="Dump cookies from web request")
    ap.add_argument('-u', '--url', type=str, default=None, help="URL to parse")
    args, l = ap.parse_known_args()
    if args.url == None:
        ap.print_help()
        sys.exit()
    else:
        return args

def main():
    args = getargs()
    cookie_jar(args.url)


if __name__=="__main__":
    main()
