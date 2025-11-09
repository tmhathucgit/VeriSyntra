# Task 1.1.1: JWT Authentication Infrastructure - TODO List

**VeriSyntra - Phase 1 Authentication Implementation**  
**Task:** JWT Authentication Infrastructure  
**Estimated Time:** 6-8 hours  
**Priority:** 🔴 CRITICAL BLOCKER  
**Status:** NOT STARTED  
**Created:** November 7, 2025

---

## Overview

This is the **FIRST TASK** of Phase 1 Authentication implementation. It establishes the foundational JWT (JSON Web Token) authentication system that all subsequent authentication features will build upon.

**Why This Task First:**
- Foundation for all authentication features
- No dependencies - can start immediately
- Required before user endpoints, RBAC, or API keys
- Blocks production deployment

---

## Prerequisites

### Current System Status
- ✅ Database is COMPLETE (DOC11 Phases 1-6)
- ✅ PostgreSQL schema with 9 tables operational
- ✅ FastAPI endpoints exist (432+ lines) but UNSECURED
- ❌ NO authentication layer
- ❌ NO security on endpoints
- 🔴 CANNOT deploy to production

### Required Environment
- Python 3.11+ installed
- PostgreSQL database running
- Redis installed (for token blacklist)
- Backend directory: `backend/veri_ai_data_inventory/`

---

## Task Breakdown

### Step 1: Install Dependencies (30 minutes)

**Action:** Add JWT authentication packages to requirements

- [ ] **1.1** Update `backend/veri_ai_data_inventory/requirements.txt`
  ```txt
  # JWT Authentication
  PyJWT==2.8.0
  python-jose[cryptography]==3.3.0
  passlib[bcrypt]==1.7.4
  bcrypt==4.1.1
  python-multipart==0.0.6
  
  # Redis for token blacklist
  redis==5.0.1
  ```

- [ ] **1.2** Install packages
  ```bash
  cd backend/veri_ai_data_inventory
  pip install -r requirements.txt
  ```

- [ ] **1.3** Verify installations
  ```bash
  python -c "import jwt; import jose; import passlib; import redis; print('All packages installed successfully')"
  ```

**Validation:**
- [ ] All packages import without errors
- [ ] Redis client connects successfully

---

### Step 2: Configure Environment Variables (30 minutes)

**Action:** Set up JWT configuration in environment

- [ ] **2.1** Create/update `.env` file in `backend/veri_ai_data_inventory/`
  ```bash
  # JWT Configuration
  JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-min-32-chars
  JWT_ALGORITHM=HS256
  JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
  JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
  
  # Redis Configuration (Token Blacklist)
  REDIS_HOST=localhost
  REDIS_PORT=6379
  REDIS_DB=1
  REDIS_PASSWORD=
  
  # Security
  BCRYPT_ROUNDS=12
  ```

- [ ] **2.2** Generate secure JWT secret key
  ```python
  # Run this to generate a secure key
  import secrets
  print(secrets.token_urlsafe(32))
  ```

- [ ] **2.3** Update `backend/veri_ai_data_inventory/config/settings.py`
  ```python
  from pydantic_settings import BaseSettings
  
  class Settings(BaseSettings):
      # ... existing settings ...
      
      # JWT Authentication
      JWT_SECRET_KEY: str
      JWT_ALGORITHM: str = "HS256"
      JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
      JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
      
      # Redis Configuration
      REDIS_HOST: str = "localhost"
      REDIS_PORT: int = 6379
      REDIS_DB: int = 1
      REDIS_PASSWORD: str = ""
      
      # Security
      BCRYPT_ROUNDS: int = 12
      
      class Config:
          env_file = ".env"
          case_sensitive = True
  
  settings = Settings()
  ```

**Validation:**
- [ ] Settings load without errors
- [ ] JWT_SECRET_KEY is set and secure (min 32 characters)
- [ ] Redis connection settings configured

---

### Step 3: Create JWT Handler Module (2-3 hours)

**Action:** Implement token generation and validation logic

- [ ] **3.1** Create directory structure
  ```bash
  mkdir -p backend/veri_ai_data_inventory/auth
  ```

