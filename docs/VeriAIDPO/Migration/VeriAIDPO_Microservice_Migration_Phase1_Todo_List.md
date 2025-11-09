# VeriAIDPO Microservice Migration - Phase 1 Todo List

**Phase:** Service Extraction (2-3 hours)  
**Status:** NOT STARTED  
**Date:** November 8, 2025

## Overview
Phase 1 focuses on extracting VeriAIDPO classification service from monolithic backend into independent microservice structure. This phase creates the service directory, copies core components, and sets up basic configuration without starting the service.

## Prerequisites
- [ ] Backend server is running and accessible
- [ ] PostgreSQL database is accessible
- [ ] Docker Desktop is installed and running
- [ ] Git working tree is clean (commit current work)

## Phase 1 Tasks

### Step 1.1: Create Service Directory Structure (30 min)

- [x] Create main service directory
  ```powershell
  New-Item -ItemType Directory -Path "services\veri-aidpo-service" -Force
  ```

- [x] Create app subdirectories
  ```powershell
  New-Item -ItemType Directory -Path "services\veri-aidpo-service\app\api\v1\endpoints" -Force
  New-Item -ItemType Directory -Path "services\veri-aidpo-service\app\core" -Force
  New-Item -ItemType Directory -Path "services\veri-aidpo-service\app\auth" -Force
  New-Item -ItemType Directory -Path "services\veri-aidpo-service\tests" -Force
  New-Item -ItemType Directory -Path "services\veri-aidpo-service\models" -Force
  ```

- [x] Create placeholder files
  ```powershell
  New-Item -ItemType File -Path "services\veri-aidpo-service\app\__init__.py" -Force
  New-Item -ItemType File -Path "services\veri-aidpo-service\app\api\__init__.py" -Force
  New-Item -ItemType File -Path "services\veri-aidpo-service\app\api\v1\__init__.py" -Force
  New-Item -ItemType File -Path "services\veri-aidpo-service\app\api\v1\endpoints\__init__.py" -Force
  New-Item -ItemType File -Path "services\veri-aidpo-service\app\core\__init__.py" -Force
  New-Item -ItemType File -Path "services\veri-aidpo-service\app\auth\__init__.py" -Force
  New-Item -ItemType File -Path "services\veri-aidpo-service\models\.gitkeep" -Force
  ```

- [x] Verify directory structure matches migration plan
  ```powershell
  tree /F services\veri-aidpo-service
  ```

### Step 1.2: Copy Core Components from Backend (45 min)

- [x] Copy model loader
  ```powershell
  # Note: model_loader.py is in app/ml/ not app/core/
  New-Item -ItemType Directory -Path "services\veri-aidpo-service\app\ml" -Force
  Copy-Item -Path "backend\app\ml\model_loader.py" -Destination "services\veri-aidpo-service\app\ml\model_loader.py"
  ```

- [x] Copy PDPL normalizer
  ```powershell
  Copy-Item -Path "backend\app\core\pdpl_normalizer.py" -Destination "services\veri-aidpo-service\app\core\pdpl_normalizer.py"
  ```

- [x] Copy company registry
  ```powershell
  Copy-Item -Path "backend\app\core\company_registry.py" -Destination "services\veri-aidpo-service\app\core\company_registry.py"
  ```

- [x] Copy classification endpoint
  ```powershell
  Copy-Item -Path "backend\app\api\v1\endpoints\veriaidpo_classification.py" -Destination "services\veri-aidpo-service\app\api\v1\endpoints\classification.py"
  ```

- [x] Verify all files copied successfully
  ```powershell
  Get-ChildItem -Path "services\veri-aidpo-service\app" -Recurse -File | Select-Object FullName
  ```

- [x] Update import paths in copied files (remove backend-specific imports)
  - classification.py: Removed sys.path.append, updated router prefix to /api/v1
  - classification.py: Imports from app.ml.model_loader (correct path)
  - classification.py: RBAC imports commented out (will be added in Phase 2)

### Step 1.3: Create Service Dependencies (30 min)

- [x] Create requirements.txt with exact versions
  ```powershell
  New-Item -ItemType File -Path "services\veri-aidpo-service\requirements.txt" -Force
  ```

- [x] Create service configuration file (app/config.py)

- [x] Create .env.example file

### Step 1.4: Create Basic FastAPI Application (45 min)

- [x] Create main.py entry point

- [x] Create health check endpoint (app/api/v1/endpoints/health.py)

### Step 1.5: Validation & Testing (30 min)

- [x] Run quick_validate.py on all created Python files
  - main.py: PASSED
  - config.py: PASSED
  - All files compliant with VeriSyntra standards

- [x] Check for VeriSyntra coding standards violations
  - No emoji characters in code
  - Vietnamese text has proper diacritics
  - No hard-coded values (use config/constants)
  - ASCII-safe database identifiers

- [x] Verify all __init__.py files are present
  ```powershell
  Get-ChildItem -Path "services\veri-aidpo-service" -Recurse -Filter "__init__.py" | Select-Object FullName
  ```

- [x] Document Phase 1 completion
  - Created PHASE1_COMPLETE.md with:
    - Directory structure created
    - Files copied and locations
    - Configuration files created
    - Validation results
    - Next steps (Phase 2)

## Completion Criteria

- [OK] All directories created matching migration plan structure
- [OK] Core components copied from backend (model_loader, pdpl_normalizer, company_registry)
- [OK] Classification endpoint copied and renamed
- [OK] requirements.txt created with all dependencies
- [OK] config.py created with service settings
- [OK] main.py FastAPI application created
- [OK] All Python files pass quick_validate.py checks
- [OK] No VeriSyntra coding standards violations
- [OK] PHASE1_COMPLETE.md documentation created

## Notes

- **DO NOT start the service yet** - Phase 1 is extraction only
- **DO NOT modify backend code** - Only copy files
- **DO NOT create Docker containers** - That is Phase 3
- Keep backend server running during Phase 1 (needed for reference)
- Commit changes after Phase 1 completion: `git add services/veri-aidpo-service && git commit -m "Phase 1: VeriAIDPO service extraction complete"`

## Troubleshooting

**Issue:** Import errors in copied files  
**Solution:** Update import paths to remove backend-specific references (e.g., `from backend.app.core` -> `from app.core`)

**Issue:** quick_validate.py reports hard-coding violations  
**Solution:** Move hard-coded values to config.py or create constants file

**Issue:** Missing __init__.py files  
**Solution:** Ensure all directories have __init__.py (Python packages requirement)

**Issue:** Vietnamese diacritics errors  
**Solution:** Verify all Vietnamese text uses proper diacritics (người not nguoi, dữ liệu not du lieu)

## Next Phase

After Phase 1 completion, proceed to **Phase 2: Authentication Integration (1-2 hours)**
- JWT validation middleware
- Permission checking via token claims
- Service-to-service authentication

---

**Document Status:** READY FOR EXECUTION  
**Last Updated:** November 8, 2025  
**Related:** VeriAIDPO_Microservice_Migration_Plan.md
