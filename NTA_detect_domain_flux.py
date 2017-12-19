#!/usr/bin/env python2
from scapy.all import *
import sys


def QRTest(pk):
    if pk.haslayer(DNSRR) and pk.getlayer(UDP).sport == 53:
        rcode = pk.getlayer(DNS).rcode
        qname = pk.getlayer(DNSQR).qname
        if rcode == 3:
            print("[!] Name lookup failed: %s" % qname)
            return True
        else:
            return False


def main():
    if len(sys.argv) <> 2:
        print("USAGE: %S %S" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        UR = 0
        pk = rdpcap(sys.argv[1])
        for p in pk:
            if QRTest(p):
                UR = UR + 1
        print("[!] %d total unanswered DNS requests" % UR)


if __name__=="__main__":
    main()

