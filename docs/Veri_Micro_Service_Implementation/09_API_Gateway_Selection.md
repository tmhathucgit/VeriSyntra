# VeriSyntra API Gateway Selection Guide

**Document Version:** 1.0.0  
**Date:** November 1, 2025  
**Purpose:** Compare API Gateway options and provide selection rationale for VeriSyntra

---

## Executive Summary

The API Gateway is the **single entry point** for all client requests in VeriSyntra's microservices architecture. The choice of gateway technology significantly impacts:
- Performance and scalability
- Vietnamese language support
- Multi-tenant routing complexity
- Development team expertise
- Operational overhead
- Cost

**Recommended Approach:** Start with **Kong Gateway** for development, with **Nginx + Lua** as lightweight alternative.

---

## API Gateway Options Comparison

### 1. Kong Gateway (RECOMMENDED for VeriSyntra)

**Overview:** Open-source API Gateway built on Nginx + OpenResty (Nginx + Lua)

#### ✅ Advantages for VeriSyntra

**Vietnamese Multi-Tenancy Support:**
- Built-in tenant isolation with API key/JWT plugins
- Custom plugins for Vietnamese business context routing
- Per-tenant rate limiting (critical for Vietnamese SaaS pricing tiers)

**Developer Experience:**
- Declarative configuration (YAML/JSON)
- Extensive plugin ecosystem (150+ plugins)
- Admin API for programmatic management
- Vietnamese language header detection possible

**Production Ready:**
- Battle-tested at scale (Airbnb, NASA, Tesla use Kong)
- Built-in load balancing
- Health checks and circuit breakers
- Comprehensive monitoring (Prometheus metrics)

**Vietnamese PDPL Compliance:**
- Request/response logging for audit trails
- Data residency control (routes to Vietnamese services only)
- Custom plugins for Vietnamese data classification

**Example Configuration:**
```yaml
# kong.yml - Vietnamese Multi-Tenant Routing
_format_version: "3.0"

services:
  - name: veri-auth-service
    url: http://veri-auth-service:8001
    routes:
      - name: auth-route
        paths:
          - /api/v1/auth
        strip_path: false
    plugins:
      - name: jwt
        config:
          claims_to_verify:
            - exp
            - tenant_id
      - name: rate-limiting
        config:
          minute: 100
          policy: redis
          redis_host: veri-redis
          redis_port: 6379

  - name: veri-cultural-intelligence
    url: http://veri-cultural-intelligence:8002
    routes:
      - name: cultural-route
        paths:
          - /api/v1/cultural
    plugins:
      - name: request-transformer
        config:
          add:
            headers:
              - "X-Vietnamese-Timezone: Asia/Ho_Chi_Minh"
      - name: response-transformer
        config:
          add:
            headers:
              - "X-Content-Language: vi-VN"
```

**Custom Vietnamese Plugin Example:**
```lua
-- kong/plugins/vietnamese-context/handler.lua
local VietnameseContextHandler = {}

function VietnameseContextHandler:access(conf)
  -- Detect Vietnamese language preference
  local accept_lang = kong.request.get_header("Accept-Language")
  local viet_lang = "vi"
  
  if accept_lang and string.find(accept_lang, "vi") then
    viet_lang = "vietnamese"
  elseif accept_lang and string.find(accept_lang, "en") then
    viet_lang = "english"
  end
  
  -- Add Vietnamese business context header
  kong.service.request.set_header("X-Veri-Language", viet_lang)
  kong.service.request.set_header("X-Veri-Timezone", "Asia/Ho_Chi_Minh")
  
  -- Extract tenant from JWT and add regional routing
  local tenant_id = kong.ctx.shared.authenticated_credential.tenant_id
  if tenant_id then
    -- Query tenant database for regional location
    -- Route to appropriate regional cluster
    kong.service.request.set_header("X-Veri-Tenant-Id", tenant_id)
  end
end

return VietnameseContextHandler
```

#### ❌ Disadvantages

- **Learning Curve:** More complex than simple Nginx
- **Resource Usage:** Higher memory footprint (PostgreSQL/Cassandra for config)
- **Operational Overhead:** Requires database for configuration storage

**Resource Requirements:**
- CPU: 2-4 cores
- Memory: 2-4 GB (with PostgreSQL)
- Storage: 10 GB

