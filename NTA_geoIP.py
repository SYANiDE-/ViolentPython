#!/usr/bin/env python2
import pygeoip, sys


geo = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')
def q(targ):
    r = geo.record_by_name(targ)
    print(str(r))
    print("[+] Target: %s : %s : %s: lat:%s lon:%s" % (targ, str(r['metro_code']), str(r['country_name']), str(r['latitude']), str(r['longitude'])))


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "[IP]"))
    else:
        try:
            q(sys.argv[1])
        except Exception, X:
            print(str(X))
    

if __name__=="__main__":
    main()



