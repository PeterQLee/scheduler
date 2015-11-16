#!/usr/bin/env python3
#from pymongo import MongoClient
import hashlib
import cgi
import random
import datetime
import http.cookies as Cookies

sys.path.insert(0,os.getcwd()+"../tools")
from DatabaseConnection import DatabaseConnection

#import redirect
#import template

print ("Content-type: text/html")

form=cgi.FieldStorage()
#get submitted password and stuff
email=form.getfirst("loginemail")
passw=form.getfirst("loginpass")
#prepare hash, or throw to error page
hashpsw=""
if passw:
    hashpsw=hashlib.sha256(passw.encode('utf-8')).hexdigest()
else:
    a=1
    #print("ERROR")


#m=MongoClient()
#g=m.unisq
#db=g.Users

DB_conn=DatabaseConnection()
dat=DB_conn.find_user({"email":email})


if not dat:
    #errormsg
    print ("""
<a href="index.py?incorrect=1">INCORRECT LOGIN</a>
<script type="text/JavaScript">

window.location="index.py?incorrect=1"

</script>
""")
#verify password match
#might need to unencode pwd
elif dat["pass"]==hashpsw:
    #print("YAY UR IN")
    #delete previous cookies

    #ses=g["Session"]

    if DB_conn.find_session({"email":email}):
        DB_conn.remove_session({"email":email})
    
    #set cookies and stuff, add cookie int to db
    key=str(random.randint(0,10000000))
    while DB_conn.find_session({"_id":int(key)}):
        key=str(random.randint(0,10000000))
    
    #TO DO, check to make sure key isnt used
    cook=Cookies.SimpleCookie()
    cook["session"]=key
    print(cook.output())
    print()
    DB_conn.insert_session({"_id":int(key),"email":email})
    
    

    #redirect user
    print("<a href=\"index.py\"> REDIRECTING...</a><br>")
    print("""
<script type="text/JavaScript">

window.location= "index.py" 



</script>""")
else:
    #send back to index page with notfication
    #print("PASSWORDS NO MATCH :(")
    #remember 
    print ("""
<a href="index.py?incorrect=1">INCORRECT LOGIN</a>
<script type="text/JavaScript">

window.location="index.py?incorrect=1"

</script>
""")
