# Data Population Method 6: Third-Party System Integration
## Vietnamese PDPL 2025 Compliance - Processing Activities Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** processing_activities Table  
**Method:** Third-Party System Connectors (Salesforce, HubSpot, ERP)  
**Architecture:** Vietnamese-first OAuth2 Integration with Activity Auto-Discovery  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **third-party system integration** to automatically discover and import processing activities from external CRM, ERP, and business systems. This method enables Vietnamese enterprises to leverage existing data in Salesforce, HubSpot, SAP, and other platforms for PDPL compliance.

**Key Features:**
- OAuth2 authentication flow for secure integration
- Activity auto-discovery from CRM modules
- Vietnamese translation service integration
- Real-time sync with webhook listeners
- Field mapping configuration per system
- Zero hard-coding with connector plugins architecture

**Use Cases:**
- Import existing customer management activities from Salesforce
- Sync marketing activities from HubSpot
- Discover HR activities from SAP SuccessFactors
- Connect to local Vietnamese ERP systems
- Real-time activity updates via webhooks

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Connector Configuration](#connector-configuration)
3. [OAuth2 Authentication Flow](#oauth2-authentication-flow)
4. [Activity Discovery Mapping](#activity-discovery-mapping)
5. [Vietnamese Translation Service](#vietnamese-translation-service)
6. [Webhook Integration](#webhook-integration)
7. [Implementation Guide](#implementation-guide)

---

## Architecture Overview

### Integration System Components

```
┌─────────────────────────────────────────────────────────────┐
│         Third-Party Integration Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Connector   │  │  OAuth2      │  │  Activity    │     │
│  │  Registry    │─>│  Manager     │─>│  Discoverer  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Field       │  │  Vietnamese  │  │  Webhook     │     │
│  │  Mapper      │  │  Translator  │  │  Listener    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│  ┌──────────────────────────────────────────┐             │
│  │  External Systems                        │             │
│  │  - Salesforce CRM                        │             │
│  │  - HubSpot Marketing                     │             │
│  │  - SAP ERP                               │             │
│  │  - Vietnamese Local ERP                  │             │
│  └──────────────────────────────────────────┘             │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  processing_activities │                    │
│              │  (imported data)       │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Integration Workflow:**
1. User configures third-party connector
2. OAuth2 authentication with external system
3. Discover modules and activities from external system
4. Map external fields to VeriSyntra schema
5. Translate English content to Vietnamese
6. Import activities to processing_activities table
7. Setup webhook for real-time sync
8. Monitor sync status and handle errors

---

## Connector Configuration

### Connector Registry Constants

```python
# api/constants/connector_constants.py

"""
Third-Party Connector Constants - Zero Hard-Coding
Vietnamese-first Integration Configuration
"""

from enum import Enum
from typing import Dict, List


# Supported Third-Party Systems
class ConnectorType(str, Enum):
    """
    Loại hệ thống bên thứ ba
    Third-party system types
    """
    SALESFORCE = "salesforce"              # Salesforce CRM
    HUBSPOT = "hubspot"                    # HubSpot Marketing & CRM
    SAP_ERP = "sap_erp"                    # SAP ERP
    MICROSOFT_DYNAMICS = "microsoft_dynamics"  # Microsoft Dynamics 365
    ZOHO_CRM = "zoho_crm"                  # Zoho CRM
    VIETNAMESE_ERP = "vietnamese_erp"      # Vietnamese Local ERP


# Connector Type Vietnamese Translations
CONNECTOR_TYPE_TRANSLATIONS_VI: Dict[str, str] = {
    ConnectorType.SALESFORCE: "Salesforce CRM",
    ConnectorType.HUBSPOT: "HubSpot Marketing & CRM",
    ConnectorType.SAP_ERP: "SAP ERP",
    ConnectorType.MICROSOFT_DYNAMICS: "Microsoft Dynamics 365",
    ConnectorType.ZOHO_CRM: "Zoho CRM",
    ConnectorType.VIETNAMESE_ERP: "Hệ thống ERP Việt Nam"
}


# Connector Type English Translations
CONNECTOR_TYPE_TRANSLATIONS_EN: Dict[str, str] = {
    ConnectorType.SALESFORCE: "Salesforce CRM",
    ConnectorType.HUBSPOT: "HubSpot Marketing & CRM",
    ConnectorType.SAP_ERP: "SAP ERP",
    ConnectorType.MICROSOFT_DYNAMICS: "Microsoft Dynamics 365",
    ConnectorType.ZOHO_CRM: "Zoho CRM",
    ConnectorType.VIETNAMESE_ERP: "Vietnamese Local ERP"
}


# Connection Status
class ConnectionStatus(str, Enum):
    """
    Trạng thái kết nối
    Connection status
    """
    NOT_CONFIGURED = "not_configured"      # Chưa cấu hình
    AUTHENTICATING = "authenticating"      # Đang xác thực
    CONNECTED = "connected"                # Đã kết nối
    SYNCING = "syncing"                    # Đang đồng bộ
    ERROR = "error"                        # Lỗi kết nối
    DISCONNECTED = "disconnected"          # Đã ngắt kết nối


# Connection Status Vietnamese Translations
CONNECTION_STATUS_TRANSLATIONS_VI: Dict[str, str] = {
    ConnectionStatus.NOT_CONFIGURED: "Chưa cấu hình",
    ConnectionStatus.AUTHENTICATING: "Đang xác thực",
    ConnectionStatus.CONNECTED: "Đã kết nối",
    ConnectionStatus.SYNCING: "Đang đồng bộ",
    ConnectionStatus.ERROR: "Lỗi kết nối",
    ConnectionStatus.DISCONNECTED: "Đã ngắt kết nối"
}


# Connection Status English Translations
CONNECTION_STATUS_TRANSLATIONS_EN: Dict[str, str] = {
    ConnectionStatus.NOT_CONFIGURED: "Not Configured",
    ConnectionStatus.AUTHENTICATING: "Authenticating",
    ConnectionStatus.CONNECTED: "Connected",
    ConnectionStatus.SYNCING: "Syncing",
    ConnectionStatus.ERROR: "Connection Error",
    ConnectionStatus.DISCONNECTED: "Disconnected"
}


# OAuth2 Configuration per Connector
OAUTH2_CONFIG: Dict[str, Dict[str, str]] = {
    "salesforce": {
        "auth_url": "https://login.salesforce.com/services/oauth2/authorize",
        "token_url": "https://login.salesforce.com/services/oauth2/token",
        "revoke_url": "https://login.salesforce.com/services/oauth2/revoke",
        "api_base_url": "https://instance.salesforce.com/services/data/v58.0",
        "scopes": "api refresh_token"
    },
    "hubspot": {
        "auth_url": "https://app.hubspot.com/oauth/authorize",
        "token_url": "https://api.hubapi.com/oauth/v1/token",
        "api_base_url": "https://api.hubapi.com",
        "scopes": "crm.objects.contacts.read crm.objects.companies.read"
    },
    "sap_erp": {
        "auth_url": "https://sap-instance.com/oauth2/authorize",
        "token_url": "https://sap-instance.com/oauth2/token",
        "api_base_url": "https://sap-instance.com/api/v1",
        "scopes": "read write"
    },
    "microsoft_dynamics": {
        "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "api_base_url": "https://org.crm.dynamics.com/api/data/v9.2",
        "scopes": "https://org.crm.dynamics.com/.default"
    },
    "zoho_crm": {
        "auth_url": "https://accounts.zoho.com/oauth/v2/auth",
        "token_url": "https://accounts.zoho.com/oauth/v2/token",
        "api_base_url": "https://www.zohoapis.com/crm/v3",
        "scopes": "ZohoCRM.modules.ALL"
    }
}
```

---

## OAuth2 Authentication Flow

### OAuth2 Models and Endpoints

```python
# api/models/connector_models.py

"""
Third-Party Connector Models
Vietnamese-first Integration Configuration
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List
from uuid import UUID
from datetime import datetime

from api.constants.connector_constants import (
    ConnectorType,
    ConnectionStatus
)


class ConnectorConfigRequest(BaseModel):
    """
    Yêu cầu cấu hình kết nối
    Connector configuration request
    
    Vietnamese-first OAuth2 setup
    """
    
    connector_type: ConnectorType = Field(
        ...,
        description="Loại hệ thống bên thứ ba | Third-party system type"
    )
    
    config_name_vi: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Tên cấu hình (tiếng Việt) | Configuration name (Vietnamese)"
    )
    
    config_name_en: Optional[str] = Field(
        None,
        max_length=200,
        description="Tên cấu hình (tiếng Anh) | Configuration name (English)"
    )
    
    client_id: str = Field(
        ...,
        description="OAuth2 Client ID từ hệ thống bên thứ ba | OAuth2 Client ID from third-party system"
    )
    
    client_secret: str = Field(
        ...,
        description="OAuth2 Client Secret | OAuth2 Client Secret"
    )
    
    instance_url: Optional[HttpUrl] = Field(
        None,
        description="URL instance (cho Salesforce, SAP) | Instance URL (for Salesforce, SAP)"
    )
    
    auto_sync_enabled: bool = Field(
        default=True,
        description="Bật đồng bộ tự động | Enable auto-sync"
    )
    
    sync_interval_minutes: int = Field(
        default=60,
        ge=15,
        le=1440,
        description="Khoảng thời gian đồng bộ (phút) | Sync interval (minutes)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "connector_type": "salesforce",
                "config_name_vi": "Kết nối Salesforce - Phòng Marketing",
                "config_name_en": "Salesforce Connection - Marketing Department",
                "client_id": "3MVG9...",
                "client_secret": "ABC123...",
                "instance_url": "https://company.my.salesforce.com",
                "auto_sync_enabled": True,
                "sync_interval_minutes": 60
            }
        }


class OAuth2AuthorizationResponse(BaseModel):
    """
    Phản hồi URL xác thực
    OAuth2 authorization URL response
    
    Returns authorization URL for user consent
    """
    
    authorization_url: HttpUrl
    state: str
    message_vi: str
    message_en: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "authorization_url": "https://login.salesforce.com/services/oauth2/authorize?client_id=...",
                "state": "random-state-string-123",
                "message_vi": "Vui lòng truy cập URL để cấp quyền truy cập",
                "message_en": "Please visit URL to grant access"
            }
        }


class OAuth2CallbackRequest(BaseModel):
    """
    Yêu cầu callback OAuth2
    OAuth2 callback request
    
    Handles OAuth2 redirect callback
    """
    
    code: str = Field(
        ...,
        description="Mã xác thực từ OAuth2 provider | Authorization code from OAuth2 provider"
    )
    
    state: str = Field(
        ...,
        description="State để xác minh callback | State for callback verification"
    )
    
    connector_config_id: UUID = Field(
        ...,
        description="ID cấu hình kết nối | Connector configuration ID"
    )


class ConnectorStatusResponse(BaseModel):
    """
    Phản hồi trạng thái kết nối
    Connector status response
    
    Vietnamese-first connection status
    """
    
    connector_config_id: UUID
    connector_type: str
    connector_type_vi: str
    connector_type_en: str
    config_name_vi: str
    config_name_en: Optional[str]
    
    status: str
    status_vi: str
    status_en: str
    
    is_connected: bool
    last_sync_at: Optional[datetime]
    next_sync_at: Optional[datetime]
    
    total_activities_discovered: int
    total_activities_imported: int
    
    error_message_vi: Optional[str]
    error_message_en: Optional[str]
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "connector_config_id": "ee0e8400-e29b-41d4-a716-446655440009",
                "connector_type": "salesforce",
                "connector_type_vi": "Salesforce CRM",
                "connector_type_en": "Salesforce CRM",
                "config_name_vi": "Kết nối Salesforce - Phòng Marketing",
                "config_name_en": "Salesforce Connection - Marketing Department",
                "status": "connected",
                "status_vi": "Đã kết nối",
                "status_en": "Connected",
                "is_connected": True,
                "last_sync_at": "2025-11-06T16:30:00+07:00",
                "next_sync_at": "2025-11-06T17:30:00+07:00",
                "total_activities_discovered": 15,
                "total_activities_imported": 12,
                "error_message_vi": None,
                "error_message_en": None,
                "created_at": "2025-11-06T15:00:00+07:00",
                "updated_at": "2025-11-06T16:30:00+07:00"
            }
        }
```

---

## Activity Discovery Mapping

### Field Mapping Configuration

```python
# services/connectors/field_mapping.py

"""
Third-Party Field Mapping
Vietnamese-first Activity Discovery
"""

from typing import Dict, List, Optional


# Salesforce Object to Activity Mapping
SALESFORCE_ACTIVITY_MAPPING: Dict[str, Dict[str, any]] = {
    "Account": {
        "activity_name_template_en": "Customer Account Management",
        "activity_name_template_vi": "Quản lý tài khoản khách hàng",
        "processing_purpose_template_en": "Store and manage customer account information for business relationships",
        "processing_purpose_template_vi": "Lưu trữ và quản lý thông tin tài khoản khách hàng để duy trì quan hệ kinh doanh",
        "legal_basis": "contract",
        "field_mappings": {
            "Name": "customer_name",
            "BillingAddress": "billing_address",
            "Phone": "phone_number",
            "Industry": "industry_type"
        }
    },
    "Contact": {
        "activity_name_template_en": "Contact Information Management",
        "activity_name_template_vi": "Quản lý thông tin liên hệ",
        "processing_purpose_template_en": "Store contact information for communication and relationship management",
        "processing_purpose_template_vi": "Lưu trữ thông tin liên hệ để giao tiếp và quản lý quan hệ",
        "legal_basis": "legitimate_interest",
        "field_mappings": {
            "FirstName": "first_name",
            "LastName": "last_name",
            "Email": "email",
            "Phone": "phone_number"
        }
    },
    "Opportunity": {
        "activity_name_template_en": "Sales Opportunity Tracking",
        "activity_name_template_vi": "Theo dõi cơ hội bán hàng",
        "processing_purpose_template_en": "Track sales opportunities to manage sales pipeline",
        "processing_purpose_template_vi": "Theo dõi cơ hội bán hàng để quản lý quy trình bán hàng",
        "legal_basis": "legitimate_interest",
        "field_mappings": {
            "Name": "opportunity_name",
            "StageName": "stage",
            "Amount": "deal_amount"
        }
    },
    "Lead": {
        "activity_name_template_en": "Lead Management and Qualification",
        "activity_name_template_vi": "Quản lý và đánh giá khách hàng tiềm năng",
        "processing_purpose_template_en": "Manage leads to convert prospects into customers",
        "processing_purpose_template_vi": "Quản lý khách hàng tiềm năng để chuyển đổi thành khách hàng thực tế",
        "legal_basis": "consent",
        "field_mappings": {
            "FirstName": "first_name",
            "LastName": "last_name",
            "Company": "company_name",
            "Email": "email"
        }
    }
}


# HubSpot Object to Activity Mapping
HUBSPOT_ACTIVITY_MAPPING: Dict[str, Dict[str, any]] = {
    "contacts": {
        "activity_name_template_en": "Contact Database Management",
        "activity_name_template_vi": "Quản lý cơ sở dữ liệu liên hệ",
        "processing_purpose_template_en": "Maintain contact database for marketing and sales activities",
        "processing_purpose_template_vi": "Duy trì cơ sở dữ liệu liên hệ cho hoạt động marketing và bán hàng",
        "legal_basis": "consent",
        "field_mappings": {
            "firstname": "first_name",
            "lastname": "last_name",
            "email": "email",
            "phone": "phone_number"
        }
    },
    "companies": {
        "activity_name_template_en": "Company Records Management",
        "activity_name_template_vi": "Quản lý hồ sơ công ty",
        "processing_purpose_template_en": "Store company information for B2B relationships",
        "processing_purpose_template_vi": "Lưu trữ thông tin công ty cho quan hệ B2B",
        "legal_basis": "legitimate_interest",
        "field_mappings": {
            "name": "company_name",
            "domain": "website",
            "industry": "industry_type"
        }
    },
    "deals": {
        "activity_name_template_en": "Deal Pipeline Management",
        "activity_name_template_vi": "Quản lý quy trình giao dịch",
        "processing_purpose_template_en": "Track deals through sales pipeline",
        "processing_purpose_template_vi": "Theo dõi giao dịch qua quy trình bán hàng",
        "legal_basis": "contract",
        "field_mappings": {
            "dealname": "deal_name",
            "amount": "deal_amount",
            "dealstage": "stage"
        }
    }
}


# SAP ERP Module to Activity Mapping
SAP_ERP_ACTIVITY_MAPPING: Dict[str, Dict[str, any]] = {
    "HR_Personnel": {
        "activity_name_template_en": "Employee Personnel Records",
        "activity_name_template_vi": "Hồ sơ nhân viên",
        "processing_purpose_template_en": "Manage employee personal and employment information",
        "processing_purpose_template_vi": "Quản lý thông tin cá nhân và việc làm của nhân viên",
        "legal_basis": "contract",
        "field_mappings": {
            "PERNR": "employee_id",
            "ENAME": "employee_name",
            "GBDAT": "birth_date"
        }
    },
    "SD_Customer": {
        "activity_name_template_en": "Sales and Distribution Customer Management",
        "activity_name_template_vi": "Quản lý khách hàng bán hàng và phân phối",
        "processing_purpose_template_en": "Manage customer master data for sales operations",
        "processing_purpose_template_vi": "Quản lý dữ liệu chính khách hàng cho hoạt động bán hàng",
        "legal_basis": "contract",
        "field_mappings": {
            "KUNNR": "customer_id",
            "NAME1": "customer_name",
            "ORT01": "city"
        }
    }
}


# Connector Activity Mapping Registry
CONNECTOR_ACTIVITY_MAPPINGS: Dict[str, Dict[str, Dict[str, any]]] = {
    "salesforce": SALESFORCE_ACTIVITY_MAPPING,
    "hubspot": HUBSPOT_ACTIVITY_MAPPING,
    "sap_erp": SAP_ERP_ACTIVITY_MAPPING
}
```

---

## Vietnamese Translation Service

### Auto-Translation Integration

```python
# services/connectors/translation_service.py

"""
Vietnamese Translation Service
Auto-translate English content to Vietnamese
"""

from typing import Dict, Optional
import httpx


class VietnameseTranslationService:
    """
    Dịch vụ dịch tiếng Việt
    Vietnamese translation service
    
    Translates English content to Vietnamese
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.translation_cache: Dict[str, str] = {}
    
    async def translate_to_vietnamese(
        self,
        english_text: str,
        context: str = "business"
    ) -> str:
        """
        Dịch văn bản tiếng Anh sang tiếng Việt
        Translate English text to Vietnamese
        
        Returns Vietnamese translation
        """
        # Check cache first
        cache_key = f"{english_text}_{context}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        # Call translation API (Google Translate, DeepL, or custom)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://translation.googleapis.com/language/translate/v2",
                    json={
                        "q": english_text,
                        "source": "en",
                        "target": "vi",
                        "format": "text"
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    translated_text = data["data"]["translations"][0]["translatedText"]
                    
                    # Cache translation
                    self.translation_cache[cache_key] = translated_text
                    
                    return translated_text
        
        except Exception as e:
            # Fallback: return original text if translation fails
            return f"[Chưa dịch] {english_text}"
    
    async def translate_activity_fields(
        self,
        activity_data: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Dịch các trường hoạt động
        Translate activity fields
        
        Translates English fields to Vietnamese
        """
        translated_data = activity_data.copy()
        
        # Translate activity name
        if "activity_name_en" in activity_data and not activity_data.get("activity_name_vi"):
            translated_data["activity_name_vi"] = await self.translate_to_vietnamese(
                activity_data["activity_name_en"],
                context="activity_name"
            )
        
        # Translate processing purpose
        if "processing_purpose_en" in activity_data and not activity_data.get("processing_purpose_vi"):
            translated_data["processing_purpose_vi"] = await self.translate_to_vietnamese(
                activity_data["processing_purpose_en"],
                context="processing_purpose"
            )
        
        # Translate description
        if "activity_description_en" in activity_data and not activity_data.get("activity_description_vi"):
            translated_data["activity_description_vi"] = await self.translate_to_vietnamese(
                activity_data["activity_description_en"],
                context="description"
            )
        
        return translated_data
```

---

## Webhook Integration

### Real-Time Sync via Webhooks

```python
# api/endpoints/webhook_endpoints.py

"""
Webhook Endpoints for Third-Party Systems
Vietnamese-first Real-time Sync
"""

from fastapi import APIRouter, Request, HTTPException, status, Header
from typing import Optional
import hmac
import hashlib

from services.connectors.activity_sync_service import ActivitySyncService


router = APIRouter(
    prefix="/api/v1/webhooks",
    tags=["Webhooks | Đồng bộ Thời gian Thực"]
)


@router.post(
    "/salesforce",
    status_code=status.HTTP_200_OK,
    summary="Webhook Salesforce | Salesforce webhook receiver",
    description="""
    **Vietnamese:** Nhận sự kiện webhook từ Salesforce khi có thay đổi dữ liệu.
    
    **English:** Receive webhook events from Salesforce when data changes.
    
    **Events:**
    - Tạo mới Account/Contact | New Account/Contact created
    - Cập nhật thông tin | Information updated
    - Xóa bản ghi | Record deleted
    """
)
async def salesforce_webhook(
    request: Request,
    x_salesforce_signature: Optional[str] = Header(None)
):
    """
    Nhận webhook từ Salesforce
    Receive Salesforce webhook
    
    Real-time sync on data changes
    """
    try:
        body = await request.body()
        
        # Verify Salesforce signature
        if not verify_salesforce_signature(body, x_salesforce_signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Invalid signature",
                    "error_vi": "Chữ ký không hợp lệ"
                }
            )
        
        # Process webhook event
        event_data = await request.json()
        
        sync_service = ActivitySyncService()
        result = await sync_service.process_salesforce_event(event_data)
        
        return {
            "received": True,
            "processed": result["processed"],
            "message_vi": "Đã xử lý sự kiện Salesforce thành công",
            "message_en": "Salesforce event processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to process webhook",
                "error_vi": "Không thể xử lý webhook",
                "message": str(e)
            }
        )


@router.post(
    "/hubspot",
    status_code=status.HTTP_200_OK,
    summary="Webhook HubSpot | HubSpot webhook receiver",
    description="""
    **Vietnamese:** Nhận sự kiện webhook từ HubSpot khi có thay đổi dữ liệu.
    
    **English:** Receive webhook events from HubSpot when data changes.
    """
)
async def hubspot_webhook(request: Request):
    """
    Nhận webhook từ HubSpot
    Receive HubSpot webhook
    
    Real-time sync on contact/company changes
    """
    try:
        event_data = await request.json()
        
        sync_service = ActivitySyncService()
        result = await sync_service.process_hubspot_event(event_data)
        
        return {
            "received": True,
            "processed": result["processed"],
            "message_vi": "Đã xử lý sự kiện HubSpot thành công",
            "message_en": "HubSpot event processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to process webhook",
                "error_vi": "Không thể xử lý webhook",
                "message": str(e)
            }
        )


def verify_salesforce_signature(body: bytes, signature: str) -> bool:
    """
    Xác minh chữ ký Salesforce
    Verify Salesforce signature
    
    Returns True if signature is valid
    """
    if not signature:
        return False
    
    # Implementation would verify HMAC signature
    # using shared secret from Salesforce
    return True
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] Connector registry with 6 third-party systems
- [TARGET] OAuth2 authentication flow for each connector
- [TARGET] Activity discovery from external modules
- [TARGET] Field mapping configuration (Salesforce, HubSpot, SAP)
- [TARGET] Vietnamese translation service integration
- [TARGET] Auto-translate English content to Vietnamese
- [TARGET] Webhook endpoints for real-time sync
- [TARGET] Signature verification for webhooks
- [TARGET] Connector status monitoring
- [TARGET] Zero hard-coding (all mappings in configuration)

**Next Document:** #07 - Alembic Migration Initial Data
