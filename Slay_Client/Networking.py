from Net_Utils import *
from Hex_Utils import fixHighlighting
from Constants import NAME_MAPPING
from pygame.locals import QUIT
import integratedServer.Net_Utils
import socket
import traceback as tb

turn = 0 # corresponds to color/userid whose turn it is. This is not the same as serverside variable turn
color = 0
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
waitingFlag = False

timeoutErrors = (TimeoutError,socket.timeout)

discovery = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
discovery.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
discovery.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
discovery.bind(("0.0.0.0", 5005))
discovery.settimeout(0.1)

class GameEndingException(Exception): ...

class GameFinishedException(Exception): ...

class GridLoadException(Exception): ...

def connect(ip,port,password=None,info_req=False,):

    userid = None
    config = None
    result = None
    global turn, color
    turn = 0
    color = 0

    client.settimeout(3)

    try:
        client.connect((ip,port))

        if info_req:
            send_message(client,Packet(Packet.SERVERINFO))
            pack = recieve_message(client)
            print(pack.data)
            disconnect()
            return pack.data

        send_message(client,Packet(Packet.CONNECT,{'password':password}))
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
            disconnect()
        else:
            print('Failed to connect, invalid server response:', pack.code, pack.data)
            result = 'Failed to connect, \ninvalid server response:' + str(pack.code)
            disconnect()

    except (ConnectionRefusedError,TimeoutError,socket.timeout):
        print('Failed to connect, Server offline')
        result = 'Failed to connect,\nServer is offline or \nnot accepting connections'
        disconnect() # just in case of weird behaviour
    except(ConnectionResetError):
        print('Failed to connect, Server reset')
        result = 'Failed to connect,\nServer reset unexpectedly'
    except(Exception) as err: # if this stops working, this used to be BaseException
        print('Failed to connect')
        print(err)
        tb.print_exc()
        result = 'Failed to connect, ' + str(err)

    return result, userid, config

def getGrid(event_getter,replayFile):
    grid = None
    client.settimeout(0.01)

    while grid is None:
        try:
            pack = recieve_message(client,debug=True)

            if pack.code == Packet.LOAD:
                grid = pack.data['grid']
                print('Succesfully recieved grid data')
                replayFile.writeNext(grid)
            else:
                print('Unexpected server response, expected grid data',pack.code,pack.data)
                raise GridLoadException(pack.data)
            
        except (TimeoutError,socket.timeout): pass
        finally: 
            if event_getter().type == QUIT: 
                declareExit()
                raise GridLoadException('User quit')

    return grid

def disconnect():
    global client
    client.close()
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def declareExit():
    send_message(client,Packet(Packet.LEAVE))

def is_our_turn():
    if waitingFlag: return False
    return turn == color

def get_turn():
    return turn

def network(moves,grid,animations,color,selected_city,set_selected_city,replayFile):

    global our_turn, turn, waitingFlag

    try:
        pack = recieve_message(client)
        replayFile.writeNext(pack)

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
                set_selected_city(fixHighlighting(grid,selected_city))
                if move.animation is not None:
                    move.animation.prepare()
                    animations.append(move)

        elif pack.code == Packet.PLAY:
            waitingFlag = False
            turn = pack.data['turn']

        elif pack.code == Packet.END:
            print('Player',pack.data['winner'],'won')
            raise GameFinishedException('Game Ended: ' + NAME_MAPPING[pack.data['winner']] + ' victory!')

        else:
            print('Invalid server response:', pack.code, pack.data)
            send_message(client,Packet(Packet.LEAVE,{'cause':'Invalid server Response'}))
            client.close()

    except (TimeoutError,socket.timeout): pass
    except (ConnectionAbortedError,ConnectionResetError): raise GameEndingException('Server terminated connection,\nNo context')

    if len(moves) != 0:
        if moves[0].__class__ == str: 
            waitingFlag = True
            send_message(client,Packet(Packet.END_TURN))  
        else: send_message(client,Packet(Packet.MOVE,moves[0]))
        our_turn=False
        del moves[0]

def getServers(servers,server_ips):
    try:
        discovery.sendto(bytes("discovery", "utf-8"), ("255.255.255.255", 5005))
        while True:
            data, _ = discovery.recvfrom(1024)
            if data == b'discovery': continue
            try: data = pickle.loads(data)
            except: continue
            if data.__class__ != ServerInfo and data.__class__ != integratedServer.Net_Utils.ServerInfo: continue
            if data.Address in server_ips: continue
            servers.append(data)
            server_ips.append(data.Address)
    except (TimeoutError,socket.timeout): pass

def closeDiscovery():
    discovery.close()