**Docker Compose Example:**
```yaml
services:
  kong-database:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: kongpass
    volumes:
      - kong-db:/var/lib/postgresql/data

  kong-migrations:
    image: kong:3.4
    command: kong migrations bootstrap
    depends_on:
      - kong-database
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database

  kong:
    image: kong:3.4
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8000:8000"  # Proxy
      - "8443:8443"  # Proxy SSL
      - "8001:8001"  # Admin API
    depends_on:
      - kong-database
      - kong-migrations
```

---

### 2. Nginx + Lua (OpenResty) - Lightweight Alternative

**Overview:** Pure Nginx with Lua scripting for custom logic

#### ✅ Advantages

**Simplicity:**
- Minimal resource footprint
- Simple file-based configuration
- No external database required

**Performance:**
- Extremely fast (C-based)
- Low latency (<1ms routing overhead)
- High throughput (100k+ req/sec)

**Vietnamese Team Familiarity:**
- Most developers know basic Nginx
- Easier to debug than Kong

**Example Configuration:**
```nginx
# nginx.conf - Vietnamese Multi-Tenant Gateway

upstream veri-auth-service {
    server veri-auth-service:8001;
}

upstream veri-cultural-intelligence {
    server veri-cultural-intelligence:8002;
}

upstream veri-compliance-engine {
    server veri-compliance-engine:8004;
}

# Vietnamese language detection and routing
map $http_accept_language $veri_language {
    default "english";
    ~*vi "vietnamese";
}

# Main server block
server {
    listen 80;
    server_name verisyntra.vn;

    # Vietnamese timezone header
    add_header X-Vietnamese-Timezone "Asia/Ho_Chi_Minh" always;
    
    # Vietnamese CORS
    add_header Access-Control-Allow-Origin "http://localhost:5173" always;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-Veri-Tenant-Id" always;

    # Rate limiting by IP (basic)
    limit_req_zone $binary_remote_addr zone=veri_limit:10m rate=100r/m;
    limit_req zone=veri_limit burst=20 nodelay;

    # Authentication service
    location /api/v1/auth {
        proxy_pass http://veri-auth-service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Veri-Language $veri_language;
        
        # Vietnamese timezone
        proxy_set_header X-Veri-Timezone "Asia/Ho_Chi_Minh";
    }

    # Cultural intelligence service
    location /api/v1/cultural {
        # JWT validation with Lua
        access_by_lua_block {
            local jwt = require "resty.jwt"
            local auth_header = ngx.var.http_authorization
            
            if not auth_header then
                ngx.status = 401
                ngx.say('{"error":"Missing authorization header"}')
                ngx.exit(401)
            end
            
            local token = string.sub(auth_header, 8)  -- Remove "Bearer "
            local jwt_obj = jwt:verify("your-secret-key", token)
            
            if not jwt_obj.verified then
                ngx.status = 401
                ngx.say('{"error":"Invalid JWT"}')
                ngx.exit(401)
            end
            
            -- Add tenant ID to header
            ngx.req.set_header("X-Veri-Tenant-Id", jwt_obj.payload.tenant_id)
        }
        
        proxy_pass http://veri-cultural-intelligence;
        proxy_set_header X-Veri-Language $veri_language;
    }

    # Compliance engine
    location /api/v1/compliance {
        # Require authentication
        auth_request /auth/validate;
        
        proxy_pass http://veri-compliance-engine;
        proxy_set_header X-Veri-Language $veri_language;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "VeriSyntra Gateway Healthy\n";
        add_header Content-Type text/plain;
    }
}
```

**Lua Script for Vietnamese Context:**
```lua
-- /etc/nginx/lua/vietnamese_context.lua
local _M = {}

function _M.detect_region(tenant_id)
    -- Connect to Redis to get tenant region
    local redis = require "resty.redis"
    local red = redis:new()
    
    red:set_timeout(1000)
    local ok, err = red:connect("veri-redis", 6379)
    
    if not ok then
        return "south"  -- default to south Vietnam
    end
    
    local region, err = red:get("tenant:" .. tenant_id .. ":region")
    
    if region == ngx.null then
        return "south"
    end
    
    return region
end

function _M.add_vietnamese_headers(tenant_id)
    local region = _M.detect_region(tenant_id)
    
    ngx.req.set_header("X-Veri-Region", region)
    ngx.req.set_header("X-Veri-Timezone", "Asia/Ho_Chi_Minh")
    
    -- Cultural context based on region
    if region == "north" then
        ngx.req.set_header("X-Veri-Formality", "high")
    elseif region == "south" then
        ngx.req.set_header("X-Veri-Formality", "moderate")
    else
        ngx.req.set_header("X-Veri-Formality", "traditional")
    end
end

return _M
```

