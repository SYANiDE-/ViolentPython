#!/usr/bin/env python2
from scapy.all import *
import argparse, sys, re, datetime

hidden = []

def Analyze(pkt):
    if pkt.haslayer(Dot11Beacon):
        if pkt.getlayer(Dot11Beacon).info == "":
            src = pkt.addr2
            if src not in hidden:
                dt = datetime.datetime.now()
                hidden.append(src)
                print("[%s] Detected hidden SSID net using mac %s" % (dt, src))


def getargs():
    ap = argparse.ArgumentParser(description="Sniff for 802.11 hidden SSIDs")
    ap.add_argument("-i", '--iface', type=str, default=None, help="interface to sniff on")
    args, l = ap.parse_known_args()
    if args.iface == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    try:
        sniff(prn=Analyze, iface=(getargs()).iface)
    except KeyboardInterrupt:
        sys.exit()


if __name__=="__main__":
    main()



