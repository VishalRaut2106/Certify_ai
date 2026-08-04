@echo off
setlocal EnableDelayedExpansion
title CertifyAI Verification System
color 0A

echo ===================================================
echo     Starting CertifyAI Verification System
echo ===================================================
echo.

cd /d "%~dp0"

:: 1. Check if built single-file executable exists
if exist "dist\CertifyAI.exe" (
    echo [INFO] Built standalone CertifyAI.exe detected.
    echo [INFO] Launching CertifyAI standalone application...
    start "" "dist\CertifyAI.exe"
    exit /b 0
)

:: 2. If no dist\CertifyAI.exe, check if user wants to build it or run via python
cd src\backend

set NEED_VENV=0

if not exist "venv\Scripts\python.exe" (
    set NEED_VENV=1
    echo [INFO] No virtual environment found.
) else (
    venv\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 (
        set NEED_VENV=1
        echo [INFO] Existing virtual environment is broken. Re-initializing...
        rmdir /s /q venv
    )
)

if !NEED_VENV!==1 (
    echo [INFO] Creating virtual environment... This may take a minute.
    python -m venv venv
    
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create virtual environment!
        echo [ERROR] Please make sure Python is installed on this computer and added to PATH.
        pause
        exit /b 1
    )
    
    echo [INFO] Installing required dependencies...
    venv\Scripts\python -m pip install --upgrade pip
    venv\Scripts\python -m pip install -r requirements.txt
    
    echo [INFO] Setup complete!
    echo.
)

:: Check Tesseract OCR
set TESSERACT_FOUND=0
if exist "tesseract\tesseract.exe" set TESSERACT_FOUND=1
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" set TESSERACT_FOUND=1

if !TESSERACT_FOUND!==0 (
    echo [INFO] Tesseract OCR is missing. Downloading Tesseract...
    if not exist "tesseract" mkdir tesseract
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe' -OutFile 'tesseract\tesseract-setup.exe'"
    echo [INFO] Installing Tesseract silently...
    tesseract\tesseract-setup.exe /S /D=%CD%\tesseract
    echo [INFO] Cleaning up installer...
    del tesseract\tesseract-setup.exe
    echo [INFO] Tesseract installed successfully!
    echo.
)

:: Check Poppler
if not exist "poppler\poppler-24.08.0\Library\bin\pdfinfo.exe" (
    echo [INFO] Poppler is missing. Downloading Poppler...
    if not exist "poppler" mkdir poppler
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip' -OutFile 'poppler\poppler.zip'"
    echo [INFO] Extracting Poppler...
    powershell -Command "Expand-Archive -Path 'poppler\poppler.zip' -DestinationPath 'poppler' -Force"
    del poppler\poppler.zip
    echo [INFO] Poppler installed successfully!
    echo.
)

:: Run the application via Python backend
echo [INFO] Launching Application...
venv\Scripts\python desktop_simple.py

echo.
echo [INFO] Server stopped or closed.
pause
