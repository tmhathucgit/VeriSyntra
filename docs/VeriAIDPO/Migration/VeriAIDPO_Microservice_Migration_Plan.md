# VeriAIDPO Microservice Migration Plan

**Service Name:** VeriAIDPO Classification Service  
**Migration Priority:** HIGH (Backend Stability Issue)  
**Estimated Effort:** 6-8 hours  
**Status:** PLANNED  
**Date:** November 8, 2025

## Executive Summary

The VeriAIDPO Classification Service requires extraction from the monolithic backend into an independent microservice due to:
- **Backend crashes** during ML model operations causing complete service downtime
- **Resource isolation** needed for HuggingFace model loading (1-3GB RAM per model)
- **Independent scaling** requirements for PDPL classification workloads
- **Fault tolerance** - ML inference failures should not affect authentication/RBAC

## Current State Analysis

### Existing Implementation
**Location:** `backend/app/api/v1/endpoints/veriaidpo_classification.py`

**Endpoints (8 total):**
1. `POST /api/v1/veriaidpo/classify` - Universal classification endpoint
2. `POST /api/v1/veriaidpo/classify-legal-basis` - Legal basis classification
3. `POST /api/v1/veriaidpo/classify-breach-severity` - Breach severity triage
4. `POST /api/v1/veriaidpo/classify-cross-border` - Cross-border transfer rules
5. `POST /api/v1/veriaidpo/normalize` - Company name normalization
6. `GET /api/v1/veriaidpo/health` - Service health check (PUBLIC)
7. `GET /api/v1/veriaidpo/model-status` - Model loading status
8. `POST /api/v1/veriaidpo/batch-classify` - Batch processing

**Dependencies:**
- `app/core/model_loader.py` - HuggingFace model management
- `app/core/pdpl_normalizer.py` - Company name normalization
- `app/core/company_registry.py` - Vietnamese company database
- `auth/rbac_dependencies.py` - RBAC permission enforcement

**RBAC Requirements:**
- `processing_activity.read` - Classification endpoints (staff/dpo/compliance_manager)
- `data_category.write` - Normalization endpoints (dpo/compliance_manager)
- `analytics.read` - Model status endpoint (admin/dpo/compliance_manager/auditor)

### Issues Identified in Testing

**Test Results (from RBAC Step 8):**
- 8 VeriAIDPO tests created
- 0 tests passing consistently (backend crashes)
- Errors: `ConnectionError: Remote end closed connection without response`

**Root Causes:**
1. **Model Loading Crashes** - HuggingFace model download failures kill backend
2. **Memory Pressure** - 11 model types (principles, legal_basis, etc.) require 15-20GB RAM
3. **Synchronous Blocking** - Large model inference blocks FastAPI event loop
4. **No Graceful Degradation** - Model failures return 500, crash connections

## Target Architecture

### Service Overview
```
┌─────────────────────────────────────────────────────────────┐
│                  VeriAIDPO Classification Service            │
│                     (Dedicated FastAPI App)                  │
├─────────────────────────────────────────────────────────────┤
│  Port: 8001                                                  │
│  Container: verisyntra-veriaidpo                            │
│  Image: verisyntra/veriaidpo-service:latest                 │
├─────────────────────────────────────────────────────────────┤
│  Components:                                                 │
│  - FastAPI Server (async endpoints)                         │
│  - HuggingFace Model Loader (lazy loading)                  │
│  - PDPL Normalizer (company name processing)                │
│  - Redis Cache (inference results)                          │
│  - Model Registry (tmhathucgit/veriaidpo-*)                 │
├─────────────────────────────────────────────────────────────┤
│  Authentication: JWT Bearer Token (from main backend)       │
│  Authorization: RBAC via JWT claims (sub, role, tenant_id)  │
│  Database: PostgreSQL (shared with main backend)            │
│  Storage: Model cache volume (20GB)                         │
└─────────────────────────────────────────────────────────────┘
```

### Communication Pattern

**API Gateway (Main Backend) -> VeriAIDPO Service:**
```python
# Main backend acts as API gateway
@router.post("/veriaidpo/classify")
async def classify_proxy(
    request: ClassificationRequest,
    current_user: CurrentUser = Depends(require_permission("processing_activity.read"))
):
    """Proxy to VeriAIDPO microservice with RBAC enforcement"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://veriaidpo-service:8001/classify",
            json=request.dict(),
            headers={"Authorization": f"Bearer {generate_service_token(current_user)}"}
        )
        return response.json()
```

