# VeriSyntra Docker Implementation Guide

**Document Version:** 1.0.0  
**Date:** November 1, 2025  
**Purpose:** Practical Docker configuration for VeriSyntra microservices

---

## Docker Strategy

### Development Environment
- **Tool:** Docker Compose
- **Purpose:** Local development and testing
- **Services:** All microservices + databases + infrastructure

### Production Environment
- **Tool:** Kubernetes with Helm
- **Purpose:** Scalable production deployment
- **Location:** Vietnamese cloud providers (Viettel IDC, VNPT, FPT Cloud)

---

## Base Docker Images

### Python Services Base Image

**File:** `docker/base/python-fastapi.Dockerfile`
```dockerfile
FROM python:3.11-slim

# Set Vietnamese timezone
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security
RUN useradd -m -u 1000 veriuser

# Set working directory
WORKDIR /app

# Install common Python dependencies
COPY requirements-base.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-base.txt

# Switch to non-root user
USER veriuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File:** `docker/base/requirements-base.txt`
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pytz==2023.3
loguru==0.7.2
aiohttp==3.9.1
httpx==0.25.2
```

---

### ML Services Base Image

**File:** `docker/base/python-ml.Dockerfile`
```dockerfile
# Use NVIDIA CUDA base for GPU support (production)
# Use CPU version for development
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Alternative for CPU-only development:
# FROM python:3.11-slim

# Set Vietnamese timezone
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install ML dependencies
COPY requirements-ml.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-ml.txt

# Pre-download PhoBERT model (optional, speeds up startup)
# RUN python -c "from transformers import AutoTokenizer, AutoModel; \
#     AutoTokenizer.from_pretrained('vinai/phobert-base'); \
#     AutoModel.from_pretrained('vinai/phobert-base')"

USER veriuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8006}/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006"]
```

**File:** `docker/base/requirements-ml.txt`
```
torch==2.0.1
transformers==4.35.2
sentencepiece==0.1.99
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
numpy==1.24.3
```

---

## Docker Compose - Complete Development Environment

