import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pdf2image import convert_from_path
import re
import os
import sys

# --- Resolve paths: dev, frozen .exe, or Linux/Docker ---
if getattr(sys, 'frozen', False):
    # PyInstaller bundle — binaries extracted to sys._MEIPASS
    _BASE = sys._MEIPASS
    pytesseract.pytesseract.tesseract_cmd = os.path.join(_BASE, 'tesseract', 'tesseract.exe')
    os.environ['TESSDATA_PREFIX'] = os.path.join(_BASE, 'tesseract', 'tessdata')
    POPPLER_PATH = os.path.join(_BASE, 'poppler', 'bin')
elif sys.platform == 'win32':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
    POPPLER_PATH = os.path.join(os.path.dirname(__file__), 'poppler', 'poppler-24.08.0', 'Library', 'bin')
else:
    # Linux (Docker / Cloud Run) — installed via apt-get
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
    POPPLER_PATH = None  # pdf2image auto-detects on Linux

# Faster Tesseract config: PSM 3 = fully automatic, OEM 1 = LSTM only (faster)
TESS_CONFIG = '--oem 1 --psm 3'

# Max dimension for images before OCR (larger = slower, no accuracy gain beyond this)
MAX_OCR_DIM = 2000

date_pattern = re.compile(
    r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*\d{4}'
)

def _prepare_image(image: Image.Image) -> Image.Image:
    """Resize oversized images and convert to greyscale for faster OCR."""
    # Convert to RGB if needed
    if image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')

    # Resize if too large — no accuracy gain past ~2000px wide
    w, h = image.size
    if max(w, h) > MAX_OCR_DIM:
        scale = MAX_OCR_DIM / max(w, h)
        image = image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # Greyscale + slight sharpening helps Tesseract
    image = image.convert('L')
    image = ImageEnhance.Contrast(image).enhance(1.4)
    image = image.filter(ImageFilter.SHARPEN)
    return image

def extract_text(image_path):
    image = None
    raw_text = ""
    try:
        if image_path.lower().endswith('.pdf'):
            # DPI 150 is sufficient for most certs and ~40% faster than 200
            pages = convert_from_path(image_path, dpi=150, poppler_path=POPPLER_PATH)
            image = pages[0]
        else:
            image = Image.open(image_path)
            image.load()

        image = _prepare_image(image)
        raw_text = pytesseract.image_to_string(image, lang='eng', config=TESS_CONFIG)
    except Exception as e:
        print(f"OCR Error on {image_path}: {e}")
    finally:
        if image and hasattr(image, 'close'):
            try:
                image.close()
            except:
                pass

    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

    extracted = {'name': None, 'course': None, 'date': None, 'issued_by': None, 'raw_text': raw_text}

    for i, line in enumerate(lines):
        lower = line.lower()

        if 'awarded to' in lower or 'certificate is awarded to' in lower:
            if i + 1 < len(lines):
                extracted['name'] = lines[i + 1]

        if 'completing the course' in lower:
            if i + 1 < len(lines):
                extracted['course'] = lines[i + 1]

        # Check line starting with "on" for date
        if lower.startswith('on '):
            match = date_pattern.search(line)
            if match:
                extracted['date'] = match.group(0)
        elif date_pattern.search(line):
            match = date_pattern.search(line)
            extracted['date'] = match.group(0)

        # Look for Issued By
        if 'issued by' in lower or 'issuer' in lower:
            if i + 1 < len(lines):
                extracted['issued_by'] = lines[i + 1]

    return extracted