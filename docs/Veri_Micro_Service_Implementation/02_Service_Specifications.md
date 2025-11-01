# VeriSyntra Microservices - Detailed Service Specifications

**Document Version:** 1.0.0  
**Date:** November 1, 2025  
**Purpose:** Technical specifications for each microservice in VeriSyntra ecosystem

---

## Service Specification Template

Each service follows this standard structure:
- **Service Name:** Unique identifier
- **Responsibility:** Single Responsibility Principle (SRP)
- **Technology Stack:** Programming language, frameworks, libraries
- **API Endpoints:** REST/GraphQL/gRPC interfaces
- **Data Storage:** Database requirements
- **Dependencies:** Other services required
- **Scalability:** Horizontal/vertical scaling strategy
- **Docker Configuration:** Container specifications

---

## 1. Authentication & Security Services

### 1.1 veri-auth-service

**Responsibility:** Multi-tenant authentication, authorization, JWT token management

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Auth Libraries:** PyJWT, passlib, python-multipart
- **Database:** PostgreSQL (user credentials, tenant mappings)

**API Endpoints:**
```yaml
POST /api/v1/auth/register
  - Register new Vietnamese business user
  - Input: email, password, company_name, veri_region
  - Output: user_id, tenant_id, verification_email_sent

POST /api/v1/auth/login
  - Authenticate Vietnamese user with multi-tenant context
  - Input: email, password, tenant_id (optional)
  - Output: access_token, refresh_token, veri_business_context

POST /api/v1/auth/refresh
  - Refresh JWT access token
  - Input: refresh_token
  - Output: new_access_token

POST /api/v1/auth/verify-email
  - Verify Vietnamese business email
  - Input: verification_token
  - Output: email_verified, account_activated

GET /api/v1/auth/me
  - Get current user profile with Vietnamese business context
  - Headers: Authorization: Bearer {token}
  - Output: user_profile, veri_business_context, permissions

POST /api/v1/auth/change-password
  - Change user password (Vietnamese language support)
  - Input: old_password, new_password
  - Output: password_changed, new_token

GET /api/v1/tenants/{tenant_id}
  - Get Vietnamese business tenant information
  - Output: tenant_profile, regional_settings, subscription_tier
```

**Data Models:**
```python
class VeriUser:
    user_id: UUID
    email: str
    hashed_password: str
    full_name: str
    full_name_vi: str  # Vietnamese name
    phone_number: str  # Vietnamese format
    tenant_id: UUID
    role: VeriUserRole  # admin, dpo, staff, auditor
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: datetime

class VeriTenant:
    tenant_id: UUID
    company_name: str
    company_name_vi: str
    veri_regional_location: str  # north, central, south
    veri_industry_type: str
    subscription_tier: str  # starter, professional, enterprise
    veri_business_context: dict
    created_at: datetime
    active: bool
```

**Environment Variables:**
```bash
DATABASE_URL=postgresql://user:pass@veri-postgres:5432/veri_auth
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
VIETNAMESE_TIMEZONE=Asia/Ho_Chi_Minh
```

**Docker Configuration:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Scalability:** Stateless service, horizontally scalable (3-10 replicas)

---

### 1.2 veri-api-gateway

**Responsibility:** Entry point for all client requests, routing, rate limiting, Vietnamese locale detection

**Technology Stack:**
- **Gateway:** Kong Gateway (DB-less mode for dev, PostgreSQL-backed for staging/prod)
- **Alternative:** FastAPI-based custom gateway (if Kong licensing becomes issue)
- **Rate Limiting:** Redis-based
- **Load Balancing:** Round-robin, weighted

**Features:**
- Vietnamese language header detection (`Accept-Language: vi-VN`)
- Multi-tenant routing based on JWT claims
- API versioning (v1, v2)
- Rate limiting per Vietnamese business tier
- Request/response logging with Vietnamese timezone
- CORS configuration for Vietnamese domains

