#cleanse database
from pymongo import MongoClient
import sys

ip="127.0.0.1"
port=27017

if len(sys.argv)==4:
    ip=sys.argv[2]
    port=int(sys.argv[3])

M=MongoClient(ip,port)


g=M.unisq
g.Conflicts.drop()
g.Choices.drop()
g.Courses.drop()
g.Session.drop()
g.Users.drop()
#g.Conflicts

g.Users.insert({"_id" : 0, "email" : "placegold@fea.da", "pass" : "yoaf32s", "courses" : [ ] })

M.close()
