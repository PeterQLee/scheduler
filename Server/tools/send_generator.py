import socket
import connectioninfo
def send_generator(num):
    addr=connectioninfo.ip
    port=connectioninfo.optport
    meslen=connectioninfo.mes_len
    try:
        s=socket.socket() #default socket used for comm
    
        s.connect((addr,port))
        
        s.send(int.to_bytes(num,meslen,'big'))
        #TODO: test explicitly for bytes requiring len>1
    except:
        print("Error with connection")
        return False
    return True

