#!/usr/bin/env python2

from pyPdf import PdfFileReader 
import argparse, sys

def Meta(f):
    PDF = PdfFileReader(file(f,'r'))
    dox = PDF.getDocumentInfo()
    print("[=] PDF Metadata in: %s" % str(f))
    for meta in dox:
        print("[+] %s:%s" % (meta, dox[meta]))

def getargs():
    ap = argparse.ArgumentParser(description="PDF metadata dump")
    ap.add_argument('-f', '--file', type=str, default=None, help="The PDF file")
    args, l = ap.parse_known_args()
    if args.file == None:
        ap.print_help()
        sys.exit()
    else:
        return args.file


def main():
    f = ""
    try:
        f = getargs()
    except:
        sys.exit()
    Meta(f)

if __name__=="__main__":
    main()
