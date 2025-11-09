# VeriAIDPO Microservice Migration - Phase 3: Docker Configuration

**Status:** Not Started  
**Estimated Time:** 30 minutes  
**Objective:** Create Docker configuration files for containerized deployment of VeriAIDPO service

---

## Prerequisites

- [x] Phase 1 complete (service structure created, core components copied)
- [x] Phase 2 complete (JWT authentication integration, permission checking)
- [ ] Docker Desktop installed and running
- [ ] Docker Compose v3.8+ available
- [ ] Access to HuggingFace token (for model downloads)
- [ ] Understanding of Docker networking and volumes

---

## Phase 3 Steps

### Step 3.1: Create Dockerfile (15 min)

**Objective:** Build Docker image for VeriAIDPO service with all dependencies

**Tasks:**

1. **Create Dockerfile**
   ```powershell
   # Working directory: C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\services\veri-aidpo-service
   New-Item -ItemType File -Path "Dockerfile" -Force
   ```

2. **Implement Dockerfile configuration**
   ```dockerfile
   # Base image: Python 3.13-slim for smaller image size
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

3. **Key configuration points:**
   - **Base image:** `python:3.13-slim` (smaller than full Python image)
   - **System deps:** `build-essential` for compiling Python packages (PyTorch, transformers)
   - **No cache:** `--no-cache-dir` reduces image size
   - **Clean up:** Remove apt lists to reduce layer size
   - **Model directory:** `/app/models` for HuggingFace model cache (volume mount)
   - **Port 8001:** VeriAIDPO service port
   - **Reload flag:** `--reload` for development (remove in production)

**Validation:**
```powershell
# Dockerfile is not Python, validation may not apply fully
# Focus on ensuring ASCII-only content, no emoji characters
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\backend
python quick_validate.py "..\services\veri-aidpo-service\Dockerfile"
```

**Completion Criteria:**
- [ ] Dockerfile created in `services/veri-aidpo-service/`
- [ ] Uses Python 3.13-slim base image
- [ ] Installs build-essential system dependencies
- [ ] Copies requirements.txt and installs dependencies
- [ ] Copies app/ directory and main.py
- [ ] Creates /app/models directory for model cache
- [ ] Exposes port 8001
- [ ] CMD runs uvicorn on 0.0.0.0:8001
- [ ] No emoji characters (ASCII-only content)

---

### Step 3.2: Create Docker Compose Configuration (15 min)

**Objective:** Configure service orchestration with dependencies (PostgreSQL, Redis)

**Tasks:**

1. **Create docker-compose.yml**
   ```powershell
   New-Item -ItemType File -Path "docker-compose.yml" -Force
   ```

2. **Implement Docker Compose configuration**
   ```yaml
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

3. **Key configuration points:**
   - **Container name:** `verisyntra-veriaidpo` (consistent naming)
   - **Port mapping:** `8001:8001` (host:container)
   - **Environment variables:**
     - `JWT_SECRET_KEY` - Shared with main backend (from .env)
     - `JWT_ALGORITHM=HS256` - Token signing algorithm
     - `DATABASE_URL` - PostgreSQL connection (shared database)
     - `REDIS_URL=redis://redis:6379/2` - Redis database 2 (VeriAIDPO-specific)
     - `HUGGINGFACE_TOKEN` - For model downloads (from .env)
     - `MODEL_CACHE_DIR=/app/models` - Model storage path
   - **Volumes:**
     - `./models:/app/models` - Persistent model storage (20GB)
     - `./app:/app/app` - Hot reload for development
   - **Network:** `verisyntra-network` (external, shared with main backend)
   - **Dependencies:** `postgres`, `redis` (must start first)
   - **Restart policy:** `unless-stopped` (auto-restart on failure)

4. **Create .env.example file**
   ```powershell
   New-Item -ItemType File -Path ".env.example" -Force
   ```
   
   Content:
   ```env
   JWT_SECRET_KEY=your-secret-key-here
   HUGGINGFACE_TOKEN=your-huggingface-token-here
   ```

**Validation:**
```powershell
# YAML validation (syntax check)
# No Python validator for YAML, manual review required
```

**Completion Criteria:**
- [ ] docker-compose.yml created in `services/veri-aidpo-service/`
- [ ] Service name: `veriaidpo-service`
- [ ] Container name: `verisyntra-veriaidpo`
- [ ] Port 8001 exposed and mapped
- [ ] All required environment variables configured
- [ ] Redis URL uses database 2 (not 0 or 1)
- [ ] Volume mounts configured (models, app code)
- [ ] Network set to `verisyntra-network` (external)
- [ ] Depends on postgres and redis
- [ ] Restart policy set to `unless-stopped`
- [ ] .env.example file created with required variables

