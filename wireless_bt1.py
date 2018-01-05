#!/usr/bin/env python2
import re, argparse, sys, datetime, time
from bluetooth import *

devlist = discover_devices()


def detect():
    for dev in devlist:
        print("[%s] Detected: %s : \"%s\"" % (datetime.datetime.now(), str(dev), str(lookup_name(dev))))


def getargs():
    ap = argparse.ArgumentParser(description="Detect bluetooth devices")
    ap.add_argument('-i', '--iface', type=str, default=None, help="Interface to packet capture on")
    args, l = ap.parse_known_args()
    if args.iface == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    while True:
        detect()
        time.sleep(5)


if __name__=="__main__":
    main()


