#!/usr/bin/env python2
from scapy.all import *
import argparse, sys, re

helptxt = {}
helptxt['pkt.sprintf("%Raw.load%")'] = """
Ctrl chars are not evaluated

'POST /lol.txt HTTP/1.1\r\nHost: 127.0.0.1\r\nUser-Agent: curl/7.57.0\r\nAccept: */*\r\nContent-Length: 22\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nthis=abra&that=cadavre'
"""
helptxt['pkt.getlayer(Raw)'] = """
Ctrl chars are evaluated

POST /lol.txt HTTP/1.1
Host: 127.0.0.1
User-Agent: curl/7.57.0
Accept: */*
Content-Length: 22
Content-Type: application/x-www-form-urlencoded

this=abra&that=cadavre
"""


def Analyze(pkt):
    # there are two different methods for assigning the raw data.
    # The method chosen determines the output format (see help)
    pload = pkt.sprintf("%Raw.load%")
    # pload = pkt.getlayer(Raw)
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



