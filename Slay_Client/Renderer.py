from TextureLoader import *
from Constants import *
from Networking import is_our_turn,get_turn
import pygame

roboto = None
roboto_heading = None
debug = None
end_button_rect = None

def reset_renderer(WINDOWX,WINDOWY):
    global roboto, roboto_heading, end_button_rect, debug
    end_button_rect = pygame.Rect((WINDOWX + 33,WINDOWY-50),(134,33)) # This windowX , windowY corresponds to grid area
    if not pygame.font.get_init(): pygame.font.init()
    roboto_heading = pygame.font.Font('./Slay_Assets/RobotoMono-VariableFont_wght.ttf',15)
    roboto_heading.set_bold(True)
    roboto = pygame.font.Font('./Slay_Assets/RobotoMono-VariableFont_wght.ttf',13)
    debug = pygame.font.Font('./Slay_Assets/RobotoMono-VariableFont_wght.ttf',10)

def resize(WINDOWX,WINDOWY):
    global end_button_rect
    end_button_rect = pygame.Rect((WINDOWX + 33 - 200,WINDOWY-50),(134,33)) # This windowX , windowY corresponds to the actual window

# Gives X position to center text ON SIDERBAR
def center(text,font):
    dimensions = font.size(text)
    return (200-dimensions[0])/2

def drawBaseLayer(screen :pygame.Surface,WINDOWX,WINDOWY):
    screen.fill((100, 100, 200))
    screen.fill((150,150,150),pygame.Rect(WINDOWX, 0, 200, WINDOWY))
    return

def drawShopWindow(screen,WINDOWX,gold):

    screen.blit(roboto_heading.render('BUY',True,(0,0,0)),(WINDOWX+center('BUY',roboto_heading),85))
    height = 85

    if gold < 10:
        screen.blit(roboto.render('Cannot Afford Anything',True,(0,0,0)),(WINDOWX+center('Cannot Afford Anything',roboto),110))
        return height + 5


    screen.blit(roboto.render('Cost',True,(0,0,0)),(WINDOWX+85,110))
    screen.blit(roboto.render('Wage',True,(0,0,0)),(WINDOWX+135,110))

    if gold >= 10:
        screen.blit(entities[MAN],(WINDOWX+23,125))
        screen.blit(roboto.render('10',True,(0,0,0)),(WINDOWX+90,140))
        screen.blit(roboto.render('2',True,(0,0,0)),(WINDOWX+140,140))
        height += 40

    if gold >= 15:
        screen.blit(entities[TOWER],(WINDOWX+23,165))
        screen.blit(roboto.render('15',True,(0,0,0)),(WINDOWX+90,180))
        screen.blit(roboto.render('-',True,(0,0,0)),(WINDOWX+140,180))
        height += 40

    if gold >= 20:
        screen.blit(entities[SPEARMAN],(WINDOWX+23,205))
        screen.blit(roboto.render('20',True,(0,0,0)),(WINDOWX+90,220))
        screen.blit(roboto.render('6',True,(0,0,0)),(WINDOWX+140,220))
        height += 40
    
    if gold >= 30:
        screen.blit(entities[BARON],(WINDOWX+23,245))
        screen.blit(roboto.render('30',True,(0,0,0)),(WINDOWX+90,260))
        screen.blit(roboto.render('18',True,(0,0,0)),(WINDOWX+140,260))
        height += 40

    if gold >= 40:
        screen.blit(entities[KNIGHT],(WINDOWX+23,285))
        screen.blit(roboto.render('40',True,(0,0,0)),(WINDOWX+90,300))
        screen.blit(roboto.render('54',True,(0,0,0)),(WINDOWX+140,300))
        height += 40

    return height

def drawReplaySideBar(screen :pygame.Surface,grid,WINDOWX,WINDOWY):

    global end_button_rect

    #Next Turn button
    if end_button_rect.collidepoint(pygame.mouse.get_pos()): screen.blit(buttons[1][1],(WINDOWX + 33,WINDOWY-50))
    else: screen.blit(buttons[1][0],(WINDOWX + 33,WINDOWY-50))