#### ❌ Disadvantages

- **Custom Code Required:** All advanced features need Lua scripting
- **No Admin UI:** Configuration via files only
- **Limited Plugin Ecosystem:** Must build everything custom
- **State Management:** Need Redis for shared state (rate limiting, etc.)

---

### 3. AWS API Gateway - Cloud-Native Option

**Overview:** Managed API Gateway from AWS

#### ✅ Advantages

- **Zero Infrastructure Management:** AWS handles scaling, HA
- **AWS Integration:** Easy Lambda, DynamoDB, Cognito integration
- **Auto-scaling:** Handles traffic spikes automatically

#### ❌ Disadvantages for VeriSyntra

**Vietnamese PDPL Compliance Issues:**
- ❌ **Data leaves Vietnam:** API Gateway logs in AWS regions outside Vietnam
- ❌ **Cross-border data transfer:** Violates Vietnamese data residency
- ❌ **No control over data location:** Cannot guarantee MPS compliance

**Vendor Lock-in:**
- Tied to AWS ecosystem
- Migration difficulty

**Cost:**
- Pay per request (can be expensive at scale)
- Vietnamese businesses prefer predictable costs

**VERDICT: NOT RECOMMENDED for VeriSyntra due to PDPL compliance**

---

### 4. Traefik - Modern Cloud-Native Gateway

**Overview:** Modern reverse proxy with Docker/Kubernetes integration

#### ✅ Advantages

- **Auto-discovery:** Automatically detects new services
- **Docker-native:** Perfect for Docker Compose
- **Dashboard UI:** Built-in monitoring
- **Let's Encrypt:** Automatic SSL certificates

**Example Configuration:**
```yaml
# docker-compose.yml with Traefik
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"  # Dashboard
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  veri-auth-service:
    build: ./services/veri-auth-service
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.auth.rule=PathPrefix(`/api/v1/auth`)"
      - "traefik.http.routers.auth.entrypoints=web"
      - "traefik.http.services.auth.loadbalancer.server.port=8001"
```

#### ❌ Disadvantages

- **Limited Advanced Features:** Fewer plugins than Kong
- **Learning Curve:** Different configuration approach
- **Less Mature:** Newer than Nginx/Kong

---

### 5. Spring Cloud Gateway - Java-Based Option

**Overview:** API Gateway for Spring Boot microservices

#### ✅ Advantages

- **Java Ecosystem:** If team knows Java/Spring
- **Reactive Programming:** Non-blocking I/O
- **Spring Integration:** Works well with Spring services

#### ❌ Disadvantages for VeriSyntra

- **Technology Mismatch:** VeriSyntra is Python-based (FastAPI)
- **Resource Heavy:** JVM overhead
- **Complexity:** Overkill for Python microservices

**VERDICT: NOT RECOMMENDED - Technology mismatch**

---

## Comparison Matrix

| Feature | Kong | Nginx + Lua | AWS API GW | Traefik | Spring Cloud GW |
|---------|------|-------------|------------|---------|-----------------|
| **Vietnamese PDPL Compliance** | ✅ Excellent | ✅ Excellent | ❌ Poor | ✅ Good | ✅ Good |
| **Multi-Tenancy** | ✅ Excellent | ⚠️ Custom | ✅ Good | ⚠️ Custom | ✅ Good |
| **Performance** | ✅ Excellent | ✅ Excellent | ✅ Good | ✅ Good | ⚠️ Moderate |
| **Ease of Setup** | ⚠️ Moderate | ✅ Easy | ✅ Very Easy | ✅ Easy | ⚠️ Complex |
| **Plugin Ecosystem** | ✅ 150+ plugins | ❌ Custom only | ✅ AWS services | ⚠️ Limited | ✅ Spring ecosystem |
| **Vietnamese Language Support** | ✅ Custom plugin | ✅ Lua script | ⚠️ Limited | ⚠️ Custom | ✅ Custom filter |
| **Resource Usage** | ⚠️ 2-4GB | ✅ <512MB | ✅ Managed | ✅ <1GB | ❌ 1-2GB (JVM) |
| **Cost** | ✅ Free (OSS) | ✅ Free | ❌ Pay per request | ✅ Free | ✅ Free |
| **Admin UI** | ✅ Yes (Konga) | ❌ No | ✅ AWS Console | ✅ Built-in | ✅ Spring Admin |
| **Vietnamese Timezone** | ✅ Easy | ✅ Easy | ⚠️ Custom | ✅ Easy | ✅ Easy |
| **Monitoring** | ✅ Prometheus | ⚠️ Custom | ✅ CloudWatch | ✅ Built-in | ✅ Micrometer |
| **Learning Curve** | ⚠️ Moderate | ✅ Low | ✅ Low | ⚠️ Moderate | ❌ High |
| **Vietnamese Data Residency** | ✅ Full control | ✅ Full control | ❌ No control | ✅ Full control | ✅ Full control |

