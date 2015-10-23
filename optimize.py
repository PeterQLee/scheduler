from pymongo import MongoClient
from time import sleep
from copy import *


##Algorithm that uses graph search to find different possible time combinations for courses assuming they have the same course name
def timedontconflict(timedata,times):
    t=timedata+times
    t.sort(key=lambda x:abs(x)) #sorts times
    for i in range(len(t)-1):
        if t[i]>0 and t[i+1]>0:
            return False
    return True
def recursedat(data,ind,curarr,timedata,co): #set term season as a variable too.. will have to communicate this in page code too
    if ind==len(data): #we've reached the last in the string of possibilities
        return [curarr]
    poslist=[]
    for i in range(len(data[ind])):
        n=copy(curarr)
        n.append(data[ind][i]) #selects id from array
        times=[]
        st=int(co.find_one({"_id":data[ind][i]})["start_time"])
        ed=int(co.find_one({"_id":data[ind][i]})["end_time"])
        dy=co.find_one({"_id":data[ind][i]})["day"]
        dap={"M":0,"T":1,"W":2,"R":3,"F":4}
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
    #checks users who need options sorted
    m=MongoClient()
    g=m.unisq
    us=g.Users
    co=g.Courses
    be=g.Choices
    buf=f.readline()
    used=[]
    while buf!="":
        if buf in used: #makes sure user hasn't already been searched this session
            buf=f.readline()
            continue
        usid=int(buf)
        
        
        clist=us.find_one({"_id":usid}) #looks up DB entry for user and their desired courses
        if clist:
            clist=clist["courses"] #here include season e.g clist["wintercourses"]
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
        #print(d+" is with "+str(mp))
        dat=list(mp.values()) #all the time info and stuff???
        choi=recursedat(dat,0,[],[],co)
        be.update({"_id":usid},{"_id":usid,"select":choi})
        buf=f.readline()
        used.append(buf)
    f.close() #wip file contents
    m=open("queue.txt","w")
    m.close()
    
    sleep(30)
