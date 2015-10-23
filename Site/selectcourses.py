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
    tag=form.getlist("tag")
    srchseas=form.getlist("season")
    if len(srchseas)!=1:srchseas="fall"
    elif srchseas[0]!="fall" and srchseas[0]!="winter": srchseas="fall"
    else:srchseas=srchseas[0]
    c=g.Courses
    #taglist=[]

    allCourses=list(c.find({"tag":{"$in":tag},"season":srchseas})) ##restrict to catagories
    taglist=c.distinct("tag")
    ty=g.Users
    userCourses=list(ty.find_one({"email":curemail})["courses"])
    allCourses+=(list(c.find({"_id":{"$in":userCourses}})))#also append the user's chosen courses
    allCourses=sorted(allCourses,key=lambda k: k["Name"])
    
    #Before we print courses, print a list of selectable tags
    #sorted(taglist)
    taglist.sort()
    #print(taglist)
    print("""
<b>Specify your course choices with course tags</b>
<div class="container jumbotron">
<form action=selectcourses.py method="GET" id="tags">
""")
    ind=0
    lasti=taglist[0]
    for i in taglist:
        if i[0]!=lasti[0]:print("<br>")
        if i in tag:
            print("""<input type="checkbox" name="tag" value=%s checked>%s"""%(i,i))
        else:
            print("""<input type="checkbox" name="tag" value=%s>%s"""%(i,i))
        ind+=1
        lasti=i
    if srchseas=="fall":
        print("""<br><input type="radio" name="season" value=fall checked>fall
<input type="radio" name="season" value=winter>winter
""")
    else:
        print("""<br><input type="radio" name="season" value=fall>fall
<input type="radio" name="season" value=winter checked>winter
""")
    print("""<br/><input type="submit" value="Confirm">""")
    print("</form></div>")
    selected=[]
    name=[]
    
    _id=[]
    day=[]
    start_time=[]
    end_time=[]
    season=[]
    #process data
    curind=0
    for i in range(len(allCourses)):
        _id.append(allCourses[i]["_id"])
        name.append(allCourses[i]["Name"])
        start_time.append(allCourses[i]["start_time"])
        end_time.append(allCourses[i]["end_time"])                    
        season.append(allCourses[i]["season"]) #formerly desc
        if len(userCourses)!=0:
            if allCourses[i]["_id"] in userCourses:
                selected.append(i)
                curind+=1
        
        dy=["","","","",""]
        for j in allCourses[i]["day"]:
            if j=="M": ##change to letter
                dy[0]="M&nbsp;"
            elif j=="T":
                dy[1]="T&nbsp;"
            elif j=="W":
                dy[2]="W&nbsp;"
            elif j=="R":
                dy[3]="R&nbsp;"
            elif j=="F":
                dy[4]="F"
            #else:
            #    dy.append(" ")
        day.append(dy)
    print ("""
<script src="jquery-1.10.2.js"></script>
<script src="displaychosen.js"></script>
<form action="enlistcourse.py">
<table class="table" id="tablein">
<tr>
<th>Selected</th>
<th>Name</th>
<th>ID</th>
<th>Start-Time</th>
<th>End-Time</th>
<th>Days</th>
<th>Season</th>
</tr>

""") #changed description to season

#######################################################

    
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
        print ("""<td id=seas%d>%s</td>"""%(_id[i],season[i])) #give season its own ID

################################################################




    print("""

</table>
<input type="submit" id="choose" value="Choose Courses">
</form>
""")
    #print add course part
    """
<b>Add Course</b>
<form action="addcourse.py">
<table>
<tr>
<th>Name</th>
<th>Start-Time</th>
<th>End-Time</th>
<th>Days<br>M T W R F</th>
<th>Winter?</th>
</tr>
<tr>
<td><input type="text" name="cname" id="cname"></td>
<td><input type="text" id="start_time" name="start_time"></td>
<td><input type="text" id="end_time" name="end_time"></td>
<td><input type="checkbox" name="M" id="M"><input type="checkbox" name="T" id="T"><input type="checkbox" name="W" id="W"><input type="checkbox" name="R" id="R"><input type="checkbox" name="F" id="F"></td>
<td><input type="checkbox" id="season" name="season"></td>
</tr>
</table>
<input type="submit" value="Add Course" id="addcourse" disabled>
</form>"""

    print("""

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
