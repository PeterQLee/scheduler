#!/usr/bin/env python3

#Script that adds course selected via html parameters to database
import cgi
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
validcook=False
d=0
if os.environ.get("HTTP_COOKIE"):
    cook.load(os.environ["HTTP_COOKIE"])
    u=checkcookie.checkcookie(cook["session"].value)
    d=cook["session"].value
    validcook=u
    #if not u:
    #    validcook=False

if validcook:
    m=MongoClient()
    g=m.unisq
    db=g.Session
    
    curemail=db.find_one({"_id":int(d)})["email"]
    template.printTemplatept1(curemail)
    
    name=cgi.escape(form.getfirst("cname"))
    start=cgi.escape(form.getfirst("start_time"))
    end=form.getfirst("end_time")
    Mflag=form.getfirst("M") #might crash
    Tflag=form.getfirst("T")
    Wflag=form.getfirst("W")
    Rflag=form.getfirst("R")
    Fflag=form.getfirst("F")
    season=form.getfirst("season")
    noflag=False
    if not name or not start or not end:
        noflag=True
    if not Mflag and not Tflag and not Wflag and not Rflag and not Fflag:
        noflag=True
    co=g.Courses
    _id=len(list(co.find()))+1
    #test to make sure there isn't an identical thing
    
    day=[]
    if Mflag:
        day.append("Monday")
    if Tflag:
        day.append("Tuesday")
    if Wflag:
        day.append("Wednesday")
    if Rflag:
        day.append("Thursday")
    if Fflag:
        day.append("Friday")
    if not co.find_one({"Name":name,"start_time":start,"end_time":end,"day":day}) and not noflag:
        co.insert({"_id":_id,"Name":name,"start_time":start,"end_time":end,"season":season,"day":day})
        print ("""
<p>Course Added Successfully!""")
        
    else:
        print ("""
<p>Identical Course Already in Place!""")
    print ("""<a href="selectcourses.py">Back</a>""")
    template.printTemplatept2()
    
else:
    print(redirect.redirect())