- [ ] **3.2** Create `backend/veri_ai_data_inventory/auth/__init__.py`
  ```python
  """
  VeriSyntra Authentication Module
  Vietnamese PDPL 2025 Compliance Platform
  """
  from .jwt_handler import (
      create_access_token,
      create_refresh_token,
      verify_token,
      get_token_payload
  )
  
  __all__ = [
      "create_access_token",
      "create_refresh_token", 
      "verify_token",
      "get_token_payload"
  ]
  ```

- [ ] **3.3** Create `backend/veri_ai_data_inventory/auth/jwt_handler.py`
  
  **File Structure:**
  ```python
  """
  JWT Token Handler for VeriSyntra Authentication
  Handles access token and refresh token generation/validation
  """
  
  from datetime import datetime, timedelta
  from typing import Dict, Optional, Any
  import jwt
  from jwt.exceptions import InvalidTokenError
  import logging
  
  from config.settings import settings
  
  logger = logging.getLogger(__name__)
  
  # Token type constants
  TOKEN_TYPE_ACCESS = "access"
  TOKEN_TYPE_REFRESH = "refresh"
  ```

- [ ] **3.3.1** Implement `create_access_token()` function
  ```python
  def create_access_token(
      data: Dict[str, Any],
      expires_delta: Optional[timedelta] = None
  ) -> str:
      """
      Create JWT access token for Vietnamese business user
      
      Args:
          data: Token payload (user_id, tenant_id, email, role)
          expires_delta: Custom expiration (default: 30 minutes)
      
      Returns:
          Encoded JWT access token string
      """
      to_encode = data.copy()
      
      # Set expiration
      if expires_delta:
          expire = datetime.utcnow() + expires_delta
      else:
          expire = datetime.utcnow() + timedelta(
              minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
          )
      
      # Add standard claims
      to_encode.update({
          "exp": expire,
          "iat": datetime.utcnow(),
          "type": TOKEN_TYPE_ACCESS,
          "iss": "verisyntra-api"  # Issuer
      })
      
      # Encode token
      encoded_jwt = jwt.encode(
          to_encode,
          settings.JWT_SECRET_KEY,
          algorithm=settings.JWT_ALGORITHM
      )
      
      logger.info(f"[OK] Access token created for user: {data.get('user_id')}")
      return encoded_jwt
  ```

- [ ] **3.3.2** Implement `create_refresh_token()` function
  ```python
  def create_refresh_token(
      data: Dict[str, Any],
      expires_delta: Optional[timedelta] = None
  ) -> str:
      """
      Create JWT refresh token for Vietnamese business user
      
      Args:
          data: Token payload (user_id, tenant_id)
          expires_delta: Custom expiration (default: 7 days)
      
      Returns:
          Encoded JWT refresh token string
      """
      to_encode = data.copy()
      
      # Set expiration
      if expires_delta:
          expire = datetime.utcnow() + expires_delta
      else:
          expire = datetime.utcnow() + timedelta(
              days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
          )
      
      # Add standard claims
      to_encode.update({
          "exp": expire,
          "iat": datetime.utcnow(),
          "type": TOKEN_TYPE_REFRESH,
          "iss": "verisyntra-api"
      })
      
      # Encode token
      encoded_jwt = jwt.encode(
          to_encode,
          settings.JWT_SECRET_KEY,
          algorithm=settings.JWT_ALGORITHM
      )
      
      logger.info(f"[OK] Refresh token created for user: {data.get('user_id')}")
      return encoded_jwt
  ```

- [ ] **3.3.3** Implement `verify_token()` function
  ```python
  def verify_token(
      token: str,
      expected_type: str = TOKEN_TYPE_ACCESS
  ) -> Dict[str, Any]:
      """
      Verify and decode JWT token
      
      Args:
          token: JWT token string
          expected_type: Expected token type ('access' or 'refresh')
      
      Returns:
          Decoded token payload
      
      Raises:
          InvalidTokenError: If token invalid, expired, or wrong type
      """
      try:
          # Decode and verify token
          payload = jwt.decode(
              token,
              settings.JWT_SECRET_KEY,
              algorithms=[settings.JWT_ALGORITHM]
          )
          
          # Verify token type
          token_type = payload.get("type")
          if token_type != expected_type:
              raise InvalidTokenError(
                  f"Wrong token type. Expected: {expected_type}, Got: {token_type}"
              )
          
          logger.info(f"[OK] Token verified for user: {payload.get('user_id')}")
          return payload
          
      except jwt.ExpiredSignatureError:
          logger.warning("[ERROR] Token expired")
          raise InvalidTokenError("Token expired - Mã thông báo đã hết hạn")
      
      except jwt.InvalidTokenError as e:
          logger.warning(f"[ERROR] Invalid token: {str(e)}")
          raise InvalidTokenError(f"Invalid token - Mã thông báo không hợp lệ: {str(e)}")
  ```

