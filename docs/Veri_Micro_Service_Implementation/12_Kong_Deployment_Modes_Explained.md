# Kong Deployment Modes: Development → Staging → Production

**Purpose:** Explain why Kong has different architectures across environments and why production uses Ingress Controller instead of PostgreSQL mode.

---

## The Three Kong Deployment Modes

Kong can run in three completely different modes, each optimized for different use cases:

### 1. DB-less Mode (Development)
**Configuration Storage:** Single `kong.yml` file  
**Best For:** Local development, quick iteration  
**Vietnamese Context:** Single developer on laptop testing VeriSyntra microservices

```yaml
# kong.yml - Everything in one file
_format_version: "3.0"
services:
  - name: veri-auth-service
    url: http://veri-auth-service:8001
    routes:
      - name: auth-route
        paths:
          - /api/v1/auth
```

**Pros:**
- [OK] Instant startup (no database connection)
- [OK] Simple - just one file to edit
- [OK] Perfect for local Docker Compose

**Cons:**
- [ERROR] No Admin API changes - must edit YAML and restart
- [ERROR] Cannot add routes/plugins through API calls
- [ERROR] No clustering (single instance only)

---

### 2. Traditional Mode with PostgreSQL (Staging)
**Configuration Storage:** PostgreSQL database  
**Best For:** Pre-production testing with manual configuration  
**Vietnamese Context:** QA team at HCMC office testing PDPL compliance flows

```yaml
# docker-compose.staging.yml
services:
  kong-database:
    image: postgres:15
    environment:
      POSTGRES_DB: kong
      
  kong:
    image: kong:3.4
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      
  konga:
    image: pantsel/konga
    ports:
      - "1337:1337"  # Web UI
```

**Why PostgreSQL in Staging:**

1. **Manual Testing Through UI**
   - QA team uses Konga web interface to test different configurations
   - "What happens if we add rate limiting to this endpoint?"
   - "Let's test JWT validation with different tenant IDs"
   - Click, test, modify, repeat - NO code changes needed

2. **Admin API Experimentation**
   ```bash
   # QA can create routes on the fly
   curl -X POST http://kong:8001/services/veri-auth-service/routes \
     -d "paths[]=/api/v1/auth" \
     -d "name=test-auth-route"
   ```

3. **Configuration Persistence**
   - Database stores all changes between restarts
   - Multiple Kong nodes can share same database (clustering)
   - Configuration history in PostgreSQL logs

4. **Realistic Production-like Environment**
   - Tests database connectivity patterns
   - Validates clustering behavior
   - Ensures PostgreSQL backup/restore procedures work

**Konga Admin UI Features:**
- Visual dashboard of all services/routes
- Plugin configuration through forms (no YAML needed)
- Traffic monitoring and health checks
- Consumer management for OAuth/JWT testing

---

### 3. Kubernetes Ingress Controller Mode (Production)
**Configuration Storage:** Kubernetes etcd (via Ingress/CRD manifests)  
**Best For:** Production with GitOps, auto-scaling, disaster recovery  
**Vietnamese Context:** Production deployment across North/Central/South Vietnam regions

```yaml
# kubernetes/veri-auth-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: veri-auth-ingress
  annotations:
    konghq.com/plugins: rate-limiting-5ps, jwt-auth
spec:
  ingressClassName: kong
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

**Why Ingress Controller (NOT PostgreSQL) in Production:**

#### Reason 1: Infrastructure as Code (GitOps)
```
[WRONG] Staging: QA clicks in Konga UI -> Config in PostgreSQL
                 (How do you know what changed? Who changed it?)

[CORRECT] Production: Developer commits YAML -> Git -> CI/CD -> Kubernetes
                      (Full audit trail, version control, rollback capability)
```

**Example Scenario:**
- Vietnamese developer in Hanoi adds new rate limiting rule
- Commits `veri-auth-ingress.yaml` to GitHub
- GitHub Actions automatically applies to Kubernetes
- Change tracked in Git history: who, what, when, why
- Can rollback with `git revert` + `kubectl apply`

With PostgreSQL mode, you'd need to:
- Manually update database with API calls
- Hope someone documented the change
- No easy rollback mechanism
- Configuration drift between environments

#### Reason 2: Kubernetes-Native Architecture
```
Traditional Mode (Staging):
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Kong Pod 1   │─────>│ PostgreSQL   │<─────│ Kong Pod 2   │
└──────────────┘      │   (Config)   │      └──────────────┘
                      └──────────────┘
                      (Single point of failure)

