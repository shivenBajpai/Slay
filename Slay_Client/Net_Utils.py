import pickle
import time

HEADERSIZE = 16

def send_message(socket,msg):
    msg = pickle.dumps(msg)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}','utf-8') + msg
    socket.sendall(msg)
    time.sleep(0.1)
    return
    
def recieve_message(socket):
    msglen = int(socket.recv(HEADERSIZE))
    msg = pickle.loads(socket.recv(msglen))
    return msg

class Packet:

    # status codes
    OK = 0      # Acknowledgement code
    ID = 1      # ID and GRID data
    LOAD = 2    # initial game state data (REDUNDANT, using ID for both)
    UPDATE = 3  # Update to game state
    PING = 4    # Ping Request
    PLAY = 5    # Instruct client to play
    MOVE = 6    # Move from player
    ERROR = 7   # Error
    FULL = 8    # Deny connection, party full (REDUNDANT, never sent)
    LEAVE = 9       # Indicate termination of connection (from client)
    DISCONNECT = 10 # Request to terminate connection (from server)

    def __init__(self,code,data={}):
        self.code = code
        self.data = data