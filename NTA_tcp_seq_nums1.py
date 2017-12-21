#!/usr/bin/env python2
from scapy.all import *
import sys


def guessSeqNumTCP(**kwargs):
    targ = kwargs['targ']
    if 'dport' in kwargs.keys():
        dport = kwargs['dport']
    else:
        dport = 80
    sn = 0
    pn = 0
    diff = 0
    for i in range(1,5):
        if pn != 0:
            pn = sn
        pkt = IP(dst=targ) / TCP(dport=dport)
        ans = sr1(pkt, verbose=0)
        sn = ans.getlayer(TCP).seq
        diff = sn - pn
        print("[+] TCP SEQ DIFF: %s" % (str(diff)))
    return sn + diff


def main():
    if not len(sys.argv) >= 2:
        print("USAGE: %s %s %s" % (sys.argv[0], "[target IP]", "[optional: dst port]"))
        sys.exit
    else:
        kwargs = {}
        kwargs['targ'] = sys.argv[1]
        try:
            kwargs['dport'] = int(sys.argv[2])
        except:
            pass
        sn = guessSeqNumTCP(**kwargs)
        print("[+] TCP_SEQ Predict (future ~ +150 ACK): %d" %(sn))


if __name__=="__main__":
    main()

