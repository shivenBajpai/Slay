import math
import pygame
from Constants import *
import random

xsize, ysize = None, None

class Hex:
    def __init__(self, color) -> None:
        self.blink = False
        self.color = color
        self.terrain = (color > 0)
        self.selected = False
        self.entity = 0
        self.hall_flag = False
        self.hall_loc = None
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
    if x>xsize-1 or y>ysize-1 or x<0 or y<0: return old_pos, False
    return (x,y), True

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

def color_aggregate(x,y,land,new,grid):
    new_this_call = []
    for neighbour in verify(neighbours(x,y,1)):
        if grid[neighbour[0]][neighbour[1]].color == grid[x][y].color and neighbour not in land and neighbour not in new:
            new.append(neighbour)
            new_this_call.append(neighbour)

    for neighbour in new_this_call:
        color_aggregate(neighbour[0],neighbour[1],land,new,grid)

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
            if location in city_land and grid[location[0]][location[1]].entity < TOWER or (grid[location[0]][location[1]].entity == level and level<KNIGHT):
                valid.append(location)

        else:
            for neighbour in neighbours(location[0],location[1],1):

                #TODO: Security level check

                if neighbour in city_land:
                    valid.append(location)
                    break

    valid.append(pos)

    return set(valid)

def getValidPlacementSpots(hall_pos,grid,level):
    valid = grid[hall_pos[0]][hall_pos[1]].land.copy()
    for loc in valid:
        if grid[loc[0]][loc[1]].entity > GRAVE:
            if level < KNIGHT and grid[loc[0]][loc[1]].entity == level: continue
            valid.remove(loc)

    # TODO: add valid bordering enemy positions
    return valid

def GetConnectingTerritories(mouse_pos,grid,color,selected_city):
    connecting = []
    for cell in verify(neighbours(mouse_pos[0],mouse_pos[1],1)):
        if (grid[cell[0]][cell[1]].color != color): continue
        if (cell in grid[selected_city[0]][selected_city[1]].land): continue
        if (grid[cell[0]][cell[1]].hall_loc is not None): connecting.append(cell)
    return connecting

def convertCity(grid,joining_city,selected_city):
    for cell in grid[joining_city[0]][joining_city[1]].land:
        grid[cell[0]][cell[1]].hall_loc = selected_city

    print(selected_city,'is joined by',joining_city)
    grid[selected_city[0]][selected_city[1]].wages += grid[joining_city[0]][joining_city[1]].wages
    grid[selected_city[0]][selected_city[1]].income += grid[joining_city[0]][joining_city[1]].income
    grid[selected_city[0]][selected_city[1]].net += grid[joining_city[0]][joining_city[1]].net
    grid[selected_city[0]][selected_city[1]].gold += grid[joining_city[0]][joining_city[1]].gold
    grid[selected_city[0]][selected_city[1]].land += grid[joining_city[0]][joining_city[1]].land

    grid[joining_city[0]][joining_city[1]].wages = None
    grid[joining_city[0]][joining_city[1]].income = None
    grid[joining_city[0]][joining_city[1]].net = None
    grid[joining_city[0]][joining_city[1]].gold = None
    grid[joining_city[0]][joining_city[1]].land = []
    grid[joining_city[0]][joining_city[1]].entity = 0

def moveHall(grid,old_pos):
    land = grid[old_pos[0]][old_pos[1]].land.copy()
    land.remove(old_pos)

    if len(land) < 3: 
        for cell in land:
            grid[cell[0]][cell[1]].hall_loc = None
            #TODO: kill units
        return land, None

    tmp = land.copy()
    rng = None

    while True:
        rng = tmp[random.randint(0,len(tmp)-1)]
        if grid[rng[0]][rng[1]].entity < TOWER:
            grid[rng[0]][rng[1]].entity = CITY
            grid[rng[0]][rng[1]].land = land
            grid[rng[0]][rng[1]].wages = grid[old_pos[0]][old_pos[1]].wages
            grid[rng[0]][rng[1]].income = grid[old_pos[0]][old_pos[1]].income - 1
            grid[rng[0]][rng[1]].net = grid[old_pos[0]][old_pos[1]].net - 1 - grid[old_pos[0]][old_pos[1]].gold
            grid[rng[0]][rng[1]].gold = 0
            
            for cell in land:
                grid[cell[0]][cell[1]].hall_loc = rng
            break
        else: tmp.remove(rng)

        if len(tmp) < 3: 
            for cell in land:
                grid[cell[0]][cell[1]].hall_loc = None
                #TODO: kill units
            break

    return land, rng

