#!/usr/bin/env python3

#deletes user's session from db
import cgi
import html
import http.cookies as Cookies
import sys
import os
from pymongo import MongoClient
sys.path.insert(0,"/home/peter/SchedulerProject/")


form=cgi.FieldStorage()
import checkcookie
import redirect

cook=Cookies.SimpleCookie()

print ("Content-Type:text/html")
validcook=True
d=0
if os.environ.get("HTTP_COOKIE"):
    cook.load(os.environ["HTTP_COOKIE"])
    u=checkcookie.checkcookie(cook["session"].value)
    d=cook["session"].value
    if not u:
        validcook=False
else:
    validcook=False
if validcook:
    m=MongoClient()
    g=m.unisq
    db=g.Session
    db.remove({"_id":int(d)})
    print (redirect.redirect())
else:
    print (redirect.redirect())
