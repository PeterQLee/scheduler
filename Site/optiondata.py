#!/usr/bin/env python3

import cgi
import html
import http.cookies as Cookies
import sys
import os
import json
from pymongo import MongoClient
sys.path.insert(0,"/home/peter/SchedulerProject/")


form=cgi.FieldStorage()
import checkcookie
import redirect
import template
cook=Cookies.SimpleCookie()

print ("Content-Type:text/html")
validcook=False
d=0
if os.environ.get("HTTP_COOKIE"):
    cook.load(os.environ["HTTP_COOKIE"])
    u=checkcookie.checkcookie(cook["session"].value)
    d=cook["session"].value
    #if not u:
        #validcook=False
    validcook=u
if validcook:
   
    m=MongoClient()
    g=m.unisq
    k=g.Users
    db=g.Session
    cs=g.Courses
    cg=g.Choices
    curemail=db.find_one({"_id":int(d)})["email"]
    template.printTemplatept1(curemail)
    p=form.get("pnum") #getfirst
    userid=k.find_one({"email":curemail})["_id"]
    if len(p)==1 and isinstance(p,int):
        currcourseid=cg.find_one({"_id":int(mn)})["select"]
        if int(p)<len(n) or int(p)>=0: #check to make sure it is in range
            cur=currcourseid[int(p)]
        #get start/end times
            times=[]
            ky={"M":0,"T":1,"W":2,"R":3,"F":4}
            for b in cur: #b=courseid
            
                nm=cs.find_one({"_id":b})["Name"] #nm is the name of the course
                kyxy=[b,nm]
                st=int(cs.find_one({"_id":b})["start_time"])
                ed=int(cs.find_one({"_id":b})["end_time"])
                dy=cs.find_one({"_id":b})["day"]
                for k in dy:
                    kyxy.append(ky[k]*2400+st)
                    kyxy.append(ky[k]*2400+ed)
                    times.append(kyxy)
            dat=json.dumps(times)
            print(dat)
        else:print('[]')
    else:
        print('[]')

else:
    print (redirect.redirect()) #danger security
