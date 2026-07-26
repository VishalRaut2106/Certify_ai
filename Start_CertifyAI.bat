@echo off
title CertifyAI Verification System
color 0A

echo ===================================================
echo     Starting CertifyAI Verification System
echo ===================================================
echo.

:: Get the directory where the .bat file is located and go there
cd /d "%~dp0"
cd backend

:: Check if the virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [INFO] First time setup detected. 
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
    venv\Scripts\pip install -r requirements.txt
    
    echo [INFO] Setup complete!
    echo.
)

:: Check if poppler is installed (required for PDF processing)
if not exist "poppler\poppler-24.08.0\Library\bin\pdfinfo.exe" (
    echo [INFO] Poppler is missing. Downloading Poppler for PDF processing...
    if not exist "poppler" mkdir poppler
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip' -OutFile 'poppler\poppler.zip'"
    echo [INFO] Extracting Poppler...
    powershell -Command "Expand-Archive -Path 'poppler\poppler.zip' -DestinationPath 'poppler' -Force"
    del poppler\poppler.zip
    echo [INFO] Poppler installed successfully!
    echo.
)

:: Run the application
echo [INFO] Launching Application...
venv\Scripts\python desktop_simple.py

echo.
echo [INFO] Server stopped or closed.
pause
