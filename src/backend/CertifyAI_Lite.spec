# -*- mode: python ; coding: utf-8 -*-
"""
CertifyAI_Lite.spec  —  Optimized lightweight build
- Faster build time (3-5 minutes)
- Smaller executable size
- Only essential hidden imports
- Simplified dependency tree

Run from backend/ directory:
    pyinstaller CertifyAI_Lite.spec --noconfirm --clean
"""

import os

HERE         = os.path.abspath(SPECPATH)
FRONTEND_DIR = os.path.join(HERE, '..', 'frontend')
POPPLER_BIN  = os.path.join(HERE, 'poppler', 'poppler-24.08.0', 'Library', 'bin')

# Find pyzbar DLLs
import site
pyzbar_path = None
for site_path in site.getsitepackages():
    candidate = os.path.join(site_path, 'pyzbar')
    if os.path.isdir(candidate):
        pyzbar_path = candidate
        break

datas = [
    (FRONTEND_DIR, 'frontend'),
]
if os.path.isdir(POPPLER_BIN):
    datas.append((POPPLER_BIN, 'poppler/bin'))

# Add pyzbar DLLs if found
binaries = []
if pyzbar_path:
    for dll in ['libiconv.dll', 'libzbar-64.dll']:
        dll_path = os.path.join(pyzbar_path, dll)
        if os.path.exists(dll_path):
            binaries.append((dll_path, 'pyzbar'))

block_cipher = None

# Minimal essential imports only
hidden_imports = [
    # Core uvicorn/fastapi
    'uvicorn.logging',
    'uvicorn.loops.auto',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan.on',
    # Async
    'anyio._backends._asyncio',
    # Essential modules
    'PIL.Image',
    'PIL.ImageEnhance',
    'PIL.ImageFilter',
    'cv2',
    'numpy',
    'pytesseract',
    'pyzbar.pyzbar',
    'openpyxl',
    'openpyxl.styles',
    'pdf2image',
    'webview',
    # Fix pyparsing issue
    'pyparsing',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
]

a = Analysis(
    ['desktop_simple.py'],  # Use simple version without pywebview
    pathex=[HERE],
    binaries=binaries,  # Include pyzbar DLLs
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude only truly unused packages - be conservative
        'scipy', 'sklearn', 'scikit_learn', 'redis', 'pymongo', 'motor',
        'pytest', 'black', 'mypy', 'ruff', 'matplotlib',
        'tkinter', '_tkinter', 'unittest', 'test', 'tests',
        # Exclude pywebview and pythonnet - using browser instead
        'webview', 'clr', 'clr_loader', 'pythonnet', 'Python.Runtime',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CertifyAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CertifyAI',
)
