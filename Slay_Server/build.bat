:: pip install pyinstaller
:: Calls pyinstaller with the required options and removes config file, it will be generated on runtime with default settings
pyinstaller --name "Slay Server" ^
    --console --onedir --noconfirm^ --uac-admin^
    --log-level=WARN ^
    --add-data="README.md;." ^
    --add-data="postinstall.bat;." ^
    --add-data="banner.png;." ^
    --icon=.\icon.ico ^
    Supervisor.py