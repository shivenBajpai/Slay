import math
import pygame
from Constants import *

xsize, ysize = None, None

class Hex:
    def __init__(self, color) -> None:
        self.blink = False
        self.color = color
        self.terrain = (color > 0)
        self.selected = False
        self.entity = 0
        self.hall_flag = False
        self.land = []
        pass

def cursor_on_grid(old_pos):
    mouse = pygame.mouse.get_pos()
    x1, y1, x2, y2 = None, None, None, None
    # set 1
    if mouse[1]%72<45:
        x1 = math.floor(mouse[0]/48)
        y1 = 2*math.floor(mouse[1]/72)
    # set 2
    if (mouse[1]-36)%72<45:
        x2 = math.floor((mouse[0]-24)/48)
        y2 = 2*math.floor((mouse[1]-36)/72)+1

    if x1 is not None and x2 is not None:
        if (24+48*x1-mouse[0])^2 + (24+72*y1-mouse[1])^2 < (48+48*x2-mouse[0])^2 + (60+72*y2-mouse[1])^2: x,y = x1,y1
        else: x,y =x2,y2
    elif x1 is None: x,y =x2,y2
    else: x,y =x1,y1
    if x>xsize-1 or y>ysize-1 or x<0 or y<0: return old_pos
    return (x,y)

def neighbours(x,y,distance):
    if distance==1:
        if y%2==1:
            return [(x,y+1),(x+1,y+1),(x-1,y),(x+1,y),(x,y-1),(x+1,y-1)]
        else:
            return [(x,y+1),(x-1,y+1),(x-1,y),(x+1,y),(x,y-1),(x-1,y-1)]
    if distance==2:
        if y%2==1:
            return [(x,y+1),(x+1,y+1),(x-1,y),(x+1,y),(x,y-1),(x+1,y-1),(x-1,y+2),(x,y+2),(x+1,y+2),(x-1,y+2),(x+2,y+1),(x-1,y+1),(x-2,y),(x+2,y),(x-1,y-2),(x,y-2),(x+1,y-2),(x-1,y-2),(x+2,y-1),(x-1,y-1)]
        else:
            return [(x,y+1),(x-1,y+1),(x-1,y),(x+1,y),(x,y-1),(x-1,y-1),(x-1,y+2),(x,y+2),(x+1,y+2),(x-1,y+2),(x-2,y+1),(x+1,y+1),(x-2,y),(x+2,y),(x-1,y-2),(x,y-2),(x+1,y-2),(x-1,y-2),(x-2,y-1),(x+1,y-1)]
    if distance==3:
    #TODO: ENTER THE CONSTANTS
        if y%2==1:
            return [(x,y+1),(x+1,y+1),(x-1,y),(x+1,y),(x,y-1),(x+1,y-1),(x-1,y+2),(x,y+2),(x+1,y+2),(x-1,y+2),(x+2,y+1),(x-1,y+1),(x-2,y),(x+2,y),(x-1,y-2),(x,y-2),(x+1,y-2),(x-1,y-2),(x+2,y-1),(x-1,y-1)]
        else:
            return [(x,y+1),(x-1,y+1),(x-1,y),(x+1,y),(x,y-1),(x-1,y-1),(x-1,y+2),(x,y+2),(x+1,y+2),(x-1,y+2),(x-2,y+1),(x+1,y+1),(x-2,y),(x+2,y),(x-1,y-2),(x,y-2),(x+1,y-2),(x-1,y-2),(x-2,y-1),(x+1,y-1)]

def verify(array):
    verified = []
    for cell in array:
        if cell[0] < 0 or cell[1] < 0: continue
        if cell[0] >= xsize or cell[1] >= ysize: continue
        verified.append(cell)
    return verified

#TODO: Remove aggregate functions if not used anywhere

def color_aggregate(x,y,land,grid):
    new = []
    for neighbour in verify(neighbours(x,y,1)):
        if grid[neighbour[0]][neighbour[1]].color == grid[x][y].color and neighbour not in land:
            land.append(neighbour)
            new.append(neighbour)

    for neighbour in new:
        color_aggregate(neighbour[0],neighbour[1],land,grid)

    return

def land_aggregate(x,y,land,grid):

    new = []
    for neighbour in verify(neighbours(x,y,1)):
        if grid[neighbour[0]][neighbour[1]].color != 0 and neighbour not in land:
            land.append(neighbour)
            new.append(neighbour)

    for neighbour in new:
        land_aggregate(neighbour[0],neighbour[1],land,grid)

    return

def getValidMoves(pos,grid,color,level):
    valid = []
    capital = grid[pos[0]][pos[1]].hall_loc
    city_land = grid[capital[0]][capital[1]].land

    for location in verify(neighbours(pos[0],pos[1],2)):

        if not grid[location[0]][location[1]].terrain: continue

        if grid[location[0]][location[1]].color == color: 
            if location in city_land and grid[location[0]][location[1]].entity < TOWER:
                #print('appending location: allied',location[0],location[1])
                valid.append(location)

        else:
            for neighbour in neighbours(location[0],location[1],1):

                #TODO: Security level check

                if neighbour in city_land:
                    valid.append(location)
                    #print('appending foreign:',location,'due to neighbour',neighbour)
                    break

    valid.append(pos)

    return set(valid)