**Configuration:**
```yaml
# Kong configuration example
services:
  - name: veri-cultural-intelligence
    url: http://veri-cultural-intelligence:8002
    routes:
      - name: cultural-route
        paths:
          - /api/v1/cultural
        strip_path: true
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: jwt
        config:
          claims_to_verify:
            - exp
            - tenant_id
```

---

## 2. Core Business Services

### 2.1 veri-cultural-intelligence

**Responsibility:** Vietnamese cultural context, regional business intelligence, localization

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Data:** In-memory Vietnamese province/cultural data
- **Cache:** Redis for frequently accessed contexts

**API Endpoints:**
```yaml
GET /api/v1/cultural/context
  - Get Vietnamese business cultural context
  - Query: region (north/central/south), industry, company_size
  - Output: veri_cultural_context, communication_style, formality_level

GET /api/v1/cultural/provinces
  - List all Vietnamese provinces with business characteristics
  - Output: provinces[], regional_grouping

GET /api/v1/cultural/holidays
  - Vietnamese business calendar and holidays
  - Query: year, region
  - Output: holidays[], business_impact_analysis

POST /api/v1/cultural/analyze-business
  - Analyze Vietnamese business profile for cultural adaptation
  - Input: company_profile, regional_location, industry
  - Output: cultural_recommendations, ui_adaptations

GET /api/v1/cultural/timezone
  - Get current Vietnamese time (Asia/Ho_Chi_Minh)
  - Output: current_time, timezone_info, business_hours
```

**Data Models:**
```python
class VeriCulturalContext:
    veri_region: str  # north, central, south
    veri_communication_style: str  # formal, balanced, friendly
    veri_hierarchy_level: str  # executive, director, manager, staff
    veri_business_maturity: str  # traditional, modern, innovative
    veri_formalities: dict
    veri_regional_patterns: dict
    veri_language_preference: str  # vietnamese_primary, bilingual

class VietnameseProvince:
    province_name: str
    province_name_en: str
    region: str  # north, central, south
    business_centers: list[str]
    economic_zones: list[str]
    cultural_characteristics: dict
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn pytz
COPY . .
EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
```

**Scalability:** Stateless, read-heavy, 2-5 replicas with Redis cache

---

### 2.2 veri-company-registry

**Responsibility:** Vietnamese company database, hot-reloadable registry, normalization

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL (company master data)
- **Cache:** Redis (company lookup cache)

**API Endpoints:**
```yaml
POST /api/v1/companies
  - Register new Vietnamese company
  - Input: company_name, company_name_vi, tax_id, industry, region
  - Output: company_id, normalized_name

GET /api/v1/companies/{company_id}
  - Get Vietnamese company details
  - Output: company_profile, veri_business_context

GET /api/v1/companies/search
  - Search Vietnamese companies
  - Query: name, tax_id, region, industry
  - Output: companies[], total_count

PUT /api/v1/companies/{company_id}
  - Update Vietnamese company information
  - Input: updated_fields
  - Output: updated_company

DELETE /api/v1/companies/{company_id}
  - Deactivate Vietnamese company (soft delete)
  - Output: deactivated_at

POST /api/v1/companies/normalize
  - Normalize Vietnamese company name
  - Input: raw_company_name
  - Output: normalized_name, confidence_score
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
```

---

### 2.3 veri-compliance-engine

**Responsibility:** PDPL 2025 compliance workflows, wizards, policy generation

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL (compliance records)
- **Queue:** Celery + Redis (async compliance tasks)

**API Endpoints:**
```yaml
POST /api/v1/compliance/wizards/start
  - Start Vietnamese PDPL compliance wizard
  - Input: wizard_type, tenant_id, veri_business_context
  - Output: wizard_session_id, steps[]

GET /api/v1/compliance/wizards/{session_id}
  - Get wizard progress and current step
  - Output: current_step, completed_steps[], next_step

POST /api/v1/compliance/wizards/{session_id}/step
  - Submit wizard step data
  - Input: step_data, veri_business_context
  - Output: validation_result, next_step

POST /api/v1/compliance/policies/generate
  - Generate Vietnamese PDPL policy documents
  - Input: company_profile, policy_type, veri_regional_context
  - Output: policy_document_id, download_url

GET /api/v1/compliance/assessments/{tenant_id}
  - Get PDPL compliance assessment for Vietnamese business
  - Output: compliance_score, gaps[], recommendations[]

POST /api/v1/compliance/data-mapping
  - Create Vietnamese data mapping record
  - Input: data_flow, processing_purpose, legal_basis
  - Output: mapping_id, pdpl_compliance_analysis
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8004
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
```

