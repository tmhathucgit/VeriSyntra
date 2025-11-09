# Data Population Method 2: Automated Database Discovery
## Vietnamese PDPL 2025 Compliance - Data Categories Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** data_categories Table  
**Method:** AI-Powered Database Schema Analysis with PDPL Classification  
**Architecture:** Vietnamese NLP + Pattern Recognition + PDPL Article 4.13 Detection  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **automated data category discovery** by scanning database schemas and using Vietnamese NLP to classify data categories according to PDPL Article 4.1 (personal data) and Article 4.13 (sensitive data). VeriAI analyzes column names, data types, and content patterns to suggest appropriate category classifications.

**Key Features:**
- Automatic PDPL Article 4.13 sensitive data detection
- Vietnamese column name pattern recognition
- Multi-database schema scanning (MySQL, PostgreSQL, SQL Server, MongoDB)
- AI confidence scoring for category suggestions
- Vietnamese NLP classification engine
- Zero hard-coding with pattern configuration

**Use Cases:**
- Auto-discover categories from existing databases
- Classify Vietnamese database columns to PDPL categories
- Suggest sensitive data categories per Article 4.13
- Bulk category creation from schema analysis
- Compliance gap identification

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Authentication & Authorization (Phase 7)](#authentication--authorization-phase-7)
3. [PDPL Detection Patterns](#pdpl-detection-patterns)
4. [Vietnamese NLP Classifier](#vietnamese-nlp-classifier)
5. [Category Suggestion Engine](#category-suggestion-engine)
6. [Multi-Database Scanner](#multi-database-scanner)
7. [Confidence Scoring](#confidence-scoring)
8. [Secure Credential Handling](#secure-credential-handling)
9. [Success Criteria](#success-criteria)

---

## Architecture Overview

### AI Discovery System

```
┌─────────────────────────────────────────────────────────────┐
│       Automated Category Discovery Architecture             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Database    │  │  Column      │  │  Vietnamese  │     │
│  │  Scanner     │─>│  Analyzer    │─>│  NLP Engine  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PDPL 4.13   │  │  Category    │  │  Confidence  │     │
│  │  Detector    │  │  Suggester   │  │  Scorer      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  data_categories       │                    │
│              │  (AI-discovered)       │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Discovery Workflow:**
1. Connect to target database
2. Scan schema for tables and columns
3. Analyze column names with Vietnamese patterns
4. Detect PDPL Article 4.13 sensitive data
5. Calculate confidence scores
6. Generate category suggestions
7. Present to user for approval
8. Create approved categories

---

## Authentication & Authorization (Phase 7)

### Overview

**Phase 7** restricts automated database discovery to **authorized personnel only** due to the sensitive nature of scanning production databases and discovering PDPL Article 4.13 sensitive data categories.

**RBAC Restrictions:**
- **Allowed Roles:** `admin`, `data_processor` (compliance_officer can approve only)
- **Required Permission:** `database_scan` (special privilege)
- **Forbidden Roles:** `viewer` (read-only users cannot initiate scans)

### Database Scan Privilege

```python
# api/auth/discovery_permissions.py

"""
Database Discovery RBAC
Restricted to admin and data_processor only
"""

from fastapi import Depends, HTTPException, status

from api.auth.jwt_dependencies import get_current_user


async def require_database_scan_permission(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Kiểm tra quyền quét cơ sở dữ liệu
    Check database scan permission
    
    Only admin and data_processor can initiate database scans
    Reason: Access to production database schemas and sensitive data discovery
    """
    
    allowed_roles = ["admin", "data_processor"]
    user_role = current_user.get("role")
    user_permissions = current_user.get("permissions", [])
    
    # Check role
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Database scan permission denied",
                "error_vi": "Không có quyền quét cơ sở dữ liệu",
                "message": f"Only admin or data_processor can scan databases. Current role: {user_role}",
                "user_role": user_role,
                "user_role_vi": current_user.get("role_vi"),
                "allowed_roles": allowed_roles,
                "allowed_roles_vi": ["Quản trị viên", "Người xử lý dữ liệu"],
                "reason_vi": "Quét database có thể truy cập dữ liệu nhạy cảm PDPL Điều 4.13"
            }
        )
    
    # Check database_scan privilege
    if "database_scan" not in user_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Missing database_scan privilege",
                "error_vi": "Thiếu đặc quyền quét cơ sở dữ liệu",
                "message": "User lacks required 'database_scan' permission",
                "user_permissions": user_permissions,
                "required_permission": "database_scan"
            }
        )
    
    return current_user


async def require_sensitive_discovery_approval(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Kiểm tra quyền phê duyệt danh mục nhạy cảm được phát hiện
    Check permission to approve discovered sensitive categories
    
    Only compliance_officer and admin can approve PDPL Article 4.13 categories
    """
    
    allowed_roles = ["compliance_officer", "admin"]
    user_role = current_user.get("role")
    
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Sensitive category approval denied",
                "error_vi": "Không có quyền phê duyệt danh mục nhạy cảm (Điều 4.13 PDPL)",
                "message": f"Only compliance_officer or admin can approve sensitive categories",
                "user_role": user_role,
                "user_role_vi": current_user.get("role_vi"),
                "pdpl_reference": "Article 4.13 PDPL - Sensitive Personal Data"
            }
        )
    
    return current_user
```

### Start Discovery Endpoint (Authenticated)

```python
@router.post(
    "/discovery/start",
    response_model=DiscoveryJobResponse,
    summary="Bắt đầu quét cơ sở dữ liệu | Start database discovery",
    description="""
    **Vietnamese:** Bắt đầu quét tự động cơ sở dữ liệu để phát hiện danh mục dữ liệu.
    
    **English:** Start automated database scan to discover data categories.
    
    **Authentication:** Requires JWT token with `database_scan` permission.
    **Allowed Roles:** admin, data_processor only.
    **Security:** Credentials encrypted, temporary access, audit logging.
    """
)
async def start_category_discovery(
    request: DiscoveryStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_database_scan_permission)
) -> DiscoveryJobResponse:
    """
    Bắt đầu quét phát hiện danh mục
    Start category discovery scan
    
    Phase 7: RBAC restriction + Tenant isolation + Audit trail
    """
    
    user_tenant_id = current_user["tenant_id"]
    user_id = current_user["user_id"]
    
    # Validate tenant access
    if request.database_config.tenant_id != user_tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Tenant access violation",
                "error_vi": "Vi phạm cách ly dữ liệu giữa các khách hàng",
                "message": "Cannot scan database from different tenant"
            }
        )
    
    # Create discovery job
    job = DiscoveryJob(
        tenant_id=user_tenant_id,
        initiated_by=user_id,
        database_type=request.database_config.database_type,
        status="running",
        started_at=datetime.now(timezone.utc)
    )
    
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    # Start background discovery task
    task = discover_categories_task.delay(
        job_id=str(job.job_id),
        database_config=request.database_config.dict(),
        tenant_id=str(user_tenant_id)
    )
    
    # Audit log
    await log_category_access(
        action="START_CATEGORY_DISCOVERY",
        action_vi="Bắt đầu quét phát hiện danh mục dữ liệu",
        category_id=None,
        user_id=user_id,
        tenant_id=user_tenant_id,
        user_role=current_user["role"],
        user_name_vi=current_user["full_name_vi"],
        ip_address=request.client.host,
        success=True,
        details={
            "job_id": str(job.job_id),
            "database_type": request.database_config.database_type,
            "database_host": request.database_config.host
        }
    )
    
    return DiscoveryJobResponse(
        job_id=job.job_id,
        status="running",
        status_vi="Đang chạy",
        message="Discovery scan started",
        message_vi="Đã bắt đầu quét phát hiện",
        started_at=job.started_at
    )


@router.post(
    "/discovery/{job_id}/approve/{suggestion_id}",
    response_model=DataCategoryResponse,
    summary="Phê duyệt danh mục được phát hiện | Approve discovered category",
    description="""
    **Vietnamese:** Phê duyệt và tạo danh mục từ kết quả phát hiện tự động.
    
    **English:** Approve and create category from discovery results.
    
    **Authentication:** Requires JWT token with appropriate permissions.
    **Sensitive Data:** Approving PDPL Article 4.13 categories requires compliance_officer or admin role.
    """
)
async def approve_discovered_category(
    job_id: UUID,
    suggestion_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> DataCategoryResponse:
    """
    Phê duyệt danh mục được phát hiện
    Approve discovered category
    
    Phase 7: Sensitive data approval check + Tenant isolation + Audit trail
    """
    
    user_tenant_id = current_user["tenant_id"]
    user_id = current_user["user_id"]
    
    # Fetch suggestion with tenant check
    query = select(CategorySuggestion).where(
        CategorySuggestion.suggestion_id == suggestion_id,
        CategorySuggestion.job_id == job_id,
        CategorySuggestion.tenant_id == user_tenant_id
    )
    
    result = await db.execute(query)
    suggestion = result.scalar_one_or_none()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Suggestion not found",
                "error_vi": "Không tìm thấy gợi ý danh mục",
                "message": f"Suggestion {suggestion_id} not found or access denied"
            }
        )
    
    # Check sensitive data approval permission
    if suggestion.is_sensitive:
        allowed_roles = ["compliance_officer", "admin"]
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Sensitive category approval denied",
                    "error_vi": "Không có quyền phê duyệt danh mục nhạy cảm (Điều 4.13 PDPL)",
                    "message": "Only compliance_officer or admin can approve PDPL Article 4.13 sensitive categories",
                    "user_role": current_user["role"],
                    "user_role_vi": current_user["role_vi"],
                    "category_type": suggestion.category_type,
                    "pdpl_reference": suggestion.pdpl_article_reference
                }
            )
    
    # Create approved category
    category = DataCategory(
        tenant_id=user_tenant_id,
        category_name_vi=suggestion.suggested_name_vi,
        category_name_en=suggestion.suggested_name_en,
        category_description_vi=suggestion.suggested_description_vi,
        category_type=suggestion.category_type,
        is_sensitive=suggestion.is_sensitive,
        pdpl_article_reference=suggestion.pdpl_article_reference,
        status=CategoryStatus.ACTIVE,
        created_by=user_id,
        updated_by=user_id
    )
    
    db.add(category)
    
    # Update suggestion status
    suggestion.status = "approved"
    suggestion.approved_by = user_id
    suggestion.approved_at = datetime.now(timezone.utc)
    
    await db.commit()
    await db.refresh(category)
    
    # Audit log
    await log_category_access(
        action="APPROVE_DISCOVERED_CATEGORY",
        action_vi=f"Phê duyệt danh mục {'nhạy cảm ' if suggestion.is_sensitive else ''}được phát hiện",
        category_id=category.category_id,
        user_id=user_id,
        tenant_id=user_tenant_id,
        user_role=current_user["role"],
        user_name_vi=current_user["full_name_vi"],
        ip_address=request.client.host,
        success=True,
        details={
            "job_id": str(job_id),
            "suggestion_id": str(suggestion_id),
            "confidence_score": suggestion.confidence_score,
            "source_table": suggestion.source_table,
            "source_column": suggestion.source_column
        }
    )
    
    return category
```

---

## Secure Credential Handling

### Database Connection Security

```python
# services/discovery/secure_credentials.py

"""
Secure Database Credential Handling
Vietnamese PDPL Compliance for Discovery
"""

from cryptography.fernet import Fernet
import os
from typing import Dict

from config.settings import settings


class SecureCredentialManager:
    """
    Quản lý bảo mật thông tin xác thực database
    Secure database credentials manager
    
    Phase 7: Encryption + Temporary access + Auto-expiry
    """
    
    def __init__(self):
        self.cipher = Fernet(settings.CREDENTIALS_ENCRYPTION_KEY)
    
    def encrypt_credentials(self, credentials: Dict[str, str]) -> str:
        """
        Mã hóa thông tin xác thực
        Encrypt database credentials
        """
        
        credentials_json = json.dumps(credentials)
        encrypted = self.cipher.encrypt(credentials_json.encode())
        return encrypted.decode()
    
    def decrypt_credentials(self, encrypted_credentials: str) -> Dict[str, str]:
        """
        Giải mã thông tin xác thực
        Decrypt database credentials
        """
        
        decrypted = self.cipher.decrypt(encrypted_credentials.encode())
        return json.loads(decrypted.decode())
    
    async def create_temporary_access(
        self,
        database_config: dict,
        tenant_id: UUID,
        user_id: UUID,
        duration_minutes: int = 60
    ) -> str:
        """
        Tạo quyền truy cập tạm thời
        Create temporary database access
        
        Credentials expire after specified duration
        """
        
        # Encrypt credentials
        encrypted = self.encrypt_credentials({
            "host": database_config["host"],
            "port": database_config["port"],
            "database": database_config["database"],
            "username": database_config["username"],
            "password": database_config["password"]
        })
        
        # Store with expiry in Redis
        access_token = f"db_access:{tenant_id}:{user_id}:{uuid.uuid4()}"
        
        await redis_client.setex(
            access_token,
            duration_minutes * 60,  # Convert to seconds
            encrypted
        )
        
        # Audit log
        logger.info(
            f"[AUDIT] Temporary database access created | "
            f"Tenant: {tenant_id} | User: {user_id} | "
            f"Expires: {duration_minutes} minutes"
        )
        
        return access_token
    
    async def revoke_access(self, access_token: str) -> None:
        """
        Thu hồi quyền truy cập
        Revoke database access
        """
        
        await redis_client.delete(access_token)
        logger.info(f"[AUDIT] Database access revoked | Token: {access_token[:20]}...")
```

**Security Features:**
- **Encryption:** Database credentials encrypted with Fernet (AES-128)
- **Temporary Access:** Credentials expire after 60 minutes
- **Auto-Revoke:** Redis TTL automatically removes expired credentials
- **Audit Trail:** All credential access logged
- **No Persistent Storage:** Credentials never stored in database unencrypted

---

## PDPL Detection Patterns

### Sensitive Data Pattern Configuration

```python
# services/discovery/pdpl_patterns.py

"""
PDPL Article 4.13 Detection Patterns
Vietnamese Sensitive Data Classification
"""

from typing import Dict, List
import re


# PDPL Article 4.13 Sensitive Data Patterns (Vietnamese)
PDPL_SENSITIVE_PATTERNS_VI: Dict[str, List[str]] = {
    "political_opinions": [
        r"(?i)(chính trị|chinh tri|đảng viên|dang vien|quan điểm chính trị)",
        r"(?i)(political|party member|political view)"
    ],
    "religious_beliefs": [
        r"(?i)(tôn giáo|ton giao|tín ngưỡng|tin nguong|đạo|dao)",
        r"(?i)(religion|religious|belief|faith)"
    ],
    "health_data": [
        r"(?i)(sức khỏe|suc khoe|y tế|y te|bệnh|benh|bệnh án|benh an)",
        r"(?i)(health|medical|disease|diagnosis|treatment|patient)",
        r"(?i)(hồ sơ bệnh án|ho so benh an|kết quả xét nghiệm|ket qua xet nghiem)",
        r"(?i)(đơn thuốc|don thuoc|thuốc|thuoc|prescription|medication)"
    ],
    "biometric_data": [
        r"(?i)(sinh trắc học|sinh trac hoc|vân tay|van tay|khuôn mặt|khuon mat)",
        r"(?i)(biometric|fingerprint|face|facial|iris|retina|voice)",
        r"(?i)(võng mạc|vong mac|giọng nói|giong noi|DNA)"
    ],
    "genetic_data": [
        r"(?i)(di truyền|di truyen|gen|gene|genetic|DNA|genome)",
        r"(?i)(mã di truyền|ma di truyen|xét nghiệm gen|xet nghiem gen)"
    ],
    "sexual_orientation": [
        r"(?i)(tình dục|tinh duc|giới tính|gioi tinh|xu hướng tình dục)",
        r"(?i)(sexual|orientation|gender|LGBT|LGBTQ)"
    ],
    "criminal_records": [
        r"(?i)(hồ sơ tư pháp|ho so tu phap|tiền án|tien an|tiền sự|tien su)",
        r"(?i)(criminal|conviction|record|sentence|judgment)",
        r"(?i)(bản án|ban an|hình sự|hinh su|tội phạm|toi pham)"
    ],
    "trade_union": [
        r"(?i)(công đoàn|cong doan|tổ chức công đoàn|to chuc cong doan)",
        r"(?i)(trade union|labor union|worker organization)"
    ],
    "children_data": [
        r"(?i)(trẻ em|tre em|thiếu niên|thieu nien|học sinh|hoc sinh)",
        r"(?i)(child|children|minor|student|under 16|dưới 16 tuổi)"
    ]
}


# Basic Personal Data Patterns (Vietnamese)
BASIC_PERSONAL_DATA_PATTERNS_VI: Dict[str, List[str]] = {
    "full_name": [
        r"(?i)(họ tên|ho ten|tên|ten|name|full name|họ và tên|ho va ten)",
        r"(?i)(first name|last name|middle name|họ|ho|tên đệm|ten dem)"
    ],
    "identification": [
        r"(?i)(CMND|CCCD|số CMND|so CMND|ID|identity|chứng minh|chung minh)",
        r"(?i)(passport|hộ chiếu|ho chieu|giấy tờ tùy thân|giay to tuy than)"
    ],
    "contact_info": [
        r"(?i)(điện thoại|dien thoai|phone|mobile|số điện thoại|so dien thoai)",
        r"(?i)(email|thư điện tử|thu dien tu|địa chỉ email|dia chi email)",
        r"(?i)(địa chỉ|dia chi|address|location|nơi ở|noi o)"
    ],
    "date_of_birth": [
        r"(?i)(ngày sinh|ngay sinh|birth|birthday|date of birth|DOB)",
        r"(?i)(năm sinh|nam sinh|birth year|tuổi|tuoi|age)"
    ],
    "financial_info": [
        r"(?i)(tài khoản|tai khoan|account|bank account|số tài khoản|so tai khoan)",
        r"(?i)(thu nhập|thu nhap|income|salary|lương|luong)",
        r"(?i)(thẻ tín dụng|the tin dung|credit card|debit card)"
    ],
    "location_data": [
        r"(?i)(vị trí|vi tri|location|GPS|coordinates|tọa độ|toa do)",
        r"(?i)(địa điểm|dia diem|place|position)"
    ],
    "online_identifier": [
        r"(?i)(IP|IP address|cookie|device ID|MAC address)",
        r"(?i)(username|user ID|tài khoản|tai khoan|login)"
    ]
}


# Category Suggestion Templates
CATEGORY_TEMPLATES_VI: Dict[str, Dict[str, str]] = {
    "political_opinions": {
        "category_name_vi": "Quan điểm chính trị",
        "category_name_en": "Political Opinions",
        "category_type": "sensitive",
        "pdpl_article": "Art. 4.13 PDPL"
    },
    "religious_beliefs": {
        "category_name_vi": "Tín ngưỡng tôn giáo",
        "category_name_en": "Religious Beliefs",
        "category_type": "sensitive",
        "pdpl_article": "Art. 4.13 PDPL"
    },
    "health_data": {
        "category_name_vi": "Thông tin sức khỏe",
        "category_name_en": "Health Information",
        "category_type": "sensitive",
        "pdpl_article": "Art. 4.13 PDPL"
    },
    "biometric_data": {
        "category_name_vi": "Dữ liệu sinh trắc học",
        "category_name_en": "Biometric Data",
        "category_type": "sensitive",
        "pdpl_article": "Art. 4.13 PDPL"
    },
    "genetic_data": {
        "category_name_vi": "Thông tin di truyền",
        "category_name_en": "Genetic Information",
        "category_type": "sensitive",
        "pdpl_article": "Art. 4.13 PDPL"
    },
    "sexual_orientation": {
        "category_name_vi": "Xu hướng tình dục",
        "category_name_en": "Sexual Orientation",
        "category_type": "sensitive",
        "pdpl_article": "Art. 4.13 PDPL"
    },
    "criminal_records": {
        "category_name_vi": "Hồ sơ tư pháp",
        "category_name_en": "Criminal Records",
        "category_type": "sensitive",
        "pdpl_article": "Art. 4.13 PDPL"
    },
    "full_name": {
        "category_name_vi": "Họ và tên",
        "category_name_en": "Full Name",
        "category_type": "basic",
        "pdpl_article": "Art. 4.1 PDPL"
    },
    "identification": {
        "category_name_vi": "Giấy tờ tùy thân",
        "category_name_en": "Identification Documents",
        "category_type": "basic",
        "pdpl_article": "Art. 4.1 PDPL"
    },
    "contact_info": {
        "category_name_vi": "Thông tin liên hệ",
        "category_name_en": "Contact Information",
        "category_type": "basic",
        "pdpl_article": "Art. 4.1 PDPL"
    },
    "date_of_birth": {
        "category_name_vi": "Ngày tháng năm sinh",
        "category_name_en": "Date of Birth",
        "category_type": "basic",
        "pdpl_article": "Art. 4.1 PDPL"
    },
    "financial_info": {
        "category_name_vi": "Thông tin tài chính",
        "category_name_en": "Financial Information",
        "category_type": "basic",
        "pdpl_article": "Art. 4.1 PDPL"
    }
}
```

---

## Vietnamese NLP Classifier

### Category Classification Engine

```python
# services/discovery/nlp_classifier.py

"""
Vietnamese NLP Category Classifier
PDPL-Aware Data Classification
"""

from typing import Dict, List, Tuple
import re


class VietnameseNLPClassifier:
    """
    Bộ phân loại NLP tiếng Việt
    Vietnamese NLP classifier for PDPL categories
    
    Classifies column names to data categories
    """
    
    def __init__(self):
        self.sensitive_patterns = PDPL_SENSITIVE_PATTERNS_VI
        self.basic_patterns = BASIC_PERSONAL_DATA_PATTERNS_VI
        self.category_templates = CATEGORY_TEMPLATES_VI
    
    def classify_column(
        self,
        column_name: str,
        table_name: str = None,
        sample_values: List[str] = None
    ) -> List[Dict[str, any]]:
        """
        Phân loại cột dữ liệu
        Classify database column to categories
        
        Returns list of category suggestions with confidence
        """
        suggestions = []
        
        # Step 1: Check sensitive data patterns (PDPL 4.13)
        sensitive_matches = self._check_sensitive_patterns(column_name)
        if sensitive_matches:
            suggestions.extend(sensitive_matches)
        
        # Step 2: Check basic personal data patterns (PDPL 4.1)
        basic_matches = self._check_basic_patterns(column_name)
        if basic_matches:
            suggestions.extend(basic_matches)
        
        # Step 3: Analyze sample values if available
        if sample_values:
            value_matches = self._analyze_sample_values(sample_values)
            suggestions.extend(value_matches)
        
        # Sort by confidence score
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return suggestions
    
    def _check_sensitive_patterns(
        self,
        column_name: str
    ) -> List[Dict[str, any]]:
        """Kiểm tra pattern dữ liệu nhạy cảm"""
        matches = []
        
        for category_key, patterns in self.sensitive_patterns.items():
            for pattern in patterns:
                if re.search(pattern, column_name):
                    template = self.category_templates[category_key]
                    
                    matches.append({
                        "category_key": category_key,
                        "category_name_vi": template["category_name_vi"],
                        "category_name_en": template["category_name_en"],
                        "category_type": template["category_type"],
                        "is_sensitive": True,
                        "pdpl_article": template["pdpl_article"],
                        "confidence": self._calculate_confidence(pattern, column_name),
                        "matched_pattern": pattern,
                        "detection_method": "sensitive_pattern_match"
                    })
                    break
        
        return matches
    
    def _check_basic_patterns(
        self,
        column_name: str
    ) -> List[Dict[str, any]]:
        """Kiểm tra pattern dữ liệu cơ bản"""
        matches = []
        
        for category_key, patterns in self.basic_patterns.items():
            for pattern in patterns:
                if re.search(pattern, column_name):
                    template = self.category_templates[category_key]
                    
                    matches.append({
                        "category_key": category_key,
                        "category_name_vi": template["category_name_vi"],
                        "category_name_en": template["category_name_en"],
                        "category_type": template["category_type"],
                        "is_sensitive": False,
                        "pdpl_article": template["pdpl_article"],
                        "confidence": self._calculate_confidence(pattern, column_name),
                        "matched_pattern": pattern,
                        "detection_method": "basic_pattern_match"
                    })
                    break
        
        return matches
    
    def _calculate_confidence(
        self,
        pattern: str,
        column_name: str
    ) -> float:
        """
        Tính điểm tin cậy
        Calculate confidence score (0.0 - 1.0)
        """
        # Exact match gets highest confidence
        if re.fullmatch(pattern, column_name, re.IGNORECASE):
            return 0.95
        
        # Pattern match in column name
        if re.search(pattern, column_name, re.IGNORECASE):
            # Longer match = higher confidence
            match = re.search(pattern, column_name, re.IGNORECASE)
            match_length = len(match.group(0))
            column_length = len(column_name)
            
            ratio = match_length / column_length
            return min(0.7 + (ratio * 0.2), 0.9)
        
        return 0.5
    
    def _analyze_sample_values(
        self,
        sample_values: List[str]
    ) -> List[Dict[str, any]]:
        """Phân tích giá trị mẫu để xác định category"""
        # Placeholder for value-based classification
        # Could check email patterns, phone number formats, etc.
        return []
```

---

## Category Suggestion Engine

### Auto-Suggest with Approval Workflow

```python
# api/models/discovery_models.py

"""
Category Discovery Models
Vietnamese-first Auto-Discovery
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime


class CategorySuggestion(BaseModel):
    """
    Gợi ý danh mục dữ liệu
    Category suggestion from discovery
    
    AI-generated category classification
    """
    
    category_key: str
    category_name_vi: str
    category_name_en: str
    category_type: str
    is_sensitive: bool
    pdpl_article: str
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Độ tin cậy (0.0-1.0) | Confidence score (0.0-1.0)"
    )
    
    matched_pattern: str
    detection_method: str
    
    source_columns: List[str] = Field(
        default_factory=list,
        description="Các cột nguồn | Source columns"
    )
    
    suggested_description_vi: Optional[str]
    suggested_description_en: Optional[str]
    suggested_examples_vi: Optional[List[str]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "category_key": "health_data",
                "category_name_vi": "Thông tin sức khỏe",
                "category_name_en": "Health Information",
                "category_type": "sensitive",
                "is_sensitive": True,
                "pdpl_article": "Art. 4.13 PDPL",
                "confidence": 0.92,
                "matched_pattern": "(?i)(sức khỏe|y tế|bệnh án)",
                "detection_method": "sensitive_pattern_match",
                "source_columns": ["ho_so_benh_an", "ket_qua_xet_nghiem"],
                "suggested_description_vi": "Thông tin về tình trạng sức khỏe, bệnh sử và kết quả xét nghiệm",
                "suggested_examples_vi": ["hồ sơ bệnh án", "kết quả xét nghiệm", "đơn thuốc"]
            }
        }


class DiscoverySessionResponse(BaseModel):
    """
    Phản hồi phiên phát hiện
    Discovery session response
    
    Results from database scan
    """
    
    session_id: UUID
    database_type: str
    tables_scanned: int
    columns_analyzed: int
    
    categories_suggested: int
    sensitive_categories: int
    basic_categories: int
    
    suggestions: List[CategorySuggestion]
    
    high_confidence_count: int  # confidence >= 0.8
    medium_confidence_count: int  # 0.5 <= confidence < 0.8
    low_confidence_count: int  # confidence < 0.5
    
    requires_review: bool
    
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "ff0e8400-e29b-41d4-a716-446655440010",
                "database_type": "mysql",
                "tables_scanned": 15,
                "columns_analyzed": 87,
                "categories_suggested": 12,
                "sensitive_categories": 3,
                "basic_categories": 9,
                "suggestions": [],
                "high_confidence_count": 8,
                "medium_confidence_count": 3,
                "low_confidence_count": 1,
                "requires_review": True,
                "created_at": "2025-11-06T20:00:00+07:00"
            }
        }


class ApprovalRequest(BaseModel):
    """
    Yêu cầu phê duyệt gợi ý
    Approval request for suggestions
    
    User approves/rejects category suggestions
    """
    
    session_id: UUID
    approved_categories: List[str] = Field(
        ...,
        description="Danh sách category_key được phê duyệt | Approved category keys"
    )
    
    rejected_categories: List[str] = Field(
        default_factory=list,
        description="Danh sách category_key bị từ chối | Rejected category keys"
    )
    
    create_approved: bool = Field(
        default=True,
        description="Tạo danh mục đã phê duyệt | Create approved categories"
    )
```

---

## Multi-Database Scanner

### Database Connection and Schema Analysis

```python
# services/discovery/database_scanner.py

"""
Multi-Database Schema Scanner
Vietnamese Column Pattern Detection
"""

from typing import Dict, List
from sqlalchemy import create_engine, inspect
import pymongo


class DatabaseSchemaScanner:
    """
    Quét schema database
    Database schema scanner
    
    Multi-database support for discovery
    """
    
    def __init__(self, connection_string: str, db_type: str):
        self.connection_string = connection_string
        self.db_type = db_type
        self.classifier = VietnameseNLPClassifier()
    
    async def scan_schema(self) -> List[Dict[str, any]]:
        """
        Quét schema database
        Scan database schema
        
        Returns column analysis results
        """
        if self.db_type in ['mysql', 'postgresql', 'mssql']:
            return await self._scan_sql_database()
        elif self.db_type == 'mongodb':
            return await self._scan_mongodb()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
    
    async def _scan_sql_database(self) -> List[Dict[str, any]]:
        """Quét SQL database (MySQL, PostgreSQL, SQL Server)"""
        engine = create_engine(self.connection_string)
        inspector = inspect(engine)
        
        results = []
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            
            for column in columns:
                column_name = column['name']
                
                # Classify column
                suggestions = self.classifier.classify_column(
                    column_name=column_name,
                    table_name=table_name
                )
                
                if suggestions:
                    results.append({
                        "table_name": table_name,
                        "column_name": column_name,
                        "column_type": str(column['type']),
                        "suggestions": suggestions
                    })
        
        return results
    
    async def _scan_mongodb(self) -> List[Dict[str, any]]:
        """Quét MongoDB collections"""
        client = pymongo.MongoClient(self.connection_string)
        db = client.get_default_database()
        
        results = []
        
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            
            # Sample document to analyze fields
            sample = collection.find_one()
            
            if sample:
                for field_name in sample.keys():
                    if field_name == '_id':
                        continue
                    
                    suggestions = self.classifier.classify_column(
                        column_name=field_name,
                        table_name=collection_name
                    )
                    
                    if suggestions:
                        results.append({
                            "collection_name": collection_name,
                            "field_name": field_name,
                            "suggestions": suggestions
                        })
        
        return results
```

---

## Confidence Scoring

### AI Confidence Calculation

```python
# services/discovery/confidence_scorer.py

"""
Confidence Scoring for Category Suggestions
Vietnamese Pattern Matching Quality
"""

from typing import Dict


class ConfidenceScorer:
    """
    Tính điểm tin cậy
    Confidence scorer for suggestions
    
    Calculates AI confidence levels
    """
    
    # Confidence thresholds
    HIGH_CONFIDENCE = 0.8
    MEDIUM_CONFIDENCE = 0.5
    
    def calculate_aggregate_confidence(
        self,
        pattern_match_score: float,
        context_score: float,
        sample_value_score: float = 0.0
    ) -> float:
        """
        Tính điểm tin cậy tổng hợp
        Calculate aggregate confidence
        
        Weighted average of multiple signals
        """
        weights = {
            "pattern": 0.6,
            "context": 0.3,
            "sample": 0.1
        }
        
        total_score = (
            pattern_match_score * weights["pattern"] +
            context_score * weights["context"] +
            sample_value_score * weights["sample"]
        )
        
        return min(total_score, 1.0)
    
    def get_confidence_level(self, score: float) -> str:
        """
        Xác định mức độ tin cậy
        Get confidence level label
        """
        if score >= self.HIGH_CONFIDENCE:
            return "high"
        elif score >= self.MEDIUM_CONFIDENCE:
            return "medium"
        else:
            return "low"
    
    def get_confidence_level_vi(self, score: float) -> str:
        """Mức độ tin cậy tiếng Việt"""
        level = self.get_confidence_level(score)
        
        translations = {
            "high": "Cao",
            "medium": "Trung bình",
            "low": "Thấp"
        }
        
        return translations.get(level, "Không xác định")
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] PDPL Article 4.13 sensitive pattern detection (9 categories)
- [TARGET] Basic personal data pattern detection (7 categories)
- [TARGET] Vietnamese NLP column name classifier
- [TARGET] Multi-database scanner (MySQL, PostgreSQL, SQL Server, MongoDB)
- [TARGET] Confidence scoring (0.0-1.0 scale)
- [TARGET] Category suggestion engine with templates
- [TARGET] Approval workflow for AI suggestions
- [TARGET] High/medium/low confidence classification
- [TARGET] Zero hard-coding (all patterns in configuration)
- [TARGET] Bilingual suggestions (Vietnamese-first)

**Next Document:** #03 - Bulk Import CSV/Excel
