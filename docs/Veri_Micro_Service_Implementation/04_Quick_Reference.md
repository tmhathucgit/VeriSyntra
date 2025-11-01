# VeriSyntra Microservices Migration - Quick Reference

**Version:** 1.0.0  
**Date:** November 1, 2025  
**Purpose:** Quick reference for development team during migration

---

## Current vs Target Architecture

### Current (Monolith)
```
Frontend (React) --> FastAPI (main_prototype.py) --> PostgreSQL
                     |
                     +-- All endpoints in one process
                     +-- Vietnamese Cultural Intelligence (inline)
                     +-- PhoBERT ML models (blocking)
                     +-- No service isolation
```

### Target (Microservices)
```
React SPA --> Kong Gateway --> [15+ Independent Services] --> [5 Databases]
                               |
                               +-- Each service scales independently
                               +-- Vietnamese cultural context distributed
                               +-- ML services with GPU optimization
                               +-- Fault tolerance & resilience
```

---

## Migration Priority Order

### Phase 1 (Weeks 1-4): Foundation
**Goal:** Docker environment + first proof-of-concept service

1. [PENDING] Set up Docker Compose development environment
2. [PENDING] Extract `veri-auth-service` (authentication)
3. [PENDING] Configure Kong API Gateway (DB-less mode)
4. [PENDING] Implement service-to-service communication
5. [PENDING] Database setup with PostgreSQL multi-tenant schema

**Success Criteria:**
- [ ] Docker Compose runs all infrastructure services
- [ ] Auth service authenticates users via API Gateway
- [ ] JWT tokens work across services
- [ ] Vietnamese timezone consistent across all services

---

### Phase 2 (Weeks 5-12): Core Services
**Goal:** Extract business logic from monolith

**Priority Services:**
1. **veri-cultural-intelligence** (Vietnamese business context)
2. **veri-company-registry** (Vietnamese company database)
3. **veri-compliance-engine** (PDPL workflows)

**Migration Pattern:**
```
Old: main_prototype.py -> cultural_intelligence.py (inline)
New: veri-cultural-intelligence service (port 8002)
     - Independent deployment
     - Redis caching
     - RESTful API
```

**Success Criteria:**
- [ ] 3 core services running independently
- [ ] Monolith calls new services (Strangler Fig pattern)
- [ ] Vietnamese cultural context API tested
- [ ] Service health checks operational

---

### Phase 3 (Weeks 13-20): AI/ML Isolation
**Goal:** Separate resource-intensive ML workloads

**Services:**
1. **veri-vi-ai-classification** (Structured + Unstructured Classification with Vietnamese patterns and PhoBERT)
2. **veri-vi-nlp-processor** (VnCoreNLP Vietnamese text processing)
3. **veri-ai-data-inventory** (Data discovery, scanning, and mapping)

**Key Changes:**
- ML models in dedicated containers with GPU support
- Asynchronous task queue (Celery + Redis)
- Model versioning and A/B testing
- Batch prediction API

**Success Criteria:**
- [ ] ML inference doesn't block API responses
- [ ] PhoBERT models and pattern libraries load once per container
- [ ] GPU utilization metrics visible
- [ ] Vietnamese text and structured data classification APIs tested

---

### Phase 4 (Weeks 21-32): VeriPortal Decomposition
**Goal:** Break down frontend-facing modules

**VeriPortal Services:**
1. veri-onboarding-service
2. veri-document-generator
3. veri-business-intelligence
4. veri-system-integration (data sync)

**Frontend Changes:**
- React app calls API Gateway instead of direct backend
- Backend-for-Frontend (BFF) pattern evaluation
- Vietnamese locale handling in gateway

---

### Phase 5 (Weeks 33-40): Database Migration
**Goal:** Database per service pattern

**Strategy:**
- Shared PostgreSQL instance with schemas per service
- MongoDB for Vietnamese document templates
- Redis for session/cache
- Elasticsearch for Vietnamese search

**Migration Script Example:**
```sql
-- Old: Single database
CREATE DATABASE verisyntra;

-- New: Service schemas
CREATE SCHEMA veri_auth;
CREATE SCHEMA veri_compliance;
CREATE SCHEMA veri_data_inventory;
```

---

## Service Port Assignments

