import socket
import copy
import sys
from Net_Utils import *
from Constants import *
from Hex_Utils import *
from Move_Utils import Move, GameUpdate

clients = []
class GameOver(Exception): ...

# Prepare for game
serverside_grid = createGrid()
turn = 0 # Corresponds to index in connections list of player whose turn it is. Does not match with client-side variable turn
activePlayers = [item for item in range(1, MAX_COLOR+1)]

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((IP,PORT))
server_socket.listen(MAX_COLOR+1)
server_socket.settimeout(0.1)

discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
discovery_socket.bind(("0.0.0.0", 5005))
discovery_socket.settimeout(0.5)

connections = {}

print('Server listening on port', PORT)
print(f'Server Discovery: {DISCOVERABLE}')

# Wait for adequate players to join
while True:
    try:
        conn, addr = server_socket.accept()
        print('connection from:',addr)
        pack = recieve_message(conn)
        conn.settimeout(0.1)
        if pack.__class__ != Packet: 
            print('illegal, bounced')
            conn.close()
            continue
        if pack.code == Packet.SERVERINFO: 
            print('serverinfo request')
            send_message(conn,Packet(Packet.SERVERINFO,{'public':PUBLIC}))
            conn.close()
            continue
        if pack.code != Packet.CONNECT: 
            print('inappropriate, bounced')
            conn.close()
            continue
        if not PUBLIC and pack.data['password'] != PASSWORD:
            print(f'wrong password, bounced ${pack.data["password"]}$ ${PASSWORD}$')
            send_message(conn,Packet(Packet.ERROR,'Wrong Password'))
            conn.close()
            continue
        connections[addr] = conn
        send_message(conn,Packet(
            Packet.ID,
            {'id':len(connections),'config':{'XSIZE':XSIZE,'YSIZE':YSIZE}}    
        ))
        if len(connections) == MAX_COLOR: break
    except Exception:
        pass
    finally:
        handleDiscoveryRequests(discovery_socket,len(connections),ServerInfo.WAITING)

    for addr, conn in connections.items():
        try:
            pack = recieve_message(conn)
            if pack.code == Packet.LEAVE:
                print(f'Leave request from {addr}',pack.code,pack.data)
                raise PlayerDisconnectException(addr)
        except (TimeoutError,socket.timeout): pass
        except PlayerDisconnectException as err:
            addr = err.args[0]
            player = COLOR_MAPPING[list(connections.keys()).index(addr)]
            for conn in connections.values():
                try:
                    send_message(conn,Packet(
                        Packet.DISCONNECT,
                        {'error':f'{player} disconnected'}
                    ))
                except Exception: pass
            sys.exit(f'Known Disconnect by {player}, {addr}! Shutting down...')            

# Send initial grid to connections
for addr in connections:
    send_message(connections[addr],Packet(
        Packet.LOAD,
        {'grid':serverside_grid}
    ))
    connections[addr].settimeout(0.1)

try:

    for addr,conn in connections.items():
        send_message(conn,Packet(
            Packet.PLAY,
            {'turn':turn+1}    
        ))

    while True:
            for addr, conn in connections.items():
                try:
                    pack = recieve_message(conn)
                    print('Recieved packet from:',addr)

                    if pack.code == Packet.PING:
                        send_message(conn,Packet(Packet.OK))

                    elif pack.code == Packet.LEAVE:
                        print(f'Leave request from {addr}',pack.code,pack.data)
                        raise PlayerDisconnectException(addr)

                    elif pack.code == Packet.MOVE:
                        print(f'recieved move from {addr}')
                        if list(connections.keys()).index(addr) == turn:
                            broadcast(connections,Packet(Packet.UPDATE,pack.data))
                            broadcast(connections,Packet(Packet.PLAY,{'turn':turn+1}))

                            pack.data.preanimation.apply(serverside_grid)
                            pack.data.postanimation.apply(serverside_grid)
                        else: 
                            print('Attempted play out of turn')

                    elif pack.code == Packet.END_TURN:
                        print(f'recieved turn end from {addr}')
                        if list(connections.keys()).index(addr) == turn:

                            turn += 1
                            if turn == len(activePlayers): 
                                turn = 0
                                move = Move({'source':0},GameUpdate([]),None,GameUpdate([]))
                                if winCheck(serverside_grid,activePlayers):
                                    broadcast(connections,Packet(Packet.END,{'winner':activePlayers[0]-1}))
                                    raise GameOver(activePlayers[0])
                                else:
                                    for cell in roundupdate(serverside_grid): move.preanimation.gridChanges.append((cell,copy.deepcopy(serverside_grid[cell[0]][cell[1]])))
                                    broadcast(connections,Packet(Packet.UPDATE,move))

                            broadcast(connections,Packet(Packet.PLAY,{'turn':activePlayers[turn]}))

                        else: 
                            print('Attempted end out of turn')

                    else: 
                        print(f'invalid Packet by {addr}',pack.code,pack.data)

                except (TimeoutError,socket.timeout):
                    pass

            time.sleep(0.1)
            handleDiscoveryRequests(discovery_socket,MAX_COLOR,ServerInfo.IN_GAME)

except (ConnectionAbortedError,ConnectionResetError,ValueError) as err:

    print(err)

    print('Unexpected Disconnect! Shutting down...')
    for conn in connections.values():
        try:
            send_message(conn,Packet(
                Packet.DISCONNECT,
                {'error':'Someone disconnected'}
            ))
        except Exception: pass

    sys.exit(err)

except PlayerDisconnectException as err:
    addr = err.args[0]
    player = COLOR_MAPPING[list(connections.keys()).index(addr)]
    print(f'Known Disconnect by {player}, {addr}! Shutting down...')
    for conn in connections.values():
        try:
            send_message(conn,Packet(
                Packet.DISCONNECT,
                {'error':f'{player} disconnected'}
            ))
        except Exception: pass

except GameOver as err:
    print(f'Player {err} won!, Shutting down...')

except BaseException as err:
    print('Unexpected Error! Shutting down...')
    for conn in connections.values():
        try:
            send_message(conn,Packet(
                Packet.ERROR,
                {'error':err}
            ))
        except Exception: pass
    sys.exit(err)

sys.exit(0)
