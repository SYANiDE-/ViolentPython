#!/usr/bin/env python2
import dpkt, socket, sys, pygeoip


geo = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')


def reader(pcap, C, L):
    for (a, b) in pcap:
        try:
            ip = dpkt.ethernet.Ethernet(b).data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            sloc, scoor = _geo(src)
            dloc, dcoor = _geo(dst)
            print("[+] %s, %s, %s, %s"  % ("S:"+src, "D:"+dst, sloc+":"+scoor, dloc+":"+dcoor))
            if scoor not in C and '...' not in scoor:
                 C.append(scoor)
                 L.append("""<Placemark><name>"""+src+"""</name><Point><coordinates>"""+scoor.replace(":",",")+"""</coordinates></Point></Placemark>""")
            if dcoor not in C and '...' not in dcoor:
                 C.append(dcoor)
                 L.append("""<Placemark><name>"""+dst+"""</name><Point><coordinates>"""+dcoor.replace(":",",")+"""</coordinates></Point></Placemark>""")
        except Exception, X:
            pass


def _geo(ip):
    GEO = '...'
    COORD = '...'
    q = geo.record_by_name(ip)
    if q != None:
        city = q['metro_code'].replace(', ', ':')
        country = q['country_code3']
        lon = q['longitude']
        lat = q['latitude']
        if city != '' and country != '':
            GEO = "'"+city+ ":" +country+"'"
        elif city == '' and country != '':
            GEO = country
        if lat != '' and lon != '':
            COORD = str(lon)+":"+str(lat)
    return GEO, COORD


def main():
    COORDS = []
    LINES = []
    if len(sys.argv) != 2:
        print("USAGE: %s %s" % (sys.argv[0], "[pcap file]"))
        sys.exit()
    else:
        f = open(sys.argv[1], 'r')
        p = dpkt.pcap.Reader(f)
        LINES.append("<?xml version='1.0' encoding='UTF-8'?><kml xmlns='http://www.opengis.net/kml/2.2'><Document>")
        reader(p, COORDS, LINES)
        f.close()
        LINES.append("</Document></kml>")
        print("[!] Writing KML (Google Earth) to outfile: %s" % (sys.argv[0].replace('.py', '.kml')))
        f = open(sys.argv[0].replace('.py', '.kml'), 'w')
        for item in LINES:
            f.write(item)
        f.close()


if __name__=="__main__":
    main()

