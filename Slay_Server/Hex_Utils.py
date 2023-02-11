import math
import random
from Constants import *

class Hex:
    def __init__(self, color) -> None:
        self.blink = False
        self.color = color
        self.terrain = (color > 0)
        self.selected = False
        self.entity = 0
        self.security = 0
        self.security_providers = []
        self.hall_flag = False
        self.hall_loc = None
        self.land = []
        self.playable = False
        pass

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

def verify(array):
    verified = []
    for cell in array:
        if cell[0] < 0 or cell[1] < 0: continue
        if cell[0] >= XSIZE or cell[1] >= YSIZE: continue
        verified.append(cell)
    return verified

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

def onShoreLine(x,y,grid):
    for neighbour in verify(neighbours(x,y,1)):
        if not grid[neighbour[0]][neighbour[1]].terrain:
            return True
    return False

def addTrees(grid):
    for y in range (0,YSIZE):
        for x in range(0,XSIZE):
            if grid[x][y].terrain and grid[x][y].entity == 0:
                if random.randint(1,10)<2:
                    if grid[x][y].hall_loc is not None: 
                        grid[grid[x][y].hall_loc[0]][grid[x][y].hall_loc[1]].income -= 1
                        grid[grid[x][y].hall_loc[0]][grid[x][y].hall_loc[1]].net -= 1
                    if onShoreLine(x,y,grid): grid[x][y].entity = PALM
                    if grid[x][y].entity == 0: grid[x][y].entity = TREE

def appendifnotAppended(array,items):
    for item in items:
        if item not in array: array.append(item)
    return

def roundupdate(grid):

    affected_cells = []
    trees_to_add = []
    palms_to_add = []
    graves_to_add = []

    for y in range (0,YSIZE):
        for x in range(0,XSIZE):
            if grid[x][y].entity == CITY:
                affected_cells.append((x,y))

                if grid[x][y].net < 0:
                    for cell in grid[x][y].land:
                        if grid[cell[0]][cell[1]].entity > CITY:
                            grid[x][y].wages -= math.floor(2*(3**(grid[cell[0]][cell[1]].entity-MAN)))
                            grid[cell[0]][cell[1]].entity = NONE
                            SecurityUpdate(grid,cell)
                            affected_cells.append(cell)
                            graves_to_add.append(cell)

                    grid[x][y].gold = 0
                    grid[x][y].net = grid[x][y].income - grid[x][y].wages
                else:
                    grid[x][y].gold = grid[x][y].net
                    grid[x][y].net = grid[x][y].gold + grid[x][y].income - grid[x][y].wages

    for y in range (0,YSIZE):
        for x in range(0,XSIZE):
    
            if not grid[x][y].terrain: continue
            if grid[x][y].entity in (NONE,TOWER,CITY): continue

            elif grid[x][y].entity == TREE:
                if random.randint(1,2) == 1:
                    for cell in verify(neighbours(x,y,1)):
                        if grid[cell[0]][cell[1]].entity == NONE and grid[cell[0]][cell[1]].terrain:
                            trees_to_add.append(cell)
                            affected_cells.append(cell)
                            if grid[cell[0]][cell[1]].hall_loc is not None: 
                                grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].income -= 1
                                grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].net -= 1
                            break

            elif grid[x][y].entity == PALM:
                for cell in verify(neighbours(x,y,1)):
                    if grid[cell[0]][cell[1]].entity == NONE and grid[cell[0]][cell[1]].terrain and onShoreLine(cell[0],cell[1],grid):
                        palms_to_add.append(cell)
                        affected_cells.append(cell)
                        if grid[cell[0]][cell[1]].hall_loc is not None: 
                            grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].income -= 1
                            grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].net -= 1
                        break
            
            elif grid[x][y].entity == GRAVE:
                grid[x][y].gravetime -= 1
                if grid[x][y].gravetime == 0:
                    if onShoreLine(x,y,grid) and random.randint(1,2) == 1: palms_to_add.append((x,y))
                    else: trees_to_add.append((x,y))
                    affected_cells.append((x,y))
                    if grid[x][y].hall_loc is not None: 
                        grid[grid[x][y].hall_loc[0]][grid[x][y].hall_loc[1]].income -= 1
                        appendifnotAppended(affected_cells,[grid[x][y].hall_loc])

            else: #Its a unit
                print('set',x,y,'to playable')
                grid[x][y].playable = True
                affected_cells.append((x,y))
    
    for cell in trees_to_add: grid[cell[0]][cell[1]].entity = TREE
    for cell in palms_to_add: grid[cell[0]][cell[1]].entity = PALM
    for cell in graves_to_add: 
        grid[cell[0]][cell[1]].entity = GRAVE
        grid[cell[0]][cell[1]].gravetime = 1
        grid[cell[0]][cell[1]].playable = False

    return affected_cells

def winCheck(grid,activePlayers):

    hallcount = [0]*MAX_COLOR

    for y in range (0,YSIZE):
        for x in range(0,XSIZE):
            if grid[x][y].entity == CITY: hallcount[grid[x][y].color-1] += 1
    
    for idx, count in enumerate(hallcount):
        if count == 0:
            activePlayers.remove(idx+1)
    
    if len(activePlayers)==1:
        return True
    return False