**Legend:**
- ✅ Excellent/Good
- ⚠️ Requires custom work / Moderate
- ❌ Poor / Not recommended

---

## Recommendation for VeriSyntra

### 🏆 Primary Recommendation: **Kong Gateway**

**Why Kong for VeriSyntra:**

1. **Vietnamese Multi-Tenancy:** Built-in support with custom plugins
2. **PDPL Compliance:** Full control over Vietnamese data
3. **Production Ready:** Battle-tested at enterprise scale
4. **Plugin Ecosystem:** 150+ plugins (JWT, rate limiting, logging)
5. **Vietnamese Language Support:** Easy to add custom headers/routing
6. **Admin API:** Programmatic configuration management
7. **Community Support:** Large community, extensive documentation

**Development to Production Path:**
```
Development:
- Kong DB-less mode (declarative config)
- Simple YAML configuration
- Fast iteration

Staging:
- Kong with PostgreSQL
- Admin UI (Konga)
- Full plugin ecosystem

Production:
- Kong cluster (HA)
- Multi-region deployment (Hanoi, Da Nang, HCMC)
- Vietnamese data center deployment
```

---

### 🥈 Alternative Recommendation: **Nginx + Lua (OpenResty)**

**When to choose Nginx:**
- Smaller team (< 5 developers)
- Simpler requirements (basic routing, auth)
- Lower resource budget
- Team already knows Nginx well
- Need absolute minimal latency

**Trade-offs:**
- More custom Lua code required
- No admin UI
- Manual plugin development

---

### 🚫 NOT Recommended:

**AWS API Gateway:**
- ❌ Violates Vietnamese PDPL data residency
- ❌ Cannot guarantee data stays in Vietnam
- ❌ MPS compliance risk

**Spring Cloud Gateway:**
- ❌ Technology mismatch (Java vs Python)
- ❌ Higher resource usage
- ❌ Unnecessary complexity

---

## Implementation Roadmap

### Phase 1: Development (Weeks 1-4)
```yaml
# Use Kong DB-less mode for simplicity
kong:
  image: kong:3.4
  environment:
    KONG_DATABASE: "off"
    KONG_DECLARATIVE_CONFIG: /kong/kong.yml
  volumes:
    - ./kong.yml:/kong/kong.yml:ro
  ports:
    - "8000:8000"
```

### Phase 2: Staging (Weeks 5-12)
```yaml
# Add Kong with PostgreSQL
kong-database:
  image: postgres:15-alpine

kong:
  image: kong:3.4
  environment:
    KONG_DATABASE: postgres
    KONG_PG_HOST: kong-database

konga:  # Admin UI
  image: pantsel/konga
  ports:
    - "1337:1337"
```

### Phase 3: Production (Weeks 49-56)
```yaml
# Kubernetes deployment with Kong Ingress Controller
apiVersion: v1
kind: Service
metadata:
  name: kong-proxy
  namespace: verisyntra
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: kong
```

---

## Migration from Current Setup

### Current (Prototype)
```
React App -> http://localhost:8000 -> main_prototype.py
```

### With Kong (Microservices)
```
React App -> http://localhost:8000 (Kong) -> [Microservices]
                                          -> veri-auth-service:8001
                                          -> veri-cultural-intelligence:8002
                                          -> veri-compliance-engine:8004
```

**Migration Steps:**
1. Deploy Kong alongside monolith
2. Route `/api/v1/auth` to Kong -> veri-auth-service
3. Gradually migrate endpoints one by one
4. Eventually remove monolith routing

---

## Kong Gateway: Development to Production Path

### TL;DR: Can Kong be used in both development AND production?

