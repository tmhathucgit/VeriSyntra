# JWT Authentication Integration Guide

**VeriSyntra Vietnamese PDPL 2025 Compliance Platform**  
**Date:** November 7, 2025  
**Version:** 1.0  
**Audience:** Backend Developers

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Authentication Flow](#authentication-flow)
4. [FastAPI Endpoint Examples](#fastapi-endpoint-examples)
5. [Database User Model](#database-user-model)
6. [Error Handling](#error-handling)
7. [Testing Authentication](#testing-authentication)
8. [Production Considerations](#production-considerations)

---

## Overview

VeriSyntra uses JWT (JSON Web Token) based authentication with the following features:

- **Access Tokens:** 30-minute expiry for API requests
- **Refresh Tokens:** 7-day expiry for token renewal
- **Password Security:** Bcrypt hashing with complexity validation
- **Token Blacklist:** Redis-based logout/revocation
- **Bilingual Errors:** Vietnamese + English error messages
- **Multi-Tenant:** Tenant isolation built into tokens

**Security Features:**
- HS256 algorithm with secure secret key
- Fail-secure Redis blacklist (deny on errors)
- Constant-time password comparison
- Vietnamese cultural business context

---

## Quick Start

### 1. Import Authentication Functions

```python
from auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
    hash_password,
    verify_password,
    validate_password_strength,
    token_blacklist,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH
)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
```

### 2. Create Security Dependency

```python
# Initialize HTTP Bearer security scheme
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Dependency to get current authenticated user from JWT token.
    
    Vietnamese: Phụ thuộc để lấy người dùng hiện tại từ mã thông báo JWT.
    """
    token = credentials.credentials
    
    # Check if token is blacklisted (logged out)
    if token_blacklist.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token has been revoked. Please login again.",
                "message_vi": "Mã thông báo đã bị thu hồi. Vui lòng đăng nhập lại."
            }
        )
    
    try:
        # Verify token and extract payload
        payload = verify_token(token, expected_type=TOKEN_TYPE_ACCESS)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid or expired token.",
                "message_vi": "Mã thông báo không hợp lệ hoặc đã hết hạn."
            }
        )
```

### 3. Protect Endpoints

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/protected-resource")
async def protected_resource(current_user: dict = Depends(get_current_user)):
    """Protected endpoint - requires valid JWT token."""
    return {
        "message": f"Hello {current_user['email']}!",
        "tenant_id": current_user["tenant_id"],
        "regional_location": current_user["regional_location"]
    }
```

---

## Authentication Flow

### Complete Authentication Workflow

```
1. User Registration
   ├── Validate password strength
   ├── Hash password with bcrypt
   └── Store user in database

2. User Login
   ├── Verify password
   ├── Create access token (30 min)
   ├── Create refresh token (7 days)
   └── Return both tokens

3. API Request
   ├── Send access token in Authorization header
   ├── Verify token signature
   ├── Check token not blacklisted
   └── Process request

4. Token Refresh
   ├── Send refresh token
   ├── Verify refresh token
   └── Issue new access token

5. User Logout
   ├── Add access token to blacklist
   ├── Add refresh token to blacklist
   └── Tokens become invalid
```

---

## FastAPI Endpoint Examples

### 1. User Registration Endpoint

```python
from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    """User registration request model."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    tenant_id: str
    regional_location: str = Field(..., pattern="^(north|central|south)$")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "nguyen.van.a@example.com",
                "password": "MatKhau123!@#",
                "full_name": "Nguyễn Văn A",
                "tenant_id": "tenant001",
                "regional_location": "south"
            }
        }

class UserRegisterResponse(BaseModel):
    """User registration response model."""
    user_id: str
    email: str
    message: str
    message_vi: str

@router.post("/auth/register", response_model=UserRegisterResponse)
async def register_user(request: UserRegisterRequest):
    """
    Register new Vietnamese business user.
    
    Vietnamese: Đăng ký người dùng doanh nghiệp Việt Nam mới.
    """
    # 1. Validate password strength
    is_valid, error = validate_password_strength(request.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error}
        )
    
    # 2. Check if email already exists (database query)
    # existing_user = await db.get_user_by_email(request.email)
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    
    # 3. Hash password
    hashed_password = hash_password(request.password)
    
    # 4. Create user in database
    user_id = "user_" + str(uuid.uuid4())[:8]
    # await db.create_user({
    #     "user_id": user_id,
    #     "email": request.email,
    #     "password_hash": hashed_password,
    #     "full_name": request.full_name,
    #     "tenant_id": request.tenant_id,
    #     "regional_location": request.regional_location
    # })
    
    return UserRegisterResponse(
        user_id=user_id,
        email=request.email,
        message="User registered successfully",
        message_vi="Đăng ký người dùng thành công"
    )
```

### 2. User Login Endpoint

```python
class UserLoginRequest(BaseModel):
    """User login request model."""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "nguyen.van.a@example.com",
                "password": "MatKhau123!@#"
            }
        }

class UserLoginResponse(BaseModel):
    """User login response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds
    user: dict
    message: str
    message_vi: str

@router.post("/auth/login", response_model=UserLoginResponse)
async def login_user(request: UserLoginRequest):
    """
    Login Vietnamese business user and issue JWT tokens.
    
    Vietnamese: Đăng nhập người dùng doanh nghiệp Việt Nam và cấp mã thông báo JWT.
    """
    # 1. Get user from database by email
    # user = await db.get_user_by_email(request.email)
    # if not user:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Mock user data for example
    user = {
        "user_id": "user123",
        "email": request.email,
        "password_hash": hash_password(request.password),  # In reality, from DB
        "full_name": "Nguyễn Văn A",
        "tenant_id": "tenant001",
        "regional_location": "south",
        "role": "admin"
    }
    
    # 2. Verify password
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid email or password",
                "message_vi": "Email hoặc mật khẩu không hợp lệ"
            }
        )
    
    # 3. Create JWT tokens with Vietnamese business context
    token_data = {
        "user_id": user["user_id"],
        "email": user["email"],
        "tenant_id": user["tenant_id"],
        "regional_location": user["regional_location"],
        "role": user["role"]
    }
    
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    # 4. Return tokens
    return UserLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800,  # 30 minutes
        user={
            "user_id": user["user_id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "tenant_id": user["tenant_id"],
            "regional_location": user["regional_location"]
        },
        message="Login successful",
        message_vi="Đăng nhập thành công"
    )
```

### 3. Token Refresh Endpoint

```python
class TokenRefreshRequest(BaseModel):
    """Token refresh request model."""
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    """Token refresh response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800
    message: str
    message_vi: str

@router.post("/auth/refresh", response_model=TokenRefreshResponse)
async def refresh_access_token(request: TokenRefreshRequest):
    """
    Refresh access token using refresh token.
    
    Vietnamese: Làm mới mã thông báo truy cập bằng mã thông báo làm mới.
    """
    # 1. Check if refresh token is blacklisted
    if token_blacklist.is_blacklisted(request.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Refresh token has been revoked",
                "message_vi": "Mã thông báo làm mới đã bị thu hồi"
            }
        )
    
    try:
        # 2. Verify refresh token
        payload = verify_token(request.refresh_token, expected_type=TOKEN_TYPE_REFRESH)
        
        # 3. Create new access token with same user data
        new_access_token = create_access_token(data={
            "user_id": payload["user_id"],
            "email": payload["email"],
            "tenant_id": payload["tenant_id"],
            "regional_location": payload["regional_location"],
            "role": payload.get("role", "user")
        })
        
        return TokenRefreshResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=1800,
            message="Access token refreshed successfully",
            message_vi="Mã thông báo truy cập được làm mới thành công"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid or expired refresh token",
                "message_vi": "Mã thông báo làm mới không hợp lệ hoặc đã hết hạn"
            }
        )
```

### 4. User Logout Endpoint

```python
class LogoutResponse(BaseModel):
    """Logout response model."""
    message: str
    message_vi: str

@router.post("/auth/logout", response_model=LogoutResponse)
async def logout_user(
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Logout user by blacklisting JWT token.
    
    Vietnamese: Đăng xuất người dùng bằng cách đưa mã thông báo JWT vào danh sách đen.
    """
    access_token = credentials.credentials
    
    # Add access token to blacklist (30 minute TTL)
    token_blacklist.add_token(access_token, expires_in_minutes=30)
    
    # If user also provides refresh token, blacklist it too
    # (In practice, you'd get this from request body)
    
    return LogoutResponse(
        message="Logged out successfully",
        message_vi="Đăng xuất thành công"
    )
```

### 5. Protected Endpoint Examples

```python
@router.get("/api/v1/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile (protected endpoint).
    
    Vietnamese: Lấy hồ sơ người dùng hiện tại (điểm cuối được bảo vệ).
    """
    # Get full user data from database
    # user = await db.get_user_by_id(current_user["user_id"])
    
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "tenant_id": current_user["tenant_id"],
        "regional_location": current_user["regional_location"],
        "role": current_user["role"]
    }

@router.put("/api/v1/profile/password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Change user password (protected endpoint).
    
    Vietnamese: Thay đổi mật khẩu người dùng (điểm cuối được bảo vệ).
    """
    # 1. Validate new password strength
    is_valid, error = validate_password_strength(new_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"error": error})
    
    # 2. Get user from database
    # user = await db.get_user_by_id(current_user["user_id"])
    
    # 3. Verify old password
    # if not verify_password(old_password, user["password_hash"]):
    #     raise HTTPException(status_code=400, detail="Incorrect old password")
    
    # 4. Hash new password
    new_password_hash = hash_password(new_password)
    
    # 5. Update password in database
    # await db.update_user_password(current_user["user_id"], new_password_hash)
    
    return {
        "message": "Password changed successfully",
        "message_vi": "Mật khẩu đã được thay đổi thành công"
    }

@router.get("/api/v1/tenant/data")
async def get_tenant_data(current_user: dict = Depends(get_current_user)):
    """
    Get tenant-specific data with multi-tenant isolation.
    
    Vietnamese: Lấy dữ liệu theo người thuê với cách ly nhiều người thuê.
    """
    tenant_id = current_user["tenant_id"]
    
    # Query data filtered by tenant_id for isolation
    # data = await db.get_tenant_data(tenant_id)
    
    return {
        "tenant_id": tenant_id,
        "regional_location": current_user["regional_location"],
        "message": f"Data for tenant {tenant_id}",
        "message_vi": f"Dữ liệu cho người thuê {tenant_id}"
    }
```

### 6. Role-Based Access Control (RBAC)

```python
from functools import wraps
from typing import List

def require_roles(allowed_roles: List[str]):
    """
    Decorator to require specific roles for endpoint access.
    
    Vietnamese: Decorator để yêu cầu vai trò cụ thể cho quyền truy cập điểm cuối.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: dict = None, **kwargs):
            user_role = current_user.get("role", "user")
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "message": f"Access denied. Required roles: {allowed_roles}",
                        "message_vi": f"Truy cập bị từ chối. Vai trò yêu cầu: {allowed_roles}"
                    }
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

@router.delete("/api/v1/admin/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete user (admin only).
    
    Vietnamese: Xóa người dùng (chỉ quản trị viên).
    """
    # Check if user has admin role
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Admin access required",
                "message_vi": "Yêu cầu quyền quản trị viên"
            }
        )
    
    # Ensure admin can only delete users in same tenant
    # user_to_delete = await db.get_user_by_id(user_id)
    # if user_to_delete["tenant_id"] != current_user["tenant_id"]:
    #     raise HTTPException(status_code=403, detail="Cannot delete user from different tenant")
    
    # await db.delete_user(user_id)
    
    return {
        "message": f"User {user_id} deleted successfully",
        "message_vi": f"Người dùng {user_id} đã được xóa thành công"
    }
```

---

## Database User Model

### Recommended PostgreSQL Schema

```sql
-- Users table for Vietnamese business authentication
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Vietnamese business context
    full_name VARCHAR(255) NOT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    regional_location VARCHAR(20) CHECK (regional_location IN ('north', 'central', 'south')),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'superadmin')),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Indexes for performance
    INDEX idx_email (email),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_regional_location (regional_location)
);

