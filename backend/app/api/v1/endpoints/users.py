"""
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime

from app.models.user import UserResponse
from app.api.v1.endpoints.auth import get_current_user
from app.core.database import get_database

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user["role"],
        institution_name=current_user.get("institution_name"),
        is_active=current_user.get("is_active", True),
        is_verified=current_user.get("is_verified", False),
        created_at=datetime.fromisoformat(current_user["created_at"]) if isinstance(current_user["created_at"], str) else current_user["created_at"],
        last_login=datetime.fromisoformat(current_user["last_login"]) if current_user.get("last_login") and isinstance(current_user["last_login"], str) else current_user.get("last_login"),
        certificates_uploaded=current_user.get("certificates_uploaded", 0),
        verifications_performed=current_user.get("verifications_performed", 0)
    )

@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update current user profile"""
    db = get_database()
    
    # Update user data
    if user_update:
        await db.users.update_one(
            {"id": current_user["id"]},
            {"$set": user_update}
        )
    
    # Get updated user
    updated_user = await db.users.find_one({"id": current_user["id"]})
    return UserResponse(
        id=updated_user["id"],
        email=updated_user["email"],
        full_name=updated_user["full_name"],
        role=updated_user["role"],
        institution_name=updated_user.get("institution_name"),
        is_active=updated_user.get("is_active", True),
        is_verified=updated_user.get("is_verified", False),
        created_at=datetime.fromisoformat(updated_user["created_at"]) if isinstance(updated_user["created_at"], str) else updated_user["created_at"],
        last_login=datetime.fromisoformat(updated_user["last_login"]) if updated_user.get("last_login") and isinstance(updated_user["last_login"], str) else updated_user.get("last_login"),
        certificates_uploaded=updated_user.get("certificates_uploaded", 0),
        verifications_performed=updated_user.get("verifications_performed", 0)
    )

@router.get("/stats")
async def get_user_statistics(current_user: dict = Depends(get_current_user)):
    """Get user statistics"""
    db = get_database()
    
    # Get certificate counts
    total_certificates = await db.certificates.count_documents({"user_id": current_user["id"]})
    verified_certificates = await db.certificates.count_documents({
        "user_id": current_user["id"],
        "verification_status": "valid"
    })
    pending_certificates = await db.certificates.count_documents({
        "user_id": current_user["id"],
        "verification_status": "pending"
    })
    
    return {
        "total_certificates": total_certificates,
        "verified_certificates": verified_certificates,
        "pending_certificates": pending_certificates,
        "verification_rate": (verified_certificates / total_certificates * 100) if total_certificates > 0 else 0
    }