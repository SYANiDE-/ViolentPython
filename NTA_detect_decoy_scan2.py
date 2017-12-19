#!/usr/bin/env python2.7
from scapy.all import *
from IPy import IP as IPTEST
import sys


ttlVals = {}
THRESH = 0


def TTL_TEST(p):
    try:
        if p.haslayer(IP):
            src = p.getlayer(IP).src
            ttl = str(p.ttl)
            print("[!] Packet received from %s with TTL %s" % (src, ttl))
            TTL_CHECK(src, ttl)
    except Exception, X:
        print(str(X))


def TTL_CHECK(p, t):
    if IPTEST(p).iptype() == 'PRIVATE':
        return
    if not ttlVals.has_key(p):
        pkt = sr1(IP(dst=p) / ICMP(), retry=0, timeout=1, verbose=0)
        ttlVals[p] = pkt.ttl
    if abs(int(t) - int(ttlVals[p])) > THRESH:
        print("[!] Detected possible spoofed packet from %s, TTL %s, Actual TTL %s" % (p, t, str(ttlVals[p])))


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s" % (sys.argv[0]))
        print("Sniffs traffic, all interfaces. Looking for a large number of hops, +5.  Windows default is 128, Linux 64.  This would indicate spoofed TTL")
        sys.exit()
    else:
        sniff(prn=TTL_TEST, store=0)


if __name__=="__main__":
    main()

