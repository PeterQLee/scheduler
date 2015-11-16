#!/usr/bin/env python3
###displays compiled options made via optimize.py###

import cgi
import html
import http.cookies as Cookies
import sys
import os
import json
#from pymongo import MongoClient

sys.path.insert(0,os.getcwd()+"../tools")
from DatabaseConnection import DatabaseConnection
import redirect
import template

#sys.path.insert(0,"/home/peter/SchedulerProject/")


form=cgi.FieldStorage()

#import checkcookie
#import redirect
#import template

cook=Cookies.SimpleCookie()

print ("Content-Type:text/html")
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
    template.printTemplatept1(curemail)
    
    mn=DB_conn.find_user({"email":curemail})["_id"]
    print ("</br></br></br>")
    
    
    n=DB_conn.find_one_choice({"_id":int(mn)})["select"]
    print("""
    <select class="form-control" id="sel-list">
    """)
      
      
      
    #print an option for each on present in the 
    for i in range(len(n)):
        print ("""<option>Option %d</option>"""%(i+1))
    print("</select>")

    print ("""</br>
<b>If your selections are not here, try refreshing the page after several seconds. It is also possible that there are no possible schedule options with your current course selections</b>""")

            
    print ("""
<script type="text/javascript" src="jquery-1.10.2.js">
</script>
<script type="text/javascript" src="drawoption.js">
</script>""") ##CHANGE THIS MOFO
    
    print("""
<canvas id="calapp" width=550 height=1500>
</canvas>
</br>
""") #scale diagram to height of window
    
    template.printTemplatept2()

else:
    print (redirect.redirect())
