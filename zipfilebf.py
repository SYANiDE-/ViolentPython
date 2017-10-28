#!/usr/bin/env python2
import zipfile, argparse, sys, threading 

def unz(zipf, pw):
    zf = zipfile.ZipFile(zipf)
    try:
        pw = pw.strip('\n')
        zf.extractall(pwd=pw)
        print("[!] Found! Password = %s" % pw)
        sys.exit()
    except:
        return

if __name__=="__main__":
    ap = argparse.ArgumentParser(description="Dictionary bruteforce password-protected zip file")
    apr = ap.add_argument_group('Required')
    apr.add_argument("-d",  "--dict", type=str, default="", required=True, help="Dictionary file to use as passwords")
    apr.add_argument("-z",  "--zipfile", type=str, default="", required=True, help="Zipfile to bruteforce")
    args = ap.parse_args()
    with open(args.dict, 'r') as d:
        counter=0
        for word in d:
            threading.Thread(target=unz, args=(args.zipfile, word)).start()
            counter+=1
            if counter%100000 == 0:
                print(str(counter/100000) + " x 100k words")
    d.close()
    
