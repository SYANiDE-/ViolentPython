#!/usr/bin/env python2
import sqlite3, sys, re

# 

def prnSearchTerm(st):
    try:
        cx = sqlite3.connect(st)
        c = cx.cursor()
        c.execute("select url, datetime(visit_date/10000000, 'unixepoch') from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;")
        print("[!] SearchTerms:")
        for i in c:
            u = str(i[0])
            d = str(i[1])
            if 'google' in u.lower():
                r = re.findall(r'q=.*\&', u)
                if r:
                    s = r[0].split('&')[0]
                    s = s.replace('q=', '').replace('+', ' ')
                    print("[+] %s:%s" % (str(d), str(s)))
    except Exception, X:
        if 'encrypted' in X:
            print("[!] Requires python sqlite lib > 3.6.22")
        else:
            print(str(X))


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "places.sqlite"))
    else:
        prnSearchTerm(sys.argv[1])


if __name__=="__main__":
    main()


