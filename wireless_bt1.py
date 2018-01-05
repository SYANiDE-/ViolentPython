#!/usr/bin/env python2
import re, argparse, sys, datetime, time
from bluetooth import *

devlist = discover_devices()


def detect():
    for dev in devlist:
        print("[%s] Detected: %s : \"%s\"" % (datetime.datetime.now(), str(dev), str(lookup_name(dev))))


def main():
    while True:
        detect()
        time.sleep(5)


if __name__=="__main__":
    main()