---

### 2.4 veri-document-generator

**Responsibility:** Vietnamese PDPL document templates, PDF generation, bilingual support

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Template Engine:** Jinja2 (Vietnamese templates)
- **PDF Generator:** WeasyPrint or ReportLab
- **Storage:** MongoDB (template storage), S3 (generated documents)

**API Endpoints:**
```yaml
GET /api/v1/documents/templates
  - List Vietnamese PDPL document templates
  - Query: template_type, language
  - Output: templates[], categories[]

POST /api/v1/documents/generate
  - Generate Vietnamese PDPL document
  - Input: template_id, data, veri_business_context, language
  - Output: document_id, download_url, preview_url

GET /api/v1/documents/{document_id}
  - Get generated Vietnamese document
  - Output: document_metadata, download_url

POST /api/v1/documents/templates
  - Create custom Vietnamese document template
  - Input: template_content, variables[], metadata
  - Output: template_id

PUT /api/v1/documents/templates/{template_id}
  - Update Vietnamese document template
  - Input: updated_content
  - Output: template_version
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 libpangoft2-1.0-0 \
    fonts-noto-cjk fonts-noto-cjk-extra  # Vietnamese font support
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8005
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
```

---

### 2.5 veri-onboarding-service

**Responsibility:** Vietnamese cultural onboarding, business profile setup, AI-powered personalization

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL (onboarding sessions)
- **AI Integration:** Calls veri-vi-ai-classification for personalization

**API Endpoints:**
```yaml
POST /api/v1/onboarding/sessions
  - Create Vietnamese onboarding session
  - Input: tenant_id, language_preference
  - Output: session_id, initial_context

GET /api/v1/onboarding/sessions/{session_id}
  - Get onboarding session state
  - Output: current_step, progress, veri_cultural_context

POST /api/v1/onboarding/sessions/{session_id}/advance
  - Advance to next Vietnamese onboarding step
  - Input: step_data, user_preferences
  - Output: next_step, ai_recommendations

POST /api/v1/onboarding/sessions/{session_id}/complete
  - Complete Vietnamese business onboarding
  - Output: completion_summary, veri_business_context

GET /api/v1/onboarding/insights/{tenant_id}
  - Get AI-powered Vietnamese onboarding insights
  - Output: cultural_adaptation_score, recommendations[]
```

---

### 2.6 veri-business-intelligence

**Responsibility:** Vietnamese compliance analytics, dashboards, reporting

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** TimescaleDB (time-series metrics), PostgreSQL (aggregated data)
- **Analytics:** Pandas, NumPy
- **Caching:** Redis (dashboard cache)

**API Endpoints:**
```yaml
GET /api/v1/bi/dashboards/{tenant_id}
  - Get Vietnamese business intelligence dashboard
  - Query: date_range, metrics[]
  - Output: dashboard_data, charts_config

GET /api/v1/bi/compliance-metrics/{tenant_id}
  - Get PDPL compliance metrics for Vietnamese business
  - Output: compliance_score, trend_analysis, benchmarks

GET /api/v1/bi/regional-comparison
  - Compare Vietnamese regional business performance
  - Query: region, industry, metrics
  - Output: comparison_data, insights[]

POST /api/v1/bi/reports/generate
  - Generate Vietnamese compliance report
  - Input: report_type, tenant_id, date_range, language
  - Output: report_id, download_url

GET /api/v1/bi/predictions/{tenant_id}
  - Get AI-powered Vietnamese business predictions
  - Output: compliance_predictions, risk_forecasts
```

---

## 3. AI/ML Services

### 3.1 veri-vi-ai-classification

