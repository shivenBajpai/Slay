import pickle
import socket
import time

HEADERSIZE = 16

def send_message(socket,msg):
    msg = pickle.dumps(msg)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}','utf-8') + msg
    socket.sendall(msg)
    time.sleep(0.1)
    return
    
def fast_recieve_message(socket,debug=True):
    msglen = int(socket.recv(HEADERSIZE))
    if debug: print(msglen)
    msg = pickle.loads(socket.recv(msglen))
    return msg
    
def recieve_message(socket,debug=True):
    remaining = int(socket.recv(HEADERSIZE))
    msg = b''
    while remaining!=0:
        if remaining > 2048: size = 2048
        else: size = remaining
        if debug: print('remaining',remaining,', pulling',size)
        msg = msg + socket.recv(size)
        remaining = remaining - size
    return pickle.loads(msg)

class Packet:

    # status codes
    END = 0      # Game Ended Gracefully
    ID = 1      # ID and Config data
    LOAD = 2    # Initial Grid state
    UPDATE = 3  # Update to game state
    PING = 4    # Ping Request
    PLAY = 5    # Instruct client to play
    MOVE = 6    # Move from player
    END_TURN = 7 # Indicate end of turn
    ERROR = 8   # Serverside Error, Command to terminate connection + context (from server only)
    LEAVE = 9       # Indicate termination of connection + context (from client only)
    DISCONNECT = 10 # Command to terminate connection + context (from server only)
    CONNECT = 11       # Request to connect, Password-Carrying packet
    SERVERINFO = 12 # Request data related to server

    def __init__(self,code,data={}):
        self.code = code
        self.data = data

class ServerInfo:

    PUBLIC = True
    PRIVATE = False

    WAITING = 0
    IN_GAME = 1

    def __init__(self,name):
        self.Name = name
        self.Address = socket.gethostbyname(socket.gethostname())
        self.Players = (0,0)
        self.Status = ServerInfo.WAITING
        self.Type = ServerInfo.PUBLIC

def type(x):
    if x == ServerInfo.PUBLIC: return 'Public'
    if x == ServerInfo.PRIVATE: return 'Private'
    return ''

def status(x):
    if x == ServerInfo.WAITING: return 'Waiting'
    if x == ServerInfo.IN_GAME: return 'In Game'
    return ''

def players(x):
    return str(x[0])+'/'+str(x[1])

def address(x):
    return x[0]+':'+str(x[1])