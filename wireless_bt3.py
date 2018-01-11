#!/usr/bin/env python2
import re, argparse, sys, datetime, time
from bluetooth import *

# Book was missing the sample code for detecting a target device name; seemed to reiterate the last code sample in place of where the new code would be.  But that's ok... not hard to imagine and produce my own!

devlist = [] 
foundtargs = []

def detect(targ):
    for (mac, name) in discover_devices(lookup_names=True):
        if mac.upper() not in devlist:
            devlist.append(mac.upper())
            print("[%s] Detected: %s : \"%s\"" % (datetime.datetime.now(), str(mac.upper()), str(name)))
        if targ.upper() in mac.upper() and targ.upper() not in foundtargs:
            foundtargs.append(targ.upper())
            print("[%s] Found target device \"%s\":  %s : \"%s\"" % (datetime.datetime.now(), str(targ.upper()), str(mac.upper()), str(name)))



def getargs():
    ap = argparse.ArgumentParser(description="Detect bluetooth devices")
    ap.add_argument('-t', '--targ', type=str, default=None, help="Target device name (contains)")
    args, l = ap.parse_known_args()
    if args.targ == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    args = getargs()
    while True:
        detect(args.targ)
        time.sleep(5)


if __name__=="__main__":
    main()


