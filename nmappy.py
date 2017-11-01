#!/usr/bin/env python2
import nmap, argparse, sys

def scanner(host, port):
    PORTS=port.split(',')
    nma = nmap.PortScanner()
    nma.scan(host, port)
    for x in PORTS:
        state=nma[host]['tcp'][int(x)]['state']
        print("[..] %s %d/port %s" % (host, int(x), state))

if __name__=="__main__":
    ap=argparse.ArgumentParser(description="Nmap port scanner written in Python")
    ap.add_argument('-i', '--ip', type=str, help="IP")
    ap.add_argument('-p', '--port', type=str, help='Port(s)')
    args=ap.parse_args()
    a, b = ap.parse_known_args()
    if a.ip == None or a.port == None:
        ap.print_help()
        sys.exit()
    IPs = args.ip.split(',')
    for x in IPs:
        scanner(x.strip(' '), args.port)



