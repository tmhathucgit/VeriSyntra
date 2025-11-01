# ============================================
# VeriSyntra Auth Service - User Models
# ============================================
# Vietnamese PDPL 2025 Compliance Platform
# Multi-tenant user authentication models
# ============================================

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class VeriUserRole(str, Enum):
    """Vietnamese business user roles"""
    ADMIN = "admin"  # Company administrator
    DPO = "dpo"  # Data Protection Officer (Vietnamese: Chuyen vien bao ve du lieu)
    COMPLIANCE_MANAGER = "compliance_manager"  # PDPL compliance manager
    STAFF = "staff"  # Regular staff member
    AUDITOR = "auditor"  # External auditor
    VIEWER = "viewer"  # Read-only access


class VeriUser(BaseModel):
    """
    Vietnamese business user model
    Supports multi-tenant authentication with Vietnamese cultural context
    """
    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    hashed_password: str
    full_name: str
    full_name_vi: Optional[str] = None  # Vietnamese full name (Ho va Ten)
    phone_number: Optional[str] = None  # Vietnamese phone format: +84 xxx xxx xxxx
    tenant_id: UUID
    role: VeriUserRole = VeriUserRole.STAFF
    is_active: bool = True
    is_verified: bool = False  # Email verification status
    is_email_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Vietnamese business context
    preferred_language: str = "vi"  # vi or en
    timezone: str = "Asia/Ho_Chi_Minh"
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "nguyen.van.a@company.vn",
                "full_name": "Nguyen Van A",
                "full_name_vi": "Nguyen Van A",
                "phone_number": "+84 901 234 567",
                "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
                "role": "dpo",
                "is_active": True,
                "is_verified": True,
                "preferred_language": "vi",
                "timezone": "Asia/Ho_Chi_Minh"
            }
        }


class VeriUserCreate(BaseModel):
    """Request model for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    full_name_vi: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r'^\+84\s?\d{3}\s?\d{3}\s?\d{3,4}$')
    tenant_id: Optional[UUID] = None  # Will be created if not provided
    company_name: Optional[str] = None  # For new tenant creation
    veri_regional_location: Optional[str] = None  # north, central, south
    preferred_language: str = "vi"
    
    @validator('password')
    def validate_password(cls, v):
        """
        Vietnamese password requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        """
        if len(v) < 8:
            raise ValueError('Mat khau phai co it nhat 8 ky tu / Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Mat khau phai chua it nhat 1 chu cai viet hoa / Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Mat khau phai chua it nhat 1 chu cai viet thuong / Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Mat khau phai chua it nhat 1 chu so / Password must contain at least one number')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "nguyen.van.a@company.vn",
                "password": "SecurePass123",
                "full_name": "Nguyen Van A",
                "full_name_vi": "Nguyen Van A",
                "phone_number": "+84 901 234 567",
                "company_name": "Cong ty TNHH VeriSyntra Viet Nam",
                "veri_regional_location": "south",
                "preferred_language": "vi"
            }
        }


class VeriUserUpdate(BaseModel):
    """Request model for user profile update"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    full_name_vi: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r'^\+84\s?\d{3}\s?\d{3}\s?\d{3,4}$')
    preferred_language: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Nguyen Van B",
                "full_name_vi": "Nguyen Van B",
                "phone_number": "+84 902 345 678",
                "preferred_language": "vi"
            }
        }


class VeriUserResponse(BaseModel):
    """Response model for user data (no sensitive info)"""
    user_id: UUID
    email: EmailStr
    full_name: str
    full_name_vi: Optional[str]
    phone_number: Optional[str]
    tenant_id: UUID
    role: VeriUserRole
    is_active: bool
    is_verified: bool
    preferred_language: str
    timezone: str
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "nguyen.van.a@company.vn",
                "full_name": "Nguyen Van A",
                "full_name_vi": "Nguyen Van A",
                "phone_number": "+84 901 234 567",
                "tenant_id": "660e8400-e29b-41d4-a716-446655440001",
                "role": "dpo",
                "is_active": True,
                "is_verified": True,
                "preferred_language": "vi",
                "timezone": "Asia/Ho_Chi_Minh",
                "created_at": "2025-11-01T10:00:00Z",
                "last_login": "2025-11-01T14:30:00Z"
            }
        }


class VeriUserLogin(BaseModel):
    """Request model for user login"""
    email: EmailStr
    password: str
    tenant_id: Optional[UUID] = None  # Optional for single-tenant users
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "nguyen.van.a@company.vn",
                "password": "SecurePass123",
                "tenant_id": "660e8400-e29b-41d4-a716-446655440001"
            }
        }


class VeriPasswordChange(BaseModel):
    """Request model for password change"""
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Vietnamese password validation"""
        if len(v) < 8:
            raise ValueError('Mat khau moi phai co it nhat 8 ky tu / New password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Mat khau moi phai chua it nhat 1 chu cai viet hoa / New password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Mat khau moi phai chua it nhat 1 chu cai viet thuong / New password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Mat khau moi phai chua it nhat 1 chu so / New password must contain at least one number')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "OldPass123",
                "new_password": "NewSecurePass456"
            }
        }
