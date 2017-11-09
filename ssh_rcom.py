#!/usr/bin/env python2
import pexpect.pxssh, argparse, sys, getpass

def snd(sock, cmd):
    sock.sendline(cmd)
    sock.prompt()
    print(sock.before)


def connect(u, h, p):
    try:
        sock = pexpect.pxssh.pxssh()
        sock.login(h, u, p)
        return sock
    except:
        print("[!!] Error connecting")
        sys.exit(0)


if __name__=="__main__":
    ap = argparse.ArgumentParser(description="SSH remote command")
    ap.add_argument('-u', '--user', type=str, help="user")
    ap.add_argument('-H', '--host', type=str, help='host')
    ap.add_argument('-c', '--command', type=str, help='command')
    args = ap.parse_args()
    a, l = ap.parse_known_args()
    if a.user == None or a.host == None or a.command == None:
        ap.print_help()
        sys.exit()
    sock = connect(args.user, args.host, getpass.getpass())
    snd(sock, args.command)