**Responsibility:** AI-powered Vietnamese data classification (structured + unstructured), PDPL categorization, legal basis detection, breach severity assessment

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **ML Libraries:** PyTorch, Transformers (Hugging Face), Scikit-learn
- **Models:** 
  - PhoBERT-base (Vietnamese BERT) for unstructured text
  - Pattern-based classifiers for structured data
  - Hybrid models for Vietnamese-specific formats
- **GPU:** CUDA 11.8+ support (optional, for PhoBERT)

**Classification Capabilities:**

**1. Structured Data Classification:**
- Database field name pattern recognition
- Data type inference from sample values
- Vietnamese-specific pattern matching (CMND/CCCD, phone, address)
- Schema-based sensitivity scoring
- Database column profiling

**2. Unstructured Data Classification:**
- Vietnamese legal/compliance text classification
- PDPL legal basis detection
- Data breach severity assessment
- Document categorization
- Named entity recognition integration

**API Endpoints:**
```yaml
# Structured Data Classification
POST /api/v1/classify/structured
  - Classify database fields and structured data
  - Input: 
      field_name: string
      data_type: string
      sample_values: array
      table_name: string (optional)
      schema_context: object (optional)
  - Output: 
      classification: string
      pdpl_category: "regular" | "sensitive"
      confidence: float
      vietnamese_type: string (e.g., "CMND/CCCD", "so_dien_thoai")
      sensitivity_score: float

POST /api/v1/classify/structured/batch
  - Batch classify multiple database fields
  - Input: fields[]
  - Output: classifications[]

# Unstructured Data Classification
POST /api/v1/classify/unstructured
  - Classify Vietnamese text with PDPL categories
  - Input: 
      text: string
      model_type: string
      language: "vi" | "en"
  - Output: 
      predicted_category: string
      confidence_score: float
      all_probabilities: object

POST /api/v1/classify/legal-basis
  - Classify Vietnamese legal basis for data processing
  - Input: processing_description: string
  - Output: 
      legal_basis_category: string
      article_reference: string
      confidence: float

POST /api/v1/classify/breach-severity
  - Classify Vietnamese data breach severity
  - Input: 
      breach_description: string
      data_types_affected: array
      number_of_individuals: integer
  - Output: 
      severity_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
      mps_notification_required: boolean
      notification_deadline: string
      fine_range: string

POST /api/v1/classify/batch
  - Batch classify Vietnamese texts (unstructured)
  - Input: texts[], model_type
  - Output: classifications[]

# Unified Classification Endpoint
POST /api/v1/classify
  - Universal classification endpoint
  - Input: 
      type: "structured" | "unstructured"
      data: object
      task: string
  - Output: classification_result

# Model Information
GET /api/v1/models/info
  - Get loaded Vietnamese AI model information
  - Output: 
      model_versions[]
      capabilities[]
      performance_metrics
      supported_vietnamese_patterns[]
```

**Vietnamese Pattern Library:**
```python
VIETNAMESE_PATTERNS = {
    "cmnd_cccd": r"\d{9,12}",  # 9-digit CMND or 12-digit CCCD
    "phone": r"(84|0)(3|5|7|8|9)\d{8}",  # Vietnamese mobile
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "address": r"(Phường|Quận|Huyện|Thành phố|Tỉnh)",
    "vietnamese_name": r"^[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ][a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+(\\s[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ][a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+)+$",
    "bank_account": r"\d{10,16}",
    "tax_code": r"\d{10}(-\d{3})?",  # Vietnamese MST
}
```

**Dockerfile (GPU-enabled):**
```dockerfile
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY models/ ./models/
COPY patterns/ ./patterns/  # Vietnamese pattern library
COPY . .
EXPOSE 8006
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006", "--workers", "2"]
```

**Resource Requirements:**
- **CPU:** 4-8 cores
- **Memory:** 8-16 GB RAM (16GB for production with both classifiers)
- **GPU:** NVIDIA GPU with 8GB+ VRAM (optional, for PhoBERT unstructured classification)
- **Storage:** 15GB (10GB PhoBERT models + 5GB pattern libraries)

