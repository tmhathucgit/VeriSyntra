# VeriSyntra AI Coding Agent Instructions

VeriSyntra is a **Vietnamese PDPL 2025 compliance platform** serving Vietnamese enterprises with culturally-intelligent microservices architecture. This system uniquely combines Vietnamese cultural business intelligence with data protection compliance.

## 🏗️ System Architecture

**Hybrid Frontend/Backend:** React + TypeScript frontend (`src/`) with FastAPI Python backend (`backend/`)
- **Frontend:** Vite + React + TypeScript with modular VeriPortal components
- **Backend:** FastAPI + Vietnamese Cultural Intelligence Engine + PDPL compliance services
- **Internationalization:** Bilingual (Vietnamese-first) using react-i18next with cultural context

**Key Directories:**
- `src/components/VeriPortal/` - Core compliance modules (5 systems: Cultural Onboarding, Compliance Wizards, Document Generation, Training, Business Intelligence)
- `backend/app/core/vietnamese_cultural_intelligence.py` - Cultural AI engine for regional business contexts
- `src/hooks/useCulturalIntelligence.ts` - Frontend cultural context integration
- `docs/VeriSystems/` - System documentation and Jupyter notebooks for AI training

## 🇻🇳 Vietnamese Cultural Intelligence Patterns

**Essential Concept:** Every component must respect Vietnamese business contexts through `VeriBusinessContext`:

```typescript
interface VeriBusinessContext {
  veriBusinessId: string;
  veriRegionalLocation: 'north' | 'central' | 'south'; // Critical for UI/UX
  veriIndustryType: 'technology' | 'manufacturing' | 'finance' | ...;
  veriCulturalPreferences: {
    veriCommunicationStyle: 'collaborative' | 'formal' | 'hierarchical';
    veriDecisionMakingStyle: 'data-driven' | 'consensus' | 'authority';
    // ... more cultural dimensions
  };
}
```

**Regional Business Patterns:**
- **North (Hanoi):** Formal hierarchy, government proximity, structured decision-making
- **South (HCMC):** Entrepreneurial, faster decisions, international business exposure  
- **Central (Da Nang/Hue):** Traditional values, consensus-building, cultural preservation

## 🔧 Development Workflows

**Frontend Development:**
```bash
npm run dev          # Start Vite dev server (localhost:5173)
npm run build        # Production build
npm run typecheck    # TypeScript validation
```

**Backend Development:**
```powershell
# Start backend server in separate window (prevents shutdown from subsequent commands)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\backend; python main_prototype.py"

# View API docs at http://localhost:8000/docs
# Verify server is running: (Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing).StatusCode
```

**CRITICAL - Backend Server Management:**
- **ALWAYS use `Start-Process powershell`** to run backend in separate window
- **DO NOT run `python main_prototype.py` directly** in current terminal (subsequent commands will shutdown server)
- Backend requires working directory to be `backend/` for proper module imports
- Server runs on http://localhost:8000 with auto-reload enabled
- Dependencies: All packages in `backend/requirements.txt` must be installed first

**VeriPortal Component Pattern:**
Each VeriPortal module follows this structure:
```
VeriPortal/ModuleName/
├── components/VeriModuleNameSystem.tsx  # Main component
├── types.ts                            # Vietnamese business types
├── services/                           # API integration
└── styles/                            # Cultural CSS
```

## �️ Microservices Architecture Standards

**Architecture Overview:**
- **Main Backend** (`backend/`) - API Gateway with RBAC enforcement (port 8000)
- **Microservices** (`services/`) - Independent FastAPI services (ports 8001+)
- **Communication:** Main backend proxies requests to microservices with JWT token forwarding

**CRITICAL - Service Directory Structure:**
```
services/
├── veri-aidpo-service/      # VeriAIDPO Classification Service (port 8001)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── main.py              # FastAPI entry point
│   ├── .env.example
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py        # Pydantic settings
│   │   ├── api/v1/endpoints/
│   │   ├── core/            # Business logic
│   │   ├── ml/              # ML models (if applicable)
│   │   └── auth/            # JWT validation
│   ├── models/              # ML model cache (volume mount)
│   └── tests/
└── veri-portal-service/     # VeriPortal Dashboard Service (port 8002)
    └── [same structure]
```

**Service Naming Convention:**
- **Directory:** `veri-[module-name]-service` (e.g., `veri-aidpo-service`)
- **Service Name:** VeriAIDPO Classification Service, VeriPortal Dashboard Service
- **Port Range:** 8001-8099 (8000 reserved for main backend)
- **Container Name:** `verisyntra-[module-name]` (e.g., `verisyntra-veriaidpo`)

**Service Configuration Standards:**

