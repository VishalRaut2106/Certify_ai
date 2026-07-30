@echo off
setlocal EnableDelayedExpansion
title CertifyAI - Setup
color 0A

echo ===================================================
echo     CertifyAI - One-Time Setup
echo ===================================================
echo.

:: Go to the project's backend folder
cd /d "%~dp0"
cd src\backend

:: Step 1: Check if Python is installed
echo [1/6] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo [ERROR] Download it from https://www.python.org/downloads/
    echo [ERROR] Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo       Found %%i
echo.

:: Step 2: Remove old/broken venv if it exists
if exist "venv" (
    echo [2/6] Removing old virtual environment...
    rmdir /s /q venv
    echo       Done.
) else (
    echo [2/6] No old virtual environment found. Skipping.
)
echo.

:: Step 3: Create fresh venv
echo [3/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)
echo       Done.
echo.

:: Step 4: Install dependencies
echo [4/6] Installing dependencies (this may take a few minutes)...
venv\Scripts\python -m pip install --upgrade pip >nul 2>&1
venv\Scripts\python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install some dependencies!
    echo [ERROR] Check the errors above and try again.
    pause
    exit /b 1
)
echo       Done.
echo.

:: Step 5: Check/install Tesseract OCR
set TESSERACT_FOUND=0
if exist "tesseract\tesseract.exe" set TESSERACT_FOUND=1
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" set TESSERACT_FOUND=1

if !TESSERACT_FOUND!==1 (
    echo [5/6] Tesseract OCR found. Skipping.
) else (
    echo [5/6] Downloading Tesseract OCR...
    if not exist "tesseract" mkdir tesseract
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe' -OutFile 'tesseract\tesseract-setup.exe'"
    echo       Installing Tesseract silently...
    tesseract\tesseract-setup.exe /S /D=%CD%\tesseract
    del tesseract\tesseract-setup.exe
    echo       Done.
)
echo.

:: Step 6: Check/install Poppler
if exist "poppler\poppler-24.08.0\Library\bin\pdfinfo.exe" (
    echo [6/6] Poppler found. Skipping.
) else (
    echo [6/6] Downloading Poppler for PDF processing...
    if not exist "poppler" mkdir poppler
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip' -OutFile 'poppler\poppler.zip'"
    echo       Extracting Poppler...
    powershell -Command "Expand-Archive -Path 'poppler\poppler.zip' -DestinationPath 'poppler' -Force"
    del poppler\poppler.zip
    echo       Done.
)
echo.

echo ===================================================
echo     Setup Complete!
echo ===================================================
echo.
echo You can now run the app by double-clicking:
echo     Start_CertifyAI.bat
echo.
pause
