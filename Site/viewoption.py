#!/usr/bin/env python3
#displays compiled options made via optimize.py
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
    p=form.getfirst("pnum")
    mn=k.find_one({"email":curemail})["_id"]
    print ("</br></br></br>")
    
    if not p:
        n=cg.find_one({"_id":int(mn)})["select"]
        print ("<ol>")
        for i in range(len(n)):
            print ("""<li><a href="viewoption.py?pnum=%d">Option %d</a></li>"""%(i,i+1))
            
        print ("</ol>")
        print ("""</br>
<b>If your selections are not here, try refreshing the page after several seconds. It is also possible that there are no possible schedule options with your current course selections</b>""")

    else:
        print ("""<a href="viewoption.py">Back to Options</a>
</br>""")
        n=cg.find_one({"_id":int(mn)})["select"]
        if int(p)>len(n) or int(p)<0:
            print ("<b>Index out of range!</b>")
        else:
            cur=n[int(p)]
        #get start/end times
            times=[]
            ky={"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4}
            for b in cur: #b=courseid
            #kyxy=[]
                nm=cs.find_one({"_id":b})["Name"]
                kyxy=[b,nm]
                st=int(cs.find_one({"_id":b})["start_time"])
                ed=int(cs.find_one({"_id":b})["end_time"])
                dy=cs.find_one({"_id":b})["day"]
                for k in dy:
                    kyxy.append(ky[k]*2400+st)
                    kyxy.append(ky[k]*2400+ed)
                    times.append(kyxy)
                    dat=json.dumps(times)
        #throw this data into js
        
            print ("""
<script type="text/javascript" src="jquery-1.10.2.js">
</script>
<script type="text/javascript" src="drawoption.js">
</script>""") ##CHANGE THIS MOFO
            print ("""
<script type="text/javascript">
var data=%s
$(draw)
</script>
"""%dat)
            print("""
<canvas id="calapp" width=550 height=1500>
</canvas>
</br>
""")
            if int(p)>0:
                print("""<a href="viewoption.py?pnum=%d" align=left>Back</a>"""%(int(p)-1))
            if int(p)<len(n)-1:
            
                print("""<a href="viewoption.py?pnum=%d" align=right>Next</a>"""%(int(p)+1))
    template.printTemplatept2()

else:
    print (redirect.redirect())
