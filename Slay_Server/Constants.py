import configparser
import os

config = configparser.ConfigParser()

if not os.path.exists('./config.ini'):
    print('Config file missing!, Generating default config and shutting down')
    DEFAULTCONFIG = '''[BASIC]
# Port on which server listens, ports 0-1023 are privileged and may require elevated access
Port = 4444

# Map size in number of cells, too many the window might be too big
# Also larger maps take much longer to generate
MapXSize = 15
MapYSize = 15

# Number of players needed for the game
NumberOfPlayers = 2

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

    raise SystemExit()

try:
    config.read('config.ini')
    PORT = int(config['BASIC']['Port'])
    XSIZE = int(config['BASIC']['MapXSize'])
    YSIZE = int(config['BASIC']['MapYSize'])
    MAX_COLOR = int(config['BASIC']['NumberOfPlayers'])
    IP = config['ADVANCED']['IP']
    DISCOVERABLE = bool(config['DISCOVERY']['EnableDiscovery'])
    NAME = config['DISCOVERY']['DiscoveryServerName']
    PASSWORD = config['DISCOVERY']['Password']
    PUBLIC = len(PASSWORD) == 0
except (Exception) as err:
    print('Error Parsing config:')
    print(err)
    raise SystemExit()

COLOR_MAPPING = ['Blue','Yellow','Red','Green']
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