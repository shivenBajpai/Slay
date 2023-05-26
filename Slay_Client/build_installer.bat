:: Requires WinRAR at the usual installation location, Builds installer exe, run after built.bat
mkdir ".\installer"
del ".\installer\SlayInstaller.exe"
"C:\Program Files\WinRAR\WinRAR.exe" a -r -y -m5 -ma5 -afrar -cfg- -k -tl -ep1 -iadm -s -iiconicon.ico -iimgbanner.png -zinstaller_options.txt -sfx ".\installer\SlayWinInstaller.exe" dist\Slay\*
"C:\Program Files\WinRAR\WinRAR.exe" a -r -y -m5 -ma5 -afzip -cfg- -k -tl -ep1 -s -xdist\Slay\banner.png -xdist\Slay\setup.exe -xdist\Slay\uninstall.exe ".\installer\Slay.zip" dist\Slay\*