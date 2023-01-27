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
        self.hall_flag = False
        self.hall_loc = None
        self.land = []
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
                    grid[x][y].blink = True
                    grid[x][y].hall_loc = (x,y)

                    # add to hall count
                    hall_count[grid[x][y].color-1] += 1

                    # find all cells in this city
                    land = ally_neighbours
                    land.append((x,y))
                    for cell in ally_neighbours:
                        color_aggregate(cell[0],cell[1],land,grid)

                    # configure said cells
                    grid[x][y].land = land
                    for ally in land:
                        grid[ally[0]][ally[1]].hall_flag = True
                        grid[ally[0]][ally[1]].hall_loc = (x,y)
                    
        grid[2][2].entity = SPEARMAN            

        if max(hall_count) - min(hall_count) > 1: continue
        if min(hall_count) == 0: continue
        break
    
    print(f'Successfully made grid in {iteration} iterations')
    return grid