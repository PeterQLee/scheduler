import networkx
import re
from collections import deque
'''parse and input data'''
f=open("courseresult.txt","rb")

data=f.read()
buffer=data.split('\\xff')
Graph=networkx.Graph()
curnode=None
for i in buffer:
    if re.match("^[A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][0-9]",i):

        #create new node and hashmap entry


def conflict(Graph,identities,remain,cur):
    for i in remain:
        x1=identities[cur][0]
        x2=identities[i][0]
        y1=identities[cur][1]
        y2=identities[i][1]
        if (x1>=x2 and x1<=y2):
            #conflcit!!!, create edge
            pass
        if (y1>=x2 and y1<=y2):
            pass
        #redundant
        '''
        if (x2>=x1 and x2<=y1):
            pass
        if (y2>=x1 and y2<=x1):
            pass
'''