**Answer: YES! Kong is PERFECT for both!**

In fact, **Kong is BETTER than Nginx** for production because:
- ✅ Same gateway from development → staging → production (consistency!)
- ✅ Configuration is portable (kong.yml works everywhere)
- ✅ No need to "migrate" from one gateway to another
- ✅ Team learns Kong once, uses it everywhere

**VeriSyntra Strategy:**
```
Development (Weeks 1-48):
├── Kong DB-less mode (lightweight, fast)
├── docker-compose.yml with Kong
└── Learn Kong configuration

Staging (Weeks 33-48):
├── Kong + PostgreSQL (store configuration)
├── Konga UI (admin interface)
└── Test production features

Production (Weeks 49-64):
├── Kong + PostgreSQL (HA setup)
├── Kong Ingress Controller (Kubernetes)
└── Multi-region deployment (North/Central/South Vietnam)
```

**Key Point:** You use the **SAME Kong Gateway** in all environments, just different deployment modes!

---

## Kong Deployment Modes (Dev → Staging → Prod)

### Mode 1: DB-less Kong (Development - Weeks 1-48)

**Perfect for:** Local development with Docker Compose

**Configuration:** Single YAML file (portable!)

```yaml
# docker-compose.yml - Development with Kong DB-less
version: '3.9'

services:
  kong-gateway:
    image: kong:3.4-alpine
    container_name: veri-kong-gateway
    environment:
      KONG_DATABASE: "off"  # DB-less mode (fast!)
      KONG_DECLARATIVE_CONFIG: /kong/kong.yml
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: "0.0.0.0:8001"
      KONG_PROXY_LISTEN: "0.0.0.0:8000"
    ports:
      - "8000:8000"  # Proxy (client requests)
      - "8001:8001"  # Admin API
    volumes:
      - ./kong.yml:/kong/kong.yml:ro  # Mount configuration
    networks:
      - veri-network

  # Your microservices
  veri-auth-service:
    build: ./services/veri-auth-service
    ports:
      - "8001:8001"
    networks:
      - veri-network

  veri-cultural-intelligence:
    build: ./services/veri-cultural-intelligence
    ports:
      - "8002:8002"
    networks:
      - veri-network
```

**kong.yml (DB-less configuration):**
```yaml
_format_version: "3.0"

services:
  - name: veri-auth-service
    url: http://veri-auth-service:8001
    routes:
      - name: auth-route
        paths:
          - /api/v1/auth
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 100

  - name: veri-cultural-intelligence
    url: http://veri-cultural-intelligence:8002
    routes:
      - name: cultural-route
        paths:
          - /api/v1/cultural
    plugins:
      - name: request-transformer
        config:
          add:
            headers:
              - "X-Vietnamese-Timezone: Asia/Ho_Chi_Minh"
```

**Advantages:**
- ✅ **Fast startup** (no database needed)
- ✅ **Simple** (single YAML file)
- ✅ **Portable** (commit kong.yml to Git)
- ✅ **Perfect for Docker Compose**

**How developers use it:**
```bash
# Start all services (including Kong)
docker-compose up -d

# Test through Kong gateway
curl http://localhost:8000/api/v1/auth/login

# View Kong configuration
curl http://localhost:8001/services

# Update kong.yml and reload
docker-compose restart kong-gateway
```

**Time to start:** 5 seconds (no database migrations!)

---

### Mode 2: Kong + PostgreSQL (Staging - Weeks 33-48)

**Perfect for:** Staging environment before production

**Configuration:** Kong with database backend + Konga admin UI

```yaml
# docker-compose.staging.yml - Staging with Kong + PostgreSQL
version: '3.9'

services:
  kong-database:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: kong
      POSTGRES_USER: kong
      POSTGRES_PASSWORD: kong_password
      TZ: Asia/Ho_Chi_Minh
    volumes:
      - kong-postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "kong"]
      interval: 10s
      timeout: 5s
      retries: 5

  kong-migration:
    image: kong:3.4-alpine
    command: kong migrations bootstrap
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kong_password
    depends_on:
      kong-database:
        condition: service_healthy

  kong-gateway:
    image: kong:3.4-alpine
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kong_password
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: "0.0.0.0:8001"
      KONG_PROXY_LISTEN: "0.0.0.0:8000"
    ports:
      - "8000:8000"  # Proxy
      - "8001:8001"  # Admin API
    depends_on:
      kong-migration:
        condition: service_completed_successfully
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 10s
      timeout: 10s
      retries: 10

  konga:
    image: pantsel/konga:latest
    container_name: veri-konga-ui
    environment:
      NODE_ENV: production
      DB_ADAPTER: postgres
      DB_HOST: kong-database
      DB_USER: kong
      DB_PASSWORD: kong_password
      DB_DATABASE: konga
    ports:
      - "1337:1337"  # Konga admin UI
    depends_on:
      kong-database:
        condition: service_healthy

volumes:
  kong-postgres-data:
```

