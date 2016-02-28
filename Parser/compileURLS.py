import re
import urllib.request
import time
import sys
class CompilePages:
    def __init__(self,location,term):
        self.DIRECTORY="urldata/"
        locations_D={"halifax":"100","truro":"200","distance":"300","other":"400"}
        term_D={"fall":"10","winter":"20","summer":"30"}
        self.tablelink="https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule"

        self.location=locations_D[location]
        self.term=term_D[term]

    def findLinks(self):
        #send request for the appropriate listings
        addr=self.tablelink+"?s_term=2016"+self.term+"&s_district="+self.location
        cname_file=open(self.DIRECTORY+"cnames.txt","w")

        #gather appropriate subjects into cnames.txt
        request=urllib.request.urlopen(addr)
        rq=request.read().decode("utf-8")
        #todo: exception handling
        #print(addr)
        #print(rq)
        matches=re.findall(r'<a href="fysktime.P_DisplaySchedule.*</a>\n',rq,re.IGNORECASE)
        #print(matches)
        for i in matches:
            cname_file.write(i)
        cname_file.close()
    

    def findPageRange(self,link):
        pass
    def compileLinks(self):
        f=open(self.DIRECTORY+"cnames.txt","r")
        c=open(self.DIRECTORY+"urs.txt","w")
        m=f.readline()
        prefix="https://dalonline.dal.ca/PROD/"
        while m != "":
            #print(m+"____________")
            l=re.sub('<[Aa] [Hh][Rr][Ee][Ff]="','',m,re.IGNORECASE)
            l=re.sub("</[Aa]>",'',l,re.IGNORECASE)
            l=re.sub("<.*",'',l)
            #print(l)
            m=f.readline()
            if len(l)>1: #if it isn't a <BR>
                l=re.sub("\">",":",l) #replace end quote and bracket with colon
                l=re.sub(r" +","_",l) #replace all spaces with underscores
                #l=re.sub(r"\&","and",l)
                l=re.sub(r"\'","",l) #delete all single quotes
                
                c.write(prefix+l)
        f.close()
        c.close()



    def srch(self,st):
            #extract the name from the html doc
        #WTF???
        start=re.findall(r"\"detthdr\".*</TD>\s+</TD>",st,re.DOTALL|re.IGNORECASE)
        
        ret=""
        if (len(start))==0:
            return None
        
        #for i in start:
        #    ret=i
        ret=start[len(start)-1]
        return ret
    
    def curlpages(self,delay=1):
        #curl the pages and save the relevant data in the appropriate files
        f=open(self.DIRECTORY+"urs.txt","r")

        m=f.readline()
        dir="htwpages/"
        
        
        while m!="":
            k=re.findall(r":\w",m)
            st=re.split(r":\w",m)
            st[1]=k[0][1]+st[1][:len(st[1])-1]
            print(st)
            st[1]=re.sub("\&","and",st[1])
            n=1

            c=open(dir+st[1]+".txt","w")
            validpage=True
            while validpage:
                try:
                    kd=urllib.request.urlopen(st[0]+"&n="+str(n))
                except:
                    thread.sleep(30)#retry??
                    continue
           
                htfile=kd.read().decode("utf-8")
            #get only the relevant data
                trimmed=self.srch(htfile)
                if (trimmed==None): break
                else:
                    c.write(trimmed)
                    time.sleep(1)
                    n+=20
            c.close()
            m=f.readline()
            
    
        """
        k=re.findall(r":\w",m)
        st=re.split(r":\w",m)
        st[1]=k[0][1]+st[1][:len(st[1])-1]
        print(st)
        st[1]=re.sub("\&","and",st[1])
        c=open(dir+st[1]+".txt","w")
        kd=urllib.request.urlopen(st[0])
            #error checking
        htfile=kd.read().decode("utf-8")
        #print (htfile)
            #get only the relevant data
        trimmed=self.srch(htfile)
        print(trimmed)
        c.write(trimmed)
        c.close()
        m=f.readline()
    """
     

print(sys.argv)        
c=CompilePages("halifax",sys.argv[1])
c.findLinks()
c.compileLinks()
c.curlpages()