**Scaling Strategy:**
- Horizontal scaling for high-volume classification
- GPU acceleration for unstructured text (PhoBERT)
- CPU-based for structured data (pattern matching)
- Redis caching for frequently classified patterns
- Batch processing for large datasets

---

### 3.2 veri-vi-nlp-processor

**Responsibility:** VnCoreNLP Vietnamese tokenization, POS tagging, NER

**Technology Stack:**
- **Language:** Python 3.11+ (wrapper), Java 11+ (VnCoreNLP)
- **Framework:** FastAPI
- **NLP Library:** VnCoreNLP
- **Cache:** Redis (processed text cache)

**API Endpoints:**
```yaml
POST /api/v1/nlp/tokenize
  - Tokenize Vietnamese text
  - Input: text
  - Output: tokens[], sentences[]

POST /api/v1/nlp/pos-tag
  - Vietnamese Part-of-Speech tagging
  - Input: text
  - Output: tagged_tokens[]

POST /api/v1/nlp/ner
  - Vietnamese Named Entity Recognition
  - Input: text
  - Output: entities[], entity_types[]

POST /api/v1/nlp/normalize
  - Normalize Vietnamese text (company names, personal names)
  - Input: raw_text
  - Output: normalized_text, normalization_rules_applied
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y default-jre
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY VnCoreNLP/ ./VnCoreNLP/
COPY . .
EXPOSE 8007
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"]
```

---

### 3.3 veri-ai-data-inventory

**Responsibility:** Data discovery and scanning, database schema analysis, data flow mapping, ROPA generation

**Vietnamese Text Support:** Generic data discovery service with **explicit Vietnamese text encoding support**:
- UTF-8 encoding for Vietnamese diacritics (á, ă, â, đ, ê, ô, ơ, ư)
- Vietnamese SQL column name handling (ho_ten, so_cmnd, dia_chi, etc.)
- Delegates Vietnamese pattern recognition to specialized services
- Preserves Vietnamese text integrity throughout scanning pipeline

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database Connectors:** SQLAlchemy (with UTF-8), PyMongo, Redis client
- **Cloud SDKs:** boto3 (AWS), azure-storage, google-cloud-storage
- **AI Integration:** Calls veri-vi-ai-classification for Vietnamese field classification
- **NLP Integration:** Calls veri-vi-nlp-processor for Vietnamese text preprocessing
- **Database:** PostgreSQL (data inventory records, UTF-8 encoding)
- **Queue:** Celery (async data discovery tasks)
- **Graph:** NetworkX (data flow mapping)

**Core Capabilities:**

**1. Database and System Scanning (Vietnamese-Aware):**
- PostgreSQL, MySQL, SQL Server, Oracle schema discovery
  * **UTF-8 encoding** for Vietnamese column names (ho_ten, so_cmnd, dia_chi)
  * Vietnamese diacritics preservation (á, ă, â, đ, ê, ô, ơ, ư)
  * Sample data extraction with encoding validation
- MongoDB collection and document structure analysis
  * UTF-8 text field handling for Vietnamese content
- Redis key pattern analysis
- Cloud storage metadata extraction (S3, Azure Blob, GCS)
  * Vietnamese filename support (UTF-8 paths)
- File system scanning (network shares, endpoints)
  * Vietnamese directory and file names

**2. Data Flow Mapping:**
- Source-to-destination relationship tracking
- Processing activity detection
- Cross-border transfer identification
- Data lineage graph generation

**3. ROPA (Record of Processing Activities) Generation:**
- Auto-generate Vietnamese PDPL-compliant data inventory
- MPS (Ministry of Public Security) reporting format
- Decree 13/2023/ND-CP compliance export

