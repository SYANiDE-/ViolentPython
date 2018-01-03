#!/usr/bin/env python2
import sys, argparse, re
from scapy.all import *

reported = []

NAVPORT = 5556
# I lack a UAV to duplicate and test this attack.  Instead, to practice some of the key concepts, I think I'll make a program that listens for an inbound packet from netcat on the destination port, prints out what layers are in the packet, then prints out the template for each layer.   Then, construct a packet based on this information, and send it back to the netcat listener.


def analyze(pkt):
    if pkt.haslayer(UDP) and pkt.getlayer(UDP).dport == NAVPORT:
        src = pkt.getlayer(UDP).sport
        dst = pkt.getlayer(UDP).dport
        if src not in reported: 
            reported.append(src)
            raw = pkt.sprintf("%Raw.load%")
            layers = list(expandLayers(pkt))
            layers_name_only = list(expandLayers_name_only(pkt))
            print(layers)
            print(layers_name_only)
            print(raw)
            for layer, name in zip(layers, layers_name_only):
                print("\n[-] Layer name: %s" % name)
                print("field, type, curr_val, (def_val)")
                ls(layer)
            temp = duplicate(pkt)
            returnToSender(temp)


def expandLayers_name_only(pkt):
    yield pkt.name
    while pkt.payload:
        pkt = pkt.payload
        yield pkt.name


def expandLayers(pkt):
    yield pkt
    while pkt.payload:
        pkt = pkt.payload
        yield pkt


def duplicate(pkt):
    ether = dEth(pkt)
    ip = dIP(pkt)
    udp = dUDP(pkt)
    raw = dRaw(pkt)
    constructed = ether / ip / udp / raw
    print("\n\n[=] Reconstructed packet:")
    print(list(expandLayers(constructed)))
    return constructed


def dEth(pkt):
    p = pkt.getlayer(Ether)
    src = p.src
    dst = p.dst
    ty = p.type
    PKT = Ether(src=src, dst=dst, type=ty)
    return PKT


def dIP(pkt):
    p = pkt.getlayer(IP)
    version = p.version
    ihl = p.ihl
    tos = p.tos
    ID = p.id
    flags = p.flags
    frag = p.frag
    ttl = p.ttl -1 
    proto = p.proto
    src = p.src
    dst = p.dst
    opt = p.options
    PKT = IP(version=version, ihl=ihl, tos=tos, id=ID, flags=flags, ttl=ttl, proto=proto, src=src, dst=dst, options=opt)
    return PKT


def dUDP(pkt):
    p = pkt.getlayer(UDP)
    sport = p.sport
    dport = p.dport
    PKT = UDP(sport=sport, dport=dport)
    return PKT


def dRaw(pkt):
    PKT = Raw(load='[!] Injected [!]\n')
    return PKT


def returnToSender(pkt):
    sendp(pkt)


def getargs():
    ap = argparse.ArgumentParser(description="Monitor network transmissins of UAVs")
    ap.add_argument('-i', '--iface', type=str, default=None, help="Interface to sniff on")
    args, l = ap.parse_known_args()
    if args.iface == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    sniff(prn=analyze, iface=(getargs()).iface)


if __name__=="__main__":
    main()


