@echo off
setlocal EnableDelayedExpansion

echo.
echo  ============================================
echo    CertifyAI  ^|  Desktop Build Script
echo  ============================================
echo.

:: ── Check venv ────────────────────────────────────────────────────────────────
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo         Run: python -m venv venv ^&^& venv\Scripts\pip install -r requirements.txt
    pause & exit /b 1
)

call venv\Scripts\activate.bat

:: ── Check PyInstaller ─────────────────────────────────────────────────────────
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller==6.6.0 --quiet
)

:: ── Check pywebview ───────────────────────────────────────────────────────────
python -c "import webview" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing pywebview...
    pip install pywebview==5.0.5 --quiet
)

:: ── Check Tesseract ───────────────────────────────────────────────────────────
if not exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [ERROR] Tesseract OCR not found at C:\Program Files\Tesseract-OCR\
    echo         Download from: https://github.com/UB-Mannheim/tesseract/wiki
    pause & exit /b 1
)

:: ── Clean previous build ──────────────────────────────────────────────────────
echo [1/3] Cleaning previous build...
if exist "build"  rmdir /s /q build
if exist "dist"   rmdir /s /q dist

:: ── Run PyInstaller ───────────────────────────────────────────────────────────
echo [2/3] Building with PyInstaller...
pyinstaller CertifyAI.spec --noconfirm

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed. Check the output above for details.
    pause & exit /b 1
)

:: ── Done ──────────────────────────────────────────────────────────────────────
echo [3/3] Build complete!
echo.
echo  Output: dist\CertifyAI\CertifyAI.exe
echo.
echo  To test: dist\CertifyAI\CertifyAI.exe
echo.

:: Ask to launch
set /p LAUNCH="Launch the app now? (y/n): "
if /i "%LAUNCH%"=="y" (
    start "" "dist\CertifyAI\CertifyAI.exe"
)

pause
