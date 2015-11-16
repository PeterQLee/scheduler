#cleanse database
from pymongo import MongoClient
import sys

ip="127.0.0.1"
port=27017

if sys.argc==4:
    ip=sys.argv[2]
    port=int(sys.argv[3])

M=MongoClient(ip,port)


g=M.unisq

g.Choices.drop()
g.Courses.drop()
g.Session.drop()
g.Users.drop()

M.close()
