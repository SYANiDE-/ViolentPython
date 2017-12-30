#!/usr/bin/env python2
from scapy.all import *
import argparse, sys, re


def Analyze(pkt):
    # pload = pkt.sprintf("%Raw.load%") # glob non-translated, ?? when no data
    pload = pkt.getlayer(Raw)# glob translated, NoneType when no data
    if pload != '??' and pload != None:
        print("%s" % pload)


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
        sniff(prn=Analyze, iface=(getargs()).iface, filter="tcp port 80")
    except KeyboardInterrupt:
        sys.exit()


if __name__=="__main__":
    main()



