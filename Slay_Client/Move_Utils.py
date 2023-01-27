from TextureLoader import entities
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from Constants import CITY,MAN,NONE
from Hex_Utils import cursor_on_grid,getValidMoves
from Networking import declareExit,is_our_turn
import math

mouse_pos = (0,0) #The cell mouse was last on top of
mousedown = False
mouse_entity = 0
valid_locations = ()
pick_up_pos = None

def reset_move_utils():
    global mouse_pos
    global mousedown
    global mouse_entity
    global valid_locations
    global pick_up_pos
    mouse_pos = (0,0)
    mousedown = False
    mouse_entity = 0
    valid_locations = ()
    pick_up_pos = None

def get_mouse_entity():
    return mouse_entity

def getpoints(a,b,n):

    xdiff = (b[0]-a[0])/(n+1)
    ydiff = (b[1]-a[1])/(n+1)
    points = []
    for i in range(1,n+1):
        points.append((
            math.floor(a[0]+i*xdiff),
            math.floor(a[1]+i*ydiff)
        ))
    return points

def handleEvent(event,grid,moves,color):

    global mouse_pos
    global mousedown
    global valid_locations
    global pick_up_pos
    global mouse_entity

    if event.type == QUIT: declareExit()

    elif event.type == MOUSEMOTION: mouse_pos = cursor_on_grid(mouse_pos)

    elif event.type == MOUSEBUTTONDOWN and event.button == 1:

        mousedown = True

        if is_our_turn() and grid[mouse_pos[0]][mouse_pos[1]].entity > CITY:
            mouse_entity = grid[mouse_pos[0]][mouse_pos[1]].entity
        
            grid[mouse_pos[0]][mouse_pos[1]].entity = NONE
            pick_up_pos = mouse_pos
            valid_locations = getValidMoves(pick_up_pos,grid,color,mouse_entity-MAN+1)

            for location in valid_locations:
                grid[location[0]][location[1]].selected = True

    elif event.type == MOUSEBUTTONUP and event.button == 1: 

        mousedown = False

        if  mouse_entity > NONE:
            if mouse_pos in valid_locations:
                grid[mouse_pos[0]][mouse_pos[1]].entity = mouse_entity

                if mouse_pos != pick_up_pos:
                    
                    move = Move({'source':color},
                            GameUpdate([(pick_up_pos, grid[pick_up_pos[0]][pick_up_pos[1]])], {}),
                            Animation(mouse_entity,pick_up_pos,mouse_pos),
                            GameUpdate([(mouse_pos, grid[mouse_pos[0]][mouse_pos[1]])], {})
                            )
                    moves.append(move)

            else:
                grid[pick_up_pos[0]][pick_up_pos[1]].entity = mouse_entity

        mouse_entity = NONE

        for location in valid_locations: grid[location[0]][location[1]].selected = False
    return

class Animation:
    def __init__(self,entity: int,startpos: tuple,endpos: tuple) -> None:
        self.entity = entity
        self.startpos = startpos
        self.endpos = endpos
        
    def prepare(self) -> None:

        if (self.startpos[1]%2==1):
            start = ((self.startpos[0]+0.5)*48,self.startpos[1]*36)
        else:
            start = (self.startpos[0]*48,self.startpos[1]*36)

        if (self.endpos[1]%2==1):
            end = ((self.endpos[0]+0.5)*48,self.endpos[1]*36)
        else:
            end = (self.endpos[0]*48,self.endpos[1]*36)

        self.frame = 0
        self.frames = getpoints(start,end,25)

    def animate(self,screen) -> bool:

        screen.blit(entities[self.entity],(self.frames[self.frame]))

        self.frame += 1
        if self.frame == len(self.frames): return True
        return False

class GameUpdate:
    def __init__(self,gridChanges: list[tuple],stateChanges: dict) -> None:
        self.gridChanges = gridChanges
        self.stateChanges = stateChanges

    def apply(self,grid,state) -> None:
        for pos, newState in self.gridChanges:
            grid[pos[0]][pos[1]] = newState

        state.update(self.stateChanges)

class Move: # just a data struct
    def __init__(self,meta,preanim: GameUpdate,anim: Animation,postanim: GameUpdate) -> None:
        self.metadata = meta
        self.preanimation = preanim
        self.animation = anim
        self.postanimation = postanim

    '''
    Metadata struct:
    source: <>

    '''
