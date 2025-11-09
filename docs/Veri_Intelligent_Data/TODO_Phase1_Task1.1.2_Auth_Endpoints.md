# ✅ COMPLETE - Task 1.1.2: User Authentication Endpoints

**Status:** ✅ **COMPLETE** - Production Ready (November 7-8, 2025)  
**Project:** VeriSyntra Vietnamese PDPL 2025 Compliance Platform  
**Phase:** Phase 1 - Authentication & Write Scaling  
**Task:** 1.1.2 User Authentication Endpoints  
**Completion Date:** November 8, 2025  
**Actual Effort:** 4-5 hours  
**Schema:** Phase 2 (Email-based authentication)  
**Testing:** 82/82 tests passing (100% success rate)

**📖 COMPLETION REFERENCE:** See `COMPLETE_Phase1_Task1.1.2_Auth_Endpoints.md` for full implementation details, testing results, and production deployment guide.

---

## Implementation Summary

This TODO document guided the successful implementation of email-based authentication endpoints with Phase 2 PostgreSQL schema. All objectives achieved:

- ✅ 5 authentication endpoints operational (register, login, /me, refresh, logout)
- ✅ Email-based authentication (NO username - Phase 2 schema)
- ✅ Multi-tenant support with foreign key constraints
- ✅ Vietnamese business context (bilingual errors, cultural fields)
- ✅ JWT token management with Redis blacklist
- ✅ Comprehensive testing (82/82 tests passing)
- ✅ Production-ready security implementation

**Next Task:** Task 1.1.3 - Role-Based Access Control (RBAC)

---

## Original TODO Content (Completed Implementation Guide)

---

## CRITICAL CONTEXT: Phase 2 Schema (Email-Based)

From conversation history and `Phase2_PostgreSQL_Integration_Complete.md`:
- **AUTHORITATIVE SCHEMA:** Phase 2 (NOT Step 1 username-based docs)
- **Authentication Method:** Email-only (NO username field)
- **Column Names:** `hashed_password` (NOT password_hash), `last_login` (NOT last_login_at)
- **Key Fields:** `email`, `hashed_password`, `full_name`, `full_name_vi`, `phone_number`, `tenant_id`, `role`

**IMPORTANT:** All code must use Phase 2 schema. Ignore any Step 1 documentation that references username-based authentication.

---

## Prerequisites (All Complete from Task 1.1.1)

- [x] JWT handler (`backend/auth/jwt_handler.py`)
- [x] Password utilities (`backend/auth/password_utils.py`)
- [x] Token blacklist (`backend/auth/token_blacklist.py`)
- [x] Redis running (localhost:6379, DB 1)
- [x] 72 unit tests passing
- [x] Integration guide (`JWT_Authentication_Integration_Guide.md`)

---

## Step 1: Verify Phase 2 Database Schema (30 min)

### 1.1 Check PostgreSQL Users Table

```powershell
# Connect to PostgreSQL container
docker exec -it verisyntra-postgres psql -U verisyntra -d verisyntra

# Check users table schema
\d users

# Expected columns (Phase 2):
# - user_id (UUID, PK)
# - email (VARCHAR, UNIQUE per tenant) - NOT username
# - hashed_password (VARCHAR) - NOT password_hash
# - full_name (VARCHAR)
# - full_name_vi (VARCHAR) - Vietnamese name with diacritics
# - phone_number (VARCHAR, OPTIONAL)
# - tenant_id (UUID, FK to tenants)
# - role (VARCHAR) - admin, dpo, compliance_manager, staff, auditor, viewer
# - is_active (BOOLEAN)
# - last_login (TIMESTAMP) - NOT last_login_at
# - created_at, updated_at (TIMESTAMP)
```

**Tasks:**
- [ ] Verify `email` column exists (NOT username)
- [ ] Verify `hashed_password` column name (NOT password_hash)
- [ ] Verify `last_login` column name (NOT last_login_at)
- [ ] Verify `full_name_vi` supports Vietnamese diacritics
- [ ] Verify `tenants` table exists (FK requirement)
- [ ] Document schema in notes

