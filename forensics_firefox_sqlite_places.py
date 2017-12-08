#!/usr/bin/env python2
import sqlite3, sys

# Expect a lot of output.  One line for every url times every date visited


def prnHist(hist):
    try:
        cx = sqlite3.connect(hist)
        c = cx.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")
        print("[!] History:")
        for i in c:
            print("[+] %s:%s" % (str(i[1]), str(i[0])))
    except Exception, X:
        if 'encrypted' in str(X):
            print("[!!] Requires python sqlite3 lib > 3.6.22")
        else:
            print(str(X))


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "places.sqlite"))
    else:
        prnHist(sys.argv[1])


if __name__=="__main__":
    main()

