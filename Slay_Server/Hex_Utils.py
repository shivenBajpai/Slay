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

'''def color_aggregate(x,y,land,grid):
    new = []
    for neighbour in verify(neighbours(x,y,1)):
        if grid[neighbour[0]][neighbour[1]].color == grid[x][y].color and neighbour not in land:
            land.append(neighbour)
            new.append(neighbour)

    for neighbour in new:
        color_aggregate(neighbour[0],neighbour[1],land,grid)

    return'''

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

def onShoreLine(x,y,grid):
    for neighbour in verify(neighbours(x,y,1)):
        if not grid[neighbour[0]][neighbour[1]].terrain:
            return True
    return False

def addTrees(grid):
    for y in range (0,YSIZE):
        for x in range(0,XSIZE):
            if grid[x][y].terrain and grid[x][y].entity == 0:
                if random.randint(1,20)<2:
                    if grid[x][y].hall_loc is not None: 
                        grid[grid[x][y].hall_loc[0]][grid[x][y].hall_loc[1]].income -= 1
                        grid[grid[x][y].hall_loc[0]][grid[x][y].hall_loc[1]].net -= 1
                    if onShoreLine(x,y,grid): grid[x][y].entity = PALM
                    if grid[x][y].entity == 0: grid[x][y].entity = TREE

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
                            affected_cells.extend(verify(neighbours(cell[0],cell[1],1)))
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
                        if grid[cell[0]][cell[1]].entity == NONE and grid[cell[0]][cell[1]].terrain and cell not in trees_to_add:
                            trees_to_add.append(cell)
                            affected_cells.append(cell)
                            if grid[cell[0]][cell[1]].hall_loc is not None: 
                                grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].income -= 1
                                grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].net -= 1
                            break

            elif grid[x][y].entity == PALM:
                for cell in verify(neighbours(x,y,1)):
                    if grid[cell[0]][cell[1]].entity == NONE and grid[cell[0]][cell[1]].terrain and onShoreLine(cell[0],cell[1],grid) and cell not in trees_to_add and cell not in palms_to_add:
                        palms_to_add.append(cell)
                        affected_cells.append(cell)
                        if grid[cell[0]][cell[1]].hall_loc is not None: 
                            grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].income -= 1
                            grid[grid[cell[0]][cell[1]].hall_loc[0]][grid[cell[0]][cell[1]].hall_loc[1]].net -= 1
                        break
            
            elif grid[x][y].entity == GRAVE:
                grid[x][y].gravetime -= 1
                affected_cells.append((x,y))
                if grid[x][y].gravetime == 0:
                    if onShoreLine(x,y,grid) and random.randint(1,2) == 1: palms_to_add.append((x,y))
                    else: trees_to_add.append((x,y))
                    affected_cells.append((x,y))
                    if grid[x][y].hall_loc is not None: 
                        grid[grid[x][y].hall_loc[0]][grid[x][y].hall_loc[1]].income -= 1
                        grid[grid[x][y].hall_loc[0]][grid[x][y].hall_loc[1]].net -= 1
                        appendifnotAppended(affected_cells,[grid[x][y].hall_loc])

            else: #Its a unit
                grid[x][y].playable = True
                affected_cells.append((x,y))
    
    for cell in trees_to_add: grid[cell[0]][cell[1]].entity = TREE
    for cell in palms_to_add: grid[cell[0]][cell[1]].entity = PALM
    for cell in graves_to_add: 
        grid[cell[0]][cell[1]].entity = GRAVE
        grid[cell[0]][cell[1]].gravetime = 1
        grid[cell[0]][cell[1]].playable = False

    return affected_cells

def CountCellsofColor(grid,claimed=True):
    
    count = [0]*MAX_COLOR
    for y in range (0,YSIZE):
        for x in range(0,XSIZE):
            if claimed and grid[x][y].hall_loc is None: continue
            if not grid[x][y].terrain: continue
            count[grid[x][y].color-1] += 1

    count = [x for x in enumerate(count)]
    count.sort(reverse=True,key=lambda x:x[1])
    return count