**File:** `docker-compose.yml`
```yaml
version: '3.9'

# Vietnamese VeriSyntra Microservices Development Environment
# All services with Vietnamese PDPL 2025 compliance support

services:
  # =====================================
  # Infrastructure Services
  # =====================================
  
  # Kong API Gateway (DB-less mode for development)
  veri-api-gateway:
    image: kong:3.4-alpine
    container_name: veri-api-gateway
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /kong/kong.yml
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8000:8000"  # Proxy port
      - "8443:8443"  # Proxy SSL port
      - "8001:8001"  # Admin API
    volumes:
      - ./kong/kong.yml:/kong/kong.yml:ro
    depends_on:
      - veri-auth-service
      - veri-cultural-intelligence
      - veri-compliance-engine
    networks:
      - veri-network
    restart: unless-stopped

  # PostgreSQL - Primary Database
  veri-postgres:
    image: postgres:15-alpine
    container_name: veri-postgres
    environment:
      POSTGRES_USER: veriuser
      POSTGRES_PASSWORD: veripass_dev
      POSTGRES_DB: verisyntra
      TZ: Asia/Ho_Chi_Minh
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    networks:
      - veri-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U veriuser -d verisyntra"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis - Cache & Session Store
  veri-redis:
    image: redis:7-alpine
    container_name: veri-redis
    command: redis-server --requirepass veripass_dev --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - veri-network
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "veripass_dev", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  # MongoDB - Document Store (Vietnamese Templates)
  veri-mongodb:
    image: mongo:6
    container_name: veri-mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: veriuser
      MONGO_INITDB_ROOT_PASSWORD: veripass_dev
      MONGO_INITDB_DATABASE: veri_documents
      TZ: Asia/Ho_Chi_Minh
    volumes:
      - mongodb-data:/data/db
    ports:
      - "27017:27017"
    networks:
      - veri-network
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Elasticsearch - Vietnamese Full-Text Search
  veri-elasticsearch:
    image: elasticsearch:8.11.0
    container_name: veri-elasticsearch
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
      - xpack.security.enabled=false
      - TZ=Asia/Ho_Chi_Minh
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - veri-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  # RabbitMQ - Message Broker
  veri-rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: veri-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: veriuser
      RABBITMQ_DEFAULT_PASS: veripass_dev
      TZ: Asia/Ho_Chi_Minh
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    networks:
      - veri-network
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  # =====================================
  # Authentication & Security Services
  # =====================================
  
  veri-auth-service:
    build:
      context: ./services/veri-auth-service
      dockerfile: Dockerfile
    container_name: veri-auth-service
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/0
      - JWT_SECRET_KEY=${JWT_SECRET_KEY:-dev-secret-change-in-production}
      - JWT_ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
      - REFRESH_TOKEN_EXPIRE_DAYS=7
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8001
    ports:
      - "8001:8001"
    depends_on:
      veri-postgres:
        condition: service_healthy
      veri-redis:
        condition: service_healthy
    networks:
      - veri-network
    volumes:
      - ./services/veri-auth-service:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =====================================
  # Core Business Services
  # =====================================
  
  veri-cultural-intelligence:
    build:
      context: ./services/veri-cultural-intelligence
      dockerfile: Dockerfile
    container_name: veri-cultural-intelligence
    environment:
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/1
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8002
    ports:
      - "8002:8002"
    depends_on:
      - veri-redis
    networks:
      - veri-network
    volumes:
      - ./services/veri-cultural-intelligence:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  veri-company-registry:
    build:
      context: ./services/veri-company-registry
      dockerfile: Dockerfile
    container_name: veri-company-registry
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/2
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8003
    ports:
      - "8003:8003"
    depends_on:
      veri-postgres:
        condition: service_healthy
      veri-redis:
        condition: service_healthy
    networks:
      - veri-network
    volumes:
      - ./services/veri-company-registry:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  veri-compliance-engine:
    build:
      context: ./services/veri-compliance-engine
      dockerfile: Dockerfile
    container_name: veri-compliance-engine
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/3
      - RABBITMQ_URL=amqp://veriuser:veripass_dev@veri-rabbitmq:5672/
      - CULTURAL_INTELLIGENCE_URL=http://veri-cultural-intelligence:8002
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8004
    ports:
      - "8004:8004"
    depends_on:
      - veri-postgres
      - veri-redis
      - veri-rabbitmq
      - veri-cultural-intelligence
    networks:
      - veri-network
    volumes:
      - ./services/veri-compliance-engine:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8004/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  veri-document-generator:
    build:
      context: ./services/veri-document-generator
      dockerfile: Dockerfile
    container_name: veri-document-generator
    environment:
      - MONGODB_URL=mongodb://veriuser:veripass_dev@veri-mongodb:27017/veri_documents?authSource=admin
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8005
      - TEMPLATE_STORAGE_PATH=/app/templates
    ports:
      - "8005:8005"
    depends_on:
      - veri-mongodb
    networks:
      - veri-network
    volumes:
      - ./services/veri-document-generator:/app
      - document-templates:/app/templates
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8005/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  veri-onboarding-service:
    build:
      context: ./services/veri-onboarding-service
      dockerfile: Dockerfile
    container_name: veri-onboarding-service
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/4
      - CULTURAL_INTELLIGENCE_URL=http://veri-cultural-intelligence:8002
      - AIDPO_CLASSIFICATION_URL=http://veri-vi-ai-classification:8006
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8008
    ports:
      - "8008:8008"
    depends_on:
      - veri-postgres
      - veri-cultural-intelligence
    networks:
      - veri-network
    volumes:
      - ./services/veri-onboarding-service:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8008/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  veri-business-intelligence:
    build:
      context: ./services/veri-business-intelligence
      dockerfile: Dockerfile
    container_name: veri-business-intelligence
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/5
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8009
    ports:
      - "8009:8009"
    depends_on:
      - veri-postgres
      - veri-redis
    networks:
      - veri-network
    volumes:
      - ./services/veri-business-intelligence:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8009/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =====================================
  # AI/ML Services
  # =====================================
  
  veri-vi-ai-classification:
    build:
      context: ./services/veri-vi-ai-classification
      dockerfile: Dockerfile
    container_name: veri-vi-ai-classification
    environment:
      - MODEL_PATH=/app/models
      - CACHE_DIR=/app/cache
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/6
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8006
      - CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}  # GPU support if available
    ports:
      - "8006:8006"
    depends_on:
      - veri-redis
    networks:
      - veri-network
    volumes:
      - ./services/veri-vi-ai-classification:/app
      - ml-models:/app/models
      - ml-cache:/app/cache
    # Uncomment for GPU support:
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8006/health"]
      interval: 30s
      timeout: 30s
      retries: 3
      start_period: 120s

  veri-vi-nlp-processor:
    build:
      context: ./services/veri-vi-nlp-processor
      dockerfile: Dockerfile
    container_name: veri-vi-nlp-processor
    environment:
      - VNCORENLP_PATH=/app/VnCoreNLP
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/7
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8007
    ports:
      - "8007:8007"
    depends_on:
      - veri-redis
    networks:
      - veri-network
    volumes:
      - ./services/veri-vi-nlp-processor:/app
      - vncore-models:/app/VnCoreNLP
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8007/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  veri-ai-data-inventory:
    build:
      context: ./services/veri-ai-data-inventory
      dockerfile: Dockerfile
    container_name: veri-ai-data-inventory
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - RABBITMQ_URL=amqp://veriuser:veripass_dev@veri-rabbitmq:5672/
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/8
      - AIDPO_CLASSIFICATION_URL=http://veri-vi-ai-classification:8006
      - NLP_PROCESSOR_URL=http://veri-vi-nlp-processor:8007
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8010
    ports:
      - "8010:8010"
    depends_on:
      - veri-postgres
      - veri-rabbitmq
      - veri-vi-ai-classification
      - veri-vi-nlp-processor
    networks:
      - veri-network
    volumes:
      - ./services/veri-ai-data-inventory:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8010/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =====================================
  # Data & Integration Services
  # =====================================
  
  veri-data-sync-service:
    build:
      context: ./services/veri-data-sync-service
      dockerfile: Dockerfile
    container_name: veri-data-sync-service
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - RABBITMQ_URL=amqp://veriuser:veripass_dev@veri-rabbitmq:5672/
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/9
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8011
    ports:
      - "8011:8011"
    depends_on:
      - veri-postgres
      - veri-rabbitmq
    networks:
      - veri-network
    volumes:
      - ./services/veri-data-sync-service:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8011/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  veri-notification-service:
    build:
      context: ./services/veri-notification-service
      dockerfile: Dockerfile
    container_name: veri-notification-service
    environment:
      - DATABASE_URL=postgresql://veriuser:veripass_dev@veri-postgres:5432/verisyntra
      - RABBITMQ_URL=amqp://veriuser:veripass_dev@veri-rabbitmq:5672/
      - REDIS_URL=redis://:veripass_dev@veri-redis:6379/10
      - SMTP_HOST=${SMTP_HOST:-smtp.gmail.com}
      - SMTP_PORT=${SMTP_PORT:-587}
      - SMTP_USER=${SMTP_USER:-}
      - SMTP_PASSWORD=${SMTP_PASSWORD:-}
      - VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
      - SERVICE_PORT=8012
    ports:
      - "8012:8012"
    depends_on:
      - veri-rabbitmq
      - veri-mongodb
    networks:
      - veri-network
    volumes:
      - ./services/veri-notification-service:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8012/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =====================================
  # Monitoring Services (Optional for Dev)
  # =====================================
  
  # Prometheus - Metrics Collection
  prometheus:
    image: prom/prometheus:latest
    container_name: veri-prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    ports:
      - "9090:9090"
    networks:
      - veri-network
    restart: unless-stopped

  # Grafana - Metrics Visualization
  grafana:
    image: grafana/grafana:latest
    container_name: veri-grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_SERVER_ROOT_URL=http://localhost:3000
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
    networks:
      - veri-network
    restart: unless-stopped

  # =====================================
  # Frontend Service
  # =====================================
  
  veri-web-app:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: veri-web-app
    environment:
      - VITE_API_GATEWAY_URL=http://localhost:80
      - VITE_VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
    ports:
      - "5173:5173"
    depends_on:
      - veri-api-gateway
    networks:
      - veri-network
    volumes:
      - ./src:/app/src
      - ./public:/app/public
    restart: unless-stopped

# =====================================
# Networks
# =====================================
networks:
  veri-network:
    driver: bridge
    name: verisyntra-network

# =====================================
# Volumes
# =====================================
volumes:
  postgres-data:
    driver: local
  mongodb-data:
    driver: local
  redis-data:
    driver: local
  elasticsearch-data:
    driver: local
  rabbitmq-data:
    driver: local
  ml-models:
    driver: local
  ml-cache:
    driver: local
  vncore-models:
    driver: local
  document-templates:
    driver: local
  prometheus-data:
    driver: local
  grafana-data:
    driver: local
```

