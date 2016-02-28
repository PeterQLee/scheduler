
import socket
import RequestServer



r=RequestServer.RequestServer()

r.start()

dat=int.to_bytes(5,3,'big')
while (int.from_bytes(dat,"big")!=0):
    print(dat)
    dat=r.next_message()
    
r.stop()
    
