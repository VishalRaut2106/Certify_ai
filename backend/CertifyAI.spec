# -*- mode: python ; coding: utf-8 -*-
"""
CertifyAI.spec  —  PyInstaller build specification
Run from the backend/ directory:
    pyinstaller CertifyAI.spec
"""

import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# ── Paths (relative to backend/) ──────────────────────────────────────────────
HERE         = os.path.abspath(SPECPATH)          # = backend/
FRONTEND_DIR = os.path.join(HERE, '..', 'frontend')
POPPLER_BIN  = os.path.join(HERE, 'poppler', 'poppler-24.08.0', 'Library', 'bin')
TESSERACT_DIR= r'C:\Program Files\Tesseract-OCR'  # adjust if installed elsewhere

block_cipher = None

# ── Collect hidden imports ─────────────────────────────────────────────────────
hidden = (
    collect_submodules('uvicorn')
    + collect_submodules('fastapi')
    + collect_submodules('starlette')
    + collect_submodules('anyio')
    + collect_submodules('multipart')
    + collect_submodules('webview')
    + [
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'anyio._backends._asyncio',
        'pytesseract',
        'pyzbar.pyzbar',
        'cv2',
        'PIL',
        'pdf2image',
        'fuzzywuzzy',
        'Levenshtein',
        'openpyxl',
        'email_validator',
        'dotenv',
    ]
)

# ── Data files to bundle ───────────────────────────────────────────────────────
datas = [
    # Frontend HTML/CSS/JS
    (FRONTEND_DIR, 'frontend'),
    # Poppler binaries (for PDF support)
    (POPPLER_BIN, 'poppler/bin'),
    # Tesseract executable + tessdata language files
    (TESSERACT_DIR, 'tesseract'),
]

# Also bundle fastapi/starlette internal data files
datas += collect_data_files('starlette')
datas += collect_data_files('fastapi')

a = Analysis(
    ['desktop.py'],
    pathex=[HERE],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Strip heavy packages we don't need in the desktop build
        'tkinter',
        'matplotlib',
        'scipy',
        'sklearn',
        'redis',
        'pymongo',
        'motor',
        'pytest',
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
    console=False,      # No console window — it's a GUI app
    icon=None,          # Add icon path here e.g. 'assets/icon.ico'
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