def drawSideBar(screen :pygame.Surface,grid,selected,WINDOWX,WINDOWY,color):

    global end_button_rect

    #Status lines

    screen.blit(roboto_heading.render(f'You are {NAME_MAPPING[color-1]}',True,COLOR_MAPPING[color-1]),(WINDOWX+center(f'You are {NAME_MAPPING[color-1]}',roboto_heading),15))

    if is_our_turn():
        screen.blit(roboto_heading.render('Your turn',True,COLOR_MAPPING[color-1]),(WINDOWX+center('Your turn',roboto_heading),45))
    else:
        turn = get_turn()
        screen.blit(roboto_heading.render(f'{NAME_MAPPING[turn-1]}\'s turn',True,COLOR_MAPPING[turn-1]),(WINDOWX+center(f'{NAME_MAPPING[turn-1]}\'s turn',roboto_heading),45))

    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,75,160,2))

    #End Turn button
    if is_our_turn():
        if end_button_rect.collidepoint(pygame.mouse.get_pos()): screen.blit(buttons[0][1],(WINDOWX + 33,WINDOWY-50))
        else: screen.blit(buttons[0][0],(WINDOWX + 33,WINDOWY-50))
    else:
        screen.blit(buttons[0][2],(WINDOWX + 33,WINDOWY-50))

    #Shop window and finances
    if selected is None:
        screen.blit(roboto_heading.render('No State Selected',True,(0,0,0)),(WINDOWX+center('No State Selected',roboto_heading),90))
        return

    offset = drawShopWindow(screen,WINDOWX,grid[selected[0]][selected[1]].gold)

    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,offset+45,160,2)) 
    screen.blit(roboto_heading.render('Finances',True,(0,0,0)),(WINDOWX+center('Finances',roboto_heading),offset+60))

    screen.blit(roboto.render(f'Current Balance{grid[selected[0]][selected[1]].gold:>4}',True,(0,0,0)),(WINDOWX+25,offset+80))
    screen.blit(roboto.render(f'Wages{("-"+str(grid[selected[0]][selected[1]].wages)):>14}',True,(0,0,0)),(WINDOWX+25,offset+100))
    screen.blit(roboto.render(f'Income{("+"+str(grid[selected[0]][selected[1]].income)):>13}',True,(0,0,0)),(WINDOWX+25,offset+120))
    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,offset+140,160,1))
    screen.blit(roboto.render(f'Next Turn{grid[selected[0]][selected[1]].net:>10}',True,((0,0,0) if grid[selected[0]][selected[1]].net>=0 else (154,46,46))),(WINDOWX+25,offset+155))

    '''screen.blit(roboto.render(f'Current Balance{grid[selected[0]][selected[1]].gold:>4}',True,(0,0,0)),(WINDOWX+25,offset+85))
    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,offset+109,160,1))
    screen.blit(roboto.render(f'Wages{("-"+str(grid[selected[0]][selected[1]].wages)):>14}',True,(0,0,0)),(WINDOWX+25,offset+115))
    screen.blit(roboto.render(f'Income{("+"+str(grid[selected[0]][selected[1]].income)):>13}',True,(0,0,0)),(WINDOWX+25,offset+135))
    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,offset+159,160,1))
    screen.blit(roboto.render(f'Next Turn{grid[selected[0]][selected[1]].net:>10}',True,((0,0,0) if grid[selected[0]][selected[1]].net>=0 else (154,46,46))),(WINDOWX+25,offset+165))'''
    return

def drawMapLayer(screen :pygame.Surface, grid, blink: bool, renderSelections: bool = True):
    for y in range (0,len(grid[0])):
        for x in range(0,len(grid)):
            if (y%2==1):
                screen.blit(cells[grid[x][y].color][(grid[x][y].selected or (blink and grid[x][y].blink)) and renderSelections],((x+0.5)*48,y*36))
                #screen.blit(debug.render(f'{x},{y}',True,(255,255,50)),((x+1)*48-8,y*36))
            else:
                screen.blit(cells[grid[x][y].color][(grid[x][y].selected or (blink and grid[x][y].blink)) and renderSelections],(x*48,y*36))
                #screen.blit(debug.render(f'{x},{y}',True,(255,255,50)),((x+0.5)*48-8,y*36))
    return

