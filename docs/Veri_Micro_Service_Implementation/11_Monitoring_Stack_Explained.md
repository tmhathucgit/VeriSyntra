# VeriSyntra Monitoring Stack Explained

**Document Version:** 1.0.0  
**Date:** November 1, 2025  
**Purpose:** Explain why we use Prometheus + Grafana + ELK Stack (not just one tool)

---

## TL;DR: Why All Three?

**Question:** Why use Prometheus, Grafana, AND ELK Stack for monitoring?

**Answer:** Because they do **DIFFERENT jobs** - like having a car dashboard (metrics), GPS (traces), and black box recorder (logs).

```
Observability = Metrics + Logs + Traces

Prometheus → Collects METRICS (numbers)
Grafana    → Visualizes METRICS (dashboards)
ELK Stack  → Aggregates LOGS (text messages)

All three needed for complete observability!
```

**Analogy:**
```
Vietnamese Business is Sick (Service Down):

Prometheus (Doctor's Instruments):
  - "Heart rate 180 bpm" (CPU: 90%)
  - "Blood pressure 200/120" (Memory: 95%)
  → Tells you WHAT is wrong (numbers)

Grafana (Medical Chart):
  - Visual graph showing heart rate spike
  - Dashboard showing all vital signs
  → Shows you WHEN it happened (visualization)

ELK Stack (Patient History):
  - "Patient ate seafood at 2 PM" (Log: AuthenticationError at 14:00)
  - "Patient complained of chest pain" (Log: Database connection timeout)
  → Tells you WHY it happened (context)

You need ALL THREE to diagnose and fix the problem!
```

---

## The Three Pillars of Observability

### Pillar 1: Metrics (Numbers)

**What:** Numeric measurements over time

**Examples:**
- CPU usage: 45%
- Memory usage: 2.3 GB
- Request rate: 1,200 requests/second
- Response time: 150ms (p95)
- Error rate: 0.5%

**Tool:** **Prometheus** (collects) + **Grafana** (visualizes)

**Use Cases:**
- "Is the service healthy right now?"
- "How many Vietnamese users are online?"
- "Is CPU usage increasing?"
- "Are we hitting rate limits?"

---

### Pillar 2: Logs (Text Messages)

**What:** Timestamped text records of events

**Examples:**
```
[2025-11-01 10:23:45] INFO: Vietnamese user logged in: user_id=123, region=south
[2025-11-01 10:23:46] ERROR: Database connection failed: timeout after 30s
[2025-11-01 10:23:47] WARN: Rate limit approaching: 95/100 requests
[2025-11-01 10:23:48] DEBUG: PhoBERT model loaded: model_version=2.0
```

**Tool:** **ELK Stack** (Elasticsearch, Logstash, Kibana)

**Use Cases:**
- "WHY did this specific request fail?"
- "What error message did the user see?"
- "Which Vietnamese company had the issue?"
- "What was the full stack trace?"

---

### Pillar 3: Traces (Request Journeys)

**What:** Path of a single request through multiple services

**Example:**
```
Vietnamese user clicks "Generate PDPL Document"
  ├─> 1. Kong Gateway (5ms)
  ├─> 2. veri-auth-service (15ms) - Check JWT
  ├─> 3. veri-company-registry (20ms) - Get company data
  ├─> 4. veri-compliance-engine (50ms) - Get PDPL requirements
  ├─> 5. veri-vi-ai-classification (200ms) - PhoBERT analysis [SLOW!]
  └─> 6. veri-document-generator (30ms) - Generate PDF
Total: 320ms
```

**Tool:** **Jaeger** or **Zipkin** (not in current stack yet, but should add!)

**Use Cases:**
- "Which service is slowing down the request?"
- "How does a Vietnamese user request flow through services?"
- "Where are the bottlenecks?"

---

## Why NOT Just One Tool?

