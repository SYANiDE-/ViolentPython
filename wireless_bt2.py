#!/usr/bin/env python2
import re, argparse, sys, datetime, time
from bluetooth import *

devlist = [] 


def detect():
    for (mac, name) in discover_devices(lookup_names=True):
        if mac not in devlist:
            devlist.append(mac)
            print("[%s] Detected: %s : \"%s\"" % (datetime.datetime.now(), str(mac), str(name)))


def main():
    while True:
        detect()
        time.sleep(5)


if __name__=="__main__":
    main()


