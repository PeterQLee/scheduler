import urllib.request
import re
import time

DIRECTORY="urldata/"


def srch(st):
    #extract the name from the html doc
    #start=re.findall(r"\"detthdr\".*</TD>\s+</TD>",st,re.DOTALL)
    start=re.findall(r"\"detthdr\".*</TD>.*</TD>",st,re.DOTALL)
    ret=""
    for i in start:
        ret=i
    return ret
f=open(DIRECTORY+"urs.txt","r")

m=f.readline()
dir="htwpages/"
while m!="":
    k=re.findall(r":\w",m)
    st=re.split(r":\w",m)
    st[1]=k[0][1]+st[1][:len(st[1])-1]
    print(st)
    st[1]=re.sub("\&","and",st[1])
    c=open(dir+st[1]+".txt","w")
    kd=urllib.request.urlopen(st[0])
    #error checking
    htfile=kd.read().decode("utf-8")
    #get only the relevant data
    trimmed=srch(htfile)
    c.write(trimmed)
    c.close()
    m=f.readline()
    
    time.sleep(1)
