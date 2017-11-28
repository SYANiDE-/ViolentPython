#!/usr/bin/env python2
import sqlite3


def sqlprint(DB):
    cx = sqlite3.connect(DB)
    c = cx.cursor()
    try:
        # Sky linux (Skype alternative)
        # ACC_TABLE is Sky synonym for Accounts table
        # ACC_TABLE cols:
        # ACC_ID,ACC_SIGNIN_ADDRESS,ACC_USERNAME,ACC_SIP_DOMAIN,ACC_AUTH_DOMAIN,ACC_AUTH_USER,ACC_PASSWORD,ACC_REM_SERVER,ACC_REM_PORT,ACC_REM_IS_INTERNAL,ACC_LAST_LOGIN_TIME,ACC_LOGIN_COUNT,ACC_LOGIN_FAILED_COUNT,ACC_IS_REMEMBERED,ACC_IS_AUTO_SIGNIN,ACC_NAME,ACC_EMAIL,ACC_PHONE_NUMBER,ACC_EPID,ACC_UUID
        c.execute("SELECT ACC_ID, ACC_SIGNIN_ADDRESS, ACC_NAME, ACC_USERNAME, ACC_AUTH_USER, ACC_PASSWORD, ACC_EMAIL  FROM ACC_TABLE;")
        print("ACC_ID, ACC_SIGNIN_ADDRESS, ACC_NAME, ACC_USERNAME, ACC_AUTH_USER, ACC_PASSWORD, ACC_EMAIL") 
        for row in c:
            print(row)
    except:
        pass
    try:
        # Skype
        c.execute("SELECT fullname, skypename, city, country, datetime(profile_timestamp, 'unix_epoch') from Accounts;")
        print("fullname, skypename, city, country, timestamp")
        for row in c:
            print(row)
    except:
        pass


def main():
    # Sky linux = Skype alternative;  
    # chat_db.sqlite (Sky) == main.db (Skype)
    try:
        # Sky linux
        db = "chat_db.sqlite"
        sqlprint(db)
    except:
        pass
    try:
        # Skype
        db = "main.db"
        sqlprint(db)
    except:
        pass



if __name__=="__main__":
    main()
