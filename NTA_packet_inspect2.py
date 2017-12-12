#!/usr/bin/env python2
import dpkt, socket, sys, pygeoip


geo = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def reader(pcap):
    for (a, b) in pcap:
        try:
            ip = dpkt.ethernet.Ethernet(b).data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print("[+] %-20s %-20s %-25s %-25s"  % ("S:"+src, "D:"+dst, _geo(src), _geo(dst)))
        except Exception, E:
            print(str(E))


def _geo(ip):
    try:
        q = geo.record_by_name(ip)
        city = q['metro_code'].replace(', ', ':')
        country = q['country_code3']
        if city != '':
            GEO = "'"+city+ ":" +country+"'"
        else:
            GEO = country
        return GEO
    except Exception, X:
        return '...'


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

