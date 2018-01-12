#!/usr/bin/env python2
import obexftp, datetime, sys, argparse


def pushit(mac,fd, port):
    try:
        obexTarg = obexftp.client(obexftp.BLUETOOTH)
        obexTarg.connect(mac, port)
        obexTarg.put_file(fd)
        print("[%s] Pushed file %s to target %s" % (datetime.datetime.now(), fd, mac))
    except:
        print("[%s] Failed OBEXFTP push file %s to target %s" % (datetime.datetime.now(), fd, mac))


def getargs():
    ap = argparse.ArgumentParser(description="Push file to target via OBEXFTP")
    ap.add_argument('-m', '--mac', type=str, default=None, help="Bluetooth target MAC")
    ap.add_argument('-f', '--file', type=str, default=None, help="File to upload")
    ap.add_argument('-p', '--port', type=int, default=None, help="ObexFTP port (use ./wireless_rfcomm_detect2.py to scan ports)")
    args, l = ap.parse_known_args()
    argues = vars(args)
    if None in argues:
        ap.print_help()
        sys.exit()
    else:
        return argues


def main():
    args = getargs()
    pushit(args['mac'], args['file'], args['port'])


if __name__=="__main__":
    main()


