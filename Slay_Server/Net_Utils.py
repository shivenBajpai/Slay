import pickle
import socket
import time
from Constants import PORT, DISCOVERABLE, NAME, PUBLIC, MAX_COLOR

HEADERSIZE = 16

def send_message(socket,msg):
    msg = pickle.dumps(msg)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}','utf-8') + msg
    socket.sendall(msg)
    time.sleep(0.1)
    return

def fast_recieve_message(socket):
    msglen = int(socket.recv(HEADERSIZE))
    msg = pickle.loads(socket.recv(msglen))
    return msg

def recieve_message(socket,debug=True):
    remaining = int(socket.recv(HEADERSIZE))
    msg = b''
    while remaining!=0:
        if remaining > 2048: size = 2048
        else: size = remaining
        msg = msg + socket.recv(size)
        remaining = remaining - size
    return pickle.loads(msg)

def broadcast(connections,message):
    for addr,conn in connections.items():
        send_message(conn,message)

def handleDiscoveryRequests(sock,players,state):
    if DISCOVERABLE:
        while True:
            try: 
                data, _ = sock.recvfrom(1024)
                if data == b'discovery':
                    sock.sendto(pickle.dumps(ServerInfo(players,state)), ("255.255.255.255", 5005))
                else: pass
            except (TimeoutError,socket.timeout): 
                break

class Packet:

    # status codes
    END = 0         # Game Ended Gracefully
    ID = 1          # ID and Config data
    LOAD = 2        # Initial Grid state
    UPDATE = 3      # Update to game state
    PING = 4        # Ping Request
    PLAY = 5        # Instruct client to play
    MOVE = 6        # Move from player
    END_TURN = 7    # Indicate end of turn
    ERROR = 8       # Serverside Error, Command to terminate connection + context (from server only)
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

    def __init__(self,players,state):
        self.Name = NAME
        self.Address = (socket.gethostbyname(socket.gethostname()),PORT)
        self.Players = (players,MAX_COLOR)
        self.Status = ServerInfo.WAITING
        self.Type = bool(PUBLIC)

class PlayerDisconnectException(Exception): ...