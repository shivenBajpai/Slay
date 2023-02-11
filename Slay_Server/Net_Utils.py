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

def broadcast(connections,message):
    for addr,conn in connections.items():
        send_message(conn,message)

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

    def __init__(self,code,data={}):
        self.code = code
        self.data = data

class PlayerDisconnectException(Exception): ...