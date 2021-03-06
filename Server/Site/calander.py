#!/usr/bin/env python3
#script prints html and encorperates js to display calander app
import cgi
import html
import http.cookies as Cookies
import sys
import os
#from pymongo import MongoClient
import json
#from StringIO import StringIO

sys.path.insert(0,os.getcwd()+"/../tools")
from MongoConnection import DatabaseConnection
import redirect
import template

#sys.path.insert(0,"/home/peter/SchedulerProject/")

form=cgi.FieldStorage()

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
#    m=MongoClient()
 #   g=m.unisq
 #   db=g.Users
 #   e=g.Session
    usemail=DB_conn.find_session({"_id":int(d)})["email"] #e.find_one({"_id":int(d)})["email"]
    courselist=DB_conn.find_user({"email":usemail})["courses"]
    template.printTemplatept1(usemail)
    #cs=g.Courses
    coursedata=[]
    
    for i in courselist:
        n=DB_conn.find_one_course({"_id":i}) #n=cs.find_one({"_id":i})
        arr=[] #id, #name, time ranges
        arr.append(int(n["_id"]))
        arr.append(n["Name"])
        times=[]
        st=int(n["start_time"])
        end=int(n["end_time"])
        for j in n["day"]:
            coff=0
            if j=="M":#"Monday":
                coff=0
            if j=="T":
                coff=1
            if j=="W":
                coff=2
            if j=="R":
                coff=3
            if j=="F":
                coff=4
            times.append(coff*2400+st)
            times.append(coff*2400+end)
        arr=arr+times
        #this is what we are dumping
        coursedata.append(arr)
    #io=StringIO()
    #json.dump(coursedata,io)
    dat=json.dumps(coursedata)#io.getvalue()
    print ("<ul>")
    for i in range(len(coursedata)):
        #dy=[]
        n=DB_conn.find_one_course({"_id":courselist[i]})
        dy=""
        for j in n["day"]:
            dy+=j+" "

        print("""<li>
<input type="checkbox" id=%d>%s %s - %s %s</li>
"""%(coursedata[i][0],coursedata[i][1]+" "+str(coursedata[i][0]),n["start_time"],n["end_time"],dy))
    print ("</ul>") ###src="http://code.jquery.com/jquery-1.7.1.min.js">
    print ("""
<script type="text/javascript" src="js/jquery-1.10.2.js">
</script>
<script type="text/javascript" src="js/drawshiz.js">
</script>""")
    print ("""
<script type="text/javascript">
var data=%s
$(draw)
"""%dat)
    print("""
$(document).ready(function(){""")
    #add events for drawing function
    for i in coursedata:
        print("""$("#%d").change(draw);
"""%i[0])
    print("""
});
</script>""")
    print("""
<canvas id="calapp" width=550 height=1500>
</canvas>
""")

    template.printTemplatept2()
else:
    print (redirect.redirect())
#DB_conn.close() #not necessary
