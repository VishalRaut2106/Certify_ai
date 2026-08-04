@echo off
setlocal EnableDelayedExpansion

title CertifyAI - Single-File Executable Builder

echo ===================================================
echo     CertifyAI - Single-File Application Builder
echo ===================================================
echo.

cd /d "%~dp0"

:: 1. Check / Initialize Virtual Environment
if not exist "src\backend\venv\Scripts\activate.bat" (
    echo [1/5] Virtual environment not found. Setting up venv...
    python -m venv src\backend\venv
    if errorlevel 1 (
        echo [ERROR] Python is required to build CertifyAI.exe. Please install Python 3.10+ and add to PATH.
        pause
        exit /b 1
    )
    call src\backend\venv\Scripts\activate.bat
    echo [INFO] Installing required dependencies...
    python -m pip install --upgrade pip --quiet
    python -m pip install -r src\backend\requirements.txt --quiet
) else (
    call src\backend\venv\Scripts\activate.bat
)

:: 2. Ensure PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller --quiet
)

:: 3. Check / Download Tesseract OCR
set TESSERACT_FOUND=0
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" set TESSERACT_FOUND=1
if exist "src\backend\tesseract\tesseract.exe" set TESSERACT_FOUND=1

if !TESSERACT_FOUND!==0 (
    echo [2/5] Tesseract OCR missing. Downloading Tesseract for bundling...
    if not exist "src\backend\tesseract" mkdir "src\backend\tesseract"
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe' -OutFile 'src\backend\tesseract\tesseract-setup.exe'"
    echo [INFO] Extracting Tesseract silently...
    src\backend\tesseract\tesseract-setup.exe /S /D=%CD%\src\backend\tesseract
    if exist "src\backend\tesseract\tesseract-setup.exe" del src\backend\tesseract\tesseract-setup.exe
    echo [INFO] Tesseract ready.
) else (
    echo [2/5] Tesseract OCR found.
)

:: 4. Check / Download Poppler
if not exist "src\backend\poppler\poppler-24.08.0\Library\bin\pdfinfo.exe" (
    echo [3/5] Poppler missing. Downloading Poppler for PDF processing...
    if not exist "src\backend\poppler" mkdir "src\backend\poppler"
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip' -OutFile 'src\backend\poppler\poppler.zip'"
    echo [INFO] Extracting Poppler...
    powershell -Command "Expand-Archive -Path 'src\backend\poppler\poppler.zip' -DestinationPath 'src\backend\poppler' -Force"
    if exist "src\backend\poppler\poppler.zip" del src\backend\poppler\poppler.zip
    echo [INFO] Poppler ready.
) else (
    echo [3/5] Poppler found.
)

:: 5. Clean previous build artifacts
echo [4/5] Cleaning previous build folders...
taskkill /F /IM CertifyAI.exe >nul 2>&1
timeout /t 1 /nobreak >nul
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

:: 6. Build Executable
echo [5/5] Building single-file CertifyAI.exe with PyInstaller...
pyinstaller CertifyAI_OneFile.spec --noconfirm --clean

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed! Check PyInstaller log above for details.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo     BUILD SUCCESSFUL!
echo ===================================================
echo.
echo Executable location:
echo     %CD%\dist\CertifyAI.exe
echo.
echo You can now distribute dist\CertifyAI.exe as a portable standalone Windows app.
echo.

set /p TEST_LAUNCH="Would you like to test launching dist\CertifyAI.exe now? (y/n): "
if /i "%TEST_LAUNCH%"=="y" (
    start "" "dist\CertifyAI.exe"
)

pause
