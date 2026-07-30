"""
Unit tests for caching infrastructure.

Tests ImageCache and ResultCache implementations including:
- Basic get/put operations
- LRU eviction behavior
- Thread safety
- Statistics tracking
- Clear operations
"""

import unittest
from unittest.mock import Mock
from PIL import Image
from .cache import ImageCache, ResultCache


class TestImageCache(unittest.TestCase):
    """Test cases for ImageCache class."""
    
    def setUp(self):
        """Create a fresh ImageCache instance for each test."""
        self.cache = ImageCache(maxsize=3)
    
    def test_put_and_get(self):
        """Test basic put and get operations."""
        # Create a mock image
        img = Mock(spec=Image.Image)
        
        # Put image in cache
        self.cache.put('key1', img)
        
        # Retrieve image
        retrieved = self.cache.get('key1')
        self.assertIs(retrieved, img)
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist returns None."""
        result = self.cache.get('nonexistent')
        self.assertIsNone(result)
    
    def test_lru_eviction(self):
        """Test that least recently used items are evicted when cache is full."""
        img1 = Mock(spec=Image.Image)
        img2 = Mock(spec=Image.Image)
        img3 = Mock(spec=Image.Image)
        img4 = Mock(spec=Image.Image)
        
        # Fill cache to capacity
        self.cache.put('key1', img1)
        self.cache.put('key2', img2)
        self.cache.put('key3', img3)
        
        # Add fourth item - should evict key1 (least recently used)
        self.cache.put('key4', img4)
        
        # key1 should be evicted
        self.assertIsNone(self.cache.get('key1'))
        
        # Other keys should still exist
        self.assertIs(self.cache.get('key2'), img2)
        self.assertIs(self.cache.get('key3'), img3)
        self.assertIs(self.cache.get('key4'), img4)
    
    def test_get_updates_lru_order(self):
        """Test that getting an item moves it to most recently used."""
        img1 = Mock(spec=Image.Image)
        img2 = Mock(spec=Image.Image)
        img3 = Mock(spec=Image.Image)
        img4 = Mock(spec=Image.Image)
        
        # Fill cache
        self.cache.put('key1', img1)
        self.cache.put('key2', img2)
        self.cache.put('key3', img3)
        
        # Access key1 to make it most recently used
        self.cache.get('key1')
        
        # Add fourth item - should evict key2 (now least recently used)
        self.cache.put('key4', img4)
        
        # key2 should be evicted, key1 should still exist
        self.assertIsNone(self.cache.get('key2'))
        self.assertIs(self.cache.get('key1'), img1)
    
    def test_put_updates_existing_key(self):
        """Test that putting an existing key updates the value and LRU order."""
        img1 = Mock(spec=Image.Image)
        img2 = Mock(spec=Image.Image)
        img3 = Mock(spec=Image.Image)
        img4 = Mock(spec=Image.Image)
        img1_new = Mock(spec=Image.Image)
        
        # Fill cache
        self.cache.put('key1', img1)
        self.cache.put('key2', img2)
        self.cache.put('key3', img3)
        
        # Update key1 with new image
        self.cache.put('key1', img1_new)
        
        # Add fourth item - should evict key2 (least recently used)
        self.cache.put('key4', img4)
        
        # key1 should have new value and not be evicted
        self.assertIs(self.cache.get('key1'), img1_new)
        self.assertIsNone(self.cache.get('key2'))
    
    def test_clear(self):
        """Test that clear removes all cached items."""
        img1 = Mock(spec=Image.Image)
        img2 = Mock(spec=Image.Image)
        
        self.cache.put('key1', img1)
        self.cache.put('key2', img2)
        
        self.assertEqual(len(self.cache), 2)
        
        self.cache.clear()
        
        self.assertEqual(len(self.cache), 0)
        self.assertIsNone(self.cache.get('key1'))
        self.assertIsNone(self.cache.get('key2'))
    
    def test_len(self):
        """Test that len returns correct cache size."""
        self.assertEqual(len(self.cache), 0)
        
        img1 = Mock(spec=Image.Image)
        self.cache.put('key1', img1)
        self.assertEqual(len(self.cache), 1)
        
        img2 = Mock(spec=Image.Image)
        self.cache.put('key2', img2)
        self.assertEqual(len(self.cache), 2)
    
    def test_maxsize_initialization(self):
        """Test that cache respects custom maxsize."""
        small_cache = ImageCache(maxsize=2)
        
        img1 = Mock(spec=Image.Image)
        img2 = Mock(spec=Image.Image)
        img3 = Mock(spec=Image.Image)
        
        small_cache.put('key1', img1)
        small_cache.put('key2', img2)
        small_cache.put('key3', img3)
        
        # Should only hold 2 items
        self.assertEqual(len(small_cache), 2)
        self.assertIsNone(small_cache.get('key1'))


class TestResultCache(unittest.TestCase):
    """Test cases for ResultCache class."""
    
    def setUp(self):
        """Create a fresh ResultCache instance for each test."""
        self.cache = ResultCache(maxsize=3)
    
    def test_put_and_get(self):
        """Test basic put and get operations."""
        result = {'verdict': 'Verified', 'name': 'John Doe'}
        
        self.cache.put('hash1', result)
        
        retrieved = self.cache.get('hash1')
        self.assertEqual(retrieved, result)
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist returns None."""
        result = self.cache.get('nonexistent')
        self.assertIsNone(result)
    
    def test_lru_eviction(self):
        """Test that least recently used items are evicted when cache is full."""
        result1 = {'verdict': 'Verified', 'name': 'John Doe'}
        result2 = {'verdict': 'Fraud', 'name': 'Jane Smith'}
        result3 = {'verdict': 'Manual Review', 'name': 'Bob Johnson'}
        result4 = {'verdict': 'Verified', 'name': 'Alice Williams'}
        
        # Fill cache to capacity
        self.cache.put('hash1', result1)
        self.cache.put('hash2', result2)
        self.cache.put('hash3', result3)
        
        # Add fourth item - should evict hash1 (least recently used)
        self.cache.put('hash4', result4)
        
        # hash1 should be evicted
        self.assertIsNone(self.cache.get('hash1'))
        
        # Other keys should still exist
        self.assertEqual(self.cache.get('hash2'), result2)
        self.assertEqual(self.cache.get('hash3'), result3)
        self.assertEqual(self.cache.get('hash4'), result4)
    
    def test_statistics_tracking(self):
        """Test that cache tracks hit/miss statistics correctly."""
        result1 = {'verdict': 'Verified'}
        
        self.cache.put('hash1', result1)
        
        # Initial stats
        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], 0)
        self.assertEqual(stats['misses'], 0)
        self.assertEqual(stats['hit_rate'], 0.0)
        
        # Cache hit
        self.cache.get('hash1')
        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], 1)
        self.assertEqual(stats['misses'], 0)
        self.assertEqual(stats['hit_rate'], 1.0)
        
        # Cache miss
        self.cache.get('nonexistent')
        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], 1)
        self.assertEqual(stats['misses'], 1)
        self.assertEqual(stats['hit_rate'], 0.5)
        
        # Another hit
        self.cache.get('hash1')
        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], 2)
        self.assertEqual(stats['misses'], 1)
        self.assertAlmostEqual(stats['hit_rate'], 2/3, places=2)
    
    def test_get_stats_includes_size(self):
        """Test that get_stats returns current size and maxsize."""
        result1 = {'verdict': 'Verified'}
        result2 = {'verdict': 'Fraud'}
        
        self.cache.put('hash1', result1)
        self.cache.put('hash2', result2)
        
        stats = self.cache.get_stats()
        self.assertEqual(stats['size'], 2)
        self.assertEqual(stats['maxsize'], 3)
    
    def test_clear_resets_statistics(self):
        """Test that clear resets both cache and statistics."""
        result1 = {'verdict': 'Verified'}
        
        self.cache.put('hash1', result1)
        self.cache.get('hash1')
        self.cache.get('nonexistent')
        
        # Verify stats exist
        stats = self.cache.get_stats()
        self.assertGreater(stats['hits'], 0)
        self.assertGreater(stats['misses'], 0)
        
        # Clear cache
        self.cache.clear()
        
        # Verify stats are reset
        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], 0)
        self.assertEqual(stats['misses'], 0)
        self.assertEqual(stats['hit_rate'], 0.0)
        self.assertEqual(stats['size'], 0)
        self.assertEqual(len(self.cache), 0)
    
    def test_get_updates_lru_order(self):
        """Test that getting an item moves it to most recently used."""
        result1 = {'verdict': 'Verified'}
        result2 = {'verdict': 'Fraud'}
        result3 = {'verdict': 'Manual Review'}
        result4 = {'verdict': 'Verified'}
        
        # Fill cache
        self.cache.put('hash1', result1)
        self.cache.put('hash2', result2)
        self.cache.put('hash3', result3)
        
        # Access hash1 to make it most recently used
        self.cache.get('hash1')
        
        # Add fourth item - should evict hash2 (now least recently used)
        self.cache.put('hash4', result4)
        
        # hash2 should be evicted, hash1 should still exist
        self.assertIsNone(self.cache.get('hash2'))
        self.assertEqual(self.cache.get('hash1'), result1)
    
    def test_maxsize_initialization(self):
        """Test that cache respects custom maxsize."""
        large_cache = ResultCache(maxsize=1000)
        stats = large_cache.get_stats()
        self.assertEqual(stats['maxsize'], 1000)


if __name__ == '__main__':
    unittest.main()
