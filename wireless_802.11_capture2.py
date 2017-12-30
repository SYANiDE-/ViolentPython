#!/usr/bin/env python2
import re, argparse, sys
from scapy.all import *

# Tested with:
#tty1: sudo ./wireless_802.11_capture2.py -i lo 
#tty2: sudo ncat -nlp 443 -k
#tty3: curl -X POST -d "LAST_NAME=douglas&ROOM_NUMBER=9876" http://127.0.0.1:443/dummy.php

__NOTE = """\
POST /dummy.php HTTP/1.1
Host: 127.0.0.1:443
User-Agent: curl/7.57.0
Accept: */*
Content-Length: 34
Content-Type: application/x-www-form-urlencoded

LAST_NAME=douglas&ROOM_NUMBER=9876
""" # ncat


def analyze(pkt):
    rawdat = pkt.sprintf("%Raw.load%")
    name = re.findall('(?i)LAST_NAME=(.*)&', rawdat)
    room = re.findall("(?i)ROOM_NUMBER=(.*)'", rawdat)
    if name:
        print("[+] Found:  %s:%s" % (name, room))


def getargs():
    ap = argparse.ArgumentParser(description="Sniff for specific data")
    ap.add_argument('-i', '--iface', type=str, default=None, help="Interface to capture on")
    args, l = ap.parse_known_args()
    if args.iface == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    try:
        sniff(filter='tcp', iface=(getargs()).iface, prn=analyze)
    except KeyboardInterrupt:
        sys.exit()


if __name__=="__main__":
    main()

