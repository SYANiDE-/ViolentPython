#!/usr/bin/env python2
import sqlite3

# USING:  Sky (Linux Skype alternative client)

def query(db):
    cx = sqlite3.connect(db)
    cc = cx.execute("SELECT IM_MSG_TYPE, IM_SENDER_URI, IM_CHAT_URI, IM_ACC_URI,datetime(IM_TIMESTAMP_MS, 'unixepoch') as ts, IM_CONTENT FROM IM_TABLE")
    print("[!] Timestamp, From, To, Message")
    for i in cc:
        if int(i[0]) == 0:
            FROM = str(i[1])
            TO = str(i[2])
            if FROM != TO:
                print("%s:::%s:::%s:::%s" % (str(i[4]), FROM, TO, str(i[5])))
        elif int(i[0]) == 1:
            FROM = str(i[1])
            TO = str(i[3])
            if FROM != TO:
                print("%s:::%s:::%s:::%s" % (str(i[4]), FROM, TO, str(i[5])))
        else:
            pass

def main():
    db = 'chat_db.sqlite'
    query(db)


if __name__=="__main__":
    main()
