#!/usr/bin/env python2
import mechanize, cookielib, random, datetime, argparse, sys


class anonBrowser(mechanize.Browser):
    # anonBrowser() extends mechanize.Browser() with proxying, User-agent spoofing, and cookie management
    def __init__(s, proxies=[], user_agents=[]):
        mechanize.Browser.__init__(s)
        s.debug(False)
        s.set_handle_robots(False)
        s.proxies = s.__getproxies()
        s.user_agents = s.__getUserAgents() 
        s.cookie_jar = cookielib.LWPCookieJar()
        s.set_cookiejar(s.cookie_jar)
        s.anonymize()


    def __getproxies(s):
        pg = s.open("http://spys.me/proxy.txt") # https://github.com/clarketm/proxy-list/blob/master/proxy-list.txt
        src = pg.read().split("\n")
        clean = []
        for item in src:
            if "+" in item and "." in item and ":" in item:
                clean.append(item.split(" ")[0])
        for x in range(0,5):
            clean.pop()[0]
        return clean


    def __getUserAgents(s):
        pg = s.open("https://gist.githubusercontent.com/ruXlab/25d711c275f220fc5a425b64afeb34f7/raw/d5ec259612e4749ae5adecabc29cd2dc8481901e/useragents.txt") #  a list of user agents
        src = pg.read().split("\n")
        return src

    def ANON_VARS(s):
        print(s.proxies)
        print(s.user_agents)
        print("[%s] # Proxies: %s" %  (datetime.datetime.now(), len(s.proxies)))
        print("[%s] # User-agents: %s" %  (datetime.datetime.now(), len(s.user_agents)))

        

    def debug(s, val):
        if val == True:
            s.DEBUG=1
        else:
            s.DEBUG=0


    def clear_cookies(s):
        s.cookie_jar = cookielib.LWPCookieJar()
        s.set_cookiejar(s.cookie_jar)
        if s.DEBUG == 1:
            print("[%s] Cleared cookies" % datetime.datetime.now())

    def change_user_agent(s):
        index = random.randrange(0, len(s.user_agents))
        s.add_headers = [('User-agent', (s.user_agents[index]))]
        if s.DEBUG == 1:
            print("[%s] %s" % (datetime.datetime.now(), [('User-agent', (s.user_agents[index]))]))

    def change_proxy(s):
        if s.proxies:
            index = random.randrange(0, len(s.proxies))
            s.set_proxies({'http' : s.proxies[index]})
            if s.DEBUG == 1:
                print("[%s] using proxy: %s" % (datetime.datetime.now(), {'http' : s.proxies[index]}))


    def anonymize(s, sleep=False, sleepintvl=60):
        s.clear_cookies()
        s.change_proxy()
        s.change_user_agent()
        if sleep:
            if s.DEBUG == 1:
                print("[%s] Sleeping for %s secs" % (datetime.datetime.now(), sleepintvl))
            time.sleep(60)
        

def main():
    # anonBrowser()
    pass

if __name__=="__main__":
    main()



