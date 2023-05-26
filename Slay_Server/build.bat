:: pip install pyinstaller
:: Calls pyinstaller with the required options and removes config file, it will be generated on runtime with default settings
pyinstaller --noconfirm --log-level=WARN --clean Server.spec