**Advantages:**
- ✅ **Persistent configuration** (survives restarts)
- ✅ **Admin UI (Konga)** for visual management
- ✅ **Multi-team collaboration** (shared configuration)
- ✅ **Closer to production setup**

**How teams use it:**
```bash
# Start staging environment
docker-compose -f docker-compose.staging.yml up -d

# Access Konga admin UI
open http://localhost:1337

# Configure services via Konga UI (visual!)
# 1. Add service: veri-auth-service
# 2. Add route: /api/v1/auth
# 3. Add plugins: JWT, rate limiting

# Or use Admin API
curl -X POST http://localhost:8001/services \
  -d "name=veri-auth-service" \
  -d "url=http://veri-auth-service:8001"

# Configuration stored in PostgreSQL
```

**Time to start:** 30 seconds (database migrations needed)

---

### Mode 3: Kong Ingress Controller (Production - Weeks 49-64)

**Perfect for:** Kubernetes production deployment

**Configuration:** Kong as Kubernetes Ingress Controller

```yaml
# kubernetes/kong-ingress-controller.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: kong

---
# Install Kong Ingress Controller via Helm
# helm repo add kong https://charts.konghq.com
# helm install kong kong/kong \
#   --namespace kong \
#   --set ingressController.enabled=true \
#   --set postgresql.enabled=true \
#   --set postgresql.auth.database=kong \
#   --set env.database=postgres

# Then use Kubernetes Ingress resources:
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: verisyntra-ingress
  namespace: verisyntra-production
  annotations:
    konghq.com/strip-path: "false"
    konghq.com/plugins: "veri-jwt-auth, veri-rate-limiting"
spec:
  ingressClassName: kong
  tls:
  - hosts:
    - api.verisyntra.vn
    secretName: verisyntra-tls
  rules:
  - host: api.verisyntra.vn
    http:
      paths:
      - path: /api/v1/auth
        pathType: Prefix
        backend:
          service:
            name: veri-auth-service
            port:
              number: 8001
      - path: /api/v1/cultural
        pathType: Prefix
        backend:
          service:
            name: veri-cultural-intelligence
            port:
              number: 8002

---
# Kong Plugin for JWT (Kubernetes CRD)
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: veri-jwt-auth
  namespace: verisyntra-production
config:
  claims_to_verify:
    - exp
    - tenant_id
plugin: jwt

---
# Kong Plugin for Rate Limiting
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: veri-rate-limiting
  namespace: verisyntra-production
config:
  minute: 1000
  policy: redis
  redis_host: veri-redis.verisyntra-production.svc.cluster.local
  redis_port: 6379
plugin: rate-limiting
```

**Advantages:**
- ✅ **Native Kubernetes integration**
- ✅ **Auto-discovery** of services
- ✅ **High availability** (multiple Kong replicas)
- ✅ **Multi-region deployment** (North/Central/South Vietnam)
- ✅ **Auto-scaling** with HPA

**Production deployment:**
```bash
# Install Kong Ingress Controller (one-time)
helm repo add kong https://charts.konghq.com
helm repo update

helm install kong kong/kong \
  --namespace kong \
  --create-namespace \
  --set ingressController.enabled=true \
  --set postgresql.enabled=true \
  --set postgresql.auth.database=kong \
  --set env.database=postgres \
  --set proxy.type=LoadBalancer \
  --set admin.enabled=true \
  --set admin.http.enabled=true

# Deploy VeriSyntra services
kubectl apply -f kubernetes/verisyntra/

# Kong automatically discovers services and routes traffic!
```

**Time to start:** 2 minutes (Kubernetes pod scheduling)

---

## Configuration Portability (Same Config, All Environments)

### The Power of Kong: Write Once, Deploy Everywhere

