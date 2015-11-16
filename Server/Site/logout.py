#!/usr/bin/env python3

#deletes user's session from db
import cgi
import html
import http.cookies as Cookies
import sys
import os

sys.path.insert(0,os.getcwd()+"../tools")
from DatabaseConnection import DatabaseConnection
import redirect
import template


form=cgi.FieldStorage()
#import checkcookie
#import redirect

cook=Cookies.SimpleCookie()

print ("Content-Type:text/html")
validcook=True
d=0
DB_conn=DatabaseConnection()

if os.environ.get("HTTP_COOKIE"):
    cook.load(os.environ["HTTP_COOKIE"])

    d=cook["session"].value
    u=DB_conn.checkcookie(d)  #checkcookie.checkcookie(cook["session"].value)
    if not u:
        validcook=False
else:
    validcook=False
if validcook:
    #m=MongoClient()
    #g=m.unisq
    #db=g.Session

    DB_conn.remove_session({"_id":int(d)})
    print (redirect.redirect())
else:
    print (redirect.redirect())
