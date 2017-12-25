#!/usr/bin/env python2
from scapy.all import *
import sys

def PrnPKT(p):
    if p.haslayer(Dot11Beacon):
        print("[+] Detected 802.11 Beacon Frame")
    elif p.haslayer(Dot11ProbeReq):
        print("[+] Detected 802.11 Probe Request Frame")
    elif p.haslayer(TCP):
        print("[+] Detected a TCP Packet")
    elif p.haslayer(DNS):
        print("[+] Detected a DNS Packet")
conf.iface="mon0"
sniff(prn=PrnPKT)

