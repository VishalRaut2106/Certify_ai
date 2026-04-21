"""
File upload endpoints for certificate processing
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, BackgroundTasks
from typing import List, Optional
import cloudinary
import cloudinary.uploader
from datetime import datetime
import hashlib
import uuid

from app.models.certificate import Certificate, CertificateCreate, FileType, BatchUpload
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.core.database import get_database
from app.core.config import settings
from app.services.background_tasks import task_processor

router = APIRouter()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

# Allowed file types and their MIME types
ALLOWED_MIME_TYPES = {
    "application/pdf": FileType.PDF,
    "image/jpeg": FileType.JPEG,
    "image/jpg": FileType.JPG,
    "image/png": FileType.PNG,
    "image/tiff": FileType.TIFF
}

@router.post("/single", status_code=status.HTTP_201_CREATED)
async def upload_single_certificate(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload a single certificate for verification"""
    
    try:
        # Validate file
        await validate_file(file)
        
        db = get_database()
        
        # Read file content
        file_content = await file.read()
        
        # Create uploads directory
        import os
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = get_file_extension(file.filename)
        unique_filename = f"cert_{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file locally
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Create certificate record compatible with SQLite
        certificate_id = str(uuid.uuid4())
        certificate_dict = {
            "id": certificate_id,
            "user_id": current_user["id"],
            "original_filename": file.filename,
            "file_path": file_path,
            "file_type": file.content_type,
            "file_size": len(file_content),
            "verification_status": "pending",
            "trust_score": None,
            "upload_timestamp": datetime.utcnow().isoformat(),
            "processing_time": None,
            "metadata": "{}"
        }
        
        # Insert into database
        await db.certificates.insert_one(certificate_dict)
        
        # Queue for AI verification
        await task_processor.queue_certificate_verification(
            certificate_id, file_path, file.content_type, file.filename
        )
        
        return {
            "message": "Certificate uploaded successfully and queued for AI verification",
            "certificate_id": certificate_id,
            "file_url": file_path,
            "status": "uploaded",
            "verification_status": "pending"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def upload_bulk_certificates(
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload multiple certificates for batch verification"""
    
    # Validate batch size
    if len(files) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch size exceeds maximum limit of {settings.MAX_BATCH_SIZE}"
        )
    
    db = get_database()
    
    # Create batch record
    batch_id = str(uuid.uuid4())
    batch_dict = {
        "id": batch_id,
        "user_id": current_user["id"],
        "total_files": len(files),
        "processed_files": 0,
        "failed_files": 0,
        "status": "processing",
        "start_time": datetime.utcnow().isoformat(),
        "end_time": None
    }
    
    await db.batch_uploads.insert_one(batch_dict)
    
    uploaded_certificates = []
    failed_uploads = []
    
    # Create uploads directory
    import os
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        try:
            # Validate individual file
            await validate_file(file)
            
            # Read file content
            file_content = await file.read()
            
            # Generate unique filename
            file_extension = get_file_extension(file.filename)
            unique_filename = f"cert_{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}.{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # Save file locally
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # Create certificate record
            certificate_id = str(uuid.uuid4())
            certificate_dict = {
                "id": certificate_id,
                "user_id": current_user["id"],
                "batch_id": batch_id,
                "original_filename": file.filename,
                "file_path": file_path,
                "file_type": file.content_type,
                "file_size": len(file_content),
                "verification_status": "pending",
                "trust_score": None,
                "upload_timestamp": datetime.utcnow().isoformat(),
                "processing_time": None,
                "metadata": "{}"
            }
            
            # Insert into database
            await db.certificates.insert_one(certificate_dict)
            
            uploaded_certificates.append({
                "certificate_id": certificate_id,
                "filename": file.filename,
                "status": "uploaded"
            })
            
        except Exception as e:
            failed_uploads.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    # Update batch statistics
    await db.batch_uploads.update_one(
        {"id": batch_id},
        {
            "$set": {
                "processed_files": len(uploaded_certificates),
                "failed_files": len(failed_uploads),
                "status": "completed" if len(failed_uploads) == 0 else "partial",
                "end_time": datetime.utcnow().isoformat()
            }
        }
    )
    
    # Update user statistics
    await db.users.update_one(
        {"id": current_user["id"]},
        {"$set": {"certificates_uploaded": current_user.get("certificates_uploaded", 0) + len(uploaded_certificates)}}
    )
    
    return {
        "message": "Batch upload completed",
        "batch_id": batch_id,
        "total_files": len(files),
        "successful_uploads": len(uploaded_certificates),
        "failed_uploads": len(failed_uploads),
        "uploaded_certificates": uploaded_certificates,
        "failed_files": failed_uploads
    }

async def validate_file(file: UploadFile) -> None:
    """Validate uploaded file"""
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE} bytes"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not supported. Allowed types: {list(ALLOWED_MIME_TYPES.keys())}"
        )

def get_file_extension(filename: str) -> str:
    """Extract file extension from filename"""
    return filename.split('.')[-1].lower() if '.' in filename else ''

@router.get("/batch/{batch_id}/progress")
async def get_batch_progress(
    batch_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get progress of batch upload"""
    db = get_database()
    
    batch = await db.batch_uploads.find_one({
        "id": batch_id,
        "user_id": current_user["id"]
    })
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    return {
        "batch_id": batch_id,
        "total_files": batch["total_files"],
        "processed_files": batch["processed_files"],
        "successful_verifications": batch["processed_files"],
        "failed_verifications": batch["failed_files"],
        "status": batch["status"],
        "start_time": batch["start_time"],
        "completion_time": batch.get("end_time"),
        "progress_percentage": (batch["processed_files"] / batch["total_files"]) * 100 if batch["total_files"] > 0 else 0
    }