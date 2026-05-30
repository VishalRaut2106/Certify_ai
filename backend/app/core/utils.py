"""
Shared utility functions for certificate verification system.

This module provides utilities for certificate hashing and image preprocessing
to support caching and optimization of bulk processing.
"""

import hashlib
from PIL import Image, ImageEnhance, ImageFilter
from typing import Union


def compute_certificate_hash(file_bytes: bytes) -> str:
    """
    Compute SHA-256 hash of certificate file content.
    
    Used as a unique identifier for caching verification results.
    Identical certificates will produce the same hash, enabling
    duplicate detection and result reuse.
    
    Args:
        file_bytes: Raw bytes of the certificate file (PDF or image)
        
    Returns:
        Hexadecimal string representation of SHA-256 hash
        
    Example:
        >>> with open('certificate.pdf', 'rb') as f:
        ...     cert_hash = compute_certificate_hash(f.read())
        >>> print(cert_hash)
        'a3b2c1d4e5f6...'
    """
    return hashlib.sha256(file_bytes).hexdigest()


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for optimal OCR and QR decoding performance.
    
    Applies the following optimizations in a single pass:
    - Resizes images exceeding 2000px in largest dimension
    - Converts to grayscale (unless already grayscale)
    - Applies contrast enhancement (1.4x)
    - Applies sharpening filter
    
    These preprocessing steps improve OCR accuracy and reduce processing time
    by normalizing image size and enhancing text clarity.
    
    Args:
        image: PIL Image object to preprocess
        
    Returns:
        Preprocessed PIL Image object ready for OCR/QR processing
        
    Example:
        >>> from PIL import Image
        >>> img = Image.open('certificate.jpg')
        >>> processed = preprocess_image(img)
        >>> # Use processed image for OCR or QR decoding
    """
    # Convert to RGB if needed (handles RGBA, CMYK, etc.)
    if image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')
    
    # Resize if too large - no accuracy gain beyond 2000px
    # Requirement 6.1: Resize images exceeding 2000 pixels
    width, height = image.size
    max_dimension = max(width, height)
    
    if max_dimension > 2000:
        scale = 2000 / max_dimension
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Skip color conversion if already grayscale
    # Requirement 6.3: Skip color conversion for grayscale images
    if image.mode != 'L':
        image = image.convert('L')
    
    # Apply contrast enhancement and sharpening in single pass
    # Requirement 6.2: Apply contrast enhancement and sharpening in single pass
    image = ImageEnhance.Contrast(image).enhance(1.4)
    image = image.filter(ImageFilter.SHARPEN)
    
    return image
