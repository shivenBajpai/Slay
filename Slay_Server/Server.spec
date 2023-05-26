# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


installer_a = Analysis(
    ['Setup.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
installer_pyz = PYZ(installer_a.pure, installer_a.zipped_data, cipher=block_cipher)

installer_exe = EXE(
    installer_pyz,
    installer_a.scripts,
    [],
    exclude_binaries=True,
    name='setup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['icon.ico'],
)

server_a = Analysis(
    ['Supervisor.py'],
    pathex=[],
    binaries=[],
    datas=[('readme.txt', '.'), ('banner.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
server_pyz = PYZ(server_a.pure, server_a.zipped_data, cipher=block_cipher)

server_exe = EXE(
    server_pyz,
    server_a.scripts,
    [],
    exclude_binaries=True,
    name='Slay_Server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['icon.ico'],
)

uninstaller_a = Analysis(
    ['Uninstaller.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
uninstaller_pyz = PYZ(uninstaller_a.pure, uninstaller_a.zipped_data, cipher=block_cipher)

uninstaller_exe = EXE(
    uninstaller_pyz,
    uninstaller_a.scripts,
    [],
    exclude_binaries=True,
    name='uninstall',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['icon.ico'],
)

coll = COLLECT(
    installer_exe,
    installer_a.binaries,
    installer_a.zipfiles,
    installer_a.datas,
    server_exe,
    server_a.binaries,
    server_a.zipfiles,
    server_a.datas,
    uninstaller_exe,
    uninstaller_a.binaries,
    uninstaller_a.zipfiles,
    uninstaller_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Slay Server',
)