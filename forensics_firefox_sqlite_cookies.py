#!/usr/bin/env python2
import sqlite3, sys


def HeyYoBLemmeTalkToCookie(cookie):
    try:
        cx = sqlite3.connect(cookie)
        c = cx.execute("SELECT host, name, value FROM moz_cookies")
        print("[!!] Cookies:")
        for i in c:
            print("[+] Host: %s, Cookie: %s, Value: %s" % (str(i[0]), str(i[1]), str(i[2])))
    except Exception, ZZ:
        if 'encrypted' in str(ZZ):
            print("[!] Error!  Requires  python sqlite3 lib > 3.6.22")
        else:
            print(str(ZZ))


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "cookies.sqlite"))
    else:
        try:
            HeyYoBLemmeTalkToCookie(sys.argv[1])
        except Exception, Z:
            print(str(Z))


if __name__=="__main__":
    main()