def winCheck(grid,activePlayers):

    hallcount = [0]*MAX_COLOR

    for y in range (0,YSIZE):
        for x in range(0,XSIZE):
            if grid[x][y].entity == CITY: hallcount[grid[x][y].color-1] += 1
    
    for idx, count in enumerate(hallcount):
        if count == 0 and idx+1 in activePlayers:
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
    elif grid[pos[0]][pos[1]].entity > CITY: highest = grid[pos[0]][pos[1]].entity-CITY

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
        grid[0] = [Hex(0)]*YSIZE
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
        deduction = 0
        for y in range (0,YSIZE):
            for x in range(0,XSIZE):

                # this is not a part of terrain
                if not grid[x][y].terrain: 
                    deduction += 1
                    continue

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
                    grid[x][y].gold = 10

                    # add to hall count
                    hall_count[grid[x][y].color-1] += 1

                    # find all cells in this city
                    land = ally_neighbours
                    land.append((x,y))
                    for cell in ally_neighbours:
                        color_aggregate(cell[0],cell[1],land,land,grid)

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
        idealColorCount = (XSIZE*YSIZE-deduction)/MAX_COLOR
        colorCounts = CountCellsofColor(grid,claimed=False)
        if colorCounts[0][1]/idealColorCount > 1.2: continue
        if colorCounts[-1][1]/idealColorCount < 0.8: continue
        break
    
    addTrees(grid)
    print(f'Successfully made grid in {iteration} iterations')
    return grid

# Code below is for AI Player Use
def getValidPlacementSpots(hall_pos,grid,entity):

    valid = []

    if entity != TOWER:
        land = getBorderingLand(hall_pos,grid)
        for loc in land:
            if grid[loc[0]][loc[1]].color == grid[hall_pos[0]][hall_pos[1]].color:
                if grid[loc[0]][loc[1]].entity <= GRAVE or (entity < KNIGHT and entity > CITY and grid[loc[0]][loc[1]].entity == entity): 
                    valid.append(loc)
            elif grid[loc[0]][loc[1]].security < entity-CITY: 
                valid.append(loc)
    else:
        land = grid[hall_pos[0]][hall_pos[1]].land.copy()
        for loc in land:
            if grid[loc[0]][loc[1]].entity <= GRAVE: valid.append(loc)

    return valid

def getBorderingLand(hall_pos,grid):
    land = grid[hall_pos[0]][hall_pos[1]].land.copy()

    for x,y in grid[hall_pos[0]][hall_pos[1]].land:
        tmp = verify(neighbours(x,y,1))
        for cell in verify(neighbours(x,y,1)): 
            if not grid[cell[0]][cell[1]].terrain: tmp.remove(cell)
        appendifnotAppended(land,tmp)

    return land

def getValidMoves(pos,grid,color,entity):
    valid = []
    capital = grid[pos[0]][pos[1]].hall_loc
    city_land = grid[capital[0]][capital[1]].land

    for location in verify(neighbours(pos[0],pos[1],2)):

        if not grid[location[0]][location[1]].terrain: continue

        if grid[location[0]][location[1]].color == color: 
            if location in city_land and (grid[location[0]][location[1]].entity < TOWER or (grid[location[0]][location[1]].entity == entity and entity<KNIGHT)):
                valid.append(location)

        else:
            
            if grid[location[0]][location[1]].security >= entity-CITY: continue
            for neighbour in neighbours(location[0],location[1],1):

                if neighbour in city_land:
                    valid.append(location)
                    break

    valid.append(pos)
    return set(valid)

# Returns list of adjacent cells to captured cell, that are allied and captured under a different city
def GetConnectingTerritories(grid,color,pos,selected_city):
    connecting = []
    for cell in verify(neighbours(pos[0],pos[1],1)):
        if (grid[cell[0]][cell[1]].color != color): continue
        if (cell in grid[selected_city[0]][selected_city[1]].land): continue
        if (grid[cell[0]][cell[1]].hall_loc is not None): connecting.append(cell)
    return connecting

def GetConnectingUnclaimed(grid,color,pos):
    connecting = []
    for cell in verify(neighbours(pos[0],pos[1],1)):
        if (grid[cell[0]][cell[1]].color != color): continue
        if (grid[cell[0]][cell[1]].hall_loc is None): connecting.append(cell)
    return connecting

def convertCity(grid,joining_city,selected_city):
    for cell in grid[joining_city[0]][joining_city[1]].land:
        grid[cell[0]][cell[1]].hall_loc = selected_city

    #print(selected_city,'is joined by',joining_city)
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

