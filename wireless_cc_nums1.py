#!/usr/bin/env python2
import re


def ccSearch(inp):
    Finder = {}
    Finder["AmEx"] = re.findall("3[47][0-9]{13}",inp) or 0
    Finder["MC"] = re.findall("5[1-5][0-9]{14}",inp) or 0
    Finder["Visa"] = re.findall("4[0-9]{12}(?:[0-9]{3})?",inp) or 0
    printer(Finder)


def printer(ZZ):
    for key, value in ZZ.iteritems():
        if value != 0:
            print("[+] %s # %s" % (key, ", ".join(value)))


def main():
    a = ccSearch("this is a test of # 341111111111111\nand also 5311111111111111")


if __name__=="__main__":
    main()
