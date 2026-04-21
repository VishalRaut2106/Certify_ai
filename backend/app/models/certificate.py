"""
Certificate data models and schemas
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any, Annotated
from datetime import datetime
from enum import Enum
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

class VerificationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    VALID = "valid"
    SUSPICIOUS = "suspicious"
    FAKE = "fake"
    ERROR = "error"

class FileType(str, Enum):
    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    TIFF = "tiff"

class Certificate(BaseModel):
    """Main certificate model"""
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., description="User who uploaded the certificate")
    batch_id: Optional[str] = Field(None, description="Batch upload identifier")
    file_path: str = Field(..., description="Cloudinary storage path")
    cloudinary_public_id: str = Field(..., description="Cloudinary public ID")
    file_type: FileType = Field(..., description="File format")
    file_size: int = Field(..., description="File size in bytes")
    original_filename: str = Field(..., description="Original uploaded filename")
    
    # Verification data
    verification_status: VerificationStatus = Field(default=VerificationStatus.PENDING)
    trust_score: Optional[float] = Field(None, ge=0, le=100, description="Trust score 0-100")
    verification_results: Optional[Dict[str, Any]] = Field(default_factory=dict)
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    
    # Metadata
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    verification_timestamp: Optional[datetime] = Field(None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CertificateCreate(BaseModel):
    """Certificate creation schema"""
    original_filename: str
    file_type: FileType
    file_size: int
    batch_id: Optional[str] = None

class CertificateUpdate(BaseModel):
    """Certificate update schema"""
    verification_status: Optional[VerificationStatus] = None
    trust_score: Optional[float] = Field(None, ge=0, le=100)
    verification_results: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    verification_timestamp: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CertificateResponse(BaseModel):
    """Certificate response schema"""
    id: str
    user_id: str
    batch_id: Optional[str]
    original_filename: str
    file_type: FileType
    file_size: int
    verification_status: VerificationStatus
    trust_score: Optional[float]
    upload_timestamp: datetime
    verification_timestamp: Optional[datetime]
    processing_time: Optional[float]

class OCRResult(BaseModel):
    """OCR processing result"""
    extracted_text: str = Field(..., description="Full extracted text")
    confidence_score: float = Field(..., ge=0, le=100, description="OCR confidence")
    detected_language: str = Field(..., description="Detected text language")
    text_regions: List[Dict[str, Any]] = Field(default_factory=list)
    processing_time: float = Field(..., description="OCR processing time")
    enhanced_image: bool = Field(default=False, description="Whether image was enhanced")

class TemplateMatchResult(BaseModel):
    """Template matching result"""
    template_id: Optional[str] = Field(None, description="Matched template ID")
    match_confidence: float = Field(..., ge=0, le=100, description="Match confidence")
    template_name: Optional[str] = Field(None, description="Template name/source")
    match_regions: List[Dict[str, Any]] = Field(default_factory=list)
    is_known_template: bool = Field(default=False)
    similarity_score: float = Field(..., ge=0, le=1, description="Visual similarity")

class QRCodeResult(BaseModel):
    """QR code processing result"""
    qr_codes_found: List[str] = Field(default_factory=list)
    qr_validation_results: Dict[str, Any] = Field(default_factory=dict)
    reuse_detected: bool = Field(default=False)
    reuse_count: int = Field(default=0)
    first_seen_date: Optional[datetime] = Field(None)
    platform_verified: bool = Field(default=False)

class FraudDetectionResult(BaseModel):
    """Fraud detection analysis result"""
    fraud_indicators: List[str] = Field(default_factory=list)
    fraud_probability: float = Field(..., ge=0, le=1, description="Fraud probability")
    anomaly_score: float = Field(..., ge=0, le=1, description="Anomaly detection score")
    pattern_matches: List[str] = Field(default_factory=list)
    risk_factors: Dict[str, float] = Field(default_factory=dict)
    manipulation_detected: bool = Field(default=False)

class PlatformVerificationResult(BaseModel):
    """Platform API verification result"""
    platform_name: str = Field(..., description="Platform name")
    verification_successful: bool = Field(default=False)
    platform_response: Dict[str, Any] = Field(default_factory=dict)
    api_call_timestamp: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = Field(None)
    cached_result: bool = Field(default=False)

class TrustScore(BaseModel):
    """Trust score calculation details"""
    overall_score: float = Field(..., ge=0, le=100, description="Overall trust score")
    component_scores: Dict[str, float] = Field(default_factory=dict)
    weight_distribution: Dict[str, float] = Field(default_factory=dict)
    confidence_level: str = Field(..., description="high, medium, low")
    score_reasoning: List[str] = Field(default_factory=list)
    calculation_timestamp: datetime = Field(default_factory=datetime.utcnow)

class VerificationResult(BaseModel):
    """Complete verification result"""
    certificate_id: str = Field(..., description="Certificate identifier")
    verification_status: VerificationStatus = Field(...)
    trust_score: TrustScore = Field(...)
    ocr_result: OCRResult = Field(...)
    template_match_result: TemplateMatchResult = Field(...)
    qr_code_result: QRCodeResult = Field(...)
    fraud_detection_result: FraudDetectionResult = Field(...)
    platform_verification_results: List[PlatformVerificationResult] = Field(default_factory=list)
    verification_timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_duration: float = Field(..., description="Total processing time")
    verification_summary: str = Field(..., description="Human-readable summary")

class BatchUpload(BaseModel):
    """Batch upload tracking"""
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., description="User who initiated the batch")
    total_files: int = Field(..., description="Total files in batch")
    processed_files: int = Field(default=0)
    successful_verifications: int = Field(default=0)
    failed_verifications: int = Field(default=0)
    batch_status: str = Field(default="processing")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    completion_time: Optional[datetime] = Field(None)
    estimated_completion: Optional[datetime] = Field(None)

class DuplicateDetection(BaseModel):
    """Duplicate certificate detection result"""
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    certificate_id: str = Field(..., description="Certificate identifier")
    duplicate_certificates: List[str] = Field(default_factory=list)
    similarity_scores: Dict[str, float] = Field(default_factory=dict)
    hash_matches: List[str] = Field(default_factory=list)
    qr_code_matches: List[str] = Field(default_factory=list)
    detection_timestamp: datetime = Field(default_factory=datetime.utcnow)