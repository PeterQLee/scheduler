from pymongo import MongoClient
from time import sleep
from copy import *


##Algorithm that uses graph search to find different possible time combinations for courses assuming they have the same course name
def timedontconflict(timedata,times):
    t=timedata+times
    t.sort(key=lambda x:abs(x))
    for i in range(len(t)-1):
        if t[i]>0 and t[i+1]>0:
            return False
    return True
def recursedat(data,ind,curarr,timedata,co):
    if ind==len(data):
        return [curarr]
    poslist=[]
    for i in range(len(data[ind])):
        n=copy(curarr)
        n.append(data[ind][i])
        times=[]
        st=int(co.find_one({"_id":data[ind][i]})["start_time"])
        ed=int(co.find_one({"_id":data[ind][i]})["end_time"])
        dy=co.find_one({"_id":data[ind][i]})["day"]
        dap={"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4}
        for j in dy:
            times.append(st+2400*dap[j])
            times.append(-ed+-2400*dap[j])

        if timedontconflict(timedata,times):
            t=timedata+times
            t.sort(key=lambda x:abs(x))
            poslist+=recursedat(data,ind+1,n,t,co)
    return poslist
            
            
while True:
    f=open("queue.txt","r")
    m=MongoClient()
    g=m.unisq
    us=g.Users
    co=g.Courses
    be=g.Choices
    buf=f.readline()
    used=[]
    while buf!="":
        if buf in used:
            buf=f.readline()
            continue
        usid=int(buf)
        
        clist=us.find_one({"_id":usid})#["courses"]
        if clist:
            clist=clist["courses"]
        else:
            buf=f.readline()
            continue
        #time to organize these into name groups
        mp={}
        for i in clist:
            d=co.find_one({"_id":i})["Name"]
            if mp.get(d):
                mp[d].append(i)
            else:
                mp[d]=[i]
        dat=list(mp.values())
        choi=recursedat(dat,0,[],[],co)
        be.update({"_id":usid},{"_id":usid,"select":choi})
        buf=f.readline()
        used.append(buf)
    f.close() #wip file contents
    m=open("queue.txt","w")
    m.close()
    
    sleep(30)
