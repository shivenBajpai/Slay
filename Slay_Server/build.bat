pyinstaller --name "Slay Server" ^
    --console --onedir --noconfirm^
    --log-level=WARN ^
    --add-data="README.md;." ^
    --icon=.\icon.ico ^
    Supervisor.py