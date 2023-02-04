import socket
from Net_Utils import *
from Constants import *
from Hex_Utils import *

clients = []

# Prepare for game
serverside_grid = createGrid()
severside_state = {}
turn = 0

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((IP,PORT))
server_socket.listen(MAX_COLOR+1)

connections = {}

print('Server listening on port', PORT)

# Wait for adequate players to join
while True:
    conn, addr = server_socket.accept()
    connections[addr] = conn
    send_message(conn,Packet(
        Packet.ID,
        {'id':len(connections),'config':{'XSIZE':XSIZE,'YSIZE':YSIZE}}    
    ))
    print('connection from:',addr)
    if len(connections) == MAX_COLOR: break

# Send initial grid to connections
for addr in connections:
    send_message(connections[addr],Packet(
        Packet.LOAD,
        {'grid':serverside_grid}
    ))
    connections[addr].settimeout(0.1)

try:

    send_message(list(connections.values())[turn],Packet(Packet.PLAY))

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
                            for addr,conn in connections.items():
                                send_message(conn,Packet(
                                    Packet.UPDATE,
                                    pack.data
                                ))

                            pack.data.preanimation.apply(serverside_grid,severside_state)
                            pack.data.postanimation.apply(serverside_grid,severside_state)

                            send_message(list(connections.values())[turn],Packet(Packet.PLAY))
                        else: 
                            print('Attempted play out of turn')

                    elif pack.code == Packet.END_TURN:
                        print(f'recieved turn end from {addr}')
                        if list(connections.keys()).index(addr) == turn:

                            turn += 1
                            if turn == len(connections): 
                                turn = 0
                                # TODO: serverside updates

                            send_message(list(connections.values())[turn],Packet(Packet.PLAY))
                        else: 
                            print('Attempted end out of turn')

                    else: 
                        print(f'invalid Packet by {addr}',pack.code,pack.data)

                except TimeoutError:
                    pass

            time.sleep(0.1)

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

except BaseException as err:
    print('Unexpected Error! Shutting down...')
    for conn in connections.values():
        try:
            send_message(conn,Packet(
                Packet.ERROR,
                {'error':err}
            ))
        except Exception: pass
    raise err

exit()