---

### Step 3.3: Test Docker Build (20 min)

**Objective:** Verify Docker image builds successfully and service starts

**Tasks:**

1. **Build Docker image**
   ```powershell
   cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\services\veri-aidpo-service
   
   docker-compose build
   ```

2. **Expected output:**
   ```
   [+] Building 45.2s (12/12) FINISHED
    => [internal] load build definition from Dockerfile
    => [internal] load .dockerignore
    => [internal] load metadata for docker.io/library/python:3.13-slim
    => [1/7] FROM docker.io/library/python:3.13-slim
    => [2/7] WORKDIR /app
    => [3/7] RUN apt-get update && apt-get install -y build-essential
    => [4/7] COPY requirements.txt .
    => [5/7] RUN pip install --no-cache-dir -r requirements.txt
    => [6/7] COPY app/ ./app/
    => [7/7] COPY main.py .
    => exporting to image
    => => naming to docker.io/library/veri-aidpo-service_veriaidpo-service
   ```

3. **Troubleshooting common build errors:**
   - **"requirements.txt not found"** - Check file exists in service directory
   - **"app/ directory not found"** - Verify app/ directory structure exists
   - **"pip install failed"** - Check requirements.txt for version conflicts
   - **"build-essential not found"** - Verify apt-get update runs successfully

4. **Verify image created**
   ```powershell
   docker images | Select-String "veriaidpo"
   ```

5. **Test container start (optional - without dependencies)**
   ```powershell
   # Test if container can start (will fail without postgres/redis)
   docker run --rm -p 8001:8001 veri-aidpo-service_veriaidpo-service
   
   # Expected: Service starts but may error on database connection
   # Stop with Ctrl+C
   ```

**Completion Criteria:**
- [ ] `docker-compose build` completes successfully
- [ ] No build errors related to Dockerfile syntax
- [ ] No errors installing dependencies from requirements.txt
- [ ] Docker image created (verify with `docker images`)
- [ ] Image size reasonable (~2-3GB with PyTorch)
- [ ] Test container start shows FastAPI starting (even if database errors)

---

### Step 3.4: Create Phase 3 Completion Documentation (20 min)

**Objective:** Document Docker configuration and build results

**Tasks:**

1. **Create completion document**
   ```powershell
   cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\docs\VeriAIDPO\Migration
   New-Item -ItemType File -Path "VeriAIDPO_Microservice_Migration_PHASE3_COMPLETE.md" -Force
   ```

