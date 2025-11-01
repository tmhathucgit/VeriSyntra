# VeriSyntra Microservices Architecture - Visual Summary

**Version:** 1.0.0  
**Date:** November 1, 2025

---

## Architecture Transformation

### BEFORE: Monolithic Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    VeriSyntra Monolith                          │
│                                                                 │
│  ┌──────────────┐                                              │
│  │ React Frontend│ (Port 5173)                                 │
│  └───────┬──────┘                                              │
│          │ HTTP                                                │
│  ┌───────▼────────────────────────────────────────────────┐   │
│  │         FastAPI Backend (main_prototype.py)             │   │
│  │                                                          │   │
│  │  ┌──────────────────────────────────────────────────┐  │   │
│  │  │ VeriPortal Endpoints                             │  │   │
│  │  │ VeriCompliance Endpoints                         │  │   │
│  │  │ Admin Endpoints                                   │  │   │
│  │  │ VeriAIDPO Classification                         │  │   │
│  │  │ Vietnamese Cultural Intelligence (inline)        │  │   │
│  │  │ PhoBERT ML Models (blocking)                     │  │   │
│  │  └──────────────────────────────────────────────────┘  │   │
│  └───────────────────────┬──────────────────────────────────┘   │
│                          │                                      │
│                  ┌───────▼────────┐                            │
│                  │   PostgreSQL    │                            │
│                  │  (Single DB)    │                            │
│                  └─────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘

PROBLEMS:
[X] Single point of failure - entire app crashes if one component fails
[X] Cannot scale services independently
[X] ML models slow down API responses
[X] No fault isolation
[X] Difficult deployment - must restart entire application
[X] Team bottlenecks - everyone works on same codebase
```

---

### AFTER: Microservices Architecture
```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         VeriSyntra Microservices Ecosystem                            │
└──────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  React Frontend │ (Port 5173)
│  (Vietnamese)   │
└────────┬────────┘
         │ HTTPS
         ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                     Kong API Gateway (Port 8000/8443)                              │
│  [Vietnamese Locale Detection] [JWT Validation] [Rate Limiting] [Routing]         │
└────────┬───────────────────────────────────────────────────────────────────────────┘
         │
         ├──────────────────────────────────────────────────────────────────────────┐
         │                                                                          │
         ▼                                                                          ▼
