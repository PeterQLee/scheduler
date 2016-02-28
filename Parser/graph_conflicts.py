import networkx
import re
import numpy
from collections import deque
'''parse and input data'''
f=open("courseresult.txt","rb")

data=str(f.read())
buffer=data.split('\\xff')
Graph=networkx.Graph()
curnode=None
ind=0
identitymap={}
curid=-1
remain=[]

for i in buffer:
    
    if re.match("^[A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][0-9]",i):
        ind=0
        #create new node and hashmap entry
        #(nodes are indexed by CID)

    if ind==1:
      #record csid
        curid=int(i)
        identitymap[curid]=[]
        
        remain.append(curid)
    
    if ind>=4 and ind<=8:
        if i!="&nbsp;":
            identitymap[curid].append(-(ind-4))
            identitymap[curid].append((ind-4))
        
    if ind==9:
        
        try:
            (a,b)=i.split("-")
            for k in range(0,len(identitymap[curid]),2):
                identitymap[curid][k]=identitymap[curid][k]*2400-int(a)
                identitymap[curid][k+1]=identitymap[curid][k+1]*2400+int(b)
            Graph.add_node(curid)

        except:
            del identitymap[curid]
            remain.remove(curid)
            
    ind+=1

def fingerwalk(mat1,mat2):
    cur=0
    lastneg=0
    for i in range(0,len(mat2),2):
        while abs(mat1[cur])<abs(mat2[i]):
            cur+=1
            if cur==len(mat1):return True
            
        if cur%2==1: return False #- is between - and +
        
        if abs(mat2[i+1]) >= abs(mat1[cur]): #compare +mat2 to -mat1 
            return False#between the start of a slot in mat1
    
            
    return True
        
        
    """
    for i in mat2:
        #TODO: check bounds
        while abs(mat1[cur])<abs(i):
            cur+=1
            if cur==len(mat1):return True
        
        if (i<0):
            lastneg=i
            if cur>0 and mat1[cur-1]<0:
                return False
        else:
            #endpoint (i>1)
            if mat1[cur]>0:
                #end point to the right, so there is definetly a collision
                return False
            #check if last negativ is bigger
            if cur!=0 and abs(lastneg)<=mat1[cur-1]: #i.e.
                return False
    """
    return True


def conflict(Graph,identities,remain,cur):
    if len(remain)==0: return
    for curh in range(len(remain)):
        
        for h in range(curh+1,len(remain)):
            
            cur=remain[curh]
            i=remain[h]
            x1=identities[cur][0]
            x2=identities[i][0]
            y1=identities[cur][1]
            y2=identities[i][1]

            if not (fingerwalk(identities[cur],identities[i])):
                Graph.add_edge(cur,i)

             
    #conflict(Graph,identities,remain[1:],remain[0])
        #create edge
print (len(remain))
conflict(Graph,identitymap,remain,remain[0])

print("AYY")  
dw=open("graph/indices.dat","w")
#readd=open("graph/read.dat","w")
#for i in Graph.nodes():
#    dw.write (str(i)+":"+str(Graph.neighbors(i))+"\n")

dw.write(str(Graph.nodes()))
adj=networkx.to_numpy_matrix(Graph)
print(str(adj))
numpy.save("adj_matrix",adj)

dw.close()
#print (networkx.adjacency_matrix(Graph).to_numpy_matrix())

