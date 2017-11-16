#!/usr/bin/env python2
import ftplib, sys, getpass

def searchDefault(ftpobj):
    try:
        dirlist = ftp.nlst()
    except:
        dirlist = []
        print("[-] No listing or unable")
        print("[-] Skipping host")
        return
    retlist=[]
    # print("[!] Files found: %s" % dirlist)
    for f in dirlist:
        fn = f.lower()
        filetypes=['.php', '.html', '.asp']
        for item in filetypes:
            if item in fn:
                print("[!] Found: %s" % fn)
                retlist.append(f)
    return retlist

arglen = len(sys.argv)
if not arglen == 3:
    print("Error!   Need args host(1) and user(2)")
    sys.exit()
host = sys.argv[1]
user = sys.argv[2]
passwd = getpass.getpass()
print("[.] Attempting to connect: %s:%s" % (host,user))
ftp = ftplib.FTP(host)
ftp.login(user,passwd)
#print(searchDefault(ftp))
searchDefault(ftp)

