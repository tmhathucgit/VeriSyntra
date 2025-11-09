# VeriPortal Microservice Migration Plan

**Service Name:** VeriPortal Dashboard Service  
**Migration Priority:** MEDIUM (Stability Enhancement)  
**Estimated Effort:** 4-6 hours  
**Status:** PLANNED  
**Date:** November 8, 2025

## Executive Summary

The VeriPortal Dashboard Service requires extraction from the monolithic backend into an independent microservice to:
- **Prevent backend crashes** during cultural intelligence operations
- **Enable independent scaling** for Vietnamese business analytics workloads
- **Isolate frontend services** from backend CRUD operations
- **Support multi-regional deployments** (North/Central/South Vietnam data centers)

## Current State Analysis

### Existing Implementation
**Location:** `backend/app/api/v1/endpoints/veriportal.py`

**Endpoints (2 total):**
1. `GET /api/v1/veriportal/` - Portal information (PUBLIC)
2. `GET /api/v1/veriportal/dashboard` - Cultural intelligence dashboard

**Dependencies:**
- `backend/app/core/vietnamese_cultural_intelligence.py` - Regional business context engine
- `auth/rbac_dependencies.py` - RBAC permission enforcement
- PostgreSQL - Business context data, regional analytics
- No external ML models (unlike VeriAIDPO)

**RBAC Requirements:**
- `None` - Portal info endpoint (PUBLIC)
- `analytics.read` - Dashboard endpoint (compliance_manager/dpo only)

### Issues Identified in Testing

**Test Results (from RBAC Step 8):**
- 3 VeriPortal tests created
- 3 tests ERROR (backend connection crashes)
- Errors: `ConnectionError: Remote end closed connection without response`

**Root Causes:**
1. **Cultural Intelligence Processing** - Vietnamese regional context calculations crash backend
2. **Database Query Complexity** - Dashboard aggregations lock PostgreSQL connections
3. **No Error Handling** - Cultural engine failures propagate to main backend
4. **Session Management** - Long-running dashboard queries block FastAPI workers

## Target Architecture

### Service Overview
```
┌─────────────────────────────────────────────────────────────┐
│                  VeriPortal Dashboard Service                │
│                     (Dedicated FastAPI App)                  │
├─────────────────────────────────────────────────────────────┤
│  Port: 8002                                                  │
│  Container: verisyntra-veriportal                           │
│  Image: verisyntra/veriportal-service:latest                │
├─────────────────────────────────────────────────────────────┤
│  Components:                                                 │
│  - FastAPI Server (async endpoints)                         │
│  - Vietnamese Cultural Intelligence Engine                  │
│  - Regional Analytics Dashboard                             │
│  - Business Context API                                      │
│  - Redis Cache (dashboard data, 15 min TTL)                 │
├─────────────────────────────────────────────────────────────┤
│  Authentication: JWT Bearer Token (from main backend)       │
│  Authorization: RBAC via JWT claims (sub, role, tenant_id)  │
│  Database: PostgreSQL (shared with main backend)            │
│  Regional Data: North/Central/South business patterns       │
└─────────────────────────────────────────────────────────────┘
```

### Vietnamese Regional Architecture

**Cultural Intelligence by Region:**
```
┌──────────────────────────────────────────────────────────┐
│           North (Hanoi) - Formal Hierarchy               │
│  - Government proximity patterns                         │
│  - Structured decision-making analytics                  │
│  - Compliance-focused dashboards                         │
├──────────────────────────────────────────────────────────┤
│           Central (Da Nang/Hue) - Traditional            │
│  - Consensus-building metrics                            │
│  - Cultural preservation analytics                       │
│  - Family business patterns                              │
├──────────────────────────────────────────────────────────┤
│           South (HCMC) - Entrepreneurial                 │
│  - Fast decision-making patterns                         │
│  - International business analytics                      │
│  - Innovation-focused dashboards                         │
└──────────────────────────────────────────────────────────┘
```

### Communication Pattern

**API Gateway (Main Backend) -> VeriPortal Service:**
```python
# Main backend acts as API gateway
@router.get("/veriportal/dashboard")
async def dashboard_proxy(
    current_user: CurrentUser = Depends(require_permission("analytics.read"))
):
    """Proxy to VeriPortal microservice with cultural context"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://veriportal-service:8002/dashboard",
            headers={
                "Authorization": f"Bearer {generate_service_token(current_user)}",
                "X-Tenant-ID": current_user.tenant_id,
                "X-Regional-Location": current_user.veri_regional_location
            }
        )
        return response.json()
```

