"""
Caching infrastructure for certificate verification system.

This module provides in-memory caching for PDF images and verification results
to optimize bulk certificate processing performance.
"""

from collections import OrderedDict
from threading import Lock
from typing import Any, Optional
from PIL import Image


class ImageCache:
    """
    LRU cache for converted PDF images.
    
    Stores PIL Image objects in memory to avoid redundant PDF-to-image conversions.
    Uses LRU eviction policy when cache reaches maximum size.
    
    Thread-safe implementation using locks for concurrent access.
    """
    
    def __init__(self, maxsize: int = 100):
        """
        Initialize ImageCache with specified maximum size.
        
        Args:
            maxsize: Maximum number of images to store (default: 100)
        """
        self._cache: OrderedDict[str, Image.Image] = OrderedDict()
        self._maxsize = maxsize
        self._lock = Lock()
    
    def get(self, key: str) -> Optional[Image.Image]:
        """
        Retrieve an image from cache.
        
        Args:
            key: Cache key (typically certificate filename or hash)
            
        Returns:
            PIL Image object if found, None otherwise
        """
        with self._lock:
            if key in self._cache:
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                return self._cache[key]
            return None
    
    def put(self, key: str, image: Image.Image) -> None:
        """
        Store an image in cache.
        
        If cache is at maximum size, evicts least recently used image.
        
        Args:
            key: Cache key (typically certificate filename or hash)
            image: PIL Image object to cache
        """
        with self._lock:
            if key in self._cache:
                # Update existing entry and move to end
                self._cache.move_to_end(key)
            else:
                # Add new entry
                if len(self._cache) >= self._maxsize:
                    # Evict least recently used (first item)
                    self._cache.popitem(last=False)
            self._cache[key] = image
    
    def clear(self) -> None:
        """
        Clear all cached images.
        
        Useful for freeing memory after batch processing completes.
        """
        with self._lock:
            self._cache.clear()
    
    def __len__(self) -> int:
        """Return current number of cached images."""
        with self._lock:
            return len(self._cache)


class ResultCache:
    """
    LRU cache for verification results indexed by certificate hash.
    
    Stores verification results to avoid reprocessing duplicate certificates.
    Uses LRU eviction policy when cache reaches maximum size.
    
    Thread-safe implementation using locks for concurrent access.
    Tracks cache hit/miss statistics for performance monitoring.
    """
    
    def __init__(self, maxsize: int = 1000):
        """
        Initialize ResultCache with specified maximum size.
        
        Args:
            maxsize: Maximum number of results to store (default: 1000)
        """
        self._cache: OrderedDict[str, dict] = OrderedDict()
        self._maxsize = maxsize
        self._lock = Lock()
        self._hits = 0
        self._misses = 0
    
    def get(self, hash_key: str) -> Optional[dict]:
        """
        Retrieve a verification result from cache.
        
        Args:
            hash_key: Certificate hash (SHA-256 hex digest)
            
        Returns:
            Verification result dictionary if found, None otherwise
        """
        with self._lock:
            if hash_key in self._cache:
                # Move to end (most recently used)
                self._cache.move_to_end(hash_key)
                self._hits += 1
                return self._cache[hash_key]
            self._misses += 1
            return None
    
    def put(self, hash_key: str, result: dict) -> None:
        """
        Store a verification result in cache.
        
        If cache is at maximum size, evicts least recently used result.
        
        Args:
            hash_key: Certificate hash (SHA-256 hex digest)
            result: Verification result dictionary
        """
        with self._lock:
            if hash_key in self._cache:
                # Update existing entry and move to end
                self._cache.move_to_end(hash_key)
            else:
                # Add new entry
                if len(self._cache) >= self._maxsize:
                    # Evict least recently used (first item)
                    self._cache.popitem(last=False)
            self._cache[hash_key] = result
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary containing:
                - hits: Number of cache hits
                - misses: Number of cache misses
                - hit_rate: Cache hit rate (0.0 to 1.0)
                - size: Current number of cached results
                - maxsize: Maximum cache size
        """
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0.0
            return {
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': hit_rate,
                'size': len(self._cache),
                'maxsize': self._maxsize
            }
    
    def clear(self) -> None:
        """
        Clear all cached results and reset statistics.
        """
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def __len__(self) -> int:
        """Return current number of cached results."""
        with self._lock:
            return len(self._cache)
