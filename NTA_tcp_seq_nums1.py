#!/usr/bin/env python2
from scapy.all import *
import sys


def guessSeqNumTCP(targ):
    sn = 0
    pn = 0
    diff = 0
    for i in range(1,5):
        if pn != 0:
            pn = sn
        pkt = IP(dst=targ) / TCP()
        ans = sr1(pkt, verbose=0)
        sn = ans.getlayer(TCP).seq
        diff = sn - pn
        print("[+] TCP SEQ DIFF: %s" % (str(diff)))
    return sn + diff


def main():
    if len(sys.argv) <> 2:
        print("USAGE: %s %s" % (sys.argv[0], "[target IP]"))
        sys.exit
    else:
        targ = sys.argv[1]
        sn = guessSeqNumTCP(targ)
        print("[+] TCP_SEQ Predict (future ~ +150 ACK): %d" %(sn))


if __name__=="__main__":
    main()