2. **Document contents (structure):**
   - **Overview:** Phase 3 summary (Docker configuration)
   - **Files Created:**
     - Dockerfile (with full content)
     - docker-compose.yml (with full content)
     - .env.example (with variables)
   - **Build Results:**
     - Build command output
     - Image size
     - Build time
     - Layers breakdown
   - **Environment Variables:**
     - JWT_SECRET_KEY - Purpose and source
     - DATABASE_URL - Shared PostgreSQL connection
     - REDIS_URL - VeriAIDPO-specific database (redis://redis:6379/2)
     - HUGGINGFACE_TOKEN - Model download authentication
     - MODEL_CACHE_DIR - Model storage path
   - **Volume Mounts:**
     - ./models:/app/models - Persistent model storage (20GB)
     - ./app:/app/app - Hot reload for development
   - **Network Configuration:**
     - verisyntra-network (external) - Shared with main backend
     - Service discovery via container name
   - **Validation Results:**
     - Dockerfile validation output
     - Build test results
   - **Next Steps:**
     - Phase 4: Backend Integration
     - Create proxy endpoints in main backend
     - Update root docker-compose.yml

3. **Content guidelines:**
   - Use `[OK]` not checkmarks (no emoji)
   - Include Vietnamese diacritics for Vietnamese terms
   - Document actual build output (copy from terminal)
   - Include troubleshooting notes if issues encountered
   - Reference migration plan sections

**Validation:**
```powershell
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\backend
python quick_validate.py "..\docs\VeriAIDPO\Migration\VeriAIDPO_Microservice_Migration_PHASE3_COMPLETE.md"
```

**Completion Criteria:**
- [ ] PHASE3_COMPLETE.md created in docs/VeriAIDPO/Migration/
- [ ] Includes Dockerfile content (full)
- [ ] Includes docker-compose.yml content (full)
- [ ] Documents all environment variables
- [ ] Documents volume mount strategy
- [ ] Documents network configuration
- [ ] Includes build test results
- [ ] Includes validation results
- [ ] No emoji characters (use `[OK]`)
- [ ] Proper Vietnamese diacritics
- [ ] Passes quick_validate.py (100% PASSED)

---

## Validation Checklist

**Docker Configuration Files Created:**
- [ ] `services/veri-aidpo-service/Dockerfile`
- [ ] `services/veri-aidpo-service/docker-compose.yml`
- [ ] `services/veri-aidpo-service/.env.example`

**Docker Build:**
- [ ] `docker-compose build` completes successfully
- [ ] Docker image created (verify with `docker images`)
- [ ] No build errors or warnings
- [ ] Image size appropriate (~2-3GB)

**Configuration Quality:**
- [ ] Dockerfile uses Python 3.13-slim base
- [ ] Build-essential installed for PyTorch compilation
- [ ] Port 8001 exposed correctly
- [ ] Model cache directory created
- [ ] docker-compose.yml uses version 3.8
- [ ] All environment variables documented
- [ ] Redis URL uses database 2 (not 0 or 1)
- [ ] External network configured correctly
- [ ] Volume mounts configured for models and app code

**Documentation:**
- [ ] PHASE3_COMPLETE.md created
- [ ] Includes full Dockerfile content
- [ ] Includes full docker-compose.yml content
- [ ] Documents environment variables
- [ ] Documents volume strategy
- [ ] Documents network configuration
- [ ] Passes validation (no hard-coding, proper diacritics, no emoji)

---

## Troubleshooting

**Issue: "Docker daemon not running"**
- **Cause:** Docker Desktop not started
- **Fix:** Start Docker Desktop, wait for initialization

**Issue: "pip install fails for torch"**
- **Cause:** Insufficient memory during build, or network timeout
- **Fix:** Increase Docker memory limit (Settings -> Resources), use pre-built PyTorch wheels

**Issue: "build-essential package not found"**
- **Cause:** apt-get update failed or base image changed
- **Fix:** Check internet connection, verify base image name

**Issue: "External network verisyntra-network not found"**
- **Cause:** Network not created yet (will be created in root docker-compose.yml)
- **Fix:** Expected at this phase, will be resolved in Phase 6 deployment

**Issue: "COPY failed: no such file or directory app/"**
- **Cause:** app/ directory doesn't exist or incorrect path
- **Fix:** Verify directory structure, check COPY paths match actual locations

**Issue: "Port 8001 already in use"**
- **Cause:** VeriAIDPO service already running from Phase 2
- **Fix:** Stop existing service before testing Docker container

---

## Next Steps

After Phase 3 completion, proceed to:
- **Phase 4:** Backend Integration (1-2 hours)
  - Create proxy endpoints in main backend
  - Update backend router to forward VeriAIDPO requests
  - Configure service-to-service authentication
  - Update root docker-compose.yml to include VeriAIDPO service
- **Phase 5:** Testing & Validation (1-2 hours)
- **Phase 6:** Deployment (30 min)

---

## Git Commit

After completing Phase 3:

```powershell
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra

git add services/veri-aidpo-service/Dockerfile
git add services/veri-aidpo-service/docker-compose.yml
git add services/veri-aidpo-service/.env.example
git add docs/VeriAIDPO/Migration/VeriAIDPO_Microservice_Migration_PHASE3_COMPLETE.md

git commit -m "Phase 3: VeriAIDPO Docker configuration complete

- Created Dockerfile with Python 3.13-slim base image
- Created docker-compose.yml with service orchestration
- Configured environment variables (JWT, database, Redis, HuggingFace)
- Configured volume mounts (models 20GB, app code hot reload)
- Configured verisyntra-network (external, shared with backend)
- Redis database 2 for VeriAIDPO service isolation
- Build tested successfully, image created
- Documentation: PHASE3_COMPLETE.md (validated, PASSED)

Files: 4 created
Build: SUCCESS (~2-3GB image)
Next: Phase 4 - Backend Integration"
```

---

## Additional Notes

**Redis Database Isolation:**
- Main backend: `redis://redis:6379/0`
- VeriAIDPO service: `redis://redis:6379/2`
- Reason: Prevent cache key collisions, service isolation

**Model Cache Volume:**
- Size: ~20GB (11 HuggingFace models)
- Mount: `./models:/app/models`
- Persistence: Survives container restarts
- Pre-download: Can pre-populate models before deployment

**Development vs Production:**
- Development: `--reload` flag, app code volume mount
- Production: Remove `--reload`, no app volume (baked into image)
- Consider: Multi-stage Docker build for smaller production image

**Security Considerations:**
- JWT_SECRET_KEY must match main backend (shared secret)
- HUGGINGFACE_TOKEN should be private (use .env, not committed)
- Database password in connection string (use secrets in production)
