from TextureLoader import *
from math import floor

def drawMapLayer(screen :pygame.Surface, grid, blink: bool):
    for y in range (0,len(grid[0])):
        for x in range(0,len(grid)):
            if (y%2==1):
                screen.blit(cells[grid[x][y].color][grid[x][y].selected or (blink and grid[x][y].blink)],((x+0.5)*48,y*36))
            else:
                screen.blit(cells[grid[x][y].color][grid[x][y].selected or (blink and grid[x][y].blink)],(x*48,y*36))
    return

def drawEntities(screen :pygame.Surface, grid, beat: int):
    for y in range (0,len(grid[0])):
        for x in range(0,len(grid)):
            if grid[x][y].entity:
                if (y%2==1):
                    if beat: screen.blit(entities[grid[x][y].entity],((x+0.5)*48,(y*36)+1))
                    else: screen.blit(entities[grid[x][y].entity],((x+0.5)*48,(y*36)-1))
                else:
                    if beat: screen.blit(entities[grid[x][y].entity],(x*48,(y*36)+1))
                    else: screen.blit(entities[grid[x][y].entity],(x*48,(y*36)-1))
    return

def drawMouseEntity(screen,entity,pos):
    if entity == 0: return
    screen.blit(entities[entity],(pos[0]-24,pos[1]-24))
    return
