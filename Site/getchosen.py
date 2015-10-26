#!/usr/bin/env python3
import json
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

print ("Content-Type:text/plain\n")
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
    c=g.Courses
    
    allCourses=[]
    tag=form.getlist("tag")
    srchseas=form.getlist("season")
    if len(srchseas)!=1:srchseas="fall" #get the season we're looking at
    elif srchseas[0]!="fall" and srchseas[0]!="winter": srchseas="fall"
    else:srchseas=srchseas[0]
    allCourses=list(c.find({"tag":{"$in":tag},"season":srchseas}))
    
    
    ty=g.Users
    userCourses=list(ty.find_one({"email":curemail})["courses"])

    allCourses+=(list(c.find({"_id":{"$in":userCourses}})))
    allCourses=sorted(allCourses,key=lambda k: k["Name"])
    #taglist.sort()

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

    curind=0
    ret={"sel":[],"name":[],"_id":[],"start_time":[],"end_time":[],"day":[],"seas":[]}
    for i in range(len(allCourses)):
        #checked=False##not sure if i should format as int or string
         
        #print ("""<tr><td><input type="checkbox" name=%d id=%d"""%(int(_id[i]),int(_id[i])))
        ret["sel"].append(0)
        if len(selected)!=curind:
            if selected[curind]==i:
             #make checkboxchecked
                curind+=1
                ret["sel"][i]=1
            
         
                #print ("checked")
        
        #print ("></td>")
        ret["name"].append(name[i])
        ret["_id"].append(_id[i])
        ret["start_time"].append(start_time[i])
        ret["end_time"].append(end_time[i])
        ret["day"].append(day[i][0]+day[i][1]+day[i][2]+day[i][3]+day[i][4])
        ret["seas"].append(season[i])
        #print ("""<td>%s</td>"""%name[i])
        #print ("""<td>%d</td>"""%_id[i])
        #print ("""<td>%s</td>"""%start_time[i])
        #print ("""<td>%s</td>"""%end_time[i])
        #print ("""<td align="left">%s %s %s %s %s</td>"""%(day[i][0],day[i][1],day[i][2#],day[i][3],day[i][4]))
        #print ("""<td id=seas%d>%s</td>"""%(_id[i],season[i])) #give season its own ID
    print (json.dumps(ret))
else:
    print("[]")
