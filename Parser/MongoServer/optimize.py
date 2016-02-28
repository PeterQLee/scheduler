from pymongo import MongoClient
from time import sleep
from copy import *
import sys
import numpy
import traceback #TODO:temp

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

    
def find_possible(data,co,conflicts):
    poss=[]
    for k in data[0]:
        poss.append([k])

    for i in range(1,len(data)):
        newposs=[]
        for k in data[i]:
            for j in poss:
                print(poss,j,k)
                if not conflicts.find_conflict(k,j):
                    newposs.append(j+[k])

        poss=newposs
            
    return poss
                

class Conflict:
    def __init__(self):
        self.mat=numpy.load("../adj_matrix.npy")
        f=open("../graph/indices.dat","r")
        dd=f.read()
        buf=dd.split(",")
        buf[0]=buf[0].replace("[","")
        buf[len(buf)-1]=buf[len(buf)-1].replace("]","")
       
       
        ind=0
        self.indices_dict={}
        for i in buf:
            self.indices_dict[int(i)]=ind
            ind+=1

    def find_conflict(self,i,j_list):
        #finds whether there is an existing conflict in the given lists
        mat=self.mat
        indic=self.indices_dict
        for j in j_list:
            print(indic[i],indic[j])
            if mat[indic[i]][indic[j]]==1:
                return True

        return False

    def exists(self,i):
        return i in self.indices_dict
#start server materials


#TODO: server exceptions           
rserver=RequestServer()
rserver.load_config("server.cnfg")
rserver.start()

DB=DatabaseConnection()#'localhost',6111)


#conflict data
conflict=Conflict()    


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
        usid=int.from_bytes(rserver.next_message(),"big") #TODO: byte int conversion
        print(usid)
        if usid==0: 
            rserver.stop()
            break #TEMP
    except:
        print("FUCK")
        traceback.print_exc()
        break
        
    clist=DB.find_user({"_id":usid}) #looks up DB entry for user and their desired courses
    if clist:
        clist=clist["courses"] #here include season e.g clist["wintercourses"]
    else:
        continue
        
    #time to organize these into name groups
    mp={}
    
        
    for i in clist:
        d=DB.find_one_course({"_id":i})["Name"]#courses.find_one({"_id":i})["Name"]
        
        #make sure its an entry here
        
        if conflicts.exists(d):
            if mp.get(d):
                mp[d].append(i)
            else:
                mp[d]=[i]
        else:
            print("Error could not find ",d," for user ",usid)
    
    c_ids=list(mp.values()) 
    #TODO: sort c_ids by length
    
    c_ids.sort(key=lambda x:len(x))
    print("c_ids: ",c_ids)
    choi=find_possible(c_ids,DB.cs,conflict)
    
    #choi=recursedat(c_ids,0,[],[],DB.cs) #old
    DB.update_choice({"_id":usid},{"_id":usid,"select":choi}) #FUX
    #choices.update({"_id":usid},{"_id":usid,"select":choi})
    print (choi)
   
 