**VeriSyntra Standards:**
- [x] ASCII-only SQL commands
- [x] Database identifiers WITHOUT diacritics (email, phone_number)
- [x] Vietnamese comments with proper diacritics

---

## Step 2: Pydantic Schemas (45 min)

### 2.1 Create `backend/auth/schemas.py`

```python
"""
Authentication Pydantic Schemas - Phase 2 Email-Based
VeriSyntra Standards: Bilingual, Vietnamese-first, NO emoji
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

# Registration Request (Email-based, Phase 2)
class UserRegisterRequest(BaseModel):
    """
    User registration - Email authentication (Phase 2)
    NO username field - email is primary identifier
    """
    email: EmailStr = Field(..., description="Email address (unique per tenant)")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    full_name: str = Field(..., min_length=1, max_length=255)
    full_name_vi: str = Field(..., description="Họ tên (tiếng Việt với dấu)")
    phone_number: Optional[str] = Field(None, description="Số điện thoại")
    tenant_id: str = Field(..., description="Tenant UUID")
    
    @validator('phone_number')
    def validate_vietnamese_phone(cls, v):
        """Vietnamese phone: +84 or 0 prefix, 9-10 digits"""
        if v and not re.match(r'^(\+84|0)[1-9][0-9]{8,9}$', v):
            raise ValueError('Invalid Vietnamese phone number')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "nguyen.van.a@verisyntra.vn",
                "password": "SecurePass123!",
                "full_name": "Nguyen Van A",
                "full_name_vi": "Nguyễn Văn A",
                "phone_number": "+84901234567",
                "tenant_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }

# Login Request (Email-based, Phase 2)
class UserLoginRequest(BaseModel):
    """Login with email and password (NO username)"""
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")

# Token Response
class TokenResponse(BaseModel):
    """JWT tokens response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes

# Current User Response
class CurrentUserResponse(BaseModel):
    """Current user profile (Vietnamese context)"""
    user_id: str
    email: str  # NOT username
    full_name: str
    full_name_vi: str
    phone_number: Optional[str]
    tenant_id: str
    role: str
    is_active: bool
    last_login: Optional[datetime]  # NOT last_login_at
    created_at: datetime
    
    class Config:
        from_attributes = True

# Bilingual Error Messages (Vietnamese-first)
class AuthErrorMessages:
    """VeriSyntra Standard: Bilingual with _vi suffix"""
    
    INVALID_CREDENTIALS = {
        "vi": "Email hoặc mật khẩu không đúng",
        "en": "Invalid email or password"
    }
    
    EMAIL_EXISTS = {
        "vi": "Email đã được sử dụng trong tenant này",
        "en": "Email already registered in this tenant"
    }
    
    USER_INACTIVE = {
        "vi": "Tài khoản đã bị vô hiệu hóa",
        "en": "Account has been deactivated"
    }
    
    INVALID_TOKEN = {
        "vi": "Token không hợp lệ hoặc đã hết hạn",
        "en": "Invalid or expired token"
    }
    
    TOKEN_BLACKLISTED = {
        "vi": "Token đã bị thu hồi",
        "en": "Token has been revoked"
    }
```

**Tasks:**
- [ ] Create file with email-based schemas (NO username)
- [ ] Add Vietnamese phone validation
- [ ] Add bilingual error messages
- [ ] Add Vietnamese examples with diacritics
- [ ] Test schema validation

**VeriSyntra Standards:**
- [x] NO emoji in code
- [x] Vietnamese diacritics in user-facing strings
- [x] NO diacritics in code identifiers (full_name_vi, phone_number)
- [x] Bilingual with _vi suffix pattern
- [x] Vietnamese-first (Vietnamese in primary position)

---

## Step 3: User CRUD Operations (45 min)

### 3.1 Update `backend/database/crud/user_crud.py`