-- Multi-tenant isolation: Always filter by tenant_id
-- Example: SELECT * FROM users WHERE tenant_id = 'tenant001' AND email = 'user@example.com';
```

### SQLAlchemy Model Example

```python
from sqlalchemy import Column, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """
    User model for Vietnamese business authentication.
    
    Vietnamese: Mô hình người dùng cho xác thực doanh nghiệp Việt Nam.
    """
    __tablename__ = "users"
    
    user_id = Column(String(50), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Vietnamese business context
    full_name = Column(String(255), nullable=False)
    tenant_id = Column(String(50), nullable=False, index=True)
    regional_location = Column(
        String(20),
        CheckConstraint("regional_location IN ('north', 'central', 'south')"),
        nullable=False,
        index=True
    )
    role = Column(
        String(20),
        CheckConstraint("role IN ('user', 'admin', 'superadmin')"),
        default="user"
    )
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
```

---

## Error Handling

### Standard Error Response Format

```python
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    """Standard error response with bilingual messages."""
    message: str
    message_vi: str
    error_code: Optional[str] = None
    details: Optional[dict] = None

# Usage in exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with bilingual errors."""
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": str(exc.detail),
                "message_vi": str(exc.detail)  # Translate if possible
            }
        )
```

### Common Error Scenarios

```python
# 1. Invalid Credentials
raise HTTPException(
    status_code=401,
    detail={
        "message": "Invalid email or password",
        "message_vi": "Email hoặc mật khẩu không hợp lệ",
        "error_code": "AUTH_INVALID_CREDENTIALS"
    }
)

