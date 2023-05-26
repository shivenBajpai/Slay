:: pip install pyinstaller
:: Calls pyinstaller with the required options, cleans up some files afterward that shouldnt be in the build and will be regened at runtime
pyinstaller --noconfirm --log-level=WARN --clean Slay.spec
rmdir /s /q "./dist/Slay/Slay_Assets/src"
del /q ".\dist\Slay\replays\*"
del /q ".\dist\Slay\integratedServer\*"