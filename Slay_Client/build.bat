pyinstaller --name Slay ^
    --noconsole --onedir --noconfirm^
    --log-level=WARN ^
    --add-data="README.md;." ^
    --add-data="Slay_Assets;Slay_Assets" ^
    --add-data="replays;replays" 
    --add-data="icon.ico;." ^
    --icon=.\icon.ico ^
    Launcher.py