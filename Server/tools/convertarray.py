#coverts array to a json array
import json
from io import StringIO
def convertarray(data):
    # s="["
    ## for i in data:
    #    for b in i:
    #        s+=str(i[b])
    #    s+=","
    #s+="]"
    #this may not work...
    s=StringIO()
    json.dump(data,s)
    return s.getValue()