Ingress Controller Mode (Production):
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Kong Pod 1   │      │ Kubernetes   │      │ Kong Pod 2   │
│ (In-memory)  │<─────│ API Server   │─────>│ (In-memory)  │
└──────────────┘      │   (etcd)     │      └──────────────┘
                      └──────────────┘
                      (Kubernetes HA cluster)
```

**Benefits:**
- No separate database to manage/backup/scale
- Kong configuration stored in Kubernetes etcd (already highly available)
- Automatic synchronization across all Kong pods
- Leverage Kubernetes' built-in HA and disaster recovery

#### Reason 3: Declarative Configuration
```yaml
# Everything defined in version-controlled YAML files

# Service definition
apiVersion: v1
kind: Service
metadata:
  name: veri-auth-service

# Kong routing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: veri-auth-ingress

# Kong plugins
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limiting-5ps
config:
  minute: 300
  policy: local
```

**Compare to PostgreSQL mode:**
```bash
# Imperative API calls - NOT in version control
curl -X POST http://kong:8001/services \
  -d "name=veri-auth-service"
  
curl -X POST http://kong:8001/routes \
  -d "service.name=veri-auth-service"
  
curl -X POST http://kong:8001/plugins \
  -d "name=rate-limiting"
# (Did someone document this? Can you reproduce it?)
```

#### Reason 4: Auto-Scaling Integration
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: kong-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kong-ingress-controller
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**What happens:**
- Traffic spike from Vietnamese enterprises during business hours
- Kubernetes auto-scales Kong pods from 3 to 15
- All new pods automatically get configuration from Kubernetes manifests
- No PostgreSQL connection pool exhaustion
- No manual database scaling

**With PostgreSQL mode:**
- Need to scale PostgreSQL separately
- Connection pool limits
- Database becomes bottleneck under high load
- More complex monitoring (Kong metrics + PostgreSQL metrics)

#### Reason 5: Vietnamese Regional Deployment
```
VeriSyntra Production Architecture:

North Vietnam (Hanoi):                South Vietnam (HCMC):
┌─────────────────────┐              ┌─────────────────────┐
│ Kubernetes Cluster  │              │ Kubernetes Cluster  │
│ ├─ Kong Ingress     │              │ ├─ Kong Ingress     │
│ ├─ veri-auth        │              │ ├─ veri-auth        │
│ └─ veri-cultural    │              │ └─ veri-cultural    │
└─────────────────────┘              └─────────────────────┘
         │                                     │
         └──────────> Git Repository <────────┘
                     (Single source of truth)
```

**Configuration Sync:**
1. Developer commits routing change to Git
2. CI/CD applies same YAML to both clusters
3. Guaranteed identical configuration North/South
4. No database replication complexity

**With PostgreSQL mode:**
- Need to replicate PostgreSQL between Hanoi and HCMC
- Database replication lag
- Conflict resolution if both regions modified
- More infrastructure to manage

---

## Summary Table

| Feature | DB-less (Dev) | PostgreSQL (Staging) | Ingress Controller (Prod) |
|---------|---------------|---------------------|---------------------------|
| **Config Storage** | YAML file | PostgreSQL | Kubernetes etcd |
| **Admin UI** | None | Konga | Kubernetes Dashboard |
| **Configuration Method** | Edit YAML, restart | Konga UI or API | Git + kubectl |
| **Version Control** | Yes (YAML in Git) | No (DB state) | Yes (manifests in Git) |
| **Clustering** | No | Yes | Yes (Kubernetes-native) |
| **Auto-scaling** | N/A | Manual | Kubernetes HPA |
| **Best For** | Single developer | QA testing | Production traffic |
| **Infrastructure** | Minimal | Kong + PostgreSQL | Kong in Kubernetes |
| **Rollback** | Git revert | Database restore | kubectl rollout undo |

---

## Why NOT PostgreSQL in Production?

### Problem 1: Configuration Drift
```
Scenario: Emergency fix at 2 AM