**API Endpoints:**
```yaml
# Data Source Discovery
POST /api/v1/data-inventory/scan
  - Scan data sources for Vietnamese business
  - Input: 
      tenant_id: string
      source_type: "database" | "cloud" | "filesystem" | "api"
      connection_config: object
      veri_business_context: object
  - Output: 
      scan_job_id: string
      estimated_time: integer

GET /api/v1/data-inventory/scans/{scan_job_id}
  - Get Vietnamese data scan job status
  - Output: 
      status: "pending" | "running" | "completed" | "failed"
      progress: integer
      discovered_assets: array
      errors: array

# Data Asset Management
GET /api/v1/data-inventory/{tenant_id}/assets
  - Get Vietnamese business data assets
  - Output: 
      data_sources[]
      total_fields: integer
      sensitive_fields: integer
      last_scan: datetime

GET /api/v1/data-inventory/{tenant_id}/assets/{asset_id}
  - Get specific data asset details
  - Output: 
      asset_metadata
      fields[]
      classifications[]  # From veri-vi-ai-classification
      data_flows[]

# Classification Integration
POST /api/v1/data-inventory/classify-fields
  - Classify database fields (calls veri-vi-ai-classification)
  - Input: 
      asset_id: string
      fields: array
  - Output: 
      classification_job_id: string

# Data Flow Mapping
POST /api/v1/data-inventory/map-flow
  - Map Vietnamese data flow between systems
  - Input: 
      source_asset_id: string
      destination_asset_id: string
      processing_activity: string
  - Output: 
      data_flow_id: string
      compliance_assessment: object

GET /api/v1/data-inventory/{tenant_id}/flows
  - Get Vietnamese data flow map
  - Output: 
      flows[]
      graph: object
      cross_border_transfers[]

# ROPA Generation
POST /api/v1/data-inventory/{tenant_id}/ropa/generate
  - Generate Vietnamese PDPL ROPA
  - Input: 
      format: "json" | "csv" | "pdf" | "mps_format"
      language: "vi" | "en"
  - Output: 
      ropa_document_id: string
      download_url: string
      mps_compliant: boolean

GET /api/v1/data-inventory/{tenant_id}/ropa/{ropa_id}
  - Get generated ROPA document
  - Output: 
      document_metadata
      download_url
      compliance_checklist[]
```

**Integration with veri-vi-ai-classification:**
```python
# Vietnamese data discovery and classification flow
1. veri-ai-data-inventory scans PostgreSQL database (UTF-8 connection)
2. Discovers table "khach_hang" with Vietnamese fields:
   - Field: "ho_ten" (VARCHAR) - Vietnamese name with diacritics
   - Field: "so_cmnd" (VARCHAR(12)) - Vietnamese national ID
   - Field: "email" (VARCHAR)
   - Field: "so_dien_thoai" (VARCHAR) - Vietnamese phone
   
3. Calls veri-vi-nlp-processor for Vietnamese text preprocessing (if needed):
   POST http://veri-vi-nlp-processor:8007/api/v1/preprocess
   {
     "text": "Nguyễn Văn A",
     "language": "vi"
   }

4. Calls veri-vi-ai-classification for each field:
   POST http://veri-vi-ai-classification:8006/api/v1/classify/structured
   {
     "field_name": "so_cmnd",
     "data_type": "VARCHAR(12)",
     "sample_values": ["001234567890", "079123456789"]
   }
   
5. Receives Vietnamese classification: 
   {
     "classification": "national_id",
     "pdpl_category": "sensitive_data",
     "vietnamese_type": "CMND/CCCD",
     "confidence": 0.98
   }
   
6. Stores classification in inventory database (UTF-8 encoding)
7. Generates Vietnamese ROPA with classified data
```

**Vietnamese Text Encoding Configuration:**
```python
# Database connection with UTF-8
DATABASE_URL = "postgresql://user:pass@host/db?client_encoding=utf8"

# SQLAlchemy engine configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": "-c client_encoding=utf8"
    },
    pool_pre_ping=True
)

# MongoDB UTF-8 handling
mongo_client = MongoClient(
    MONGO_URL,
    unicode_decode_error_handler='strict'  # Fail on invalid UTF-8
)

# File system scanning with UTF-8
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Sample data extraction preserving Vietnamese diacritics
def extract_sample_data(table_name, column_name, limit=100):
    """Extract sample data with Vietnamese text preservation"""
    query = text(f"SELECT {column_name} FROM {table_name} LIMIT :limit")
    result = conn.execute(query, {"limit": limit})
    samples = [row[0] for row in result if row[0]]
    
    # Validate UTF-8 encoding
    for sample in samples:
        try:
            sample.encode('utf-8').decode('utf-8')
        except UnicodeError:
            logger.warning(f"Invalid UTF-8 in {table_name}.{column_name}: {sample}")
    
    return samples
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

# Set UTF-8 locale for Vietnamese text support
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=utf-8

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    default-libmysqlclient-dev \
    build-essential \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Generate UTF-8 locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
```

