#!/usr/bin/env python2
import smtplib, argparse, sys, datetime, getpass
from email.mime.text import MIMEText

def sendthatshit(usr, recip, subj, txt):
    msg = MIMEText(txt)
    msg['From'] = usr
    msg['To'] = recip
    msg['Subject'] = subj
    try:
        SRV = smtplib.SMTP('smtp.gmail.com', 587)
        print("[%s] CX to Google:587" % (datetime.datetime.now()))
        SRV.ehlo()
        print("[%s] TLS handshake" % (datetime.datetime.now()))
        SRV.starttls()
        SRV.ehlo()
        print("[%s] Logging in... using account %s" % (datetime.datetime.now(), usr))
        SRV.login(usr, getpass.getpass())
        print("[%s] Sending mail..." % (datetime.datetime.now()))
        SRV.sendmail(usr, recip, msg.as_string())
        SRV.close()
        print("[%s] Sent." % (datetime.datetime.now()))
    except Exception, X:
        print(str(X))
        print("[%s] FAILED" % (datetime.datetime.now()))


def getargs():
    ap = argparse.ArgumentParser(description="Send email via Google authenticated TLS")
    ap.add_argument('-u', '--user', type=str, default=None, help='AUTH user')
    ap.add_argument('-r', '--recipient', type=str, default=None, help='Recipient address')
    ap.add_argument('-s', '--subj', type=str, default=None, help='Subject line')
    ap.add_argument('-b', '--body', type=str, default=None, help='Email body')
    args, l = ap.parse_known_args()
    ARGS = vars(args)
    if None in ARGS.values():
        ap.print_help()
        sys.exit()
    else:
        return args


def main():
    args = getargs()
    sendthatshit(args.user, args.recipient, args.subj, args.body)


if __name__=="__main__":
    main()



        
        