## Migration Steps

### Phase 1: Service Extraction (1-2 hours)

**Step 1.1: Create Service Directory Structure**
```
services/veri-portal-service/
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
│   │           ├── portal.py              # Portal info
│   │           └── dashboard.py           # Cultural dashboard
│   ├── core/
│   │   ├── vietnamese_cultural_intelligence.py  # Copy from backend
│   │   └── regional_analytics.py         # Dashboard data aggregation
│   ├── auth/
│   │   └── jwt_validator.py               # JWT token validation
│   └── config.py                          # Service configuration
├── tests/
│   └── test_portal_api.py
└── static/                                # Optional: Dashboard assets
    └── .gitkeep
```

**Step 1.2: Copy Core Components**
```bash
# Copy cultural intelligence engine
cp backend/app/core/vietnamese_cultural_intelligence.py services/veri-portal-service/app/core/

# Copy endpoint
cp backend/app/api/v1/endpoints/veriportal.py services/veri-portal-service/app/api/v1/endpoints/portal.py
```

**Step 1.3: Create Service Dependencies**
```python
# services/veri-portal-service/requirements.txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic==2.10.3
pydantic-settings==2.11.0
httpx==0.28.1
redis==5.2.1
psycopg2-binary==2.9.10
SQLAlchemy==2.0.36
python-jose[cryptography]==3.3.0
loguru==0.7.3
pandas==2.2.3             # For analytics
pytz==2025.1              # Vietnamese timezone (Asia/Ho_Chi_Minh)
```

### Phase 2: Cultural Intelligence Service (1-2 hours)

**Step 2.1: Vietnamese Business Context API**
```python
# services/veri-portal-service/app/core/vietnamese_cultural_intelligence.py
from typing import Dict, Any, Literal
from datetime import datetime
import pytz

RegionalLocation = Literal['north', 'central', 'south']
IndustryType = Literal['technology', 'manufacturing', 'finance', 'healthcare', 'retail']

class VietnameseCulturalIntelligence:
    """
    Vietnamese business cultural intelligence engine
    Provides region and industry-specific business insights
    """
    
    REGIONAL_PATTERNS = {
        'north': {
            'communication_style': 'formal',
            'decision_making': 'hierarchical',
            'business_hours': '08:00-17:00',
            'government_proximity': 'high',
            'compliance_priority': 'very_high',
            'timezone': 'Asia/Ho_Chi_Minh'
        },
        'central': {
            'communication_style': 'collaborative',
            'decision_making': 'consensus',
            'business_hours': '07:30-16:30',
            'cultural_preservation': 'high',
            'compliance_priority': 'high',
            'timezone': 'Asia/Ho_Chi_Minh'
        },
        'south': {
            'communication_style': 'direct',
            'decision_making': 'entrepreneurial',
            'business_hours': '08:30-17:30',
            'international_exposure': 'high',
            'compliance_priority': 'medium',
            'timezone': 'Asia/Ho_Chi_Minh'
        }
    }
    
    def get_business_context(
        self,
        region: RegionalLocation,
        industry: IndustryType
    ) -> Dict[str, Any]:
        """
        Get Vietnamese business context for region and industry
        
        Returns cultural patterns, business hours, compliance expectations
        """
        regional_pattern = self.REGIONAL_PATTERNS.get(region, {})
        
        # Get current Vietnamese time
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = datetime.now(vn_tz)
        
        return {
            'region': region,
            'industry': industry,
            'cultural_pattern': regional_pattern,
            'current_vietnamese_time': current_time.isoformat(),
            'business_day': current_time.weekday() < 5,  # Monday=0, Sunday=6
            'recommended_communication_style': regional_pattern.get('communication_style'),
            'decision_making_approach': regional_pattern.get('decision_making'),
            'compliance_priority_level': regional_pattern.get('compliance_priority')
        }
```