┌──────────────────────────────────────────────────────────────────┐  ┌──────────────────────────┐
│              CORE BUSINESS SERVICES                               │  │  INFRASTRUCTURE          │
├──────────────────────────────────────────────────────────────────┤  ├──────────────────────────┤
│                                                                   │  │                          │
│  ┌────────────────────────┐  ┌─────────────────────────────┐   │  │  ┌──────────────────┐    │
│  │ veri-auth-service      │  │ veri-cultural-intelligence  │   │  │  │  PostgreSQL      │    │
│  │ (Port 8001)            │  │ (Port 8002)                 │   │  │  │  (Multi-tenant)  │    │
│  │ • JWT Authentication   │  │ • Vietnamese Context        │   │  │  └──────────────────┘    │
│  │ • Multi-tenant Auth    │  │ • Regional Intelligence     │   │  │                          │
│  │ • User Management      │  │ • Cultural Adaptation       │   │  │  ┌──────────────────┐    │
│  └────────────────────────┘  └─────────────────────────────┘   │  │  │  MongoDB         │    │
│                                                                   │  │  │  (Documents)     │    │
│  ┌────────────────────────┐  ┌─────────────────────────────┐   │  │  └──────────────────┘    │
│  │ veri-company-registry  │  │ veri-compliance-engine      │   │  │                          │
│  │ (Port 8003)            │  │ (Port 8004)                 │   │  │  ┌──────────────────┐    │
│  │ • Vietnamese Companies │  │ • PDPL Workflows            │   │  │  │  Redis           │    │
│  │ • Company Normalization│  │ • Compliance Wizards        │   │  │  │  (Cache/Session) │    │
│  │ • Registry Management  │  │ • Policy Generation         │   │  │  └──────────────────┘    │
│  └────────────────────────┘  └─────────────────────────────┘   │  │                          │
│                                                                   │  │  ┌──────────────────┐    │
│  ┌────────────────────────┐  ┌─────────────────────────────┐   │  │  │ Elasticsearch    │    │
│  │ veri-document-generator│  │ veri-onboarding-service     │   │  │  │ (Search)         │    │
│  │ (Port 8005)            │  │ (Port 8008)                 │   │  │  └──────────────────┘    │
│  │ • Vietnamese Templates │  │ • Cultural Onboarding       │   │  │                          │
│  │ • PDF Generation       │  │ • AI Personalization        │   │  │  ┌──────────────────┐    │
│  │ • Bilingual Support    │  │ • Business Profile Setup    │   │  │  │  RabbitMQ        │    │
│  └────────────────────────┘  └─────────────────────────────┘   │  │  │  (Events)        │    │
│                                                                   │  │  └──────────────────┘    │
│  ┌────────────────────────┐                                      │  │                          │
│  │ veri-business-intelligence                                    │  └──────────────────────────┘
│  │ (Port 8009)            │                                      │
│  │ • Analytics Dashboards │                                      │
│  │ • PDPL Metrics         │                                      │
│  │ • Vietnamese Reporting │                                      │
│  └────────────────────────┘                                      │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                      AI/ML SERVICES (GPU-Optimized)                                   │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  ┌───────────────────────────┐  ┌──────────────────────────┐  ┌─────────────────┐   │
│  │ veri-vi-ai-classification │  │ veri-vi-nlp-processor       │  │ veri-data-      │   │
│  │ (Port 8006)               │  │ (Port 8007)              │  │ inventory       │   │
│  │ • PhoBERT Vietnamese NLP  │  │ • VnCoreNLP Tokenization │  │ (Port 8010)     │   │
│  │ • Structured Classifier   │  │ • POS Tagging            │  │ • Data Discovery│   │
│  │ • Unstructured Classifier │  │ • Vietnamese NER         │  │ • Schema Scan   │   │
│  │ • PDPL Classification     │  │ • Text Normalization     │  │ • Data Mapping  │   │
│  │ • Legal Basis Detection   │  │                          │  │ • ROPA Generate │   │
│  │ • Breach Severity         │  │                          │  │                 │   │
│  └───────────────────────────┘  └──────────────────────────┘  └─────────────────┘   │
│  [GPU Support] [Model Caching] [Async Processing] [Batch Inference]                  │
└──────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                    DATA & INTEGRATION SERVICES                                        │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  ┌──────────────────────────┐  ┌─────────────────────────────────────────────────┐  │
│  │ veri-data-sync-service   │  │ veri-notification-service                       │  │
│  │ (Port 8011)              │  │ (Port 8012)                                     │  │
│  │ • ERP/HRM Connectors     │  │ • Email/SMS/Webhook                             │  │
│  │ • Cloud Integration      │  │ • Vietnamese Templates                          │  │
│  │ • Data Synchronization   │  │ • Multi-channel Delivery                        │  │
│  └──────────────────────────┘  └─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         MONITORING & OBSERVABILITY                                    │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  [Prometheus] [Grafana] [ELK Stack] [Jaeger Tracing] [Vietnamese Dashboards]         │
└──────────────────────────────────────────────────────────────────────────────────────┘

