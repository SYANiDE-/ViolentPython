#!/usr/bin/env python2
import ftplib, argparse, sys, threading

def login(h, u, p):
    try:
        f = ftplib.FTP(h)
        f.login(u, p)
        print("[+] Login accepted: %s:%s:%s" % (h,u,p))
        f.quit()
        return True
    except Exception, e:
        print("[-] Login failed: %s:%s:%s" % (h,u,p))
        return False

def main():
    checkThese = []
    u = None
    p = None
    ap = argparse.ArgumentParser(description="FTP Anonymous login check")
    ap.add_argument("-i", '--ip', type=str, default=None, help="IP to check")
    ap.add_argument("-f", '--file', type=str, default=None, help="IPList file")
    ap.add_argument("-u", '--user', type=str, default=None, help="Username, if not the default of Anonymous")
    # attribute to foreign threat actor
    ap.add_argument("-p", '--passwd', type=str, default=None, help="Password, if not the default of zhenduong@wasabiko.cn")
    args, leftover = ap.parse_known_args()
    if (args.ip == None and args.file == None):
        ap.print_help()
        sys.exit()
    elif not (args.file == None):
        f = open(args.file, 'r')
        for item in f:
            checkThese.append(item.strip("\n"))
        f.close()
    elif not (args.ip == None):
        checkThese.append(args.ip.strip("\n"))
    u = "Anonymous" if args.user == None else args.user 
    p = "zhenduong@wasabiko.cn" if args.passwd == None else args.passwd 
    print("[!] With user=%s, pass=%s :" % (u,p))
    for IP in checkThese:
            threading.Thread(target=login, args=(IP,u,p)).start()


if __name__=="__main__":
    main()