[PostgreSQL Mode]
1. DevOps runs curl command to add rate limiting
2. Fix works, everyone goes back to sleep
3. Next deployment overwrites the change
4. (No one documented the curl command)
5. Production breaks again

[Ingress Controller Mode]
1. DevOps commits YAML to emergency-fix branch
2. CI/CD applies to production
3. Fix is in Git history forever
4. Next deployment includes the fix
5. Can rollback anytime with git revert
```

### Problem 2: Disaster Recovery
```
[PostgreSQL Mode]
Disaster: Database corrupted
Recovery Steps:
1. Restore PostgreSQL from backup (hope backup is recent)
2. Verify all routes/plugins restored correctly
3. Manually compare with documentation (if exists)
4. Hope no one made undocumented changes

[Ingress Controller Mode]
Disaster: Entire Kubernetes cluster lost
Recovery Steps:
1. Create new Kubernetes cluster
2. kubectl apply -f kubernetes/
3. All configuration restored from Git
4. Guaranteed identical to before disaster
```

### Problem 3: Compliance (Vietnamese PDPL)
```yaml
# PDPL Audit Requirement: "Show all configuration changes in Q4 2025"

[PostgreSQL Mode]
- Check PostgreSQL logs (if enabled)
- Hope database wasn't backed up over logs
- Try to reconstruct from Konga screenshots?
- Stressful audit

[Ingress Controller Mode]
git log --since="2025-10-01" --until="2025-12-31" \
  --grep="veri-.*-ingress.yaml"
# Full audit trail: who, what, when, why
# Show auditor the Git commits
# Easy PDPL compliance
```

---

## The Migration Path

### Week 1-48 (Development):
```yaml
# docker-compose.yml
veri-api-gateway:
  image: kong:3.4-alpine
  environment:
    KONG_DATABASE: "off"
    KONG_DECLARATIVE_CONFIG: /kong/kong.yml
```
**Focus:** Build microservices, test locally

---

### Week 40-48 (Staging Setup):
```yaml
# docker-compose.staging.yml
kong-database:
  image: postgres:15
  
kong:
  image: kong:3.4
  environment:
    KONG_DATABASE: postgres
    
konga:
  image: pantsel/konga
```
**Focus:** QA team tests with UI, experiments with plugins

---

### Week 49-64 (Production):
```yaml
# kubernetes/kong-ingress-controller.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kong-ingress-controller
spec:
  replicas: 3
```
**Focus:** GitOps, auto-scaling, multi-region deployment

---

## Vietnamese Business Context

**For Vietnamese Development Team:**
- **Development:** Each developer runs Kong DB-less on laptop (simple, fast)
- **Staging:** QA team in HCMC uses Konga UI to test PDPL compliance flows (visual, interactive)
- **Production:** DevOps team in Hanoi manages through Git/Kubernetes (auditable, compliant)

**For Vietnamese Enterprises (VeriSyntra Customers):**
- Production uses Ingress Controller for:
  - PDPL audit compliance (full Git history)
  - Multi-region deployment (North/Central/South Vietnam)
  - Government reporting (all changes tracked)
  - Data residency compliance (Kubernetes namespace isolation)

---

## Final Answer

**Why no PostgreSQL in Production?**

Because **Kubernetes itself is the database**. The Ingress Controller mode uses Kubernetes' etcd (the same database that stores all Kubernetes configuration) to store Kong configuration. This means:

1. ✅ **One less database to manage** (no PostgreSQL backups, scaling, monitoring)
2. ✅ **Configuration in Git** (version control, audit trail, rollback)
3. ✅ **Kubernetes-native** (works with HPA, service mesh, namespaces)
4. ✅ **GitOps ready** (CI/CD applies YAML, no manual API calls)
5. ✅ **PDPL compliant** (full audit trail for Vietnamese regulators)

**Why PostgreSQL in Staging?**

Because **QA needs manual testing**. The PostgreSQL mode with Konga UI allows:

1. ✅ **Click-based testing** (try different routes without code changes)
2. ✅ **Plugin experimentation** (test rate limiting, JWT configs visually)
3. ✅ **Realistic environment** (tests database patterns before production)
4. ✅ **Learning environment** (QA team learns Kong without breaking production)

---

**Document Status:** Complete  
**Last Updated:** November 1, 2025  
**Next Document:** 11_Kubernetes_Production_Deployment.md
