#!/usr/bin/env python2
import mechanize, sys, datetime, argparse


def get_source(url, proxy={}):
    try:
        br = mechanize.Browser()
        print(proxy)
        if len(proxy) != 0:
            br.set_proxies(proxy)
        pg = br.open(url)
        src = pg.read()
        print(src)
    except KeyboardInterrupt:
        sys.exit()
    except Exception, X:
        print(str(X))


def getargs():
    ap = argparse.ArgumentParser(description="Retrieve sourcd code (client-side available) through a PROXY")
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
    args = getargs()
    if args.proxyip != None:
        proxy[args.proxymeth] = args.proxyip +":"+ str(args.proxyport)
        print(proxy)
    get_source(args.url, proxy)
        

if __name__=="__main__":
    main()



