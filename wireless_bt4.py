#!/usr/bin/env python2
import datetime, argparse, sys
from scapy.all import *

# Not finding my target device in wireless traffic... is this iPhone-specific?
# Could not verify!
# Pixel 2 XL via LG Electronics (apparently)
# 10:F1:F2:xx:xx:xx


def wifi_find_mac(pkt, vMac='10:F1:F2'):
    if pkt.haslayer(Dot11):
        MAC = pkt.getlayer(Dot11).addr2
        if str(vMac).lower() == str(MAC)[:8].lower():
            print("[%s] Detected target vendor OUI %s : >  \"%s\"" % (datetime.datetime.now(), vMac, MAC))


def getargs():
    ap = argparse.ArgumentParser(description="Detect vendor OUI in MAC address floating 802.11")
    ap.add_argument('-i', '--iface', type=str, default=None, help='Interface to capture on (suggest Wlan)')
    ap.add_argument('-o', '--oui', type=str, default=None, help='Vendor OUI portion of mac address to search for.  @Example:  ab:cd:ef')
    args, l = ap.parse_known_args()
    if args.iface == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    args=getargs()
    if args.oui:
        sniff(iface=args.iface, prn=wifi_find_mac(args.oui))
    else:
        sniff(iface=args.iface, prn=wifi_find_mac)


if __name__=="__main__":
    main()

