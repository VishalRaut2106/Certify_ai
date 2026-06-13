# Desktop App Build Instructions

## Quick Start (Recommended)

### Option 1: Lite Build (Fast - 3-5 minutes)

```batch
cd backend
build_lite.bat
```

**Output:** `dist\CertifyAI\CertifyAI.exe`

### Option 2: Full Build (Slow - 10-20 minutes)

```batch
cd backend
build_desktop.bat
```

---

## Prerequisites

### 1. Tesseract OCR
- **Required:** Must be installed on the system
- **Download:** https://github.com/UB-Mannheim/tesseract/wiki
- **Default Location:** `C:\Program Files\Tesseract-OCR\`

### 2. Python Environment
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyparsing packaging pyinstaller pywebview
```

---

## Build Configurations

### Lite Build (CertifyAI_Lite.spec)
✅ **Pros:**
- Faster build time (3-5 minutes)
- Smaller executable size
- Simplified dependency tree
- Fewer potential errors

❌ **Cons:**
- May miss some edge case dependencies

**Use when:**
- You want quick builds for testing
- Building on slower machines
- CI/CD pipelines

### Full Build (CertifyAI.spec)
✅ **Pros:**
- Complete dependency coverage
- Maximum compatibility
- All features guaranteed

❌ **Cons:**
- Very slow build time (10-20 minutes)
- Larger executable size
- More complex dependency tree

**Use when:**
- Final production builds
- Maximum compatibility needed
- Building on fast machines

---

## Manual Build Commands

### Lite Build
```batch
cd backend
venv\Scripts\activate
pyinstaller CertifyAI_Lite.spec --noconfirm --clean
```

### Full Build
```batch
cd backend
venv\Scripts\activate
pyinstaller CertifyAI.spec --noconfirm --clean
```

---

## Troubleshooting

### Error: "pyparsing package is required"
**Solution:**
```batch
pip install pyparsing packaging
```

### Error: "Tesseract not found"
**Solution:**
- Install Tesseract OCR at `C:\Program Files\Tesseract-OCR\`
- Or update `ocr.py` with correct path

### Build Hangs on "Performing binary reclassification"
**Solution:**
- This is normal for full build (can take 5-10 minutes)
- Be patient or use lite build instead
- Check Task Manager - Python should be using CPU

### Error: "Module not found"
**Solution:**
```batch
pip install -r requirements.txt
pip list  # Verify all packages installed
```

---

## Testing the Build

### After Build Completes

1. Navigate to output folder:
```batch
cd dist\CertifyAI
```

2. Run the executable:
```batch
CertifyAI.exe
```

3. Expected behavior:
   - Splash screen appears
   - Main window opens automatically
   - Web interface loads

### Test Checklist

- [ ] App launches without errors
- [ ] Single certificate upload works
- [ ] Bulk certificate upload works
- [ ] Excel report downloads correctly
- [ ] Excel has 6 columns: File Name, Name on Certificate, Issued By, Course, Date, Result
- [ ] Color coding works (green/red/yellow)
- [ ] App closes cleanly

---

## Distribution

### For End Users

**Option A: Zip Distribution**
```batch
# Zip the entire folder
powershell Compress-Archive -Path "dist\CertifyAI" -DestinationPath "CertifyAI.zip"
```

**Option B: Create Installer**
- Use Inno Setup or NSIS
- Include Tesseract OCR in installer
- Creates professional installation experience

---

## CI/CD Build (GitHub Actions Example)

```yaml
name: Build Desktop App

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pyparsing packaging pyinstaller pywebview
    
    - name: Build with PyInstaller (Lite)
      run: |
        cd backend
        pyinstaller CertifyAI_Lite.spec --noconfirm --clean
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: CertifyAI-Windows
        path: backend/dist/CertifyAI/
```

---

## Performance Comparison

| Build Type | Time | Size | Dependencies |
|------------|------|------|--------------|
| Lite | 3-5 min | ~150 MB | Minimal |
| Full | 10-20 min | ~200 MB | Complete |

---

## Notes

- Build time varies based on CPU speed and available RAM
- First build is slower (PyInstaller caches data)
- Subsequent builds are faster
- Antivirus may slow down or block build process
- Windows Defender may flag the .exe (false positive)

---

## Support

If build fails:
1. Check this document first
2. Verify all prerequisites installed
3. Try lite build instead of full build
4. Check GitHub Issues
5. Run diagnostic: `python test_desktop.py`

---

**Last Updated:** 2024
