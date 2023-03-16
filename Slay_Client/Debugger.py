import configparser
import os
import pygame
from pygame.constants import QUIT

DebugPos = (1,1)

if os.path.exists('./config.ini'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    DEBUG = config['DEBUG']['EnableDebugger'] == 'True'
    FREEZE = config['DEBUG']['FreezeOnCrash'] == 'True'
else:
    DEBUG = False
    FREEZE = False

def HandleFreezing(caption,err):
    if FREEZE: 
        print(err)
        pygame.display.set_caption(caption)
        while True:
            if pygame.event.poll().type == QUIT: break
    return

def SetDebugPos(pos):
    global DebugPos
    DebugPos = pos

def GetDebugPos():
    global DebugPos
    return DebugPos