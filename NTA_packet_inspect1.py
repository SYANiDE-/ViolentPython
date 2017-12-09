#!/usr/bin/env python2
import dpkt, socket, sys


def reader(pcap):
    for (a, b) in pcap:
        try:
            ip = dpkt.ethernet.Ethernet(b).data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print("[+] %-20s %-20s" % ("S:"+src, "D:"+dst))
        except Exception, E:
            print(str(E))


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        f = open(sys.argv[1], 'r')
        p = dpkt.pcap.Reader(f)
        reader(p)


if __name__=="__main__":
    main()

