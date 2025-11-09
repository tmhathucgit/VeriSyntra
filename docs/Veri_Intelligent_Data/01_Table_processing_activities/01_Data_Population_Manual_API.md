# Data Population Method 1: Manual Data Entry via API
## Vietnamese PDPL 2025 Compliance - Processing Activities Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** processing_activities Table  
**Method:** Manual API Entry (Primary Method)  
**Architecture:** Vietnamese-first Bilingual REST API  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **manual data entry** into the `processing_activities` table via RESTful API endpoints. This is the **primary method** for Vietnamese compliance officers to enter ROPA data through VeriPortal UI.

**Key Features:**
- Vietnamese-first bilingual API (Vietnamese primary, English secondary)
- Zero hard-coding architecture with named constants
- PDPL Article 12 compliance validation
- Multi-tenant isolation enforced
- Complete audit trail

---

## Table of Contents

1. [Authentication & Authorization](#authentication--authorization)
2. [API Endpoints Design](#api-endpoints-design)
3. [Request/Response Models](#requestresponse-models)
4. [CRUD Operations Implementation](#crud-operations-implementation)
5. [Validation Rules](#validation-rules)
6. [Error Handling](#error-handling)
7. [Usage Examples](#usage-examples)

---

## Authentication & Authorization

### Overview

**Phase 7 Integration:** All API endpoints require JWT-based authentication with Role-Based Access Control (RBAC).

**Authentication Method:** JWT Bearer Token  
**Token Type:** Access token (30-minute expiration)  
**Authorization:** Role-based permissions checked per endpoint

### Required Roles & Permissions

**Roles Hierarchy:**
- **admin** (Quản trị viên): Full system access, all permissions
- **compliance_officer** (Cán bộ tuân thủ): Read/write ROPA and processing activities, export
- **data_processor** (Người xử lý dữ liệu): Read/write processing activities, read ROPA
- **viewer** (Người xem): Read-only access to ROPA and processing activities

**Endpoint Permissions:**

| Endpoint | HTTP Method | Required Permission | Roles Allowed |
|----------|-------------|---------------------|---------------|
| `/api/v1/data-inventory/processing-activities` | POST | `processing_activity.write` | admin, compliance_officer, data_processor |
| `/api/v1/data-inventory/processing-activities` | GET | `processing_activity.read` | admin, compliance_officer, data_processor, viewer |
| `/api/v1/data-inventory/processing-activities/{id}` | GET | `processing_activity.read` | admin, compliance_officer, data_processor, viewer |
| `/api/v1/data-inventory/processing-activities/{id}` | PUT | `processing_activity.write` | admin, compliance_officer, data_processor |
| `/api/v1/data-inventory/processing-activities/{id}` | DELETE | `processing_activity.delete` | admin |

### Authentication Headers

**Required Header:**
```http
Authorization: Bearer <access_token>
```

**Example:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDIiLCJ0ZW5hbnRfaWQiOiI2NjBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDEiLCJyb2xlcyI6WyJkYXRhX3Byb2Nlc3NvciJdLCJleHAiOjE3MzEwMDAwMDAsImlhdCI6MTczMDk5ODIwMCwidHlwZSI6ImFjY2VzcyJ9.signature_here
```

**Token Payload (Decoded):**
```json
{
  "sub": "770e8400-e29b-41d4-a716-446655440002",  // user_id
  "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "roles": ["data_processor"],
  "exp": 1731000000,  // Expiration timestamp
  "iat": 1730998200,  // Issued at timestamp
  "type": "access"
}
```

### Authentication Error Responses

**401 Unauthorized - Missing Token:**
```json
{
  "error": "Not authenticated",
  "error_vi": "Chưa xác thực",
  "detail": "Authorization header missing"
}
```

**401 Unauthorized - Invalid Token:**
```json
{
  "error": "Invalid authentication credentials",
  "error_vi": "Thông tin xác thực không hợp lệ",
  "message": "Token expired"
}
```

**403 Forbidden - Insufficient Permissions:**
```json
{
  "error": "Insufficient permissions. Required: processing_activity.write",
  "error_vi": "Không đủ quyền. Cần: processing_activity.write",
  "required_permission": "processing_activity.write",
  "user_permissions": ["processing_activity.read", "ropa.read"]
}
```

**403 Forbidden - Tenant Mismatch:**
```json
{
  "error": "Access denied. Cannot access data from different tenant",
  "error_vi": "Truy cập bị từ chối. Không thể truy cập dữ liệu của tenant khác",
  "requested_tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "user_tenant_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Multi-Tenant Authorization

**Tenant Isolation Enforcement:**
- JWT token contains `tenant_id` claim
- All API operations validate user's `tenant_id` matches requested resource's `tenant_id`
- Users cannot access data from other tenants (even with admin role)
- Cross-tenant operations require special "super admin" privileges (future Phase 9)

**Validation Logic:**
```python
# auth/dependencies.py

async def get_current_tenant(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UUID:
    """
    Extract and validate tenant_id from JWT token
    
    Raises:
        HTTPException 401: If token invalid or missing tenant_id
    """
    try:
        token = credentials.credentials
        payload = verify_token(token, token_type="access")
        tenant_id = payload.get("tenant_id")
        
        if not tenant_id:
            raise ValueError("Token missing tenant_id")
        
        return UUID(tenant_id)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid tenant credentials",
                "error_vi": "Thông tin tenant không hợp lệ",
                "message": str(e)
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
```

### Obtaining Access Tokens

**Login Endpoint:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Login Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,  // 30 minutes in seconds
  "user": {
    "user_id": "770e8400-e29b-41d4-a716-446655440002",
    "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
    "email": "user@example.com",
    "full_name_vi": "Nguyễn Văn An",
    "roles": ["data_processor"]
  }
}
```

**Token Refresh Endpoint:**
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Refresh Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**See Also:**
- Phase 7 Documentation: `DOC12_PHASE_7_AUTH_IMPLEMENTATION_PLAN.md`
- Authentication endpoints: `/api/v1/auth/*`
- User management: `/api/v1/users/*`



### Endpoint Structure

```
POST   /api/v1/data-inventory/processing-activities          # Tạo hoạt động xử lý mới
GET    /api/v1/data-inventory/processing-activities          # Lấy danh sách hoạt động
GET    /api/v1/data-inventory/processing-activities/{id}     # Lấy chi tiết hoạt động
PUT    /api/v1/data-inventory/processing-activities/{id}     # Cập nhật hoạt động
DELETE /api/v1/data-inventory/processing-activities/{id}     # Xóa hoạt động
```

**Vietnamese-first Naming:**
- All response fields include `_vi` (primary, NOT NULL) and `_en` (secondary, nullable)
- Error messages bilingual with Vietnamese first
- Vietnamese timezone (Asia/Ho_Chi_Minh) throughout

---

## Request/Response Models

### Constants Definition

```python
# api/constants.py

"""
API Constants - Zero Hard-Coding Architecture
Vietnamese PDPL 2025 Compliance
"""

from enum import Enum
from typing import Dict

# Legal Basis Constants (Article 13.1 PDPL)
class LegalBasisType(str, Enum):
    """
    Cơ sở pháp lý xử lý dữ liệu (Art. 13.1 PDPL)
    Legal basis for data processing
    """
    CONSENT = "consent"                    # Sự đồng ý (Art. 13.1.a)
    CONTRACT = "contract"                  # Thực hiện hợp đồng (Art. 13.1.b)
    LEGAL_OBLIGATION = "legal_obligation"  # Nghĩa vụ pháp lý (Art. 13.1.c)
    VITAL_INTEREST = "vital_interest"      # Lợi ích sống còn (Art. 13.1.d)
    PUBLIC_INTEREST = "public_interest"    # Lợi ích công cộng (Art. 13.1.e)
    LEGITIMATE_INTEREST = "legitimate_interest"  # Lợi ích hợp pháp (Art. 13.1.f)


# Legal Basis Vietnamese Translations
LEGAL_BASIS_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    LegalBasisType.CONSENT: {
        "vi": "Sự đồng ý",
        "en": "Consent"
    },
    LegalBasisType.CONTRACT: {
        "vi": "Thực hiện hợp đồng",
        "en": "Contract performance"
    },
    LegalBasisType.LEGAL_OBLIGATION: {
        "vi": "Nghĩa vụ pháp lý",
        "en": "Legal obligation"
    },
    LegalBasisType.VITAL_INTEREST: {
        "vi": "Lợi ích sống còn",
        "en": "Vital interest"
    },
    LegalBasisType.PUBLIC_INTEREST: {
        "vi": "Lợi ích công cộng",
        "en": "Public interest"
    },
    LegalBasisType.LEGITIMATE_INTEREST: {
        "vi": "Lợi ích hợp pháp",
        "en": "Legitimate interest"
    }
}


# Regional Location Constants
class VeriRegionalLocation(str, Enum):
    """
    Vị trí khu vực Việt Nam
    Vietnamese regional location
    """
    NORTH = "north"      # Miền Bắc (Hà Nội)
    CENTRAL = "central"  # Miền Trung (Đà Nẵng, Huế)
    SOUTH = "south"      # Miền Nam (TP.HCM)


# Activity Status Constants
class ActivityStatus(str, Enum):
    """
    Trạng thái hoạt động xử lý
    Processing activity status
    """
    ACTIVE = "active"        # Đang hoạt động
    INACTIVE = "inactive"    # Tạm dừng
    ARCHIVED = "archived"    # Đã lưu trữ


# Status Vietnamese Translations
STATUS_TRANSLATIONS_VI: Dict[str, str] = {
    ActivityStatus.ACTIVE: "Đang hoạt động",
    ActivityStatus.INACTIVE: "Tạm dừng",
    ActivityStatus.ARCHIVED: "Đã lưu trữ"
}


# Status English Translations
STATUS_TRANSLATIONS_EN: Dict[str, str] = {
    ActivityStatus.ACTIVE: "Active",
    ActivityStatus.INACTIVE: "Inactive",
    ActivityStatus.ARCHIVED: "Archived"
}


# Validation Constants
MIN_ACTIVITY_NAME_LENGTH = 5  # Minimum 5 characters for activity name
MAX_ACTIVITY_NAME_LENGTH = 200  # Maximum 200 characters
MIN_PURPOSE_LENGTH = 10  # Minimum 10 characters for purpose description
```

---

### Request Model (Vietnamese-first)

```python
# api/models/processing_activity_models.py

"""
Processing Activity API Models
Vietnamese-first Bilingual Support
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

from api.constants import (
    LegalBasisType,
    VeriRegionalLocation,
    MIN_ACTIVITY_NAME_LENGTH,
    MAX_ACTIVITY_NAME_LENGTH,
    MIN_PURPOSE_LENGTH
)


class ProcessingActivityCreateRequest(BaseModel):
    """
    Yêu cầu tạo hoạt động xử lý mới
    Request to create new processing activity
    
    Vietnamese-first architecture:
    - _vi fields are required (primary)
    - _en fields are optional (secondary)
    """
    
    # Activity Name - Vietnamese-first (REQUIRED)
    activity_name_vi: str = Field(
        ...,
        min_length=MIN_ACTIVITY_NAME_LENGTH,
        max_length=MAX_ACTIVITY_NAME_LENGTH,
        description="Tên hoạt động xử lý (bắt buộc) | Activity name (required)"
    )
    activity_name_en: Optional[str] = Field(
        None,
        max_length=MAX_ACTIVITY_NAME_LENGTH,
        description="Tên hoạt động bằng tiếng Anh (tùy chọn) | Activity name in English (optional)"
    )
    
    # Activity Description - Vietnamese-first
    activity_description_vi: Optional[str] = Field(
        None,
        description="Mô tả hoạt động (tiếng Việt) | Activity description (Vietnamese)"
    )
    activity_description_en: Optional[str] = Field(
        None,
        description="Mô tả hoạt động (tiếng Anh) | Activity description (English)"
    )
    
    # Processing Purpose - Vietnamese-first (REQUIRED)
    processing_purpose_vi: str = Field(
        ...,
        min_length=MIN_PURPOSE_LENGTH,
        description="Mục đích xử lý (bắt buộc) | Processing purpose (required)"
    )
    processing_purpose_en: Optional[str] = Field(
        None,
        description="Mục đích xử lý (tiếng Anh, tùy chọn) | Processing purpose (English, optional)"
    )
    
    # Legal Basis (REQUIRED - Article 13.1 PDPL)
    legal_basis: LegalBasisType = Field(
        ...,
        description="Cơ sở pháp lý (Art. 13.1 PDPL) | Legal basis (Art. 13.1 PDPL)"
    )
    
    # Compliance Flags
    has_sensitive_data: bool = Field(
        default=False,
        description="Có dữ liệu nhạy cảm (Art. 4.13 PDPL) | Has sensitive data (Art. 4.13 PDPL)"
    )
    has_cross_border_transfer: bool = Field(
        default=False,
        description="Có chuyển giao xuyên biên giới (Art. 20 PDPL) | Has cross-border transfer (Art. 20 PDPL)"
    )
    requires_dpia: bool = Field(
        default=False,
        description="Yêu cầu đánh giá tác động (DPIA) | Requires impact assessment (DPIA)"
    )
    
    # Vietnamese Business Context
    veri_regional_location: Optional[VeriRegionalLocation] = Field(
        None,
        description="Vị trí khu vực (Bắc/Trung/Nam) | Regional location (North/Central/South)"
    )
    veri_business_unit: Optional[str] = Field(
        None,
        max_length=100,
        description="Đơn vị kinh doanh | Business unit"
    )
    
    @validator('activity_name_vi')
    def validate_activity_name_vi(cls, v):
        """Validate Vietnamese activity name has proper diacritics"""
        if not v or v.strip() == "":
            raise ValueError("Tên hoạt động không được để trống | Activity name cannot be empty")
        
        # Check for common non-diacritic mistakes
        # Các từ KHÔNG có dấu (sai): quản lý, khách hàng, nhân viên, dữ liệu
        non_diacritic_keywords = ["quan ly", "khach hang", "nhan vien", "du lieu"]
        v_lower = v.lower()
        for keyword in non_diacritic_keywords:
            if keyword in v_lower:
                raise ValueError(
                    f"Vui lòng sử dụng dấu tiếng Việt đúng (ví dụ: 'quản lý' thay vì 'quan ly') | "
                    f"Please use proper Vietnamese diacritics (e.g., 'quản lý' instead of 'quan ly')"
                )
        
        return v.strip()
    
    @validator('processing_purpose_vi')
    def validate_purpose_vi(cls, v):
        """Validate Vietnamese purpose description"""
        if not v or v.strip() == "":
            raise ValueError("Mục đích xử lý không được để trống | Processing purpose cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "activity_name_vi": "Quản lý quan hệ khách hàng",
                "activity_name_en": "Customer Relationship Management",
                "activity_description_vi": "Hệ thống quản lý thông tin và tương tác với khách hàng",
                "activity_description_en": "System for managing customer information and interactions",
                "processing_purpose_vi": "Lưu trữ và quản lý thông tin khách hàng để cung cấp dịch vụ tốt hơn",
                "processing_purpose_en": "Store and manage customer information to provide better services",
                "legal_basis": "contract",
                "has_sensitive_data": False,
                "has_cross_border_transfer": False,
                "requires_dpia": False,
                "veri_regional_location": "south",
                "veri_business_unit": "Phòng Kinh doanh TP.HCM"
            }
        }


class ProcessingActivityResponse(BaseModel):
    """
    Phản hồi hoạt động xử lý
    Processing activity response
    
    Vietnamese-first bilingual fields
    """
    
    # Identity
    activity_id: UUID
    tenant_id: UUID
    
    # Activity Details - Vietnamese-first
    activity_name_vi: str
    activity_name_en: Optional[str]
    activity_description_vi: Optional[str]
    activity_description_en: Optional[str]
    
    # Processing Purpose - Vietnamese-first
    processing_purpose_vi: str
    processing_purpose_en: Optional[str]
    
    # Legal Basis with Vietnamese translation
    legal_basis: str
    legal_basis_vi: str
    legal_basis_en: str
    
    # Status
    status: str
    status_vi: str  # Vietnamese translation
    status_en: str  # English translation
    
    # Compliance Flags
    has_sensitive_data: bool
    has_cross_border_transfer: bool
    requires_dpia: bool
    mps_reportable: bool
    
    # Vietnamese Context
    veri_regional_location: Optional[str]
    veri_business_unit: Optional[str]
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    last_reviewed_at: Optional[datetime]
    
    class Config:
        json_schema_extra = {
            "example": {
                "activity_id": "550e8400-e29b-41d4-a716-446655440000",
                "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
                "activity_name_vi": "Quản lý quan hệ khách hàng",
                "activity_name_en": "Customer Relationship Management",
                "processing_purpose_vi": "Lưu trữ và quản lý thông tin khách hàng",
                "processing_purpose_en": "Store and manage customer information",
                "legal_basis": "contract",
                "legal_basis_vi": "Thực hiện hợp đồng",
                "legal_basis_en": "Contract performance",
                "status": "active",
                "status_vi": "Đang hoạt động",
                "status_en": "Active",
                "has_sensitive_data": False,
                "has_cross_border_transfer": False,
                "requires_dpia": False,
                "mps_reportable": True,
                "veri_regional_location": "south",
                "veri_business_unit": "Phòng Kinh doanh TP.HCM",
                "created_at": "2025-11-06T10:30:00+07:00",
                "updated_at": "2025-11-06T10:30:00+07:00",
                "created_by": "770e8400-e29b-41d4-a716-446655440002",
                "last_reviewed_at": None
            }
        }
```

---

## CRUD Operations Implementation

### CREATE Operation

```python
# api/endpoints/processing_activity_endpoints.py

"""
Processing Activity API Endpoints
Vietnamese-first Bilingual REST API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from database.connection import get_db
from api.models.processing_activity_models import (
    ProcessingActivityCreateRequest,
    ProcessingActivityResponse
)
from api.constants import (
    LEGAL_BASIS_TRANSLATIONS,
    STATUS_TRANSLATIONS_VI,
    STATUS_TRANSLATIONS_EN
)
from crud.processing_activity import create_processing_activity
from crud.audit import create_audit_log
from auth.dependencies import get_current_user, get_current_tenant
from auth.rbac import require_permission


router = APIRouter(
    prefix="/api/v1/data-inventory/processing-activities",
    tags=["Processing Activities | Hoạt động Xử lý Dữ liệu"]
)


@router.post(
    "",
    response_model=ProcessingActivityResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("processing_activity.write"))],
    summary="Tạo hoạt động xử lý mới | Create new processing activity",
    description="""
    **Vietnamese:** Tạo hoạt động xử lý dữ liệu cá nhân mới theo yêu cầu của Điều 12 PDPL.
    
    **English:** Create new personal data processing activity per Article 12 PDPL requirements.
    
    **Authentication:** JWT Bearer Token required
    **Permission:** `processing_activity.write`
    **Allowed Roles:** admin, compliance_officer, data_processor
    
    **Required fields (Vietnamese primary):**
    - activity_name_vi: Tên hoạt động (bắt buộc)
    - processing_purpose_vi: Mục đích xử lý (bắt buộc)
    - legal_basis: Cơ sở pháp lý (bắt buộc, theo Art. 13.1 PDPL)
    """
)
async def create_processing_activity_endpoint(
    request: ProcessingActivityCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> ProcessingActivityResponse:
    """
    Tạo hoạt động xử lý mới
    Create new processing activity
    
    Vietnamese-first implementation with zero hard-coding
    
    Authentication:
    - Requires JWT Bearer token in Authorization header
    - Tenant ID extracted from token (not from request parameter)
    - Permission 'processing_activity.write' required
    - User must belong to the same tenant as the activity being created
    """
    try:
        # Get legal basis translations (no hard-coding)
        legal_basis_translation = LEGAL_BASIS_TRANSLATIONS[request.legal_basis]
        
        # Create activity (tenant_id from JWT token, not request parameter)
        activity = await create_processing_activity(
            db=db,
            tenant_id=current_tenant,  # From JWT token
            activity_name_vi=request.activity_name_vi,
            activity_name_en=request.activity_name_en,
            activity_description_vi=request.activity_description_vi,
            activity_description_en=request.activity_description_en,
            processing_purpose_vi=request.processing_purpose_vi,
            processing_purpose_en=request.processing_purpose_en,
            legal_basis=request.legal_basis.value,
            legal_basis_vi=legal_basis_translation["vi"],
            has_sensitive_data=request.has_sensitive_data,
            has_cross_border_transfer=request.has_cross_border_transfer,
            requires_dpia=request.requires_dpia,
            veri_regional_location=request.veri_regional_location.value if request.veri_regional_location else None,
            veri_business_unit=request.veri_business_unit,
            created_by=current_user
        )
        
        # Create audit log (Vietnamese-first)
        await create_audit_log(
            db=db,
            tenant_id=current_tenant,  # From JWT token
            action_type="create",
            entity_type="processing_activity",
            entity_id=activity.activity_id,
            user_id=current_user,  # From JWT token
            audit_message_vi=f"Tạo hoạt động xử lý: {request.activity_name_vi}",
            audit_message_en=f"Created processing activity: {request.activity_name_en or request.activity_name_vi}",
            new_values={
                "activity_name_vi": request.activity_name_vi,
                "legal_basis": request.legal_basis.value
            }
        )
        
        # Build response with Vietnamese-first translations
        return ProcessingActivityResponse(
            activity_id=activity.activity_id,
            tenant_id=activity.tenant_id,
            activity_name_vi=activity.activity_name_vi,
            activity_name_en=activity.activity_name_en,
            activity_description_vi=activity.activity_description_vi,
            activity_description_en=activity.activity_description_en,
            processing_purpose_vi=activity.processing_purpose_vi,
            processing_purpose_en=activity.processing_purpose_en,
            legal_basis=activity.legal_basis,
            legal_basis_vi=legal_basis_translation["vi"],
            legal_basis_en=legal_basis_translation["en"],
            status=activity.status,
            status_vi=_get_status_translation_vi(activity.status),
            status_en=_get_status_translation_en(activity.status),
            has_sensitive_data=activity.has_sensitive_data,
            has_cross_border_transfer=activity.has_cross_border_transfer,
            requires_dpia=activity.requires_dpia,
            mps_reportable=activity.mps_reportable,
            veri_regional_location=activity.veri_regional_location,
            veri_business_unit=activity.veri_business_unit,
            created_at=activity.created_at,
            updated_at=activity.updated_at,
            created_by=activity.created_by,
            last_reviewed_at=activity.last_reviewed_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to create processing activity",
                "error_vi": "Không thể tạo hoạt động xử lý",
                "message": str(e)
            }
        )


### READ Operations (GET)

```python
@router.get(
    "",
    response_model=List[ProcessingActivityResponse],
    dependencies=[Depends(require_permission("processing_activity.read"))],
    summary="Lấy danh sách hoạt động xử lý | List processing activities",
    description="""
    **Vietnamese:** Lấy danh sách tất cả hoạt động xử lý dữ liệu trong tenant.
    
    **English:** Retrieve list of all processing activities in tenant.
    
    **Authentication:** JWT Bearer Token required
    **Permission:** `processing_activity.read`
    **Allowed Roles:** admin, compliance_officer, data_processor, viewer
    """
)
async def list_processing_activities(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> List[ProcessingActivityResponse]:
    """
    Lấy danh sách hoạt động xử lý
    List processing activities
    
    Authentication:
    - Requires JWT Bearer token
    - Returns only activities from user's tenant
    - Permission 'processing_activity.read' required
    """
    try:
        from crud.processing_activity import get_processing_activities_by_tenant
        
        # Get activities for current tenant only (from JWT token)
        activities = await get_processing_activities_by_tenant(
            db=db,
            tenant_id=current_tenant,
            skip=skip,
            limit=limit
        )
        
        # Build response list
        response_list = []
        for activity in activities:
            legal_basis_translation = LEGAL_BASIS_TRANSLATIONS.get(activity.legal_basis, {})
            
            response_list.append(ProcessingActivityResponse(
                activity_id=activity.activity_id,
                tenant_id=activity.tenant_id,
                activity_name_vi=activity.activity_name_vi,
                activity_name_en=activity.activity_name_en,
                activity_description_vi=activity.activity_description_vi,
                activity_description_en=activity.activity_description_en,
                processing_purpose_vi=activity.processing_purpose_vi,
                processing_purpose_en=activity.processing_purpose_en,
                legal_basis=activity.legal_basis,
                legal_basis_vi=legal_basis_translation.get("vi", activity.legal_basis),
                legal_basis_en=legal_basis_translation.get("en", activity.legal_basis),
                status=activity.status,
                status_vi=_get_status_translation_vi(activity.status),
                status_en=_get_status_translation_en(activity.status),
                has_sensitive_data=activity.has_sensitive_data,
                has_cross_border_transfer=activity.has_cross_border_transfer,
                requires_dpia=activity.requires_dpia,
                mps_reportable=activity.mps_reportable,
                veri_regional_location=activity.veri_regional_location,
                veri_business_unit=activity.veri_business_unit,
                created_at=activity.created_at,
                updated_at=activity.updated_at,
                created_by=activity.created_by,
                last_reviewed_at=activity.last_reviewed_at
            ))
        
        return response_list
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to retrieve processing activities",
                "error_vi": "Không thể lấy danh sách hoạt động xử lý",
                "message": str(e)
            }
        )


@router.get(
    "/{activity_id}",
    response_model=ProcessingActivityResponse,
    dependencies=[Depends(require_permission("processing_activity.read"))],
    summary="Lấy chi tiết hoạt động xử lý | Get processing activity details",
    description="""
    **Vietnamese:** Lấy thông tin chi tiết một hoạt động xử lý dữ liệu.
    
    **English:** Retrieve detailed information of a processing activity.
    
    **Authentication:** JWT Bearer Token required
    **Permission:** `processing_activity.read`
    **Allowed Roles:** admin, compliance_officer, data_processor, viewer
    """
)
async def get_processing_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> ProcessingActivityResponse:
    """
    Lấy chi tiết hoạt động xử lý
    Get processing activity details
    
    Authentication:
    - Requires JWT Bearer token
    - Validates activity belongs to user's tenant
    - Permission 'processing_activity.read' required
    """
    try:
        from crud.processing_activity import get_processing_activity_by_id
        
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
                    "error": "Access denied. Cannot access data from different tenant",
                    "error_vi": "Truy cập bị từ chối. Không thể truy cập dữ liệu của tenant khác",
                    "requested_tenant_id": str(activity.tenant_id),
                    "user_tenant_id": str(current_tenant)
                }
            )
        
        # Build response
        legal_basis_translation = LEGAL_BASIS_TRANSLATIONS.get(activity.legal_basis, {})
        
        return ProcessingActivityResponse(
            activity_id=activity.activity_id,
            tenant_id=activity.tenant_id,
            activity_name_vi=activity.activity_name_vi,
            activity_name_en=activity.activity_name_en,
            activity_description_vi=activity.activity_description_vi,
            activity_description_en=activity.activity_description_en,
            processing_purpose_vi=activity.processing_purpose_vi,
            processing_purpose_en=activity.processing_purpose_en,
            legal_basis=activity.legal_basis,
            legal_basis_vi=legal_basis_translation.get("vi", activity.legal_basis),
            legal_basis_en=legal_basis_translation.get("en", activity.legal_basis),
            status=activity.status,
            status_vi=_get_status_translation_vi(activity.status),
            status_en=_get_status_translation_en(activity.status),
            has_sensitive_data=activity.has_sensitive_data,
            has_cross_border_transfer=activity.has_cross_border_transfer,
            requires_dpia=activity.requires_dpia,
            mps_reportable=activity.mps_reportable,
            veri_regional_location=activity.veri_regional_location,
            veri_business_unit=activity.veri_business_unit,
            created_at=activity.created_at,
            updated_at=activity.updated_at,
            created_by=activity.created_by,
            last_reviewed_at=activity.last_reviewed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to retrieve processing activity",
                "error_vi": "Không thể lấy thông tin hoạt động xử lý",
                "message": str(e)
            }
        )


### UPDATE Operation (PUT)

```python
@router.put(
    "/{activity_id}",
    response_model=ProcessingActivityResponse,
    dependencies=[Depends(require_permission("processing_activity.write"))],
    summary="Cập nhật hoạt động xử lý | Update processing activity",
    description="""
    **Vietnamese:** Cập nhật thông tin hoạt động xử lý dữ liệu.
    
    **English:** Update processing activity information.
    
    **Authentication:** JWT Bearer Token required
    **Permission:** `processing_activity.write`
    **Allowed Roles:** admin, compliance_officer, data_processor
    """
)
async def update_processing_activity_endpoint(
    activity_id: UUID,
    request: ProcessingActivityCreateRequest,  # Reuse create model for update
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
) -> ProcessingActivityResponse:
    """
    Cập nhật hoạt động xử lý
    Update processing activity
    
    Authentication:
    - Requires JWT Bearer token
    - Validates activity belongs to user's tenant
    - Permission 'processing_activity.write' required
    - Audit trail created for changes
    """
    try:
        from crud.processing_activity import get_processing_activity_by_id, update_processing_activity
        
        # Get existing activity
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
                    "error": "Access denied. Cannot modify data from different tenant",
                    "error_vi": "Truy cập bị từ chối. Không thể sửa đổi dữ liệu của tenant khác",
                    "requested_tenant_id": str(activity.tenant_id),
                    "user_tenant_id": str(current_tenant)
                }
            )
        
        # Get legal basis translations
        legal_basis_translation = LEGAL_BASIS_TRANSLATIONS[request.legal_basis]
        
        # Update activity
        updated_activity = await update_processing_activity(
            db=db,
            activity_id=activity_id,
            activity_name_vi=request.activity_name_vi,
            activity_name_en=request.activity_name_en,
            activity_description_vi=request.activity_description_vi,
            activity_description_en=request.activity_description_en,
            processing_purpose_vi=request.processing_purpose_vi,
            processing_purpose_en=request.processing_purpose_en,
            legal_basis=request.legal_basis.value,
            legal_basis_vi=legal_basis_translation["vi"],
            has_sensitive_data=request.has_sensitive_data,
            has_cross_border_transfer=request.has_cross_border_transfer,
            requires_dpia=request.requires_dpia,
            veri_regional_location=request.veri_regional_location.value if request.veri_regional_location else None,
            veri_business_unit=request.veri_business_unit
        )
        
        # Create audit log
        await create_audit_log(
            db=db,
            tenant_id=current_tenant,
            action_type="update",
            entity_type="processing_activity",
            entity_id=activity_id,
            user_id=current_user,
            audit_message_vi=f"Cập nhật hoạt động xử lý: {request.activity_name_vi}",
            audit_message_en=f"Updated processing activity: {request.activity_name_en or request.activity_name_vi}",
            old_values={
                "activity_name_vi": activity.activity_name_vi,
                "legal_basis": activity.legal_basis
            },
            new_values={
                "activity_name_vi": request.activity_name_vi,
                "legal_basis": request.legal_basis.value
            }
        )
        
        # Build response
        return ProcessingActivityResponse(
            activity_id=updated_activity.activity_id,
            tenant_id=updated_activity.tenant_id,
            activity_name_vi=updated_activity.activity_name_vi,
            activity_name_en=updated_activity.activity_name_en,
            activity_description_vi=updated_activity.activity_description_vi,
            activity_description_en=updated_activity.activity_description_en,
            processing_purpose_vi=updated_activity.processing_purpose_vi,
            processing_purpose_en=updated_activity.processing_purpose_en,
            legal_basis=updated_activity.legal_basis,
            legal_basis_vi=legal_basis_translation["vi"],
            legal_basis_en=legal_basis_translation["en"],
            status=updated_activity.status,
            status_vi=_get_status_translation_vi(updated_activity.status),
            status_en=_get_status_translation_en(updated_activity.status),
            has_sensitive_data=updated_activity.has_sensitive_data,
            has_cross_border_transfer=updated_activity.has_cross_border_transfer,
            requires_dpia=updated_activity.requires_dpia,
            mps_reportable=updated_activity.mps_reportable,
            veri_regional_location=updated_activity.veri_regional_location,
            veri_business_unit=updated_activity.veri_business_unit,
            created_at=updated_activity.created_at,
            updated_at=updated_activity.updated_at,
            created_by=updated_activity.created_by,
            last_reviewed_at=updated_activity.last_reviewed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to update processing activity",
                "error_vi": "Không thể cập nhật hoạt động xử lý",
                "message": str(e)
            }
        )


### DELETE Operation

```python
@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("processing_activity.delete"))],
    summary="Xóa hoạt động xử lý | Delete processing activity",
    description="""
    **Vietnamese:** Xóa hoạt động xử lý dữ liệu (soft delete).
    
    **English:** Delete processing activity (soft delete).
    
    **Authentication:** JWT Bearer Token required
    **Permission:** `processing_activity.delete`
    **Allowed Roles:** admin only
    
    **Note:** This is a soft delete. Data is marked as deleted but retained in database for audit purposes.
    """
)
async def delete_processing_activity_endpoint(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
    current_tenant: UUID = Depends(get_current_tenant)
):
    """
    Xóa hoạt động xử lý
    Delete processing activity
    
    Authentication:
    - Requires JWT Bearer token
    - Validates activity belongs to user's tenant
    - Permission 'processing_activity.delete' required (admin only)
    - Soft delete with audit trail
    """
    try:
        from crud.processing_activity import get_processing_activity_by_id, soft_delete_processing_activity
        
        # Get existing activity
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
                    "error": "Access denied. Cannot delete data from different tenant",
                    "error_vi": "Truy cập bị từ chối. Không thể xóa dữ liệu của tenant khác",
                    "requested_tenant_id": str(activity.tenant_id),
                    "user_tenant_id": str(current_tenant)
                }
            )
        
        # Soft delete activity
        await soft_delete_processing_activity(db, activity_id)
        
        # Create audit log
        await create_audit_log(
            db=db,
            tenant_id=current_tenant,
            action_type="delete",
            entity_type="processing_activity",
            entity_id=activity_id,
            user_id=current_user,
            audit_message_vi=f"Xóa hoạt động xử lý: {activity.activity_name_vi}",
            audit_message_en=f"Deleted processing activity: {activity.activity_name_en or activity.activity_name_vi}",
            old_values={
                "activity_name_vi": activity.activity_name_vi,
                "status": activity.status
            }
        )
        
        return  # 204 No Content
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to delete processing activity",
                "error_vi": "Không thể xóa hoạt động xử lý",
                "message": str(e)
            }
        )
```

---

# Helper functions for status translations (using constants - no hard-coding)
def _get_status_translation_vi(status: str) -> str:
    """
    Get Vietnamese translation for status
    
    Uses STATUS_TRANSLATIONS_VI constant (no hard-coding)
    """
    return STATUS_TRANSLATIONS_VI.get(status, status)


def _get_status_translation_en(status: str) -> str:
    """
    Get English translation for status
    
    Uses STATUS_TRANSLATIONS_EN constant (no hard-coding)
    """
    return STATUS_TRANSLATIONS_EN.get(status, status)
```

---

## Validation Rules

### Vietnamese-First Validation

```python
# api/validators/processing_activity_validators.py

"""
Processing Activity Validators
Vietnamese-first with proper diacritics enforcement
"""

from typing import Dict, List
import re


# Vietnamese diacritics validation
VIETNAMESE_DIACRITIC_PATTERN = re.compile(r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]', re.IGNORECASE)


def validate_vietnamese_text(text: str, field_name: str) -> Dict[str, str]:
    """
    Validate Vietnamese text has proper diacritics
    
    Returns bilingual error message if invalid
    """
    if not text:
        return {
            "valid": False,
            "error_vi": f"{field_name} không được để trống",
            "error_en": f"{field_name} cannot be empty"
        }
    
    # Check for Vietnamese diacritics
    has_diacritics = bool(VIETNAMESE_DIACRITIC_PATTERN.search(text))
    
    # Check for common non-diacritic Vietnamese words
    # Các từ KHÔNG có dấu để phát hiện lỗi: quản lý, khách hàng, nhân viên, dữ liệu, cơ sở, mục đích, thông tin, người dùng
    non_diacritic_words = [
        "quan ly", "khach hang", "nhan vien", "du lieu",
        "co so", "muc dich", "thong tin", "nguoi dung"
    ]
    
    text_lower = text.lower()
    found_non_diacritic = [word for word in non_diacritic_words if word in text_lower]
    
    if found_non_diacritic and not has_diacritics:
        return {
            "valid": False,
            "error_vi": f"Vui lòng sử dụng dấu tiếng Việt đúng. Ví dụ: 'quản lý' thay vì 'quan ly'",
            "error_en": f"Please use proper Vietnamese diacritics. Example: 'quản lý' instead of 'quan ly'"
        }
    
    return {"valid": True}


def validate_legal_basis_context(
    legal_basis: str,
    has_sensitive_data: bool,
    has_cross_border: bool
) -> Dict[str, str]:
    """
    Validate legal basis appropriate for context
    
    Returns bilingual validation result
    """
    # Consent required for sensitive data (Art. 13.1.a PDPL)
    if has_sensitive_data and legal_basis != "consent":
        return {
            "valid": False,
            "warning_vi": "Dữ liệu nhạy cảm thường yêu cầu sự đồng ý (Art. 13.1.a PDPL)",
            "warning_en": "Sensitive data typically requires consent (Art. 13.1.a PDPL)"
        }
    
    # Cross-border may need additional safeguards (Art. 20 PDPL)
    if has_cross_border:
        return {
            "valid": True,
            "info_vi": "Chuyển giao xuyên biên giới yêu cầu biện pháp bảo vệ bổ sung (Art. 20 PDPL)",
            "info_en": "Cross-border transfer requires additional safeguards (Art. 20 PDPL)"
        }
    
    return {"valid": True}
```

---

## Authenticated Usage Examples

### Example 1: Complete Workflow with Authentication

**Step 1: Login to obtain JWT tokens**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nguyen.van.an@verisyntra.vn",
    "password": "SecurePassword123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDIiLCJ0ZW5hbnRfaWQiOiI2NjBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDEiLCJyb2xlcyI6WyJkYXRhX3Byb2Nlc3NvciJdLCJleHAiOjE3MzEwMDAwMDAsImlhdCI6MTczMDk5ODIwMCwidHlwZSI6ImFjY2VzcyJ9.signature",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDIiLCJ0ZW5hbnRfaWQiOiI2NjBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDEiLCJleHAiOjE3MzE2MDAwMDAsImlhdCI6MTczMDk5ODIwMCwidHlwZSI6InJlZnJlc2gifQ.signature",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "user_id": "770e8400-e29b-41d4-a716-446655440002",
    "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
    "email": "nguyen.van.an@verisyntra.vn",
    "full_name_vi": "Nguyễn Văn An",
    "roles": ["data_processor"]
  }
}
```

**Step 2: Create processing activity with JWT token**

```bash
curl -X POST "http://localhost:8000/api/v1/data-inventory/processing-activities" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDIiLCJ0ZW5hbnRfaWQiOiI2NjBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDEiLCJyb2xlcyI6WyJkYXRhX3Byb2Nlc3NvciJdLCJleHAiOjE3MzEwMDAwMDAsImlhdCI6MTczMDk5ODIwMCwidHlwZSI6ImFjY2VzcyJ9.signature" \
  -d '{
    "activity_name_vi": "Quản lý hồ sơ nhân viên",
    "activity_name_en": "Employee Records Management",
    "activity_description_vi": "Quản lý thông tin cá nhân và hồ sơ công việc của nhân viên",
    "activity_description_en": "Manage personal information and work records of employees",
    "processing_purpose_vi": "Quản lý nguồn nhân lực, tính lương, và tuân thủ quy định lao động",
    "processing_purpose_en": "HR management, payroll processing, and labor law compliance",
    "legal_basis": "contract",
    "has_sensitive_data": true,
    "has_cross_border_transfer": false,
    "requires_dpia": false,
    "veri_regional_location": "south",
    "veri_business_unit": "Phòng Nhân sự TP.HCM"
  }'
```

**Response (201 Created):**
```json
{
  "activity_id": "880e8400-e29b-41d4-a716-446655440003",
  "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
  "activity_name_vi": "Quản lý hồ sơ nhân viên",
  "activity_name_en": "Employee Records Management",
  "activity_description_vi": "Quản lý thông tin cá nhân và hồ sơ công việc của nhân viên",
  "activity_description_en": "Manage personal information and work records of employees",
  "processing_purpose_vi": "Quản lý nguồn nhân lực, tính lương, và tuân thủ quy định lao động",
  "processing_purpose_en": "HR management, payroll processing, and labor law compliance",
  "legal_basis": "contract",
  "legal_basis_vi": "Thực hiện hợp đồng",
  "legal_basis_en": "Contract performance",
  "status": "active",
  "status_vi": "Đang hoạt động",
  "status_en": "Active",
  "has_sensitive_data": true,
  "has_cross_border_transfer": false,
  "requires_dpia": false,
  "mps_reportable": true,
  "veri_regional_location": "south",
  "veri_business_unit": "Phòng Nhân sự TP.HCM",
  "created_at": "2025-11-07T14:30:00+07:00",
  "updated_at": "2025-11-07T14:30:00+07:00",
  "created_by": "770e8400-e29b-41d4-a716-446655440002",
  "last_reviewed_at": null
}
```

**Step 3: List all activities (with authentication)**

```bash
curl -X GET "http://localhost:8000/api/v1/data-inventory/processing-activities?skip=0&limit=10" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDIiLCJ0ZW5hbnRfaWQiOiI2NjBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDEiLCJyb2xlcyI6WyJkYXRhX3Byb2Nlc3NvciJdLCJleHAiOjE3MzEwMDAwMDAsImlhdCI6MTczMDk5ODIwMCwidHlwZSI6ImFjY2VzcyJ9.signature"
```

**Response (200 OK):**
```json
[
  {
    "activity_id": "880e8400-e29b-41d4-a716-446655440003",
    "activity_name_vi": "Quản lý hồ sơ nhân viên",
    "legal_basis_vi": "Thực hiện hợp đồng",
    "status_vi": "Đang hoạt động",
    ...
  },
  {
    "activity_id": "990e8400-e29b-41d4-a716-446655440004",
    "activity_name_vi": "Hệ thống CRM khách hàng",
    "legal_basis_vi": "Sự đồng ý",
    "status_vi": "Đang hoạt động",
    ...
  }
]
```

### Example 2: Authentication Error Scenarios

**Missing Authorization Header:**

```bash
curl -X POST "http://localhost:8000/api/v1/data-inventory/processing-activities" \
  -H "Content-Type: application/json" \
  -d '{"activity_name_vi": "Test Activity"}'
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated",
  "error_vi": "Chưa xác thực",
  "detail": "Authorization header missing"
}
```

**Expired Token:**

```bash
curl -X GET "http://localhost:8000/api/v1/data-inventory/processing-activities" \
  -H "Authorization: Bearer expired_token_here"
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid authentication credentials",
  "error_vi": "Thông tin xác thực không hợp lệ",
  "message": "Token expired"
}
```

**Insufficient Permissions (viewer trying to create):**

```bash
# User with 'viewer' role attempting to create activity
curl -X POST "http://localhost:8000/api/v1/data-inventory/processing-activities" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer viewer_token_here" \
  -d '{
    "activity_name_vi": "Test Activity",
    "processing_purpose_vi": "Testing",
    "legal_basis": "consent"
  }'
```

**Response (403 Forbidden):**
```json
{
  "error": "Insufficient permissions. Required: processing_activity.write",
  "error_vi": "Không đủ quyền. Cần: processing_activity.write",
  "required_permission": "processing_activity.write",
  "user_permissions": ["processing_activity.read", "ropa.read"]
}
```

**Tenant Mismatch (accessing another tenant's data):**

```bash
# User from tenant A trying to access tenant B's activity
curl -X GET "http://localhost:8000/api/v1/data-inventory/processing-activities/tenant-b-activity-id" \
  -H "Authorization: Bearer tenant_a_user_token"
```

**Response (403 Forbidden):**
```json
{
  "error": "Access denied. Cannot access data from different tenant",
  "error_vi": "Truy cập bị từ chối. Không thể truy cập dữ liệu của tenant khác",
  "requested_tenant_id": "tenant-b-id",
  "user_tenant_id": "tenant-a-id"
}
```

### Example 3: Token Refresh Flow

**When access token expires (after 30 minutes):**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDIiLCJ0ZW5hbnRfaWQiOiI2NjBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDEiLCJleHAiOjE3MzE2MDAwMDAsImlhdCI6MTczMDk5ODIwMCwidHlwZSI6InJlZnJlc2gifQ.signature"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new_access_token.signature",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Example 4: Python Client with Authentication

```python
import requests
from typing import Dict, Optional

class VeriSyntraClient:
    """
    VeriSyntra API Client with JWT Authentication
    Vietnamese-first PDPL 2025 Compliance
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    def login(self, email: str, password: str) -> Dict:
        """Login and store JWT tokens"""
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        
        return data["user"]
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        if not self.access_token:
            raise ValueError("Not authenticated. Call login() first.")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def create_processing_activity(self, activity_data: Dict) -> Dict:
        """Create new processing activity"""
        response = requests.post(
            f"{self.base_url}/api/v1/data-inventory/processing-activities",
            json=activity_data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def list_processing_activities(self, skip: int = 0, limit: int = 100) -> list:
        """List processing activities"""
        response = requests.get(
            f"{self.base_url}/api/v1/data-inventory/processing-activities",
            params={"skip": skip, "limit": limit},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_processing_activity(self, activity_id: str) -> Dict:
        """Get processing activity details"""
        response = requests.get(
            f"{self.base_url}/api/v1/data-inventory/processing-activities/{activity_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def update_processing_activity(self, activity_id: str, activity_data: Dict) -> Dict:
        """Update processing activity"""
        response = requests.put(
            f"{self.base_url}/api/v1/data-inventory/processing-activities/{activity_id}",
            json=activity_data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def delete_processing_activity(self, activity_id: str) -> None:
        """Delete processing activity (admin only)"""
        response = requests.delete(
            f"{self.base_url}/api/v1/data-inventory/processing-activities/{activity_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()
    
    def refresh_access_token(self) -> str:
        """Refresh access token"""
        if not self.refresh_token:
            raise ValueError("No refresh token available. Login again.")
        
        response = requests.post(
            f"{self.base_url}/api/v1/auth/refresh",
            json={"refresh_token": self.refresh_token}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data["access_token"]
        return self.access_token


# Usage example
if __name__ == "__main__":
    client = VeriSyntraClient()
    
    # Login
    user = client.login(
        email="nguyen.van.an@verisyntra.vn",
        password="SecurePassword123!"
    )
    print(f"Logged in as: {user['full_name_vi']} (Role: {user['roles'][0]})")
    
    # Create activity
    activity = client.create_processing_activity({
        "activity_name_vi": "Quản lý đơn hàng trực tuyến",
        "activity_name_en": "Online Order Management",
        "processing_purpose_vi": "Xử lý và giao hàng đơn đặt hàng của khách hàng",
        "processing_purpose_en": "Process and fulfill customer orders",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "veri_regional_location": "south"
    })
    print(f"Created activity: {activity['activity_id']}")
    
    # List activities
    activities = client.list_processing_activities(skip=0, limit=10)
    print(f"Found {len(activities)} activities")
    
    # Handle token refresh (after 30 minutes)
    try:
        activities = client.list_processing_activities()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Access token expired. Refreshing...")
            client.refresh_access_token()
            activities = client.list_processing_activities()
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] POST endpoint creates activities with Vietnamese-first fields
- [TARGET] All Vietnamese text validated for proper diacritics
- [TARGET] Legal basis auto-translated (Vietnamese/English)
- [TARGET] Zero hard-coding (all constants defined)
- [TARGET] Complete audit trail with bilingual messages
- [TARGET] Multi-tenant isolation enforced
- [TARGET] PDPL compliance validation active
- [PHASE 7] JWT authentication required on all endpoints
- [PHASE 7] RBAC permissions validated per endpoint (admin, compliance_officer, data_processor, viewer)
- [PHASE 7] Tenant isolation enforced via JWT token (no cross-tenant access)
- [PHASE 7] Bilingual authentication error messages (401, 403)
- [PHASE 7] Audit logs capture user_id from JWT token
- [PHASE 7] Token refresh flow implemented (30min access, 7day refresh)

**Phase 7 Integration Status:** DOCUMENTED (awaiting implementation)

---

## Performance Optimization: Phase 8 Batch Insert API

### When to Use Batch Insert vs. Individual POST

**Use Individual POST** (current endpoint) when:
- Creating 1-10 processing activities manually
- Interactive UI operations (user entering data one by one)
- Real-time validation feedback required per activity
- Low volume, human-driven data entry

**Use Batch Insert API** (Phase 8.1) when:
- Creating >100 processing activities at once
- Automated data scan results (database discovery)
- Bulk import from CSV/Excel files
- Migration from legacy systems
- Integration with third-party systems (Salesforce, SAP, HubSpot)

### Performance Comparison

| Operation | Individual POST | Batch Insert API | Performance Gain |
|-----------|----------------|------------------|------------------|
| Create 10 activities | 1.0 seconds | 0.5 seconds | 2x faster |
| Create 100 activities | 10 seconds | 1 second | 10x faster |
| Create 1,000 activities | 60 seconds | 2 seconds | **30x faster** |
| Create 10,000 activities | 600 seconds | 20 seconds | **30x faster** |

**Why 30x Faster:**
- **Single Network Round Trip:** 1 HTTP request instead of 1,000
- **Single Database Transaction:** Bulk INSERT instead of 1,000 individual INSERTs
- **Connection Pool Efficiency:** Uses write pool connection once instead of 1,000 times
- **Reduced Overhead:** Authentication validated once, not 1,000 times

### Batch Insert Endpoint

**Endpoint:**
```http
POST /api/v1/data-inventory/processing-activities/batch
```

**Authentication:** JWT Bearer Token required  
**Permission:** `processing_activity.write`  
**Allowed Roles:** admin, compliance_officer, data_processor

**Request Model:**

```python
class ProcessingActivityBatchCreate(BaseModel):
    """
    Batch create processing activities
    
    Accepts up to 10,000 activities in single request
    """
    activities: List[ProcessingActivityCreate] = Field(
        ...,
        min_items=1,
        max_items=10000,
        description="List of processing activities to create"
    )
```

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/v1/data-inventory/processing-activities/batch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "activities": [
      {
        "activity_name_vi": "Quản lý hồ sơ nhân viên",
        "activity_name_en": "Employee Records Management",
        "processing_purpose_vi": "Quản lý nguồn nhân lực",
        "processing_purpose_en": "HR management",
        "legal_basis": "contract",
        "has_sensitive_data": true,
        "has_cross_border_transfer": false,
        "requires_dpia": false,
        "veri_regional_location": "south"
      },
      {
        "activity_name_vi": "Hệ thống CRM khách hàng",
        "activity_name_en": "Customer CRM System",
        "processing_purpose_vi": "Quản lý quan hệ khách hàng",
        "processing_purpose_en": "Customer relationship management",
        "legal_basis": "consent",
        "has_sensitive_data": false,
        "has_cross_border_transfer": false,
        "requires_dpia": false,
        "veri_regional_location": "north"
      },
      ... // Up to 10,000 activities
    ]
  }'
```

**Response (201 Created):**

```json
{
  "message": "Batch insert completed successfully",
  "message_vi": "Chèn hàng loạt hoàn tất thành công",
  "total_submitted": 1000,
  "total_created": 995,
  "total_failed": 5,
  "activity_ids": [
    "880e8400-e29b-41d4-a716-446655440003",
    "990e8400-e29b-41d4-a716-446655440004",
    ...
  ],
  "errors": [
    {
      "index": 47,
      "activity_name_vi": "Hoạt động không hợp lệ",
      "error": "Missing required field: processing_purpose_vi",
      "error_vi": "Thiếu trường bắt buộc: processing_purpose_vi"
    },
    {
      "index": 152,
      "activity_name_vi": "Hoạt động trùng lặp",
      "error": "Duplicate activity name",
      "error_vi": "Tên hoạt động trùng lặp"
    }
  ],
  "duration_seconds": 2.34
}
```

### Partial Success Handling

The batch insert API supports **partial success**:
- If 995 out of 1,000 activities are valid, 995 will be created
- Failed records (5) are returned in `errors` array with details
- Client can retry failed records individually or fix and re-batch

**Error Response Fields:**
- `index`: Position in submitted array (0-based)
- `activity_name_vi`: Activity that failed (for identification)
- `error`: English error message
- `error_vi`: Vietnamese error message

### Recommendation for API Users

**Decision Logic:**

```python
def create_processing_activities(activities: List[dict]) -> None:
    """
    Intelligently choose between individual POST and batch insert
    
    Uses batch API for efficiency when creating >100 activities
    """
    if len(activities) <= 100:
        # Use individual POST for small batches
        # Better user feedback, easier error handling
        for activity in activities:
            response = requests.post(
                f"{base_url}/api/v1/data-inventory/processing-activities",
                json=activity,
                headers=auth_headers
            )
            response.raise_for_status()
    else:
        # Use batch insert for large volumes (>100)
        # 30x faster, single transaction
        response = requests.post(
            f"{base_url}/api/v1/data-inventory/processing-activities/batch",
            json={"activities": activities},
            headers=auth_headers
        )
        response.raise_for_status()
        
        # Handle partial failures
        result = response.json()
        if result['total_failed'] > 0:
            print(f"Warning: {result['total_failed']} activities failed")
            for error in result['errors']:
                print(f"  - Index {error['index']}: {error['error_vi']}")
```

### Integration with Data Population Methods

The following data population methods automatically use Phase 8.1 Batch Insert API when available:

1. **Automated Database Discovery** (Doc 02): Uses batch API for scan results (100-10,000 activities per scan)
2. **Bulk Import from CSV/Excel** (Doc 03): Switches to batch API for >100 rows
3. **Database Seeding** (Doc 05): Uses batch API for baseline 18 activities
4. **Third-Party Integration** (Doc 06): Uses batch API for Salesforce/SAP/HubSpot sync
5. **Alembic Migration** (Doc 07): Uses batch API for initial tenant setup

**Connection Pool Integration:**

Batch insert API uses the **write pool** from Phase 8.3:
- Min connections: 2
- Max connections: 10
- Dedicated to write operations (INSERT, UPDATE, DELETE)
- Prevents read operations from blocking writes

### See Also

- **Phase 8.1 Full Documentation:** `DOC13.1_PHASE_8.1_BATCH_INSERT_API.md`
- **Background Processing (>10,000 records):** Phase 8.2 - Celery async tasks
- **Connection Pool Configuration:** Phase 8.3 - Read/write separation
- **Performance Monitoring:** Phase 8.5 - Prometheus metrics for `batch_insert_duration`
- **Load Testing:** Phase 8.6 - Batch insert benchmarks

---

**Next Document:** #02 - Automated Database Discovery Method

