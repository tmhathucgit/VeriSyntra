# ============================================
# VeriSyntra Auth Service - Security Utilities
# ============================================
# JWT token creation, verification, password hashing
# Vietnamese PDPL 2025 compliance context
# ============================================

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from uuid import UUID

# ============================================
# Configuration
# ============================================

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer scheme for token authentication
security = HTTPBearer()


# ============================================
# Password Hashing Functions
# ============================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================
# JWT Token Functions
# ============================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token with Vietnamese business context
    
    Args:
        data: Payload data including user_id, email, tenant_id, role
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token with extended expiration
    
    Args:
        data: Payload data including user_id, email
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verify token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Loai token khong hop le / Invalid token type",
                    "english": "Invalid token type"
                }
            )
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Token da het han / Token expired",
                    "english": "Token expired"
                }
            )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token khong hop le / Invalid token",
                "english": "Invalid token",
                "error": str(e)
            }
        )


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode JWT token without verification (for debugging)
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
    except JWTError:
        return {}


# ============================================
# FastAPI Dependencies
# ============================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    FastAPI dependency to get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        User data from token payload
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    token = credentials.credentials
    
    try:
        payload = verify_token(token, token_type="access")
        return payload
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Khong the xac thuc nguoi dung / Could not authenticate user",
                "english": "Could not authenticate user",
                "error": str(e)
            }
        )


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    FastAPI dependency to get current active user
    
    Args:
        current_user: User data from get_current_user dependency
        
    Returns:
        Active user data
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Tai khoan da bi vo hieu hoa / Account is inactive",
                "english": "Account is inactive"
            }
        )
    
    return current_user


# ============================================
# Token Response Models
# ============================================

def create_token_response(
    user_id: UUID,
    email: str,
    tenant_id: UUID,
    role: str,
    full_name: str,
    is_active: bool = True,
    veri_business_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create complete token response with Vietnamese business context
    
    Args:
        user_id: User UUID
        email: User email
        tenant_id: Tenant UUID
        role: User role
        full_name: User full name
        is_active: User active status
        veri_business_context: Vietnamese business context data
        
    Returns:
        Dictionary containing access_token, refresh_token, and user info
    """
    token_data = {
        "sub": str(user_id),
        "user_id": str(user_id),
        "email": email,
        "tenant_id": str(tenant_id),
        "role": role,
        "full_name": full_name,
        "is_active": is_active
    }
    
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data={"sub": str(user_id), "email": email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
        "user": {
            "user_id": str(user_id),
            "email": email,
            "full_name": full_name,
            "tenant_id": str(tenant_id),
            "role": role
        },
        "veri_business_context": veri_business_context or {}
    }