```python
"""
User CRUD - Phase 2 Email-Based Authentication
VeriSyntra Standards: Dynamic code, Vietnamese context, NO emoji
"""

from sqlalchemy.orm import Session
from database.models.user import User
from auth.password_utils import hash_password, verify_password
from datetime import datetime
import uuid

class UserCRUD:
    """Phase 2: Email-based authentication CRUD"""
    
    @staticmethod
    def create_user(
        db: Session,
        email: str,
        password: str,
        full_name: str,
        tenant_id: str,
        full_name_vi: str = None,
        phone_number: str = None,
        role: str = "viewer"
    ) -> User:
        """
        Create user - Phase 2 email-based
        
        Args:
            email: Email address (unique per tenant)
            password: Plain password (will be hashed)
            full_name: Full name (English)
            tenant_id: Tenant UUID
            full_name_vi: Họ tên (tiếng Việt)
            phone_number: Số điện thoại (optional)
            role: User role (default: viewer)
        """
        hashed_password = hash_password(password)
        
        user = User(
            user_id=uuid.uuid4(),
            email=email,
            hashed_password=hashed_password,  # Phase 2: hashed_password
            full_name=full_name,
            full_name_vi=full_name_vi or full_name,
            phone_number=phone_number,
            tenant_id=uuid.UUID(tenant_id),
            role=role,
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str, tenant_id: str = None) -> User:
        """
        Get user by email (Phase 2: email-based, NOT username)
        
        Args:
            email: Email address
            tenant_id: Optional tenant filter
        """
        query = db.query(User).filter(User.email == email)
        
        if tenant_id:
            query = query.filter(User.tenant_id == uuid.UUID(tenant_id))
        
        return query.first()
    
    @staticmethod
    def verify_user_password(db: Session, email: str, password: str) -> User:
        """
        Verify credentials and update last_login (Phase 2)
        
        Args:
            email: Email address (NOT username)
            password: Plain password
            
        Returns:
            User if valid, None if invalid
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        # Update last_login (Phase 2: last_login NOT last_login_at)
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
```

**Tasks:**
- [ ] Update/create CRUD with email-based methods
- [ ] Use `hashed_password` column (NOT password_hash)
- [ ] Use `last_login` column (NOT last_login_at)
- [ ] Remove any username references
- [ ] Add Vietnamese field support
- [ ] Test CRUD operations

**VeriSyntra Standards:**
- [x] Dynamic code (parameterized functions)
- [x] Vietnamese diacritics in docstrings/comments
- [x] Database column names without diacritics
- [x] NO emoji characters

---

## Step 4: Authentication Dependencies (30 min)

### 4.1 Create `backend/auth/dependencies.py`

```python
"""
FastAPI Security Dependencies - Phase 2
VeriSyntra Standards: Multi-layer security, bilingual errors
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.session import get_db
from database.crud.user_crud import UserCRUD
from auth.jwt_handler import verify_access_token
from auth.token_blacklist import is_token_blacklisted
from auth.schemas import AuthErrorMessages
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Multi-layer security:
    1. Token blacklist check (logout)
    2. JWT verification (signature + expiry)
    3. User database lookup
    4. Active status check
    
    Returns: User with Vietnamese context
    """
    # Check blacklist
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": AuthErrorMessages.TOKEN_BLACKLISTED["en"],
                "message_vi": AuthErrorMessages.TOKEN_BLACKLISTED["vi"]
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify JWT
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": AuthErrorMessages.INVALID_TOKEN["en"],
                "message_vi": AuthErrorMessages.INVALID_TOKEN["vi"]
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    user_id: str = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": AuthErrorMessages.INVALID_TOKEN["en"],
                "message_vi": AuthErrorMessages.INVALID_TOKEN["vi"]
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    from database.models.user import User
    user = db.query(User).filter(User.user_id == uuid.UUID(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "User not found",
                "message_vi": "Không tìm thấy người dùng"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": AuthErrorMessages.USER_INACTIVE["en"],
                "message_vi": AuthErrorMessages.USER_INACTIVE["vi"]
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
```