- [ ] **3.3.4** Implement `get_token_payload()` function
  ```python
  def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
      """
      Extract payload from token without verification (for debugging)
      
      Args:
          token: JWT token string
      
      Returns:
          Decoded payload or None if invalid
      """
      try:
          # Decode without verification
          payload = jwt.decode(
              token,
              options={"verify_signature": False}
          )
          return payload
      except Exception as e:
          logger.error(f"[ERROR] Failed to decode token: {str(e)}")
          return None
  ```

**Validation:**
- [ ] All functions defined with proper type hints
- [ ] Vietnamese bilingual error messages included
- [ ] Logging statements added
- [ ] Proper exception handling

---

### Step 4: Create Redis Token Blacklist (1-2 hours)

**Action:** Implement token revocation system

- [ ] **4.1** Create `backend/veri_ai_data_inventory/auth/token_blacklist.py`
  ```python
  """
  Token Blacklist using Redis
  Manages revoked JWT tokens for logout functionality
  """
  
  import redis
  from typing import Optional
  from datetime import timedelta
  import logging
  
  from config.settings import settings
  
  logger = logging.getLogger(__name__)
  
  
  class TokenBlacklist:
      """Redis-based token blacklist for revoked tokens"""
      
      def __init__(self):
          """Initialize Redis connection"""
          self.redis_client = redis.Redis(
              host=settings.REDIS_HOST,
              port=settings.REDIS_PORT,
              db=settings.REDIS_DB,
              password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
              decode_responses=True
          )
          
          # Test connection
          try:
              self.redis_client.ping()
              logger.info("[OK] Token blacklist Redis connection established")
          except redis.ConnectionError as e:
              logger.error(f"[ERROR] Redis connection failed: {str(e)}")
              raise
      
      def add_token(
          self,
          token: str,
          expires_in_minutes: int = 30
      ) -> bool:
          """
          Add token to blacklist
          
          Args:
              token: JWT token to blacklist
              expires_in_minutes: Token TTL in Redis (match token expiration)
          
          Returns:
              True if successful
          """
          try:
              # Store token with expiration
              key = f"blacklist:{token}"
              self.redis_client.setex(
                  key,
                  timedelta(minutes=expires_in_minutes),
                  "revoked"
              )
              logger.info("[OK] Token added to blacklist")
              return True
          except Exception as e:
              logger.error(f"[ERROR] Failed to blacklist token: {str(e)}")
              return False
      
      def is_blacklisted(self, token: str) -> bool:
          """
          Check if token is blacklisted
          
          Args:
              token: JWT token to check
          
          Returns:
              True if token is blacklisted (revoked)
          """
          try:
              key = f"blacklist:{token}"
              return self.redis_client.exists(key) > 0
          except Exception as e:
              logger.error(f"[ERROR] Failed to check blacklist: {str(e)}")
              # Fail secure - treat as blacklisted if Redis error
              return True
      
      def remove_token(self, token: str) -> bool:
          """
          Remove token from blacklist (rare use case)
          
          Args:
              token: JWT token to remove
          
          Returns:
              True if successful
          """
          try:
              key = f"blacklist:{token}"
              self.redis_client.delete(key)
              logger.info("[OK] Token removed from blacklist")
              return True
          except Exception as e:
              logger.error(f"[ERROR] Failed to remove token: {str(e)}")
              return False
  
  
  # Global instance
  token_blacklist = TokenBlacklist()
  ```

- [ ] **4.2** Update `backend/veri_ai_data_inventory/auth/__init__.py`
  ```python
  from .jwt_handler import (
      create_access_token,
      create_refresh_token,
      verify_token,
      get_token_payload
  )
  from .token_blacklist import token_blacklist
  
  __all__ = [
      "create_access_token",
      "create_refresh_token",
      "verify_token",
      "get_token_payload",
      "token_blacklist"
  ]
  ```

