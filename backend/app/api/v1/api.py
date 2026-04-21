"""
Main API router for version 1
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, certificates, upload, verification, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(certificates.router, prefix="/certificates", tags=["certificates"])
api_router.include_router(verification.router, prefix="/verification", tags=["verification"])