def moveHall(grid,old_pos,affected_cells,queued_security_updates):
    land = grid[old_pos[0]][old_pos[1]].land.copy()
    land.remove(old_pos)

    queued_security_updates.append(old_pos)
    appendifnotAppended(affected_cells,verify(neighbours(old_pos[0],old_pos[1],1)))
    appendifnotAppended(affected_cells,land)

    if len(land) < 2: 
        for cell in land:
            grid[cell[0]][cell[1]].hall_loc = None
            if grid[cell[0]][cell[1]].entity > CITY: 
                grid[cell[0]][cell[1]].entity = GRAVE
                grid[cell[0]][cell[1]].gravetime = 1
                SecurityUpdate(grid,cell)
        return None

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

        if len(tmp) == 0: 
            for cell in land:
                grid[cell[0]][cell[1]].hall_loc = None
                if grid[cell[0]][cell[1]].entity > CITY: 
                    grid[cell[0]][cell[1]].entity = GRAVE
                    grid[cell[0]][cell[1]].gravetime = 1
                    SecurityUpdate(grid,cell)
            rng = None
            break

    return rng # rng is the new position of the enemy city

def checkForDivide(hall_pos,grid):
    actual_land = [hall_pos]
    color_aggregate(hall_pos[0],hall_pos[1],actual_land,actual_land,grid)
    if len(actual_land) != len(grid[hall_pos[0]][hall_pos[1]].land): 
        #print('divide caught!')
        return True, actual_land
    #print('no divide')
    return False, actual_land

def createCity(land,grid,affected_cells,queued_security_updates):

    #print(f'createCity logs: \n Called with arguments: {land}')

    if len(land)==1: 
        grid[land[0][0]][land[0][1]].hall_loc = None
        if grid[land[0][0]][land[0][1]].entity > CITY: 
            grid[land[0][0]][land[0][1]].entity = GRAVE
            grid[land[0][0]][land[0][1]].gravetime = 1
            grid[land[0][0]][land[0][1]].playable = False
            SecurityUpdate(grid,land[0])
            affected_cells.extend(land)
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

        if len(tmp) == 0: 
            for cell in land:
                grid[cell[0]][cell[1]].hall_loc = None
                if grid[cell[0]][cell[1]].entity > CITY: 
                    grid[cell[0]][cell[1]].entity = GRAVE
                    grid[cell[0]][cell[1]].gravetime = 1
                    grid[cell[0]][cell[1]].playable = False
                    SecurityUpdate(grid,cell)
            rng = None
            break

    if rng is not None: 
        #print(f' Calling HandleSplits with: rng = {rng}\n its land is {grid[rng[0]][rng[1]].land}')
        HandleSplits(grid,rng,affected_cells,queued_security_updates)
    affected_cells.extend(land)
    return rng

def appendifnotAppended(array,items):
    for item in items:
        if item not in array: array.append(item)
    return

def HandleSplits(grid,original_hall,affected_cells,queued_security_updates):
    isDivide, actual_land = checkForDivide(original_hall,grid)
    if isDivide:
        
        #print(f'Handlesplit logs:\n Called with Arguments {original_hall},{len(affected_cells)},{len(queued_security_updates)}\n This hall has land: {grid[original_hall[0]][original_hall[1]].land}\n Actual land eval to: {actual_land}')

        if affected_cells is not None:
            appendifnotAppended(affected_cells,grid[original_hall[0]][original_hall[1]].land)

        if len(actual_land)>1:
            #print(original_hall,'had more than 1, ',len(actual_land))
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
            #print(original_hall,'had 1, ',len(actual_land))
            split_land = grid[original_hall[0]][original_hall[1]].land.copy()
            split_land.remove(original_hall)
            grid[original_hall[0]][original_hall[1]].land = []
            grid[original_hall[0]][original_hall[1]].income = None
            grid[original_hall[0]][original_hall[1]].wages = None
            grid[original_hall[0]][original_hall[1]].net = None
            grid[original_hall[0]][original_hall[1]].hall_loc = None
            grid[original_hall[0]][original_hall[1]].entity = 0

        new_hall_loc = createCity(split_land,grid,affected_cells,queued_security_updates)
        if new_hall_loc is not None:
            queued_security_updates.append(new_hall_loc)
            appendifnotAppended(affected_cells,verify(neighbours(new_hall_loc[0],new_hall_loc[1],1)))