def drawEntities(screen :pygame.Surface, grid, beat: int, color: int):
    for y in range (0,len(grid[0])):
        for x in range(0,len(grid)):
            if grid[x][y].entity:
                if (y%2==1):
                    if beat and grid[x][y].playable and grid[x][y].color == color: screen.blit(entities[grid[x][y].entity],((x+0.5)*48,(y*36)+1))
                    else: screen.blit(entities[grid[x][y].entity],((x+0.5)*48,(y*36)-1))
                else:
                    if beat and grid[x][y].playable and grid[x][y].color == color: screen.blit(entities[grid[x][y].entity],(x*48,(y*36)+1))
                    else: screen.blit(entities[grid[x][y].entity],(x*48,(y*36)-1))
    return

def drawMouseEntity(screen :pygame.Surface,entity,pos):
    if entity == 0: return
    screen.blit(entities[entity],(pos[0]-24,pos[1]-24))
    return

def writeLandArray(land,max_len,x,y,screen):
    formattedLines = ['']
    linesize = 0
    for i in land:
        item = str(i)+','
        itemsize = roboto.size(item)[0]
        if linesize+itemsize > max_len:
            formattedLines.append(item)
            linesize=itemsize
        else:
            formattedLines[-1] += item
            linesize+=itemsize

    for idx, line in enumerate(formattedLines):
        screen.blit(roboto.render(line,True,(255,255,255)),(x,y+idx*20))

def drawDebugger(screen :pygame.Surface, grid, debug_pos, WINDOWY, WINDOWX):
    screen.fill((223, 100, 227),pygame.Rect(0,WINDOWY,WINDOWX+200,200)) # magenta bg
    screen.fill((255, 255, 255),pygame.Rect(5,WINDOWY+5,WINDOWX+190,190)) # white box
    screen.fill((223, 100, 227),pygame.Rect(7,WINDOWY+7,WINDOWX+186,186)) # magenta fill
    screen.fill((223, 100, 227),pygame.Rect((WINDOWX+200-50)/2,WINDOWY+5,50,2)) # text bg
    screen.blit(roboto.render('DEBUG',True,(255,255,255)),((WINDOWX+200-40)/2,WINDOWY))

    #Highlight cell
    if debug_pos[1]%2==1:
        screen.blit(debugOverlay,((debug_pos[0]+0.5)*48,debug_pos[1]*36))
    else:
        screen.blit(debugOverlay,(debug_pos[0]*48,debug_pos[1]*36))

    # Writing out the actual info
    screen.blit(roboto.render(f'Position: {debug_pos}',True,(255,255,255)),(50,WINDOWY+20))
    screen.blit(roboto.render(f'Entity: {grid[debug_pos[0]][debug_pos[1]].entity}',True,(255,255,255)),(50,WINDOWY+40))
    screen.blit(roboto.render(f'Landlen: {len(grid[debug_pos[0]][debug_pos[1]].land)}',True,(255,255,255)),(50,WINDOWY+60))
    screen.blit(roboto.render(f'Gold: {(grid[debug_pos[0]][debug_pos[1]].gold if hasattr(grid[debug_pos[0]][debug_pos[1]],"gold") else None)}',True,(255,255,255)),(50,WINDOWY+80))
    screen.blit(roboto.render(f'Land: ',True,(255,255,255)),(50,WINDOWY+100))
    writeLandArray(grid[debug_pos[0]][debug_pos[1]].land,WINDOWX+100,90,WINDOWY+100,screen)
    screen.blit(roboto.render(f'Income: {(grid[debug_pos[0]][debug_pos[1]].income if hasattr(grid[debug_pos[0]][debug_pos[1]],"income") else None)}',True,(255,255,255)),((WINDOWX+250)/2,WINDOWY+20))
    screen.blit(roboto.render(f'Security Level: {grid[debug_pos[0]][debug_pos[1]].security}',True,(255,255,255)),((WINDOWX+250)/2,WINDOWY+40))
    screen.blit(roboto.render(f'Wage: {(grid[debug_pos[0]][debug_pos[1]].wages if hasattr(grid[debug_pos[0]][debug_pos[1]],"wages") else None)}',True,(255,255,255)),((WINDOWX+250)/2,WINDOWY+60))
    screen.blit(roboto.render(f'Net: {(grid[debug_pos[0]][debug_pos[1]].net if hasattr(grid[debug_pos[0]][debug_pos[1]],"net") else None)}',True,(255,255,255)),((WINDOWX+250)/2,WINDOWY+80))
    
