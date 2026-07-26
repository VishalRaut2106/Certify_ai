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

:: Run the application
echo [INFO] Launching Application...
venv\Scripts\python desktop_simple.py

echo.
echo [INFO] Server stopped or closed.
pause