**Development kong.yml:**
```yaml
_format_version: "3.0"

services:
  - name: veri-auth-service
    url: http://veri-auth-service:8001  # Docker Compose hostname
    routes:
      - name: auth-route
        paths:
          - /api/v1/auth
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 100  # Dev: lower limits
```

**Staging (same structure, different values):**
```yaml
_format_version: "3.0"

services:
  - name: veri-auth-service
    url: http://veri-auth-service.verisyntra-staging.svc.cluster.local:8001
    routes:
      - name: auth-route
        paths:
          - /api/v1/auth
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 500  # Staging: higher limits
```

**Production (Kubernetes Ingress):**
```yaml
# Same routing logic, Kubernetes-native format
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: verisyntra-ingress
  annotations:
    konghq.com/plugins: "veri-jwt-auth, veri-rate-limiting-prod"
spec:
  rules:
  - host: api.verisyntra.vn
    http:
      paths:
      - path: /api/v1/auth
        pathType: Prefix
        backend:
          service:
            name: veri-auth-service
            port:
              number: 8001
```

**Key Point:** The **routing logic** is the same across all environments. Only deployment details change!

---

## Kong vs Nginx: Production Comparison

### Why Kong is BETTER than Nginx for Production

| Feature | Kong Gateway ✅ | Nginx + Lua ⚠️ | Winner |
|---------|-----------------|----------------|--------|
| **Dev → Prod Consistency** | Same everywhere | Different configs | **Kong** |
| **Configuration Format** | Declarative YAML | Imperative nginx.conf | **Kong** |
| **Admin UI** | Konga (built-in) | None (manual) | **Kong** |
| **Plugin Ecosystem** | 150+ plugins | Manual Lua coding | **Kong** |
| **Multi-Tenancy** | Built-in (JWT, API keys) | Custom Lua | **Kong** |
| **Rate Limiting** | Per-tenant, Redis-backed | Custom Lua | **Kong** |
| **Kubernetes Integration** | Kong Ingress Controller | Nginx Ingress (separate) | **Kong** |
| **Vietnamese Language** | Custom plugins easy | Custom Lua harder | **Kong** |
| **Monitoring** | Prometheus built-in | Manual setup | **Kong** |
| **Circuit Breaker** | Plugin available | Custom Lua | **Kong** |
| **Service Discovery** | Automatic (K8s) | Manual config | **Kong** |
| **HA Setup** | PostgreSQL clustering | Nginx+ (paid) | **Kong** |
| **Cost** | Free (OSS) + Enterprise | Free (OSS) + Nginx+ (paid) | **Tie** |
| **Learning Curve** | Medium | Medium-High | **Kong** |
| **Performance** | Excellent (Nginx-based) | Excellent (native) | **Tie** |

**Score: Kong 12 - 2 Nginx**

---

## Migration Path: Kong DB-less → Kong + PostgreSQL → Kong Ingress

### Week-by-Week Progression

**Weeks 1-32 (Development):**
```bash
# docker-compose.yml with Kong DB-less
services:
  kong-gateway:
    image: kong:3.4-alpine
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /kong/kong.yml
    volumes:
      - ./kong.yml:/kong/kong.yml:ro

# Developers work with kong.yml (Git-tracked)
git add kong.yml
git commit -m "Add Vietnamese cultural intelligence routing"
```

**Weeks 33-48 (Staging):**
```bash
# docker-compose.staging.yml with Kong + PostgreSQL
services:
  kong-database:
    image: postgres:15-alpine
  
  kong-gateway:
    image: kong:3.4-alpine
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database

  konga:
    image: pantsel/konga
    # Visual admin UI at http://staging.verisyntra.vn:1337

# Team uses Konga UI to manage configuration
# Configuration stored in PostgreSQL (persistent)
```

**Weeks 49-64 (Production):**
```bash
# Kubernetes with Kong Ingress Controller
helm install kong kong/kong \
  --namespace kong \
  --set ingressController.enabled=true \
  --set postgresql.enabled=true

# Deploy VeriSyntra Ingress
kubectl apply -f kubernetes/ingress.yaml

# Kong automatically routes traffic to microservices
# Multi-region deployment (Hanoi + HCMC)
```

**Key Point:** You're using **Kong** in all 3 environments. The configuration concepts are the same!

---

## Real-World Example: Vietnamese Auth Service Routing

### Same Logic, All Environments

