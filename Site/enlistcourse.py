#!/usr/bin/env python3
#adds course to users personal list
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
import template
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
if validcook:
    
    m=MongoClient()
    g=m.unisq
    ses=g.Session
    
    usemail=ses.find_one({"_id":int(d)})["email"]
    
    template.printTemplatept1(usemail)
    
    db=g.Users #check
    idlist=[]
    for i in form:
        if i.isdigit():###redo
            idlist.append(int(i))
    #check to make sure ids are in course load
    c=g.Courses
    uselist=[]
    for i in idlist:
        if c.find_one({"_id":i}):
            uselist.append(i)
    n=db.find_one({"email":usemail})["pass"]
    d=db.find_one({"email":usemail})["_id"]
    db.update({"email":usemail},{"email":usemail,"_id":d,"pass":n,"courses":uselist})
    
    f=open("../queue.txt","a")
    f.write(str(d)+"\n")
    print ("""
<p>Courses Added successfully!</p>
<p>Click <a href="index.py">here</a> to go back to index</p>
""")
    template.printTemplatept2()
    
    

else:
    print(redirect.redirect())