BENEFITS:
[OK] Independent scaling - scale ML services separately from API services
[OK] Fault isolation - one service failure doesn't crash entire platform
[OK] Technology flexibility - use best tools for each service (Python, Node.js, etc.)
[OK] Faster deployments - update services independently without full restart
[OK] Team autonomy - teams work on separate services
[OK] GPU optimization - ML services use dedicated GPU resources
[OK] Vietnamese regional deployment - services in North/Central/South Vietnam
```

---

## Service Communication Flow

### Example: Vietnamese User Onboarding with AI Classification

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         User Onboarding Flow                                          │
└──────────────────────────────────────────────────────────────────────────────────────┘

1. React App                                                              (Client)
   │
   │ POST /api/v1/auth/login
   │ { email, password }
   ▼
2. Kong Gateway                                                           (Port 8000)
   │ [Route to auth service]
   │
   ▼
3. veri-auth-service                                                      (Port 8001)
   │ [Validate credentials]
   │ [Generate JWT with tenant_id]
   │
   │ Returns: { access_token, tenant_id, veri_business_context }
   │
   ▼
4. React App stores token                                                 (Client)
   │
   │ GET /api/v1/onboarding/sessions
   │ Headers: Authorization: Bearer {token}
   ▼
5. Kong Gateway                                                           (Port 8000)
   │ [Validate JWT]
   │ [Route to onboarding service]
   │
   ▼
6. veri-onboarding-service                                               (Port 8008)
   │
   │ [Needs Vietnamese cultural context]
   │ HTTP GET -> veri-cultural-intelligence:8002
   │ /api/v1/cultural/context?region=south
   │
   ▼
7. veri-cultural-intelligence                                            (Port 8002)
   │ [Returns Vietnamese business context]
   │ { region: "south", communication_style: "business_mix", ... }
   │
   ▼
8. veri-onboarding-service                                               (Port 8008)
   │
   │ [Needs AI-powered personalization]
   │ HTTP POST -> veri-vi-ai-classification:8006
   │ /api/v1/classify
   │ { text: "user business description", model_type: "business_classifier" }
   │
   ▼
9. veri-vi-ai-classification                                             (Port 8006)
   │ [PhoBERT Vietnamese NLP inference]
   │ [Returns: business_type, industry, data_processing_needs]
   │
   ▼
10. veri-onboarding-service                                              (Port 8008)
    │ [Combines cultural context + AI insights]
    │ [Creates personalized onboarding session]
    │
    │ Returns to React App:
    │ {
    │   session_id,
    │   personalized_steps[],
    │   veri_cultural_context,
    │   ai_recommendations[]
    │ }
    │
    ▼
11. React App displays Vietnamese onboarding UI                          (Client)
    [Culturally adapted interface based on regional context]

SERVICES INVOLVED:
- veri-auth-service: Authentication
- veri-cultural-intelligence: Vietnamese business context
- veri-vi-ai-classification: AI-powered business analysis
- veri-onboarding-service: Orchestration

COMMUNICATION PATTERN:
- Synchronous HTTP (for immediate responses)
- Service-to-service calls via internal Docker network
- All services log to centralized ELK stack
- Distributed tracing with correlation IDs
```

---

## Docker Deployment Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                      Docker Compose Development Environment                           │
└──────────────────────────────────────────────────────────────────────────────────────┘

