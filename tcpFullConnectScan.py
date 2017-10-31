#!/usr/bin/env python2
import socket, argparse, threading


def cx(ip, port):
    xc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        xc.connect((ip, int(port)))
        xc.send("asdf\r\n")
        quack = xc.recv(1024)
        quack = quack.split('\n')[0]
        slock.acquire()
        print("[+] %s %d/tcp open | %s" % (ip, port, quack))
    except:
        slock.acquire()
        print("[-] %s %d/tcp closed" % (ip, port))
    finally:
        slock.release()
        xc.close()


def portscan(host, port_s):
    try:
        targIP = socket.gethostbyname(host)
    except:
        print("[!] Unable to resolve host %s !" % host)
    try:
        targName = socket.gethostbyaddr(targIP)
        print("[:] Scan results for %s" % targName[0])
    except:
        print("[:] Scan results for %s" % targIP)
    socket.setdefaulttimeout(1)
    p = port_s.strip(' ').split(",")
    for port in p:
        threading.Thread(target=cx, args=(host, int(port))).start()



if __name__=="__main__":
    ap = argparse.ArgumentParser(description="TCP Connect Full Scan.  CSV ip/ports in quotes.")
    ap.add_argument('-i', '--inet', type=str,  help="IP")
    ap.add_argument('-p', '--port', type=str,  help="port")
    parsed = ap.parse_args()
    args, leftovers = ap.parse_known_args()
    if args.inet == None or args.port == None:
        ap.print_help()
    slock = threading.Semaphore(value=1)
    i = parsed.inet.strip(' ').split(',')
    for ip in i:
        portscan(ip, parsed.port)


