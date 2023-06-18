import configparser
import os

config = configparser.ConfigParser()

COLOR_MAPPING = ['Blue','Yellow','Pink','Green','Lime','Violet','Turqoise','Orange','Red','Brown']
NONE = 0
TREE = 1
PALM = 2
GRAVE = 3
TOWER = 4
CITY = 5
MAN = 6
SPEARMAN = 7
BARON = 8
KNIGHT = 9
CITY_SECURITY = 1
TOWER_SECURITY = 2

if not os.path.exists('./config.ini'):
    print('Config file missing!, Generating default config file')
    DEFAULTCONFIG = '''[BASIC]
# Port on which server listens, ports 0-1023 are privileged and may require elevated access
Port = 4444

# Map size in number of cells, minimum 5 on each axis
# Reccomended atleast 1.6*Number of players for fast map creation. 2*Number of players if more than 5 players
MapXSize = 15
MapYSize = 15

# Number of players needed for the game and the number of bots in the game (there must be atleast one human player)
NumberOfPlayers = 2
NumberofBots = 0

# Automatically-Relaunch server every time game ends/crashes
AutoReboot = False

[DISCOVERY]
# Allow other computers on the local network to find and connect to this server
# If set to False, all discovery related options are meaningless
EnableDiscovery = True

# Name of server in server list on client side
DiscoveryServerName = Slay Server

# Password required to join
# If empty, password will not be required
Password = 

[ADVANCED]
# Dont touch unless you know what you're doing
# IP on which server socket requests to listen
IP = 0.0.0.0'''
    f = open("config.ini", "w")
    f.write(DEFAULTCONFIG)
    f.close()

try:
    config.read('config.ini')
    PORT = int(config['BASIC']['Port'])
    XSIZE = int(config['BASIC']['MapXSize'])
    if XSIZE < 4: 
        print('Map X Size must be atleast 4. Overriding')
        XSIZE = 5
    XSIZE += 1
    YSIZE = int(config['BASIC']['MapYSize'])
    if YSIZE < 4: 
        print('Map Y Size must be atleast 4. Overriding')
        YSIZE = 5
    YSIZE += 1
    MAX_COLOR = int(config['BASIC']['NumberOfPlayers'])
    if MAX_COLOR > len(COLOR_MAPPING): raise Exception('Too many players! Max 10')
    BOTS = int(config['BASIC']['NumberOfBots'])
    if BOTS >= MAX_COLOR: raise Exception('Too many bots!')
    AUTOREBOOT = config['BASIC']['AutoReboot'] == 'True'
    IP = config['ADVANCED']['IP']
    DISCOVERABLE = config['DISCOVERY']['EnableDiscovery'] == 'True'
    NAME = config['DISCOVERY']['DiscoveryServerName']
    PASSWORD = config['DISCOVERY']['Password']
    PUBLIC = len(PASSWORD) == 0
except (Exception) as err:
    print('Error Parsing config:')
    print(err)
    raise SystemExit()