**Validation:**
- [ ] Redis connection established
- [ ] Tokens can be added to blacklist
- [ ] Blacklist check works correctly
- [ ] TTL expires tokens automatically

---

### Step 5: Create Unit Tests (1-2 hours)

**Action:** Test JWT token operations

- [ ] **5.1** Create `backend/veri_ai_data_inventory/tests/test_jwt_auth.py`
  ```python
  """
  Unit tests for JWT authentication
  """
  
  import pytest
  from datetime import timedelta
  import time
  
  from auth.jwt_handler import (
      create_access_token,
      create_refresh_token,
      verify_token,
      TOKEN_TYPE_ACCESS,
      TOKEN_TYPE_REFRESH
  )
  from auth.token_blacklist import token_blacklist
  from jwt.exceptions import InvalidTokenError
  
  
  class TestJWTTokens:
      """Test JWT token creation and verification"""
      
      def test_create_access_token(self):
          """Test access token creation"""
          payload = {
              "user_id": "test-user-123",
              "tenant_id": "tenant-abc",
              "email": "test@example.com",
              "role": "admin"
          }
          
          token = create_access_token(payload)
          
          assert isinstance(token, str)
          assert len(token) > 0
      
      def test_create_refresh_token(self):
          """Test refresh token creation"""
          payload = {
              "user_id": "test-user-123",
              "tenant_id": "tenant-abc"
          }
          
          token = create_refresh_token(payload)
          
          assert isinstance(token, str)
          assert len(token) > 0
      
      def test_verify_access_token(self):
          """Test access token verification"""
          payload = {
              "user_id": "test-user-123",
              "tenant_id": "tenant-abc",
              "email": "test@example.com"
          }
          
          token = create_access_token(payload)
          decoded = verify_token(token, TOKEN_TYPE_ACCESS)
          
          assert decoded["user_id"] == payload["user_id"]
          assert decoded["tenant_id"] == payload["tenant_id"]
          assert decoded["type"] == TOKEN_TYPE_ACCESS
      
      def test_verify_refresh_token(self):
          """Test refresh token verification"""
          payload = {
              "user_id": "test-user-123",
              "tenant_id": "tenant-abc"
          }
          
          token = create_refresh_token(payload)
          decoded = verify_token(token, TOKEN_TYPE_REFRESH)
          
          assert decoded["user_id"] == payload["user_id"]
          assert decoded["type"] == TOKEN_TYPE_REFRESH
      
      def test_wrong_token_type(self):
          """Test token type validation"""
          payload = {"user_id": "test-user"}
          
          access_token = create_access_token(payload)
          
          # Try to verify access token as refresh token
          with pytest.raises(InvalidTokenError):
              verify_token(access_token, TOKEN_TYPE_REFRESH)
      
      def test_expired_token(self):
          """Test expired token rejection"""
          payload = {"user_id": "test-user"}
          
          # Create token with 1 second expiration
          token = create_access_token(
              payload,
              expires_delta=timedelta(seconds=1)
          )
          
          # Wait for expiration
          time.sleep(2)
          
          # Should raise expired error
          with pytest.raises(InvalidTokenError):
              verify_token(token)
  
  
  class TestTokenBlacklist:
      """Test token blacklist functionality"""
      
      def test_add_token_to_blacklist(self):
          """Test adding token to blacklist"""
          token = "test-token-123"
          
          result = token_blacklist.add_token(token, expires_in_minutes=1)
          
          assert result is True
          assert token_blacklist.is_blacklisted(token) is True
      
      def test_blacklist_check(self):
          """Test blacklist status check"""
          token = "test-token-456"
          
          # Should not be blacklisted initially
          assert token_blacklist.is_blacklisted(token) is False
          
          # Add to blacklist
          token_blacklist.add_token(token)
          
          # Should be blacklisted now
          assert token_blacklist.is_blacklisted(token) is True
      
      def test_remove_from_blacklist(self):
          """Test removing token from blacklist"""
          token = "test-token-789"
          
          # Add to blacklist
          token_blacklist.add_token(token)
          assert token_blacklist.is_blacklisted(token) is True
          
          # Remove from blacklist
          result = token_blacklist.remove_token(token)
          
          assert result is True
          assert token_blacklist.is_blacklisted(token) is False
  ```