**Tasks:**
- [ ] Create dependencies file
- [ ] Implement multi-layer security
- [ ] Add bilingual error messages
- [ ] Test dependency with valid/invalid tokens

**VeriSyntra Standards:**
- [x] Bilingual output with _vi suffix
- [x] Vietnamese-first error messages
- [x] NO emoji in code
- [x] Dynamic validation

---

## Step 5: Authentication Endpoints (60 min)

### 5.1 Create `backend/api/routes/auth.py`

**CRITICAL:** Use `data={}` format for token creation (from Task 1.1.1)

```python
"""
Authentication REST API - Phase 2 Email-Based
VeriSyntra Standards: Vietnamese-first, bilingual, NO emoji
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from database.crud.user_crud import UserCRUD
from auth.schemas import (
    UserRegisterRequest, UserLoginRequest, TokenResponse,
    CurrentUserResponse, AuthErrorMessages
)
from auth.jwt_handler import create_access_token, create_refresh_token, verify_refresh_token
from auth.token_blacklist import blacklist_token, get_token_ttl, is_token_blacklisted
from auth.dependencies import get_current_user, oauth2_scheme

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register", response_model=CurrentUserResponse, status_code=201)
async def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Register new user (email-based, Phase 2)
    
    Vietnamese Context:
    - Email unique per tenant
    - Vietnamese names with diacritics (full_name_vi)
    - Vietnamese phone validation
    """
    # Check email exists (email + tenant_id unique)
    existing = UserCRUD.get_user_by_email(db, request.email, request.tenant_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": AuthErrorMessages.EMAIL_EXISTS["en"],
                "message_vi": AuthErrorMessages.EMAIL_EXISTS["vi"]
            }
        )
    
    # Create user
    user = UserCRUD.create_user(
        db=db,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        full_name_vi=request.full_name_vi,
        phone_number=request.phone_number,
        tenant_id=request.tenant_id
    )
    
    return user

@router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Login with email/password (Phase 2: NO username)
    
    Security:
    - Password verification (bcrypt)
    - JWT tokens (30 min access, 7 day refresh)
    - Updates last_login timestamp
    """
    # Verify credentials (email + password)
    user = UserCRUD.verify_user_password(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={
                "message": AuthErrorMessages.INVALID_CREDENTIALS["en"],
                "message_vi": AuthErrorMessages.INVALID_CREDENTIALS["vi"]
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail={
                "message": AuthErrorMessages.USER_INACTIVE["en"],
                "message_vi": AuthErrorMessages.USER_INACTIVE["vi"]
            }
        )
    
    # CRITICAL: Use data={} format from Task 1.1.1
    access_token = create_access_token(
        data={
            "user_id": str(user.user_id),
            "email": user.email,
            "tenant_id": str(user.tenant_id),
            "role": user.role
        }
    )
    
    refresh_token = create_refresh_token(
        data={
            "user_id": str(user.user_id),
            "email": user.email
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user profile (Vietnamese context)"""
    return current_user

@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token"""
    if is_token_blacklisted(refresh_token):
        raise HTTPException(
            status_code=401,
            detail={
                "message": AuthErrorMessages.TOKEN_BLACKLISTED["en"],
                "message_vi": AuthErrorMessages.TOKEN_BLACKLISTED["vi"]
            }
        )
    
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail={
                "message": AuthErrorMessages.INVALID_TOKEN["en"],
                "message_vi": AuthErrorMessages.INVALID_TOKEN["vi"]
            }
        )
    
    user_id = payload.get("user_id")
    email = payload.get("email")
    
    from database.models.user import User
    import uuid
    user = db.query(User).filter(User.user_id == uuid.UUID(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "User not found or inactive",
                "message_vi": "Không tìm thấy người dùng hoặc tài khoản không hoạt động"
            }
        )
    
    # CRITICAL: Use data={} format
    new_access_token = create_access_token(
        data={
            "user_id": str(user.user_id),
            "email": user.email,
            "tenant_id": str(user.tenant_id),
            "role": user.role
        }
    )
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=refresh_token
    )

@router.post("/logout", status_code=204)
async def logout(token: str = Depends(oauth2_scheme), current_user = Depends(get_current_user)):
    """Logout - blacklist access token"""
    ttl = get_token_ttl(token)
    blacklist_token(token, ttl)
    return None
```

