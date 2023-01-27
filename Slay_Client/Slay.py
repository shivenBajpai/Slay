import contextlib
with contextlib.redirect_stdout(None): import pygame
from Networking import *
from Constants import *
from math import floor
import Hex_Utils

def main(grid,color,config):

    Hex_Utils.xsize = config['XSIZE']
    Hex_Utils.ysize = config['YSIZE']
    WINDOWX = (config['XSIZE']+1)*48 + 32 
    WINDOWY = (config['YSIZE']+1)*36 + 24

    pygame.init()
    if not pygame.font.get_init(): pygame.font.init()
    font = pygame.font.Font('./Slay_Assets/RobotoMono-VariableFont_wght.ttf',15)
    screen = pygame.display.set_mode([WINDOWX+ 200, WINDOWY])
    pygame.display.set_caption('Slay')

    from Renderer import cells,drawEntities,drawMapLayer,drawMouseEntity
    from Move_Utils import handleEvent,get_mouse_entity,reset_move_utils

    pygame.display.set_icon(cells[color][0])

    running = True
    moves = []
    animations = []
    state = {}
    beat = 0
    reset_move_utils()

    try:
        while running:

            beat += 0.2
            if beat == 20: beat = 0 #beat loops from 0 to 19

            for event in pygame.event.get():
                handleEvent(event,grid,moves,color)
                '''if event.type == QUIT: declareExit()

                elif event.type == MOUSEMOTION: mouse_pos = Hex_Utils.cursor_on_grid(mouse_pos)

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                    mousedown = True

                    if is_our_turn() and grid[mouse_pos[0]][mouse_pos[1]].entity > CITY:
                        mouse_entity = grid[mouse_pos[0]][mouse_pos[1]].entity
                    
                        grid[mouse_pos[0]][mouse_pos[1]].entity = NONE
                        pick_up_pos = mouse_pos
                        valid_locations = Hex_Utils.getValidMoves(pick_up_pos,grid,color,mouse_entity-MAN+1)

                        for location in valid_locations:
                            grid[location[0]][location[1]].selected = True

                elif event.type == MOUSEBUTTONUP and event.button == 1: 

                    mousedown = False

                    if  mouse_entity > NONE:
                        #if grid[mouse_pos[0]][mouse_pos[1]].terrain and grid[mouse_pos[0]][mouse_pos[1]].entity == NONE:
                        if mouse_pos in valid_locations:
                            grid[mouse_pos[0]][mouse_pos[1]].entity = mouse_entity

                            if mouse_pos != pick_up_pos:
                                moves.append(Move(
                                    {'source':color},
                                    GameUpdate([
                                        (pick_up_pos,grid[pick_up_pos[0]][pick_up_pos[1]])
                                        ],{}),
                                    Animation(mouse_entity,pick_up_pos,mouse_pos),
                                    GameUpdate([
                                        (mouse_pos,grid[mouse_pos[0]][mouse_pos[1]])
                                        ],{})
                                ))
                                pass

                        else:
                            grid[pick_up_pos[0]][pick_up_pos[1]].entity = mouse_entity

                    mouse_entity = NONE

                    for location in valid_locations:
                        grid[location[0]][location[1]].selected = False'''

            # logic
            network(moves,grid,state,animations,color)

            # draw
            screen.fill((100, 100, 200))
            screen.fill((150,150,150),pygame.Rect(WINDOWX, 0, 200, WINDOWY))
            screen.blit(font.render('Waiting for server...',True,(0,0,0)),(WINDOWX+15,15))

            drawMapLayer(screen, grid, floor(beat/2)%2==0)
            drawEntities(screen, grid, floor(beat/2)%2==0)
            drawMouseEntity(screen, get_mouse_entity(), pygame.mouse.get_pos())

            for index, animation in enumerate(animations):
                if animation.animation.animate(screen): 
                    animation.postanimation.apply(grid,state)
                    del animations[index]

            pygame.display.flip()
            time.sleep(1/100)

        pygame.quit()

        return 'Game ended', True

    except GameEndingException as err:
        pygame.quit()
        return 'Error: ' + str(err), False