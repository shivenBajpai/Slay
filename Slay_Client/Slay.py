import contextlib
with contextlib.redirect_stdout(None): import pygame
import traceback as tb
from Networking import *
from Constants import *
from Debugger import DEBUG,FREEZE,HandleFreezing,GetDebugPos
from Replay_Utils import Replay
from math import floor
import Hex_Utils

def main(color,config):

    screen = pygame.display.set_mode([640, 480])
    pygame.display.set_caption('Slay')

    screen.fill((48,48,48))
    screen.blit(pygame.image.load('./Slay_Assets/waiting_text.png'),(0,0))
    pygame.display.flip()
    
    replayFile = Replay()
    replayFile.writeNext(config)

    try: 
        grid = getGrid(pygame.event.poll,replayFile)
    except GridLoadException as err: 
        pygame.quit()
        return 'Failed to load game: ' + str(err), False
        
    Hex_Utils.xsize = config['XSIZE']
    Hex_Utils.ysize = config['YSIZE']
    WINDOWX = (config['XSIZE']+1)*48 + 32 
    WINDOWY = (config['YSIZE']+1)*36 + 24
    if WINDOWY<YMIN: WINDOWY = YMIN

    if DEBUG: screen = pygame.display.set_mode([WINDOWX+200, WINDOWY+200])
    else: screen = pygame.display.set_mode([WINDOWX+200, WINDOWY])
    pygame.display.set_caption('Slay')

    screen.fill((48,48,48))
    screen.blit(pygame.image.load('./Slay_Assets/loading_text.png'),(0,0))
    pygame.display.flip()

    # They need pygame initialized first, so we import them later
    from Sound_Utils import restart_mixer

    restart_mixer(config['VOL'])

    from Renderer import cells,drawEntities,drawMapLayer,drawMouseEntity,drawBaseLayer,drawSideBar,reset_renderer,drawDebugger
    from Move_Utils import handleEvent,get_mouse_entity,get_selected_city,set_selected_city,reset_move_utils

    reset_move_utils(WINDOWX,WINDOWY)
    reset_renderer(WINDOWX,WINDOWY)

    pygame.display.set_icon(cells[color][0])

    moves = []
    animations = []
    beat = 0

    try:
        while True:

            beat += 0.2
            if beat == 20: beat = 0 #beat loops from 0 to 19

            # handle events, includes logic
            for event in pygame.event.get(): handleEvent(event,grid,moves,color)
                
            # talk to server
            network(moves,grid,animations,color,get_selected_city(),set_selected_city,replayFile)

            # draw
            drawBaseLayer(screen,WINDOWX,WINDOWY)
            drawMapLayer(screen, grid, floor(beat/2)%2==0)
            drawEntities(screen, grid, floor(beat/2)%2==0, color)
            drawSideBar(screen, grid, get_selected_city(), WINDOWX, WINDOWY, color)
            drawMouseEntity(screen, get_mouse_entity(), pygame.mouse.get_pos())
            if DEBUG: drawDebugger(screen,grid,GetDebugPos(),WINDOWY,WINDOWX)

            for index, animation in enumerate(animations):
                if animation.animation.animate(screen): 
                    animation.postanimation.apply(grid)
                    set_selected_city(Hex_Utils.fixHighlighting(grid,get_selected_city()))
                    del animations[index]
    
            pygame.display.flip()
            time.sleep(1/100)

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