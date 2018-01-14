#!/usr/bin/env python2
import mechanize, sys, datetime, argparse


# http://www.useragentstring.com/pages/useragentstring.php for a list of valid user agent strings
# Fake a real user agent of different OS:
# Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3pre) Gecko/20100403 Lorentz/3.6.3plugin2pre (.NET CLR 4.0.20506)

def get_source(url, useragent=[('User-agent', "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre")], proxy={}):
    try:
        br = mechanize.Browser()
        print(proxy)
        if len(proxy) != 0:
            br.set_proxies(proxy)
        br.addheaders = useragent
        pg = br.open(url)
        src = pg.read()
        print(src)
    except KeyboardInterrupt:
        sys.exit()
    except Exception, X:
        print(str(X))


def getargs():
    ap = argparse.ArgumentParser(description="Retrieve sourcd code (client-side available) through a PROXY.  Additionally send spoofed userAgent, possibly also spoofing OS")
    ap.add_argument('-u', '--url', type=str, default=None, help="Url of web resource to retrieve.")
    ap.add_argument('-pM', '--proxymeth', type=str, default=None, help="Proxy method (http, socks5, etc)")
    ap.add_argument('-pI', '--proxyip', type=str, default=None, help="Proxy method (http, socks5, etc)")
    ap.add_argument('-pP', '--proxyport', type=int, default=None, help="Proxy port")
    args, l = ap.parse_known_args()
    if args.url == None:
        ap.print_help()
        sys.exit()
    else:
        return args 


def main():
    proxy = {}
    UserAgent = [('User-agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3pre) Gecko/20100403 Lorentz/3.6.3plugin2pre (.NET CLR 4.0.20506)")]
    args = getargs()
    if args.proxyip != None:
        proxy[args.proxymeth] = args.proxyip +":"+ str(args.proxyport)
        print(proxy)
    get_source(args.url, UserAgent, proxy)


if __name__=="__main__":
    main()