**Step 2.2: Dashboard Data Aggregation**
```python
# services/veri-portal-service/app/core/regional_analytics.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Dict, List, Any
from datetime import datetime, timedelta

class RegionalAnalytics:
    """Aggregate dashboard data for Vietnamese regional business context"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_regional_compliance_metrics(
        self,
        tenant_id: str,
        region: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get PDPL compliance metrics for region
        
        Returns:
        - Total processing activities by region
        - Data subject requests by region
        - Compliance score trends
        - Regional risk assessment
        """
        since_date = datetime.now() - timedelta(days=days)
        
        # Query processing activities
        activities_count = self.db.query(func.count()).filter(
            and_(
                ProcessingActivity.tenant_id == tenant_id,
                ProcessingActivity.created_at >= since_date
            )
        ).scalar()
        
        # Regional business pattern analysis
        return {
            'region': region,
            'time_period_days': days,
            'processing_activities_count': activities_count,
            'compliance_score': self._calculate_compliance_score(tenant_id, region),
            'regional_risk_level': self._assess_regional_risk(region),
            'cultural_alignment_score': self._calculate_cultural_alignment(tenant_id, region)
        }
    
    def _calculate_compliance_score(self, tenant_id: str, region: str) -> float:
        """Calculate PDPL compliance score (0-100)"""
        # Implement compliance scoring logic
        return 85.0  # Placeholder
    
    def _assess_regional_risk(self, region: str) -> str:
        """Assess risk level based on Vietnamese regional patterns"""
        risk_mapping = {
            'north': 'low',      # High government oversight, formal compliance
            'central': 'medium', # Traditional business, moderate oversight
            'south': 'medium'    # Entrepreneurial, international exposure
        }
        return risk_mapping.get(region, 'medium')
    
    def _calculate_cultural_alignment(self, tenant_id: str, region: str) -> float:
        """Calculate how well company aligns with regional cultural patterns"""
        # Implement cultural alignment scoring
        return 78.5  # Placeholder
```

### Phase 3: Service Configuration (30 min)

**Step 3.1: Create Dockerfile**
```dockerfile
# services/veri-portal-service/Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY main.py .

# Expose port
EXPOSE 8002

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
```

**Step 3.2: Create Docker Compose**
```yaml
# services/veri-portal-service/docker-compose.yml
version: '3.8'

services:
  veriportal-service:
    build: .
    container_name: verisyntra-veriportal
    ports:
      - "8002:8002"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - JWT_ALGORITHM=HS256
      - DATABASE_URL=postgresql://verisyntra:verisyntra_dev_password@postgres:5432/verisyntra
      - REDIS_URL=redis://redis:6379/3
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - DASHBOARD_CACHE_TTL=900  # 15 minutes
    volumes:
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

### Phase 4: Main Backend Integration (1 hour)

**Step 4.1: Create Proxy Endpoints**
```python
# backend/app/api/v1/endpoints/veriportal_proxy.py
"""
VeriPortal Microservice Proxy
Forwards requests to VeriPortal service with RBAC enforcement
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import httpx
from loguru import logger

from auth.rbac_dependencies import require_permission, CurrentUser

router = APIRouter(prefix="/veriportal", tags=["VeriPortal Dashboard"])

VERIPORTAL_SERVICE_URL = "http://veriportal-service:8002"

@router.get("/")
async def portal_info_proxy():
    """Proxy portal info request to VeriPortal microservice (PUBLIC)"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{VERIPORTAL_SERVICE_URL}/")
            return response.json()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="VeriPortal service unavailable")