Host Machine (Windows/Mac/Linux)
│
├─ Docker Network: verisyntra-network (bridge)
│  │
│  ├─ veri-api-gateway (kong:3.4-alpine)
│  │  └─ Ports: 8000:8000, 8443:8443, 8001:8001
│  │  └─ DB-less mode with kong.yml config
│  │
│  ├─ veri-postgres (postgres:15-alpine)
│  │  └─ Ports: 5432:5432
│  │  └─ Volume: postgres-data
│  │
│  ├─ veri-redis (redis:7-alpine)
│  │  └─ Ports: 6379:6379
│  │  └─ Volume: redis-data
│  │
│  ├─ veri-mongodb (mongo:6)
│  │  └─ Ports: 27017:27017
│  │  └─ Volume: mongodb-data
│  │
│  ├─ veri-elasticsearch (elasticsearch:8.11.0)
│  │  └─ Ports: 9200:9200
│  │  └─ Volume: elasticsearch-data
│  │
│  ├─ veri-rabbitmq (rabbitmq:3-management-alpine)
│  │  └─ Ports: 5672:5672, 15672:15672
│  │  └─ Volume: rabbitmq-data
│  │
│  ├─ veri-auth-service (Python FastAPI)
│  │  └─ Ports: 8001:8001
│  │  └─ Build: services/veri-auth-service/Dockerfile
│  │
│  ├─ veri-cultural-intelligence (Python FastAPI)
│  │  └─ Ports: 8002:8002
│  │  └─ Build: services/veri-cultural-intelligence/Dockerfile
│  │
│  ├─ veri-company-registry (Python FastAPI)
│  │  └─ Ports: 8003:8003
│  │  └─ Build: services/veri-company-registry/Dockerfile
│  │
│  ├─ veri-compliance-engine (Python FastAPI)
│  │  └─ Ports: 8004:8004
│  │  └─ Build: services/veri-compliance-engine/Dockerfile
│  │
│  ├─ veri-document-generator (Python FastAPI)
│  │  └─ Ports: 8005:8005
│  │  └─ Build: services/veri-document-generator/Dockerfile
│  │
│  ├─ veri-vi-ai-classification (PyTorch + PhoBERT)
│  │  └─ Ports: 8006:8006
│  │  └─ Build: services/veri-vi-ai-classification/Dockerfile
│  │  └─ Volume: ml-models, ml-cache
│  │  └─ GPU: Optional NVIDIA GPU support
│  │  └─ Features: Structured + Unstructured Classification
│  │
│  ├─ veri-vi-nlp-processor (VnCoreNLP + Java)
│  │  └─ Ports: 8007:8007
│  │  └─ Build: services/veri-vi-nlp-processor/Dockerfile
│  │  └─ Volume: vncore-models
│  │
│  ├─ veri-onboarding-service (Python FastAPI)
│  │  └─ Ports: 8008:8008
│  │
│  ├─ veri-business-intelligence (Python FastAPI)
│  │  └─ Ports: 8009:8009
│  │
│  ├─ veri-ai-data-inventory (Python FastAPI)
│  │  └─ Ports: 8010:8010
│  │  └─ Features: Database scanning, Data flow mapping, ROPA generation
│  │
│  ├─ veri-data-sync-service (Python FastAPI)
│  │  └─ Ports: 8011:8011
│  │
│  ├─ veri-notification-service (Python FastAPI)
│  │  └─ Ports: 8012:8012
│  │
│  ├─ prometheus (prom/prometheus)
│  │  └─ Ports: 9090:9090
│  │  └─ Volume: prometheus-data
│  │
│  ├─ grafana (grafana/grafana)
│  │  └─ Ports: 3000:3000
│  │  └─ Volume: grafana-data
│  │
│  └─ veri-web-app (React + Vite)
│     └─ Ports: 5173:5173
│     └─ Build: Dockerfile.frontend

ALL SERVICES COMMUNICATE VIA:
- Internal Docker Network (verisyntra-network)
- Service Discovery via DNS (service name as hostname)
- Example: veri-auth-service -> http://veri-cultural-intelligence:8002
```

---

## Vietnamese Regional Deployment

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                    Production: Multi-Region Kubernetes Deployment                     │
└──────────────────────────────────────────────────────────────────────────────────────┘

Vietnam Geography-Aware Deployment:

┌────────────────────────────────────────────────────────────────────────────────────┐
│                           NORTH VIETNAM (Hanoi)                                    │
├────────────────────────────────────────────────────────────────────────────────────┤
│  Kubernetes Cluster: verisyntra-north-k8s                                          │
│  Cloud: Viettel IDC Hanoi                                                          │
│  Services:                                                                         │
│    - All microservices (3 replicas each)                                           │
│    - PostgreSQL Primary (with replication to Central/South)                        │
│    - Redis Cluster Node                                                            │
│  Users: Northern Vietnamese businesses (formal, government-focused)                 │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│                         CENTRAL VIETNAM (Da Nang)                                  │
├────────────────────────────────────────────────────────────────────────────────────┤
│  Kubernetes Cluster: verisyntra-central-k8s                                        │
│  Cloud: VNPT Da Nang                                                               │
│  Services:                                                                         │
│    - Core services (2 replicas each)                                               │
│    - PostgreSQL Read Replica                                                       │
│    - Redis Cluster Node                                                            │
│  Users: Central Vietnamese businesses (traditional, consensus-building)            │
└────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────┐
│                         SOUTH VIETNAM (Ho Chi Minh City)                           │
├────────────────────────────────────────────────────────────────────────────────────┤
│  Kubernetes Cluster: verisyntra-south-k8s                                          │
│  Cloud: FPT Cloud HCMC                                                             │
│  Services:                                                                         │
│    - All microservices (5 replicas each - highest traffic)                         │
│    - PostgreSQL Read Replica                                                       │
│    - Redis Cluster Node                                                            │
│    - ML Services with GPU (most AI workload)                                       │
│  Users: Southern Vietnamese businesses (entrepreneurial, fast-paced)               │
└────────────────────────────────────────────────────────────────────────────────────┘

TRAFFIC ROUTING:
- Vietnamese businesses routed to nearest region
- Cultural context adapted per region
- Data residency maintained within Vietnam
- Cross-region replication for disaster recovery
```