### Option 1: Use ONLY Prometheus/Grafana (❌ Not Enough!)

**What you CAN do:**
- ✅ See CPU usage is 95%
- ✅ See error rate is 10%
- ✅ See response time is 2,000ms

**What you CANNOT do:**
- ❌ See WHICH Vietnamese user had the error
- ❌ See the ACTUAL error message
- ❌ Search for "Database connection failed" across all services
- ❌ Debug WHY the error happened

**Example Problem:**
```
Grafana Dashboard:
  [ALERT] veri-auth-service error rate: 50% (last 5 minutes)

Developer: "What's the error?"
Grafana: "I don't know, I only track numbers, not error messages!"

→ Need ELK Stack to see the actual error logs!
```

---

### Option 2: Use ONLY ELK Stack (❌ Not Enough!)

**What you CAN do:**
- ✅ Search for "Database connection failed"
- ✅ See full error stack traces
- ✅ Filter logs by Vietnamese company ID

**What you CANNOT do:**
- ❌ See trends over time (is CPU increasing?)
- ❌ Alert when response time > 500ms
- ❌ Visualize Vietnamese user traffic patterns
- ❌ Track metrics aggregations (average, percentiles)

**Example Problem:**
```
ELK Logs:
  [ERROR] Database connection timeout
  [ERROR] Database connection timeout
  [ERROR] Database connection timeout
  ... (1000 more errors)

Developer: "How many errors per second? Is it getting worse?"
ELK: "I don't track metrics, only logs!"

→ Need Prometheus to track error rate over time!
```

---

## The VeriSyntra Monitoring Stack

### Complete Observability Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VeriSyntra Microservices                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Auth    │  │ Cultural │  │ AIDPO    │  │  BizIntel│            │
│  │ Service  │  │   Intel  │  │   (ML)   │  │  Service │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       │             │              │             │                  │
│       ├─── Metrics ─┴──────────────┴─────────────┤                  │
│       │             (CPU, memory, requests/sec)  │                  │
│       │                                           │                  │
│       ├─── Logs ────┬──────────────┬─────────────┤                  │
│       │      (Error messages, user IDs, events)  │                  │
│       │                                           │                  │
│       ├─── Traces ──┴──────────────┴─────────────┤                  │
│       │      (Request flow across services)      │                  │
└───────┼───────────────────────────────────────────┼──────────────────┘
        │                                           │
        ▼                                           ▼
┌───────────────────┐                      ┌───────────────────┐
│   PROMETHEUS      │                      │    ELK STACK      │
│  (Metrics Store)  │                      │  (Logs Store)     │
├───────────────────┤                      ├───────────────────┤
│ - Scrapes metrics │                      │ - Elasticsearch   │
│   every 15s       │                      │   (Store logs)    │
│ - Time-series DB  │                      │ - Logstash        │
│ - Alert rules     │                      │   (Process logs)  │
│ - Retention: 30d  │                      │ - Kibana          │
└────────┬──────────┘                      │   (Search logs)   │
         │                                  └───────────────────┘
         ▼
┌───────────────────┐
│     GRAFANA       │
│  (Visualization)  │
├───────────────────┤
│ - Dashboards      │
│ - Graphs/Charts   │
│ - Alerts UI       │
│ - Vietnamese UI   │
└───────────────────┘
```

---

## Tool-by-Tool Breakdown

### 1. Prometheus (Metrics Collection)

**What it does:** Scrapes numeric metrics from services

**How it works:**
```python
# In veri-auth-service (FastAPI)
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
login_attempts = Counter(
    'veri_auth_login_attempts_total',
    'Total login attempts',
    ['region', 'status']  # Vietnamese region, success/failure
)

