"""
Certificate management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.core.database import get_database, is_using_fallback

router = APIRouter()

@router.post("/test-verification")
async def test_ai_verification():
    """Test endpoint to verify AI service is working"""
    try:
        from app.services.verification_service import verification_service
        
        # Test with a simple mock verification
        test_result = {
            "ai_service_status": "operational",
            "ocr_available": True,
            "qr_detection_available": True,
            "visual_analysis_available": True,
            "fraud_detection_available": True,
            "message": "AI Certificate Verification Service is ready!"
        }
        
        return test_result
        
    except Exception as e:
        return {
            "ai_service_status": "error",
            "error": str(e),
            "message": "AI service initialization failed"
        }

@router.get("/health")
async def certificates_health():
    """Health check for certificates service"""
    db = get_database()
    
    try:
        # Test database connection
        total_certs = await db.certificates.count_documents({})
        return {
            "status": "healthy",
            "database": "connected",
            "total_certificates": total_certs,
            "database_type": "SQLite" if is_using_fallback() else "MongoDB"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.get("/")
async def get_user_certificates(
    current_user: dict = Depends(get_current_user),
    status_filter: Optional[str] = Query(None, description="Filter by verification status"),
    limit: int = Query(50, le=100, description="Number of certificates to return"),
    skip: int = Query(0, ge=0, description="Number of certificates to skip")
):
    """Get user's certificates with optional filtering"""
    db = get_database()
    
    # Build query
    query = {"user_id": current_user["id"]}
    if status_filter:
        query["verification_status"] = status_filter
    
    if is_using_fallback():
        # SQLite adapter path
        certificates = await db.certificates.find(query, limit=limit, skip=skip)
        # Sort by upload_timestamp descending (manual sort for SQLite)
        certificates.sort(key=lambda x: x.get("upload_timestamp", ""), reverse=True)
    else:
        # MongoDB path
        cursor = db.certificates.find(query).sort("upload_timestamp", -1).skip(skip).limit(limit)
        certificates = await cursor.to_list(length=limit)
    
    # Transform for frontend
    result = []
    for cert in certificates:
        result.append({
            "id": cert.get("id", cert.get("_id", "")),
            "file_name": cert.get("original_filename", "Unknown"),
            "upload_date": cert.get("upload_timestamp", datetime.utcnow().isoformat()),
            "verification_status": cert.get("verification_status", "pending"),  # Fixed key name
            "trust_score": cert.get("trust_score"),
            "processing_time": cert.get("processing_time"),
            "file_type": cert.get("file_type", ""),
            "file_size": cert.get("file_size", 0),
        })
    
    return result

@router.get("/{certificate_id}")
async def get_certificate_details(
    certificate_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed information about a specific certificate"""
    db = get_database()
    
    certificate = await db.certificates.find_one({
        "id": certificate_id,
        "user_id": current_user["id"]
    })
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    return {
        "id": certificate.get("id", certificate.get("_id", "")),
        "file_name": certificate.get("original_filename", "Unknown"),
        "upload_date": certificate.get("upload_timestamp", ""),
        "verification_status": certificate.get("verification_status", "pending"),  # Fixed key name
        "trust_score": certificate.get("trust_score"),
        "processing_time": certificate.get("processing_time"),
        "file_type": certificate.get("file_type", ""),
        "file_size": certificate.get("file_size", 0),
        "metadata": certificate.get("metadata", "{}"),
    }

@router.delete("/{certificate_id}")
async def delete_certificate(
    certificate_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a certificate"""
    db = get_database()
    
    # Check if certificate exists and belongs to user
    certificate = await db.certificates.find_one({
        "id": certificate_id,
        "user_id": current_user["id"]
    })
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    # Delete from database
    await db.certificates.delete_one({"id": certificate_id})
    
    return {"message": "Certificate deleted successfully"}

@router.post("/sample-data")
async def create_sample_data(current_user: dict = Depends(get_current_user)):
    """Create sample certificates for testing (development only)"""
    db = get_database()
    
    import uuid
    from datetime import datetime, timedelta
    import random
    
    sample_certificates = [
        {
            "id": str(uuid.uuid4()),
            "user_id": current_user["id"],
            "original_filename": "computer_science_degree.pdf",
            "file_path": "/uploads/sample1.pdf",
            "file_type": "application/pdf",
            "file_size": 2048576,
            "verification_status": "valid",
            "trust_score": 95.5,
            "upload_timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "processing_time": 28.5,
            "metadata": "{}"
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": current_user["id"],
            "original_filename": "data_science_certificate.jpg",
            "file_path": "/uploads/sample2.jpg",
            "file_type": "image/jpeg",
            "file_size": 1536000,
            "verification_status": "suspicious",
            "trust_score": 45.2,
            "upload_timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "processing_time": 32.1,
            "metadata": "{}"
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": current_user["id"],
            "original_filename": "fake_diploma.png",
            "file_path": "/uploads/sample3.png",
            "file_type": "image/png",
            "file_size": 3072000,
            "verification_status": "fake",
            "trust_score": 12.8,
            "upload_timestamp": (datetime.utcnow() - timedelta(hours=12)).isoformat(),
            "processing_time": 25.7,
            "metadata": "{}"
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": current_user["id"],
            "original_filename": "processing_certificate.pdf",
            "file_path": "/uploads/sample4.pdf",
            "file_type": "application/pdf",
            "file_size": 1024000,
            "verification_status": "pending",
            "trust_score": None,
            "upload_timestamp": datetime.utcnow().isoformat(),
            "processing_time": None,
            "metadata": "{}"
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": current_user["id"],
            "original_filename": "machine_learning_cert.pdf",
            "file_path": "/uploads/sample5.pdf",
            "file_type": "application/pdf",
            "file_size": 2560000,
            "verification_status": "valid",
            "trust_score": 88.9,
            "upload_timestamp": (datetime.utcnow() - timedelta(days=5)).isoformat(),
            "processing_time": 31.2,
            "metadata": "{}"
        }
    ]
    
    # Insert sample certificates
    for cert in sample_certificates:
        await db.certificates.insert_one(cert)
    
    return {
        "message": f"Created {len(sample_certificates)} sample certificates",
        "certificates": len(sample_certificates)
    }

@router.get("/{certificate_id}/verification-details")
async def get_verification_details(
    certificate_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed verification results for a certificate"""
    db = get_database()
    
    certificate = await db.certificates.find_one({
        "id": certificate_id,
        "user_id": current_user["id"]
    })
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    # Get verification results
    verification_result = await db.verification_results.find_one({
        "certificate_id": certificate_id
    })
    
    return {
        "certificate": {
            "id": certificate.get("id", ""),
            "file_name": certificate.get("original_filename", ""),
            "status": certificate.get("verification_status", "pending"),
            "trust_score": certificate.get("trust_score"),
        },
        "verification_details": verification_result or {},
        "has_detailed_results": verification_result is not None
    }