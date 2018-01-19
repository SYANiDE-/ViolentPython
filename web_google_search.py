#!/usr/bin/env python2
import argparse, sys, web_AnonBrowserClass as WAB, urllib

# Google done bumped it's head.  Now AnonBrowser Google search be dead, matey.
# this is broken:
# resp = ab.open('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' +term)
# {"responseData": null, "responseDetails": "The Google Web Search API is no longer available. Please migrate to the Google Custom Search API (https://developers.google.com/custom-search/)", "responseStatus": 403}
# Sadface


def google(term):
    ab = WAB.anonBrowser()
    ab.debug(True)
    ab.anonymize()
    term = urllib.quote_plus(term)
    resp = ab.open('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' +term)
    print(resp.read())


def getargs():
    ap = argparse.ArgumentParser(description="Google search using anonBrowser")
    ap.add_argument("-s", "--searchterm", type=str, default=None, help="Search term")
    args, l = ap.parse_known_args()
    if args.searchterm == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    args = getargs()
    google(args.searchterm)


if __name__=="__main__":
    main()

        
