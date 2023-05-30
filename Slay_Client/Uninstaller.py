import os
import shutil
import winreg
import sys

auto_flag = False

try:
    if sys.argv[1] == '--auto': auto_flag = True
except Exception:
    pass

REG_PATH = 'SOFTWARE\Microsoft\Windows\CurrentVersion\\Uninstall'
KNOWN_FAILS = ['C:\\Program Files (x86)\\Slay\\python310.dll','C:\\Program Files (x86)\\Slay\\uninstall.exe','C:\\Program Files (x86)\\Slay\\VCRUNTIME140.dll','C:\\Program Files (x86)\\Slay\\_bz2.pyd','C:\\Program Files (x86)\\Slay\\_lzma.pyd','C:\\Program Files (x86)\\Slay']

installPath =  os.environ["ProgramFiles(x86)"] + r'\Slay'
shortcutPath = os.environ["USERPROFILE"] + r'\Desktop\Slay.lnk'

print('DO NOT CLOSE THIS WINDOW')

def ErrorHandler(func,path,err):
    if path in KNOWN_FAILS: return
    print(f'WARN: Error raised by {func} removing {path}, {err}\nContinuing...')

if os.path.exists(installPath):
    print('Program installation found! Removing...')
    shutil.rmtree(installPath,onerror=ErrorHandler)
else:
    print('WARNING: Program installation not found!, No files were removed.')

if os.path.exists(shortcutPath): 
    print('Desktop Shortcut found! Removing...')
    os.remove(shortcutPath)
else:
    print('Desktop Shortcut not found! Skipping...')

try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_WRITE) as registry_key:
            winreg.DeleteKey(registry_key, 'Slay')
            winreg.CloseKey(registry_key)
            print('Registry Entries removed')
except WindowsError as err:
    print('Error Erasing Registry entries:',err)

if not auto_flag: _ = input('Process complete successfully, press Enter to finish...')