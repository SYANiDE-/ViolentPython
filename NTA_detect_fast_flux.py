#!/usr/bin/env python2
from scapy.all import *


records = {}
min_count = 5  # we only care if the domain name has more than min_count IPs associated with it.

def examine(pk):
    if pk.haslayer(DNSRR):
        rname = pk.getlayer(DNSRR).rrname
        rdata = pk.getlayer(DNSRR).rdata
        if records.has_key(rname):
            if rdata not in records[rname]:
                records[rname].append(rdata)
        else:
            records[rname] = []
            records[rname].append(rdata)


def main():
    if len(sys.argv) <> 2:
        print("USAGE: %s %s" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        pk = rdpcap(sys.argv[1])
        for pkt in pk:
            examine(pkt)
        for rec in records:
            if len(records[rec]) >= min_count:
                print("[+] %s has %s unique IPs" % (rec, str(len(records[rec]))))


if __name__=="__main__":
    main()

