import winreg
import os

UninstallString =  os.getcwd() + '\\uninstall.exe'
InstallPath = os.getcwd()
displayIcon = os.getcwd() + '\Slay Server.exe'
ExeName = 'Slay Server.exe'
EstimatedSize = 0x000030D4
displayVersion = '1.0'
displayName = 'Slay Server'

REG_PATH = 'SOFTWARE\Microsoft\Windows\CurrentVersion\\Uninstall\Slay_Server'

print('Software installation: SUCCESS')
print('Setting up Slay Server...')

def set_key(name, value, type):
    try:
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH)
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_WRITE) as registry_key:
            winreg.SetValueEx(registry_key, name, 0, type, value)
            winreg.CloseKey(registry_key)
            return 'SUCCESS'
    except WindowsError as err:
        return err
    
print(f'Writing UninstallString: { set_key("UninstallString",UninstallString,winreg.REG_SZ) }')
print(f'Writing InstallPath: {set_key("InstallPath",InstallPath,winreg.REG_SZ)}')
print(f'Writing displayIcon: {set_key("displayIcon",displayIcon,winreg.REG_SZ)}')
print(f'Writing ExeName: {set_key("ExeName",ExeName,winreg.REG_SZ)}')
print(f'Writing EstimatedSize: {set_key("EstimatedSize",EstimatedSize,winreg.REG_DWORD)}')
print(f'Writing displayVersion: {set_key("displayVersion",displayVersion,winreg.REG_SZ)}')
print(f'Writing displayName: {set_key("displayName",displayName,winreg.REG_SZ)}')

_ = input('Installation successful, press Enter to finish...')