def SecurityUpdate(grid,position):
    
    SecurityCalculate(grid,position)

    for cell in verify(neighbours(position[0],position[1],1)):
        if grid[cell[0]][cell[1]].terrain: SecurityCalculate(grid,cell)
        
    return

def SecurityCalculate(grid,pos):
    highest = 0
    color = grid[pos[0]][pos[1]].color
    grid[pos[0]][pos[1]].security_providers = []
    if grid[pos[0]][pos[1]].hall_loc is None: 
        grid[pos[0]][pos[1]].security = 0
        return
    if grid[pos[0]][pos[1]].entity == TOWER: highest = TOWER_SECURITY
    elif grid[pos[0]][pos[1]].entity == CITY: highest = CITY_SECURITY
    elif grid[pos[0]][pos[1]].entity > CITY: grid[pos[0]][pos[1]].entity-CITY

    for cell in verify(neighbours(pos[0],pos[1],1)):
        if grid[cell[0]][cell[1]].terrain and grid[cell[0]][cell[1]].color == color and grid[cell[0]][cell[1]].entity > GRAVE:
            if grid[cell[0]][cell[1]].entity == TOWER and highest <= TOWER_SECURITY:
                if highest != TOWER_SECURITY:
                    grid[pos[0]][pos[1]].security_providers = [cell]
                else:
                    grid[pos[0]][pos[1]].security_providers.append(cell)
                highest = TOWER_SECURITY

            elif grid[cell[0]][cell[1]].entity == CITY and highest <= CITY_SECURITY: 
                if highest != CITY_SECURITY:
                    grid[pos[0]][pos[1]].security_providers = [cell]
                else:
                    grid[pos[0]][pos[1]].security_providers.append(cell)
                highest = CITY_SECURITY

            elif highest <= grid[cell[0]][cell[1]].entity-CITY:
                if highest != grid[cell[0]][cell[1]].entity-CITY:
                    grid[pos[0]][pos[1]].security_providers = [cell]
                else:
                    grid[pos[0]][pos[1]].security_providers.append(cell)
                highest = grid[cell[0]][cell[1]].entity-CITY

    grid[pos[0]][pos[1]].security = highest
    grid[pos[0]][pos[1]].security = highest
    return

def createGrid():

    grid = []
    iteration = 0

    while True:
        iteration += 1
        grid = []
        for x in range(0,XSIZE):
            grid.append([])
            for y in range(0,YSIZE):
                if random.randint(1,10) < 4:   
                    grid[x].append(Hex(0))
                else:
                    grid[x].append(Hex(random.randint(1,MAX_COLOR)))

        #padding
        grid[0] = [Hex(0)]*XSIZE
        for col in grid:
            col[0] = Hex(0)

        #unsuitable case
        if grid[1][1].color == 0: continue

        #mark mainland
        mainland = [(1,1)]
        land_aggregate(1,1,mainland,grid)

        # land connected to 1,1 itself is an island, unsuitable case
        if len(mainland) < math.floor((XSIZE-1)*(YSIZE-1)*0.5): continue
        
        for y in range(0,YSIZE):
            for x in range(0,XSIZE):
                if grid[x][y] == 0: continue
                if (x,y) not in mainland:
                    grid[x][y] = Hex(0)

        #validity checks & create halls
        hall_count = [0]*(MAX_COLOR)
        for y in range (0,YSIZE):
            for x in range(0,XSIZE):

                # this is not a part of terrain
                if not grid[x][y].color: continue

                # already handled, move on
                if grid[x][y].hall_flag: continue

                # is this a valid spot
                ally_neighbours = []
                for neighbour in verify(neighbours(x,y,1)):
                    if grid[neighbour[0]][neighbour[1]].color == grid[x][y].color: ally_neighbours.append(neighbour)

                # If so, make this the city centre
                if len(ally_neighbours) > 1:
                    grid[x][y].hall_flag = True
                    grid[x][y].entity = CITY
                    grid[x][y].hall_loc = (x,y)
                    grid[x][y].gold = 50

                    # add to hall count
                    hall_count[grid[x][y].color-1] += 1

                    # find all cells in this city
                    land = ally_neighbours
                    land.append((x,y))
                    for cell in ally_neighbours:
                        color_aggregate(cell[0],cell[1],land,grid)

                    # configure said cells
                    grid[x][y].land = land
                    grid[x][y].income = len(land)
                    grid[x][y].wages = 0
                    grid[x][y].net = grid[x][y].gold + grid[x][y].income 
                    for ally in land:
                        grid[ally[0]][ally[1]].hall_flag = True
                        grid[ally[0]][ally[1]].hall_loc = (x,y)

                    #security setup
                    SecurityUpdate(grid,(x,y))

        if max(hall_count) - min(hall_count) > 1: continue
        if min(hall_count) == 0: continue
        break
    
    addTrees(grid)
    print(f'Successfully made grid in {iteration} iterations')
    return grid