**Development (kong.yml):**
```yaml
services:
  - name: veri-auth-service
    url: http://veri-auth-service:8001
    routes:
      - name: auth-login
        paths:
          - /api/v1/auth/login
        methods:
          - POST
    plugins:
      - name: rate-limiting
        config:
          minute: 10  # Dev: 10 requests/min
      - name: request-transformer
        config:
          add:
            headers:
              - "X-Vietnamese-Region: development"
```

**Staging (PostgreSQL via Konga UI):**
- Service: `veri-auth-service` → `http://veri-auth-service.staging:8001`
- Route: `/api/v1/auth/login` (POST)
- Plugin: Rate Limiting → 100 requests/min
- Plugin: Request Transformer → Add header `X-Vietnamese-Region: staging`

**Production (Kubernetes Ingress):**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: veri-auth-ingress
  annotations:
    konghq.com/plugins: "veri-rate-limiting-prod, veri-vietnamese-transformer"
spec:
  rules:
  - host: api.verisyntra.vn
    http:
      paths:
      - path: /api/v1/auth/login
        pathType: Prefix
        backend:
          service:
            name: veri-auth-service
            port:
              number: 8001

---
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: veri-rate-limiting-prod
config:
  minute: 1000  # Prod: 1000 requests/min
plugin: rate-limiting

---
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: veri-vietnamese-transformer
config:
  add:
    headers:
      - "X-Vietnamese-Region: production"
plugin: request-transformer
```

**Result:** Same routing logic in all environments!

---

## Conclusion: Kong for Development AND Production

### Final Answer: YES, use Kong everywhere!

**Why Kong is the RIGHT choice for VeriSyntra:**

✅ **Consistency:** Same gateway from development to production  
✅ **Portability:** Configuration translates across environments  
✅ **Learning:** Team learns Kong once, uses it everywhere  
✅ **No Migration:** No need to switch from Nginx to Kong later  
✅ **Vietnamese Ready:** Custom plugins for cultural intelligence  
✅ **PDPL Compliant:** Built-in logging and audit trails  
✅ **Production Proven:** Used by Airbnb, NASA, Tesla at massive scale  
✅ **Cost Effective:** Free open-source, no licensing fees  

**VeriSyntra Strategy:**
```
Development (Weeks 1-48):
  Kong DB-less mode ✅
  Fast, simple, portable

Staging (Weeks 33-48):
  Kong + PostgreSQL ✅
  Persistent config, Konga UI

Production (Weeks 49-64):
  Kong Ingress Controller ✅
  Kubernetes-native, HA, multi-region
```

**Don't use Nginx for production!** Stick with Kong from development to production for:
- Easier team learning
- Consistent configuration
- Better plugin ecosystem
- Superior multi-tenancy features
- Perfect for Vietnamese PDPL compliance

---

## Conclusion

**Final Recommendation:** Start with **Kong Gateway** for VeriSyntra

**Rationale:**
1. ✅ Best fit for Vietnamese multi-tenant SaaS
2. ✅ PDPL 2025 compliance ready
3. ✅ Production-proven at scale
4. ✅ Extensive plugin ecosystem
5. ✅ Vietnamese language support via custom plugins
6. ✅ Lower total cost of ownership than custom Nginx solutions
7. ✅ **Same gateway from development to production** (consistency!)
8. ✅ **No migration needed** (use Kong everywhere)

**Deployment Strategy:**
- **Development (Weeks 1-48):** Kong DB-less mode (fast, simple)
- **Staging (Weeks 33-48):** Kong + PostgreSQL + Konga UI
- **Production (Weeks 49-64):** Kong Ingress Controller (Kubernetes)

**Fallback:** If Kong proves too complex, use **Nginx + Lua** as lightweight alternative (but you'll need to migrate to Kong for production anyway, so better to start with Kong!)

**Avoid:** AWS API Gateway (PDPL compliance issues), Spring Cloud Gateway (technology mismatch)

---

**Next Steps:**
1. Review Kong documentation: https://docs.konghq.com
2. Try Kong DB-less mode in development
3. Build Vietnamese custom plugin prototype
4. Test multi-tenant routing
5. Evaluate performance with PhoBERT ML services

---

**Document Status:** Technical Decision Record  
**Decision:** Kong Gateway (Primary), Nginx + Lua (Alternative)  
**Rationale:** Vietnamese PDPL compliance, multi-tenancy, production readiness  
**Review Date:** Phase 1 Completion (Week 4)
