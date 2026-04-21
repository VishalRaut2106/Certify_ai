"""
User authentication and management models
"""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional
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

class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    EVALUATOR = "evaluator"
    STUDENT = "student"

class User(BaseModel):
    """User model for authentication and authorization"""
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(..., description="User email address")
    hashed_password: str = Field(..., description="Hashed password")
    full_name: str = Field(..., description="User's full name")
    role: UserRole = Field(default=UserRole.TEACHER, description="User role")
    institution_id: Optional[str] = Field(None, description="Associated institution")
    institution_name: Optional[str] = Field(None, description="Institution name")
    
    # Permissions and access control
    permissions: List[str] = Field(default_factory=list, description="User permissions")
    is_active: bool = Field(default=True, description="Account active status")
    is_verified: bool = Field(default=False, description="Email verification status")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(None)
    login_count: int = Field(default=0)
    
    # Usage statistics
    certificates_uploaded: int = Field(default=0)
    verifications_performed: int = Field(default=0)

class UserCreate(BaseModel):
    """User creation schema"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    full_name: str = Field(..., min_length=2, description="Full name")
    role: UserRole = UserRole.TEACHER
    institution_name: Optional[str] = None

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    institution_name: Optional[str] = None
    is_active: Optional[bool] = None
    permissions: Optional[List[str]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserResponse(BaseModel):
    """User response schema (without sensitive data)"""
    id: str
    email: EmailStr
    full_name: str
    role: UserRole
    institution_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    certificates_uploaded: int
    verifications_performed: int

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class TokenData(BaseModel):
    """Token payload data"""
    user_id: str
    email: str
    role: UserRole
    permissions: List[str] = Field(default_factory=list)

class PasswordReset(BaseModel):
    """Password reset request"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        "upload_certificates",
        "view_all_results", 
        "export_results",
        "manage_users",
        "system_configuration",
        "view_analytics",
        "manual_review",
        "delete_certificates"
    ],
    UserRole.TEACHER: [
        "upload_certificates",
        "view_own_results",
        "export_own_results",
        "manual_review"
    ],
    UserRole.EVALUATOR: [
        "view_results",
        "manual_review",
        "export_results"
    ],
    UserRole.STUDENT: [
        "upload_certificates",
        "view_own_results"
    ]
}