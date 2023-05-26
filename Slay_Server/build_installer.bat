:: Requires WinRAR at the usual installation location, Builds installer exe, run after built.bat
mkdir ".\installer"
del ".\installer\SlayServerInstaller.exe"
"C:\Program Files\WinRAR\WinRAR.exe" a -r -y -m5 -ma5 -afrar -cfg- -k -tl -ep1 -iadm -s -iiconicon.ico -iimgbanner.png -zinstaller_options.txt -sfx ".\installer\SlayServerWinInstaller.exe" "dist\Slay Server\*"
"C:\Program Files\WinRAR\WinRAR.exe" a -r -y -m5 -ma5 -afzip -cfg- -k -tl -ep1 -s "-xdist\Slay Server\banner.png" "-xdist\Slay Server\setup.exe" "-xdist\Slay Server\uninstall.exe" ".\installer\SlayServer.zip" "dist\Slay Server\*"