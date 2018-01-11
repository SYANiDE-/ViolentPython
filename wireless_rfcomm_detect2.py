#!/usr/bin/env python2
import bluetooth, sys, argparse


def enumerate_rfcomm(**kw):
    svcs = bluetooth.find_service(address=kw['mac'])
    for serv in svcs:
        name = serv['name']
        proto = serv['protocol']
        port = serv['port']
        print("[+] Found: %s:%s:%s : %s" % (kw['mac'], proto, port, name))

def getargs():
    ap = argparse.ArgumentParser(description="BT RFCOMM scanner")
    ap.add_argument("-m", '--mac', type=str, default=None, help="MAC address")
    args, l = ap.parse_known_args()
    if args.mac == None:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    kw = {}
    args = getargs()
    kw['mac'] = args.mac
    enumerate_rfcomm(**kw)


if __name__=="__main__":
    main()