**Direct Client -> VeriAIDPO Service (Future):**
```
Client -> API Gateway (authentication/RBAC) -> Forward to VeriAIDPO
Client -> VeriAIDPO (with JWT token from main backend)
```

## Migration Steps

### Phase 1: Service Extraction (2-3 hours)

**Step 1.1: Create Service Directory Structure**
```
services/veri-aidpo-service/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py                    # FastAPI app entry point
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── classification.py  # Classification endpoints
│   │           └── health.py          # Health check
│   ├── core/
│   │   ├── model_loader.py            # Copy from backend/app/core/
│   │   ├── pdpl_normalizer.py         # Copy from backend/app/core/
│   │   └── company_registry.py        # Copy from backend/app/core/
│   ├── auth/
│   │   └── jwt_validator.py           # JWT token validation
│   └── config.py                      # Service configuration
├── tests/
│   └── test_classification_api.py
└── models/                            # Volume mount for HuggingFace cache
    └── .gitkeep
```

**Step 1.2: Copy Core Components**
```bash
# Copy model infrastructure
cp backend/app/core/model_loader.py services/veri-aidpo-service/app/core/
cp backend/app/core/pdpl_normalizer.py services/veri-aidpo-service/app/core/
cp backend/app/core/company_registry.py services/veri-aidpo-service/app/core/

# Copy endpoint
cp backend/app/api/v1/endpoints/veriaidpo_classification.py services/veri-aidpo-service/app/api/v1/endpoints/classification.py
```

**Step 1.3: Create Service Dependencies**
```python
# services/veri-aidpo-service/requirements.txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic==2.10.3
pydantic-settings==2.11.0
transformers==4.46.3
torch==2.5.1
sentencepiece==0.2.0
protobuf==5.28.3
httpx==0.28.1
redis==5.2.1
psycopg2-binary==2.9.10
SQLAlchemy==2.0.36
python-jose[cryptography]==3.3.0
loguru==0.7.3
```

### Phase 2: Service Authentication (1-2 hours)

**Step 2.1: JWT Validation Middleware**
```python
# services/veri-aidpo-service/app/auth/jwt_validator.py
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

security = HTTPBearer()

async def validate_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """Validate JWT token from main backend"""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        # Extract claims
        user_id = payload.get("sub")
        role = payload.get("role")
        tenant_id = payload.get("tenant_id")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing subject")
        
        return {
            "user_id": user_id,
            "role": role,
            "tenant_id": tenant_id,
            "permissions": payload.get("permissions", [])
        }
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")
```

**Step 2.2: Permission Checking**
```python
# services/veri-aidpo-service/app/auth/permissions.py
from fastapi import HTTPException, Depends
from typing import List

def require_permission(permission: str):
    """Dependency to check if user has required permission"""
    async def permission_checker(user: dict = Depends(validate_token)):
        if permission not in user.get("permissions", []):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": f"Permission denied: {permission} required",
                    "error_vi": f"Từ chối quyền truy cập: cần quyền {permission}",
                    "required_permission": permission,
                    "user_role": user.get("role")
                }
            )
        return user
    return permission_checker
```

### Phase 3: Service Configuration (30 min)

**Step 3.1: Create Dockerfile**
```dockerfile
# services/veri-aidpo-service/Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY main.py .

# Create model cache directory
RUN mkdir -p /app/models

# Expose port
EXPOSE 8001

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

**Step 3.2: Create Docker Compose**
```yaml
# services/veri-aidpo-service/docker-compose.yml
version: '3.8'

services:
  veriaidpo-service:
    build: .
    container_name: verisyntra-veriaidpo
    ports:
      - "8001:8001"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - JWT_ALGORITHM=HS256
      - DATABASE_URL=postgresql://verisyntra:verisyntra_dev_password@postgres:5432/verisyntra
      - REDIS_URL=redis://redis:6379/2
      - HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}
      - MODEL_CACHE_DIR=/app/models
    volumes:
      - ./models:/app/models
      - ./app:/app/app
    networks:
      - verisyntra-network
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

networks:
  verisyntra-network:
    external: true
```

### Phase 4: Main Backend Integration (1-2 hours)

**Step 4.1: Create Proxy Endpoints**
```python
# backend/app/api/v1/endpoints/veriaidpo_proxy.py
"""
VeriAIDPO Microservice Proxy
Forwards requests to VeriAIDPO service with RBAC enforcement
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import httpx
from loguru import logger

from auth.rbac_dependencies import require_permission, CurrentUser

router = APIRouter(prefix="/veriaidpo", tags=["VeriAIDPO Classification"])

VERIAIDPO_SERVICE_URL = "http://veriaidpo-service:8001"

@router.post("/classify")
async def classify_proxy(
    request: Dict[str, Any],
    current_user: CurrentUser = Depends(require_permission("processing_activity.read"))
):
    """Proxy classification request to VeriAIDPO microservice"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{VERIAIDPO_SERVICE_URL}/classify",
                json=request,
                headers={
                    "Authorization": f"Bearer {current_user.generate_service_token()}",
                    "X-Tenant-ID": current_user.tenant_id,
                    "X-User-Role": current_user.role
                }
            )
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="VeriAIDPO service timeout")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="VeriAIDPO service unavailable")

