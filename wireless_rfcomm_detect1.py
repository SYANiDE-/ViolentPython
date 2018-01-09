#!/usr/bin/env python2
import bluetooth


def detect_rfcomm(**kw):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        sock.connect(kw['mac'], kw['port'])
        print("[+] RFCOMM host %s Port %s open" % (kw['mac'], kw['port']))
    except Exception, e:
        print("[+] RFCOMM host %s Port %s closed" % (kw['mac'], kw['port']))
    finally:
        sock.close()


def main():
    kw = {}
    kw['mac'] = '10:F1:F2:F0:85:BB'
    for port in range(1,30):
        kw['port'] = port
        detect_rfcomm(**kw)


if __name__=="__main__":
    main()
