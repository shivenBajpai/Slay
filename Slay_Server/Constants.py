import configparser
import os
import sys

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
no_file_mode = '--nofile' in sys.argv

def evaluate_bool(string):
    if string in ['True','true','T','t','Yes','yes','Y','y','On','on','1']: return True
    elif string in ['False','false','F','f','No','no','N','n','Off','off','0']: return False
    else: print('Invalid option for boolean:',string)

if not no_file_mode:
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

    # Whether bots play all their moves at once, or they play their moves slowly (1 by 1)
    BotFastMode = False

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
        YSIZE = int(config['BASIC']['MapYSize'])
        MAX_COLOR = int(config['BASIC']['NumberOfPlayers'])
        BOTS = int(config['BASIC']['NumberOfBots'])
        AUTOREBOOT = config['BASIC']['AutoReboot'] == 'True'
        FASTMODE = config['BASIC']['BotFastMode'] == 'True'
        DISCOVERABLE = config['DISCOVERY']['EnableDiscovery'] == 'True'
        NAME = config['DISCOVERY']['DiscoveryServerName']
        PASSWORD = config['DISCOVERY']['Password']
        IP = config['ADVANCED']['IP']
    except (Exception) as err:
        print('Error Parsing config:')
        print(err)
        raise SystemExit()
else:
    PORT = None
    XSIZE = None
    YSIZE = None
    MAX_COLOR = None
    BOTS = 0
    AUTOREBOOT = False
    FASTMODE = False
    DISCOVERABLE = True
    NAME = 'Slay Server'
    PASSWORD = ""
    IP = "0.0.0.0"

del sys.argv[0]
i=0

while i<len(sys.argv):
    try:
        item = sys.argv[i]
        option = sys.argv[i+1]
        if item in ['--fastmode','--fast','-f']: FASTMODE = evaluate_bool(option)
        elif item in ['--autoreboot','--auto']: AUTOREBOOT = evaluate_bool(option)
        elif item in ['--discovery']: DISCOVERABLE = evaluate_bool(option)
        elif item in ['--name','-n']: NAME = option
        elif item in ['--password','--pass','-p']: PASSWORD = option
        elif item in ['--ip']: IP = option
        elif item in ['--port']: PORT = int(option)
        elif item in ['--xsize','-x']: XSIZE = int(option)
        elif item in ['--ysize','-y']: YSIZE = int(option)
        elif item in ['--maxcolor','--max','--max-color','--players']: MAX_COLOR = int(option)
        elif item in ['--bots']: BOTS = int(option)
        elif item == '--nofile': i -= 1
        else:
            print('unrecognized switch:',item)
        
        i += 2
    except IndexError:
        raise SystemExit('Incomplete/Invalid command line options')

try:
    if PORT is None: raise Exception('Missing option: PORT')
    if XSIZE is None: raise Exception('Missing option: XSIZE')
    if YSIZE is None: raise Exception('Missing option: YSIZE')
    if MAX_COLOR is None: raise Exception('Missing option: MAX_COLOR')

    if XSIZE < 4: 
        print('Map X Size must be atleast 4. Overriding')
        XSIZE = 5
    XSIZE += 1
    if YSIZE < 4: 
        print('Map Y Size must be atleast 4. Overriding')
        YSIZE = 5
    YSIZE += 1
    if MAX_COLOR > len(COLOR_MAPPING): raise Exception('Too many players! Max 10')
    if BOTS >= MAX_COLOR: raise Exception('Too many bots!')
except (Exception) as err:
    print('Error Parsing config:')
    print(err)
    raise SystemExit('Error Parsing config')
PUBLIC = len(PASSWORD) == 0