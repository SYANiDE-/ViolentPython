#!/usr/bin/env python2
import sqlite3, sys

note="""
It should be noted that, Arch Linux + Firefox 57 'Quantum', there doesn't appear to be a 'downloads.sqlite', so didn't get a chance to try this one out:

$ ls *.sqlite
ant_data.sqlite       formhistory.sqlite  storage.sqlite
content-prefs.sqlite  kinto.sqlite        storage-sync.sqlite
cookies.sqlite        permissions.sqlite  webappsstore.sqlite
favicons.sqlite       places.sqlite
"""


def dls(db):
    cx = sqlite3.connect(db)
    c = cx.cursor()
    c.execute('SELECT name, source, datetime(endTime/1000000,"unixepoch") FROM moz_downloads;')
    print("[!] Downloaded files:")
    for i in c:
        print("[+] : %s : %s : %s" % (i[2], i[0], i[1]))


def main():
    argsz = len(sys.argv)
    if argsz == 2:
        dls(sys.argv[1])
    else:
        print("USAGE: %s %s" % (sys.argv[0], "downloads.sqlite"))

if __name__=="__main__":
    main()
