#!/usr/bin/env python2
import web_AnonBrowserClass as WAB, datetime

url = "http://www.kittenwar.com"
ab = WAB.anonBrowser()
ab.debug(True)
for itera in range(1,5):
    ab.anonymize()
    print("[%s] fetching page %s" % (datetime.datetime.now(), url))
    res = ab.open(url)
    for cookie in ab.cookie_jar:
        print("%s" % cookie)




