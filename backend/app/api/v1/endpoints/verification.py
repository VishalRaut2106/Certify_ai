"""
Verification and results endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.core.database import get_database, is_using_fallback

router = APIRouter()

@router.get("/results")
async def get_verification_results(
    current_user: dict = Depends(get_current_user),
    status_filter: Optional[str] = Query(None),
    days: int = Query(30, description="Number of days to look back"),
    limit: int = Query(50, le=100)
):
    """Get verification results summary"""
    db = get_database()
    
    # Build query
    query = {"user_id": current_user["id"]}
    if status_filter:
        query["verification_status"] = status_filter
    
    if is_using_fallback():
        # SQLite path - no date filtering on query level (SQLite adapter doesn't support $gte)
        certificates = await db.certificates.find(query, limit=limit)
        certificates.sort(key=lambda x: x.get("upload_timestamp", ""), reverse=True)
    else:
        # MongoDB path
        start_date = datetime.utcnow() - timedelta(days=days)
        query["upload_timestamp"] = {"$gte": start_date}
        certificates = await db.certificates.find(query).sort("upload_timestamp", -1).limit(limit).to_list(length=limit)
    
    # Calculate statistics
    total = len(certificates)
    valid_count = len([c for c in certificates if c.get("verification_status") == "valid"])
    suspicious_count = len([c for c in certificates if c.get("verification_status") == "suspicious"])
    fake_count = len([c for c in certificates if c.get("verification_status") == "fake"])
    pending_count = len([c for c in certificates if c.get("verification_status") == "pending"])
    
    return {
        "summary": {
            "total_certificates": total,
            "valid_certificates": valid_count,
            "suspicious_certificates": suspicious_count,
            "fake_certificates": fake_count,
            "pending_certificates": pending_count,
            "verification_rate": ((total - pending_count) / total * 100) if total > 0 else 0
        },
        "certificates": certificates
    }

@router.get("/statistics")
async def get_verification_statistics(
    current_user: dict = Depends(get_current_user),
    days: int = Query(30, description="Number of days for statistics")
):
    """Get detailed verification statistics"""
    db = get_database()
    
    query = {"user_id": current_user["id"]}
    
    # Get all user certificates and compute stats in Python
    certificates = await db.certificates.find(query)
    
    # Group by status
    stats_by_status = {}
    total_processed = 0
    valid_count = 0
    fake_count = 0
    suspicious_count = 0
    pending_count = 0
    total_processing_time = 0
    processing_count = 0
    total_trust_score = 0
    trust_score_count = 0
    
    for cert in certificates:
        status = cert.get("verification_status", "pending")
        total_processed += 1
        
        if status not in stats_by_status:
            stats_by_status[status] = {
                "count": 0,
                "average_trust_score": 0,
                "average_processing_time": 0,
                "trust_scores": [],
                "processing_times": []
            }
        
        stats_by_status[status]["count"] += 1
        
        if status == "valid":
            valid_count += 1
        elif status == "fake":
            fake_count += 1
        elif status == "suspicious":
            suspicious_count += 1
        elif status == "pending":
            pending_count += 1
        
        # Processing time
        pt = cert.get("processing_time")
        if pt is not None:
            try:
                pt_float = float(pt)
                total_processing_time += pt_float
                processing_count += 1
                stats_by_status[status]["processing_times"].append(pt_float)
            except (ValueError, TypeError):
                pass
        
        # Trust score
        ts = cert.get("trust_score")
        if ts is not None:
            try:
                ts_float = float(ts)
                total_trust_score += ts_float
                trust_score_count += 1
                stats_by_status[status]["trust_scores"].append(ts_float)
            except (ValueError, TypeError):
                pass
    
    # Calculate averages for each status
    for status, data in stats_by_status.items():
        if data["trust_scores"]:
            data["average_trust_score"] = sum(data["trust_scores"]) / len(data["trust_scores"])
        if data["processing_times"]:
            data["average_processing_time"] = sum(data["processing_times"]) / len(data["processing_times"])
        # Clean up temporary lists
        del data["trust_scores"]
        del data["processing_times"]
    
    avg_processing_time = total_processing_time / processing_count if processing_count > 0 else 0
    avg_trust_score = total_trust_score / trust_score_count if trust_score_count > 0 else 0
    
    return {
        "statistics_by_status": stats_by_status,
        "total_processed": total_processed,
        "valid_count": valid_count,
        "fake_count": fake_count,
        "suspicious_count": suspicious_count,
        "pending_count": pending_count,
        "average_processing_time": round(avg_processing_time, 2),
        "average_trust_score": round(avg_trust_score, 1),
        "period_days": days,
        "generated_at": datetime.utcnow().isoformat()
    }

@router.post("/manual-review")
async def request_manual_review(
    certificate_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Request manual review for a certificate"""
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
    
    # Update certificate status
    await db.certificates.update_one(
        {"id": certificate_id},
        {"$set": {"verification_status": "review_requested"}}
    )
    
    return {
        "message": "Manual review requested successfully",
        "certificate_id": certificate_id,
        "status": "review_requested"
    }