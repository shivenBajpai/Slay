import configparser
import os
import pygame
from pygame.constants import QUIT

DebugPos = (1,1)

DEFAULTCONFIG = '''[DEBUG]
EnableDebugger = False
FreezeOnCrash = False'''

if os.path.exists('./config.ini'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    DEBUG = config['DEBUG']['EnableDebugger'] == 'True'
    FREEZE = config['DEBUG']['FreezeOnCrash'] == 'True'
else:
    DEBUG = False
    FREEZE = False
    with open('./config.ini','x') as f: f.write(DEFAULTCONFIG) 

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