# 2. Token Expired
raise HTTPException(
    status_code=401,
    detail={
        "message": "Token has expired. Please login again.",
        "message_vi": "Mã thông báo đã hết hạn. Vui lòng đăng nhập lại.",
        "error_code": "AUTH_TOKEN_EXPIRED"
    }
)

# 3. Token Blacklisted
raise HTTPException(
    status_code=401,
    detail={
        "message": "Token has been revoked. Please login again.",
        "message_vi": "Mã thông báo đã bị thu hồi. Vui lòng đăng nhập lại.",
        "error_code": "AUTH_TOKEN_REVOKED"
    }
)

# 4. Insufficient Permissions
raise HTTPException(
    status_code=403,
    detail={
        "message": "Insufficient permissions to access this resource",
        "message_vi": "Không đủ quyền để truy cập tài nguyên này",
        "error_code": "AUTH_INSUFFICIENT_PERMISSIONS"
    }
)

# 5. Weak Password
is_valid, error = validate_password_strength(password)
if not is_valid:
    raise HTTPException(
        status_code=400,
        detail={
            "error": error,  # Already bilingual
            "error_code": "AUTH_WEAK_PASSWORD"
        }
    )
```

---

## Testing Authentication

### Manual Testing with curl

```bash
# 1. Register User
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nguyen.van.a@example.com",
    "password": "MatKhau123!@#",
    "full_name": "Nguyễn Văn A",
    "tenant_id": "tenant001",
    "regional_location": "south"
  }'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nguyen.van.a@example.com",
    "password": "MatKhau123!@#"
  }'

