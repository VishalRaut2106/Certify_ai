"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional

from app.models.user import User, UserCreate, UserLogin, Token, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.core.database import get_database
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Add CORS preflight handler
@router.options("/register")
@router.options("/login")
@router.options("/me")
async def options_handler():
    """Handle CORS preflight requests"""
    return Response(status_code=200)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    db = get_database()
    user_doc = await db.users.find_one({"id": user_id})
    if user_doc is None:
        raise credentials_exception
    
    if not user_doc.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    return user_doc

@router.post("/test", status_code=200)
async def test_endpoint():
    """Simple test endpoint to verify CORS"""
    return {"message": "CORS test successful", "status": "ok"}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        db = get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        # Truncate password if too long for bcrypt (72 byte limit)
        password_to_hash = user_data.password[:72] if len(user_data.password.encode('utf-8')) > 72 else user_data.password
        hashed_password = get_password_hash(password_to_hash)
        
        # Generate user ID
        import uuid
        user_id = str(uuid.uuid4())
        
        user_dict = {
            "id": user_id,
            "email": user_data.email,
            "hashed_password": hashed_password,
            "full_name": user_data.full_name,
            "role": user_data.role,
            "institution_name": user_data.institution_name,
            "permissions": [],
            "is_active": True,
            "is_verified": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "last_login": None,
            "login_count": 0,
            "certificates_uploaded": 0,
            "verifications_performed": 0
        }
        
        # Insert user into database
        await db.users.insert_one(user_dict)
        
        # Return user response (without sensitive data)
        return UserResponse(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            institution_name=user_data.institution_name,
            is_active=True,
            is_verified=False,
            created_at=datetime.utcnow(),
            last_login=None,
            certificates_uploaded=0,
            verifications_performed=0
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """User login with email and password"""
    db = get_database()
    
    # Find user by email
    user_doc = await db.users.find_one({"email": form_data.username})
    print(f"Login attempt for: {form_data.username}")
    print(f"User found: {user_doc is not None}")
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password - handle both bcrypt and SHA256 hashes
    print(f"Verifying password for user: {user_doc['email']}")
    print(f"Stored hash length: {len(user_doc['hashed_password'])}")
    print(f"Hash starts with: {user_doc['hashed_password'][:10]}...")
    
    # Truncate password if too long (same as registration)
    password_to_verify = form_data.password[:72] if len(form_data.password.encode('utf-8')) > 72 else form_data.password
    
    password_valid = verify_password(password_to_verify, user_doc["hashed_password"])
    print(f"Password valid: {password_valid}")
    
    if not password_valid:
        # Try with original password (in case truncation wasn't applied during registration)
        password_valid = verify_password(form_data.password, user_doc["hashed_password"])
        print(f"Password valid (without truncation): {password_valid}")
    
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user_doc.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Update last login
    await db.users.update_one(
        {"id": user_doc["id"]},
        {
            "$set": {
                "last_login": datetime.utcnow().isoformat(),
                "login_count": user_doc.get("login_count", 0) + 1
            }
        }
    )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user_doc["id"]), "email": user_doc["email"], "role": user_doc["role"]}
    )
    
    # Create user response
    user_response = UserResponse(
        id=user_doc["id"],
        email=user_doc["email"],
        full_name=user_doc["full_name"],
        role=user_doc["role"],
        institution_name=user_doc.get("institution_name"),
        is_active=user_doc.get("is_active", True),
        is_verified=user_doc.get("is_verified", False),
        created_at=datetime.fromisoformat(user_doc["created_at"]) if isinstance(user_doc["created_at"], str) else user_doc["created_at"],
        last_login=datetime.fromisoformat(user_doc["last_login"]) if user_doc.get("last_login") and isinstance(user_doc["last_login"], str) else user_doc.get("last_login"),
        certificates_uploaded=user_doc.get("certificates_uploaded", 0),
        verifications_performed=user_doc.get("verifications_performed", 0)
    )
    
    return Token(
        access_token=access_token,
        expires_in=settings.JWT_EXPIRATION,
        user=user_response
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
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