# VeriAIDPO Microservice Migration - Phase 2: Authentication Integration

**Status:** Not Started  
**Estimated Time:** 1-2 hours  
**Objective:** Implement JWT token validation and permission checking for VeriAIDPO service

---

## Prerequisites

- [x] Phase 1 complete (service structure created, core components copied)
- [x] JWT_SECRET_KEY available from main backend environment
- [ ] Main backend authentication working (can generate valid JWT tokens)
- [ ] Understanding of RBAC permission system (require_permission decorator)

---

## Phase 2 Steps

### Step 2.1: Create JWT Validation Middleware (30 min)

**Objective:** Validate JWT tokens from main backend and extract user claims

**Tasks:**

1. **Create `app/auth/jwt_validator.py`**
   ```powershell
   # Working directory: C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\services\veri-aidpo-service
   New-Item -ItemType File -Path "app\auth\jwt_validator.py" -Force
   ```

2. **Implement token validation logic**
   - Import: `jose.jwt`, `fastapi.security.HTTPBearer`, `HTTPException`
   - Use shared JWT secret from `app.config.Settings`
   - Decode JWT token using `jwt_secret_key` and `jwt_algorithm`
   - Extract claims: `sub` (user_id), `role`, `tenant_id`, `permissions`
   - Return user dict with all claims
   - Raise 401 HTTPException for invalid tokens

3. **Add HTTPBearer security scheme**
   ```python
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   
   security = HTTPBearer()
   
   async def validate_token(
       credentials: HTTPAuthorizationCredentials = Security(security)
   ) -> dict:
       # Token validation logic
   ```

**Expected Output:**
```python
# Example return value
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "role": "dpo",
    "tenant_id": "company-123",
    "permissions": ["processing_activity.read", "veriaidpo.classify"]
}
```

**Validation:**
```powershell
# Check file exists and has no syntax errors
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\backend
python quick_validate.py "..\services\veri-aidpo-service\app\auth\jwt_validator.py"
```

**Completion Criteria:**
- [ ] `app/auth/jwt_validator.py` created
- [ ] `validate_token()` function implemented
- [ ] JWT decoding uses shared secret from config
- [ ] Returns user dict with user_id, role, tenant_id, permissions
- [ ] Raises 401 for invalid/missing tokens
- [ ] No coding standards violations (PASSED validation)

---

### Step 2.2: Create Permission Checking Dependency (30 min)

**Objective:** Implement `require_permission()` decorator for endpoint authorization

**Tasks:**

1. **Create `app/auth/permissions.py`**
   ```powershell
   New-Item -ItemType File -Path "app\auth\permissions.py" -Force
   ```

2. **Implement permission checking logic**
   - Import: `validate_token` from `jwt_validator`
   - Create `require_permission(permission: str)` factory function
   - Return async dependency that checks user permissions
   - Raise 403 HTTPException with bilingual error message (Vietnamese + English)
   - Include `required_permission` and `user_role` in error detail

3. **Bilingual error format (CRITICAL)**
   ```python
   raise HTTPException(
       status_code=403,
       detail={
           "error": f"Permission denied: {permission} required",
           "error_vi": f"Từ chối quyền truy cập: cần quyền {permission}",
           "required_permission": permission,
           "user_role": user.get("role")
       }
   )
   ```

**Validation:**
```powershell
python quick_validate.py "..\services\veri-aidpo-service\app\auth\permissions.py"
```

**Completion Criteria:**
- [ ] `app/auth/permissions.py` created
- [ ] `require_permission()` factory function implemented
- [ ] Returns async dependency using `validate_token`
- [ ] Checks if permission exists in user permissions list
- [ ] Raises 403 with bilingual error (error + error_vi fields)
- [ ] No coding standards violations (PASSED validation)

---

### Step 2.3: Update Classification Endpoint (30 min)

**Objective:** Integrate authentication into classification API endpoints

**Tasks:**

1. **Uncomment RBAC imports in `classification.py`**
   ```python
   # File: services/veri-aidpo-service/app/api/v1/endpoints/classification.py
   
   # BEFORE (Phase 1 - commented out):
   # from auth.rbac_dependencies import require_permission, CurrentUser
   
   # AFTER (Phase 2 - active):
   from app.auth.permissions import require_permission
   from app.auth.jwt_validator import validate_token
   ```

