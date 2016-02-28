#!/usr/bin/env python3

#adds user's account to database
#from pymongo import MongoClient
import cgi
import hashlib
import re
import sys
import os

sys.path.insert(0,os.getcwd()+"/../tools")
from MongoConnection import DatabaseConnection
#import redirect
#import template

form=cgi.FieldStorage()

email=form.getfirst("regemail")
passw=form.getfirst("regpwd")
print ("Content-type: text/html")
head="""
<html>
<head>
<title>Something messed up</title>
</head>
<body>
"""
rest="""<p><a href="index.py">Click Here</a> to go back</p>
</body>
</html>"""


DB_conn=DatabaseConnection()
if not email or not passw: 
    print (head)
    print ("""
<p>Invalid Request</p>
""")
    print (rest)
elif DB_conn.find_user({"email":email}): #check valid email
    #badstuff,
    print (head)
    print ("<p>Email Already Taken:</p>")
    print (rest)

else:
    hashpsw=hashlib.sha256(passw.encode('utf-8')).hexdigest()
    ##might need to str hashpsw
    idd=DB_conn.user_len()+1
    DB_conn.insert_user({"_id":idd,"email":email,"pass":hashpsw,"courses":[],"custom_conflicts":[]})

    #gd=g.Choices
    
    DB_conn.insert_choice({"_id":idd,"select":[]})

    
    #redirect

    print(head)
    print ("""
<a href="index.py?success=1">Registration successful!</a>
<script type="text/JavaScript">

window.location="index.py?success=1"

</script>
""")
    print(rest)

