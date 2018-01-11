#!/usr/bin/env python2
import bluetooth, sys, argparse


def detect_rfcomm(**kw):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        sock.connect(kw['mac'], kw['port'])
        print("[+] RFCOMM host %s Port %s open" % (kw['mac'], kw['port']))
    except Exception, e:
        print("[+] RFCOMM host %s Port %s closed" % (kw['mac'], kw['port']))
    finally:
        sock.close()

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
    # kw['mac'] = '10:F1:F2:FF:FF:FF'  # nulling last three bytes for Github upload
    kw['mac'] = args.mac
    for port in range(1,30):
        kw['port'] = port
        detect_rfcomm(**kw)


if __name__=="__main__":
    main()

