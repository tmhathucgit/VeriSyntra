# Phase 7: Authentication & Authorization Implementation Plan

**Document:** DOC12 Phase 7 - Authentication & Authorization  
**Vietnamese PDPL 2025 Compliance Platform**  
**Start Date:** November 6, 2025  
**Estimated Duration:** 2-3 weeks (35-48 hours total)  
**Status:** PLANNING

---

## Executive Summary

Phase 7 implements **comprehensive authentication and authorization** for VeriSyntra's Data Inventory system. This phase transforms the system from assuming pre-authenticated users to a production-ready secure API with:

- **JWT-Based Authentication** (access + refresh tokens)
- **Role-Based Access Control (RBAC)** (4 roles: admin, compliance_officer, data_processor, viewer)
- **API Key Management** (for system integrations)
- **OAuth2 Integration** (Google, Microsoft SSO)
- **Session Management** (Redis-backed)
- **Security Audit Logging** (bilingual Vietnamese-first)

**Dependencies:** Phases 1-6 must be complete (database integration, CRUD operations, API endpoints)

---

## Table of Contents

1. [Phase Overview](#phase-overview)
2. [Phase 7.1: JWT Authentication Infrastructure](#phase-71-jwt-authentication-infrastructure)
3. [Phase 7.2: User Authentication Endpoints](#phase-72-user-authentication-endpoints)
4. [Phase 7.3: Role-Based Access Control (RBAC)](#phase-73-role-based-access-control-rbac)
5. [Phase 7.4: API Key Management](#phase-74-api-key-management)
6. [Phase 7.5: Secure All Existing Endpoints](#phase-75-secure-all-existing-endpoints)
7. [Phase 7.6: OAuth2 Integration](#phase-76-oauth2-integration-optional)
8. [Phase 7.7: Session Management with Redis](#phase-77-session-management-with-redis)
9. [Phase 7.8: Security Audit Logging](#phase-78-security-audit-logging)
10. [Phase 7.9: Integration Tests](#phase-79-integration-tests-for-auth)
11. [Phase 7.10: Documentation and Deployment](#phase-710-documentation-and-deployment)
12. [Implementation Timeline](#implementation-timeline)
13. [Security Considerations](#security-considerations)
14. [Vietnamese PDPL Compliance Notes](#vietnamese-pdpl-compliance-notes)

---

## Phase Overview

### Current State (After Phase 6)

**Working:**
- Database integration complete (PostgreSQL + async SQLAlchemy)
- 10 CRUD modules operational
- ROPA generation from database functional
- Multi-tenant data isolation enforced at database level

**Security Gaps:**
- No user authentication (endpoints assume pre-authenticated `tenant_id`)
- No authorization checks (any user can access any tenant's data)
- No API key support (cannot integrate with external systems securely)
- No audit trail for authentication events

### Target State (After Phase 7)

**Authentication:**
- JWT-based login with access/refresh tokens
- Password hashing with bcrypt
- Email verification for new accounts
- Password reset flow
- Optional MFA (future enhancement)

**Authorization:**
- 4 roles with granular permissions
- Tenant-level role assignment
- Permission-based endpoint protection
- API key authentication for system integrations

**Security:**
- Redis-backed session management
- Comprehensive auth audit logging (bilingual)
- OAuth2 SSO integration (Google, Microsoft)
- Rate limiting on auth endpoints

---

## Phase 7.1: JWT Authentication Infrastructure

**Duration:** 4-6 hours  
**Deliverables:** JWT utilities, password hashing, auth middleware

### 1.1 Dependencies Installation

```bash
# Add to requirements.txt
python-jose[cryptography]==3.3.0  # JWT token generation
passlib[bcrypt]==1.7.4           # Password hashing
python-multipart==0.0.6          # Form data parsing
```

### 1.2 JWT Token Service (`auth/jwt_service.py`)

**Purpose:** Generate and validate JWT tokens

```python
"""
JWT Token Service
Vietnamese PDPL 2025 Compliance - VeriSyntra

Handles JWT access and refresh token generation/validation.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from uuid import UUID
import os

# Named constants (zero hard-coding)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-min-32-chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Vietnamese timezone
VIETNAM_TIMEZONE = "Asia/Ho_Chi_Minh"


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    
    Args:
        data: Token payload (user_id, tenant_id, roles)
        expires_delta: Custom expiration (default: 30 minutes)
    
    Returns:
        Encoded JWT token
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
    Create JWT refresh token
    
    Args:
        data: Token payload (user_id, tenant_id)
        expires_delta: Custom expiration (default: 7 days)
    
    Returns:
        Encoded JWT refresh token
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
        token_type: Expected token type ('access' or 'refresh')
    
    Returns:
        Decoded token payload
    
    Raises:
        JWTError: If token is invalid or expired
        ValueError: If token type mismatch
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Validate token type
        if payload.get("type") != token_type:
            raise ValueError(f"Invalid token type. Expected: {token_type}")
        
        return payload
    
    except JWTError as e:
        raise JWTError(f"Token validation failed: {str(e)}")


def extract_user_id(token: str) -> UUID:
    """Extract user_id from token payload"""
    payload = verify_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Token missing user_id (sub claim)")
    return UUID(user_id)


def extract_tenant_id(token: str) -> UUID:
    """Extract tenant_id from token payload"""
    payload = verify_token(token)
    tenant_id = payload.get("tenant_id")
    if not tenant_id:
        raise ValueError("Token missing tenant_id")
    return UUID(tenant_id)
```

### 1.3 Password Hashing Service (`auth/password_service.py`)

```python
"""
Password Hashing Service
Vietnamese PDPL 2025 Compliance - VeriSyntra

Secure password hashing with bcrypt.
"""

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password (bcrypt format)
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    
    Args:
        plain_password: User-provided password
        hashed_password: Stored bcrypt hash
    
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> tuple[bool, str, str]:
    """
    Validate password meets security requirements
    
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - At least 1 special character
    
    Returns:
        Tuple of (is_valid, error_message_en, error_message_vi)
    """
    if len(password) < 8:
        return (False, 
                "Password must be at least 8 characters",
                "Mật khẩu phải có ít nhất 8 ký tự")
    
    if not any(c.isupper() for c in password):
        return (False,
                "Password must contain at least 1 uppercase letter",
                "Mật khẩu phải có ít nhất 1 chữ hoa")
    
    if not any(c.islower() for c in password):
        return (False,
                "Password must contain at least 1 lowercase letter",
                "Mật khẩu phải có ít nhất 1 chữ thường")
    
    if not any(c.isdigit() for c in password):
        return (False,
                "Password must contain at least 1 digit",
                "Mật khẩu phải có ít nhất 1 chữ số")
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return (False,
                "Password must contain at least 1 special character",
                "Mật khẩu phải có ít nhất 1 ký tự đặc biệt")
    
    return (True, "", "")
```

### 1.4 Authentication Middleware (`auth/dependencies.py`)

```python
"""
Authentication Dependencies for FastAPI
Vietnamese PDPL 2025 Compliance - VeriSyntra

FastAPI dependency injection for authentication.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from database.connection import get_db
from auth.jwt_service import verify_token, extract_user_id, extract_tenant_id
from crud.user import get_user_by_id  # New CRUD module

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> UUID:
    """
    Extract and validate current user from JWT token
    
    Returns:
        User ID (UUID)
    
    Raises:
        HTTPException: 401 if token invalid
    """
    try:
        token = credentials.credentials
        payload = verify_token(token, token_type="access")
        user_id = UUID(payload.get("sub"))
        
        # Verify user exists in database
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "User not found",
                    "error_vi": "Không tìm thấy người dùng"
                }
            )
        
        return user_id
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid authentication credentials",
                "error_vi": "Thông tin xác thực không hợp lệ",
                "message": str(e)
            },
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_tenant(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """
    Extract tenant_id from JWT token
    
    Returns:
        Tenant ID (UUID)
    
    Raises:
        HTTPException: 401 if token invalid or missing tenant_id
    """
    try:
        token = credentials.credentials
        payload = verify_token(token, token_type="access")
        tenant_id = payload.get("tenant_id")
        
        if not tenant_id:
            raise ValueError("Token missing tenant_id")
        
        return UUID(tenant_id)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid tenant credentials",
                "error_vi": "Thông tin tenant không hợp lệ",
                "message": str(e)
            },
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[UUID]:
    """
    Optional authentication - returns None if no token provided
    
    Useful for public endpoints with enhanced features for authenticated users
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token, token_type="access")
        return UUID(payload.get("sub"))
    except:
        return None
```

---

## Phase 7.2: User Authentication Endpoints

**Duration:** 4-5 hours  
**Deliverables:** Login, registration, password reset endpoints

### 2.1 User Database Schema

**Add to `database/schema.sql`:**

```sql
-- ============================================
-- Users Table (Authentication)
-- ============================================

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    
    -- User credentials
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name_vi VARCHAR(255) NOT NULL,  -- Họ tên (Vietnamese primary)
    full_name_en VARCHAR(255),           -- Full name (English fallback)
    
    -- Account status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    
    -- Security
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    password_changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Lifecycle
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,  -- Soft delete
    
    CONSTRAINT users_tenant_email_unique UNIQUE (tenant_id, email)
);

-- Indexes
CREATE INDEX idx_users_tenant ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active) WHERE deleted_at IS NULL;

-- Comments
COMMENT ON TABLE users IS 'User authentication and account management - Vietnamese PDPL 2025';
COMMENT ON COLUMN users.full_name_vi IS 'Họ tên (Full name in Vietnamese - primary)';
COMMENT ON COLUMN users.full_name_en IS 'Full name (English - fallback)';
```

### 2.2 Authentication API Models (`models/auth_models.py`)

```python
"""
Authentication API Models
Vietnamese PDPL 2025 Compliance - VeriSyntra

Pydantic models for authentication requests/responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID


class UserRegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name_vi: str = Field(..., min_length=2, max_length=255)
    full_name_en: Optional[str] = Field(None, max_length=255)
    tenant_id: UUID


class UserLoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds until access token expires
    user_id: UUID
    tenant_id: UUID


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset initiation request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation with token"""
    reset_token: str
    new_password: str = Field(..., min_length=8)


class ChangePasswordRequest(BaseModel):
    """Change password for authenticated user"""
    current_password: str
    new_password: str = Field(..., min_length=8)
```

### 2.3 Authentication Endpoints (`api/auth_endpoints.py`)

```python
"""
Authentication API Endpoints
Vietnamese PDPL 2025 Compliance - VeriSyntra

User registration, login, token refresh, password reset.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from database.connection import get_db
from models.auth_models import (
    UserRegisterRequest, UserLoginRequest, TokenResponse,
    RefreshTokenRequest, PasswordResetRequest, PasswordResetConfirm,
    ChangePasswordRequest
)
from auth.jwt_service import create_access_token, create_refresh_token, verify_token
from auth.password_service import hash_password, verify_password, validate_password_strength
from auth.dependencies import get_current_user
from crud.user import (
    create_user, get_user_by_email, update_user_login,
    increment_failed_login, reset_failed_login
)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register_user(
    request: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Register new user account
    
    Vietnamese PDPL 2025 Compliance:
    - Password strength validation
    - Bilingual full name support
    - Tenant isolation
    """
    # Validate password strength
    is_valid, error_en, error_vi = validate_password_strength(request.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error_en, "error_vi": error_vi}
        )
    
    # Check if email already exists
    existing_user = await get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "Email already registered",
                "error_vi": "Email đã được đăng ký"
            }
        )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create user
    user = await create_user(
        db=db,
        tenant_id=request.tenant_id,
        email=request.email,
        password_hash=password_hash,
        full_name_vi=request.full_name_vi,
        full_name_en=request.full_name_en
    )
    
    # Generate tokens
    access_token = create_access_token(data={
        "sub": str(user.user_id),
        "tenant_id": str(user.tenant_id)
    })
    refresh_token = create_refresh_token(data={
        "sub": str(user.user_id),
        "tenant_id": str(user.tenant_id)
    })
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800,  # 30 minutes
        user_id=user.user_id,
        tenant_id=user.tenant_id
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    User login with email/password
    
    Returns JWT access and refresh tokens.
    """
    # Get user by email
    user = await get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid email or password",
                "error_vi": "Email hoặc mật khẩu không đúng"
            }
        )
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Account temporarily locked due to failed login attempts",
                "error_vi": "Tài khoản tạm thời bị khóa do đăng nhập sai nhiều lần"
            }
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        await increment_failed_login(db, user.user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid email or password",
                "error_vi": "Email hoặc mật khẩu không đúng"
            }
        )
    
    # Reset failed login attempts
    await reset_failed_login(db, user.user_id)
    
    # Update last login
    await update_user_login(db, user.user_id)
    
    # Generate tokens
    access_token = create_access_token(data={
        "sub": str(user.user_id),
        "tenant_id": str(user.tenant_id)
    })
    refresh_token = create_refresh_token(data={
        "sub": str(user.user_id),
        "tenant_id": str(user.tenant_id)
    })
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=1800,
        user_id=user.user_id,
        tenant_id=user.tenant_id
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Refresh access token using refresh token
    """
    try:
        # Verify refresh token
        payload = verify_token(request.refresh_token, token_type="refresh")
        user_id = UUID(payload.get("sub"))
        tenant_id = UUID(payload.get("tenant_id"))
        
        # Verify user still exists and is active
        user = await get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "User not found or inactive"}
            )
        
        # Generate new access token
        new_access_token = create_access_token(data={
            "sub": str(user_id),
            "tenant_id": str(tenant_id)
        })
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=request.refresh_token,  # Keep same refresh token
            expires_in=1800,
            user_id=user_id,
            tenant_id=tenant_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid refresh token",
                "error_vi": "Token làm mới không hợp lệ"
            }
        )


@router.post("/change-password", status_code=200)
async def change_password(
    request: ChangePasswordRequest,
    current_user: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change password for authenticated user
    """
    # Get user
    user = await get_user_by_id(db, current_user)
    
    # Verify current password
    if not verify_password(request.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Current password is incorrect",
                "error_vi": "Mật khẩu hiện tại không đúng"
            }
        )
    
    # Validate new password strength
    is_valid, error_en, error_vi = validate_password_strength(request.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error_en, "error_vi": error_vi}
        )
    
    # Hash and update password
    new_password_hash = hash_password(request.new_password)
    await update_user_password(db, user.user_id, new_password_hash)
    
    return {
        "message": "Password changed successfully",
        "message_vi": "Đổi mật khẩu thành công"
    }
```

---

## Phase 7.3: Role-Based Access Control (RBAC)

**Duration:** 5-6 hours  
**Deliverables:** Roles, permissions, RBAC middleware

### 3.1 RBAC Database Schema

```sql
-- ============================================
-- Roles and Permissions Tables
-- ============================================

CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_name_vi VARCHAR(50) NOT NULL,  -- Tên vai trò (Vietnamese)
    description TEXT,
    description_vi TEXT,  -- Mô tả (Vietnamese)
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Default roles
INSERT INTO roles (role_name, role_name_vi, description, description_vi) VALUES
('admin', 'Quản trị viên', 'Full system access', 'Truy cập toàn quyền hệ thống'),
('compliance_officer', 'Cán bộ tuân thủ', 'Manage compliance and generate ROPAs', 'Quản lý tuân thủ và tạo ROPA'),
('data_processor', 'Người xử lý dữ liệu', 'Manage processing activities', 'Quản lý hoạt động xử lý dữ liệu'),
('viewer', 'Người xem', 'Read-only access', 'Chỉ được xem');


CREATE TABLE user_roles (
    user_role_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(role_id) ON DELETE CASCADE,
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    assigned_by UUID REFERENCES users(user_id),
    
    CONSTRAINT user_roles_unique UNIQUE (user_id, role_id, tenant_id)
);

-- Indexes
CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_user_roles_role ON user_roles(role_id);
CREATE INDEX idx_user_roles_tenant ON user_roles(tenant_id);


CREATE TABLE permissions (
    permission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    permission_name VARCHAR(100) NOT NULL UNIQUE,
    permission_name_vi VARCHAR(100) NOT NULL,
    resource VARCHAR(50) NOT NULL,  -- e.g., 'ropa', 'processing_activity', 'user'
    action VARCHAR(50) NOT NULL,    -- e.g., 'read', 'write', 'delete', 'export'
    
    description TEXT,
    description_vi TEXT
);

-- Permission examples
INSERT INTO permissions (permission_name, permission_name_vi, resource, action, description, description_vi) VALUES
('ropa.read', 'Xem ROPA', 'ropa', 'read', 'View ROPA documents', 'Xem tài liệu ROPA'),
('ropa.write', 'Tạo ROPA', 'ropa', 'write', 'Create and edit ROPA documents', 'Tạo và chỉnh sửa tài liệu ROPA'),
('ropa.delete', 'Xóa ROPA', 'ropa', 'delete', 'Delete ROPA documents', 'Xóa tài liệu ROPA'),
('ropa.export', 'Xuất ROPA', 'ropa', 'export', 'Export ROPA in various formats', 'Xuất ROPA ở nhiều định dạng'),
('processing_activity.read', 'Xem hoạt động xử lý', 'processing_activity', 'read', 'View processing activities', 'Xem hoạt động xử lý dữ liệu'),
('processing_activity.write', 'Tạo hoạt động xử lý', 'processing_activity', 'write', 'Create and edit processing activities', 'Tạo và chỉnh sửa hoạt động xử lý'),
('processing_activity.delete', 'Xóa hoạt động xử lý', 'processing_activity', 'delete', 'Delete processing activities', 'Xóa hoạt động xử lý'),
('user.manage', 'Quản lý người dùng', 'user', 'manage', 'Manage users and roles', 'Quản lý người dùng và vai trò');


CREATE TABLE role_permissions (
    role_permission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role_id UUID NOT NULL REFERENCES roles(role_id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES permissions(permission_id) ON DELETE CASCADE,
    
    CONSTRAINT role_permissions_unique UNIQUE (role_id, permission_id)
);

-- Admin role gets all permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM roles r
CROSS JOIN permissions p
WHERE r.role_name = 'admin';

-- Compliance officer permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM roles r
JOIN permissions p ON p.permission_name IN (
    'ropa.read', 'ropa.write', 'ropa.export',
    'processing_activity.read', 'processing_activity.write'
)
WHERE r.role_name = 'compliance_officer';

-- Data processor permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM roles r
JOIN permissions p ON p.permission_name IN (
    'processing_activity.read', 'processing_activity.write',
    'ropa.read'
)
WHERE r.role_name = 'data_processor';

-- Viewer permissions (read-only)
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM roles r
JOIN permissions p ON p.permission_name IN (
    'ropa.read', 'processing_activity.read'
)
WHERE r.role_name = 'viewer';
```

### 3.2 RBAC Middleware (`auth/rbac.py`)

```python
"""
Role-Based Access Control (RBAC) Middleware
Vietnamese PDPL 2025 Compliance - VeriSyntra

Permission-based endpoint protection.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from database.connection import get_db
from auth.dependencies import get_current_user, get_current_tenant
from crud.user_roles import get_user_permissions_for_tenant


def require_permission(required_permission: str):
    """
    Dependency factory for permission-based authorization
    
    Usage:
        @router.post("/ropa/generate", dependencies=[Depends(require_permission("ropa.write"))])
    
    Args:
        required_permission: Permission name (e.g., 'ropa.write', 'processing_activity.delete')
    
    Returns:
        FastAPI dependency function
    """
    async def check_permission(
        current_user: UUID = Depends(get_current_user),
        current_tenant: UUID = Depends(get_current_tenant),
        db: AsyncSession = Depends(get_db)
    ):
        # Get user's permissions for this tenant
        permissions = await get_user_permissions_for_tenant(db, current_user, current_tenant)
        
        # Check if user has required permission
        if required_permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": f"Insufficient permissions. Required: {required_permission}",
                    "error_vi": f"Không đủ quyền. Cần: {required_permission}",
                    "required_permission": required_permission,
                    "user_permissions": permissions
                }
            )
        
        return True
    
    return check_permission


def require_role(required_role: str):
    """
    Dependency factory for role-based authorization
    
    Usage:
        @router.delete("/users/{user_id}", dependencies=[Depends(require_role("admin"))])
    
    Args:
        required_role: Role name (e.g., 'admin', 'compliance_officer')
    
    Returns:
        FastAPI dependency function
    """
    async def check_role(
        current_user: UUID = Depends(get_current_user),
        current_tenant: UUID = Depends(get_current_tenant),
        db: AsyncSession = Depends(get_db)
    ):
        from crud.user_roles import get_user_roles_for_tenant
        
        # Get user's roles for this tenant
        roles = await get_user_roles_for_tenant(db, current_user, current_tenant)
        
        # Check if user has required role
        if required_role not in [r.role_name for r in roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": f"Insufficient role. Required: {required_role}",
                    "error_vi": f"Vai trò không đủ. Cần: {required_role}",
                    "required_role": required_role,
                    "user_roles": [r.role_name for r in roles]
                }
            )
        
        return True
    
    return check_role
```

---

## Phase 7.4: API Key Management

**Duration:** 3-4 hours  
**Deliverables:** API key generation, validation, rotation

### 4.1 API Keys Database Schema

```sql
-- ============================================
-- API Keys Table
-- ============================================

CREATE TABLE api_keys (
    api_key_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    
    -- Key details
    key_name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,  -- Hashed API key
    key_prefix VARCHAR(20) NOT NULL,  -- First 8 chars for identification
    
    -- Permissions
    scopes TEXT[] DEFAULT ARRAY[]::TEXT[],  -- e.g., ['ropa.read', 'ropa.write']
    
    -- Status and lifecycle
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    
    -- Audit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(user_id),
    revoked_at TIMESTAMP WITH TIME ZONE,
    revoked_by UUID REFERENCES users(user_id),
    
    -- Rate limiting
    rate_limit_per_minute INTEGER DEFAULT 60,
    usage_count INTEGER DEFAULT 0,
    
    CONSTRAINT api_keys_tenant_name_unique UNIQUE (tenant_id, key_name)
);

-- Indexes
CREATE INDEX idx_api_keys_tenant ON api_keys(tenant_id);
CREATE INDEX idx_api_keys_prefix ON api_keys(key_prefix);
CREATE INDEX idx_api_keys_active ON api_keys(is_active) WHERE revoked_at IS NULL;

COMMENT ON TABLE api_keys IS 'API keys for system integrations - Vietnamese PDPL 2025';
```

### 4.2 API Key Service (`auth/api_key_service.py`)

```python
"""
API Key Management Service
Vietnamese PDPL 2025 Compliance - VeriSyntra

Generate, validate, and manage API keys.
"""

import secrets
import hashlib
from typing import Tuple, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from auth.password_service import hash_password, verify_password


def generate_api_key() -> Tuple[str, str, str]:
    """
    Generate new API key
    
    Returns:
        Tuple of (full_key, key_hash, key_prefix)
        - full_key: Plain text key (show to user ONCE)
        - key_hash: Hashed key (store in database)
        - key_prefix: First 8 chars (for identification)
    """
    # Generate random key (32 bytes = 64 hex chars)
    full_key = f"veri_{secrets.token_urlsafe(32)}"
    
    # Hash the key for storage
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    
    # Get prefix for identification
    key_prefix = full_key[:13]  # "veri_" + 8 chars
    
    return (full_key, key_hash, key_prefix)


def verify_api_key(plain_key: str, stored_hash: str) -> bool:
    """
    Verify API key against stored hash
    
    Args:
        plain_key: User-provided API key
        stored_hash: SHA-256 hash from database
    
    Returns:
        True if key matches, False otherwise
    """
    computed_hash = hashlib.sha256(plain_key.encode()).hexdigest()
    return computed_hash == stored_hash
```

---

## Implementation Timeline

**Week 1: Authentication Foundation (Days 1-5)**
- Days 1-2: Phase 7.1 - JWT Infrastructure + Password Service
- Days 3-4: Phase 7.2 - User Authentication Endpoints
- Day 5: Testing authentication flow

**Week 2: Authorization (Days 6-10)**
- Days 6-8: Phase 7.3 - RBAC Implementation
- Day 9: Phase 7.4 - API Key Management
- Day 10: Phase 7.5 - Secure Existing Endpoints

**Week 3: Advanced Features & Testing (Days 11-15)**
- Days 11-12: Phase 7.6 - OAuth2 Integration (optional)
- Day 13: Phase 7.7 - Session Management (Redis)
- Day 14: Phase 7.8 - Security Audit Logging + Phase 7.9 - Testing
- Day 15: Phase 7.10 - Documentation

**Total:** 35-48 hours over 3 weeks

---

## Security Considerations

**Password Security:**
- Bcrypt hashing with automatic salt
- Minimum 8 characters with complexity requirements
- Account lockout after 5 failed attempts (30 minutes)
- Password change forces token refresh

**Token Security:**
- Short-lived access tokens (30 minutes)
- Long-lived refresh tokens (7 days)
- Secure storage recommendations (httpOnly cookies)
- Token revocation on logout

**API Key Security:**
- SHA-256 hashing for storage
- Key prefix for identification without exposing full key
- Scope-based permissions
- Automatic expiration
- Rate limiting per key

**Vietnamese PDPL Compliance:**
- Audit all authentication events
- Bilingual error messages
- Vietnamese timezone for all timestamps
- Multi-tenant isolation enforced

---

## Vietnamese PDPL Compliance Notes

**Bilingual Support:**
- All error messages in Vietnamese (primary) + English (fallback)
- Role names and descriptions bilingual
- Permission names bilingual
- Audit logs bilingual

**Data Protection:**
- Password hashes never exposed in logs
- API keys hashed before storage
- Sensitive fields encrypted at rest (future enhancement)
- Audit trail for all security events

**Timezone Handling:**
- All timestamps in Asia/Ho_Chi_Minh timezone
- Login timestamps, token expiration, audit logs

---

**Document Status:** PLANNING COMPLETE  
**Ready to Start:** Phase 7.1 (JWT Authentication Infrastructure)  
**Estimated Completion:** 3 weeks from start date

**Next Action:** Begin Phase 7.1 implementation or review plan with stakeholders.
