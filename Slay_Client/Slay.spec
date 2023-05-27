# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


slay_a = Analysis(
    ['Launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.'), ('Slay_Assets', 'Slay_Assets'), ('integratedServer', 'integratedServer'), ('replays', 'replays'), ('icon.ico', '.'), ('banner.png', '.')],
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
slay_pyz = PYZ(slay_a.pure, slay_a.zipped_data, cipher=block_cipher)

slay_exe = EXE(
    slay_pyz,
    slay_a.scripts,
    [],
    exclude_binaries=True,
    name='Slay',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['icon.ico'],
)

uninstall_a = Analysis(
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
uninstall_pyz = PYZ(uninstall_a.pure, uninstall_a.zipped_data, cipher=block_cipher)

uninstall_exe = EXE(
    uninstall_pyz,
    uninstall_a.scripts,
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
    uac_admin=True,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)

coll = COLLECT(
    slay_exe,
    slay_a.binaries,
    slay_a.zipfiles,
    slay_a.datas,
    installer_exe,
    installer_a.binaries,
    installer_a.zipfiles,
    installer_a.datas,
    uninstall_exe,
    uninstall_a.binaries,
    uninstall_a.zipfiles,
    uninstall_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Slay',
)