# Response: {"access_token": "eyJ...", "refresh_token": "eyJ..."}

# 3. Access Protected Endpoint
curl -X GET http://localhost:8000/api/v1/profile \
  -H "Authorization: Bearer eyJ..."

# 4. Refresh Token
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "eyJ..."}'

# 5. Logout
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer eyJ..."
```

### Integration Test Example

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_authentication_flow():
    """Test complete authentication flow."""
    
    # 1. Register user
    register_response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "tenant_id": "test_tenant",
        "regional_location": "south"
    })
    assert register_response.status_code == 200
    
    # 2. Login
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "TestPassword123!"
    })
    assert login_response.status_code == 200
    tokens = login_response.json()
    access_token = tokens["access_token"]
    
    # 3. Access protected endpoint
    profile_response = client.get(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert profile_response.status_code == 200
    
    # 4. Logout
    logout_response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert logout_response.status_code == 200
    
    # 5. Try to use token after logout (should fail)
    profile_response_2 = client.get(
        "/api/v1/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert profile_response_2.status_code == 401
```

---

## Production Considerations

### 1. Environment Variables

```python
# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT Configuration
    JWT_SECRET_KEY: str  # From secret manager
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 1
    REDIS_PASSWORD: str = ""  # From secret manager in production
    
    # Security
    BCRYPT_ROUNDS: int = 12
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
```

### 2. HTTPS Only

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Force HTTPS in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### 3. CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),  # From config
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### 4. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login_user(request: Request, ...):
    """Login with rate limiting."""
    pass
```

### 5. Token Rotation

```python
# Implement token rotation on refresh
@router.post("/auth/refresh")
async def refresh_access_token(request: TokenRefreshRequest):
    """Refresh token with rotation (blacklist old refresh token)."""
    
    # Verify old refresh token
    payload = verify_token(request.refresh_token, TOKEN_TYPE_REFRESH)
    
    # Blacklist old refresh token
    token_blacklist.add_token(request.refresh_token, expires_in_minutes=10080)  # 7 days
    
    # Issue new access token AND new refresh token
    new_access_token = create_access_token(data=payload)
    new_refresh_token = create_refresh_token(data=payload)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token  # New refresh token
    }
```

### 6. Multi-Tenant Isolation

```python
async def get_current_user_with_tenant_check(
    current_user: dict = Depends(get_current_user),
    tenant_id: str = None  # From path or query parameter
):
    """Verify user belongs to requested tenant."""
    if tenant_id and current_user["tenant_id"] != tenant_id:
        raise HTTPException(
            status_code=403,
            detail={
                "message": "Access denied to different tenant data",
                "message_vi": "Truy cập bị từ chối vào dữ liệu người thuê khác"
            }
        )
    return current_user

