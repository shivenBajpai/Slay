import os
import shutil
import winreg

REG_PATH = 'SOFTWARE\Microsoft\Windows\CurrentVersion\\Uninstall'

installPath =  os.environ["ProgramFiles(x86)"] + r'\Slay Server'
shortcutPath = os.environ["USERPROFILE"] + r'\Desktop\Slay Server.lnk'

print('DO NOT CLOSE THIS WINDOW')

def ErrorHandler(func,path,err):
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
            winreg.DeleteKey(registry_key, 'Slay_Server')
            winreg.CloseKey(registry_key)
            print('Registry Entries removed')
except WindowsError as err:
    print('Error Erasing Registry entries:',err)

_ = input('Process complete successfully, press Enter to finish...')