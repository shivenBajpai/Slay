from TextureLoader import entities
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import Rect, mouse
from Constants import *
from Hex_Utils import cursor_on_grid,getValidMoves,getValidPlacementSpots,GetConnectingTerritories,color_aggregate,convertCity,moveHall,HandleSplits
from Networking import declareExit,is_our_turn
import math
import copy

mouse_pos = (0,0) #The cell mouse was last on top of
mousedown = False
mouse_entity = 0
valid_locations = None
pick_up_pos = None
mouse_on_grid = False
shop_button_rects = []
end_button_rect = None
selected_city = None

def reset_move_utils(WINDOWX,WINDOWY):
    global mouse_pos, mousedown, mouse_entity, valid_locations, pick_up_pos, shop_button_rects, selected_city, mouse_on_grid, end_button_rect
    mouse_pos = (0,0)
    mousedown = False
    mouse_on_grid = False
    mouse_entity = 0
    valid_locations = None
    pick_up_pos = None
    selected_city = None
    shop_button_rects = (
        (Rect((WINDOWX+23,95),(48,48)),10),
        (Rect((WINDOWX+23,135),(48,48)),20),
        (Rect((WINDOWX+23,175),(48,48)),30),
        (Rect((WINDOWX+23,215),(48,48)),40)
    ) # Bounding Box and Cost pairs
    end_button_rect = Rect((WINDOWX + 33,WINDOWY-50),(134,33))

def get_mouse_entity():
    return mouse_entity

