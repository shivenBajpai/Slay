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
    end_button_rect = pygame.Rect((WINDOWX + 33,WINDOWY-50),(134,33))
    if not pygame.font.get_init(): pygame.font.init()
    roboto_heading = pygame.font.Font('./Slay_Assets/RobotoMono-VariableFont_wght.ttf',15)
    roboto_heading.set_bold(True)
    roboto = pygame.font.Font('./Slay_Assets/RobotoMono-VariableFont_wght.ttf',13)
    debug = pygame.font.Font('./Slay_Assets/RobotoMono-VariableFont_wght.ttf',10)

def center(text,font):
    dimensions = font.size(text)
    return (200-dimensions[0])/2

def drawBaseLayer(screen :pygame.Surface,WINDOWX,WINDOWY):
    screen.fill((100, 100, 200))
    screen.fill((150,150,150),pygame.Rect(WINDOWX, 0, 200, WINDOWY))
    return

def drawShopWindow(screen,WINDOWX,gold):

    screen.blit(roboto_heading.render('BUY',True,(0,0,0)),(WINDOWX+center('BUY',roboto_heading),55))
    height = 55

    if gold < 10:
        screen.blit(roboto.render('Cannot Afford Anything',True,(0,0,0)),(WINDOWX+center('Cannot Afford Anything',roboto),80))
        return height + 5


    screen.blit(roboto.render('Cost',True,(0,0,0)),(WINDOWX+85,80))
    screen.blit(roboto.render('Wage',True,(0,0,0)),(WINDOWX+135,80))

    if gold >= 10:
        screen.blit(entities[MAN],(WINDOWX+23,95))
        screen.blit(roboto.render('10',True,(0,0,0)),(WINDOWX+90,110))
        screen.blit(roboto.render('2',True,(0,0,0)),(WINDOWX+140,110))
        height += 40

    if gold >= 15:
        screen.blit(entities[TOWER],(WINDOWX+23,135))
        screen.blit(roboto.render('15',True,(0,0,0)),(WINDOWX+90,150))
        screen.blit(roboto.render('-',True,(0,0,0)),(WINDOWX+140,150))
        height += 40

    if gold >= 20:
        screen.blit(entities[SPEARMAN],(WINDOWX+23,175))
        screen.blit(roboto.render('20',True,(0,0,0)),(WINDOWX+90,190))
        screen.blit(roboto.render('6',True,(0,0,0)),(WINDOWX+140,190))
        height += 40
    
    if gold >= 30:
        screen.blit(entities[BARON],(WINDOWX+23,215))
        screen.blit(roboto.render('30',True,(0,0,0)),(WINDOWX+90,230))
        screen.blit(roboto.render('18',True,(0,0,0)),(WINDOWX+140,230))
        height += 40

    if gold >= 40:
        screen.blit(entities[KNIGHT],(WINDOWX+23,255))
        screen.blit(roboto.render('40',True,(0,0,0)),(WINDOWX+90,270))
        screen.blit(roboto.render('36',True,(0,0,0)),(WINDOWX+140,270))
        height += 40

    return height

def drawSideBar(screen :pygame.Surface,grid,selected,WINDOWX,WINDOWY,color):

    global end_button_rect

    #Status line
    if is_our_turn():
        screen.blit(roboto_heading.render('Your turn',True,COLOR_MAPPING[color-1]),(WINDOWX+center('Your turn',roboto_heading),15))
    else:
        turn = get_turn()
        screen.blit(roboto_heading.render(f'{NAME_MAPPING[turn-1]}\'s turn',True,COLOR_MAPPING[turn-1]),(WINDOWX+center(f'{NAME_MAPPING[turn-1]}\'s turn',roboto_heading),15))

    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,45,160,2))

    #End Turn button
    if is_our_turn():
        if end_button_rect.collidepoint(pygame.mouse.get_pos()): screen.blit(buttons[0][1],(WINDOWX + 33,WINDOWY-50))
        else: screen.blit(buttons[0][0],(WINDOWX + 33,WINDOWY-50))
    else:
        screen.blit(buttons[0][2],(WINDOWX + 33,WINDOWY-50))
        


    #Shop window and finances
    if selected is None:
        screen.blit(roboto_heading.render('No State Selected',True,(0,0,0)),(WINDOWX+center('No State Selected',roboto_heading),60))
        return

    offset = drawShopWindow(screen,WINDOWX,grid[selected[0]][selected[1]].gold)

    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,offset+45,160,2)) 
    screen.blit(roboto_heading.render('Finances',True,(0,0,0)),(WINDOWX+center('Finances',roboto_heading),offset+60))

    screen.blit(roboto.render(f'Savings{grid[selected[0]][selected[1]].gold:>12}',True,(0,0,0)),(WINDOWX+25,offset+80))
    screen.blit(roboto.render(f'Wages{("-"+str(grid[selected[0]][selected[1]].wages)):>14}',True,(0,0,0)),(WINDOWX+25,offset+100))
    screen.blit(roboto.render(f'Income{("+"+str(grid[selected[0]][selected[1]].income)):>13}',True,(0,0,0)),(WINDOWX+25,offset+120))
    screen.fill((0,0,0),pygame.Rect(WINDOWX+20,offset+140,160,1))
    screen.blit(roboto.render(f'Net{grid[selected[0]][selected[1]].net:>16}',True,(0,0,0)),(WINDOWX+25,offset+155))
    return

def drawMapLayer(screen :pygame.Surface, grid, blink: bool):
    for y in range (0,len(grid[0])):
        for x in range(0,len(grid)):
            if (y%2==1):
                screen.blit(cells[grid[x][y].color][grid[x][y].selected or (blink and grid[x][y].blink)],((x+0.5)*48,y*36))
                screen.blit(debug.render(str(grid[x][y].security),True,(255,255,100)),((x+1)*48,y*36))
            else:
                screen.blit(cells[grid[x][y].color][grid[x][y].selected or (blink and grid[x][y].blink)],(x*48,y*36))
                screen.blit(debug.render(str(grid[x][y].security),True,(255,255,100)),((x+0.5)*48,y*36))
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