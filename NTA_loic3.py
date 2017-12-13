#!/usr/bin/env python2
import dpkt, socket, sys


# detect active DDoS attack activity


THRESH = 10000

def searchForAttack(pcap):
    pktCount = {}
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            if dport == 80:
                stream = src+ ":" +dst
                if pktCount.has_key(stream):
                    pktCount[stream] = pktCount[stream] +1
                else:
                    pktCount[stream] =1
        except Exception, X:
            # pass
            print(str(X))
    for stream in pktCount:
        pktsSent = pktCount[stream]
        if pktsSent > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print("[+] "+src+" attacked "+dst+" with "+str(pktsSent)+" pkts")


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        f = open(sys.argv[1], 'r')
        pcap = dpkt.pcap.Reader(f)
        searchForAttack(pcap)
        f.close()


if __name__=="__main__":
    main()


