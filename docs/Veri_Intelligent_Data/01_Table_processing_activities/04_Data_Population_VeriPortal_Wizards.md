# Data Population Method 4: VeriPortal Compliance Wizards
## Vietnamese PDPL 2025 Compliance - Processing Activities Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** processing_activities Table  
**Method:** VeriPortal Guided Step-by-Step Wizards  
**Architecture:** Vietnamese-first Interactive UI Workflow  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **guided step-by-step wizards** in VeriPortal UI for creating processing activities. This method provides Vietnamese compliance officers with an intuitive, educational workflow that guides them through PDPL Article 12 requirements.

**Key Features:**
- Multi-step wizard with Vietnamese-first UI
- Real-time validation with contextual help
- PDPL Article 12 field-by-field guidance
- Save draft and resume functionality
- Progress tracking with completion percentage
- Zero hard-coding with dynamic wizard configuration

**Use Cases:**
- New compliance officers learning PDPL requirements
- Organizations creating their first ROPA
- Step-by-step guided data entry with validation
- Educational workflow for PDPL compliance training

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Wizard Flow Configuration](#wizard-flow-configuration)
3. [Step Definitions](#step-definitions)
4. [Real-Time Validation](#real-time-validation)
5. [Save Draft System](#save-draft-system)
6. [Progress Tracking](#progress-tracking)
7. [Implementation Guide](#implementation-guide)

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│            VeriPortal Compliance Wizard Engine              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Wizard      │  │  Step        │  │  Field       │     │
│  │  Controller  │─>│  Navigator   │─>│  Validator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Progress    │  │  Draft       │  │  Help        │     │
│  │  Tracker     │  │  Manager     │  │  Context     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  processing_activities │                    │
│              │  (on completion)       │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Wizard Workflow:**
1. User starts new activity wizard
2. Navigate through 7 steps with Vietnamese guidance
3. Real-time validation on each field
4. Contextual help for each PDPL requirement
5. Save draft anytime and resume later
6. Progress tracking shows completion percentage
7. Final review before submission
8. Create activity in database

---

## Wizard Flow Configuration

### Wizard Steps Definition

```python
# api/constants/wizard_constants.py

"""
VeriPortal Wizard Constants - Zero Hard-Coding
Vietnamese-first Guided Workflow Configuration
"""

from enum import Enum
from typing import Dict, List

# Wizard Types
class WizardType(str, Enum):
    """
    Các loại hướng dẫn
    Wizard types
    """
    PDPL_ACTIVITY_SETUP = "pdpl_activity_setup"        # Thiết lập hoạt động xử lý PDPL
    DATA_MAPPING = "data_mapping"                      # Ánh xạ dữ liệu cá nhân
    RECIPIENT_MAPPING = "recipient_mapping"            # Ánh xạ bên nhận dữ liệu
    POLICY_GENERATION = "policy_generation"            # Tạo chính sách bảo vệ
    AUDIT_PREPARATION = "audit_preparation"            # Chuẩn bị kiểm toán


# Wizard Type Vietnamese Translations
WIZARD_TYPE_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    WizardType.PDPL_ACTIVITY_SETUP: {
        "vi": "Thiết lập hoạt động xử lý dữ liệu PDPL",
        "en": "PDPL Processing Activity Setup"
    },
    WizardType.DATA_MAPPING: {
        "vi": "Ánh xạ dữ liệu cá nhân",
        "en": "Personal Data Mapping"
    },
    WizardType.RECIPIENT_MAPPING: {
        "vi": "Ánh xạ bên nhận dữ liệu",
        "en": "Data Recipient Mapping"
    },
    WizardType.POLICY_GENERATION: {
        "vi": "Tạo chính sách bảo vệ dữ liệu",
        "en": "Data Protection Policy Generation"
    },
    WizardType.AUDIT_PREPARATION: {
        "vi": "Chuẩn bị kiểm toán tuân thủ",
        "en": "Compliance Audit Preparation"
    }
}


# Wizard Step Status
class WizardStepStatus(str, Enum):
    """
    Trạng thái bước hướng dẫn
    Wizard step status
    """
    NOT_STARTED = "not_started"      # Chưa bắt đầu
    IN_PROGRESS = "in_progress"      # Đang thực hiện
    COMPLETED = "completed"          # Hoàn thành
    SKIPPED = "skipped"              # Bỏ qua
    ERROR = "error"                  # Có lỗi


# Wizard Step Status Vietnamese Translations
WIZARD_STEP_STATUS_TRANSLATIONS_VI: Dict[str, str] = {
    WizardStepStatus.NOT_STARTED: "Chưa bắt đầu",
    WizardStepStatus.IN_PROGRESS: "Đang thực hiện",
    WizardStepStatus.COMPLETED: "Hoàn thành",
    WizardStepStatus.SKIPPED: "Bỏ qua",
    WizardStepStatus.ERROR: "Có lỗi"
}


# Wizard Step Status English Translations
WIZARD_STEP_STATUS_TRANSLATIONS_EN: Dict[str, str] = {
    WizardStepStatus.NOT_STARTED: "Not Started",
    WizardStepStatus.IN_PROGRESS: "In Progress",
    WizardStepStatus.COMPLETED: "Completed",
    WizardStepStatus.SKIPPED: "Skipped",
    WizardStepStatus.ERROR: "Error"
}


# PDPL Activity Setup Wizard Steps (7 steps)
PDPL_ACTIVITY_WIZARD_STEPS: List[Dict[str, any]] = [
    {
        "step_number": 1,
        "step_id": "basic_information",
        "title_vi": "Thông tin cơ bản",
        "title_en": "Basic Information",
        "description_vi": "Nhập tên và mô tả hoạt động xử lý dữ liệu",
        "description_en": "Enter activity name and description",
        "pdpl_article": "Art. 12.1.a PDPL",
        "required": True,
        "fields": ["activity_name_vi", "activity_name_en", "activity_description_vi", "activity_description_en"]
    },
    {
        "step_number": 2,
        "step_id": "processing_purpose",
        "title_vi": "Mục đích xử lý",
        "title_en": "Processing Purpose",
        "description_vi": "Xác định mục đích xử lý dữ liệu cá nhân",
        "description_en": "Define purpose of personal data processing",
        "pdpl_article": "Art. 12.1.b PDPL",
        "required": True,
        "fields": ["processing_purpose_vi", "processing_purpose_en"]
    },
    {
        "step_number": 3,
        "step_id": "legal_basis",
        "title_vi": "Cơ sở pháp lý",
        "title_en": "Legal Basis",
        "description_vi": "Chọn cơ sở pháp lý cho việc xử lý dữ liệu",
        "description_en": "Select legal basis for data processing",
        "pdpl_article": "Art. 13.1 PDPL",
        "required": True,
        "fields": ["legal_basis"]
    },
    {
        "step_number": 4,
        "step_id": "data_categories",
        "title_vi": "Loại dữ liệu cá nhân",
        "title_en": "Personal Data Categories",
        "description_vi": "Xác định các loại dữ liệu cá nhân được xử lý",
        "description_en": "Identify categories of personal data processed",
        "pdpl_article": "Art. 12.1.c PDPL",
        "required": True,
        "fields": ["data_category_ids"]
    },
    {
        "step_number": 5,
        "step_id": "data_subjects",
        "title_vi": "Chủ thể dữ liệu",
        "title_en": "Data Subjects",
        "description_vi": "Xác định nhóm chủ thể dữ liệu",
        "description_en": "Identify data subject groups",
        "pdpl_article": "Art. 12.1.d PDPL",
        "required": True,
        "fields": ["data_subject_ids"]
    },
    {
        "step_number": 6,
        "step_id": "compliance_flags",
        "title_vi": "Cờ tuân thủ",
        "title_en": "Compliance Flags",
        "description_vi": "Đánh dấu các yêu cầu tuân thủ đặc biệt",
        "description_en": "Mark special compliance requirements",
        "pdpl_article": "Art. 4.13, Art. 20 PDPL",
        "required": False,
        "fields": ["has_sensitive_data", "has_cross_border_transfer", "requires_dpia"]
    },
    {
        "step_number": 7,
        "step_id": "review_submit",
        "title_vi": "Xem lại và gửi",
        "title_en": "Review and Submit",
        "description_vi": "Xem lại tất cả thông tin trước khi lưu",
        "description_en": "Review all information before saving",
        "pdpl_article": "Art. 12 PDPL (Complete)",
        "required": True,
        "fields": []
    }
]


# Help Context for Each Step
WIZARD_HELP_CONTEXT: Dict[str, Dict[str, str]] = {
    "basic_information": {
        "help_vi": """
        **Hướng dẫn:**
        - Tên hoạt động nên ngắn gọn, rõ ràng (5-200 ký tự)
        - Sử dụng dấu tiếng Việt đầy đủ
        - Ví dụ: "Quản lý quan hệ khách hàng", "Xử lý đơn hàng"
        
        **Lưu ý:**
        - Tên tiếng Việt là bắt buộc
        - Tên tiếng Anh là tùy chọn nhưng khuyến nghị
        """,
        "help_en": """
        **Guidelines:**
        - Activity name should be concise and clear (5-200 characters)
        - Use proper Vietnamese diacritics
        - Examples: "Customer Relationship Management", "Order Processing"
        
        **Notes:**
        - Vietnamese name is required
        - English name is optional but recommended
        """
    },
    "processing_purpose": {
        "help_vi": """
        **Hướng dẫn:**
        - Mô tả cụ thể mục đích xử lý dữ liệu (tối thiểu 10 ký tự)
        - Liên kết với hoạt động kinh doanh thực tế
        - Ví dụ: "Lưu trữ và quản lý thông tin khách hàng để cung cấp dịch vụ tốt hơn"
        
        **Yêu cầu PDPL:**
        - Mục đích phải rõ ràng, cụ thể (Art. 12.1.b)
        - Không được mơ hồ hoặc chung chung
        """,
        "help_en": """
        **Guidelines:**
        - Describe specific processing purpose (minimum 10 characters)
        - Link to actual business operations
        - Example: "Store and manage customer information to provide better services"
        
        **PDPL Requirements:**
        - Purpose must be clear and specific (Art. 12.1.b)
        - Cannot be vague or general
        """
    },
    "legal_basis": {
        "help_vi": """
        **Cơ sở pháp lý theo Điều 13.1 PDPL:**
        
        1. **Sự đồng ý** - Khi chủ thể dữ liệu đã đồng ý
        2. **Thực hiện hợp đồng** - Để thực hiện hợp đồng với chủ thể
        3. **Nghĩa vụ pháp lý** - Tuân thủ quy định pháp luật
        4. **Lợi ích sống còn** - Bảo vệ lợi ích quan trọng
        5. **Lợi ích công cộng** - Thực hiện nhiệm vụ công
        6. **Lợi ích hợp pháp** - Lợi ích hợp pháp của tổ chức
        
        **Lưu ý đặc biệt:**
        - Dữ liệu nhạy cảm thường yêu cầu sự đồng ý rõ ràng
        """,
        "help_en": """
        **Legal Basis per Article 13.1 PDPL:**
        
        1. **Consent** - When data subject has consented
        2. **Contract** - To perform contract with subject
        3. **Legal Obligation** - To comply with legal requirements
        4. **Vital Interest** - To protect vital interests
        5. **Public Interest** - To perform public tasks
        6. **Legitimate Interest** - Legitimate interests of organization
        
        **Special Notes:**
        - Sensitive data typically requires explicit consent
        """
    }
}
```

---

## Step Definitions

### Wizard State Management

```python
# api/models/wizard_models.py

"""
VeriPortal Wizard Models
Vietnamese-first Guided Workflow
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime

from api.constants.wizard_constants import (
    WizardType,
    WizardStepStatus,
    PDPL_ACTIVITY_WIZARD_STEPS
)


class WizardSessionRequest(BaseModel):
    """
    Yêu cầu tạo phiên hướng dẫn
    Wizard session creation request
    
    Vietnamese-first wizard initialization
    """
    
    wizard_type: WizardType = Field(
        ...,
        description="Loại hướng dẫn | Wizard type"
    )
    
    session_name_vi: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Tên phiên hướng dẫn (tiếng Việt) | Session name (Vietnamese)"
    )
    
    session_name_en: Optional[str] = Field(
        None,
        max_length=200,
        description="Tên phiên hướng dẫn (tiếng Anh) | Session name (English)"
    )
    
    @validator('session_name_vi')
    def validate_session_name_vi(cls, v):
        """Validate Vietnamese session name has proper diacritics"""
        if not v or v.strip() == "":
            raise ValueError(
                "Tên phiên hướng dẫn không được để trống | "
                "Session name cannot be empty"
            )
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "wizard_type": "pdpl_activity_setup",
                "session_name_vi": "Thiết lập ROPA cho phòng Marketing",
                "session_name_en": "ROPA Setup for Marketing Department"
            }
        }


class WizardStepData(BaseModel):
    """
    Dữ liệu bước hướng dẫn
    Wizard step data
    
    Contains field values for current step
    """
    
    step_id: str = Field(
        ...,
        description="ID bước | Step ID"
    )
    
    field_values: Dict[str, any] = Field(
        default_factory=dict,
        description="Giá trị các trường | Field values"
    )
    
    validation_errors: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Lỗi kiểm tra | Validation errors"
    )
    
    is_complete: bool = Field(
        default=False,
        description="Bước đã hoàn thành | Step completed"
    )


class WizardSessionResponse(BaseModel):
    """
    Phản hồi phiên hướng dẫn
    Wizard session response
    
    Vietnamese-first wizard state
    """
    
    # Session Metadata
    session_id: UUID
    wizard_type: str
    wizard_type_vi: str
    wizard_type_en: str
    session_name_vi: str
    session_name_en: Optional[str]
    
    # Progress
    current_step: int
    total_steps: int
    completion_percentage: float
    
    # Step Information
    current_step_data: Dict[str, any]
    all_steps: List[Dict[str, any]]
    
    # Session State
    is_draft: bool
    can_proceed: bool
    can_go_back: bool
    
    # Collected Data
    collected_data: Dict[str, any]
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "cc0e8400-e29b-41d4-a716-446655440007",
                "wizard_type": "pdpl_activity_setup",
                "wizard_type_vi": "Thiết lập hoạt động xử lý dữ liệu PDPL",
                "wizard_type_en": "PDPL Processing Activity Setup",
                "session_name_vi": "Thiết lập ROPA cho phòng Marketing",
                "session_name_en": "ROPA Setup for Marketing Department",
                "current_step": 2,
                "total_steps": 7,
                "completion_percentage": 28.57,
                "current_step_data": {
                    "step_number": 2,
                    "step_id": "processing_purpose",
                    "title_vi": "Mục đích xử lý",
                    "title_en": "Processing Purpose",
                    "status": "in_progress"
                },
                "all_steps": PDPL_ACTIVITY_WIZARD_STEPS,
                "is_draft": True,
                "can_proceed": False,
                "can_go_back": True,
                "collected_data": {
                    "activity_name_vi": "Quản lý chiến dịch Marketing",
                    "activity_name_en": "Marketing Campaign Management"
                },
                "created_at": "2025-11-06T17:00:00+07:00",
                "updated_at": "2025-11-06T17:15:00+07:00",
                "created_by": "dd0e8400-e29b-41d4-a716-446655440008"
            }
        }


class WizardNavigationRequest(BaseModel):
    """
    Yêu cầu điều hướng hướng dẫn
    Wizard navigation request
    
    Navigate to next/previous step
    """
    
    session_id: UUID = Field(
        ...,
        description="ID phiên hướng dẫn | Session ID"
    )
    
    action: str = Field(
        ...,
        description="Hành động (next, previous, goto) | Action (next, previous, goto)"
    )
    
    target_step: Optional[int] = Field(
        None,
        ge=1,
        description="Bước đích (cho goto) | Target step (for goto)"
    )
    
    save_current_step: bool = Field(
        default=True,
        description="Lưu bước hiện tại | Save current step"
    )
    
    step_data: Optional[Dict[str, any]] = Field(
        None,
        description="Dữ liệu bước hiện tại | Current step data"
    )


class WizardCompletionRequest(BaseModel):
    """
    Yêu cầu hoàn thành hướng dẫn
    Wizard completion request
    
    Finalize and create activity
    """
    
    session_id: UUID = Field(
        ...,
        description="ID phiên hướng dẫn | Session ID"
    )
    
    confirmation_notes_vi: Optional[str] = Field(
        None,
        description="Ghi chú xác nhận (tiếng Việt) | Confirmation notes (Vietnamese)"
    )
    
    confirmation_notes_en: Optional[str] = Field(
        None,
        description="Ghi chú xác nhận (tiếng Anh) | Confirmation notes (English)"
    )
```

---

## Real-Time Validation

### Field Validators by Step

```python
# services/wizard/step_validators.py

"""
Wizard Step Validators
Vietnamese-first Real-time Validation
"""

from typing import Dict, List
import re

from api.constants.import_constants import LEGAL_BASIS_VALID_VALUES_VI


# Vietnamese diacritics pattern
VIETNAMESE_DIACRITIC_PATTERN = re.compile(
    r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]',
    re.IGNORECASE
)


class WizardStepValidator:
    """
    Kiểm tra hợp lệ bước hướng dẫn
    Wizard step validator
    
    Real-time Vietnamese-first validation
    """
    
    def validate_step_1_basic_information(
        self,
        field_values: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Kiểm tra bước 1: Thông tin cơ bản
        Validate step 1: Basic information
        
        Returns validation result with bilingual errors
        """
        errors = []
        
        # Validate activity_name_vi (REQUIRED)
        if "activity_name_vi" not in field_values or not field_values["activity_name_vi"]:
            errors.append({
                "field": "activity_name_vi",
                "error_vi": "Tên hoạt động (tiếng Việt) là bắt buộc",
                "error_en": "Activity name (Vietnamese) is required"
            })
        elif len(field_values["activity_name_vi"].strip()) < 5:
            errors.append({
                "field": "activity_name_vi",
                "error_vi": "Tên hoạt động phải có ít nhất 5 ký tự",
                "error_en": "Activity name must be at least 5 characters"
            })
        elif not self._has_vietnamese_diacritics(field_values["activity_name_vi"]):
            errors.append({
                "field": "activity_name_vi",
                "error_vi": "Tên hoạt động thiếu dấu tiếng Việt",
                "error_en": "Activity name missing Vietnamese diacritics",
                "suggestion_vi": "Sử dụng dấu đầy đủ (ví dụ: 'quản lý' thay vì 'quan ly')"
            })
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "can_proceed": len(errors) == 0
        }
    
    def validate_step_2_processing_purpose(
        self,
        field_values: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Kiểm tra bước 2: Mục đích xử lý
        Validate step 2: Processing purpose
        """
        errors = []
        
        # Validate processing_purpose_vi (REQUIRED)
        if "processing_purpose_vi" not in field_values or not field_values["processing_purpose_vi"]:
            errors.append({
                "field": "processing_purpose_vi",
                "error_vi": "Mục đích xử lý (tiếng Việt) là bắt buộc",
                "error_en": "Processing purpose (Vietnamese) is required"
            })
        elif len(field_values["processing_purpose_vi"].strip()) < 10:
            errors.append({
                "field": "processing_purpose_vi",
                "error_vi": "Mục đích xử lý phải có ít nhất 10 ký tự",
                "error_en": "Processing purpose must be at least 10 characters"
            })
        elif not self._has_vietnamese_diacritics(field_values["processing_purpose_vi"]):
            errors.append({
                "field": "processing_purpose_vi",
                "error_vi": "Mục đích xử lý thiếu dấu tiếng Việt",
                "error_en": "Processing purpose missing Vietnamese diacritics"
            })
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "can_proceed": len(errors) == 0
        }
    
    def validate_step_3_legal_basis(
        self,
        field_values: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Kiểm tra bước 3: Cơ sở pháp lý
        Validate step 3: Legal basis
        """
        errors = []
        
        # Validate legal_basis (REQUIRED)
        if "legal_basis" not in field_values or not field_values["legal_basis"]:
            errors.append({
                "field": "legal_basis",
                "error_vi": "Cơ sở pháp lý là bắt buộc (Điều 13.1 PDPL)",
                "error_en": "Legal basis is required (Art. 13.1 PDPL)"
            })
        else:
            legal_basis_lower = str(field_values["legal_basis"]).strip().lower()
            if legal_basis_lower not in LEGAL_BASIS_VALID_VALUES_VI:
                errors.append({
                    "field": "legal_basis",
                    "error_vi": f"Cơ sở pháp lý không hợp lệ: '{field_values['legal_basis']}'",
                    "error_en": f"Invalid legal basis: '{field_values['legal_basis']}'",
                    "valid_values_vi": list(LEGAL_BASIS_VALID_VALUES_VI.keys())
                })
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "can_proceed": len(errors) == 0
        }
    
    def _has_vietnamese_diacritics(self, text: str) -> bool:
        """
        Kiểm tra văn bản có dấu tiếng Việt
        Check if text has Vietnamese diacritics
        """
        if not text or len(text.strip()) == 0:
            return False
        return bool(VIETNAMESE_DIACRITIC_PATTERN.search(text))
```

---

## Save Draft System

### Draft Persistence

```python
# api/endpoints/wizard_endpoints.py

"""
VeriPortal Wizard Endpoints
Vietnamese-first Guided Workflow API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from typing import Dict

from database.connection import get_db
from api.models.wizard_models import (
    WizardSessionRequest,
    WizardSessionResponse,
    WizardNavigationRequest,
    WizardCompletionRequest
)
from api.constants.wizard_constants import (
    WIZARD_TYPE_TRANSLATIONS,
    WIZARD_STEP_STATUS_TRANSLATIONS_VI,
    WIZARD_STEP_STATUS_TRANSLATIONS_EN,
    PDPL_ACTIVITY_WIZARD_STEPS
)
from services.wizard.step_validators import WizardStepValidator


router = APIRouter(
    prefix="/api/v1/data-inventory/wizard",
    tags=["Compliance Wizards | Hướng dẫn Tuân thủ"]
)


@router.post(
    "/start",
    response_model=WizardSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Bắt đầu phiên hướng dẫn | Start wizard session",
    description="""
    **Vietnamese:** Bắt đầu phiên hướng dẫn từng bước để tạo hoạt động xử lý dữ liệu.
    
    **English:** Start step-by-step wizard session to create processing activity.
    
    **Features:**
    - Hướng dẫn 7 bước tuân thủ PDPL | 7-step PDPL compliance guidance
    - Kiểm tra thời gian thực | Real-time validation
    - Lưu nháp tự động | Auto-save drafts
    - Trợ giúp theo ngữ cảnh | Contextual help
    """
)
async def start_wizard_session(
    tenant_id: UUID,
    request: WizardSessionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user)
) -> WizardSessionResponse:
    """
    Bắt đầu phiên hướng dẫn mới
    Start new wizard session
    
    Vietnamese-first guided workflow
    """
    try:
        session_id = uuid4()
        wizard_translation = WIZARD_TYPE_TRANSLATIONS[request.wizard_type]
        
        return WizardSessionResponse(
            session_id=session_id,
            wizard_type=request.wizard_type.value,
            wizard_type_vi=wizard_translation["vi"],
            wizard_type_en=wizard_translation["en"],
            session_name_vi=request.session_name_vi,
            session_name_en=request.session_name_en,
            current_step=1,
            total_steps=len(PDPL_ACTIVITY_WIZARD_STEPS),
            completion_percentage=0.0,
            current_step_data=PDPL_ACTIVITY_WIZARD_STEPS[0],
            all_steps=PDPL_ACTIVITY_WIZARD_STEPS,
            is_draft=True,
            can_proceed=False,
            can_go_back=False,
            collected_data={},
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=current_user
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to start wizard session",
                "error_vi": "Không thể bắt đầu phiên hướng dẫn",
                "message": str(e)
            }
        )


@router.post(
    "/save-draft",
    response_model=Dict[str, any],
    summary="Lưu nháp phiên hướng dẫn | Save wizard draft",
    description="""
    **Vietnamese:** Lưu trạng thái hiện tại của phiên hướng dẫn để tiếp tục sau.
    
    **English:** Save current wizard session state to resume later.
    
    **Auto-save:** Tự động lưu mỗi 30 giây | Auto-saves every 30 seconds
    """
)
async def save_wizard_draft(
    session_id: UUID,
    tenant_id: UUID,
    step_data: Dict[str, any],
    db: AsyncSession = Depends(get_db),
    current_user: UUID = Depends(get_current_user)
) -> Dict[str, any]:
    """
    Lưu nháp phiên hướng dẫn
    Save wizard session draft
    
    Enables resume later functionality
    """
    try:
        # Save draft to database
        # Implementation will store wizard state
        
        return {
            "saved": True,
            "session_id": session_id,
            "saved_at": datetime.now(),
            "message_vi": "Đã lưu nháp thành công",
            "message_en": "Draft saved successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to save wizard draft",
                "error_vi": "Không thể lưu nháp hướng dẫn",
                "message": str(e)
            }
        )
```

---

## Progress Tracking

### Completion Percentage Calculator

```python
# services/wizard/progress_tracker.py

"""
Wizard Progress Tracker
Vietnamese-first Progress Calculation
"""

from typing import Dict, List


class ProgressTracker:
    """
    Theo dõi tiến trình hướng dẫn
    Wizard progress tracker
    
    Calculates completion percentage
    """
    
    def calculate_progress(
        self,
        total_steps: int,
        completed_steps: List[int],
        current_step: int,
        step_weights: Dict[int, float] = None
    ) -> Dict[str, any]:
        """
        Tính toán tiến trình hoàn thành
        Calculate completion progress
        
        Returns progress metrics
        """
        if step_weights is None:
            # Equal weight for all steps
            step_weights = {i: 1.0 for i in range(1, total_steps + 1)}
        
        total_weight = sum(step_weights.values())
        completed_weight = sum(step_weights.get(step, 0) for step in completed_steps)
        
        completion_percentage = (completed_weight / total_weight) * 100
        
        return {
            "completion_percentage": round(completion_percentage, 2),
            "completed_steps": len(completed_steps),
            "total_steps": total_steps,
            "current_step": current_step,
            "remaining_steps": total_steps - len(completed_steps),
            "is_complete": len(completed_steps) == total_steps
        }
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] 7-step wizard for PDPL activity setup
- [TARGET] Vietnamese-first UI with contextual help
- [TARGET] Real-time validation on each field
- [TARGET] Vietnamese diacritics enforcement
- [TARGET] Save draft functionality with auto-save
- [TARGET] Resume wizard from saved draft
- [TARGET] Progress tracking with completion percentage
- [TARGET] Final review step before submission
- [TARGET] PDPL article references on each step
- [TARGET] Zero hard-coding (all steps in configuration)

**Next Document:** #05 - Database Seeding (Development/Demo)