2. **Add authentication to endpoints**
   ```python
   @router.post("/classify")
   async def classify_endpoint(
       request: ClassificationRequest,
       user: dict = Depends(require_permission("veriaidpo.classify"))
   ):
       # Add tenant isolation
       if user.get("tenant_id"):
           # Validate request belongs to user's tenant
           pass
       
       # Existing classification logic
       ...
   ```

3. **Update all classification endpoints:**
   - `/classify` - requires `veriaidpo.classify` permission
   - `/normalize` - requires `veriaidpo.normalize` permission (if exists)
   - `/health` - public (no authentication)
   - `/model_status` - requires `veriaidpo.read` permission

4. **Add tenant isolation (optional but recommended)**
   - Extract `tenant_id` from user dict
   - Validate data access belongs to user's tenant
   - Return 403 if cross-tenant access attempted

**Validation:**
```powershell
python quick_validate.py "..\services\veri-aidpo-service\app\api\v1\endpoints\classification.py"
```

**Completion Criteria:**
- [ ] RBAC imports uncommented and updated
- [ ] `require_permission()` added to protected endpoints
- [ ] Correct permission strings used (veriaidpo.classify, veriaidpo.read)
- [ ] `/health` endpoint remains public (no auth)
- [ ] Tenant isolation implemented (optional)
- [ ] No undefined reference errors
- [ ] No coding standards violations (PASSED validation)

---

### Step 2.4: Update Main Application (15 min)

**Objective:** Register authentication middleware in main FastAPI app

**Tasks:**

1. **Update `main.py` imports**
   ```python
   # File: services/veri-aidpo-service/main.py
   
   from app.auth.jwt_validator import validate_token
   from app.auth.permissions import require_permission
   ```

2. **Add authentication documentation**
   ```python
   app = FastAPI(
       title=settings.service_name,
       version=settings.service_version,
       description="VeriAIDPO Classification Service with JWT authentication",
       docs_url="/docs",
       openapi_url="/openapi.json"
   )
   ```

3. **Add security scheme to OpenAPI**
   ```python
   from fastapi.openapi.utils import get_openapi
   
   def custom_openapi():
       if app.openapi_schema:
           return app.openapi_schema
       openapi_schema = get_openapi(
           title=settings.service_name,
           version=settings.service_version,
           routes=app.routes,
       )
       openapi_schema["components"]["securitySchemes"] = {
           "Bearer": {
               "type": "http",
               "scheme": "bearer",
               "bearerFormat": "JWT"
           }
       }
       app.openapi_schema = openapi_schema
       return app.openapi_schema
   
   app.openapi = custom_openapi
   ```

**Validation:**
```powershell
python quick_validate.py "..\services\veri-aidpo-service\main.py"
```

**Completion Criteria:**
- [ ] Authentication imports added to main.py
- [ ] OpenAPI security scheme configured
- [ ] `/docs` shows lock icon on protected endpoints
- [ ] No coding standards violations (PASSED validation)

---

### Step 2.5: Test Authentication (30 min)

**Objective:** Verify JWT token validation and permission checking work correctly

**Tasks:**

1. **Start VeriAIDPO service (standalone)**
   ```powershell
   cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\services\veri-aidpo-service
   
   # Set environment variables
   $env:JWT_SECRET_KEY = "your-secret-key-from-backend"
   $env:DATABASE_URL = "postgresql://verisyntra:password@localhost:5432/verisyntra"
   $env:REDIS_URL = "redis://localhost:6379/2"
   
   # Start service
   python main.py
   ```

2. **Test with valid JWT token**
   ```powershell
   # Get valid token from main backend (port 8000)
   $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method Post -Body (@{username="admin@example.com"; password="admin123"} | ConvertTo-Json) -ContentType "application/json"
   $token = $loginResponse.access_token
   
   # Test VeriAIDPO service (port 8001) with token
   $headers = @{ Authorization = "Bearer $token" }
   Invoke-RestMethod -Uri "http://localhost:8001/api/v1/classify" -Method Post -Headers $headers -Body (@{text="test data"; company_id="123"} | ConvertTo-Json) -ContentType "application/json"
   ```

3. **Test without token (expect 401)**
   ```powershell
   # Should return 401 Unauthorized
   Invoke-RestMethod -Uri "http://localhost:8001/api/v1/classify" -Method Post -Body (@{text="test"} | ConvertTo-Json) -ContentType "application/json"
   ```