**Environment Variables:**
```bash
# Database connections (UTF-8 enforced)
DATABASE_URL=postgresql://user:pass@postgres:5432/verisyntra?client_encoding=utf8
MONGODB_URL=mongodb://mongo:27017/verisyntra
REDIS_URL=redis://redis:6379/2

# Vietnamese text encoding
PYTHONIOENCODING=utf-8
LANG=C.UTF-8
LC_ALL=C.UTF-8

# Service integration
CLASSIFICATION_SERVICE_URL=http://veri-vi-ai-classification:8006
NLP_SERVICE_URL=http://veri-vi-nlp-processor:8007

# Scanning configuration
MAX_SAMPLE_SIZE=1000
SCAN_TIMEOUT=3600
CELERY_BROKER_URL=redis://redis:6379/3
```

**Vietnamese Text Handling Best Practices:**
```python
# [OK] Correct approach for Vietnamese data
class VietnameseDataScanner:
    """Scanner with Vietnamese text support"""
    
    def __init__(self):
        self.encoding = 'utf-8'
        self.diacritics = ['á', 'à', 'ả', 'ã', 'ạ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ',
                          'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'đ', 'é', 'è', 'ẻ', 'ẽ',
                          'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'í', 'ì', 'ỉ', 'ĩ',
                          'ị', 'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ',
                          'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'ú', 'ù', 'ủ', 'ũ',
                          'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ']
    
    def validate_vietnamese_text(self, text: str) -> bool:
        """Validate Vietnamese text encoding"""
        try:
            # Ensure text can be encoded/decoded as UTF-8
            text.encode('utf-8').decode('utf-8')
            return True
        except UnicodeError:
            return False
    
    def scan_database_with_vietnamese(self, connection_string: str):
        """Scan database with Vietnamese column name support"""
        # Force UTF-8 encoding
        if 'postgresql' in connection_string:
            connection_string += '?client_encoding=utf8'
        
        engine = create_engine(connection_string)
        
        # Get Vietnamese column names
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
            """))
            
            for row in result:
                table_name = row[0]
                column_name = row[1]  # May be Vietnamese: ho_ten, dia_chi, etc.
                
                # Validate UTF-8
                if not self.validate_vietnamese_text(column_name):
                    logger.error(f"Invalid UTF-8 in column: {table_name}.{column_name}")
                    continue
                
                # Extract sample data (with Vietnamese content)
                samples = self.extract_samples(conn, table_name, column_name)
                
                # Delegate to Vietnamese AI for classification
                classification = self.classify_vietnamese_field(column_name, samples)
```

**Resource Requirements:**
- **CPU:** 2-4 cores
- **Memory:** 4-8 GB RAM
- **Storage:** 20GB for scan results and metadata
- **Network:** High bandwidth for database/cloud scanning

**Scaling Strategy:**
- Celery workers for parallel scanning
- Distributed task queue for large enterprise scans
- Redis caching for scan results
- Incremental scanning for updated detections

---

## 4. Data & Integration Services

### 4.1 veri-data-sync-service

**Responsibility:** ERP/HRM/Cloud system connectors, data synchronization

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Connectors:** Custom adapters for Vietnamese ERP/HRM systems
- **Queue:** Celery + Redis (async sync tasks)

**Supported Systems:**
- Vietnamese ERP: MISA, Bravo, Fast, Bizzi
- Vietnamese HRM: Base.vn, 1Office, Timviec365
- Cloud: Google Drive, Dropbox, OneDrive
- Databases: MySQL, PostgreSQL, SQL Server

