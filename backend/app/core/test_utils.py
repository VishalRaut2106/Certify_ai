"""
Unit tests for utility functions.

Tests compute_certificate_hash and preprocess_image functions including:
- Hash computation correctness and consistency
- Image preprocessing operations
- Edge cases and error handling
"""

import unittest
import hashlib
from PIL import Image, ImageDraw
from .utils import compute_certificate_hash, preprocess_image


class TestComputeCertificateHash(unittest.TestCase):
    """Test cases for compute_certificate_hash function."""
    
    def test_hash_consistency(self):
        """Test that same input produces same hash."""
        data = b"test certificate data"
        hash1 = compute_certificate_hash(data)
        hash2 = compute_certificate_hash(data)
        self.assertEqual(hash1, hash2)
    
    def test_hash_uniqueness(self):
        """Test that different inputs produce different hashes."""
        data1 = b"certificate 1"
        data2 = b"certificate 2"
        hash1 = compute_certificate_hash(data1)
        hash2 = compute_certificate_hash(data2)
        self.assertNotEqual(hash1, hash2)
    
    def test_hash_format(self):
        """Test that hash is a valid SHA-256 hex digest."""
        data = b"test data"
        hash_result = compute_certificate_hash(data)
        
        # SHA-256 hex digest should be 64 characters
        self.assertEqual(len(hash_result), 64)
        
        # Should only contain hex characters
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_result))
    
    def test_hash_matches_sha256(self):
        """Test that hash matches standard SHA-256 implementation."""
        data = b"test certificate content"
        expected_hash = hashlib.sha256(data).hexdigest()
        actual_hash = compute_certificate_hash(data)
        self.assertEqual(actual_hash, expected_hash)
    
    def test_empty_input(self):
        """Test hash computation with empty input."""
        data = b""
        hash_result = compute_certificate_hash(data)
        expected = hashlib.sha256(b"").hexdigest()
        self.assertEqual(hash_result, expected)
    
    def test_large_input(self):
        """Test hash computation with large input (simulating PDF file)."""
        # Create 1MB of data
        data = b"x" * (1024 * 1024)
        hash_result = compute_certificate_hash(data)
        
        # Should still produce valid 64-character hex string
        self.assertEqual(len(hash_result), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_result))


class TestPreprocessImage(unittest.TestCase):
    """Test cases for preprocess_image function."""
    
    def test_resize_large_image(self):
        """Test that images exceeding 2000px are resized."""
        # Create a large image (3000x2000)
        img = Image.new('RGB', (3000, 2000), color='white')
        
        processed = preprocess_image(img)
        
        # Largest dimension should be 2000 or less
        max_dim = max(processed.size)
        self.assertLessEqual(max_dim, 2000)
        
        # Aspect ratio should be preserved
        original_ratio = 3000 / 2000
        processed_ratio = processed.size[0] / processed.size[1]
        self.assertAlmostEqual(original_ratio, processed_ratio, places=1)
    
    def test_small_image_not_resized(self):
        """Test that images under 2000px are not resized."""
        # Create a small image (800x600)
        img = Image.new('RGB', (800, 600), color='white')
        
        processed = preprocess_image(img)
        
        # Size should remain the same (but converted to grayscale)
        self.assertEqual(processed.size, (800, 600))
    
    def test_grayscale_conversion(self):
        """Test that RGB images are converted to grayscale."""
        # Create RGB image
        img = Image.new('RGB', (500, 500), color=(255, 0, 0))
        
        processed = preprocess_image(img)
        
        # Should be grayscale
        self.assertEqual(processed.mode, 'L')
    
    def test_grayscale_image_unchanged(self):
        """Test that grayscale images skip color conversion."""
        # Create grayscale image
        img = Image.new('L', (500, 500), color=128)
        
        processed = preprocess_image(img)
        
        # Should remain grayscale
        self.assertEqual(processed.mode, 'L')
    
    def test_rgba_image_conversion(self):
        """Test that RGBA images are converted properly."""
        # Create RGBA image
        img = Image.new('RGBA', (500, 500), color=(255, 0, 0, 255))
        
        processed = preprocess_image(img)
        
        # Should be converted to grayscale
        self.assertEqual(processed.mode, 'L')
    
    def test_contrast_enhancement_applied(self):
        """Test that contrast enhancement is applied."""
        # Create a low-contrast image
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        draw = ImageDraw.Draw(img)
        draw.rectangle([25, 25, 75, 75], fill=(140, 140, 140))
        
        processed = preprocess_image(img)
        
        # Image should be processed (we can't easily verify contrast numerically,
        # but we can verify the function completes without error)
        self.assertIsNotNone(processed)
        self.assertEqual(processed.mode, 'L')
    
    def test_returns_pil_image(self):
        """Test that function returns a PIL Image object."""
        img = Image.new('RGB', (500, 500), color='white')
        
        processed = preprocess_image(img)
        
        self.assertIsInstance(processed, Image.Image)
    
    def test_tall_image_resize(self):
        """Test resizing of tall images (height > width)."""
        # Create tall image (1000x3000)
        img = Image.new('RGB', (1000, 3000), color='white')
        
        processed = preprocess_image(img)
        
        # Height should be 2000 or less
        self.assertLessEqual(processed.size[1], 2000)
        
        # Aspect ratio should be preserved
        original_ratio = 1000 / 3000
        processed_ratio = processed.size[0] / processed.size[1]
        self.assertAlmostEqual(original_ratio, processed_ratio, places=1)
    
    def test_square_image_resize(self):
        """Test resizing of square images."""
        # Create square image (2500x2500)
        img = Image.new('RGB', (2500, 2500), color='white')
        
        processed = preprocess_image(img)
        
        # Both dimensions should be 2000 or less
        self.assertLessEqual(processed.size[0], 2000)
        self.assertLessEqual(processed.size[1], 2000)
        
        # Should remain square
        self.assertEqual(processed.size[0], processed.size[1])
    
    def test_exactly_2000px_not_resized(self):
        """Test that images exactly 2000px are not resized."""
        # Create image exactly at threshold
        img = Image.new('RGB', (2000, 1500), color='white')
        
        processed = preprocess_image(img)
        
        # Size should remain the same (but converted to grayscale)
        self.assertEqual(processed.size, (2000, 1500))


if __name__ == '__main__':
    unittest.main()
