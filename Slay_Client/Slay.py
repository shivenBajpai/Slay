import contextlib
import datetime
with contextlib.redirect_stdout(None): import pygame
import traceback as tb
from Networking import *
from Constants import *
from Replay_Utils import Replay
from math import floor
import Hex_Utils

freeze = False
debugPos = (1,1)

def HandleFreezing(caption,err):
    if freeze: 
        print(err)
        pygame.display.set_caption(caption)
        while True:
            if pygame.event.poll().type == QUIT: break
    return

def setDebugPos(value):
    global debugPos
    debugPos=value

def main(color,config):

    global freeze
    global debugPos
    freeze=config['freeze']
    DEBUG=config['debug']
    FRAMES_PER_ANIMATION=50-config['animation_speed']

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
    else: screen = pygame.display.set_mode([WINDOWX+200, WINDOWY], flags=pygame.RESIZABLE)
    pygame.display.set_caption('Slay')

    screen.fill((48,48,48))
    screen.blit(pygame.image.load('./Slay_Assets/loading_text.png'),(0,0))
    pygame.display.flip()

    # They need pygame initialized first, so we import them later
    from Sound_Utils import restart_mixer

    restart_mixer(config['volume'])

    from TextureLoader import loadTextures
    from Renderer import cells,drawEntities,drawMapLayer,drawMouseEntity,drawBaseLayer,drawSideBar,reset_renderer,drawDebugger
    from Move_Utils import handleEvent,get_mouse_entity,get_selected_city,set_selected_city,reset_move_utils,Move

    loadTextures()
    reset_move_utils(WINDOWX,WINDOWY,FRAMES_PER_ANIMATION)
    reset_renderer(WINDOWX,WINDOWY)

    pygame.display.set_icon(cells[color][0])

    moves = []
    animations: list[Move] = []
    beat = 0
    startTime = datetime.datetime.now()

    try:
        while True:

            beat += 0.2
            if beat == 20: beat = 0 #beat loops from 0 to 19

            # handle events, includes logic
            for event in pygame.event.get(): handleEvent(event,grid,moves,color,setDebugPos,WINDOWX,WINDOWY,DEBUG)
                
            # talk to server
            network(moves,animations,color,replayFile,Move)

            # draw
            drawBaseLayer(screen,pygame.display.get_window_size()[0]-200,pygame.display.get_window_size()[1])
            drawMapLayer(screen, grid, floor(beat/2)%2==0)
            drawEntities(screen, grid, floor(beat/2)%2==0, color)
            drawSideBar(screen, grid, get_selected_city(), pygame.display.get_window_size()[0]-200, pygame.display.get_window_size()[1]-(200 if DEBUG else 0), color)
            drawMouseEntity(screen, get_mouse_entity(), pygame.mouse.get_pos())
            if DEBUG: drawDebugger(screen,grid,debugPos,pygame.display.get_window_size()[1]-200,pygame.display.get_window_size()[0]-200)
            
            try:
                if animations[0].__class__ == int:
                    set_turn(animations[0])
                    if animations[0] != color: clear_waiting_flag()
                    del animations[0]
                if not animations[0].preanimated:
                    animations[0].preanimation.apply(grid)
                    set_selected_city(fixHighlighting(grid,get_selected_city()))
                if not animations[0].animated or animations[0].animation.animate(screen): 
                    animations[0].postanimation.apply(grid)
                    set_selected_city(Hex_Utils.fixHighlighting(grid,get_selected_city()))
                    del animations[0]
            except IndexError:
                pass
    
            pygame.display.flip()
            time.sleep(1/100)

    except GameEndingException as err:
        replayFile.close()
        HandleFreezing('Slay - Frozen - GameEndingException',err)
        pygame.quit()
        return 'Error: ' + str(err.args[0]), False, 0, 0, 0, 0

    except GameFinishedException as err:
        replayFile.close()
        HandleFreezing('Slay - Frozen - Game Finished','')
        pygame.quit()
        return str(err.args[0]), True, 1, err.args[1], err.args[2], int((datetime.datetime.now()-startTime).total_seconds()//60)

    except Exception as err:
        replayFile.close()
        HandleFreezing('Slay - Frozen - Exception',err)
        pygame.quit()
        print(err)
        tb.print_exc()
        return 'Client-side Error: ' + str(err.args[0]), False, 0, 0, 0, 0