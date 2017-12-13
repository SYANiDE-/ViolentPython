#!/usr/bin/env python2
import dpkt, socket, sys


THRESH = 10000

def search(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)
            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri.lower() and 'loic' in uri.lower():
                    print('[!] '+src+' Downloaded LOIC')
        except Exception, X:
            # print(str(X))
            pass


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
        search(pcap)
        searchForHive(pcap)
        searchForAttack(pcap)
        f.close()


if __name__=="__main__":
    main()