| Service | Port | Purpose |
|---------|------|---------|
| veri-api-gateway | 80/443 | Entry point |
| veri-auth-service | 8001 | Authentication |
| veri-cultural-intelligence | 8002 | Vietnamese context |
| veri-company-registry | 8003 | Company database |
| veri-compliance-engine | 8004 | PDPL workflows |
| veri-document-generator | 8005 | Document templates |
| veri-vi-ai-classification | 8006 | Structured + Unstructured Classification |
| veri-vi-nlp-processor | 8007 | VnCoreNLP |
| veri-onboarding-service | 8008 | Cultural onboarding |
| veri-business-intelligence | 8009 | Analytics |
| veri-ai-data-inventory | 8010 | Data discovery & mapping |
| veri-data-sync-service | 8011 | ERP/HRM sync |
| veri-notification-service | 8012 | Email/SMS |

---

## Common Development Commands

### Docker Compose Workflow
```bash
# Start all services
docker-compose up -d

# View all service logs
docker-compose logs -f

# View specific service logs (Vietnamese cultural intelligence)
docker-compose logs -f veri-cultural-intelligence

# Restart single service after code change
docker-compose restart veri-auth-service

# Rebuild after Dockerfile change
docker-compose up -d --build veri-auth-service

# Check service health
docker-compose ps

# Stop all services
docker-compose down

# Stop and remove data (WARNING)
docker-compose down -v
```

### Testing Individual Services
```bash
# Test auth service health
curl http://localhost:8001/health

# Test Vietnamese cultural context API
curl http://localhost:8002/api/v1/cultural/context?region=south

# Test company registry
curl http://localhost:8003/api/v1/companies/search?region=south

# Test ML classification
curl -X POST http://localhost:8006/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"Vietnamese text here","model_type":"pdpl_principles"}'
```

### Database Access
```bash
# PostgreSQL
docker exec -it veri-postgres psql -U veriuser -d verisyntra

# MongoDB
docker exec -it veri-mongodb mongosh -u veriuser -p veripass_dev

# Redis
docker exec -it veri-redis redis-cli -a veripass_dev
```

---

## Service Communication Patterns

### Synchronous (REST)
```python
# Service-to-service HTTP call
import httpx

async def get_cultural_context(region: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://veri-cultural-intelligence:8002/api/v1/cultural/context",
            params={"region": region}
        )
        return response.json()
```

### Asynchronous (Message Queue)
```python
# Publish event to RabbitMQ
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('veri-rabbitmq')
)
channel = connection.channel()
channel.queue_declare(queue='veri-compliance-events')

message = {
    "event": "data_mapping_created",
    "tenant_id": "123",
    "timestamp": "2025-11-01T10:00:00+07:00"
}

channel.basic_publish(
    exchange='',
    routing_key='veri-compliance-events',
    body=json.dumps(message)
)
```

---

## Troubleshooting Guide

### Service Won't Start
```bash
# Check logs
docker-compose logs veri-auth-service

# Check if dependent services are healthy
docker-compose ps

# Verify environment variables
docker-compose config

# Rebuild container
docker-compose up -d --build veri-auth-service
```

### Database Connection Issues
```bash
# Check if PostgreSQL is healthy
docker exec veri-postgres pg_isready -U veriuser

# Verify connection string
docker exec veri-auth-service env | grep DATABASE_URL

# Test manual connection
docker exec -it veri-auth-service python -c "
import asyncpg
import asyncio
async def test():
    conn = await asyncpg.connect('postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra')
    print('Connected!')
    await conn.close()
asyncio.run(test())
"
```

### Network Issues Between Services
```bash
# List Docker networks
docker network ls

# Inspect VeriSyntra network
docker network inspect verisyntra-network

# Test connectivity from one service to another
docker exec veri-auth-service curl http://veri-cultural-intelligence:8002/health
```

### ML Model Loading Slow
```bash
# Pre-download models during build
# Add to Dockerfile:
RUN python -c "from transformers import AutoTokenizer; \
    AutoTokenizer.from_pretrained('vinai/phobert-base')"

# Use model cache volume
volumes:
  - ml-models:/app/models
```

---

## Vietnamese PDPL Compliance Checklist

### Data Residency
- [ ] All PostgreSQL data in Vietnamese data centers
- [ ] Vietnamese timezone (`Asia/Ho_Chi_Minh`) configured
- [ ] No cross-border data transfer without approval
- [ ] Multi-region deployment (North/Central/South Vietnam)

