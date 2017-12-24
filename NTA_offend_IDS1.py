#!/usr/bin/env python2
from scapy.all import *
import sys, argparse

notes="""Offend Snort and make it generate IDS alerts."""

def t_ddos(s,d,i,c):
    pkt = IP(src=s, dst=d)/ICMP(type=8, id=678)/Raw(load='1234')
    send(pkt, iface=i, count=c)
    pkt = IP(src=s, dst=d)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
    send(pkt, iface=i, count=c)
    pkt = IP(src=s,dst=d)/UDP(dport=31335)/Raw(load='PONG')
    send(pkt, iface=i, count=c)
    pkt = IP(src=s,dst=d)/ICMP(type=0,id=456)
    send(pkt, iface=i, count=c)
src='192.168.56.180'
dst='192.168.56.1'
iface='eth1'
count=1
for i in range(1,40):
    t_ddos(src,dst,iface,count)