@router.get("/api/v1/tenants/{tenant_id}/data")
async def get_tenant_data(
    tenant_id: str,
    current_user: dict = Depends(get_current_user_with_tenant_check)
):
    """Get tenant data with automatic tenant isolation."""
    # User can only access their own tenant data
    pass
```

### 7. Monitoring and Logging

```python
from loguru import logger

@router.post("/auth/login")
async def login_user(request: UserLoginRequest):
    """Login with audit logging."""
    
    logger.info(
        f"[AUTH] Login attempt -> Email: {request.email}"
    )
    
    # ... authentication logic ...
    
    if success:
        logger.info(
            f"[AUTH] Login successful -> User: {user['user_id']}, "
            f"Tenant: {user['tenant_id']}, Region: {user['regional_location']}"
        )
    else:
        logger.warning(
            f"[AUTH] Login failed -> Email: {request.email}, "
            f"Reason: Invalid credentials"
        )
```

### 8. Health Check Endpoint

```python
@router.get("/health/auth")
async def auth_health_check():
    """Health check for authentication system."""
    
    # Check Redis connection
    redis_health = token_blacklist.health_check()
    
    return {
        "status": "healthy" if redis_health["connected"] else "unhealthy",
        "redis": redis_health,
        "jwt": "configured",
        "password_hashing": "bcrypt"
    }
```

---

## Security Best Practices

### 1. Never Log Sensitive Data

```python
# BAD - Do not log passwords or tokens
logger.info(f"User login: {email}, password: {password}")  # NO!
logger.info(f"Token created: {access_token}")  # NO!

# GOOD - Log only non-sensitive info
logger.info(f"User login attempt: {email}")
logger.info(f"Token created for user: {user_id}")
```

### 2. Validate Input Thoroughly

```python
from pydantic import validator

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
    @validator("email")
    def email_must_be_lowercase(cls, v):
        return v.lower()
    
    @validator("password")
    def password_must_be_strong(cls, v):
        is_valid, error = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error)
        return v
```

### 3. Use Secure Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### 4. Implement Account Lockout

```python
# Track failed login attempts in Redis
async def check_login_attempts(email: str):
    """Check if account is locked due to failed attempts."""
    key = f"login_attempts:{email}"
    attempts = await redis.get(key)
    
    if attempts and int(attempts) >= 5:
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Account temporarily locked. Too many failed attempts.",
                "message_vi": "Tài khoản tạm thời bị khóa. Quá nhiều lần thử không thành công."
            }
        )

async def record_failed_login(email: str):
    """Record failed login attempt."""
    key = f"login_attempts:{email}"
    await redis.incr(key)
    await redis.expire(key, 900)  # Lock for 15 minutes
```

---

## Complete Main Application Example

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
    hash_password,
    verify_password,
    validate_password_strength,
    token_blacklist,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH
)
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="VeriSyntra API",
    description="Vietnamese PDPL 2025 Compliance Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    
    if token_blacklist.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token has been revoked",
                "message_vi": "Mã thông báo đã bị thu hồi"
            }
        )
    
    try:
        payload = verify_token(token, TOKEN_TYPE_ACCESS)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid or expired token",
                "message_vi": "Mã thông báo không hợp lệ hoặc đã hết hạn"
            }
        )

# Routes
@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "VeriSyntra API - Vietnamese PDPL 2025 Compliance Platform",
        "message_vi": "API VeriSyntra - Nền tảng tuân thủ PDPL 2025 Việt Nam",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    redis_health = token_blacklist.health_check()
    return {
        "status": "healthy",
        "redis": redis_health,
        "authentication": "enabled"
    }

# Include authentication routes
# from routes import auth_router
# app.include_router(auth_router, prefix="/auth", tags=["authentication"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

---

## Summary

This integration guide provides everything needed to implement JWT authentication in VeriSyntra:

✅ **Complete FastAPI endpoints** (register, login, refresh, logout)  
✅ **Security dependencies** (get_current_user, RBAC)  
✅ **Database models** (PostgreSQL, SQLAlchemy)  
✅ **Error handling** (bilingual Vietnamese+English)  
✅ **Testing examples** (manual and automated)  
✅ **Production considerations** (HTTPS, CORS, rate limiting, monitoring)  
✅ **Vietnamese business context** (multi-tenant, regional location)  

**Next Steps:**
1. Implement database layer (PostgreSQL + SQLAlchemy)
2. Create authentication routes module
3. Add rate limiting and security middleware
4. Deploy with secret manager integration
5. Monitor authentication metrics

---

**Last Updated:** November 7, 2025  
**Author:** VeriSyntra Backend Team  
**License:** Proprietary - VeriSyntra Vietnamese PDPL 2025 Compliance Platform
