#!/usr/bin/env python2
from scapy.all import *
import sys, argparse, random, os, time


ntalkdBOF="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8"
mountdBOF="^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F"


def t_ddos1(s,d,i,c):
    pkt = IP(src=s, dst=d)/ICMP(type=8, id=678)/Raw(load='1234')
    send(pkt, iface=i, count=c)


def t_ddos2(s,d,i,c):
    pkt = IP(src=s, dst=d)/ICMP(type=0)/Raw(load='AAAAAAAAAA')
    send(pkt, iface=i, count=c)


def t_ddos3(s,d,i,c):
    pkt = IP(src=s,dst=d)/UDP(dport=31335)/Raw(load='PONG')
    send(pkt, iface=i, count=c)


def t_ddos4(s,d,i,c):
    pkt = IP(src=s,dst=d)/ICMP(type=0,id=456)
    send(pkt, iface=i, count=c)


def t_exploit1(s,d,i,c):
    pkt = IP(src=s, dst=d)/UDP(dport=518)/Raw(load=ntalkdBOF)
    send(pkt, iface=i, count=c)


def t_exploit2(s,d,i,c):
    pkt = IP(src=s, dst=d)/UDP(dport=635)/Raw(load=mountdBOF)
    send(pkt, iface=i, count=c)


def t_recon1(s,d,i,c):
    pkt = IP(src=s, dst=d)/UDP(dport=7)/Raw(load="cybercop")
    send(pkt, iface=i, count=c)


def t_recon2(s,d,i,c):
    pkt = IP(src=s, dst=d)/UDP(dport=10081)/Raw(load="Amanda")
    send(pkt, iface=i, count=c)


def getargs():
    ap = argparse.ArgumentParser(description="IDS noise generator MKv1.  Note that specific IDS-offending signatures/attacks are triggered randomly for greater \"humanization\"")
    ap.add_argument("-s", '--src', type=str, default=None, help="Source IP for generated packets")
    ap.add_argument("-d", '--dst', type=str, default=None, help="Dest IP for generated packets")
    ap.add_argument("-i", '--intfc', type=str, default=None, help="Interface for sending generated packets")
    ap.add_argument("-c", '--count', type=int, default=None, help="Number of successive times, upon each call, to fire the specific signature/attack. (--count * --total == grand total)")
    ap.add_argument("-t", '--total', type=int, default=None, help="Total function calls to make.  (--count * --total == grand total")
    ap.add_argument("-m", '--maxsleep', type=int, default=None, help="randint(0,X) where X == Maximum seconds to sleep in between calls")
    args, l = ap.parse_known_args()
    aaargs = vars(args)
    if None in aaargs.values():
        ap.print_help()
        sys.exit()
    else:
        return aaargs


def main():
    funcs = {1:t_ddos1, 2:t_ddos2, 3:t_ddos3, 4:t_ddos4, 5:t_exploit1, 6:t_exploit2, 7:t_recon1, 8:t_recon2}
    args = getargs()
    # print(args)
    s=args['src']
    d=args['dst']
    i=args['intfc']
    c=args['count']
    t=args['total']
    m=args['maxsleep']
    for iterator in range(1,t):
        time.sleep(random.randint(0,m))
        funcs[random.randint(1,8)](s,d,i,c)


if __name__=="__main__":
    main()

