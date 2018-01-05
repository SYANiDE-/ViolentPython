#!/usr/bin/env python2
import re, argparse, sys, datetime
from scapy.all import *

Zcookies = {}


def scrape(pkt):
    raw = pkt.sprintf("%Raw.load%")
    found = re.findall('wordpress_[0-9a-fA-F]{32}', raw)
    if found and 'set' not in raw.lower():
        if found[0] not in Zcookies.keys():
            Zcookies[found[0]] = pkt.getlayer(IP).src
            print("[%s] %s > %s : Cookie : %s" % (datetime.now(), pkt.getlayer(IP).src, pkt.getlayer(IP).dst, found[0]))
        elif Zcookies[found[0]] != pkt.getlayer(IP).src:
            print("[%s] Detected cookie reuse. Cookie: %s, SrcIP was: %s, now: %s" % (datetime.now(), found[0], Zcookies[found[0]], pkt.getlayer(IP).src))


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