4. **Test with wrong permission (expect 403)**
   ```powershell
   # Login as viewer (no veriaidpo.classify permission)
   $viewerLogin = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method Post -Body (@{username="viewer@example.com"; password="viewer123"} | ConvertTo-Json) -ContentType "application/json"
   $viewerToken = $viewerLogin.access_token
   
   # Should return 403 Forbidden with Vietnamese error
   $headers = @{ Authorization = "Bearer $viewerToken" }
   Invoke-RestMethod -Uri "http://localhost:8001/api/v1/classify" -Method Post -Headers $headers -Body (@{text="test"} | ConvertTo-Json) -ContentType "application/json"
   ```

5. **Verify error messages are bilingual**
   - Check 403 response includes both `error` and `error_vi` fields
   - Vietnamese diacritics displayed correctly

**Expected Results:**
- Valid token with permission -> 200 OK (or 500 if model not loaded, RBAC verified)
- No token -> 401 Unauthorized
- Valid token without permission -> 403 Forbidden with bilingual error
- Health endpoint -> 200 OK (no auth required)

**Completion Criteria:**
- [ ] Service starts without errors
- [ ] Valid JWT token allows access to protected endpoints
- [ ] Missing token returns 401
- [ ] Wrong permission returns 403 with bilingual error
- [ ] Health endpoint accessible without authentication
- [ ] Error messages include Vietnamese translations

---

## Validation Checklist

**Authentication Files Created:**
- [ ] `services/veri-aidpo-service/app/auth/__init__.py`
- [ ] `services/veri-aidpo-service/app/auth/jwt_validator.py`
- [ ] `services/veri-aidpo-service/app/auth/permissions.py`

**Code Quality:**
- [ ] All files pass `backend/quick_validate.py` (no hard-coding, proper Vietnamese diacritics, no emoji)
- [ ] JWT secret key loaded from config (not hard-coded)
- [ ] Bilingual error messages (error + error_vi fields)
- [ ] No undefined references to backend RBAC modules

**Functional Testing:**
- [ ] Service starts successfully
- [ ] JWT token validation works (401 for invalid tokens)
- [ ] Permission checking works (403 for missing permissions)
- [ ] Protected endpoints require authentication
- [ ] Public endpoints (health) work without auth
- [ ] Error messages are bilingual (Vietnamese + English)

**Documentation:**
- [ ] OpenAPI docs show authentication requirements
- [ ] Lock icon visible on protected endpoints in `/docs`

---

## Troubleshooting

**Issue: "Module 'auth.rbac_dependencies' not found"**
- **Cause:** Old import from backend monolith
- **Fix:** Update imports to `app.auth.jwt_validator` and `app.auth.permissions`

**Issue: "Invalid JWT token"**
- **Cause:** JWT secret mismatch between backend and service
- **Fix:** Ensure `JWT_SECRET_KEY` environment variable matches main backend

**Issue: "Permission denied" for all users**
- **Cause:** JWT payload doesn't include permissions claim
- **Fix:** Check main backend token generation includes permissions array

**Issue: Vietnamese characters corrupted in error messages**
- **Cause:** Encoding issue
- **Fix:** Ensure response uses UTF-8 encoding, check bilingual field structure

**Issue: "401 Unauthorized" even with valid token**
- **Cause:** Token expiration or signature verification failure
- **Fix:** Check token expiry time, verify JWT algorithm matches (HS256)

---

## Next Steps

After Phase 2 completion, proceed to:
- **Phase 3:** Docker Configuration (Dockerfile, docker-compose.yml)
- **Phase 4:** Backend Integration (proxy endpoints in main backend)
- **Phase 5:** Testing & Validation (integration tests, RBAC regression tests)

---

## Git Commit

After completing Phase 2:

```powershell
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra

git add services/veri-aidpo-service/app/auth
git add services/veri-aidpo-service/app/api/v1/endpoints/classification.py
git add services/veri-aidpo-service/main.py
git add docs/VeriAIDPO/Migration

git commit -m "Phase 2: VeriAIDPO authentication integration complete

- Created JWT validation middleware (app/auth/jwt_validator.py)
- Created permission checking dependency (app/auth/permissions.py)
- Integrated authentication into classification endpoints
- Updated main.py with OpenAPI security scheme
- Bilingual error messages (Vietnamese + English)
- All files validated against VeriSyntra coding standards
- RBAC imports updated from backend to service modules"
```
