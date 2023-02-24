pyinstaller --name "Slay Server" ^
    --console --onedir --noconfirm^
    --log-level=WARN ^
    --add-data="README.md;." ^
    --icon=.\icon.ico ^
    Slay_Server.py