import os
import shutil
import winreg
import sys

auto_flag = False

try:
    if sys.argv[1] == '--auto': auto_flag = True
except Exception:
    pass

installPath = __file__[:-15]
desktopShortcutPath = os.environ["USERPROFILE"] + r'\Desktop\Slay.lnk'
startShortcutPath = os.environ["APPDATA"] + '\\Microsoft\\Windows\\Start Menu\\Programs\\Slay.lnk'

REG_PATH = 'SOFTWARE\Microsoft\Windows\CurrentVersion\\Uninstall'
KNOWN_FAILS = [installPath+'\\python310.dll',installPath+'\\uninstall.exe',installPath+'\\VCRUNTIME140.dll',installPath+'\\_bz2.pyd',installPath+'\\_lzma.pyd',installPath]

print('DO NOT CLOSE THIS WINDOW')

def ErrorHandler(func,path,err):
    if path in KNOWN_FAILS: return
    print(f'WARN: Error raised by {func} removing {path}, {err}\nContinuing...')

try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_WRITE) as registry_key:
            winreg.DeleteKey(registry_key, 'Slay')
            winreg.CloseKey(registry_key)
            print('Registry Entries removed')
except WindowsError as err:
    print('Error Erasing Registry entries:',err)

if os.path.exists(desktopShortcutPath): 
    print('Desktop Shortcut found! Removing...')
    os.remove(desktopShortcutPath)
else:
    print('Desktop Shortcut not found! Skipping...')

if os.path.exists(startShortcutPath): 
    print('Start Menu Shortcut found! Removing...')
    os.remove(startShortcutPath)
else:
    print('Start Menu Shortcut not found! Skipping...')

if os.path.exists(installPath):
    try:
        print('Program installation found! Removing...')
        shutil.rmtree(installPath,onerror=ErrorHandler)
    except Exception as err:
        print(err)
else:
    print('WARNING: Program installation not found!, No files were removed.')

if not auto_flag: _ = input('Process complete successfully, press Enter to finish...')