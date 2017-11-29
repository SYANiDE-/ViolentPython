#!/usr/bin/env python2
import sqlite3

# Easier to enum table structure via GUI "sqlitebrowser", which is included in Kali 2.3 by default
# However, "sqlite3 chat_db.sqlite and .database, .table, .schema [tablename] also work for this

def query(db):
    cx = sqlite3.connect(db)
    cc = cx.cursor()
    cc.execute("SELECT CT_ID, ACC_SIGNIN_ADDRESS, CT_URI, CT_GROUP_ID FROM CONTACT_TABLE")
    for i in cc:
        print(i)

def main():
    db = 'chat_db.sqlite'
    query(db)


if __name__=="__main__":
    main()
