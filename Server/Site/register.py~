#!/usr/bin/env python3

#adds user's account to database
from pymongo import MongoClient
import cgi
import hashlib
import re
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
m=MongoClient()
g=m["unisq"]
db=g["Users"]
if not email or not passw: 
    print (head)
    print ("""
<p>Invalid Request</p>
""")
    print (rest)
elif db.find_one({"email":email}): #check valid email
    #badstuff,
    print (head)
    print ("<p>Email Already Taken:</p>")
    print (rest)
elif not re.match (r"[^@]+@[^@]+\.[^@]+",email) or re.match(r"[<|>]",email): #make safe!
    #invalid email
    print (head)
    print ("<p>Invalid Email</p>")
    print (rest)  
else:
    hashpsw=hashlib.sha256(passw.encode('utf-8')).hexdigest()
    ##might need to str hashpsw
    idd=len(list(db.find()))+1
    db.insert({"_id":idd,"email":email,"pass":hashpsw,"courses":[]})
    gd=g.Choices
    gd.insert({"_id":idd,"select":[]})
    
    #redirect

    print(head)
    print ("""
<a href="index.py?success=1">Registration successful!</a>
<script type="text/JavaScript">

window.location="index.py?success=1"

</script>
""")
    print(rest)

