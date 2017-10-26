#!/usr/bin/env python2
import crypt as C 
import sys

results = []

def usage():
    print(\
"""[!] USAGE: """+sys.argv[0]+""" +:
    [1] [pw] [salt]
        crypt a password, salt combo
    [2] [dict_file] [hash]
        dict bruteforce single hash
    [3] [dict_file] [hash_file]
        dict bruteforce hashes in file
""")
    sys.exit()


def crypt(listiten):
    li = []
    for x in listitem:
        li.append(x)
    try:
        print(C.crypt(li[0], li[1]))
    except:
        usage()


def decrypt(listitem):
    global results
    li = []
    for x in listitem:
        li.append(x)
    target=li[1]
    salt=target[0:2]
    print "[..] PW, SALT: ", target, salt
    with open(li[0], 'r') as f:
        for candidate in f:
            subj = C.crypt(candidate.strip('\n'), salt)
            print(subj, candidate.strip('\n'))
            if subj == target:
                results.append(str("  [!] Match found! "+target+" = "+candidate))
                print(results[-1])
                # sys.exit()
    f.close()


def multidecrypt(listitem):
    li = []
    for x in listitem:
        li.append(x)
    with open(li[1], 'r') as f:
        for candidate in f:
            lo = []
            lo.append(li[0])
            lo.append(candidate.strip('\n'))
            decrypt(lo)
    f.close()

 

if __name__=="__main__":
    modes = { 1:crypt, 2:decrypt, 3:multidecrypt }
    args = sys.argv[2:] if len(sys.argv) >= 2 else ""
    if len(sys.argv) == 1:
        usage()
    modes[int(sys.argv[1])](args)
    if len(results) >= 1:
        print("\n### ### ### ### ###\n")
        for x in range(0, len(results)):
            print(results[x])