def checkForDivide(hall_pos,grid):
    actual_land = [hall_pos]
    color_aggregate(hall_pos[0],hall_pos[1],actual_land,actual_land,grid)
    if len(actual_land) != len(grid[hall_pos[0]][hall_pos[1]].land): 
        print('divide caught!')
        return True, actual_land
    print('no divide')
    return False, actual_land

def createCity(land,grid):
    if len(land)==1: 
        grid[land[0][0]][land[0][1]].hall_loc = None
        #TODO: Kill the unit if exists
        return

    tmp = land.copy()
    rng = None

    while True:
        rng = tmp[random.randint(0,len(tmp)-1)]
        if grid[rng[0]][rng[1]].entity < TOWER:
            grid[rng[0]][rng[1]].entity = CITY
            grid[rng[0]][rng[1]].land = land
            grid[rng[0]][rng[1]].wages = 0
            grid[rng[0]][rng[1]].income = 0
            grid[rng[0]][rng[1]].gold = 0
            
            for cell in land:
                grid[cell[0]][cell[1]].hall_loc = rng
                if grid[cell[0]][cell[1]].entity not in (2,3):
                    grid[rng[0]][rng[1]].income += 1
                    if grid[cell[0]][cell[1]].entity > CITY: grid[rng[0]][rng[1]].wages += math.floor(2*(3**(grid[cell[0]][cell[1]].entity- MAN)))

            grid[rng[0]][rng[1]].net = grid[rng[0]][rng[1]].income - grid[rng[0]][rng[1]].wages
            break

        else: tmp.remove(rng)

        if len(tmp) < 2: 
            for cell in land:
                grid[cell[0]][cell[1]].hall_loc = None
                #TODO: kill units
            break

    HandleSplits(grid,rng,None)
    return

def appendLandifnotAppended(affected_cells,land):
    for cell in land:
        if cell not in affected_cells: affected_cells.append(cell)
    return

def HandleSplits(grid,original_hall,affected_cells):
    isDivide, actual_land = checkForDivide(original_hall,grid)
    if isDivide:
        
        if affected_cells is not None:
            appendLandifnotAppended(affected_cells,grid[original_hall[0]][original_hall[1]].land)

        if len(actual_land)>1:
            print(original_hall,'had more than 1, ',len(actual_land))
            split_land = grid[original_hall[0]][original_hall[1]].land.copy()
            grid[original_hall[0]][original_hall[1]].land = actual_land
            grid[original_hall[0]][original_hall[1]].income = 0
            grid[original_hall[0]][original_hall[1]].wages = 0

            for land in actual_land:
                split_land.remove(land)
                if grid[land[0]][land[1]].entity not in (2,3):
                    grid[original_hall[0]][original_hall[1]].income += 1
                    if grid[land[0]][land[1]].entity > CITY: grid[original_hall[0]][original_hall[1]].wages += math.floor(2*(3**(grid[land[0]][land[1]].entity- MAN)))

            grid[original_hall[0]][original_hall[1]].net = grid[original_hall[0]][original_hall[1]].gold + grid[original_hall[0]][original_hall[1]].income - grid[original_hall[0]][original_hall[1]].wages
        else:
            print(original_hall,'had 1, ',len(actual_land))
            split_land = grid[original_hall[0]][original_hall[1]].land.copy()
            split_land.remove(original_hall)
            grid[original_hall[0]][original_hall[1]].land = []
            grid[original_hall[0]][original_hall[1]].income = None
            grid[original_hall[0]][original_hall[1]].wages = None
            grid[original_hall[0]][original_hall[1]].net = None
            grid[original_hall[0]][original_hall[1]].hall_loc = None
            grid[original_hall[0]][original_hall[1]].entity = 0

        createCity(split_land,grid)
    
    return