import re

DIRECTORY="urldata/"

f=open(urldata+"cnames.txt","r")
c=open(urldata+"urs.txt","w")
m=f.readline()
prefix="https://dalonline.dal.ca/PROD/"
while m != "":
    l=re.sub("<A HREF=\"",'',m,re.IGNORECASE)
    l=re.sub("</A>",'',l,re.IGNORECASE)
    l=re.sub("<.*",'',l)
    print(l)
    m=f.readline()
    if len(l)!=1:
        l=re.sub("\">",":",l)
        l=re.sub(r" +","_",l)
        #l=re.sub(r"\&","and",l)
        l=re.sub(r"\'","",l)
        c.write(prefix+l)

