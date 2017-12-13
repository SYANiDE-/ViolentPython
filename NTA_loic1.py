#!/usr/bin/env python2
import dpkt, socket, sys


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


def main():
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        f = open(sys.argv[1], 'r')
        pcap = dpkt.pcap.Reader(f)
        search(pcap)
        f.close()


if __name__=="__main__":
    main()