login_duration = Histogram(
    'veri_auth_login_duration_seconds',
    'Login request duration',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

@app.post("/api/v1/auth/login")
async def login(credentials: LoginRequest):
    with login_duration.time():  # Measure duration
        try:
            user = await authenticate(credentials)
            login_attempts.labels(
                region=user.region,
                status='success'
            ).inc()
            return {"token": generate_jwt(user)}
        except AuthenticationError:
            login_attempts.labels(
                region=credentials.region,
                status='failure'
            ).inc()
            raise

# Prometheus scrapes this endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

**Prometheus scrapes every 15 seconds:**
```
# GET http://veri-auth-service:8001/metrics

# HELP veri_auth_login_attempts_total Total login attempts
# TYPE veri_auth_login_attempts_total counter
veri_auth_login_attempts_total{region="north",status="success"} 1234
veri_auth_login_attempts_total{region="north",status="failure"} 56
veri_auth_login_attempts_total{region="south",status="success"} 5678
veri_auth_login_attempts_total{region="south",status="failure"} 123

# HELP veri_auth_login_duration_seconds Login request duration
# TYPE veri_auth_login_duration_seconds histogram
veri_auth_login_duration_seconds_bucket{le="0.1"} 234
veri_auth_login_duration_seconds_bucket{le="0.5"} 1890
veri_auth_login_duration_seconds_bucket{le="1.0"} 2345
veri_auth_login_duration_seconds_sum 1567.8
veri_auth_login_duration_seconds_count 2500
```

**What Prometheus stores:**
- Metric name: `veri_auth_login_attempts_total`
- Labels: `region=north`, `status=success`
- Value: `1234` (at timestamp `2025-11-01 10:23:45`)

**Prometheus Query Language (PromQL):**
```promql
# Total login attempts per second (all regions)
rate(veri_auth_login_attempts_total[5m])

# Login failure rate (percentage)
sum(rate(veri_auth_login_attempts_total{status="failure"}[5m]))
/
sum(rate(veri_auth_login_attempts_total[5m]))
* 100

# p95 login duration
histogram_quantile(0.95, rate(veri_auth_login_duration_seconds_bucket[5m]))

# Vietnamese south region login rate
rate(veri_auth_login_attempts_total{region="south"}[5m])
```

**Why you need Prometheus:**
- ✅ Time-series data (track trends over time)
- ✅ Efficient storage (optimized for metrics)
- ✅ Alert rules (trigger when metric crosses threshold)
- ✅ Service discovery (auto-discover new services)

---

### 2. Grafana (Metrics Visualization)

**What it does:** Creates beautiful dashboards from Prometheus data

**Example Dashboard: VeriSyntra Vietnamese Auth Service**

```
┌─────────────────────────────────────────────────────────────────────┐
│  VeriSyntra Auth Service - Vietnamese Business Hours Monitoring     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [Login Attempts per Second]                                        │
│   300 ┤                                      ╭─╮                    │
│       │                                  ╭───╯ ╰─╮                  │
│   200 ┤                          ╭───────╯       ╰─╮                │
│       │                  ╭───────╯                 ╰──╮             │
│   100 ┤          ╭───────╯                            ╰────         │
│       │  ────────╯                                                  │
│     0 ┤                                                             │
│       └────────────────────────────────────────────────────────     │
│       8AM    9AM    10AM   11AM   12PM   1PM    2PM    3PM          │
│       (Peak: 9-10 AM Vietnamese business hours)                     │
│                                                                      │
│  [Login Success Rate by Region]                                     │
│   North Vietnam:  98.5% ✅  (1,234 requests)                        │
│   Central Vietnam: 97.2% ✅  (567 requests)                         │
│   South Vietnam:   99.1% ✅  (5,678 requests)                       │
│                                                                      │
│  [Response Time (p95)]                                              │
│   150ms ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 150ms       │
│   Target: < 200ms ✅                                                │
│                                                                      │
│  [Active Vietnamese Users]                                          │
│   [🔵 3,245 users online]                                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Grafana Configuration:**
```json
{
  "dashboard": {
    "title": "VeriSyntra Auth Service",
    "panels": [
      {
        "title": "Login Attempts per Second",
        "targets": [
          {
            "expr": "sum(rate(veri_auth_login_attempts_total[5m]))",
            "legendFormat": "Total Logins"
          },
          {
            "expr": "sum(rate(veri_auth_login_attempts_total{region=\"north\"}[5m]))",
            "legendFormat": "North Vietnam"
          },
          {
            "expr": "sum(rate(veri_auth_login_attempts_total{region=\"south\"}[5m]))",
            "legendFormat": "South Vietnam"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Login Success Rate",
        "targets": [
          {
            "expr": "sum(rate(veri_auth_login_attempts_total{status=\"success\"}[5m])) / sum(rate(veri_auth_login_attempts_total[5m])) * 100"
          }
        ],
        "type": "singlestat",
        "thresholds": "95,98"  // Yellow < 95%, Green > 98%
      }
    ]
  }
}
```

**Why you need Grafana:**
- ✅ Visual dashboards (humans understand graphs better than numbers)
- ✅ Multi-datasource (Prometheus, Elasticsearch, etc.)
- ✅ Alerting UI (see alerts in visual format)
- ✅ Team sharing (Vietnamese team can view same dashboards)
- ✅ Vietnamese timezone support (display in Asia/Ho_Chi_Minh)

**What Grafana CANNOT do:**
- ❌ Store metrics (that's Prometheus's job)
- ❌ Show log messages (that's ELK's job)
- ❌ Search for errors (that's Kibana's job)

---

### 3. ELK Stack (Logs Aggregation)

**ELK = Elasticsearch + Logstash + Kibana**

#### 3a. Elasticsearch (Log Storage)

**What it does:** Stores and indexes log messages for fast search

**Example logs stored:**
```json
{
  "@timestamp": "2025-11-01T10:23:45.123Z",
  "service": "veri-auth-service",
  "level": "ERROR",
  "message": "Database connection timeout",
  "user_id": "user_123",
  "company_id": "company_456",
  "region": "south",
  "request_id": "req-789",
  "stack_trace": "Traceback (most recent call last)...",
  "duration_ms": 30000
}
```

**Why Elasticsearch:**
- ✅ Full-text search (find "Database connection" across all logs)
- ✅ Fast search (millions of logs in milliseconds)
- ✅ Indexing (automatic fields extraction)
- ✅ Vietnamese text search (supports Vietnamese language)

---

#### 3b. Logstash (Log Processing)

**What it does:** Collects logs from services, processes them, sends to Elasticsearch

**Configuration:**
```ruby
# logstash.conf
input {
  # Collect logs from all VeriSyntra services
  beats {
    port => 5044
  }
}

filter {
  # Parse JSON logs
  json {
    source => "message"
  }

  # Add Vietnamese timezone
  date {
    match => ["@timestamp", "ISO8601"]
    timezone => "Asia/Ho_Chi_Minh"
  }

  # Extract Vietnamese company ID from message
  grok {
    match => {
      "message" => ".*company_id=%{NOTSPACE:company_id}.*"
    }
  }

  # Add Vietnamese region based on company
  if [company_id] =~ /^VN-HN-/ {
    mutate { add_field => { "region" => "north" } }
  } else if [company_id] =~ /^VN-DN-/ {
    mutate { add_field => { "region" => "central" } }
  } else if [company_id] =~ /^VN-HCM-/ {
    mutate { add_field => { "region" => "south" } }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "verisyntra-logs-%{+YYYY.MM.dd}"
  }
}
```

---

#### 3c. Kibana (Log Search & Visualization)

**What it does:** UI for searching and visualizing logs

**Example Searches:**

**Search 1: Find all Vietnamese auth errors today:**
```
service:veri-auth-service AND level:ERROR AND @timestamp:[now-1d TO now]
```

**Search 2: Find which Vietnamese company had database issues:**
```
message:"Database connection timeout" AND company_id:*
```

**Search 3: Vietnamese south region login failures:**
```
service:veri-auth-service AND region:south AND message:"Login failed"
```

**Kibana Dashboard Example:**
```
┌─────────────────────────────────────────────────────────────────────┐
│  VeriSyntra Logs - Last 24 Hours (Vietnamese Timezone)              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [Error Rate by Service]                                            │
│   veri-auth-service:      23 errors                                 │
│   veri-cultural:          5 errors                                  │
│   veri-aidpo (PhoBERT):   45 errors ⚠️ (GPU memory issues)          │
│                                                                      │
│  [Top Error Messages]                                               │
│   1. "Database connection timeout" (34 occurrences)                 │
│   2. "PhoBERT model out of memory" (23 occurrences)                 │
│   3. "Vietnamese company not found" (12 occurrences)                │
│                                                                      │
│  [Recent Errors]                                                    │
│   10:23:45 ERROR veri-auth Database connection timeout              │
│              user_id=123, company_id=VN-HCM-456, req=req-789        │
│              Stack trace: ... (click to expand)                     │
│                                                                      │
│   10:23:46 ERROR veri-aidpo PhoBERT OOM: 16GB GPU memory exceeded  │
│              company_id=VN-HN-789, document_size=50MB               │
│              Recommendation: Split document into smaller chunks     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Why you need ELK:**
- ✅ Search error messages (find "Database timeout" across all services)
- ✅ Context (see full stack traces, user IDs, company IDs)
- ✅ Debugging (understand WHY something failed)
- ✅ Audit trails (PDPL compliance - track who accessed what)
- ✅ Vietnamese language support (search Vietnamese error messages)

**What ELK CANNOT do:**
- ❌ Track numeric trends (that's Prometheus's job)
- ❌ Show CPU/memory usage (that's Prometheus's job)
- ❌ Alert on metrics (that's Prometheus's job)

---

## Real-World Debugging Scenario

### Scenario: "Vietnamese Users Cannot Login!"

**Step 1: Check Grafana Dashboard (Metrics)**

```
Grafana Alert:
[CRITICAL] veri-auth-service error rate: 50% (last 5 minutes)

Dashboard shows:
- Login attempts: 200/sec (normal)
- Login failures: 100/sec ⚠️ (usually 2/sec)
- Response time: 5,000ms 🚨 (usually 150ms)
- CPU: 95% 🚨 (usually 40%)
- Memory: 85% ⚠️
```

**What you know:**
- ✅ WHEN: Started 5 minutes ago
- ✅ WHAT: 50% login failure rate
- ✅ WHERE: veri-auth-service
- ❓ WHY: Unknown (need logs!)

---

**Step 2: Check Kibana Logs (ELK)**

```kibana
Search: service:veri-auth-service AND level:ERROR AND @timestamp:[now-5m TO now]

Results (100 errors):
┌────────────────────────────────────────────────────────────────┐
│ 10:23:45 ERROR Database connection timeout                    │
│   Connection pool exhausted: 50/50 connections in use         │
│   Waited 30s, no available connections                        │
│   company_id=VN-HCM-456, user_id=123                          │
│   Stack trace: sqlalchemy.exc.TimeoutError                    │
│                                                                │
│ (Repeated 100 times in last 5 minutes)                        │
└────────────────────────────────────────────────────────────────┘
```

**What you know NOW:**
- ✅ WHY: Database connection pool exhausted
- ✅ ROOT CAUSE: Too many concurrent database connections
- ✅ AFFECTED: All Vietnamese users trying to login

---

**Step 3: Check Prometheus (Metrics) - Database Service**

```promql
# Check database connection pool usage
veri_postgres_connections_active

Result: 50/50 (maxed out!)

# Check which service is using most connections
veri_postgres_connections_by_service{service="veri-auth-service"}: 10
veri_postgres_connections_by_service{service="veri-cultural"}: 5
veri_postgres_connections_by_service{service="veri-aidpo"}: 35 🚨 (PhoBERT using 35!)
```

**FOUND IT!**
- ✅ Root cause: `veri-vi-ai-classification` (PhoBERT ML service) is holding 35 database connections
- ✅ Likely: PhoBERT batch processing Vietnamese documents, forgot to close connections

---

**Step 4: Check ELK Logs (veri-vi-ai-classification)**

```kibana
Search: service:veri-vi-ai-classification AND @timestamp:[now-10m TO now]

Result:
┌────────────────────────────────────────────────────────────────┐
│ 10:18:00 INFO Starting batch processing: 1,000 Vietnamese     │
│              PDPL documents for company VN-HCM-789            │
│                                                                │
│ 10:18:05 WARN Database connection not closed in               │
│              process_document() function                      │
│                                                                │
│ (Connection leak detected!)                                   │
└────────────────────────────────────────────────────────────────┘
```

**SOLUTION:**
```python
# Bug in veri-vi-ai-classification/app/processor.py
async def process_document(doc_id: str):
    conn = await db.get_connection()
    # ... process with PhoBERT
    # BUG: Forgot to close connection!

# Fix:
async def process_document(doc_id: str):
    async with db.get_connection() as conn:  # Auto-close with context manager
        # ... process with PhoBERT
        # ✅ Connection automatically closed
```

**Deploy fix, 2 minutes later:**
- Grafana: Error rate 0%, response time 150ms ✅
- Kibana: No more timeout errors ✅
- Problem solved!

---

## Summary: Why All Three Tools?

### What Each Tool Does

| Tool | Purpose | What It Stores | Query Language | Best For |
|------|---------|----------------|----------------|----------|
| **Prometheus** | Collect metrics | Numbers (time-series) | PromQL | Trends, alerts, monitoring |
| **Grafana** | Visualize metrics | Nothing (uses Prometheus data) | Visual UI | Dashboards, graphs |
| **Elasticsearch** | Store logs | Text (log messages) | Lucene Query | Search, debugging |
| **Logstash** | Process logs | Nothing (pipeline) | N/A | Log parsing, enrichment |
| **Kibana** | Search logs | Nothing (uses Elasticsearch data) | Kibana Query Language | Log search, analysis |

### The Debugging Workflow

```
1. Grafana Alert fires
   → "Error rate is 50%!"
   → You know: WHAT, WHEN, WHERE

2. Check Kibana logs
   → Search for errors in that timeframe
   → You discover: WHY (error messages, stack traces)

3. Check Prometheus metrics
   → Find which service/resource is affected
   → You confirm: ROOT CAUSE (database connection pool)

4. Fix the code
   → Deploy fix

5. Verify in Grafana
   → Error rate back to 0%
   → Response time back to normal
```

---

## VeriSyntra Monitoring Stack Configuration

### Docker Compose (Development)

```yaml
# docker-compose.monitoring.yml
version: '3.9'

services:
  # 1. Prometheus (Metrics Collection)
  prometheus:
    image: prom/prometheus:latest
    container_name: veri-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'
    networks:
      - veri-network

  # 2. Grafana (Metrics Visualization)
  grafana:
    image: grafana/grafana:latest
    container_name: veri-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_DEFAULT_TIMEZONE=Asia/Ho_Chi_Minh
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    depends_on:
      - prometheus
    networks:
      - veri-network

  # 3. Elasticsearch (Log Storage)
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    container_name: veri-elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
      - xpack.security.enabled=false
      - TZ=Asia/Ho_Chi_Minh
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    networks:
      - veri-network

  # 4. Logstash (Log Processing)
  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    container_name: veri-logstash
    ports:
      - "5044:5044"
      - "9600:9600"
    environment:
      - TZ=Asia/Ho_Chi_Minh
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    depends_on:
      - elasticsearch
    networks:
      - veri-network

  # 5. Kibana (Log Visualization)
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    container_name: veri-kibana
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - I18N_LOCALE=vi  # Vietnamese UI
      - SERVER_TIMEZONE=Asia/Ho_Chi_Minh
    depends_on:
      - elasticsearch
    networks:
      - veri-network

volumes:
  prometheus-data:
  grafana-data:
  elasticsearch-data:

networks:
  veri-network:
    external: true
```

---

## Alternatives (Why NOT use them for VeriSyntra)

### Alternative 1: Datadog / New Relic (All-in-One SaaS)

**Pros:**
- ✅ All-in-one (metrics + logs + traces)
- ✅ Easy setup (SaaS)
- ✅ Beautiful UI

**Cons:**
- ❌ **EXPENSIVE** ($15-30 per host per month)
- ❌ **PDPL VIOLATION** (data sent to US servers, not Vietnam!)
- ❌ Vendor lock-in

**Verdict:** ❌ NOT suitable for Vietnamese PDPL compliance

---

### Alternative 2: CloudWatch (AWS)

**Pros:**
- ✅ Integrated with AWS

**Cons:**
- ❌ **PDPL VIOLATION** (data in AWS, not Vietnamese data centers)
- ❌ Expensive
- ❌ Vendor lock-in (AWS only)

**Verdict:** ❌ NOT suitable for Vietnamese PDPL compliance

---

### Alternative 3: Loki (Grafana's Log Solution)

**What it is:** Grafana's log aggregation (alternative to ELK)

**Pros:**
- ✅ Integrated with Grafana
- ✅ Cheaper than Elasticsearch (less indexing)

**Cons:**
- ⚠️ Limited search capabilities (no full-text indexing)
- ⚠️ Slower for complex queries
- ⚠️ Less mature than Elasticsearch

**Verdict:** ⚠️ Could consider for VeriSyntra if ELK is too resource-heavy

---

## Final Recommendation for VeriSyntra

### Use All Three: Prometheus + Grafana + ELK

**Why:**
1. ✅ **Complete observability** (metrics + logs + visualization)
2. ✅ **Open-source** (no licensing costs)
3. ✅ **PDPL compliant** (data stays in Vietnamese data centers)
4. ✅ **Industry standard** (easy to hire Vietnamese developers who know these tools)
5. ✅ **Vietnamese timezone support** (all tools support Asia/Ho_Chi_Minh)
6. ✅ **Scalable** (works for 10,000+ Vietnamese businesses)

**Cost:**
- Open-source: $0 licensing
- Infrastructure: ~$200-500/month (Vietnamese cloud servers)

**Team effort:**
- Setup time: 1-2 weeks (Phase 8, Weeks 57-64)
- Maintenance: 4-8 hours/month

---

## Conclusion

**Question:** Why use Prometheus, Grafana, AND ELK Stack?

**Answer:**

```
Prometheus → Collect WHAT is happening (metrics)
Grafana    → Visualize WHEN it happened (dashboards)
ELK Stack  → Understand WHY it happened (logs)

All three = Complete observability for VeriSyntra!
```

**Vietnamese Business Analogy:**
```
Running VeriSyntra without all three monitoring tools is like:

Running a Vietnamese restaurant with:
- No customer count (Prometheus)
- No sales dashboard (Grafana)
- No customer feedback (ELK)

→ You're flying blind! You need all three to succeed!
```

---

**Don't cut corners on observability. Use all three tools for production-ready VeriSyntra!** 🚀

---

**Document Status:** Technical Explanation  
**Tools:** Prometheus (metrics), Grafana (visualization), ELK (logs)  
**Recommendation:** Use all three for complete observability  
**Cost:** ~$200-500/month Vietnamese cloud infrastructure  
**Next Steps:** Implement in Phase 8 (Weeks 57-64)
