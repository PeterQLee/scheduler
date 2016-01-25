
import socket

s=socket.socket()
s.connect(('127.0.0.1',6010))

s.send(b'0')

