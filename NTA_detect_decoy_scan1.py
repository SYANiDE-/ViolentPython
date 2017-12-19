#!/usr/bin/env python2.7
from scapy.all import sniff, IP
import sys

def TTL_TEST(p):
    try:
        if p.haslayer(IP):
            src = p.getlayer(IP).src
            ttl = str(p.ttl)
            print("[!] Packet received from %s with TTL %s" % (src, ttl))
    except Exception, X:
        print(str(X))


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        sniff(prn=TTL_TEST, store=0)

if __name__=="__main__":
    main()

