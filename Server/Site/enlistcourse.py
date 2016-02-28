#!/usr/bin/env python3
#adds course to users personal list
import cgi
import html
import http.cookies as Cookies
import sys
import os
#from pymongo import MongoClient
sys.path.insert(0,os.getcwd()+"/../tools")
from MongoConnection import DatabaseConnection
import redirect
import template
import send_generator

form=cgi.FieldStorage()


cook=Cookies.SimpleCookie()

print ("Content-Type:text/html")
validcook=True
d=0
DB_conn=DatabaseConnection()
if os.environ.get("HTTP_COOKIE"): #check login
    cook.load(os.environ["HTTP_COOKIE"])
    d=cook["session"].value
    u=DB_conn.checkcookie(d)
    #u=checkcookie.checkcookie(cook["session"].value)

    if not u:
        validcook=False
if validcook:
    
    usemail=DB_conn.find_session({"_id":int(d)})["email"]
    
    template.printTemplatept1(usemail)
    
    #db=g.Users #check
    idlist=[]
    for i in form: 
        if i.isdigit():###redo
            idlist.append(int(i))
    #check to make sure ids are in course load

    #c=g.Courses

    uselist=[]
    first=True
    season=""
    for i in idlist: #makes sure user didn't spoof the form to add a course from a different season
        if DB_conn.find_one_course({"_id":i}):
            season=DB_conn.find_one_course({"_id":i})["season"]
            break
    
    for i in idlist:
        if DB_conn.find_one_course({"_id":i,"season":season}):
            uselist.append(i)
    n=DB_conn.find_user({"email":usemail})["pass"]
    d=DB_conn.find_user({"email":usemail})["_id"]

    DB_conn.update_user({"email":usemail},{"email":usemail,"_id":d,"pass":n,"courses":uselist})
    #db.update({"email":usemail},{"email":usemail,"_id":d,"pass":n,"courses":uselist})
    
    result=send_generator.send_generator(d)
    if result:
        print ("""
<p>Courses Added successfully!</p>
<p>Click <a href="index.py">here</a> to go back to index</p>
""")
    else:
        print("""
<p> Due to an unknown error, your schedule possibilities were unable to be generated. Contact the system admin.</p>
<p>Click <a href="index.py">here</a> to go back to index</p>
""")
    template.printTemplatept2()
    
    

else:
    print(redirect.redirect())