### Service-Level Compliance
- [ ] veri-auth-service: Vietnamese business authentication
- [ ] veri-cultural-intelligence: Regional context (North/Central/South)
- [ ] veri-vi-ai-classification: Vietnamese NLP models and pattern libraries for PDPL compliance
- [ ] veri-document-generator: Vietnamese legal templates
- [ ] veri-ai-data-inventory: PDPL-compliant data discovery and scanning

---

## Monitoring Dashboards

### Prometheus Metrics (port 9090)
```
http://localhost:9090

# Example queries:
- verisyntra_requests_total
- verisyntra_response_time_seconds
- verisyntra_ml_inference_duration
- verisyntra_cultural_context_cache_hits
```

### Grafana Dashboards (port 3000)
```
http://localhost:3000
User: admin
Password: admin

# Vietnamese Business Dashboards:
- VeriSyntra Overview (all services health)
- PDPL Compliance Metrics
- Vietnamese Regional Performance (North/Central/South)
- ML Model Performance
```

### RabbitMQ Management (port 15672)
```
http://localhost:15672
User: veriuser
Password: veripass_dev

# Monitor Vietnamese business event queues
```

---

## Code Migration Patterns

### Before (Monolith)
```python
# backend/main_prototype.py
from app.core.vietnamese_cultural_intelligence import VietnameseCulturalIntelligence

cultural_ai = VietnameseCulturalIntelligence()

@app.get("/api/v1/cultural/context")
async def get_context(region: str):
    return cultural_ai.get_regional_context(region)
```

### After (Microservice)
```python
# services/veri-cultural-intelligence/main.py
from fastapi import FastAPI

app = FastAPI(title="Vietnamese Cultural Intelligence Service")

@app.get("/api/v1/cultural/context")
async def get_context(region: str):
    # Same logic, but in isolated service
    return cultural_ai.get_regional_context(region)

# Other services call via HTTP:
# GET http://veri-cultural-intelligence:8002/api/v1/cultural/context?region=south
```

---

## Security Best Practices

### JWT Token Flow
```
1. Client -> POST /api/v1/auth/login (veri-auth-service)
2. veri-auth-service -> Returns JWT with tenant_id + role
3. Client -> GET /api/v1/compliance/... (with Bearer token)
4. veri-api-gateway -> Validates JWT
5. Gateway -> Forwards to veri-compliance-engine with tenant context
```

### Service-to-Service Auth
```python
# Internal service call with service token
headers = {
    "Authorization": f"Bearer {SERVICE_TOKEN}",
    "X-Service-Name": "veri-compliance-engine",
    "X-Tenant-Id": tenant_id
}

response = await httpx.get(
    "http://veri-cultural-intelligence:8002/api/v1/cultural/context",
    headers=headers
)
```

---

## Next Phase Actions

### Week 1-2: Setup
- [ ] Clone VeriSyntra repository
- [ ] Install Docker Desktop
- [ ] Create `.env.development` file
- [ ] Run `docker-compose up -d`
- [ ] Verify all infrastructure services healthy

### Week 3-4: First Service
- [ ] Create `services/veri-auth-service/` directory
- [ ] Extract auth logic from `main_prototype.py`
- [ ] Write Dockerfile for auth service
- [ ] Test JWT authentication via gateway
- [ ] Document API endpoints

### Week 5+: Continue Migration
- Follow Phase 2-8 roadmap in `00_Migration_Overview.md`
- Extract services one at a time
- Maintain backward compatibility with monolith
- Gradually switch traffic to microservices

---

## Useful Links

- **Migration Overview:** `00_Migration_Overview.md`
- **Service Specs:** `01_Service_Specifications.md`
- **Docker Guide:** `02_Docker_Implementation_Guide.md`
- **Database Strategy:** `03_Database_Migration_Strategy.md` (TBD)
- **API Gateway:** `04_API_Gateway_Design.md` (TBD)
- **Kubernetes:** `05_Kubernetes_Deployment_Guide.md` (TBD)

---

**Quick Help:**
- Stuck? Check `docker-compose logs -f`
- Service not responding? Check `docker-compose ps`
- Database issues? Check `docker exec -it veri-postgres psql -U veriuser`
- Need to reset? `docker-compose down -v && docker-compose up -d`

**Vietnamese Support:** All error messages and logs support Vietnamese (vi) and English (en)
