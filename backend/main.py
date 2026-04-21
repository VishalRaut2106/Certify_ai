"""
AI-Powered Bulk Certificate Verification System
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection, is_using_fallback
from app.api.v1.api import api_router
from app.services.background_tasks import task_processor

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await connect_to_mongo()
    await task_processor.start_processor()
    print("🚀 Certificate Verification System started successfully!")
    print("🤖 AI Verification Service is running!")
    yield
    # Shutdown
    await task_processor.stop_processor()
    await close_mongo_connection()
    print("📋 Certificate Verification System shutdown complete!")
    print("[OK] Certificate Verification System shutdown complete!")

# Create FastAPI application
app = FastAPI(
    title="AI-Powered Certificate Verification System",
    description="Bulk certificate verification with AI-powered fraud detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure properly for production
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "AI-Powered Certificate Verification System",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "features": [
            "Bulk certificate upload",
            "Multi-layer AI verification",
            "Fraud detection",
            "Trust scoring",
            "Real-time processing"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }

@app.get("/api/v1/system/status")
async def system_status():
    """System status endpoint with database information"""
    database_type = "SQLite (Development)" if is_using_fallback() else "MongoDB Atlas"
    database_status = "connected"
    
    return {
        "status": "operational",
        "database": {
            "type": database_type,
            "status": database_status,
            "is_fallback": is_using_fallback()
        },
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "message": "SQLite fallback active - perfect for development!" if is_using_fallback() else "Connected to MongoDB Atlas"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )