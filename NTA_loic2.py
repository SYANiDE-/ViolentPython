#!/usr/bin/env python2
import dpkt, socket, sys


# detect "Hivemind" DDoS attack

def searchForHive(pcap):
    for (ts, buf) in pcap:
        try:
            direction=''
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            sport = tcp.sport
            dport = tcp.dport
            if dport == 6667:
                s, d = 'sent', 'to'
            elif sport == 6667:
                s, d = 'received', 'from'
            if s != '' and d != '' and '!lazor' in tcp.data.lower():
                print("[!] Hivemind DDoS detected!")
                print("[+] %s %s CMD %s %s: %s" % (str(src+ ":" +str(sport)), s, d, str(dst+ ":" +str(dport)), tcp.data))
        except Exception, X:
            # print(str(X))
            pass


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        f = open(sys.argv[1], 'r')
        pcap = dpkt.pcap.Reader(f)
        searchForHive(pcap)
        f.close()


if __name__=="__main__":
    main()


