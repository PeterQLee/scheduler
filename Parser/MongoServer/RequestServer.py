import socket
import threading
import time
from collections import deque


class RequestServer:
    '''
    A server for recieving requests via the front end page
    '''

    def __init__(self):
        '''
        initialize network and default data
        '''
        self.listen_thread=None
        self.listen_flag=True

        self.hostname='127.0.0.1'
        self.port=6010 #?
        #self.S_TYPE=socket.SOCKET_STREAM
        self.banl={"127.0.0.1"} #TODO: configure to match all local hosts
        self.request_queue=deque()
        
        #try:
            #self.list_socket=socket.socket(family=self.S_TYPE,)
    def load_config(self,filename):
        pass
    def start(self):
        '''
        start and bind the server
        '''
        try:
            #configure types later
            self.message_socket=socket.socket()
            self.message_socket.bind((self.hostname,self.port))
            self.listen_flag=True

            #start thread
            thr=threading.Thread(target = self.run, args=())
            thr.start()
            self.listen_thread=thr
        except:
            print("Cannot host server on port "+str(self.port))
    
    def run(self):
        '''
        function to be ran on another thread and record requests
        '''
        while self.listen_flag:
            print("MM")
            self.message_socket.listen(1)
            info=self.message_socket.accept()
            addr=info[1]
            conn=info[0]
            if addr in self.banl:
                print("REJECTED CLIENT")
                conn.close()
                continue
            else:
                message=conn.recv(256) #fix arbitrary size
                conn.send(bytes(1))
                self.request_queue.appendleft(message) #TODO, only enqueue unique messages??
                conn.close()
        
    def next_message(self):
        while len(self.request_queue)==0:
            #TODO: optimize
            time.sleep(5)
            pass
        return self.request_queue.pop()
    def stop(self):
        self.listen_flag=False
        s=socket.socket(socket.AF_INET, 
                      socket.SOCK_STREAM)
        s.connect((self.hostname,self.port))
        s.send(b'0')

        s.close()

                                                 
        
#test script
if __name__=="__main__":
    r=RequestServer()
    r.start()
    time.sleep(1)
    r.stop()
