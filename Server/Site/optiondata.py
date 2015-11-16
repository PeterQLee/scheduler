#!/usr/bin/env python3

import cgi
import html
import http.cookies as Cookies
import sys
import os
import json
#from pymongo import MongoClient
#sys.path.insert(0,"/home/peter/SchedulerProject/")
sys.path.insert(0,os.getcwd()+"../tools")
from DatabaseConnection import DatabaseConnection
import redirect
import template

form=cgi.FieldStorage()

#import checkcookie
#import redirect
#import template

cook=Cookies.SimpleCookie()

print ("Content-Type:text/plain\n")
validcook=False
d=0
DB_conn=DatabaseConnection()
if os.environ.get("HTTP_COOKIE"):
    cook.load(os.environ["HTTP_COOKIE"])
    
    d=cook["session"].value
    u=DB_conn.checkcookie(d)  #checkcookie.checkcookie(cook["session"].value)

    validcook=u
if validcook:
    
    #m=MongoClient()
    #g=m.unisq
    #k=g.Users
    #db=g.Session
    #cs=g.Courses
    #cg=g.Choices

    curemail=DB_conn.find_session({"_id":int(d)})["email"]
    #print("Content-type:text/plain\n\n")
    #template.printTemplatept1(curemail)
    p=form.getfirst("pnum") #getfirst
    userid=DB_conn.find_user({"email":curemail})["_id"]
    n=DB_conn.find_one_choice({"_id":int(userid)})["select"]
    no=False
    try:
        int(p)
    except:
        no=True
    if len(p)>=1 and not no: 
        #ensure p is a valid integer
        
        currcourseid=DB_conn.find_one_choice({"_id":int(userid)})["select"] #mn
        if int(p)<len(n) or int(p)>=0: #check to make sure it is in range
            cur=currcourseid[int(p)]
            #select that option at p as the current list of courses

            #get start/end times
            times=[] #[[courseid,coursename,sttime,endtime],...]

            ky={"M":0,"T":1,"W":2,"R":3,"F":4}
            
            for b in cur: #b=courseid
            
                courseinstance=DB_conn.find_one_course({"_id":b})
                nm=courseinstance["Name"] #nm is the name of the course
                kyxy=[b,nm]
                st=int(courseinstance["start_time"])
                ed=int(courseinstance["end_time"])
                dy=courseinstance["day"]
                for k in dy:
                    #convert minute time to weekday time
                    kyxy.append(ky[k]*2400+st)
                    kyxy.append(ky[k]*2400+ed)
                    #add to time clump
                    times.append(kyxy)
            dat=json.dumps(times)
            print(dat)
        else:print('[]')
    else:
        print('[]')

else:
    print (redirect.redirect()) #danger security
