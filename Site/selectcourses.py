#!/usr/bin/env python3
#allow user to select courses
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
    db=g.Session
    curemail=db.find_one({"_id":int(d)})["email"]
    template.printTemplatept1(curemail)
    #query database for all courses+ user's selcted 
    allCourses=[]
   
    c=g.Courses
    allCourses=list(c.find())
    ty=g.Users
    userCourses=list(ty.find_one({"email":curemail})["courses"])
    
    selected=[]
    name=[]
    
    _id=[]
    day=[]
    start_time=[]
    end_time=[]
    desc=[]
    #process data
    curind=0
    for i in range(len(allCourses)):
        _id.append(allCourses[i]["_id"])
        name.append(allCourses[i]["Name"])
        start_time.append(allCourses[i]["start_time"])
        end_time.append(allCourses[i]["end_time"])                    
        desc.append(allCourses[i]["desc"])
        if len(userCourses)!=0:
            if allCourses[i]["_id"] in userCourses:
                selected.append(i)
                curind+=1
        
        dy=["","","","",""]
        for j in allCourses[i]["day"]:
            if j=="Monday":
                dy[0]="M&nbsp;"
            elif j=="Tuesday":
                dy[1]="T&nbsp;"
            elif j=="Wednesday":
                dy[2]="W&nbsp;"
            elif j=="Thursday":
                dy[3]="R&nbsp;"
            elif j=="Friday":
                dy[4]="F"
            #else:
            #    dy.append(" ")
        day.append(dy)
    print ("""
<form action="enlistcourse.py">
<table>
<tr>
<th>Selected</th>
<th>Name</th>
<th>ID</th>
<th>Start-Time</th>
<th>End-Time</th>
<th>Days</th>
<th>Description</th>
</tr>
""")
    curind=0
    for i in range(len(allCourses)):
        checked=False##not sure if i should format as int or string
        print ("""<tr><td><input type="checkbox" name=%d id=%d"""%(int(_id[i]),int(_id[i])))
        if len(selected)!=curind:
            if selected[curind]==i:
            #make checkboxchecked
                curind+=1
                print ("checked")
        print ("></td>")
        print ("""<td>%s</td>"""%name[i])
        print ("""<td>%d</td>"""%_id[i])
        print ("""<td>%s</td>"""%start_time[i])
        print ("""<td>%s</td>"""%end_time[i])
        print ("""<td align="left">%s %s %s %s %s</td>"""%(day[i][0],day[i][1],day[i][2],day[i][3],day[i][4]))
        print ("""<td>%s</td>"""%desc[i])
    print("""
</table>
<input type="submit" id="choose" value="Choose Courses">
</form>
""")
    #print add course part
    print("""
<b>Add Course</b>
<form action="addcourse.py">
<table>
<tr>
<th>Name</th>
<th>Start-Time</th>
<th>End-Time</th>
<th>Days<br>M T W R F</th>
<th>Description</th>
</tr>
<tr>
<td><input type="text" name="cname" id="cname"></td>
<td><input type="text" id="start_time" name="start_time"></td>
<td><input type="text" id="end_time" name="end_time"></td>
<td><input type="checkbox" name="M" id="M"><input type="checkbox" name="T" id="T"><input type="checkbox" name="W" id="W"><input type="checkbox" name="R" id="R"><input type="checkbox" name="F" id="F"></td>
<td><textarea id="desc" name="desc" rows=5 cols=20></textarea></td>
</tr>
</table>
<input type="submit" value="Add Course" id="addcourse" disabled>
</form>
<p id="feedback"></p>
<script type="text/javascript" src="jquery-1.10.2.js">
</script>
<script type="text/javascript" src="./courseselect.js">
</script>
""")
#http://code.jquery.com/jquery-1.7.1.min.js
#increase textbox for description

#throw in some js to stop idiots from killing script
    template.printTemplatept2()
        
else:
    print(redirect.redirect())