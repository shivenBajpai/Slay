from Net_Utils import *
from Hex_Utils import fixhighlighting
import socket

turn = 0 # corresponds to color/userid whose turn it is. This is not the same as serverside variable turn
color = 0
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class GameEndingException(Exception): ...

def connect(ip,port):

    userid = None
    config = None
    result = None
    global turn, color
    turn = 0
    color = 0

    client.settimeout(3)

    try:
        client.connect((ip,port))
        pack = recieve_message(client)
        if pack.code == Packet.ID:
            userid = pack.data['id']
            config = pack.data['config']
            print('Succesfully connected as id:',userid)
            result = 'Connected, waiting \nfor game to start...'
            color = userid
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

def is_our_turn():
    return turn == color

def get_turn():
    return turn

def network(moves,grid,animations,color,selected_city):

    global our_turn, turn

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
                move.preanimation.apply(grid)
                fixhighlighting(grid,selected_city)
                if move.animation is not None:
                    move.animation.prepare()
                    animations.append(move)

        elif pack.code == Packet.PLAY:
            print('DEBUG: PLAY packet')
            turn = pack.data['turn']

        else:
            print('Invalid server response:', pack.code, pack.data)
            send_message(client,Packet(Packet.LEAVE,{'cause':'Invalid server Response'}))
            client.close()

    except (TimeoutError,socket.timeout): pass
    except (ConnectionAbortedError,ConnectionResetError): raise GameEndingException('Server terminated connection,\nNo context')

    if len(moves) != 0:
        if moves[0].__class__ == str: send_message(client,Packet(Packet.END_TURN))  
        else: send_message(client,Packet(Packet.MOVE,moves[0]))
        our_turn=False
        del moves[0]