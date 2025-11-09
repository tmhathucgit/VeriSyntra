# Data Population Method 6: Third-Party Integration
## Vietnamese PDPL 2025 Compliance - Data Categories Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** data_categories Table  
**Method:** External System Integration with Data Catalog Sync  
**Architecture:** REST API + OAuth2 + Vietnamese Translation Service  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **third-party data catalog integration** to import and sync data categories from external compliance tools, data governance platforms, and Vietnamese ERP systems.

**Key Features:**
- Integration with data catalog systems (Collibra, Alation, Apache Atlas)
- Vietnamese ERP system connectors (Misa, Fast, Bravo)
- OAuth2 authentication and token management
- Automatic Vietnamese translation service
- Category mapping and normalization
- Real-time sync with webhook support
- Zero hard-coding with connector configuration

**Use Cases:**
- Import categories from existing data catalogs
- Sync with global compliance tools
- Integrate Vietnamese ERP data classifications
- Automatic category updates from external systems
- Cross-platform PDPL compliance alignment

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Connector Configuration](#connector-configuration)
3. [OAuth2 Authentication](#oauth2-authentication)
4. [Category Mapping](#category-mapping)
5. [Vietnamese Translation Service](#vietnamese-translation-service)
6. [Webhook Integration](#webhook-integration)
7. [Success Criteria](#success-criteria)

---

## Architecture Overview

### Third-Party Integration System

```
┌─────────────────────────────────────────────────────────────┐
│         Third-Party Integration Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  OAuth2      │  │  Connector   │  │  Category    │     │
│  │  Manager     │─>│  Registry    │─>│  Mapper      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Vietnamese  │  │  Webhook     │  │  Sync        │     │
│  │  Translator  │  │  Handler     │  │  Manager     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  data_categories       │                    │
│              │  (Synced from External)│                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Integration Workflow:**
1. Configure connector with OAuth2 credentials
2. Authenticate and obtain access token
3. Fetch categories from external system
4. Map external schema to VeriSyntra schema
5. Translate to Vietnamese if needed
6. Validate PDPL compliance
7. Import or update categories
8. Set up webhook for real-time sync

---

## Connector Configuration

### Supported Third-Party Systems

```python
# services/integration/connector_config.py

"""
Third-Party Connector Configuration
Vietnamese and International Systems
"""

from enum import Enum
from typing import Dict, Optional


class ConnectorType(str, Enum):
    """
    Loại connector
    Connector type
    """
    # Data Catalog Systems
    COLLIBRA = "collibra"
    ALATION = "alation"
    APACHE_ATLAS = "apache_atlas"
    
    # Vietnamese ERP Systems
    MISA_ERP = "misa_erp"
    FAST_ERP = "fast_erp"
    BRAVO_ERP = "bravo_erp"
    
    # Compliance Tools
    ONETRUST = "onetrust"
    TRUSTARC = "trustarc"
    
    # Custom API
    CUSTOM_API = "custom_api"


class ConnectionStatus(str, Enum):
    """
    Trạng thái kết nối
    Connection status
    """
    NOT_CONFIGURED = "not_configured"
    CONFIGURED = "configured"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    SYNCING = "syncing"
    ERROR = "error"


# Connector endpoints configuration
CONNECTOR_ENDPOINTS: Dict[str, Dict[str, str]] = {
    "collibra": {
        "auth_url": "https://api.collibra.com/oauth2/authorize",
        "token_url": "https://api.collibra.com/oauth2/token",
        "api_base_url": "https://api.collibra.com/rest/2.0",
        "categories_endpoint": "/assets/types",
        "scopes": "READ"
    },
    "alation": {
        "auth_url": "https://alation-instance.alationcloud.com/integration/v1/authorize",
        "token_url": "https://alation-instance.alationcloud.com/integration/v1/token",
        "api_base_url": "https://alation-instance.alationcloud.com/integration/v1",
        "categories_endpoint": "/catalog/custom_field",
        "scopes": "catalog:read"
    },
    "apache_atlas": {
        "auth_url": None,  # Uses Basic Auth
        "token_url": None,
        "api_base_url": "http://atlas-server:21000/api/atlas/v2",
        "categories_endpoint": "/types/typedefs/headers",
        "scopes": None
    },
    "misa_erp": {
        "auth_url": "https://api.misa.vn/oauth/authorize",
        "token_url": "https://api.misa.vn/oauth/token",
        "api_base_url": "https://api.misa.vn/v1",
        "categories_endpoint": "/data-classification",
        "scopes": "read_data"
    },
    "fast_erp": {
        "auth_url": "https://api.fast.com.vn/oauth/authorize",
        "token_url": "https://api.fast.com.vn/oauth/token",
        "api_base_url": "https://api.fast.com.vn/v1",
        "categories_endpoint": "/master-data/categories",
        "scopes": "read"
    },
    "onetrust": {
        "auth_url": "https://app.onetrust.com/oauth/authorize",
        "token_url": "https://app.onetrust.com/oauth/token",
        "api_base_url": "https://app.onetrust.com/api",
        "categories_endpoint": "/data-elements",
        "scopes": "data_inventory:read"
    }
}


# Field mapping templates
CONNECTOR_FIELD_MAPPINGS: Dict[str, Dict[str, str]] = {
    "collibra": {
        "name": "category_name_en",
        "displayName": "category_name_en",
        "description": "category_description_en",
        "type": "category_type"
    },
    "alation": {
        "field_name": "category_name_en",
        "description": "category_description_en",
        "field_type": "category_type"
    },
    "misa_erp": {
        "ten_danh_muc": "category_name_vi",
        "mo_ta": "category_description_vi",
        "loai": "category_type"
    },
    "onetrust": {
        "name": "category_name_en",
        "description": "category_description_en",
        "dataElementType": "category_type",
        "sensitive": "is_sensitive"
    }
}
```

---

## OAuth2 Authentication

### Token Management Service

```python
# services/integration/oauth2_manager.py

"""
OAuth2 Authentication Manager
Token Management for Third-Party Systems
"""

from typing import Dict, Optional
import httpx
import time
from datetime import datetime, timedelta


class OAuth2Manager:
    """
    Quản lý OAuth2
    OAuth2 authentication manager
    
    Handles token acquisition and refresh
    """
    
    def __init__(self, connector_type: ConnectorType):
        self.connector_type = connector_type
        self.config = CONNECTOR_ENDPOINTS.get(connector_type)
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
    
    async def authenticate(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Xác thực OAuth2
        OAuth2 authentication
        
        Returns access token and refresh token
        """
        if not self.config["auth_url"]:
            # Use Basic Auth for systems like Apache Atlas
            return await self._basic_auth(client_id, client_secret)
        
        # OAuth2 Authorization Code Flow
        auth_code = await self._get_authorization_code(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scopes=self.config["scopes"]
        )
        
        # Exchange code for tokens
        tokens = await self._exchange_code_for_tokens(
            auth_code=auth_code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        )
        
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens.get("refresh_token")
        
        # Calculate expiration
        expires_in = tokens.get("expires_in", 3600)
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        return tokens
    
    async def get_valid_token(self) -> str:
        """
        Lấy token hợp lệ
        Get valid access token
        
        Refreshes if expired
        """
        if not self.access_token:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        # Check if token is expired or about to expire (5 min buffer)
        if self.token_expires_at and datetime.now() >= (self.token_expires_at - timedelta(minutes=5)):
            await self._refresh_access_token()
        
        return self.access_token
    
    async def _refresh_access_token(self) -> None:
        """Làm mới access token"""
        if not self.refresh_token:
            raise ValueError("No refresh token available. Re-authenticate required.")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.config["token_url"],
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token
                }
            )
            
            response.raise_for_status()
            tokens = response.json()
            
            self.access_token = tokens["access_token"]
            expires_in = tokens.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
    
    async def _basic_auth(self, username: str, password: str) -> Dict[str, str]:
        """Basic authentication for systems without OAuth2"""
        import base64
        
        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        
        self.access_token = f"Basic {encoded}"
        
        return {
            "access_token": self.access_token,
            "token_type": "Basic"
        }
```

---

## Category Mapping

### External Schema to VeriSyntra Mapping

```python
# services/integration/category_mapper.py

"""
Category Mapping Service
External Schema Normalization
"""

from typing import Dict, List, Optional


class CategoryMapper:
    """
    Bộ ánh xạ category
    Category mapper
    
    Maps external categories to VeriSyntra schema
    """
    
    def __init__(self, connector_type: ConnectorType):
        self.connector_type = connector_type
        self.field_mappings = CONNECTOR_FIELD_MAPPINGS.get(connector_type, {})
    
    def map_category(self, external_data: Dict[str, any]) -> Dict[str, any]:
        """
        Ánh xạ category từ hệ thống bên ngoài
        Map external category to VeriSyntra schema
        
        Returns normalized category data
        """
        mapped = {}
        
        # Map fields using configuration
        for external_field, verisyntra_field in self.field_mappings.items():
            if external_field in external_data:
                mapped[verisyntra_field] = external_data[external_field]
        
        # Normalize category type
        if "category_type" in mapped:
            mapped["category_type"] = self._normalize_type(mapped["category_type"])
        
        # Auto-detect sensitive flag
        if "is_sensitive" not in mapped:
            mapped["is_sensitive"] = self._detect_sensitive(mapped)
        
        # Set defaults
        mapped.setdefault("usage_count", 0)
        mapped.setdefault("is_active", True)
        
        return mapped
    
    def _normalize_type(self, type_value: str) -> str:
        """Chuẩn hóa loại category"""
        type_lower = str(type_value).lower()
        
        sensitive_keywords = ["sensitive", "nhạy cảm", "confidential", "restricted"]
        
        for keyword in sensitive_keywords:
            if keyword in type_lower:
                return "sensitive"
        
        return "basic"
    
    def _detect_sensitive(self, category_data: Dict[str, any]) -> bool:
        """Tự động phát hiện dữ liệu nhạy cảm"""
        # Check category type
        if category_data.get("category_type") == "sensitive":
            return True
        
        # Check category name for PDPL keywords
        sensitive_keywords = [
            "health", "sức khỏe", "biometric", "sinh trắc",
            "genetic", "di truyền", "political", "chính trị",
            "religious", "tôn giáo", "criminal", "tư pháp"
        ]
        
        name_vi = category_data.get("category_name_vi", "").lower()
        name_en = category_data.get("category_name_en", "").lower()
        
        for keyword in sensitive_keywords:
            if keyword in name_vi or keyword in name_en:
                return True
        
        return False
```

---

## Vietnamese Translation Service

### Automatic Translation for External Data

```python
# services/integration/translation_service.py

"""
Vietnamese Translation Service
Auto-translate English Categories
"""

from typing import Dict, Optional
import httpx


class VietnameseTranslationService:
    """
    Dịch vụ dịch tiếng Việt
    Vietnamese translation service
    
    Translates English categories to Vietnamese
    """
    
    # Translation cache
    _translation_cache: Dict[str, str] = {}
    
    # Common PDPL translations
    PDPL_TRANSLATIONS: Dict[str, str] = {
        "Personal Information": "Thông tin cá nhân",
        "Health Information": "Thông tin sức khỏe",
        "Biometric Data": "Dữ liệu sinh trắc học",
        "Genetic Information": "Thông tin di truyền",
        "Political Opinions": "Quan điểm chính trị",
        "Religious Beliefs": "Tín ngưỡng tôn giáo",
        "Sexual Orientation": "Xu hướng tình dục",
        "Criminal Records": "Hồ sơ tư pháp",
        "Trade Union": "Thông tin công đoàn",
        "Children's Data": "Dữ liệu trẻ em",
        "Contact Information": "Thông tin liên hệ",
        "Financial Information": "Thông tin tài chính",
        "Location Data": "Dữ liệu vị trí",
        "Full Name": "Họ và tên",
        "Date of Birth": "Ngày tháng năm sinh",
        "Identification": "Giấy tờ tùy thân"
    }
    
    async def translate_category(
        self,
        category_data: Dict[str, any]
    ) -> Dict[str, any]:
        """
        Dịch category sang tiếng Việt
        Translate category to Vietnamese
        
        Adds Vietnamese fields if missing
        """
        # Check if Vietnamese already exists
        if "category_name_vi" in category_data and category_data["category_name_vi"]:
            return category_data
        
        # Get English name
        name_en = category_data.get("category_name_en", "")
        
        if not name_en:
            return category_data
        
        # Try PDPL translations first
        if name_en in self.PDPL_TRANSLATIONS:
            category_data["category_name_vi"] = self.PDPL_TRANSLATIONS[name_en]
        else:
            # Use translation API
            translated = await self._translate_via_api(name_en)
            if translated:
                category_data["category_name_vi"] = translated
        
        # Translate description if needed
        desc_en = category_data.get("category_description_en", "")
        if desc_en and "category_description_vi" not in category_data:
            desc_vi = await self._translate_via_api(desc_en)
            if desc_vi:
                category_data["category_description_vi"] = desc_vi
        
        return category_data
    
    async def _translate_via_api(self, text: str) -> Optional[str]:
        """Dịch qua API (Google Translate, DeepL, etc.)"""
        # Check cache first
        if text in self._translation_cache:
            return self._translation_cache[text]
        
        # Placeholder: Integrate with translation API
        # Example: Google Cloud Translation API
        # For now, return None (would be implemented with actual API)
        
        return None
```

---

## Webhook Integration

### Real-time Sync Handler

```python
# services/integration/webhook_handler.py

"""
Webhook Integration Handler
Real-time Category Updates
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict


router = APIRouter()


class WebhookHandler:
    """
    Xử lý webhook
    Webhook handler
    
    Receives real-time updates from external systems
    """
    
    @staticmethod
    async def handle_collibra_webhook(payload: Dict[str, any]) -> Dict[str, str]:
        """Xử lý webhook từ Collibra"""
        event_type = payload.get("eventType")
        
        if event_type == "ASSET_CREATED":
            # New category created in Collibra
            await WebhookHandler._sync_new_category(payload)
        
        elif event_type == "ASSET_UPDATED":
            # Category updated in Collibra
            await WebhookHandler._sync_updated_category(payload)
        
        elif event_type == "ASSET_DELETED":
            # Category deleted in Collibra
            await WebhookHandler._sync_deleted_category(payload)
        
        return {"status": "processed"}
    
    @staticmethod
    async def handle_onetrust_webhook(payload: Dict[str, any]) -> Dict[str, str]:
        """Xử lý webhook từ OneTrust"""
        event_type = payload.get("eventType")
        
        if event_type == "DATA_ELEMENT_CREATED":
            await WebhookHandler._sync_new_category(payload)
        
        return {"status": "processed"}
    
    @staticmethod
    async def _sync_new_category(payload: Dict[str, any]) -> None:
        """Đồng bộ category mới"""
        # Map external data
        mapper = CategoryMapper(payload.get("source"))
        category_data = mapper.map_category(payload.get("data", {}))
        
        # Translate to Vietnamese
        translator = VietnameseTranslationService()
        category_data = await translator.translate_category(category_data)
        
        # Create in database
        # ... implementation


@router.post("/webhooks/collibra")
async def collibra_webhook(request: Request):
    """Collibra webhook endpoint"""
    payload = await request.json()
    
    handler = WebhookHandler()
    result = await handler.handle_collibra_webhook(payload)
    
    return result


@router.post("/webhooks/onetrust")
async def onetrust_webhook(request: Request):
    """OneTrust webhook endpoint"""
    payload = await request.json()
    
    handler = WebhookHandler()
    result = await handler.handle_onetrust_webhook(payload)
    
    return result
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] OAuth2 authentication for external systems
- [TARGET] Connector configuration (8+ systems)
- [TARGET] Vietnamese ERP integration (Misa, Fast, Bravo)
- [TARGET] International data catalog integration (Collibra, Alation, Apache Atlas)
- [TARGET] Category schema mapping and normalization
- [TARGET] Automatic Vietnamese translation service
- [TARGET] PDPL-aware sensitive data detection
- [TARGET] Webhook support for real-time sync
- [TARGET] Token refresh automation
- [TARGET] Translation caching
- [TARGET] Zero hard-coding (all mappings in configuration)
- [TARGET] Bilingual error handling

**Next Document:** #07 - Alembic Migration
