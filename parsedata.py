#mongostuff
import re
import sys

courseseason=sys.argv[1]
print(courseseason)
f=open("/mirror/mpiu/courseresult.txt","rb")
buf=f.read()
print(buf)
buf=str(buf)
kei=("Name","_id","days","avail")
ind=0

dic={}
nentry=""
entry=""
G=buf.split("\\xff")
print(G)
ind =0
i=""
dic["Name"]=""
dic["day"]=[]
for i in G:
    if re.match("^[A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][0-9]",i):
        print(dic)
        if (len(dic["day"])==0):
            pass #dont update
        dic={"day":[],"Name":""}
        
        ind=0

    #i+=k
    print(i)
    #dic["Name"]=""
    #dic["_id"]=0
    #dic["days"]=[]
    #dic["avail"]=[]
    if ind==0 or ind==2:dic["Name"]=dic["Name"]+i+" : "
    elif ind==1:dic["_id"]=int(i)
    elif ind==3:dic["Name"]+=i
    elif ind>=4 and ind<=8:
        if i!="&nbsp;":
            dic["day"].append(i)

    elif ind==9:
        try:
            dic["start_time"]=int(i.split("-")[0])
            dic["end_time"]=int(i.split("-")[1])
        except:
            dic={"day":[],"Name":""}
            ind=11
    elif ind==10:
        dic["avail"]=int(i)
    ind+=1
        #ind+=1

"""for i in buf:
    if ord(i)==255:
        if (ind==0 or ind==2):# or ind==3):
            nentry+=" : "
            continue
        if (i==3):
            dic[kei[0]]=nentry
        if (i==1):
            dic[kei[1]]=int(entry)
        if (i>=4 and i<=8):
            if entry=
elif ind==9:dic["avail"]=int(i)"""