- [ ] **5.2** Run tests
  ```bash
  cd backend/veri_ai_data_inventory
  pytest tests/test_jwt_auth.py -v
  ```

**Validation:**
- [ ] All tests pass
- [ ] Token creation works
- [ ] Token verification works
- [ ] Expiration handling works
- [ ] Blacklist operations work

---

### Step 6: Integration Documentation (30 minutes)

**Action:** Document the JWT authentication system

- [ ] **6.1** Create `backend/veri_ai_data_inventory/auth/README.md`
  ```markdown
  # VeriSyntra Authentication Module
  
  JWT-based authentication for Vietnamese PDPL 2025 compliance platform.
  
  ## Components
  
  - `jwt_handler.py` - Token generation and validation
  - `token_blacklist.py` - Revoked token management (Redis)
  
  ## Token Types
  
  1. **Access Token** - Short-lived (30 minutes)
  2. **Refresh Token** - Long-lived (7 days)
  
  ## Usage
  
  ### Create Tokens
  ```python
  from auth import create_access_token, create_refresh_token
  
  payload = {
      "user_id": "user-123",
      "tenant_id": "tenant-abc",
      "email": "user@company.vn",
      "role": "admin"
  }
  
  access_token = create_access_token(payload)
  refresh_token = create_refresh_token(payload)
  ```
  
  ### Verify Tokens
  ```python
  from auth import verify_token, TOKEN_TYPE_ACCESS
  from jwt.exceptions import InvalidTokenError
  
  try:
      payload = verify_token(token, TOKEN_TYPE_ACCESS)
      user_id = payload["user_id"]
  except InvalidTokenError as e:
      print(f"Invalid token: {e}")
  ```
  
  ### Revoke Tokens (Logout)
  ```python
  from auth import token_blacklist
  
  token_blacklist.add_token(access_token, expires_in_minutes=30)
  ```
  
  ## Configuration
  
  Environment variables in `.env`:
  - `JWT_SECRET_KEY` - Secret key for signing tokens
  - `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` - Access token lifetime
  - `JWT_REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token lifetime
  - `REDIS_HOST`, `REDIS_PORT` - Token blacklist storage
  ```

- [ ] **6.2** Add comments to code explaining Vietnamese business context

**Validation:**
- [ ] Documentation is clear and complete
- [ ] Usage examples work
- [ ] Configuration documented

---

## Success Criteria

### Completion Checklist

- [ ] All dependencies installed and verified
- [ ] Environment variables configured
- [ ] JWT handler module created with all functions
- [ ] Token blacklist implemented with Redis
- [ ] Unit tests created and passing
- [ ] Documentation complete

### Functional Validation

- [ ] Can create access tokens with correct expiration
- [ ] Can create refresh tokens with correct expiration
- [ ] Can verify valid tokens
- [ ] Can reject expired tokens
- [ ] Can reject invalid tokens
- [ ] Can add tokens to blacklist
- [ ] Can check blacklist status
- [ ] Redis connection stable

### Code Quality

- [ ] Type hints on all functions
- [ ] Vietnamese bilingual error messages
- [ ] Logging statements in place
- [ ] Exception handling implemented
- [ ] Code follows VeriSyntra standards (no emojis, proper diacritics)

---

## Next Steps After Completion

Once this task is complete, proceed to:

**Task 1.1.2: User Authentication Endpoints (4-5 hours)**
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- POST /api/v1/auth/logout
- POST /api/v1/auth/register
- GET /api/v1/auth/me

This will use the JWT handler created in this task.

---

## Troubleshooting

### Common Issues

**Issue:** Redis connection fails
- **Solution:** Ensure Redis is running: `redis-cli ping` should return "PONG"
- **Solution:** Check Redis host/port in `.env`

**Issue:** Token signature verification fails
- **Solution:** Ensure JWT_SECRET_KEY is same for creation and verification
- **Solution:** Check JWT_ALGORITHM matches in settings

**Issue:** Tests fail on token expiration
- **Solution:** Increase sleep time in expiration test
- **Solution:** Check system time is synchronized

---

**Task Status:** NOT STARTED  
**Estimated Completion:** 6-8 hours  
**Blocking:** All other authentication tasks  
**Document Reference:** DOC12_PHASE_7_AUTH_IMPLEMENTATION_PLAN.md