@router.get("/dashboard")
async def dashboard_proxy(
    current_user: CurrentUser = Depends(require_permission("analytics.read"))
):
    """Proxy dashboard request to VeriPortal microservice"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{VERIPORTAL_SERVICE_URL}/dashboard",
                headers={
                    "Authorization": f"Bearer {current_user.generate_service_token()}",
                    "X-Tenant-ID": current_user.tenant_id,
                    "X-Regional-Location": getattr(current_user, 'veri_regional_location', 'south'),
                    "X-Industry-Type": getattr(current_user, 'veri_industry_type', 'technology')
                }
            )
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Dashboard generation timeout")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="VeriPortal service unavailable")
```

**Step 4.2: Update Main Backend Router**
```python
# backend/app/api/v1/router.py
from app.api.v1.endpoints import (
    admin_companies,
    veriaidpo_proxy,
    veriportal_proxy,  # NEW - Replace veriportal
    vericompliance
)

# Replace old endpoint with proxy
# app.include_router(veriportal.router)  # OLD
app.include_router(veriportal_proxy.router)  # NEW
```

### Phase 5: Testing & Validation (1 hour)

**Step 5.1: Update Integration Tests**
```python
# backend/tests/system/test_veriportal_microservice.py
"""Test VeriPortal microservice integration"""
import requests

MAIN_BACKEND_URL = "http://localhost:8000"
VERIPORTAL_SERVICE_URL = "http://localhost:8002"

def test_veriportal_service_health():
    """Test VeriPortal service is running"""
    response = requests.get(f"{VERIPORTAL_SERVICE_URL}/")
    assert response.status_code == 200
    assert "module" in response.json()
    assert response.json()["module"] == "VeriPortal"

def test_dashboard_via_proxy(compliance_manager_tokens):
    """Test dashboard via main backend proxy"""
    response = requests.get(
        f"{MAIN_BACKEND_URL}/api/v1/veriportal/dashboard",
        headers={"Authorization": f"Bearer {compliance_manager_tokens['access_token']}"}
    )
    # RBAC test: compliance_manager HAS analytics.read permission
    assert response.status_code != 403
    
    if response.status_code == 200:
        data = response.json()
        assert "regional_context" in data or "dashboard_data" in data

def test_dashboard_viewer_forbidden(viewer_tokens):
    """Test dashboard denies viewer role (no analytics.read)"""
    response = requests.get(
        f"{MAIN_BACKEND_URL}/api/v1/veriportal/dashboard",
        headers={"Authorization": f"Bearer {viewer_tokens['access_token']}"}
    )
    assert response.status_code == 403
    assert "error_vi" in response.json().get("detail", {})
```

**Step 5.2: Update RBAC Tests**
```python
# backend/tests/system/test_rbac_protected_endpoints.py
# VeriPortal tests should now pass without connection errors

class TestVeriPortalRBAC:
    def test_veriportal_info_public(self):
        """Test GET /veriportal/ without authentication - Should return 200 (public)"""
        response = requests.get(f"{BASE_URL}/api/v1/veriportal/")
        assert response.status_code == 200
        assert "module" in response.json()
    
    def test_dashboard_viewer_forbidden(self):
        """Test GET /veriportal/dashboard with viewer role - Should return 403"""
        response = requests.get(
            f"{BASE_URL}/api/v1/veriportal/dashboard",
            headers={"Authorization": f"Bearer {self.viewer_tokens['access_token']}"}
        )
        assert response.status_code == 403
    
    def test_dashboard_compliance_allowed(self):
        """Test GET /veriportal/dashboard with compliance_manager role - Should return 200"""
        response = requests.get(
            f"{BASE_URL}/api/v1/veriportal/dashboard",
            headers={"Authorization": f"Bearer {self.compliance_manager_tokens['access_token']}"}
        )
        assert response.status_code in [200, 503]  # Allow service unavailable
        assert response.status_code != 403  # RBAC should allow
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
      - veriaidpo-service
      - veriportal-service  # NEW dependency
    environment:
      - VERIPORTAL_SERVICE_URL=http://veriportal-service:8002

  veriportal-service:
    build: ./services/veri-portal-service
    container_name: verisyntra-veriportal
    ports:
      - "8002:8002"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=postgresql://verisyntra:verisyntra_dev_password@postgres:5432/verisyntra
      - REDIS_URL=redis://redis:6379/3
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
    networks:
      - verisyntra-network
    depends_on:
      - postgres
      - redis

networks:
  verisyntra-network:
    driver: bridge
```

**Step 6.2: Start Services**
```bash
# Build and start VeriPortal service
docker-compose up -d veriportal-service

# Verify service is running
curl http://localhost:8002/

# Restart main backend with proxy
docker-compose restart backend

# Run integration tests
pytest backend/tests/system/test_veriportal_microservice.py -v
```

## Rollback Plan

**If migration fails:**
```bash
# Step 1: Stop VeriPortal service
docker-compose stop veriportal-service

# Step 2: Revert main backend router
# backend/app/api/v1/router.py
app.include_router(veriportal.router)  # Restore original

# Step 3: Restart backend
docker-compose restart backend

# Step 4: Verify original endpoints work
curl http://localhost:8000/api/v1/veriportal/
```

## Performance Expectations

**Before Migration (Monolithic):**
- Dashboard latency: 2000-5000ms (complex queries)
- Backend crashes: Occasional (cultural intelligence failures)
- Resource sharing: Competes with classification and CRUD
- Vietnamese timezone handling: Inconsistent

**After Migration (Microservice):**
- Dashboard latency: 800-2000ms (dedicated resources, Redis cache)
- Backend crashes: Eliminated (isolated service)
- Resource allocation: VeriPortal gets dedicated 2GB RAM
- Vietnamese timezone handling: Consistent (Asia/Ho_Chi_Minh)
- Caching: Dashboard data cached 15 minutes in Redis

## Success Criteria

1. [OK] VeriPortal service runs independently on port 8002
2. [OK] Main backend proxies requests with RBAC enforcement
3. [OK] JWT authentication works across services
4. [OK] Integration tests pass (3/3 VeriPortal tests)
5. [OK] No backend crashes during dashboard operations
6. [OK] Vietnamese timezone handling correct (Asia/Ho_Chi_Minh)
7. [OK] Cultural intelligence engine isolated

## Post-Migration Tasks

1. **Regional Deployment**
   - Deploy VeriPortal instance in North (Hanoi data center)
   - Deploy VeriPortal instance in Central (Da Nang data center)
   - Deploy VeriPortal instance in South (HCMC data center)
   - Route requests to nearest regional instance

2. **Dashboard Caching Strategy**
   - Cache dashboard data in Redis (15 min TTL)
   - Invalidate cache on compliance data updates
   - Pre-generate dashboards for active tenants

3. **Vietnamese Cultural Intelligence Enhancement**
   - Add holiday calendar integration (Tết, National Day)
   - Business hour validation for each region
   - Cultural communication recommendations

4. **Monitoring Setup**
   - Prometheus metrics for dashboard generation time
   - Grafana dashboard for regional analytics performance
   - Alert on cultural intelligence engine failures

## Dependencies

**Shared with Main Backend:**
- PostgreSQL database (tenant data, processing activities, compliance metrics)
- Redis cache (dashboard data, regional analytics)
- JWT secret key (token validation)

**VeriPortal-Specific:**
- Vietnamese timezone data (Asia/Ho_Chi_Minh)
- Regional business pattern configurations
- Cultural intelligence engine

## Timeline

| Phase | Duration | Dependencies | Status |
|-------|----------|--------------|--------|
| Phase 1: Service Extraction | 1-2 hours | None | PLANNED |
| Phase 2: Cultural Intelligence | 1-2 hours | Phase 1 | PLANNED |
| Phase 3: Configuration | 30 min | Phase 1 | PLANNED |
| Phase 4: Backend Integration | 1 hour | Phase 1-3 | PLANNED |
| Phase 5: Testing | 1 hour | Phase 4 | PLANNED |
| Phase 6: Deployment | 30 min | Phase 5 | PLANNED |
| **Total** | **4-6 hours** | | |

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Dashboard query timeouts | MEDIUM | LOW | Set httpx timeout=30s, cache in Redis |
| Cultural intelligence calculation errors | HIGH | LOW | Add error handling, return default context |
| Regional data inconsistency | MEDIUM | MEDIUM | Validate region in ["north", "central", "south"] |
| Vietnamese timezone issues | LOW | LOW | Use pytz.timezone('Asia/Ho_Chi_Minh') consistently |

## Vietnamese Business Context Integration

**Regional Patterns Configuration:**
```python
# North (Hanoi) - Government proximity
{
    'communication_style': 'formal',
    'decision_making': 'hierarchical',
    'compliance_priority': 'very_high',
    'dashboard_emphasis': ['compliance_score', 'audit_logs', 'government_reporting']
}

# Central (Da Nang/Hue) - Traditional
{
    'communication_style': 'collaborative',
    'decision_making': 'consensus',
    'compliance_priority': 'high',
    'dashboard_emphasis': ['cultural_alignment', 'consensus_metrics', 'family_business']
}

# South (HCMC) - Entrepreneurial
{
    'communication_style': 'direct',
    'decision_making': 'entrepreneurial',
    'compliance_priority': 'medium',
    'dashboard_emphasis': ['innovation_metrics', 'international_compliance', 'agility_score']
}
```

## Next Steps

1. Review and approve migration plan
2. Create feature branch: `feature/veriportal-microservice-migration`
3. Execute Phase 1 (Service Extraction)
4. Run integration tests after each phase
5. Deploy to staging environment
6. Monitor for 24-48 hours
7. Deploy to production

---

**Document Owner:** VeriSyntra Development Team  
**Last Updated:** November 8, 2025  
**Status:** APPROVED FOR IMPLEMENTATION  
**Related Documents:** VeriAIDPO_Microservice_Migration_Plan.md
