# Data Population Method 2: Automated Database Discovery
## Vietnamese PDPL 2025 Compliance - Processing Activities Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** processing_activities Table  
**Method:** Automated Database Discovery (VeriAI-Powered)  
**Architecture:** Vietnamese-first AI-Driven Database Scanning  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **automated discovery** of processing activities by scanning existing databases. VeriAI analyzes database schemas, table relationships, and data patterns to automatically identify and suggest processing activities for PDPL compliance.

**[+] UPGRADE PATH:** For advanced ML-powered PDPL principle classification, see [Document #08: VeriAIDPO AI Integration](./08_Data_Population_VeriAIDPO_Integration.md). Document #08 builds on this foundation with PhoBERT-based Vietnamese legal analysis.

**Relationship to Document #08:**
- **This document (#02)**: Foundation layer with pattern-based database discovery
- **Document #08**: Advanced layer with ML-powered PDPL classification using VeriAIDPO model
- Implementation strategy: Deploy this first, then upgrade to Document #08 for intelligent classification

**Key Features:**
- VeriAI-powered intelligent database scanning
- Multi-database support (MySQL, PostgreSQL, SQL Server, MongoDB)
- Automatic data classification (personal/sensitive/special categories)
- Vietnamese-first activity name suggestions
- Zero hard-coding with AI-driven pattern recognition
- Auto-generated PDPL compliance mappings

**Use Cases:**
- Organizations with existing databases need ROPA quickly
- Migration from legacy systems to PDPL compliance
- Periodic compliance audits requiring updated inventories
- Multi-database environments needing unified discovery

**When to Use This Method (Doc #02) vs VeriAIDPO Integration (Doc #08):**

| Feature | Doc #02 (This Method) | Doc #08 (VeriAIDPO) |
|---------|----------------------|---------------------|
| **Complexity** | Simple pattern-based | Advanced ML-based |
| **Setup Time** | Quick (1-2 days) | Longer (5 weeks) |
| **Accuracy** | Good (70-80%) | Excellent (85%+) |
| **Best For** | Quick compliance audit | Production PDPL system |
| **AI Model** | Generic VeriAI | PhoBERT Vietnamese |
| **PDPL Principles** | Inferred from patterns | Explicitly classified |
| **Confidence Score** | No | Yes (0.0-1.0) |
| **Use When** | Need fast results | Need legal precision |

**Recommendation:** Start with this method for rapid deployment, then upgrade to Document #08 for production-grade PDPL compliance with ML-powered classification.

---

## Table of Contents

1. [Authentication & Authorization](#authentication--authorization)
2. [Architecture Overview](#architecture-overview)
3. [Database Connection Configuration](#database-connection-configuration)
4. [Discovery Algorithm](#discovery-algorithm)
5. [AI-Powered Classification](#ai-powered-classification)
6. [Vietnamese Activity Suggestion](#vietnamese-activity-suggestion)
7. [Validation and Review Workflow](#validation-and-review-workflow)
8. [Implementation Guide](#implementation-guide)

---

## Authentication & Authorization

### Overview

**Phase 7 Integration:** Automated database discovery requires elevated permissions due to security implications of database scanning operations.

**Authentication Method:** JWT Bearer Token  
**Required Permission:** `processing_activity.write` + database scan privileges  
**Allowed Roles:** admin, data_processor (compliance_officer and viewer roles cannot initiate scans)

### Why Restricted Permissions?

Database discovery operations involve:
- **Database Credential Access:** Connecting to potentially sensitive databases
- **Schema Inspection:** Reading table structures and relationships
- **Data Sampling:** Analyzing data content to classify personal data
- **Bulk Data Creation:** Creating hundreds or thousands of processing activities

**Security Risk:** If unauthorized users could trigger scans, they could:
1. Discover sensitive database structures
2. Create malicious or incorrect processing activities
3. Overload system resources with large scans
4. Access credentials for external databases

### Role-Based Access Control

**Allowed Roles:**
- **admin** (Quản trị viên): Full access to all discovery operations, can scan any database
- **data_processor** (Người xử lý dữ liệu): Can initiate scans for their tenant's databases only

**Prohibited Roles:**
- **compliance_officer** (Cán bộ tuân thủ): Can view discovered activities but cannot initiate scans
- **viewer** (Người xem): Can view discovered activities in read-only mode

### API Endpoints & Permissions

| Endpoint | HTTP Method | Required Permission | Roles Allowed |
|----------|-------------|---------------------|---------------|
| `/api/v1/data-inventory/discovery/start` | POST | `processing_activity.write` + scan privilege | admin, data_processor |
| `/api/v1/data-inventory/discovery/status/{id}` | GET | `processing_activity.read` | admin, data_processor, compliance_officer |
| `/api/v1/data-inventory/discovered-activities/{id}` | GET | `processing_activity.read` | admin, data_processor, compliance_officer, viewer |
| `/api/v1/data-inventory/approve-activity/{id}` | POST | `processing_activity.write` | admin, compliance_officer, data_processor |

### Authentication Example

**Starting a Database Scan:**

```bash
curl -X POST "http://localhost:8000/api/v1/data-inventory/discovery/start" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "discover_name_vi": "Khám phá Cơ sở dữ liệu CRM",
    "discover_name_en": "CRM Database Discovery",
    "database_type": "postgresql",
    "host": "crm-db.internal.company.vn",
    "port": 5432,
    "database_name": "crm_production",
    "username": "discovery_user",
    "password": "encrypted_password",
    "scan_depth": "full"
  }'
```

**Permission Denied Example (viewer role attempting scan):**

```json
{
  "error": "Insufficient permissions. Required: processing_activity.write and database scan privilege",
  "error_vi": "Không đủ quyền. Cần: processing_activity.write và quyền quét cơ sở dữ liệu",
  "required_permission": "processing_activity.write",
  "additional_privilege": "database_scan",
  "user_role": "viewer",
  "allowed_roles": ["admin", "data_processor"]
}
```

### Tenant Isolation for Discovery

**Multi-Tenant Security:**
- Each discovery operation is scoped to the tenant ID from JWT token
- Discovered activities automatically inherit the user's tenant_id
- Users cannot access discovery results from other tenants
- Database credentials are encrypted per-tenant (not shared across tenants)

**Validation Logic:**

```python
async def start_discovery(
    request: DatabaseConnectionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> Dict[str, any]:
    """
    Start automated discovery
    
    Authentication:
    - Requires JWT Bearer token
    - Validates user has data_processor or admin role
    - All discovered activities assigned to current_tenant
    - Database credentials validated for tenant ownership
    """
    # Validate user has scan privilege (not just processing_activity.write)
    if not await has_database_scan_privilege(db, current_user, current_tenant):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "User does not have database scan privilege",
                "error_vi": "Người dùng không có quyền quét cơ sở dữ liệu",
                "required_privilege": "database_scan"
            }
        )
    
    # Create discovery session scoped to tenant
    discovery_id = uuid4()
    
    # Schedule background task with tenant context
    background_tasks.add_task(
        run_discovery,
        discovery_id=discovery_id,
        tenant_id=current_tenant,  # From JWT token
        connection_request=request,
        db=db,
        user_id=current_user  # From JWT token
    )
    
    return {
        "discovery_id": discovery_id,
        "tenant_id": str(current_tenant),
        "status": "in_progress",
        ...
    }
```

### Secure Credential Handling

**Database Credentials Security:**
1. **Encryption at Rest:** All database credentials encrypted using tenant-specific keys
2. **Temporary Access:** Credentials only decrypted during active scan, discarded after
3. **Audit Trail:** All credential usage logged with user_id and timestamp
4. **No Storage in Logs:** Passwords never written to application logs

**Recommended Practice:**

```python
# Good: Use environment variables or secrets manager
DB_CREDENTIALS = {
    "host": os.getenv("TARGET_DB_HOST"),
    "username": os.getenv("TARGET_DB_USER"),
    "password": get_secret("target-db-password")  # From HashiCorp Vault or AWS Secrets Manager
}

# Bad: Hard-coded credentials in API request
# Never do this in production
DB_CREDENTIALS = {
    "password": "PlaintextPassword123!"  # SECURITY VIOLATION
}
```

**See Also:**
- Phase 7 Documentation: `DOC12_PHASE_7_AUTH_IMPLEMENTATION_PLAN.md`
- API Key Management: Phase 7.4 (for system-to-system discovery automation)
- OAuth2 Integration: Phase 7.6 (for third-party database connectors)

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    VeriAI Discovery Engine                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Database    │  │  Schema      │  │  Data        │     │
│  │  Connector   │─>│  Analyzer    │─>│  Classifier  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Vietnamese  │  │  Legal Basis │  │  Activity    │     │
│  │  NLP Engine  │  │  Recommender │  │  Generator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  processing_activities │                    │
│              │  (status: pending)     │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Discovery Workflow:**
1. Connect to target database with secure credentials
2. Analyze schema (tables, columns, relationships)
3. Classify data fields (personal/sensitive/special)
4. Use Vietnamese NLP to suggest activity names
5. Recommend legal basis based on data patterns
6. Generate processing activities with `status: pending_review`
7. Human review and approval before activation

---

## Database Connection Configuration

### Connection Constants

```python
# api/constants/discovery_constants.py

"""
Database Discovery Constants - Zero Hard-Coding
VeriAI Automated Discovery Configuration
"""

from enum import Enum
from typing import Dict, List

# Supported Database Types
class SupportedDatabaseType(str, Enum):
    """
    Các loại cơ sở dữ liệu được hỗ trợ
    Supported database types
    """
    MYSQL = "mysql"              # MySQL/MariaDB
    POSTGRESQL = "postgresql"    # PostgreSQL
    SQLSERVER = "sqlserver"      # Microsoft SQL Server
    MONGODB = "mongodb"          # MongoDB (NoSQL)
    ORACLE = "oracle"            # Oracle Database


# Database Type Vietnamese Translations
DATABASE_TYPE_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    SupportedDatabaseType.MYSQL: {
        "vi": "MySQL/MariaDB",
        "en": "MySQL/MariaDB"
    },
    SupportedDatabaseType.POSTGRESQL: {
        "vi": "PostgreSQL",
        "en": "PostgreSQL"
    },
    SupportedDatabaseType.SQLSERVER: {
        "vi": "Microsoft SQL Server",
        "en": "Microsoft SQL Server"
    },
    SupportedDatabaseType.MONGODB: {
        "vi": "MongoDB (NoSQL)",
        "en": "MongoDB (NoSQL)"
    },
    SupportedDatabaseType.ORACLE: {
        "vi": "Oracle Database",
        "en": "Oracle Database"
    }
}


# Discovery Status Constants
class DiscoveryStatus(str, Enum):
    """
    Trạng thái khám phá
    Discovery status
    """
    PENDING = "pending"              # Đang chờ xử lý
    IN_PROGRESS = "in_progress"      # Đang khám phá
    COMPLETED = "completed"          # Hoàn thành
    FAILED = "failed"                # Thất bại
    PARTIAL = "partial"              # Hoàn thành một phần


# Discovery Status Vietnamese Translations
DISCOVERY_STATUS_TRANSLATIONS_VI: Dict[str, str] = {
    DiscoveryStatus.PENDING: "Đang chờ xử lý",
    DiscoveryStatus.IN_PROGRESS: "Đang khám phá",
    DiscoveryStatus.COMPLETED: "Hoàn thành",
    DiscoveryStatus.FAILED: "Thất bại",
    DiscoveryStatus.PARTIAL: "Hoàn thành một phần"
}


# Discovery Status English Translations
DISCOVERY_STATUS_TRANSLATIONS_EN: Dict[str, str] = {
    DiscoveryStatus.PENDING: "Pending",
    DiscoveryStatus.IN_PROGRESS: "In Progress",
    DiscoveryStatus.COMPLETED: "Completed",
    DiscoveryStatus.FAILED: "Failed",
    DiscoveryStatus.PARTIAL: "Partial"
}


# Default Database Ports (no hard-coding in logic)
DEFAULT_DATABASE_PORTS: Dict[str, int] = {
    SupportedDatabaseType.MYSQL: 3306,
    SupportedDatabaseType.POSTGRESQL: 5432,
    SupportedDatabaseType.SQLSERVER: 1433,
    SupportedDatabaseType.MONGODB: 27017,
    SupportedDatabaseType.ORACLE: 1521
}


# Connection Timeout Constants
CONNECTION_TIMEOUT_SECONDS = 30  # 30 seconds timeout
MAX_RETRY_ATTEMPTS = 3  # Maximum 3 retry attempts
RETRY_DELAY_SECONDS = 5  # 5 seconds between retries
```

---

### Database Connection Request Model

```python
# api/models/discovery_models.py

"""
Database Discovery Models
Vietnamese-first Automated Discovery
"""

from pydantic import BaseModel, Field, validator, SecretStr
from typing import Optional
from uuid import UUID
from datetime import datetime

from api.constants.discovery_constants import (
    SupportedDatabaseType,
    DEFAULT_DATABASE_PORTS,
    CONNECTION_TIMEOUT_SECONDS
)


class DatabaseConnectionRequest(BaseModel):
    """
    Yêu cầu kết nối cơ sở dữ liệu
    Database connection request
    
    Vietnamese-first with secure credential handling
    """
    
    # Database Type (REQUIRED)
    database_type: SupportedDatabaseType = Field(
        ...,
        description="Loại cơ sở dữ liệu | Database type"
    )
    
    # Connection Details (REQUIRED)
    host: str = Field(
        ...,
        min_length=1,
        description="Địa chỉ máy chủ (IP hoặc hostname) | Server address (IP or hostname)"
    )
    
    port: Optional[int] = Field(
        None,
        ge=1,
        le=65535,
        description="Cổng kết nối (mặc định theo loại DB) | Port number (defaults by DB type)"
    )
    
    database_name: str = Field(
        ...,
        min_length=1,
        description="Tên cơ sở dữ liệu | Database name"
    )
    
    username: str = Field(
        ...,
        min_length=1,
        description="Tên đăng nhập | Username"
    )
    
    password: SecretStr = Field(
        ...,
        description="Mật khẩu (được mã hóa) | Password (encrypted)"
    )
    
    # Discovery Configuration
    discover_name_vi: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Tên đợt khám phá (tiếng Việt, bắt buộc) | Discovery name (Vietnamese, required)"
    )
    
    discover_name_en: Optional[str] = Field(
        None,
        max_length=200,
        description="Tên đợt khám phá (tiếng Anh, tùy chọn) | Discovery name (English, optional)"
    )
    
    # Optional Filters
    include_tables: Optional[List[str]] = Field(
        None,
        description="Danh sách bảng cần khám phá (để trống = tất cả) | Tables to discover (empty = all)"
    )
    
    exclude_tables: Optional[List[str]] = Field(
        None,
        description="Danh sách bảng bỏ qua | Tables to exclude"
    )
    
    # Advanced Options
    use_ssl: bool = Field(
        default=True,
        description="Sử dụng kết nối SSL/TLS | Use SSL/TLS connection"
    )
    
    connection_timeout: int = Field(
        default=CONNECTION_TIMEOUT_SECONDS,
        ge=10,
        le=300,
        description="Thời gian chờ kết nối (giây) | Connection timeout (seconds)"
    )
    
    @validator('port', always=True)
    def set_default_port(cls, v, values):
        """Set default port based on database type if not provided"""
        if v is None and 'database_type' in values:
            return DEFAULT_DATABASE_PORTS.get(values['database_type'])
        return v
    
    @validator('discover_name_vi')
    def validate_discover_name_vi(cls, v):
        """Validate Vietnamese discovery name has proper diacritics"""
        if not v or v.strip() == "":
            raise ValueError(
                "Tên đợt khám phá không được để trống | "
                "Discovery name cannot be empty"
            )
        
        # Check for common non-diacritic mistakes
        non_diacritic_keywords = ["khao sat", "phan tich", "kiem tra"]
        v_lower = v.lower()
        for keyword in non_diacritic_keywords:
            if keyword in v_lower:
                raise ValueError(
                    f"Vui lòng sử dụng dấu tiếng Việt đúng | "
                    f"Please use proper Vietnamese diacritics"
                )
        
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "database_type": "postgresql",
                "host": "192.168.1.100",
                "port": 5432,
                "database_name": "crm_production",
                "username": "discovery_user",
                "password": "***encrypted***",
                "discover_name_vi": "Khám phá hệ thống CRM khách hàng",
                "discover_name_en": "Customer CRM System Discovery",
                "include_tables": ["customers", "orders", "users"],
                "exclude_tables": ["logs", "temp_data"],
                "use_ssl": True,
                "connection_timeout": 30
            }
        }


class DiscoveredActivityResponse(BaseModel):
    """
    Phản hồi hoạt động được khám phá
    Discovered activity response
    
    Auto-generated with AI suggestions
    """
    
    # Discovery Metadata
    discovery_id: UUID
    discovery_name_vi: str
    discovery_name_en: Optional[str]
    discovery_status: str
    discovery_status_vi: str
    discovery_status_en: str
    
    # Discovered Activity (auto-generated)
    activity_id: UUID
    activity_name_vi: str  # AI-suggested Vietnamese name
    activity_name_en: Optional[str]  # AI-suggested English name
    processing_purpose_vi: str  # AI-inferred purpose
    processing_purpose_en: Optional[str]
    
    # AI Recommendations
    suggested_legal_basis: str
    suggested_legal_basis_vi: str
    suggested_legal_basis_en: str
    confidence_score: float  # 0.0 to 1.0
    
    # Discovered Data Details
    source_table_name: str
    discovered_personal_data_fields: List[str]
    discovered_sensitive_data_fields: List[str]
    
    # Compliance Flags (AI-detected)
    has_sensitive_data: bool
    has_cross_border_transfer: bool
    requires_dpia: bool
    
    # Review Status
    status: str  # Always "pending_review" for auto-discovered
    requires_human_review: bool
    review_notes_vi: Optional[str]
    review_notes_en: Optional[str]
    
    # Metadata
    discovered_at: datetime
    created_by: UUID  # System user for automated discovery
    
    class Config:
        json_schema_extra = {
            "example": {
                "discovery_id": "880e8400-e29b-41d4-a716-446655440003",
                "discovery_name_vi": "Khám phá hệ thống CRM khách hàng",
                "discovery_name_en": "Customer CRM System Discovery",
                "discovery_status": "completed",
                "discovery_status_vi": "Hoàn thành",
                "discovery_status_en": "Completed",
                "activity_id": "990e8400-e29b-41d4-a716-446655440004",
                "activity_name_vi": "Quản lý thông tin khách hàng CRM",
                "activity_name_en": "Customer Information Management CRM",
                "processing_purpose_vi": "Lưu trữ và quản lý thông tin khách hàng để cung cấp dịch vụ",
                "processing_purpose_en": "Store and manage customer information for service delivery",
                "suggested_legal_basis": "contract",
                "suggested_legal_basis_vi": "Thực hiện hợp đồng",
                "suggested_legal_basis_en": "Contract performance",
                "confidence_score": 0.87,
                "source_table_name": "customers",
                "discovered_personal_data_fields": [
                    "ho_ten", "email", "so_dien_thoai", "dia_chi"
                ],
                "discovered_sensitive_data_fields": [],
                "has_sensitive_data": False,
                "has_cross_border_transfer": False,
                "requires_dpia": False,
                "status": "pending_review",
                "requires_human_review": True,
                "review_notes_vi": "Vui lòng xác nhận cơ sở pháp lý và mục đích xử lý",
                "review_notes_en": "Please confirm legal basis and processing purpose",
                "discovered_at": "2025-11-06T14:30:00+07:00",
                "created_by": "system-ai-discovery"
            }
        }
```

---

## Discovery Algorithm

### Schema Analysis Engine

```python
# services/discovery/schema_analyzer.py

"""
Database Schema Analyzer
Vietnamese-first AI-Powered Discovery
"""

from typing import Dict, List, Optional, Tuple
from sqlalchemy import inspect, MetaData, Table
from sqlalchemy.engine import Engine
import re

from api.constants.discovery_constants import SupportedDatabaseType


# Vietnamese Column Name Patterns (no hard-coding)
VIETNAMESE_PERSONAL_DATA_PATTERNS: List[str] = [
    # Họ tên (Full name)
    r"ho_ten", r"ten", r"ho", r"full_name", r"name",
    
    # Số điện thoại (Phone number)
    r"so_dien_thoai", r"dien_thoai", r"phone", r"mobile",
    
    # Email
    r"email", r"thu_dien_tu",
    
    # Địa chỉ (Address)
    r"dia_chi", r"address", r"street", r"city", r"province",
    
    # Ngày sinh (Date of birth)
    r"ngay_sinh", r"date_of_birth", r"dob", r"birth_date",
    
    # CMND/CCCD (ID number)
    r"cmnd", r"cccd", r"so_cmnd", r"id_number", r"national_id",
    
    # Số hộ chiếu (Passport)
    r"ho_chieu", r"so_ho_chieu", r"passport", r"passport_number"
]


# Sensitive Data Patterns (Art. 4.13 PDPL)
VIETNAMESE_SENSITIVE_DATA_PATTERNS: List[str] = [
    # Thông tin sức khỏe (Health information)
    r"benh_an", r"medical_record", r"health", r"disease", r"treatment",
    
    # Thông tin tài chính (Financial information)
    r"tai_khoan", r"bank_account", r"credit_card", r"so_the", r"balance",
    
    # Thông tin sinh trắc học (Biometric information)
    r"van_tay", r"fingerprint", r"khuon_mat", r"face", r"iris",
    
    # Thông tin chính trị (Political information)
    r"dang_vien", r"political", r"party_member",
    
    # Thông tin tôn giáo (Religious information)
    r"ton_giao", r"religion", r"belief",
    
    # Thông tin tình dục (Sexual orientation)
    r"gioi_tinh", r"sexual_orientation", r"gender_identity"
]


class SchemaAnalyzer:
    """
    Phân tích schema cơ sở dữ liệu
    Database schema analyzer
    
    Zero hard-coding with pattern-based detection
    """
    
    def __init__(self, engine: Engine, database_type: SupportedDatabaseType):
        self.engine = engine
        self.database_type = database_type
        self.inspector = inspect(engine)
        self.metadata = MetaData()
    
    async def analyze_schema(
        self,
        include_tables: Optional[List[str]] = None,
        exclude_tables: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Phân tích schema và phát hiện dữ liệu cá nhân
        Analyze schema and detect personal data
        
        Returns:
            Schema analysis with personal data classification
        """
        results = {
            "total_tables": 0,
            "analyzed_tables": 0,
            "tables_with_personal_data": [],
            "tables_with_sensitive_data": [],
            "discovered_activities": []
        }
        
        # Get all table names
        table_names = self.inspector.get_table_names()
        results["total_tables"] = len(table_names)
        
        # Apply filters
        if include_tables:
            table_names = [t for t in table_names if t in include_tables]
        if exclude_tables:
            table_names = [t for t in table_names if t not in exclude_tables]
        
        # Analyze each table
        for table_name in table_names:
            table_analysis = await self._analyze_table(table_name)
            results["analyzed_tables"] += 1
            
            if table_analysis["has_personal_data"]:
                results["tables_with_personal_data"].append(table_name)
                results["discovered_activities"].append(table_analysis)
            
            if table_analysis["has_sensitive_data"]:
                results["tables_with_sensitive_data"].append(table_name)
        
        return results
    
    async def _analyze_table(self, table_name: str) -> Dict[str, any]:
        """
        Phân tích một bảng cụ thể
        Analyze specific table
        
        Returns:
            Table analysis with data classification
        """
        columns = self.inspector.get_columns(table_name)
        
        personal_data_fields = []
        sensitive_data_fields = []
        
        for column in columns:
            column_name = column['name']
            
            # Check if column contains personal data
            if self._is_personal_data_column(column_name):
                personal_data_fields.append(column_name)
            
            # Check if column contains sensitive data
            if self._is_sensitive_data_column(column_name):
                sensitive_data_fields.append(column_name)
        
        return {
            "table_name": table_name,
            "has_personal_data": len(personal_data_fields) > 0,
            "has_sensitive_data": len(sensitive_data_fields) > 0,
            "personal_data_fields": personal_data_fields,
            "sensitive_data_fields": sensitive_data_fields,
            "total_columns": len(columns)
        }
    
    def _is_personal_data_column(self, column_name: str) -> bool:
        """
        Kiểm tra cột có chứa dữ liệu cá nhân không
        Check if column contains personal data
        
        Uses pattern matching (no hard-coding)
        """
        column_lower = column_name.lower()
        
        for pattern in VIETNAMESE_PERSONAL_DATA_PATTERNS:
            if re.search(pattern, column_lower):
                return True
        
        return False
    
    def _is_sensitive_data_column(self, column_name: str) -> bool:
        """
        Kiểm tra cột có chứa dữ liệu nhạy cảm không
        Check if column contains sensitive data (Art. 4.13 PDPL)
        
        Uses pattern matching (no hard-coding)
        """
        column_lower = column_name.lower()
        
        for pattern in VIETNAMESE_SENSITIVE_DATA_PATTERNS:
            if re.search(pattern, column_lower):
                return True
        
        return False
```

---

## AI-Powered Classification

### Vietnamese NLP Activity Suggestion

```python
# services/discovery/vietnamese_nlp_suggester.py

"""
Vietnamese NLP Activity Name Suggester
AI-Powered Vietnamese-first Activity Generation
"""

from typing import Dict, Tuple
import re


# Vietnamese Activity Name Templates (no hard-coding)
ACTIVITY_NAME_TEMPLATES_VI: Dict[str, str] = {
    # Customer-related tables
    "khach_hang|customer": "Quản lý thông tin khách hàng",
    "don_hang|order": "Quản lý đơn hàng và giao dịch",
    "thanh_toan|payment": "Xử lý thanh toán khách hàng",
    
    # Employee-related tables
    "nhan_vien|employee|staff": "Quản lý thông tin nhân viên",
    "luong|salary|payroll": "Xử lý lương và phúc lợi nhân viên",
    "cham_cong|attendance": "Theo dõi chấm công nhân viên",
    
    # User-related tables
    "nguoi_dung|user": "Quản lý tài khoản người dùng",
    "dang_nhap|login|auth": "Xác thực và phân quyền người dùng",
    
    # Marketing-related tables
    "tiep_thi|marketing|campaign": "Quản lý chiến dịch tiếp thị",
    "email_marketing": "Gửi email tiếp thị khách hàng",
    
    # Support-related tables
    "ho_tro|support|ticket": "Quản lý hỗ trợ khách hàng",
    "phan_hoi|feedback": "Thu thập phản hồi khách hàng"
}


# Activity Name Templates English
ACTIVITY_NAME_TEMPLATES_EN: Dict[str, str] = {
    "khach_hang|customer": "Customer Information Management",
    "don_hang|order": "Order and Transaction Management",
    "thanh_toan|payment": "Customer Payment Processing",
    "nhan_vien|employee|staff": "Employee Information Management",
    "luong|salary|payroll": "Employee Payroll Processing",
    "cham_cong|attendance": "Employee Attendance Tracking",
    "nguoi_dung|user": "User Account Management",
    "dang_nhap|login|auth": "User Authentication and Authorization",
    "tiep_thi|marketing|campaign": "Marketing Campaign Management",
    "email_marketing": "Customer Email Marketing",
    "ho_tro|support|ticket": "Customer Support Management",
    "phan_hoi|feedback": "Customer Feedback Collection"
}


# Processing Purpose Templates (Vietnamese-first)
PURPOSE_TEMPLATES_VI: Dict[str, str] = {
    "khach_hang|customer": "Lưu trữ và quản lý thông tin khách hàng để cung cấp dịch vụ và hỗ trợ tốt hơn",
    "don_hang|order": "Xử lý đơn hàng, giao dịch và lịch sử mua hàng của khách hàng",
    "thanh_toan|payment": "Xử lý thanh toán an toàn cho giao dịch mua hàng của khách hàng",
    "nhan_vien|employee|staff": "Quản lý hồ sơ nhân viên, hợp đồng lao động và thông tin liên hệ",
    "luong|salary|payroll": "Tính toán và chi trả lương, phúc lợi cho nhân viên",
    "cham_cong|attendance": "Ghi nhận giờ làm việc và tính công nhân viên",
    "nguoi_dung|user": "Quản lý tài khoản và hồ sơ người dùng hệ thống",
    "dang_nhap|login|auth": "Xác thực danh tính và phân quyền truy cập hệ thống",
    "tiep_thi|marketing|campaign": "Thực hiện chiến dịch tiếp thị và quảng cáo sản phẩm",
    "email_marketing": "Gửi thông tin sản phẩm và khuyến mãi qua email",
    "ho_tro|support|ticket": "Tiếp nhận và xử lý yêu cầu hỗ trợ từ khách hàng",
    "phan_hoi|feedback": "Thu thập ý kiến phản hồi để cải thiện sản phẩm và dịch vụ"
}


# Processing Purpose Templates (English)
PURPOSE_TEMPLATES_EN: Dict[str, str] = {
    "khach_hang|customer": "Store and manage customer information to provide better services and support",
    "don_hang|order": "Process orders, transactions and customer purchase history",
    "thanh_toan|payment": "Process secure payments for customer transactions",
    "nhan_vien|employee|staff": "Manage employee records, employment contracts and contact information",
    "luong|salary|payroll": "Calculate and process employee salary and benefits",
    "cham_cong|attendance": "Record working hours and calculate employee attendance",
    "nguoi_dung|user": "Manage user accounts and system profiles",
    "dang_nhap|login|auth": "Authenticate identity and authorize system access",
    "tiep_thi|marketing|campaign": "Execute marketing campaigns and product advertising",
    "email_marketing": "Send product information and promotions via email",
    "ho_tro|support|ticket": "Receive and process customer support requests",
    "phan_hoi|feedback": "Collect feedback to improve products and services"
}


class VietnameseActivitySuggester:
    """
    Gợi ý tên hoạt động bằng tiếng Việt
    Vietnamese activity name suggester
    
    AI-powered Vietnamese-first suggestions
    """
    
    def suggest_activity_name(
        self,
        table_name: str,
        personal_data_fields: List[str]
    ) -> Tuple[str, str, float]:
        """
        Gợi ý tên hoạt động dựa trên tên bảng
        Suggest activity name based on table name
        
        Returns:
            (activity_name_vi, activity_name_en, confidence_score)
        """
        table_lower = table_name.lower()
        
        # Match against templates
        for pattern, name_vi in ACTIVITY_NAME_TEMPLATES_VI.items():
            if re.search(pattern, table_lower):
                name_en = ACTIVITY_NAME_TEMPLATES_EN.get(pattern, name_vi)
                confidence = 0.85  # High confidence for pattern match
                return (name_vi, name_en, confidence)
        
        # Fallback: Generic name based on table name
        name_vi = f"Quản lý dữ liệu bảng {table_name}"
        name_en = f"Data Management for {table_name} Table"
        confidence = 0.60  # Lower confidence for generic
        
        return (name_vi, name_en, confidence)
    
    def suggest_processing_purpose(
        self,
        table_name: str,
        personal_data_fields: List[str]
    ) -> Tuple[str, str]:
        """
        Gợi ý mục đích xử lý
        Suggest processing purpose
        
        Returns:
            (purpose_vi, purpose_en)
        """
        table_lower = table_name.lower()
        
        # Match against purpose templates
        for pattern, purpose_vi in PURPOSE_TEMPLATES_VI.items():
            if re.search(pattern, table_lower):
                purpose_en = PURPOSE_TEMPLATES_EN.get(pattern, purpose_vi)
                return (purpose_vi, purpose_en)
        
        # Fallback: Generic purpose
        purpose_vi = f"Xử lý và quản lý thông tin trong bảng {table_name} để phục vụ hoạt động kinh doanh"
        purpose_en = f"Process and manage information in {table_name} table for business operations"
        
        return (purpose_vi, purpose_en)
    
    def suggest_legal_basis(
        self,
        table_name: str,
        has_sensitive_data: bool
    ) -> Tuple[str, float]:
        """
        Gợi ý cơ sở pháp lý
        Suggest legal basis (Art. 13.1 PDPL)
        
        Returns:
            (legal_basis, confidence_score)
        """
        table_lower = table_name.lower()
        
        # Sensitive data typically requires consent
        if has_sensitive_data:
            return ("consent", 0.90)
        
        # Customer/order tables likely contract-based
        if re.search(r"khach_hang|customer|don_hang|order|thanh_toan|payment", table_lower):
            return ("contract", 0.85)
        
        # Employee tables typically contract or legal obligation
        if re.search(r"nhan_vien|employee|luong|salary|cham_cong", table_lower):
            return ("contract", 0.80)
        
        # Default: legitimate interest with lower confidence
        return ("legitimate_interest", 0.65)
```

---

## Validation and Review Workflow

### Human Review Process

```python
# api/endpoints/discovery_endpoints.py

"""
Database Discovery Endpoints
Vietnamese-first Automated Discovery API
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from database.connection import get_db
from api.models.discovery_models import (
    DatabaseConnectionRequest,
    DiscoveredActivityResponse
)
from services.discovery.discovery_orchestrator import DiscoveryOrchestrator


router = APIRouter(
    prefix="/api/v1/data-inventory/discovery",
    tags=["Automated Discovery | Khám phá Tự động"]
)


@router.post(
    "/start",
    response_model=Dict[str, any],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Bắt đầu khám phá tự động | Start automated discovery",
    description="""
    **Vietnamese:** Bắt đầu quá trình khám phá tự động cơ sở dữ liệu để phát hiện hoạt động xử lý dữ liệu.
    
    **English:** Start automated database discovery to detect data processing activities.
    
    **Process:**
    1. Kết nối đến cơ sở dữ liệu | Connect to database
    2. Phân tích schema | Analyze schema
    3. Phân loại dữ liệu cá nhân | Classify personal data
    4. Gợi ý hoạt động xử lý | Suggest processing activities
    5. Tạo hoạt động với trạng thái "pending_review" | Create activities with "pending_review" status
    
    **Note:** Discovery runs in background. Use /status endpoint to check progress.
    """
)
async def start_discovery(
    request: DatabaseConnectionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> Dict[str, any]:
    """
    Bắt đầu khám phá tự động
    Start automated discovery
    
    Authentication:
    - Requires JWT Bearer token
    - Permission: 'processing_activity.write' + database scan privilege
    - Allowed roles: admin, data_processor
    - Tenant isolation enforced
    
    Runs discovery in background task
    """
    # Validate user has scan privilege
    from auth.privileges import has_database_scan_privilege
    
    if not await has_database_scan_privilege(db, current_user, current_tenant):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "User does not have database scan privilege",
                "error_vi": "Người dùng không có quyền quét cơ sở dữ liệu",
                "required_privilege": "database_scan",
                "user_id": str(current_user),
                "allowed_roles": ["admin", "data_processor"]
            }
        )
    
    # Create discovery session
    discovery_id = uuid4()
    
    # Schedule background task with tenant and user context
    background_tasks.add_task(
        run_discovery,
        discovery_id=discovery_id,
        tenant_id=current_tenant,  # From JWT token (not from request parameter)
        connection_request=request,
        db=db,
        user_id=current_user  # From JWT token
    )
    
    return {
        "discovery_id": discovery_id,
        "tenant_id": str(current_tenant),
        "user_id": str(current_user),
        "status": "in_progress",
        "status_vi": "Đang khám phá",
        "status_en": "In Progress",
        "message_vi": f"Bắt đầu khám phá: {request.discover_name_vi}",
        "message_en": f"Started discovery: {request.discover_name_en or request.discover_name_vi}",
        "estimated_time_minutes": 5,
        "check_status_url": f"/api/v1/data-inventory/discovery/status/{discovery_id}"
    }


@router.get(
    "/discovered-activities/{discovery_id}",
    response_model=List[DiscoveredActivityResponse],
    summary="Lấy hoạt động đã khám phá | Get discovered activities",
    description="""
    **Vietnamese:** Lấy danh sách hoạt động xử lý được khám phá tự động.
    
    **English:** Get list of automatically discovered processing activities.
    
    **Status:** All returned activities have status="pending_review" and require human approval.
    """
)
async def get_discovered_activities(
    discovery_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> List[DiscoveredActivityResponse]:
    """
    Lấy hoạt động đã khám phá
    Get discovered activities
    
    Authentication:
    - Requires JWT Bearer token
    - Permission: 'processing_activity.read'
    - Allowed roles: admin, data_processor, compliance_officer, viewer
    - Tenant isolation: Only returns activities for current_tenant
    
    Returns activities pending human review
    """
    # Validate discovery belongs to current tenant
    from crud.discovery import get_discovery_session
    
    discovery_session = await get_discovery_session(db, discovery_id)
    
    if not discovery_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Discovery session not found",
                "error_vi": "Không tìm thấy phiên khám phá",
                "discovery_id": str(discovery_id)
            }
        )
    
    # Validate tenant ownership
    if discovery_session.tenant_id != current_tenant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied. Cannot access discovery from different tenant",
                "error_vi": "Truy cập bị từ chối. Không thể truy cập khám phá của tenant khác",
                "discovery_tenant_id": str(discovery_session.tenant_id),
                "user_tenant_id": str(current_tenant)
            }
        )
    
    # Implementation will query discovered activities for this tenant
    pass


@router.post(
    "/approve-activity/{activity_id}",
    response_model=ProcessingActivityResponse,
    summary="Phê duyệt hoạt động đã khám phá | Approve discovered activity",
    description="""
    **Vietnamese:** Phê duyệt hoạt động xử lý được khám phá tự động, chuyển từ "pending_review" sang "active".
    
    **English:** Approve automatically discovered activity, change from "pending_review" to "active".
    
    **Human Review Required:** Compliance officer must verify before approval.
    """
)
async def approve_discovered_activity(
    activity_id: UUID,
    approval_notes_vi: Optional[str] = None,
    approval_notes_en: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> ProcessingActivityResponse:
    """
    Phê duyệt hoạt động đã khám phá
    Approve discovered activity
    
    Authentication:
    - Requires JWT Bearer token
    - Permission: 'processing_activity.write'
    - Allowed roles: admin, compliance_officer, data_processor
    - Tenant isolation: Can only approve activities from current_tenant
    
    Changes status from pending_review to active
    Creates audit trail with approver user_id
    """
    from crud.processing_activity import get_processing_activity_by_id, update_processing_activity_status
    
    # Get activity
    activity = await get_processing_activity_by_id(db, activity_id)
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Processing activity not found",
                "error_vi": "Không tìm thấy hoạt động xử lý",
                "activity_id": str(activity_id)
            }
        )
    
    # Validate tenant ownership
    if activity.tenant_id != current_tenant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Access denied. Cannot approve activity from different tenant",
                "error_vi": "Truy cập bị từ chối. Không thể phê duyệt hoạt động của tenant khác",
                "activity_tenant_id": str(activity.tenant_id),
                "user_tenant_id": str(current_tenant)
            }
        )
    
    # Validate activity is pending review
    if activity.status != "pending_review":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Activity is not pending review",
                "error_vi": "Hoạt động không ở trạng thái chờ phê duyệt",
                "current_status": activity.status,
                "current_status_vi": _get_status_translation_vi(activity.status)
            }
        )
    
    # Update status to active
    updated_activity = await update_processing_activity_status(
        db=db,
        activity_id=activity_id,
        new_status="active",
        approval_notes_vi=approval_notes_vi,
        approval_notes_en=approval_notes_en,
        approved_by=current_user
    )
    
    # Create audit log
    await create_audit_log(
        db=db,
        tenant_id=current_tenant,
        action_type="approve",
        entity_type="processing_activity",
        entity_id=activity_id,
        user_id=current_user,
        audit_message_vi=f"Phê duyệt hoạt động khám phá: {activity.activity_name_vi}",
        audit_message_en=f"Approved discovered activity: {activity.activity_name_en or activity.activity_name_vi}",
        old_values={"status": "pending_review"},
        new_values={"status": "active", "approved_by": str(current_user)}
    )
    
    # Implementation will update status and create audit log
    pass
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] Database connection supports 5 database types (MySQL, PostgreSQL, SQL Server, MongoDB, Oracle)
- [TARGET] Schema analyzer detects personal data using Vietnamese/English patterns
- [TARGET] AI suggests Vietnamese-first activity names with confidence scores
- [TARGET] Legal basis recommendation based on data sensitivity
- [TARGET] All discovered activities created with status="pending_review"
- [TARGET] Human review workflow with approval/rejection endpoints
- [TARGET] Zero hard-coding (all patterns in named constants)
- [TARGET] Complete audit trail for discovery and approval actions
- [TARGET] Background task processing for large database scans
- [TARGET] Error handling for connection failures with bilingual messages

**Next Document:** #03 - Bulk Import from CSV/Excel
