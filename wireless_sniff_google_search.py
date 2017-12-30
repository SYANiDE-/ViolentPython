#!/usr/bin/env python2
from scapy.all import *
import argparse, sys, re

# I think these days, HSTS run tings (https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security).  I find that request-attempts to Google using http versus https fail; seems to force HTTPS.
# Script still written for ceremonious reasons.


def Google(pkt):
    if pkt.haslayer(Raw):
        pload = pkt.getlayer(Raw).load
        if 'GET' in pload:
            if 'google' in pload.lower():
                rexp = re.findall(r'(?i)\&q=(.*?)\&', pload)
                if rexp:
                    temp = rexp[0].split('&')[0]
                    temp = temp.replace('q=', '').replace('+', ' ').replace("%20", ' ')
                    print("[+] Found term: %s" % temp)

def getargs():
    ap = argparse.ArgumentParser(description="Sniff Google search terms")
    ap.add_argument("-i", '--iface', type=str, default=None, help="interface to sniff on")
    args, l = ap.parse_known_args()
    if args.iface == None:
        ap.print_help()
        sys.exit()
    else:
        return args

def main():
    try:
        sniff(prn=Google, iface=(getargs()).iface, filter="tcp port 80")
    except KeyboardInterrupt:
        sys.exit()

if __name__=="__main__":
    main()



