# -*- mode: python ; coding: utf-8 -*-
"""
CertifyAI_OneFile.spec — PyInstaller Single-File Executable Spec
Bundles:
  - Backend script (desktop_simple.py)
  - Frontend static assets (src/frontend)
  - Poppler binaries (src/backend/poppler/poppler-24.08.0/Library/bin)
  - Tesseract binaries & tessdata (C:/Program Files/Tesseract-OCR or src/backend/tesseract)
  - Pyzbar DLLs
Outputs:
  - dist/CertifyAI.exe (Single standalone executable file)
"""

import os
import sys
import site

HERE = os.path.abspath(SPECPATH)
BACKEND_DIR = os.path.join(HERE, 'src', 'backend')
FRONTEND_DIR = os.path.join(HERE, 'src', 'frontend')

# Determine Poppler directory
POPPLER_BIN = os.path.join(BACKEND_DIR, 'poppler', 'poppler-24.08.0', 'Library', 'bin')
if not os.path.exists(POPPLER_BIN):
    POPPLER_BIN = os.path.join(BACKEND_DIR, 'poppler', 'bin')

# Determine Tesseract directory
TESSERACT_DIR = r'C:\Program Files\Tesseract-OCR'
if not os.path.exists(TESSERACT_DIR):
    TESSERACT_DIR = os.path.join(BACKEND_DIR, 'tesseract')

datas = [
    (FRONTEND_DIR, 'frontend'),
]

if os.path.exists(POPPLER_BIN):
    datas.append((POPPLER_BIN, 'poppler/bin'))

if os.path.exists(TESSERACT_DIR):
    datas.append((TESSERACT_DIR, 'tesseract'))

# Pyzbar DLLs search
binaries = []
for site_path in site.getsitepackages():
    pyzbar_path = os.path.join(site_path, 'pyzbar')
    if os.path.isdir(pyzbar_path):
        for dll in ['libiconv.dll', 'libzbar-64.dll']:
            dll_path = os.path.join(pyzbar_path, dll)
            if os.path.exists(dll_path):
                binaries.append((dll_path, 'pyzbar'))
        break

hidden_imports = [
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.loops.asyncio',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi',
    'fastapi.responses',
    'fastapi.staticfiles',
    'starlette.routing',
    'starlette.responses',
    'starlette.staticfiles',
    'starlette.middleware',
    'anyio',
    'anyio._backends._asyncio',
    'asyncio',
    'multipart',
    'python_multipart',
    'pytesseract',
    'pyzbar.pyzbar',
    'PIL',
    'PIL.Image',
    'PIL.ImageEnhance',
    'PIL.ImageFilter',
    'cv2',
    'numpy',
    'pdf2image',
    'openpyxl',
    'openpyxl.styles',
    'fuzzywuzzy',
    'Levenshtein',
    'requests',
    'dotenv',
    'h11',
    'email.message',
    'pyparsing',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
]

block_cipher = None

a = Analysis(
    [os.path.join(BACKEND_DIR, 'desktop_simple.py')],
    pathex=[BACKEND_DIR, HERE],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'scipy', 'sklearn', 'scikit_learn', 'redis', 'pymongo', 'motor',
        'pytest', 'black', 'mypy', 'ruff', 'matplotlib', 'tkinter', '_tkinter',
        'unittest', 'test', 'tests', 'clr', 'clr_loader', 'pythonnet', 'Python.Runtime'
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CertifyAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
