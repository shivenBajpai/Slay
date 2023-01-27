from Net_Utils import *
import socket

our_turn = False
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class GameEndingException(Exception): ...

def connect(ip,port):

    userid = None
    config = None
    result = None
    global our_turn
    our_turn = False

    client.settimeout(3)

    try:
        client.connect((ip,port))
        pack = recieve_message(client)
        if pack.code == Packet.ID:
            userid = pack.data['id']
            config = pack.data['config']
            print('Succesfully connected as id:',userid)
            result = 'Connected, waiting \nfor game to start...'
        elif pack.code == Packet.ERROR:
            print('Failed to connect, error occured:', pack.data)
            result = 'Failed to connect, \nerror occured:' + str(pack.data)
        else:
            print('Failed to connect, invalid server response:', pack.code, pack.data)
            result = 'Failed to connect, \ninvalid server response:' + str(pack.code)
    except (ConnectionRefusedError,TimeoutError):
        print('Failed to connect, Server offline')
        result = 'Failed to connect,\nServer is offline or \nnot accepting connections'
    except(ConnectionResetError):
        print('Failed to connect, Server reset')
        result = 'Failed to connect,\nServer reset unexpectedly'
    except (socket.gaierror):
        print('gaierror')
        result = 'Error resolving address,\ntry again if the issue \npersists,you have the wrong \naddress'

    return result, userid, config

def getGrid():
    grid = None

    client.settimeout(None)

    while grid is None:
        pack = recieve_message(client)

        if pack.code == Packet.LOAD:
            grid = pack.data['grid']
            print('Succesfully recieved grid data')
        else:
            print('Unexpected server response, expected grid data',pack.code,pack.data)
            raise Exception()

    client.settimeout(0.02)

    return grid

def disconnect():
    global client
    client.close()
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def declareExit():
    send_message(client,Packet(Packet.LEAVE))

def send_move():
    pass

def is_our_turn():
    return our_turn

def network(moves,grid,state,animations,color):

    global our_turn

    try:
        pack = recieve_message(client)

        if pack.code == Packet.DISCONNECT:
            print('Connection terminated by server')
            raise GameEndingException('Connection terminated by server,\n' + str(pack.data['error']))

        elif pack.code == Packet.ERROR:
            print('Error occured:', pack.data)
            raise GameEndingException('Serverside Error,\n' + str(pack.data['error']))

        elif pack.code == Packet.UPDATE:
            if pack.data.metadata['source'] != color: 
                move = pack.data
                move.animation.prepare()
                move.preanimation.apply(grid,state)
                animations.append(move)

        elif pack.code == Packet.PLAY:
            print('DEBUG: Permission to play')
            our_turn = True

        else:
            print('Invalid server response:', pack.code, pack.data)
            send_message(client,Packet(Packet.LEAVE,{'cause':'Invalid server Response'}))
            client.close()

    except TimeoutError: pass
    except (ConnectionAbortedError,ConnectionResetError): raise GameEndingException('Server terminated connection,\nNo context')

    if len(moves) != 0:
        print(moves)
        send_message(client,Packet(Packet.MOVE,moves[0]))
        our_turn=False
        del moves[0]