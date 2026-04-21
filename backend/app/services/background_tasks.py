"""
Background task processing for certificate verification
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from app.services.verification_service import verification_service
from app.core.database import get_database

logger = logging.getLogger(__name__)

class BackgroundTaskProcessor:
    """Handles background processing of certificate verification"""
    
    def __init__(self):
        self.processing_queue = asyncio.Queue()
        self.is_running = False
    
    async def start_processor(self):
        """Start the background task processor"""
        if self.is_running:
            return
        
        self.is_running = True
        logger.info("Starting background task processor...")
        
        # Start processing loop
        asyncio.create_task(self._process_queue())
    
    async def stop_processor(self):
        """Stop the background task processor"""
        self.is_running = False
        logger.info("Stopping background task processor...")
    
    async def queue_certificate_verification(self, certificate_id: str, file_path: str, 
                                           file_type: str, original_filename: str):
        """Queue a certificate for verification"""
        task_data = {
            "certificate_id": certificate_id,
            "file_path": file_path,
            "file_type": file_type,
            "original_filename": original_filename,
            "queued_at": datetime.utcnow().isoformat()
        }
        
        await self.processing_queue.put(task_data)
        logger.info(f"Queued certificate {certificate_id} for verification")
    
    async def _process_queue(self):
        """Main processing loop"""
        while self.is_running:
            try:
                # Wait for tasks with timeout
                task_data = await asyncio.wait_for(
                    self.processing_queue.get(), 
                    timeout=1.0
                )
                
                # Process the certificate
                await self._process_certificate(task_data)
                
            except asyncio.TimeoutError:
                # No tasks in queue, continue loop
                continue
            except Exception as e:
                logger.error(f"Error in background processor: {e}")
                await asyncio.sleep(1)  # Brief pause before retrying
    
    async def _process_certificate(self, task_data: Dict[str, Any]):
        """Process a single certificate verification"""
        certificate_id = task_data["certificate_id"]
        
        try:
            logger.info(f"Starting verification for certificate {certificate_id}")
            
            # Update certificate status to processing
            db = get_database()
            await db.certificates.update_one(
                {"id": certificate_id},
                {"$set": {"verification_status": "processing"}}
            )
            
            # Perform verification
            verification_result = await verification_service.verify_certificate(
                task_data["file_path"],
                task_data["file_type"],
                task_data["original_filename"]
            )
            
            # Update certificate with results
            await db.certificates.update_one(
                {"id": certificate_id},
                {
                    "$set": {
                        "verification_status": verification_result["verification_status"],
                        "trust_score": verification_result["trust_score"],
                        "processing_time": verification_result["processing_time"],
                        "metadata": str(verification_result["verification_details"])
                    }
                }
            )
            
            # Store detailed verification results
            verification_record = {
                "id": f"verify_{certificate_id}",
                "certificate_id": certificate_id,
                "verification_timestamp": datetime.utcnow().isoformat(),
                "ocr_results": str(verification_result["verification_details"].get("ocr_analysis", {})),
                "qr_results": str(verification_result["verification_details"].get("qr_code_analysis", {})),
                "template_match_results": str(verification_result["verification_details"].get("visual_analysis", {})),
                "fraud_indicators": str(verification_result.get("fraud_indicators", [])),
                "trust_score": verification_result["trust_score"],
                "verification_details": str(verification_result)
            }
            
            await db.verification_results.insert_one(verification_record)
            
            logger.info(f"Completed verification for certificate {certificate_id}: {verification_result['verification_status']} (Trust: {verification_result['trust_score']}%)")
            
        except Exception as e:
            logger.error(f"Failed to process certificate {certificate_id}: {e}")
            
            # Update certificate with error status
            try:
                db = get_database()
                await db.certificates.update_one(
                    {"id": certificate_id},
                    {
                        "$set": {
                            "verification_status": "error",
                            "trust_score": 0.0,
                            "processing_time": 0.0,
                            "metadata": f"Error: {str(e)}"
                        }
                    }
                )
            except Exception as update_error:
                logger.error(f"Failed to update certificate {certificate_id} with error status: {update_error}")

# Global task processor instance
task_processor = BackgroundTaskProcessor()