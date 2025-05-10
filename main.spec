# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],  # Entry point of your program
    pathex=[],
    binaries=[],
    datas=[
        ('bg.png', '.'), 
        ('left-arrow.png', '.'), 
        ('superplay_icon.ico', '.'), 
        ('packs.json', '.'), 
        ('resources.json', '.'), 
        ('links.json', '.'), 
        ('packs.json', '.'), 
        ('filtered_packs.json', '.'), 
        ('dynamic_manager.json', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'grp', 'posix', 'resource', 'fcntl', 'termios', 'multiprocessing', 
        'readline', 'setuptools', 'scipy', 'torch', 'matplotlib', 'IPython'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='superplay_icon.ico',  # Icon for the .exe
)