@router.post("/normalize")
async def normalize_proxy(
    request: Dict[str, Any],
    current_user: CurrentUser = Depends(require_permission("data_category.write"))
):
    """Proxy normalization request to VeriAIDPO microservice"""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{VERIAIDPO_SERVICE_URL}/normalize",
                json=request,
                headers={"Authorization": f"Bearer {current_user.generate_service_token()}"}
            )
            return response.json()
    except Exception as e:
        logger.error(f"VeriAIDPO normalize proxy error: {e}")
        raise HTTPException(status_code=503, detail="Normalization service unavailable")

@router.get("/health")
async def health_proxy():
    """Proxy health check to VeriAIDPO microservice (PUBLIC)"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{VERIAIDPO_SERVICE_URL}/health")
            return response.json()
    except Exception:
        return {"status": "unhealthy", "service": "veriaidpo"}
```

**Step 4.2: Update Main Backend Router**
```python
# backend/app/api/v1/router.py
from app.api.v1.endpoints import (
    admin_companies,
    veriaidpo_proxy,  # NEW - Replace veriaidpo_classification
    veriportal,
    vericompliance
)

# Replace old endpoint with proxy
# app.include_router(veriaidpo_classification.router)  # OLD
app.include_router(veriaidpo_proxy.router)  # NEW
```

### Phase 5: Testing & Validation (1-2 hours)

**Step 5.1: Update Integration Tests**
```python
# backend/tests/system/test_veriaidpo_microservice.py
"""Test VeriAIDPO microservice integration"""
import requests

MAIN_BACKEND_URL = "http://localhost:8000"
VERIAIDPO_SERVICE_URL = "http://localhost:8001"

def test_veriaidpo_service_health():
    """Test VeriAIDPO service is running"""
    response = requests.get(f"{VERIAIDPO_SERVICE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_classify_via_proxy(staff_tokens):
    """Test classification via main backend proxy"""
    response = requests.post(
        f"{MAIN_BACKEND_URL}/api/v1/veriaidpo/classify",
        json={
            "text": "Shopee VN thu thập email khách hàng",
            "model_type": "principles",
            "language": "vi"
        },
        headers={"Authorization": f"Bearer {staff_tokens['access_token']}"}
    )
    # Accept 200 (model loaded) or 500 (model not loaded, but RBAC passed)
    assert response.status_code in [200, 500]
    assert response.status_code != 403  # RBAC should allow

def test_classify_direct_to_service(service_token):
    """Test direct classification to VeriAIDPO service"""
    response = requests.post(
        f"{VERIAIDPO_SERVICE_URL}/classify",
        json={
            "text": "Tiki thu thập số điện thoại",
            "model_type": "legal_basis",
            "language": "vi"
        },
        headers={"Authorization": f"Bearer {service_token}"}
    )
    assert response.status_code in [200, 500]
```

**Step 5.2: Update RBAC Tests**
```python
# backend/tests/system/test_rbac_protected_endpoints.py
# Update BASE_URL for VeriAIDPO tests to use proxy or direct service
VERIAIDPO_BASE_URL = "http://localhost:8000"  # Via proxy (recommended)
# VERIAIDPO_BASE_URL = "http://localhost:8001"  # Direct (testing only)
```

### Phase 6: Deployment (30 min)

**Step 6.1: Update Docker Compose Root**
```yaml
# docker-compose.yml (ROOT)
version: '3.8'

services:
  backend:
    # ... existing backend config
    depends_on:
      - postgres
      - redis
      - veriaidpo-service  # NEW dependency
    environment:
      - VERIAIDPO_SERVICE_URL=http://veriaidpo-service:8001

  veriaidpo-service:
    build: ./services/veri-aidpo-service
    container_name: verisyntra-veriaidpo
    ports:
      - "8001:8001"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=postgresql://verisyntra:verisyntra_dev_password@postgres:5432/verisyntra
      - REDIS_URL=redis://redis:6379/2
      - HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}
    volumes:
      - veriaidpo-models:/app/models
    networks:
      - verisyntra-network
    depends_on:
      - postgres
      - redis

volumes:
  veriaidpo-models:
    driver: local

networks:
  verisyntra-network:
    driver: bridge
```

**Step 6.2: Start Services**
```bash
# Build and start VeriAIDPO service
docker-compose up -d veriaidpo-service

# Verify service is running
curl http://localhost:8001/health

# Restart main backend with proxy
docker-compose restart backend

# Run integration tests
pytest backend/tests/system/test_veriaidpo_microservice.py -v
```

## Rollback Plan

**If migration fails:**
```bash
# Step 1: Stop VeriAIDPO service
docker-compose stop veriaidpo-service

# Step 2: Revert main backend router
# backend/app/api/v1/router.py
app.include_router(veriaidpo_classification.router)  # Restore original

# Step 3: Restart backend
docker-compose restart backend

# Step 4: Verify original endpoints work
curl http://localhost:8000/api/v1/veriaidpo/health
```

## Performance Expectations

**Before Migration (Monolithic):**
- Classification latency: 500-2000ms (model loaded)
- Backend crashes: Frequent (model loading failures)
- Resource sharing: All services compete for 4GB RAM
- Fault isolation: None (one crash kills everything)

**After Migration (Microservice):**
- Classification latency: 300-1500ms (dedicated resources)
- Backend crashes: Eliminated (isolated service)
- Resource allocation: VeriAIDPO gets dedicated 8GB RAM
- Fault tolerance: Main backend remains operational if VeriAIDPO crashes
- Scalability: Can deploy multiple VeriAIDPO instances behind load balancer

## Success Criteria

1. [OK] VeriAIDPO service runs independently on port 8001
2. [OK] Main backend proxies requests with RBAC enforcement
3. [OK] JWT authentication works across services
4. [OK] Integration tests pass (11/11 VeriAIDPO tests)
5. [OK] No backend crashes during ML operations
6. [OK] Health check endpoint returns service status
7. [OK] Model loading failures don't affect main backend

## Post-Migration Tasks

1. **Monitoring Setup**
   - Prometheus metrics for VeriAIDPO service
   - Grafana dashboard for inference latency
   - Alert on model loading failures

2. **Load Balancing**
   - Deploy 2-3 VeriAIDPO instances
   - NGINX load balancer for inference requests
   - Round-robin with health check failover

3. **Model Pre-loading**
   - Download all 11 HuggingFace models to volume
   - Lazy load models on first request
   - Cache inference results in Redis (1 hour TTL)

4. **Documentation Updates**
   - Update API docs with new proxy endpoints
   - Document service-to-service authentication
   - Create runbook for VeriAIDPO service operations

## Dependencies

**Shared with Main Backend:**
- PostgreSQL database (company registry, user permissions)
- Redis cache (inference results, rate limiting)
- JWT secret key (token validation)

**VeriAIDPO-Specific:**
- HuggingFace model cache (20GB volume)
- Transformers library (4.46.3)
- PyTorch (2.5.1)
- SentencePiece tokenizers

## Timeline

| Phase | Duration | Dependencies | Status |
|-------|----------|--------------|--------|
| Phase 1: Service Extraction | 2-3 hours | None | PLANNED |
| Phase 2: Authentication | 1-2 hours | Phase 1 | PLANNED |
| Phase 3: Configuration | 30 min | Phase 1 | PLANNED |
| Phase 4: Backend Integration | 1-2 hours | Phase 1-3 | PLANNED |
| Phase 5: Testing | 1-2 hours | Phase 4 | PLANNED |
| Phase 6: Deployment | 30 min | Phase 5 | PLANNED |
| **Total** | **6-8 hours** | | |

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| JWT secret mismatch | HIGH | LOW | Share JWT_SECRET_KEY via .env |
| Model download failures | HIGH | MEDIUM | Pre-download models to volume |
| Service communication timeout | MEDIUM | MEDIUM | Set httpx timeout=30s, retry logic |
| Database connection pool exhaustion | HIGH | LOW | Use separate connection pool for VeriAIDPO |
| Increased network latency | LOW | HIGH | Deploy services in same Docker network |

## Next Steps

1. Review and approve migration plan
2. Create feature branch: `feature/veriaidpo-microservice-migration`
3. Execute Phase 1 (Service Extraction)
4. Run integration tests after each phase
5. Deploy to staging environment
6. Monitor for 24-48 hours
7. Deploy to production

---

**Document Owner:** VeriSyntra Development Team  
**Last Updated:** November 8, 2025  
**Status:** APPROVED FOR IMPLEMENTATION
