#!/usr/bin/env python2
from scapy.all import *
import argparse, sys, re, datetime

probes = []

def Analyze(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        net = pkt.getlayer(Dot11ProbeReq).info
        src = pkt.addr2
        if net not in probes:
            dt = datetime.datetime.now()
            probes.append(net)
            print("[%s] ProbeReq: %s requested SSID %s" % (dt, src, net))


def getargs():
    ap = argparse.ArgumentParser(description="Sniff for 802.11 probe requests")
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