**Tasks:**
- [ ] Create 5 endpoints (register, login, /me, refresh, logout)
- [ ] Use email-based authentication (NO username)
- [ ] Use `data={}` token creation format
- [ ] Add bilingual error messages
- [ ] Register router in main app
- [ ] Test all endpoints

**VeriSyntra Standards:**
- [x] NO emoji in code
- [x] Bilingual errors with _vi suffix
- [x] Vietnamese diacritics in messages
- [x] Dynamic code (no hard-coding)

---

## Step 6: Integration Testing (45 min)

### 6.1 Create `backend/tests/test_auth_phase2.py`

```python
"""
Phase 2 Authentication Tests (Email-based)
VeriSyntra Standards: ASCII output, Vietnamese validation
"""

import requests
import time
import psycopg2
from psycopg2.extras import RealDictCursor

BASE_URL = "http://127.0.0.1:8000"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "verisyntra",
    "user": "verisyntra",
    "password": "verisyntra_dev_password"
}

def create_test_tenant():
    """Create tenant for user FK constraint"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            INSERT INTO tenants (tenant_id, name, name_vi, created_at)
            VALUES (
                '123e4567-e89b-12d3-a456-426614174000'::uuid,
                'VeriSyntra Test',
                'Công ty Kiểm thử VeriSyntra',
                NOW()
            )
            ON CONFLICT (tenant_id) DO NOTHING
        """)
        conn.commit()
        print("[OK] Tenant created")
    except Exception as e:
        print(f"[WARNING] Tenant: {e}")
    finally:
        cursor.close()
        conn.close()

def test_1_server_health():
    print("\n[TEST 1] Server health...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("[OK] Server healthy")

def test_2_user_registration():
    print("\n[TEST 2] Email-based registration...")
    create_test_tenant()
    
    payload = {
        "email": "nguyen.van.test@verisyntra.vn",
        "password": "TestPass123!",
        "full_name": "Nguyen Van Test",
        "full_name_vi": "Nguyễn Văn Test",
        "phone_number": "+84901234567",
        "tenant_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name_vi"] == payload["full_name_vi"]
    print(f"[OK] User registered: {data['email']}")

def test_3_duplicate_email():
    print("\n[TEST 3] Duplicate email prevention...")
    
    payload = {
        "email": "nguyen.van.test@verisyntra.vn",
        "password": "TestPass123!",
        "full_name": "Duplicate",
        "full_name_vi": "Người dùng trùng lặp",
        "tenant_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    
    error = response.json()
    assert "message_vi" in error["detail"]
    print(f"[OK] Duplicate rejected: {error['detail']['message_vi']}")

def test_4_login():
    print("\n[TEST 4] Email-based login...")
    
    payload = {
        "email": "nguyen.van.test@verisyntra.vn",
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    
    global ACCESS_TOKEN, REFRESH_TOKEN
    ACCESS_TOKEN = data["access_token"]
    REFRESH_TOKEN = data["refresh_token"]
    
    print("[OK] Login successful")

def test_5_get_current_user():
    print("\n[TEST 5] Get current user...")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == "nguyen.van.test@verisyntra.vn"
    assert "full_name_vi" in data
    
    print(f"[OK] User: {data['full_name_vi']}")

def test_6_token_refresh():
    print("\n[TEST 6] Token refresh...")
    
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/refresh",
        params={"refresh_token": REFRESH_TOKEN}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    print("[OK] Token refreshed")

def test_7_logout():
    print("\n[TEST 7] Logout...")
    
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.post(f"{BASE_URL}/api/v1/auth/logout", headers=headers)
    assert response.status_code == 204
    
    # Verify blacklisted
    time.sleep(1)
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
    
    print("[OK] Logout successful, token blacklisted")

if __name__ == "__main__":
    print("=" * 60)
    print("Phase 2 Authentication Tests (Email-based)")
    print("=" * 60)
    
    test_1_server_health()
    test_2_user_registration()
    test_3_duplicate_email()
    test_4_login()
    test_5_get_current_user()
    test_6_token_refresh()
    test_7_logout()
    
    print("\n" + "=" * 60)
    print("[OK] All 7 tests passed!")
    print("=" * 60)
```