---

## Environment Variables

**File:** `.env.development`
```bash
# VeriSyntra Development Environment Variables

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-development-key-change-in-production
JWT_ALGORITHM=HS256

# Database
POSTGRES_USER=veriuser
POSTGRES_PASSWORD=veripass_dev
POSTGRES_DB=verisyntra

# Redis
REDIS_PASSWORD=veripass_dev

# MongoDB
MONGO_INITDB_ROOT_USERNAME=veriuser
MONGO_INITDB_ROOT_PASSWORD=veripass_dev

# RabbitMQ
RABBITMQ_USER=veriuser
RABBITMQ_PASSWORD=veripass_dev

# SMTP (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# Vietnamese Configuration
VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
DEFAULT_LANGUAGE=vi
REGIONAL_SUPPORT=north,central,south

# GPU Support (optional)
# CUDA_VISIBLE_DEVICES=0
```

---

## Service-Specific Dockerfiles

### veri-auth-service

**File:** `services/veri-auth-service/Dockerfile`
```dockerfile
FROM python:3.11-slim

ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m veriuser && chown -R veriuser:veriuser /app
USER veriuser

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

**File:** `services/veri-auth-service/requirements.txt`
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.13.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
redis==5.0.1
pytz==2023.3
loguru==0.7.2
```