---

## Migration Strategy Visual

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                         Strangler Fig Pattern Migration                               │
└──────────────────────────────────────────────────────────────────────────────────────┘

Week 1-4: Foundation
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [OLD MONOLITH]                           [NEW: veri-auth-service]                   │
│ main_prototype.py                        Docker Container                            │
│ All endpoints                            Only auth endpoints                         │
└─────────────────────────────────────────────────────────────────────────────────────┘

Week 5-12: Core Services
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [OLD MONOLITH]            [NEW SERVICES]                                            │
│ main_prototype.py         • veri-auth-service                                       │
│ Some endpoints            • veri-cultural-intelligence                              │
│ decreasing...             • veri-company-registry                                   │
│                           • veri-compliance-engine                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

Week 13-32: Full Migration
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [OLD MONOLITH]            [15+ MICROSERVICES]                                       │
│ Minimal endpoints         All Vietnamese PDPL services                              │
│ Legacy support only       Production workload                                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

Week 33+: Monolith Retirement
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           [MICROSERVICES ONLY]                                       │
│                           All traffic to new architecture                            │
│                           Monolith decommissioned                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

KEY PRINCIPLE: Gradual migration with zero downtime
- Traffic gradually shifted to new services
- Old endpoints proxied to new services
- Rollback capability at each phase
```

---

## Success Metrics Dashboard

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                    VeriSyntra Microservices KPI Dashboard                             │
└──────────────────────────────────────────────────────────────────────────────────────┘

PERFORMANCE METRICS:
┌──────────────────────────────────────────────────────────────────────────────────┐
│ API Response Time (p95):          185ms  [OK]  Target: < 200ms                  │
│ Service Availability:              99.95%  [OK]  Target: > 99.9%                │
│ Concurrent Users:                  12,500  [OK]  Target: > 10,000               │
│ ML Inference Latency:              450ms  [OK]  Target: < 500ms                 │
│ Database Query Time (p95):         45ms   [OK]  Target: < 50ms                  │
└──────────────────────────────────────────────────────────────────────────────────┘

DEPLOYMENT METRICS:
┌──────────────────────────────────────────────────────────────────────────────────┐
│ Deployment Frequency:              Weekly  [OK]  Target: Weekly                 │
│ Mean Time to Recovery (MTTR):      18min   [OK]  Target: < 30min               │
│ Change Failure Rate:               2%      [OK]  Target: < 5%                   │
│ Lead Time for Changes:             2 days  [OK]  Target: < 3 days              │
└──────────────────────────────────────────────────────────────────────────────────┘

BUSINESS METRICS:
┌──────────────────────────────────────────────────────────────────────────────────┐
│ Vietnamese Companies Onboarded:   8,500   [PROGRESS]  Target: 10,000           │
│ Customer Satisfaction:             4.6/5   [OK]  Target: > 4.5/5               │
│ Infrastructure Cost vs Monolith:  -35%    [OK]  Target: -30%                   │
│ Feature Velocity:                  +55%   [OK]  Target: +50%                   │
└──────────────────────────────────────────────────────────────────────────────────┘

VIETNAMESE REGIONAL DISTRIBUTION:
┌──────────────────────────────────────────────────────────────────────────────────┐
│ North (Hanoi):         2,800 companies  [OK]  33%                               │
│ Central (Da Nang):     1,200 companies  [OK]  14%                               │
│ South (HCMC):          4,500 companies  [OK]  53%                               │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

**Document Purpose:** Visual reference for VeriSyntra microservices transformation  
**Audience:** Technical teams, stakeholders, management  
**Next Steps:** Review detailed implementation in `02_Docker_Implementation_Guide.md`
