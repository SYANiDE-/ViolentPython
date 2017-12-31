#!/usr/bin/env python2
from scapy.all import *
import argparse, sys, re, datetime


hidden = []
unhidden = []


def Analyze(pkt):
    if pkt.haslayer(Dot11ProbeResp):
        src = pkt.getlayer(Dot11).addr2
        if src in hidden and src not in unhidden:
            dt = datetime.datetime.now()
            net = pkt.getlayer(Dot11ProbeResp).info
            unhidden.append(src)
            print("[%s] Detected: Probe Response: Hidden SSID \"%s\", mac %s" % (dt, net, src))
    if pkt.haslayer(Dot11Beacon):
        if pkt.getlayer(Dot11Beacon).info == "":
            src = pkt.getlayer(Dot11).addr2
            if src not in hidden:
                dt = datetime.datetime.now()
                hidden.append(src)
                print("[%s] Detected: Beacon frame w/hidden SSID, mac %s" % (dt, src))


def getargs():
    ap = argparse.ArgumentParser(description="Sniff for 802.11 hidden SSID in beacon and decloak SSID BSSID via probe response")
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



