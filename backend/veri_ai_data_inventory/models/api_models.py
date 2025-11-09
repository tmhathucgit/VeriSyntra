"""
API Request/Response Models for ROPA Generation
Vietnamese PDPL 2025 Compliance - Document #3 Section 7

This module provides Pydantic models for ROPA generation API endpoints.
All models follow zero hard-coding patterns using enums and type safety.

Document #3 Section 7: API Endpoints - API Models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum

from .ropa_models import ROPALanguage, ROPAOutputFormat


class ROPAGenerateRequest(BaseModel):
    """
    Request model for ROPA generation - ZERO HARD-CODING
    
    Uses enums for format and language validation instead of strings.
    All fields are type-safe with Vietnamese context support.
    """
    tenant_id: UUID = Field(..., description="Tenant UUID for multi-tenancy")
    format: ROPAOutputFormat = Field(
        default=ROPAOutputFormat.JSON,
        description="Output format: json, csv, pdf, or mps_format"
    )
    language: ROPALanguage = Field(
        default=ROPALanguage.VIETNAMESE,
        description="Output language: vi (Vietnamese) or en (English)"
    )
    include_sensitive: bool = Field(
        default=True,
        description="Include sensitive data categories in ROPA"
    )
    include_cross_border: bool = Field(
        default=True,
        description="Include cross-border transfer information"
    )
    veri_business_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Vietnamese business context (region, industry, size)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
                "format": "pdf",
                "language": "vi",
                "include_sensitive": True,
                "include_cross_border": True,
                "veri_business_context": {
                    "region": "south",
                    "industry": "technology",
                    "business_size": "enterprise"
                }
            }
        }


class ROPAGenerateResponse(BaseModel):
    """Response after successful ROPA generation"""
    ropa_document_id: UUID = Field(..., description="Generated ROPA document UUID")
    download_url: str = Field(..., description="URL to download the generated ROPA")
    mps_compliant: bool = Field(..., description="MPS (Bộ Công an) compliance status")
    generated_at: datetime = Field(..., description="Generation timestamp (Asia/Ho_Chi_Minh)")
    file_size_bytes: int = Field(..., description="Generated file size in bytes")
    entry_count: int = Field(..., description="Number of processing activities")
    format: ROPAOutputFormat = Field(..., description="Generated document format")
    language: ROPALanguage = Field(..., description="Generated document language")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ropa_document_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "download_url": "/api/v1/data-inventory/550e8400-e29b-41d4-a716-446655440000/ropa/7c9e6679-7425-40de-944b-e07fc1f90ae7/download",
                "mps_compliant": True,
                "generated_at": "2025-11-05T22:00:00+07:00",
                "file_size_bytes": 26209,
                "entry_count": 5,
                "format": "pdf",
                "language": "vi"
            }
        }


class ROPAMetadata(BaseModel):
    """Metadata for a single ROPA document"""
    ropa_id: UUID
    tenant_id: UUID
    format: ROPAOutputFormat
    language: ROPALanguage
    generated_at: datetime
    file_size_bytes: int
    download_url: str
    entry_count: int
    mps_compliant: bool
    has_sensitive_data: bool
    has_cross_border_transfers: bool


class ROPAListResponse(BaseModel):
    """Response for listing ROPA documents with pagination"""
    total: int = Field(..., description="Total number of ROPA documents")
    items: List[ROPAMetadata] = Field(..., description="ROPA document metadata list")
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")
    has_next: bool = Field(..., description="Whether there are more pages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 25,
                "items": [],
                "page": 1,
                "page_size": 20,
                "has_next": True
            }
        }


class ROPAPreviewResponse(BaseModel):
    """
    Preview ROPA metadata without generating full document
    
    Useful for checking what will be included before generation
    """
    entry_count: int = Field(..., description="Number of processing activities")
    data_categories: List[str] = Field(..., description="Unique data categories found")
    has_sensitive_data: bool = Field(..., description="Whether sensitive data is processed")
    has_cross_border_transfers: bool = Field(..., description="Whether cross-border transfers exist")
    compliance_checklist: Dict[str, bool] = Field(
        ...,
        description="Vietnamese PDPL compliance checklist status"
    )
    estimated_file_size_kb: int = Field(..., description="Estimated file size in KB")
    
    class Config:
        json_schema_extra = {
            "example": {
                "entry_count": 5,
                "data_categories": ["Họ và tên", "Email", "Số điện thoại", "Địa chỉ"],
                "has_sensitive_data": False,
                "has_cross_border_transfers": True,
                "compliance_checklist": {
                    "has_controller_info": True,
                    "has_dpo": True,
                    "has_legal_basis": True,
                    "has_retention_period": True,
                    "has_security_measures": True
                },
                "estimated_file_size_kb": 25
            }
        }


class ROPADeleteResponse(BaseModel):
    """Response after ROPA document deletion"""
    success: bool = Field(..., description="Whether deletion was successful")
    message: str = Field(..., description="Deletion confirmation message")
    deleted_at: datetime = Field(..., description="Deletion timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "ROPA document deleted successfully",
                "deleted_at": "2025-11-05T22:05:00+07:00"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response format"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message in English")
    message_vi: str = Field(..., description="Error message in Vietnamese")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "TenantNotFound",
                "message": "Tenant not found",
                "message_vi": "Không tìm thấy tenant",
                "details": {
                    "tenant_id": "550e8400-e29b-41d4-a716-446655440000"
                }
            }
        }


# Export all API models
__all__ = [
    'ROPAGenerateRequest',
    'ROPAGenerateResponse',
    'ROPAMetadata',
    'ROPAListResponse',
    'ROPAPreviewResponse',
    'ROPADeleteResponse',
    'ErrorResponse'
]
