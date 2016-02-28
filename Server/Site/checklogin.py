#!/usr/bin/env python3

import cgi
import html
import http.cookies as Cookies
import sys
import os
import json
#from pymongo import MongoClient
#sys.path.insert(0,"/home/peter/SchedulerProject/")
sys.path.insert(0,os.getcwd()+"/../tools")
from MongoConnection import DatabaseConnection
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

p=form.getfirst("email")

data=DB_conn.find_user({"email":p})
if not data:
    print(json.dumps(False))
else:
    #dat=json.dumps(data)

    print(json.dumps(True))