def get_selected_city():
    return selected_city

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

    global mouse_pos, mousedown, mouse_entity, valid_locations, pick_up_pos, selected_city, mouse_on_grid

    if event.type == QUIT: declareExit()

    elif event.type == MOUSEMOTION: mouse_pos, mouse_on_grid = cursor_on_grid(mouse_pos)

    elif event.type == MOUSEBUTTONDOWN and event.button == 1:

        mousedown = True

        if selected_city is not None:
            for cell in grid[selected_city[0]][selected_city[1]].land:
                    grid[cell[0]][cell[1]].selected = False

        if mouse_on_grid:

            if grid[mouse_pos[0]][mouse_pos[1]].color == color:
                selected_city = grid[mouse_pos[0]][mouse_pos[1]].hall_loc

            else:
                selected_city = None

            if is_our_turn() and grid[mouse_pos[0]][mouse_pos[1]].entity > CITY and grid[mouse_pos[0]][mouse_pos[1]].color == color:
                mouse_entity = grid[mouse_pos[0]][mouse_pos[1]].entity
            
                grid[mouse_pos[0]][mouse_pos[1]].entity = NONE
                pick_up_pos = mouse_pos
                valid_locations = getValidMoves(pick_up_pos,grid,color,mouse_entity)

                for location in valid_locations:
                    grid[location[0]][location[1]].selected = True

        elif is_our_turn() and end_button_rect.collidepoint(mouse.get_pos()):
            moves.append('end')

        elif is_our_turn() and selected_city != None:
            for idx, rect in enumerate(shop_button_rects):
                if rect[0].collidepoint(mouse.get_pos()) and grid[selected_city[0]][selected_city[1]].gold >= rect[1]:
                    pick_up_pos = None
                    mouse_entity = MAN + idx
                    valid_locations = getValidPlacementSpots(selected_city,grid,mouse_entity)

                    for location in valid_locations:
                        grid[location[0]][location[1]].selected = True

                    break
        
        if valid_locations is None and selected_city is not None:
            for cell in grid[selected_city[0]][selected_city[1]].land:
                grid[cell[0]][cell[1]].selected = True

    elif event.type == MOUSEBUTTONUP and event.button == 1: 

        mousedown = False

        if  mouse_entity > NONE:
            if mouse_pos in valid_locations and mouse_on_grid:
                
                affected_cells = []
                affected_enemy_hall = None

                # doubling up
                if grid[mouse_pos[0]][mouse_pos[1]].entity == mouse_entity and grid[mouse_pos[0]][mouse_pos[1]].color == color: 
                    affected_cells.append(selected_city)
                    wage_change = math.floor(2*(3**(mouse_entity-MAN+1))-2*(3**(mouse_entity-MAN)))
                    grid[selected_city[0]][selected_city[1]].wages += wage_change
                    grid[selected_city[0]][selected_city[1]].net -= wage_change

                    grid[mouse_pos[0]][mouse_pos[1]].entity = mouse_entity + 1
                else: 

                    # land capturing
                    if grid[mouse_pos[0]][mouse_pos[1]].color != color:
                        grid[mouse_pos[0]][mouse_pos[1]].color = color

                        affected_cells.append(selected_city)
                        print(selected_city)
                        grid[selected_city[0]][selected_city[1]].income += 1
                        grid[selected_city[0]][selected_city[1]].net += 1
                        grid[selected_city[0]][selected_city[1]].land.append(mouse_pos)

                        # land belongs to enemy, update enemy centre
                        if grid[mouse_pos[0]][mouse_pos[1]].hall_loc is not None:

                            if grid[mouse_pos[0]][mouse_pos[1]].entity == CITY:
                                # Captured enemy centre, move it
                                enemy_land, affected_enemy_hall = moveHall(grid,mouse_pos)
                                affected_cells.extend(enemy_land)
                            else:
                                # captured random enemy land
                                affected_cells.append(grid[mouse_pos[0]][mouse_pos[1]].hall_loc)
                                affected_enemy_hall = affected_cells[-1]
                                grid[affected_cells[-1][0]][affected_cells[-1][1]].income -= 1
                                wage_change = math.floor(2*3**(grid[mouse_pos[0]][mouse_pos[1]].entity-MAN))
                                grid[affected_cells[-1][0]][affected_cells[-1][1]].wages -= wage_change
                                grid[affected_cells[-1][0]][affected_cells[-1][1]].net += wage_change - 1
                                grid[affected_cells[-1][0]][affected_cells[-1][1]].land.remove(mouse_pos)

                        # check if this connects to even more land
                        connections = GetConnectingTerritories(mouse_pos,grid,color,selected_city)

                        for connection in connections:
                            #This connecting bit of land belongs to a city, join these two cities.

                            if grid[connection[0]][connection[1]].hall_loc == selected_city: continue
                            joining_city = grid[connection[0]][connection[1]].hall_loc
                            affected_cells.extend(grid[joining_city[0]][joining_city[1]].land)
                            convertCity(grid,joining_city,selected_city)
    
                        #Now any connecting bit of land does not belong to city, therefore any indirectly connecting bits also dont beling to a city. Find them and add
                        new_land = []
                        color_aggregate(mouse_pos[0],mouse_pos[1],grid[selected_city[0]][selected_city[1]].land,new_land,grid)
                        for cell in new_land:
                            affected_cells.append(cell)
                            grid[cell[0]][cell[1]].hall_loc = selected_city
                            grid[selected_city[0]][selected_city[1]].land.append(cell)
                            if grid[cell[0]][cell[1]] != TREE and grid[cell[0]][cell[1]] != PALM:
                                grid[selected_city[0]][selected_city[1]].income += 1
                                grid[selected_city[0]][selected_city[1]].net += 1

                    # new unit
                    if pick_up_pos is None:
                        if selected_city not in affected_cells: affected_cells.append(selected_city)
                        wage_change = math.floor(2*(3**(mouse_entity-MAN)))
                        grid[selected_city[0]][selected_city[1]].wages += wage_change
                        grid[selected_city[0]][selected_city[1]].net -= wage_change

                    grid[mouse_pos[0]][mouse_pos[1]].hall_loc = selected_city
                    grid[mouse_pos[0]][mouse_pos[1]].entity = mouse_entity

                    # check if we split a enemy city in two
                    if affected_enemy_hall is not None:
                        HandleSplits(grid,affected_enemy_hall,affected_cells)

                for location in valid_locations: grid[location[0]][location[1]].selected = False
                valid_locations = None

                if pick_up_pos is not None:
                    if mouse_pos != pick_up_pos:

                        move = Move({'source':color},
                                GameUpdate([(pick_up_pos, copy.deepcopy(grid[pick_up_pos[0]][pick_up_pos[1]]) )], {}),
                                Animation(mouse_entity,pick_up_pos,mouse_pos),
                                GameUpdate([(mouse_pos, copy.deepcopy(grid[mouse_pos[0]][mouse_pos[1]]) )], {})
                                )
                        for centre in affected_cells: move.postanimation.gridChanges.append((centre,copy.deepcopy(grid[centre[0]][centre[1]])))
                        moves.append(move)

                else:

                    move = Move({'source':color},
                            GameUpdate([(mouse_pos, copy.deepcopy(grid[mouse_pos[0]][mouse_pos[1]]) )], {}),
                            None,
                            GameUpdate([], {})
                            )
                    for centre in affected_cells: move.preanimation.gridChanges.append((centre,copy.deepcopy(grid[centre[0]][centre[1]])))
                    moves.append(move)

            elif pick_up_pos is not None:
                grid[pick_up_pos[0]][pick_up_pos[1]].entity = mouse_entity

            for cell in grid[selected_city[0]][selected_city[1]].land:
                grid[cell[0]][cell[1]].selected = True

        mouse_entity = NONE
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
        self.frames = getpoints(start,end,15)

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