**Tasks:**
- [ ] Create test file with email-based tests
- [ ] Add tenant creation (FK requirement)
- [ ] Test all 7 scenarios
- [ ] Verify Vietnamese diacritics preserved
- [ ] Verify bilingual error messages

**VeriSyntra Standards:**
- [x] ASCII-only output markers ([OK], [TEST], [WARNING])
- [x] Vietnamese diacritics in test data
- [x] NO emoji characters
- [x] Dynamic test data

---

## Step 7: Manual Testing & Validation (30 min)

### 7.1 Test with curl

```powershell
# Test 1: Register
curl -X POST http://127.0.0.1:8000/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    \"email\": \"manual.test@verisyntra.vn\",
    \"password\": \"ManualTest123!\",
    \"full_name\": \"Manual Test\",
    \"full_name_vi\": \"Người dùng kiểm thử\",
    \"phone_number\": \"+84912345678\",
    \"tenant_id\": \"123e4567-e89b-12d3-a456-426614174000\"
  }'

# Test 2: Login (email-based)
curl -X POST http://127.0.0.1:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    \"email\": \"manual.test@verisyntra.vn\",
    \"password\": \"ManualTest123!\"
  }'

# Test 3: Get current user
curl -X GET http://127.0.0.1:8000/api/v1/auth/me `
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Tasks:**
- [ ] Test all endpoints manually
- [ ] Verify Vietnamese diacritics preserved
- [ ] Verify bilingual error messages
- [ ] Check database records

---

## Step 8: Documentation (30 min)

### 8.1 Update Swagger UI

**Tasks:**
- [ ] Start server: `python backend/main_prototype.py`
- [ ] Open http://127.0.0.1:8000/docs
- [ ] Verify 5 endpoints visible
- [ ] Test "Try it out" functionality
- [ ] Verify Vietnamese examples

### 8.2 Create Completion Document

**File:** `COMPLETE_Phase1_Task1.1.2_Auth_Endpoints.md`

**Tasks:**
- [ ] Document implementation summary
- [ ] List all endpoints (5 total)
- [ ] Include test results
- [ ] Mark Task 1.1.2 COMPLETE in main TODO

---

## Success Criteria

- [ ] All 5 endpoints working (register, login, /me, refresh, logout)
- [ ] Email-based authentication (NO username)
- [ ] Token creation uses `data={}` format
- [ ] Vietnamese fields preserved (full_name_vi, phone_number)
- [ ] Bilingual error messages working
- [ ] Phase 2 schema validated (hashed_password, last_login)
- [ ] All 7 integration tests passing
- [ ] Swagger UI documentation complete
- [ ] Manual testing validated

---

## VeriSyntra Standards Compliance

- [x] NO emoji characters anywhere
- [x] Vietnamese diacritics in user-facing strings
- [x] NO diacritics in database identifiers
- [x] Bilingual output with _vi suffix
- [x] Vietnamese-first approach
- [x] Dynamic code over hard-coding
- [x] ASCII-only terminal output

---

**Next Task:** 1.1.3 RBAC (8-10 hours)  
**Estimated Time:** 4-5 hours  
**Actual Time:** ___ hours