**API Endpoints:**
```yaml
POST /api/v1/connectors/configure
  - Configure Vietnamese system connector
  - Input: connector_type, credentials, tenant_id
  - Output: connector_id, connection_test_result

GET /api/v1/connectors/{connector_id}/test
  - Test Vietnamese system connection
  - Output: connection_status, available_endpoints

POST /api/v1/sync/start
  - Start data synchronization job
  - Input: connector_id, sync_config
  - Output: sync_job_id

GET /api/v1/sync/jobs/{job_id}
  - Get Vietnamese sync job status
  - Output: status, records_synced, errors[]

GET /api/v1/connectors/{tenant_id}
  - List configured Vietnamese connectors
  - Output: connectors[], health_status[]
```

---

### 4.2 veri-notification-service

**Responsibility:** Multi-channel notifications (email, SMS, webhooks) for Vietnamese businesses

**Technology Stack:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Email:** SMTP (Vietnamese providers), SendGrid
- **SMS:** Vietnamese carriers (Viettel, VinaPhone, MobiFone)
- **Queue:** Celery + Redis

**API Endpoints:**
```yaml
POST /api/v1/notifications/send
  - Send Vietnamese notification
  - Input: channel, recipient, message, language, template_id
  - Output: notification_id, delivery_status

GET /api/v1/notifications/{notification_id}
  - Get Vietnamese notification status
  - Output: delivery_status, delivered_at, read_at

POST /api/v1/notifications/templates
  - Create Vietnamese notification template
  - Input: template_type, content_vi, content_en
  - Output: template_id

GET /api/v1/notifications/history/{tenant_id}
  - Get Vietnamese notification history
  - Output: notifications[], delivery_stats
```

---

## 5. Infrastructure Services

### 5.1 veri-config-server

**Responsibility:** Centralized configuration management for all microservices

**Technology Stack:**
- **Technology:** Spring Cloud Config Server or Consul
- **Storage:** Git repository or Consul KV store

**Configuration Example:**
```yaml
# veri-auth-service-production.yml
database:
  url: postgresql://veri-postgres:5432/veri_auth
  max_connections: 20

jwt:
  secret_key: ${JWT_SECRET}
  algorithm: HS256
  expire_minutes: 30

vietnamese:
  timezone: Asia/Ho_Chi_Minh
  default_language: vi
  regional_support:
    - north
    - central
    - south
```

---

### 5.2 veri-service-discovery

**Responsibility:** Service registration and discovery (Consul or Eureka)

**Technology Stack:**
- **Technology:** Consul or Netflix Eureka
- **DNS:** Kubernetes Internal DNS (primary)

**Service Registry Example:**
```json
{
  "service": "veri-cultural-intelligence",
  "id": "veri-cultural-intelligence-1",
  "address": "veri-cultural-intelligence",
  "port": 8002,
  "tags": ["python", "fastapi", "vietnamese-cultural"],
  "meta": {
    "version": "1.0.0",
    "region": "vietnam",
    "language_support": "vi,en"
  },
  "checks": [
    {
      "http": "http://veri-cultural-intelligence:8002/health",
      "interval": "10s"
    }
  ]
}
```

---

## Service Communication Patterns

### Synchronous Communication (REST)
- Client -> API Gateway -> Service
- Service -> Service (for real-time data)

### Asynchronous Communication (Message Queue)
- Event-driven workflows (RabbitMQ/Kafka)
- Long-running tasks (Celery + Redis)
- Data synchronization pipelines

### Service Mesh (Istio/Linkerd)
- Service-to-service mTLS
- Traffic management
- Circuit breakers and retries

---

## Next Documents

- **02_Docker_Implementation_Guide.md:** Docker Compose and Dockerfile examples
- **03_Database_Migration_Strategy.md:** Multi-tenant database architecture
- **04_API_Gateway_Design.md:** Kong Gateway configuration (DB-less, PostgreSQL, Ingress Controller modes)
- **05_Kubernetes_Deployment_Guide.md:** Helm charts and K8s manifests

---

**Document Status:** Draft v1.0  
**Last Updated:** November 1, 2025  
**Next Review:** Phase 1 completion
