#initialize database
import sys
from pymongo import MongoClient

ip="127.0.0.1"
port=27017
if sys.argc==4:
    ip=sys.argv[2]
    port=int(sys.argv[3])

M=MongoClient(ip,port) #return code?
g=M.unisq
#check to make sure that db is not done (cleanse if otherwise)
users=g.Users
if :users.count()==0

    g.create_collection("Choices")
    g.create_collection("Courses")
    
    g.create_collections("Session")
    #choices=g.Choices
    #courses=g.Courses
    #session=g.Session


    #make a fake user
    users.insert({"_id":0,"email":"placeholder","pass":"abcd","courses":[]}) #security

#make sure stuff is initialized...
M.close()
