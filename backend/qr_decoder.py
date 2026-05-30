import cv2
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
import numpy as np
import json
import os
import sys

if sys.platform == 'win32':
    POPPLER_PATH = os.path.join(os.path.dirname(__file__), 'poppler', 'poppler-24.08.0', 'Library', 'bin')
else:
    POPPLER_PATH = None  # auto-detected on Linux

def decode_qr(image_path):
    # Handle PDF
    if image_path.lower().endswith('.pdf'):
        pages = convert_from_path(image_path, dpi=200, poppler_path=POPPLER_PATH)
        pil_image = pages[0]
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    else:
        image = cv2.imread(image_path)

    if image is None:
        return None

    qr_codes = decode(image)

    if not qr_codes:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        qr_codes = decode(gray)

    if not qr_codes:
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        qr_codes = decode(thresh)

    if not qr_codes:
        return None

    raw_data = qr_codes[0].data.decode('utf-8')

    try:
        qr_json = json.loads(raw_data)
        credential = qr_json.get('credentialSubject', {})

        extracted = {
            'name': credential.get('issuedTo', None),
            'course': credential.get('course', None),
            'date': credential.get('completedOn', None),
            'issued_by': credential.get('issuedBy', None) or credential.get('issuer', None)
        }

        return extracted

    except json.JSONDecodeError:
        return None