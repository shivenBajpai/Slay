import socket
import pickle

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),4444))

s.sendall(b'SENDIT')
data = s.recv(2048)
print(pickle.loads(data))


