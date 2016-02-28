#checks cookie and validates whether the id matches a user session in database
from pymongo import MongoClient

def checkcookie(cookid):
    m=MongoClient()
    t=m.unisq
    g=t.Session
    if g.find_one({"_id":int(cookid)}):
        return True
    else:
        return False
