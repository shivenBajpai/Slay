:: pip install pyinstaller
:: Calls pyinstaller with the required options, cleans up some files afterward and removes config files, they will be generated on runtime with default settings
pyinstaller --name Slay ^
    --noconsole --onedir --noconfirm --uac-admin^
    --log-level=WARN ^
    --add-data="README.md;." ^
    --add-data="postinstall.bat;." ^
    --add-data="Slay_Assets;Slay_Assets" ^
    --add-data="integratedServer;integratedServer" ^
    --add-data="replays;replays" ^
    --add-data="icon.ico;." ^
    --add-data="banner.png;." ^
    --icon=.\icon.ico ^
    Launcher.py
rmdir /s /q "./dist/Slay/Slay_Assets/src"
del /q ".\dist\Slay\replays\*"
del ".\dist\Slay\integratedServer\config.ini"