import contextlib
with contextlib.redirect_stdout(None): import pygame
import traceback as tb
from Networking import *
from Constants import *
from Debugger import DEBUG,HandleFreezing,GetDebugPos
from Replay_Utils import Replay
from math import floor
import Hex_Utils

def main(filename):

    try:
        replayFile = Replay(filename)
        config = replayFile.readNext()
    except Exception: 
        return 'Broken Replay File' ,False

    screen = pygame.display.set_mode([640, 480])
    pygame.display.set_caption('Slay')

    grid = replayFile.readNext()
        
    Hex_Utils.xsize = config['XSIZE']
    Hex_Utils.ysize = config['YSIZE']
    WINDOWX = (config['XSIZE']+1)*48 + 32 
    WINDOWY = (config['YSIZE']+1)*36 + 24
    if WINDOWY<YMIN: WINDOWY = YMIN

    if DEBUG: screen = pygame.display.set_mode([WINDOWX+200, WINDOWY+200])
    else: screen = pygame.display.set_mode([WINDOWX+200, WINDOWY])
    pygame.display.set_caption(f'Slay Replay - {filename}')

    screen.fill((48,48,48))
    screen.blit(pygame.image.load('./Slay_Assets/loading_text.png'),(0,0))
    pygame.display.flip()

    from Renderer import cells,drawEntities,drawMapLayer,drawMouseEntity,drawBaseLayer,drawReplaySideBar,reset_renderer,drawDebugger
    from Move_Utils import handleReplayEvent,get_mouse_entity,reset_move_utils

    reset_move_utils(WINDOWX,WINDOWY)
    reset_renderer(WINDOWX,WINDOWY)

    pygame.display.set_icon(cells[0][0])

    running = True
    moves = []
    beat = 0
    curr_color = 1
    last_packet = None

    try:
        while running:

            beat += 0.2
            if beat == 20: beat = 0 #beat loops from 0 to 19

            # handle events
            for event in pygame.event.get(): handleReplayEvent(event,moves)

            try:
                # check if we have ended
                if last_packet is not None and moves[-1] == 'next':
                    if last_packet.code == Packet.DISCONNECT:
                        print('Connection terminated by server')
                        raise GameEndingException('Connection terminated by server,\n' + str(last_packet.data['error']))

                    elif last_packet.code == Packet.ERROR:
                        print('Error occured:', last_packet.data)
                        raise GameEndingException('Serverside Error,\n' + str(last_packet.data['error']))

                    elif last_packet.code == Packet.END:
                        print('Player',last_packet.data['winner'],'won')
                        raise GameFinishedException('Game Ended: ' + NAME_MAPPING[last_packet.data['winner']] + ' victory!')

                    else:
                        print('Invalid server response:', last_packet.code, last_packet.data)
                        raise GameEndingException('Invalid Server Response,\n' + str(last_packet.data['error']))
                
                # load the events
                if moves[-1] == 'next':
                    moves.pop()
                    while True:
                        try: pack = replayFile.readNext()
                        except StopIteration: raise GameEndingException('Unexpected End of replay file')
                        if pack.code == Packet.UPDATE: moves.append(pack.data)
                        elif pack.code == Packet.PLAY:
                            if pack.data['turn'] != curr_color:
                                curr_color = pack.data['turn']
                                break 
                            curr_color = pack.data['turn']
                        else:
                            last_packet = pack
                            break
            except IndexError: pass


            # draw
            drawBaseLayer(screen,WINDOWX,WINDOWY)
            drawMapLayer(screen, grid, floor(beat/2)%2==0,renderSelections=False)
            drawEntities(screen, grid, floor(beat/2)%2==0, color)
            drawReplaySideBar(screen, grid, WINDOWX, WINDOWY)
            drawMouseEntity(screen, get_mouse_entity(), pygame.mouse.get_pos())
            if DEBUG: drawDebugger(screen,grid,GetDebugPos(),WINDOWY,WINDOWX)

            #carry out the moves
            for move in moves:
                move.preanimation.apply(grid)
                move.postanimation.apply(grid)
            moves = []
    
            pygame.display.flip()
            time.sleep(1/50)
        print('Broke out!')
    except GameEndingException as err:
        replayFile.close()
        HandleFreezing('Slay - Frozen - GameEndingException',err)
        pygame.quit()
        return 'Error: ' + str(err), False

    except GameFinishedException as err:
        replayFile.close()
        HandleFreezing('Slay - Frozen - Game Finished','')
        pygame.quit()
        return str(err), True

    except Exception as err:
        replayFile.close()
        HandleFreezing('Slay - Frozen - Exception',err)
        pygame.quit()
        print(err)
        tb.print_exc()
        return 'Client-side Error: ' + str(err), False