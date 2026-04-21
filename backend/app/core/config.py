"""
Configuration settings for the Certificate Verification System
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    MONGODB_URL: str
    DATABASE_NAME: str = "certificate_verification"
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_URL: str
    
    # Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 3600
    ENCRYPTION_KEY: str
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://localhost:3000"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    MAX_BATCH_SIZE: int = 100
    
    # AI/ML Configuration
    TESSERACT_PATH: str = "/usr/bin/tesseract"
    OPENCV_DATA_PATH: str = "/usr/share/opencv4/haarcascades"
    OCR_CONFIDENCE_THRESHOLD: int = 60
    FRAUD_DETECTION_THRESHOLD: float = 0.7
    
    # Platform APIs
    COURSERA_API_KEY: str = ""
    EDX_API_KEY: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()