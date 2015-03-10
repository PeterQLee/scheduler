#!/usr/bin/env python3

#main page, handles login and stuff
import cgi
import html
import http.cookies as Cookies
import sys
import os
from pymongo import MongoClient
sys.path.insert(0,"/home/peter/SchedulerProject/")

form=cgi.FieldStorage()
import checkcookie
import loginpage
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
if validcook:
    m=MongoClient()
    g=m.unisq
    db=g.Session
    use=db.find_one({"_id":int(d)})["email"]
    template.printTemplatept1(use)
    print ("""
<h2 align="center">Welcome to University Scheduler!</h2>
	<p>Thank you for creating an account on University Scheduler. We are pleased to assist you on creating a schedule optimal to your
	timing needs!</p>
<br>
<h4>Please click "Select Courses" from the navigation bar above to to begin making your schedule!</h4>
<br>
<center><h5>See below for an example of what a timetable might look like</h5>

<img id="CalenderExample" src="CalendarScreenshot.gif" alt="Calendar"></center>""")
    template.printTemplatept2()
        
else:
    loginpage.LoginPage(form)
