# ============================================
# VeriSyntra Auth Service - Tenant Models
# ============================================
# Vietnamese PDPL 2025 Compliance Platform
# Multi-tenant organization models
# ============================================

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class VeriRegionalLocation(str, Enum):
    """Vietnamese regional business locations"""
    NORTH = "north"  # Ha Noi, Hai Phong, Quang Ninh
    CENTRAL = "central"  # Da Nang, Hue, Quang Nam
    SOUTH = "south"  # TP.HCM, Dong Nai, Binh Duong


class VeriIndustryType(str, Enum):
    """Vietnamese business industry types"""
    TECHNOLOGY = "technology"  # Cong nghe thong tin
    MANUFACTURING = "manufacturing"  # San xuat
    FINANCE = "finance"  # Tai chinh ngan hang
    ECOMMERCE = "ecommerce"  # Thuong mai dien tu
    HEALTHCARE = "healthcare"  # Y te
    EDUCATION = "education"  # Giao duc
    RETAIL = "retail"  # Ban le
    LOGISTICS = "logistics"  # Van tai logistics
    REAL_ESTATE = "real_estate"  # Bat dong san
    TOURISM = "tourism"  # Du lich
    TELECOMMUNICATIONS = "telecommunications"  # Vien thong
    OTHER = "other"  # Khac


class VeriSubscriptionTier(str, Enum):
    """VeriSyntra subscription tiers"""
    STARTER = "starter"  # 1-10 users, basic compliance
    PROFESSIONAL = "professional"  # 11-50 users, advanced features
    ENTERPRISE = "enterprise"  # 51+ users, custom solutions


class VeriTenant(BaseModel):
    """
    Vietnamese business tenant/organization model
    Represents a company using VeriSyntra PDPL compliance platform
    """
    tenant_id: UUID = Field(default_factory=uuid4)
    company_name: str
    company_name_vi: Optional[str] = None  # Vietnamese company name
    tax_id: Optional[str] = None  # Ma so thue (Vietnamese tax ID)
    
    # Regional and industry context
    veri_regional_location: VeriRegionalLocation = VeriRegionalLocation.SOUTH
    veri_industry_type: VeriIndustryType = VeriIndustryType.TECHNOLOGY
    
    # Subscription and billing
    subscription_tier: VeriSubscriptionTier = VeriSubscriptionTier.STARTER
    subscription_start_date: Optional[datetime] = None
    subscription_end_date: Optional[datetime] = None
    max_users: int = 10
    
    # Vietnamese business context
    veri_business_context: Dict[str, Any] = Field(default_factory=dict)
    
    # Contact information
    primary_email: Optional[str] = None
    primary_phone: Optional[str] = None
    address: Optional[str] = None
    address_vi: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None  # Tinh/Thanh pho
    
    # Status
    is_active: bool = True
    is_verified: bool = False  # Business verification status
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # PDPL compliance settings
    data_residency_region: str = "vietnam"  # Data must stay in Vietnam
    pdpl_compliant: bool = False  # PDPL 2025 compliance status
    
    class Config:
        json_schema_extra = {
            "example": {
                "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
                "company_name": "VeriSyntra Vietnam Co., Ltd.",
                "company_name_vi": "Cong ty TNHH VeriSyntra Viet Nam",
                "tax_id": "0123456789",
                "veri_regional_location": "south",
                "veri_industry_type": "technology",
                "subscription_tier": "professional",
                "max_users": 50,
                "primary_email": "contact@verisyntra.vn",
                "primary_phone": "+84 28 1234 5678",
                "city": "Ho Chi Minh City",
                "province": "TP. Ho Chi Minh",
                "data_residency_region": "vietnam",
                "pdpl_compliant": True
            }
        }


class VeriTenantCreate(BaseModel):
    """Request model for tenant creation"""
    company_name: str = Field(..., min_length=2, max_length=200)
    company_name_vi: Optional[str] = Field(None, min_length=2, max_length=200)
    tax_id: Optional[str] = Field(None, pattern=r'^\d{10,13}$')  # Vietnamese tax ID format
    veri_regional_location: VeriRegionalLocation = VeriRegionalLocation.SOUTH
    veri_industry_type: VeriIndustryType = VeriIndustryType.TECHNOLOGY
    subscription_tier: VeriSubscriptionTier = VeriSubscriptionTier.STARTER
    primary_email: Optional[str] = None
    primary_phone: Optional[str] = Field(None, pattern=r'^\+84\s?\d{2,3}\s?\d{3,4}\s?\d{4}$')
    address: Optional[str] = None
    address_vi: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "VeriSyntra Vietnam Co., Ltd.",
                "company_name_vi": "Cong ty TNHH VeriSyntra Viet Nam",
                "tax_id": "0123456789",
                "veri_regional_location": "south",
                "veri_industry_type": "technology",
                "subscription_tier": "professional",
                "primary_email": "contact@verisyntra.vn",
                "primary_phone": "+84 28 1234 5678",
                "city": "Ho Chi Minh City",
                "province": "TP. Ho Chi Minh"
            }
        }


class VeriTenantUpdate(BaseModel):
    """Request model for tenant update"""
    company_name: Optional[str] = Field(None, min_length=2, max_length=200)
    company_name_vi: Optional[str] = Field(None, min_length=2, max_length=200)
    tax_id: Optional[str] = Field(None, pattern=r'^\d{10,13}$')
    veri_regional_location: Optional[VeriRegionalLocation] = None
    veri_industry_type: Optional[VeriIndustryType] = None
    primary_email: Optional[str] = None
    primary_phone: Optional[str] = Field(None, pattern=r'^\+84\s?\d{2,3}\s?\d{3,4}\s?\d{4}$')
    address: Optional[str] = None
    address_vi: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "VeriSyntra Vietnam Co., Ltd. - Updated",
                "company_name_vi": "Cong ty TNHH VeriSyntra Viet Nam - Cap nhat",
                "primary_phone": "+84 28 9876 5432"
            }
        }


class VeriTenantResponse(BaseModel):
    """Response model for tenant data"""
    tenant_id: UUID
    company_name: str
    company_name_vi: Optional[str]
    tax_id: Optional[str]
    veri_regional_location: VeriRegionalLocation
    veri_industry_type: VeriIndustryType
    subscription_tier: VeriSubscriptionTier
    max_users: int
    primary_email: Optional[str]
    primary_phone: Optional[str]
    city: Optional[str]
    province: Optional[str]
    is_active: bool
    is_verified: bool
    pdpl_compliant: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
                "company_name": "VeriSyntra Vietnam Co., Ltd.",
                "company_name_vi": "Cong ty TNHH VeriSyntra Viet Nam",
                "tax_id": "0123456789",
                "veri_regional_location": "south",
                "veri_industry_type": "technology",
                "subscription_tier": "professional",
                "max_users": 50,
                "primary_email": "contact@verisyntra.vn",
                "primary_phone": "+84 28 1234 5678",
                "city": "Ho Chi Minh City",
                "province": "TP. Ho Chi Minh",
                "is_active": True,
                "is_verified": True,
                "pdpl_compliant": True,
                "created_at": "2025-11-01T10:00:00Z"
            }
        }
