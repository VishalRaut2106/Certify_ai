"""
Test script to diagnose desktop app issues before building with PyInstaller
"""
import sys
import os

print("="*80)
print("DESKTOP APP DIAGNOSTIC REPORT")
print("="*80)
print()

# Test 1: Check Python version
print("1. Python Version:")
print(f"   {sys.version}")
print(f"   Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print()

# Test 2: Check all required imports
print("2. Required Dependencies:")
required_modules = [
    'fastapi',
    'uvicorn',
    'openpyxl',
    'pytesseract',
    'PIL',
    'cv2',
    'pyzbar.pyzbar',
    'pdf2image',
    'webview',
    'requests',
    'dotenv',
    'fuzzywuzzy',
]

all_imports_ok = True
for module in required_modules:
    try:
        __import__(module)
        print(f"   ✅ {module}")
    except ImportError as e:
        print(f"   ❌ {module} - {e}")
        all_imports_ok = False

print()

# Test 3: Check Tesseract installation
print("3. Tesseract OCR:")
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_path):
    print(f"   ✅ Found at: {tesseract_path}")
else:
    print(f"   ❌ NOT FOUND at: {tesseract_path}")
    all_imports_ok = False
print()

# Test 4: Check Poppler
print("4. Poppler (PDF to Image):")
poppler_path = os.path.join(os.path.dirname(__file__), 'poppler', 'poppler-24.08.0', 'Library', 'bin')
if os.path.exists(poppler_path):
    print(f"   ✅ Found at: {poppler_path}")
    # Check for key DLLs
    key_files = ['pdftoppm.exe', 'pdftocairo.exe']
    for f in key_files:
        fpath = os.path.join(poppler_path, f)
        if os.path.exists(fpath):
            print(f"      ✅ {f}")
        else:
            print(f"      ❌ {f} missing")
else:
    print(f"   ❌ NOT FOUND at: {poppler_path}")
    all_imports_ok = False
print()

# Test 5: Check frontend files
print("5. Frontend Files:")
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.exists(frontend_path):
    print(f"   ✅ Found at: {frontend_path}")
    html_file = os.path.join(frontend_path, 'index.html')
    if os.path.exists(html_file):
        print(f"      ✅ index.html")
    else:
        print(f"      ❌ index.html missing")
else:
    print(f"   ❌ NOT FOUND at: {frontend_path}")
    all_imports_ok = False
print()

# Test 6: Try to import desktop.py
print("6. Desktop Module:")
try:
    import desktop
    print("   ✅ desktop.py can be imported")
except ImportError as e:
    print(f"   ❌ desktop.py import error: {e}")
    all_imports_ok = False
except Exception as e:
    print(f"   ⚠️  desktop.py import warning: {e}")
print()

# Test 7: Try to import app.py
print("7. FastAPI App:")
try:
    from app import app as fastapi_app
    print("   ✅ app.py can be imported")
    print(f"   ✅ FastAPI app object: {fastapi_app}")
except ImportError as e:
    print(f"   ❌ app.py import error: {e}")
    all_imports_ok = False
except Exception as e:
    print(f"   ⚠️  app.py import warning: {e}")
print()

# Test 8: Check PyInstaller
print("8. PyInstaller:")
try:
    import PyInstaller
    print(f"   ✅ PyInstaller version: {PyInstaller.__version__}")
    
    # Check spec file
    spec_file = os.path.join(os.path.dirname(__file__), 'CertifyAI.spec')
    if os.path.exists(spec_file):
        print(f"   ✅ CertifyAI.spec exists")
    else:
        print(f"   ❌ CertifyAI.spec missing")
        all_imports_ok = False
except ImportError:
    print("   ❌ PyInstaller not installed")
    all_imports_ok = False
print()

# Test 9: Check app/core modules (from Task 1)
print("9. Task 1 Cache Modules:")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
    from core.cache import ImageCache, ResultCache
    from core.utils import compute_certificate_hash, preprocess_image
    print("   ✅ ImageCache")
    print("   ✅ ResultCache")
    print("   ✅ compute_certificate_hash")
    print("   ✅ preprocess_image")
except ImportError as e:
    print(f"   ❌ Cache modules import error: {e}")
except Exception as e:
    print(f"   ⚠️  Cache modules warning: {e}")
print()

# Final Summary
print("="*80)
print("SUMMARY")
print("="*80)
if all_imports_ok:
    print("✅ All checks passed! Desktop app should build successfully.")
else:
    print("❌ Some checks failed. Fix the issues above before building.")
print()
