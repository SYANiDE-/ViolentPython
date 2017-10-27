#!/usr/bin/env python2
import crypt as C 
import sys

results = []

def usage():
    print(\
"""[!] USAGE: """+sys.argv[0]+""" +:
    [1] [pw] [salt] [algorithm]
        crypt a password, salt combo
    [2] [dict_file] [hash]
        dict bruteforce single hash
    [3] [dict_file] [hash_file] 
        dict bruteforce hashes in file

For [algorithm], where relevant, use:
des
md5
sha256
sha512

Example hashes that can be accepted:
DES:     ZUlEM0Qn0KMlQ
MD5:     $1$E9f9WqDY$up3YDQYIDYtoaPAul6mj00
sha256:  $5$E9f9WqDY$TdcW8Gm6/ERqnGrpHtSOociFRrpfrhJA9taKpxwMZl5
sha512:  $6$E9f9WqDY$uhWjOkF5MAlGbRYWf4VshRGzZx03s2ZKmEOBYIChZa1KLLpvpyBScQI6x8jFqKTGt4Id8PD5xuKlFp7UriI0f1 
""")
    sys.exit()


def crypt(listitem):
    algs = { 'des':'', 'md5':'$1$', 'sha256':'$5$', 'sha512':'$6$' }
    li = []
    preamble = ''
    for x in listitem:
        li.append(x)
    if len(li) == 3:
        if li[2] in algs.keys():
            preamble=algs[li[2]]
    try:
        print(C.crypt(li[0], preamble + li[1]))
    except:
        usage()


def decrypt(listitem):
    global results
    li = []
    for x in listitem:
        li.append(x)
    target=li[1]
    if target.find('$') != -1:  #if target contain '$', then not DES
        sss = target.split('$')
        if sss[0] == '':
            sss.pop(0)
        salt = '$'+sss[0]+'$'+sss[1]
    else:  # no '$'?  Then must be DES
        salt=target[0:2] 
        print "[..] PW, SALT: ", target, salt
    with open(li[0], 'r') as f:
        for candidate in f:
            subj = C.crypt(candidate.strip('\n'), salt)
            print(subj, candidate.strip('\n'))
            if subj == target:
                results.append(str("  [!] Match found! "+target+" = "+candidate))
                print(results[-1])
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