---

### veri-vi-ai-classification

**File:** `services/veri-vi-ai-classification/Dockerfile`
```dockerfile
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-download PhoBERT models (optional)
RUN python -c "from transformers import AutoTokenizer; \
    AutoTokenizer.from_pretrained('vinai/phobert-base')"

COPY . .

RUN useradd -m veriuser && chown -R veriuser:veriuser /app
USER veriuser

EXPOSE 8006

HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8006/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006"]
```

**File:** `services/veri-vi-ai-classification/requirements.txt`
```
torch==2.0.1
transformers==4.35.2
sentencepiece==0.1.99
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
numpy==1.24.3
redis==5.0.1
loguru==0.7.2
```

---

## Quick Start Commands

### Start All Services
```bash
# Start all Vietnamese microservices
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f veri-auth-service
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Rebuild Services
```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build veri-auth-service

# Rebuild and restart
docker-compose up -d --build
```

### Health Checks
```bash
# Check all service health
docker-compose ps

# Test API Gateway
curl http://localhost:80/health

# Test Vietnamese Cultural Intelligence
curl http://localhost:8002/health

# Test Auth Service
curl http://localhost:8001/health
```

---

## Database Initialization

**File:** `database/init/01-init-vietnamese-schema.sql`
```sql
-- VeriSyntra Vietnamese PDPL Microservices Database Schema

-- Create schemas for multi-tenancy
CREATE SCHEMA IF NOT EXISTS veri_auth;
CREATE SCHEMA IF NOT EXISTS veri_compliance;
CREATE SCHEMA IF NOT EXISTS veri_data_inventory;
CREATE SCHEMA IF NOT EXISTS veri_onboarding;

-- Set timezone to Vietnamese time
SET timezone = 'Asia/Ho_Chi_Minh';

-- Vietnamese tenants table
CREATE TABLE veri_auth.tenants (
    tenant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name VARCHAR(255) NOT NULL,
    company_name_vi VARCHAR(255),
    veri_regional_location VARCHAR(20) CHECK (veri_regional_location IN ('north', 'central', 'south')),
    veri_industry_type VARCHAR(100),
    subscription_tier VARCHAR(50) DEFAULT 'starter',
    veri_business_context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE
);

-- Vietnamese users table
CREATE TABLE veri_auth.users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES veri_auth.tenants(tenant_id),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    full_name_vi VARCHAR(255),
    phone_number VARCHAR(20),
    role VARCHAR(50) DEFAULT 'staff',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Vietnamese company registry
CREATE TABLE veri_compliance.companies (
    company_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES veri_auth.tenants(tenant_id),
    company_name VARCHAR(255) NOT NULL,
    company_name_vi VARCHAR(255),
    tax_id VARCHAR(50),
    industry VARCHAR(100),
    region VARCHAR(20),
    normalized_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for Vietnamese business queries
CREATE INDEX idx_tenants_region ON veri_auth.tenants(veri_regional_location);
CREATE INDEX idx_users_tenant ON veri_auth.users(tenant_id);
CREATE INDEX idx_users_email ON veri_auth.users(email);
CREATE INDEX idx_companies_tenant ON veri_compliance.companies(tenant_id);
CREATE INDEX idx_companies_region ON veri_compliance.companies(region);

-- Vietnamese timezone function
CREATE OR REPLACE FUNCTION vietnamese_now()
RETURNS TIMESTAMP WITH TIME ZONE AS $$
BEGIN
    RETURN NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh';
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION vietnamese_now() IS 'Returns current time in Vietnamese timezone';
```

---

## Next Steps

1. **Create Service Directories:**
   ```bash
   mkdir -p services/{veri-auth-service,veri-cultural-intelligence,veri-compliance-engine}
   ```

2. **Implement Each Service:** See service-specific implementation in `01_Service_Specifications.md`

3. **Configure Kong Gateway:** Create `kong/kong.yml` for DB-less mode (see `05_API_Gateway_Selection.md`)

4. **Run Development Environment:**
   ```bash
   docker-compose up -d
   ```

5. **Test Integration:** Run integration tests across microservices

---

**Document Status:** Draft v1.0  
**Last Updated:** November 1, 2025  
**Next:** Database Migration Strategy
