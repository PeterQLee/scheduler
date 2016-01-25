from pymongo import MongoClient
from time import sleep
from copy import *
import sys

#TEMPORARY
sys.path.insert(0,"../../Server/tools")

from MongoConnection import DatabaseConnection #TODO: set paths correctly
from RequestServer import RequestServer

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

#start server materials

#TODO: server exceptions           
rserver=RequestServer()
rserver.load_config("server.cnfg")
rserver.start()

DB=DatabaseConnection()#'localhost',6111)
    
while True:
    ##f=open("queue.txt","r")
    #checks users who need options sorted
    ##m=MongoClient()
    ##collection=m.unisq
    ##users=collection.Users
    ##courses=collection.Courses
    ##choices=collection.Choices
    ##buf=f.readline() #replace..
    print("start")
    #start 
    try:
        usid=int(rserver.next_message()) #TODO: byte int conversion
        if usid==0: 
            rserver.stop()
            break #TEMP
    except:
        continue
        
    clist=DB.find_user({"_id":usid}) #looks up DB entry for user and their desired courses
    if clist:
        clist=clist["courses"] #here include season e.g clist["wintercourses"]
    else:
        continue
        
    #time to organize these into name groups
    mp={}
        
    for i in clist:
        d=DB.find_one_course({"_id":i})["Name"]#courses.find_one({"_id":i})["Name"]
        
        #TODO:remove irrelevant code
        if mp.get(d):
            mp[d].append(i)
        else:
            mp[d]=[i]

    c_ids=list(mp.values()) #all the time info and stuff???
    choi=recursedat(c_ids,0,[],[],DB.cs)
    DB.update_course({"_id":usid},{"_id":usid,"select":choi})
    #choices.update({"_id":usid},{"_id":usid,"select":choi})
    print (choi)
   
 