```python
# app/config.py - Use pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Service info
    service_name: str = "VeriAIDPO Classification Service"
    service_version: str = "1.0.0"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    
    # JWT Authentication
    jwt_secret_key: str = ""  # Shared with main backend
    jwt_algorithm: str = "HS256"
    
    # Database (shared PostgreSQL)
    database_url: str = ""
    
    # Redis (service-specific database number)
    redis_url: str = "redis://redis:6379/1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

**Service-to-Service Communication:**

Main backend acts as **API Gateway** with RBAC enforcement:

```python
# Main backend proxy endpoint
@router.post("/veriaidpo/classify")
async def classify_proxy(
    request: ClassificationRequest,
    current_user: CurrentUser = Depends(require_permission("processing_activity.read"))
):
    """Proxy to VeriAIDPO microservice with RBAC enforcement"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://veriaidpo-service:8001/api/v1/classify",
            json=request.dict(),
            headers={
                "Authorization": f"Bearer {generate_service_token(current_user)}",
                "X-Tenant-ID": current_user.tenant_id
            }
        )
        return response.json()
```

**Authentication Standards:**

Each microservice validates JWT tokens independently:

```python
# services/veri-aidpo-service/app/auth/jwt_validator.py
from jose import jwt, JWTError
from app.config import settings

def validate_token(token: str) -> dict:
    """Validate JWT token using shared secret"""
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Docker Compose Integration:**

```yaml
# docker-compose.yml (ROOT)
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - veriaidpo-service
      - veriportal-service
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - VERIAIDPO_SERVICE_URL=http://veriaidpo-service:8001
      - VERIPORTAL_SERVICE_URL=http://veriportal-service:8002
    networks:
      - verisyntra-network

  veriaidpo-service:
    build: ./services/veri-aidpo-service
    container_name: verisyntra-veriaidpo
    ports:
      - "8001:8001"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=postgresql://verisyntra:password@postgres:5432/verisyntra
      - REDIS_URL=redis://redis:6379/1
    volumes:
      - veriaidpo-models:/app/models  # ML model cache (20GB)
    networks:
      - verisyntra-network
    depends_on:
      - postgres
      - redis

  veriportal-service:
    build: ./services/veri-portal-service
    container_name: verisyntra-veriportal
    ports:
      - "8002:8002"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=postgresql://verisyntra:password@postgres:5432/verisyntra
      - REDIS_URL=redis://redis:6379/3
    networks:
      - verisyntra-network
    depends_on:
      - postgres
      - redis

networks:
  verisyntra-network:
    driver: bridge

volumes:
  veriaidpo-models:  # Persistent ML model storage
```

**Testing Standards:**

```
backend/tests/
├── unit/                    # Fast unit tests (< 1 min)
├── system/                  # Integration tests (~3-4 min)
│   ├── test_rbac_protected_endpoints.py
│   ├── test_veriaidpo_microservice.py    # VeriAIDPO service integration
│   └── test_veriportal_microservice.py   # VeriPortal service integration
└── ml/                      # ML model tests (10-15 min)

services/veri-aidpo-service/tests/
├── test_classification_api.py           # Service-specific unit tests
└── test_jwt_validation.py               # Authentication tests

services/veri-portal-service/tests/
├── test_dashboard_api.py
└── test_cultural_intelligence.py
```

**Service Health Checks:**

Every microservice must implement:

```python
# main.py
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.service_name,
        "version": settings.service_version
    }
```

**Migration Workflow:**

When extracting service from monolithic backend:

1. **Phase 1: Service Extraction (2-3 hours)**
   - Create service directory structure
   - Copy core components from `backend/app/`
   - Create configuration files
   - Update import paths
   - Validate with `backend/quick_validate.py`

2. **Phase 2: Authentication Integration (1-2 hours)**
   - Create JWT validation middleware
   - Implement permission checking
   - Add service-to-service authentication

3. **Phase 3: Docker Configuration (30 min)**
   - Create Dockerfile
   - Update docker-compose.yml
   - Configure environment variables

4. **Phase 4: Backend Integration (1-2 hours)**
   - Create proxy endpoints in main backend
   - Update router configuration
   - Add RBAC enforcement

5. **Phase 5: Testing & Validation (1-2 hours)**
   - Update integration tests
   - Run regression tests
   - Verify service isolation

6. **Phase 6: Deployment (30 min)**
   - Build Docker images
   - Start services
   - Monitor health checks

**Service Isolation Benefits:**

- **Fault Tolerance:** Service crashes don't affect main backend
- **Independent Scaling:** Scale ML-heavy services independently
- **Resource Allocation:** Dedicated RAM/CPU per service
- **Development Velocity:** Teams work on services independently
- **Testing:** Services tested in isolation

**Shared Resources:**

- **PostgreSQL Database:** All services use same database with tenant isolation
- **Redis:** Each service uses different database number (0=backend, 1=VeriAIDPO, 2=VeriPortal)
- **JWT Secret Key:** Shared across all services for authentication
- **Network:** All services on same Docker network for inter-service communication

**Documentation:**

Each microservice must organize documentation by purpose in subdirectories:
- Migration documentation: `docs/VeriAIDPO/Migration/`
- New features: `docs/VeriAIDPO/New/`
- Feature updates: `docs/VeriAIDPO/Update/`
- Removed features: `docs/VeriAIDPO/Delete/`

**Document Directory Structure:**
- **ALWAYS use service name as directory** under `docs/` (e.g., `docs/VeriAIDPO/`, `docs/VeriPortal/`)
- **Organize by purpose** with subdirectories: `Migration/`, `New/`, `Update/`, `Delete/`
- **Example structure:**
  ```
  docs/
  ├── VeriAIDPO/                              # VeriAIDPO service documentation
  │   ├── Migration/                          # Migration from monolithic backend
  │   │   ├── VeriAIDPO_Microservice_Migration_Plan.md
  │   │   ├── VeriAIDPO_Phase1_Todo_List.md
  │   │   └── VeriAIDPO_PHASE1_COMPLETE.md
  │   ├── New/                                # New features documentation
  │   │   ├── VeriAIDPO_Advanced_Classification.md
  │   │   └── VeriAIDPO_Model_Versioning.md
  │   ├── Update/                             # Feature updates/changes
  │   │   ├── VeriAIDPO_API_V2_Update.md
  │   │   └── VeriAIDPO_Performance_Improvements.md
  │   └── Delete/                             # Removed/deprecated features
  │       └── VeriAIDPO_Legacy_Endpoints_Removal.md
  ├── VeriPortal/                             # VeriPortal service documentation
  │   ├── Migration/
  │   │   ├── VeriPortal_Microservice_Migration_Plan.md
  │   │   └── VeriPortal_PHASE2_COMPLETE.md
  │   ├── New/
  │   ├── Update/
  │   └── Delete/
  └── Veri_Intelligent_Data/                  # Monolithic backend documentation
      └── [existing documentation]
  ```

**Document Naming Convention:**
- **ALWAYS use service name prefix** for microservice documentation files (e.g., `VeriAIDPO_`, `VeriPortal_`)
- **Migration plans:** `docs/VeriAIDPO/Migration/VeriAIDPO_Microservice_Migration_Plan.md`
- **Todo lists:** `docs/VeriAIDPO/Migration/VeriAIDPO_[FeatureName]_Todo_List.md` or `docs/VeriAIDPO/New/VeriAIDPO_[FeatureName]_Todo_List.md` or `docs/VeriAIDPO/Update/VeriAIDPO_[FeatureName]_Todo_List.md`
- **Completion docs:** `docs/VeriAIDPO/Migration/VeriAIDPO_[FeatureName]_COMPLETE.md` or `docs/VeriAIDPO/New/VeriAIDPO_[FeatureName]_COMPLETE.md` or `docs/VeriAIDPO/Update/VeriAIDPO_[FeatureName]_COMPLETE.md`
- **New features:** `docs/VeriAIDPO/New/VeriAIDPO_[FeatureName].md`
- **Updates:** `docs/VeriAIDPO/Update/VeriAIDPO_[ChangeDescription].md`
- **Deletions:** `docs/VeriAIDPO/Delete/VeriAIDPO_[RemovedFeature].md`
- **Reason:** Clear service identification, organized by purpose, easy to find migration vs new features, consistent documentation structure

**Document Validation:**
- **ALWAYS use `backend/quick_validate.py`** to validate all newly created or updated documentation files
- **Run validation** after creating/updating migration plans, todo lists, completion docs, or any markdown documentation
- **Fix violations** before committing: emoji characters (→ to ->), missing Vietnamese diacritics, hard-coded values
- **Command:** `cd backend; python quick_validate.py "..\docs\VeriAIDPO\Migration\[FileName].md"`
- **Expected result:** `[PASSED] Document is compliant with VeriSyntra standards`

**Code Validation:**
- **ALWAYS use `backend/quick_validate.py`** to validate all newly created or updated Python files
- **Run validation** after creating/updating service scripts, endpoints, utilities, or any Python code
- **Fix violations** before committing: hard-coded values, missing Vietnamese diacritics, emoji characters, missing bilingual fields
- **Command:** `cd backend; python quick_validate.py "..\services\veri-aidpo-service\app\auth\[FileName].py"`
- **Expected result:** `[PASSED] Document is compliant with VeriSyntra standards`
- **Applies to:** Backend Python files, microservice Python files, utility scripts, configuration files

## �🎯 PDPL 2025 Compliance Integration

**Critical:** All data handling must consider PDPL 2025 Vietnamese data protection law:
- Use `VeriBusinessContext` for compliance-aware UI rendering
- Cultural AI engine (`VietnameseCulturalIntelligence`) provides contextual guidance
- Bilingual error messages and audit trails required

**Compliance Wizard Pattern:**
```typescript
const veriWizardTypes = [
  'pdpl-2025-setup',     // Primary compliance wizard
  'data-mapping',        // Vietnamese data categorization
  'policy-generation',   // Culturally appropriate policies
  'audit-preparation'    // MPS reporting integration
];
```

## 🌐 Internationalization Conventions

**Language Priority:** Vietnamese-first with English fallback
```typescript
// In components, use cultural hooks
const { isVietnamese, tCultural } = useCulturalIntelligence();

// Cultural translations with regional context
const title = tCultural('compliance.title', { 
  region: veriBusinessContext.veriRegionalLocation 
});
```

**File Structure:**
- `src/locales/vi/` - Vietnamese translations (primary)
- `src/locales/en/` - English translations (fallback)
- Cultural context embedded in translation keys

## 📊 Data Intelligence Patterns

**VeriAnalytics Dashboard Context:**
```typescript
type VeriAnalyticsScope = 
  | 'compliance-performance'  // PDPL compliance metrics
  | 'cultural-alignment'      // Vietnamese business fit
  | 'regulatory-tracking'     // Government requirement changes
  | 'predictive-analytics';   // Vietnamese market predictions
```

**Vietnamese Business Calendar Integration:**
- Use `Asia/Ho_Chi_Minh` timezone throughout
- Cultural holiday and business cycle awareness in analytics
- Regional business hour optimization (North vs South patterns)

## 🔄 System Integration Points

**Government Systems:** MPS (Ministry of Public Security) integration for PDPL reporting
**Cultural Engine:** All UI decisions routed through Vietnamese cultural intelligence
**AI Training Pipeline:** Jupyter notebooks in `docs/VeriSystems/` for PDPL compliance model training using PhoBERT

## 🎨 UI/UX Cultural Guidelines

**Vietnamese Color Palette:**
- Primary: `#6b8e6b` (Vietnamese green)
- Secondary: `#7fa3c3` (Vietnamese blue)  
- Accent: `#d4c18a` (Vietnamese gold)

**Component Naming Convention:**
- Prefix all Vietnamese-specific components with `Veri`
- Cultural context props always include `veriBusinessContext`
- Bilingual prop interfaces required

## 🚨 Critical Integration Notes

**Backend API Integration:**
- Cultural intelligence API at `/api/v1/veriportal/cultural-context`
- All Vietnamese datetime formatting through cultural engine
- Regional business validation for Vietnamese provinces/cities

**Development Environment:**
- Python environment setup required for Jupyter notebooks
- VnCoreNLP integration for Vietnamese NLP processing
- GPU setup for PhoBERT model training pipelines

## 🔤 Code Style Requirements

**CRITICAL - No Emoji Characters:**
- **NEVER use emoji characters** in any code (✓, ✗, ⚠️, •, →, 🔧, etc.)
- Use ASCII alternatives: `[OK]`, `[ERROR]`, `[WARNING]`, `>`, `->`
- Applies to: Python, TypeScript, JavaScript, JSON, Markdown, comments
- Reason: Terminal compatibility, CI/CD systems, cross-platform support

**Status Indicator Standards:**
```python
# CORRECT - ASCII only
print("[OK] Operation successful")
print("[ERROR] Operation failed")
print("[WARNING] Potential issue detected")
print("  > Item 1")  # Use > for bullet points
print("Step 1 -> Step 2")  # Use -> for arrows

# WRONG - Do not use
print("✓ Operation successful")  # NO EMOJI
print("✗ Operation failed")      # NO EMOJI
print("⚠️ Warning")              # NO EMOJI
print("  • Item 1")              # NO EMOJI
print("Step 1 → Step 2")         # NO EMOJI
```

**CRITICAL - Dynamic Code Over Hard-Coding:**
- **ALWAYS prefer dynamic, reusable code** over hard-coded values
- **Use functions, classes, and configuration** instead of duplicating code
- **Follow DRY (Don't Repeat Yourself)** principle strictly
- **Single source of truth** for data definitions and constants

**Dynamic Coding Standards:**
```python
# CORRECT - Dynamic approach
def calculate_total(items):
    """Reusable function with parameters"""
    return sum(item['price'] for item in items)

# Use existing definitions instead of redefining
if 'PDPL_CATEGORIES' in globals():
    print(f"[OK] Using {len(PDPL_CATEGORIES)} categories")
else:
    raise ValueError("Run Step 2 first to define PDPL_CATEGORIES")

# Dynamic validation with detailed feedback
cat2_total = sum(len(v) for v in CAT2_DISTINCTIVE_PHRASES.values())
print(f"[OK] {cat2_total} markers across {len(CAT2_DISTINCTIVE_PHRASES)} categories")

# WRONG - Hard-coded approach
total = items[0]['price'] + items[1]['price'] + items[2]['price']  # NO - not reusable

# Duplicate definitions (violates DRY)
PDPL_CATEGORIES = {...}  # Defined in Step 2
PDPL_CATEGORIES = {...}  # NO - Redefining in Step 4 (use Step 2's definition)

# Hard-coded counts
print("18 markers loaded")  # NO - calculate dynamically
```

**Code Reusability Checklist:**
- [ ] Check if data/function already exists before creating new
- [ ] Use dependency validation (check prerequisites exist)
- [ ] Calculate values dynamically instead of hard-coding numbers
- [ ] Add clear error messages pointing to dependencies
- [ ] Make functions accept parameters instead of using globals
- [ ] Use configuration files/objects for constants

**CRITICAL - Vietnamese Diacritics:**
- **ALWAYS use proper Vietnamese diacritics** when writing Vietnamese text in code
- **NEVER use non-diacritic Vietnamese** (e.g., "quan ly" should be "quản lý")
- Applies to: Strings, comments, documentation, configuration, UI text
- Reason: Professional appearance, proper pattern matching, NLP compatibility, PDPL compliance

**Vietnamese Diacritics Standards:**
```python
# CORRECT - Proper Vietnamese with diacritics
KEYWORDS = [
    "quản lý khách hàng",  # Customer management
    "địa chỉ",             # Address
    "số điện thoại",       # Phone number
    "hồ sơ",               # Profile
    "dịch vụ"              # Service
]

# WRONG - Non-diacritic Vietnamese
KEYWORDS = [
    "quan ly khach hang",  # NO - Missing diacritics
    "dia chi",             # NO - Missing diacritics
    "so dien thoai",       # NO - Missing diacritics
    "ho so",               # NO - Missing diacritics
    "dich vu"              # NO - Missing diacritics
]

# Comments should also use proper Vietnamese
# CORRECT: Quản lý người dùng - User management
# WRONG: Quan ly nguoi dung - User management
```

**Vietnamese Diacritics Checklist:**
- [ ] All Vietnamese keywords have proper tone marks (á, à, ả, ã, ạ)
- [ ] All Vietnamese text includes proper vowel marks (ă, â, ê, ô, ơ, ư)
- [ ] Check Vietnamese text in: strings, comments, logs, error messages
- [ ] Use Vietnamese spell-check or native speaker review when uncertain
- [ ] Pattern matching accounts for both diacritic and non-diacritic variations if needed

**CRITICAL - Bilingual Output Support (`_vi` Suffix Pattern):**
- **ALWAYS provide bilingual outputs** for user-facing validation messages and compliance results
- **Use `_vi` suffix** for Vietnamese field names (e.g., `status_vi`, `message_vi`)
- **Vietnamese-first approach:** Vietnamese translations are primary, English is secondary
- Applies to: Validation outputs, compliance reports, error messages, recommendations
- Internal logs and debugging remain English-only

**Bilingual Output Standards:**
```python
# CORRECT - Bilingual output with _vi suffix
validation_result = {
    'is_compliant': True,
    'is_compliant_vi': 'Tuân thủ',  # Vietnamese translation
    'status': 'compliant',
    'status_vi': 'tuân thủ',
    'message': 'Transfer approved',
    'message_vi': 'Chuyển giao được phê duyệt',
    'recommendations': ['Use encryption'],
    'recommendations_vi': ['Sử dụng mã hóa']
}

# WRONG - English-only output for Vietnamese users
validation_result = {
    'is_compliant': True,
    'status': 'compliant',  # NO - Missing Vietnamese translation
    'message': 'Transfer approved'  # NO - Vietnamese users need Vietnamese
}
```

**Vietnamese Legal Terminology (PDPL 2025):**
- Cross-border transfer: "chuyển giao xuyên biên giới"
- Data protection: "bảo vệ dữ liệu cá nhân"
- PDPL Article 20: "Điều 20 PDPL" or "Điều 20 Luật Bảo vệ Dữ liệu Cá nhân"
- Ministry of Public Security: "Bộ Công an" (MPS in English)
- Adequate protection: "bảo vệ tương đương"
- Standard contractual clauses: "điều khoản hợp đồng tiêu chuẩn"
- Explicit consent: "sự đồng ý rõ ràng"
- Compliant: "tuân thủ"
- Non-compliant: "không tuân thủ"
- Requires review: "cần xem xét"
- Pending MPS approval: "chờ phê duyệt Bộ Công an"

**Bilingual Output Checklist:**
- [ ] All validation outputs include both English and Vietnamese fields
- [ ] Vietnamese translations use proper diacritics
- [ ] Legal terminology follows official PDPL Vietnamese translations
- [ ] Status messages include `_vi` suffix for Vietnamese versions
- [ ] Recommendations/issues arrays have both English and Vietnamese versions
- [ ] Internal logs remain English-only (no bilingual requirement)
- [ ] API documentation shows example bilingual outputs

**CRITICAL - Database Identifiers WITHOUT Diacritics:**
- **DO NOT use Vietnamese diacritics** in database column names, table names, or technical identifiers
- **Use non-diacritic Vietnamese** for database schemas to ensure compatibility
- **Add Vietnamese comments** with proper diacritics to explain what identifiers mean
- Applies to: SQL column names, MongoDB field names, API parameter names, file paths
- Reason: Database compatibility, ASCII-safe identifiers, system interoperability

**Database Identifier Standards:**
```python
# CORRECT - Non-diacritic identifiers with Vietnamese comments
column_patterns = [
    # Họ tên (Full name)
    "ho_ten", "ten", "ho",
    
    # Số điện thoại (Phone number)
    "so_dien_thoai", "dien_thoai", "phone",
    
    # Địa chỉ (Address)
    "dia_chi", "address"
]

# Database column definition
CREATE TABLE nguoi_dung (  -- Người dùng (User table)
    ho_ten VARCHAR(255),    -- Họ tên (Full name)
    dia_chi TEXT,           -- Địa chỉ (Address)
    so_dien_thoai VARCHAR(20)  -- Số điện thoại (Phone)
);

# WRONG - Diacritics in database identifiers
CREATE TABLE người_dùng (  -- NO - Database name should be ASCII
    họ_tên VARCHAR(255),   -- NO - Column name should be ASCII
    địa_chỉ TEXT           -- NO - Column name should be ASCII
);
```

**When to Use/Avoid Vietnamese Diacritics:**

✅ **USE diacritics:**
- User-facing strings and messages
- Comments and documentation
- Log messages shown to users
- UI labels and translations
- Vietnamese configuration values (not keys)
- PDPL compliance reports
- Vietnamese keyword search patterns

❌ **AVOID diacritics:**
- Database table names
- Database column names
- MongoDB collection/field names
- API endpoint paths
- API parameter names (query/body)
- File paths and filenames
- Environment variable names
- Python variable names (use English)
- Function/class names (use English)
- Configuration keys (values can have diacritics)

**Database Identifier Checklist:**
- [ ] Table names use non-diacritic Vietnamese or English
- [ ] Column names use ASCII-safe identifiers (e.g., `ho_ten`, not `họ_tên`)
- [ ] Add Vietnamese comments explaining what identifiers represent
- [ ] API parameters use snake_case without diacritics
- [ ] File paths use ASCII-safe characters only
- [ ] Configuration keys are ASCII, values can have diacritics

## 🧹 Test & Verification Script Management

**CRITICAL - Cleanup After Testing:**
- **ALWAYS delete test/verification scripts** after successful testing completion
- **Only keep essential test files** in dedicated test directories (`tests/`, `__tests__/`)
- **Remove temporary verification scripts** from production code directories
- **Keep workspace clean** - no orphaned test files in source directories

**Test Script Lifecycle:**
```python
# Step 1: Create verification script for testing
# File: verify_step1_complete.py (temporary)

# Step 2: Run verification and confirm all tests pass
# Command: python verify_step1_complete.py
# Result: [OK] All tests passed

# Step 3: DELETE verification script immediately after success
# Command: Remove-Item verify_step1_complete.py
# Reason: Prevents workspace clutter, keeps codebase clean
```

**Test Script Guidelines:**
1. **Temporary Scripts:** Create in same directory as code being tested
2. **Naming Convention:** `verify_*.py`, `test_*.py`, `check_*.py`
3. **After Success:** DELETE immediately - don't commit to repository
4. **Permanent Tests:** Move to `backend/tests/` directory if needed long-term
5. **Documentation:** Keep results in markdown (e.g., `STEP1_COMPLETE.md`)

**Test Organization Standard:**
- **CRITICAL:** All backend test scripts MUST be in `backend/tests/` directory
- **Unit Tests:** `backend/tests/unit/` - Fast unit tests for core logic
  - Python: `test_*.py` - Password utils, JWT, token blacklist, PDPL normalizer
  - No external dependencies (mocked where needed)
  - Duration: < 1 minute
  - Trigger: Every code change
  - Documentation: `backend/tests/unit/README.md`
- **System Tests:** `backend/tests/system/` - Integration and database validation
  - Python: `test_auth_phase2.py`, `test_admin_companies_api.py`, `test_company_registry.py`
  - Python: `test_ropa_endpoints.py`, `test_database_integration.py`, `test_visualization_reporting.py`
  - PowerShell: `test_vietnamese_encoding.ps1` - Vietnamese UTF-8 encoding tests
  - Requires running backend and database
  - Duration: ~3-4 minutes
  - Trigger: Every code change, PR, deployment
  - Documentation: `backend/tests/system/README.md`
- **ML Tests:** `backend/tests/ml/` - Slow tests for ML validation
  - Model tests: `test_model_integration.py`, `test_all_model_types.py`
  - API tests: `test_veriaidpo_classification_api.py`
  - Dataset tests: `test_vietnamese_hard_dataset_generator.py`
  - Runner: `run_ml_tests.py` - ML test suite (10-15 min, use `--quick` for 3-5 min)
  - Trigger: ML changes, model updates, scheduled/nightly
  - Documentation: `backend/tests/ml/README.md`
- **Frontend Tests:** `src/__tests__/` or `src/components/**/__tests__/` - React component tests
- **Main Documentation:** `backend/tests/README.md`

**Microservice Test Organization:**
- **CRITICAL:** All microservice test scripts MUST be in `Test/services/{service_name}/` directory
- **Directory Structure:**
  ```
  Test/
  └── services/
      ├── veri-aidpo-service/
      │   ├── unit/                    # Unit tests for microservice
      │   │   ├── test_jwt_validator.py
      │   │   ├── test_permissions.py
      │   │   └── test_classification_logic.py
      │   ├── system/                  # Integration tests for microservice
      │   │   ├── test_authentication_integration.py
      │   │   ├── test_classification_api.py
      │   │   └── test_model_integration.py
      │   └── Regression_Test_VeriAIDPO.py  # Main regression test runner
      └── veri-portal-service/
          ├── unit/
          ├── system/
          └── Regression_Test_VeriPortal.py
  ```
- **Unit Tests:** `Test/services/{service_name}/unit/` - Fast microservice unit tests
  - Test authentication modules (JWT validation, permissions)
  - Test business logic without external dependencies
  - Mock database and API calls
  - Duration: < 1 minute
  - Trigger: Every code change
- **System Tests:** `Test/services/{service_name}/system/` - Microservice integration tests
  - Test API endpoints with authentication
  - Test database integration
  - Test service-to-service communication
  - Requires running microservice
  - Duration: ~2-3 minutes
  - Trigger: Every code change, PR, deployment
- **Regression Test Runner:** `Test/services/{service_name}/Regression_Test_{ServiceName}.py`
  - Naming: `Regression_Test_VeriAIDPO.py`, `Regression_Test_VeriPortal.py`
  - Runs all unit + system tests for the microservice
  - Auto-updates when new tests are added to unit/ or system/
  - Reports: Pass/fail summary, execution time, coverage (optional)
  - Example:
    ```python
    """
    VeriAIDPO Microservice Regression Test Runner
    Auto-discovers and runs all unit and system tests
    """
    import pytest
    import os
    
    def run_regression_tests():
        test_dirs = [
            "Test/services/veri-aidpo-service/unit",
            "Test/services/veri-aidpo-service/system"
        ]
        pytest.main(["-v", "--tb=short"] + test_dirs)
    
    if __name__ == "__main__":
        run_regression_tests()
    ```

**Microservice Testing Standards:**
- **ALWAYS create/update regression test runner** when adding new unit or system tests
- **Test file naming:** `test_*.py` for all test files
- **Test class naming:** `Test{FeatureName}` (e.g., `TestJWTValidation`, `TestClassificationAPI`)
- **Test method naming:** `test_{scenario}_{expected}` (e.g., `test_classify_no_token_returns_403`)
- **Fixtures:** Use `conftest.py` in each test directory for shared fixtures
- **Assertions:** Use descriptive assertion messages
- **Cleanup:** Always clean up test data in teardown methods

**Test Execution Patterns:**
- **Unit Tests:** Fast core logic tests (< 1 min) - No external dependencies
- **System Tests:** Integration and database tests (~3-4 min) - Requires infrastructure
- **Backend Regression:** Unit + System tests combined (~3-4 min total)
- **ML Tests:** Run separately from backend regression (10-15 min)
- **DO NOT** mix unit/system tests with ML tests (different test cadence)

**What to DELETE After Testing:**
- `verify_step1_complete.py` - One-time verification script
- `check_*.py` - Temporary validation scripts
- `test_integration_*.py` - Ad-hoc integration tests (move to `backend/tests/` if permanent)
- `validate_*.py` - One-off validation scripts

**What to KEEP in `backend/tests/`:**
- `test_*.py` - Permanent pytest test suites
- `test_*.ps1` - PowerShell test scripts (e.g., Vietnamese encoding)
- `conftest.py` - Pytest configuration
- `run_regression_tests.py` - Unified test runner
- `README.md` - Test documentation
- `STEP*_COMPLETE.md` - Step completion documentation

**Cleanup Commands (PowerShell):**
```powershell
# Delete single verification script
Remove-Item verify_step1_complete.py

# Delete all temporary verification scripts
Remove-Item verify_*.py

# Keep only tests directory
Get-ChildItem -File -Filter "*test*.py" | Where-Object {$_.DirectoryName -notlike "*\tests\*"} | Remove-Item
```

**Example Cleanup After Step 1:**
```powershell
# Step 1 implementation complete and verified
cd backend/veri_ai_data_inventory

# Remove temporary verification script
Remove-Item verify_step1_complete.py

# Keep documentation and config
# KEEP: STEP1_COMPLETE.md (documentation)
# KEEP: config/constants.py (production code)
# KEEP: config/__init__.py (production code)
```

## 🗄️ Database Migration Standards

**CRITICAL - Vietnamese UTF-8 Encoding Protection:**
- **ALWAYS use `scripts\run_migration_safe.ps1`** for migrations with Vietnamese text
- **NEVER use PowerShell pipe** (`Get-Content | docker exec`) - corrupts UTF-8 multi-byte characters
- **Reason:** PowerShell pipeline converts Vietnamese diacritics (ạ, ộ, ệ, ủ) to ASCII replacements (`???`)

**Migration Execution Pattern:**
```powershell
# ✓ CORRECT - Use safe migration script
.\scripts\run_migration_safe.ps1 -MigrationFile "backend\veri_ai_data_inventory\migrations\add_permissions_table.sql"

# ❌ WRONG - PowerShell pipe corrupts Vietnamese UTF-8
Get-Content migration.sql | docker exec -i verisyntra-postgres psql -U verisyntra -d verisyntra
```

**Safe Migration Script Features:**
- ✓ UTF-8 encoding preservation using `docker cp`
- ✓ Pre-migration validation for missing Vietnamese diacritics
- ✓ Automatic detection of non-diacritic patterns (nguoi → người, cong ty → công ty)
- ✓ Post-migration encoding verification (byte_count > char_count)
- ✓ Interactive prompts if issues detected
- ✓ Colored output and detailed logging

**Migration File Standards:**
```sql
-- CORRECT - SQL migration with proper Vietnamese diacritics
INSERT INTO permissions (permission_name, permission_name_vi, description_vi) VALUES
('user.read', 'Xem người dùng', 'Xem thông tin người dùng trong hệ thống'),
('user.write', 'Tạo/sửa người dùng', 'Tạo và cập nhật người dùng'),
('data_category.manage', 'Quản lý danh mục', 'Quản lý danh mục dữ liệu cá nhân');

-- WRONG - Missing Vietnamese diacritics
INSERT INTO permissions (permission_name, permission_name_vi, description_vi) VALUES
('user.read', 'Xem nguoi dung', 'Xem thong tin nguoi dung'),  -- NO - Missing diacritics
('user.write', 'Tao/sua nguoi dung', 'Tao va cap nhat');      -- NO - Missing diacritics
```

**Vietnamese Encoding Validation:**

After migration, verify encoding integrity:
```powershell
# Run comprehensive encoding tests
.\scripts\test_vietnamese_encoding.ps1

# Strict mode (fail on warnings)
.\scripts\test_vietnamese_encoding.ps1 -FailOnWarnings $true
```

**Manual Verification Query:**
```sql
-- Check if Vietnamese UTF-8 is correct (bytes > chars for diacritics)
SELECT 
    permission_name,
    permission_name_vi,
    length(permission_name_vi) as chars,
    octet_length(permission_name_vi) as bytes,
    CASE 
        WHEN octet_length(permission_name_vi) > length(permission_name_vi) 
        THEN 'UTF-8 OK' 
        ELSE 'CHECK' 
    END as status
FROM permissions
WHERE permission_name_vi IS NOT NULL
LIMIT 5;

-- Expected: bytes > chars (e.g., "Người dùng" = 10 chars, 14 bytes)
-- If bytes = chars for all entries → UTF-8 corruption detected
```

**Migration Checklist:**
- [ ] Use `.\scripts\run_migration_safe.ps1` for all Vietnamese migrations
- [ ] Verify SQL file has proper Vietnamese diacritics (not "nguoi dung")
- [ ] Review pre-migration warnings if script detects issues
- [ ] Run `.\scripts\test_vietnamese_encoding.ps1` after migration
- [ ] Check sample data with char/byte count query
- [ ] Document migration in `STEP*_COMPLETE.md`

**Common Vietnamese Diacritics Issues in Migrations:**

| ❌ Wrong (No Diacritics) | ✓ Correct (With Diacritics) |
|-------------------------|----------------------------|
| nguoi dung              | người dùng                 |
| cong ty                 | công ty                    |
| dia chi                 | địa chỉ                    |
| quan ly                 | quản lý                    |
| bao mat                 | bảo mật                    |
| nhan vien               | nhân viên                  |
| chu the                 | chủ thể                    |
| du lieu                 | dữ liệu                    |
| hop dong                | hợp đồng                   |
| dang ky                 | đăng ký                    |

**Regression Testing Integration:**

Include Vietnamese encoding tests in CI/CD:
```yaml
# .github/workflows/database-tests.yml
- name: Run Vietnamese encoding tests
  run: .\scripts\test_vietnamese_encoding.ps1 -FailOnWarnings $true
```

**Recovery from Corrupted Migration:**

If Vietnamese encoding was corrupted:
```powershell
# Step 1: Delete corrupted data
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "DELETE FROM table_name;"

# Step 2: Re-run with safe script
.\scripts\run_migration_safe.ps1 -MigrationFile "path\to\migration.sql"

# Step 3: Verify fix
.\scripts\test_vietnamese_encoding.ps1
```

When working on this codebase, always consider the Vietnamese business cultural context first, then implement technical solutions that respect these cultural patterns while maintaining PDPL 2025 compliance requirements.