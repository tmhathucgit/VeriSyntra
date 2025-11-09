"""
ROPA (Record of Processing Activities) Data Models
Vietnamese PDPL 2025 Decree 13/2023/ND-CP Article 12 Compliance

This module provides Pydantic models for generating Vietnamese PDPL-compliant
Record of Processing Activities (ROPA) per Decree 13/2023/ND-CP Article 12.

Legal References:
- Decree 13/2023/ND-CP Article 12: ROPA mandatory fields
- PDPL Article 17: Data controller obligations  
- Circular 09/2024/TT-BCA: MPS reporting specifications

ZERO HARD-CODING:
- Language enum instead of 'vi'/'en' strings
- Output format enum instead of string literals
- Type-safe data subject and recipient categories
- Pydantic validation for all fields
- Bilingual support via _vi suffix pattern

Document #3 Section 3: ROPA Data Model - COMPLETE
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class ROPALanguage(str, Enum):
    """
    Language options for ROPA generation - ZERO HARD-CODING
    
    Used throughout ROPA generation to eliminate hard-coded language checks.
    """
    VIETNAMESE = "vi"
    ENGLISH = "en"


class ROPAOutputFormat(str, Enum):
    """
    Output format options for ROPA export - ZERO HARD-CODING
    
    Supported export formats per MPS Circular 09/2024/TT-BCA
    """
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"
    MPS_FORMAT = "mps_format"


class DataSubjectCategory(str, Enum):
    """Vietnamese data subject categories per PDPL"""
    CUSTOMERS = "khach_hang"  # Khách hàng (Customers)
    EMPLOYEES = "nhan_vien"  # Nhân viên (Employees)
    SUPPLIERS = "nha_cung_cap"  # Nhà cung cấp (Suppliers)
    PARTNERS = "doi_tac"  # Đối tác (Partners)
    WEBSITE_VISITORS = "nguoi_truy_cap_website"  # Người truy cập website (Website visitors)
    CHILDREN = "tre_em"  # Trẻ em (Children under 16)


class RecipientCategory(str, Enum):
    """Recipient categories for data transfers"""
    INTERNAL = "noi_bo"  # Nội bộ (Internal departments)
    PROCESSOR = "ben_xu_ly"  # Bên xử lý (Data processors)
    THIRD_PARTY = "ben_thu_ba"  # Bên thứ ba (Third parties)
    PUBLIC_AUTHORITY = "co_quan_nha_nuoc"  # Cơ quan nhà nước (Government agencies)
    FOREIGN_ENTITY = "to_chuc_nuoc_ngoai"  # Tổ chức nước ngoài (Foreign entities)


class ROPAEntry(BaseModel):
    """
    Single Record of Processing Activity entry
    Per Decree 13/2023/ND-CP Article 12
    
    Represents one processing activity with all mandatory PDPL fields.
    Supports bilingual content (Vietnamese primary, English secondary)
    and column filter transparency for MPS reporting.
    
    Total fields: 49 (including 20 bilingual field pairs)
    """
    
    # === Identity Fields (2) ===
    entry_id: UUID
    tenant_id: UUID
    
    # === Controller Information - Article 12.1.a (7 fields) ===
    controller_name: str = Field(..., description="Tên tổ chức xử lý dữ liệu")
    controller_name_vi: str
    controller_address: str
    controller_tax_id: str = Field(..., description="Mã số thuế")
    controller_contact_person: str
    controller_phone: str
    controller_email: str
    
    # === DPO Information - Article 12.1.b (3 fields) ===
    dpo_name: Optional[str] = None
    dpo_name_vi: Optional[str] = None
    dpo_email: Optional[str] = None
    dpo_phone: Optional[str] = None
    
    # === Processing Activity - Article 12.1.c (6 fields) ===
    processing_activity_name: str
    processing_activity_name_vi: str
    processing_purpose: str
    processing_purpose_vi: str
    legal_basis: str
    legal_basis_vi: str
    
    # === Data Categories - Article 12.1.d (4 fields) ===
    data_categories: List[str] = Field(default_factory=list)
    data_categories_vi: List[str] = Field(default_factory=list)
    sensitive_data_categories: List[str] = Field(default_factory=list)
    sensitive_data_categories_vi: List[str] = Field(default_factory=list)
    has_sensitive_data: bool = Field(
        default=False,
        description="Whether this entry processes sensitive personal data"
    )
    
    # === Column Filter Transparency (5 fields) ===
    # For MPS reporting when not all discovered fields are included
    column_filter_applied: bool = Field(default=False)
    filter_scope_statement: Optional[str] = Field(
        default=None,
        description="Vietnamese statement describing column filter scope"
    )
    filter_scope_statement_en: Optional[str] = None
    total_fields_discovered: Optional[int] = None
    fields_included_in_ropa: Optional[int] = None
    
    # === Data Subjects - Article 12.1.e (2 fields) ===
    data_subject_categories: List[DataSubjectCategory] = Field(default_factory=list)
    estimated_data_subjects: Optional[int] = None
    
    # === Recipients - Article 12.1.f (1 field) ===
    recipients: List[Dict[str, Any]] = Field(
        default_factory=list,
        description='List of recipients, e.g., [{"name": "AWS", "type": "processor", "country": "SG"}]'
    )
    
    # === Cross-Border Transfers - Article 12.1.g (5 fields) ===
    has_cross_border_transfer: bool = False
    destination_countries: List[str] = Field(default_factory=list)
    transfer_mechanism: Optional[str] = None
    transfer_safeguards: List[str] = Field(default_factory=list)
    transfer_safeguards_vi: List[str] = Field(default_factory=list)
    
    # === Retention Period - Article 12.1.h (4 fields) ===
    retention_period: str
    retention_period_vi: str
    deletion_procedure: Optional[str] = None
    deletion_procedure_vi: Optional[str] = None
    
    # === Security Measures - Article 12.1.i (2 fields) ===
    security_measures: List[str] = Field(default_factory=list)
    security_measures_vi: List[str] = Field(default_factory=list)
    
    # === Processing Location - Article 12.1.j (2 fields) ===
    processing_locations: List[str] = Field(default_factory=list)
    data_center_region: Optional[str] = Field(
        default=None,
        description="Vietnamese regional context: 'north', 'central', or 'south'"
    )
    
    # === Metadata (3 fields) ===
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    
    class Config:
        """Pydantic configuration with Vietnamese example"""
        json_schema_extra = {
            "example": {
                "controller_name": "ABC Company Limited",
                "controller_name_vi": "Công ty TNHH ABC",
                "controller_address": "123 Nguyễn Huệ, Quận 1, TP.HCM",
                "controller_tax_id": "0123456789",
                "processing_activity_name": "Customer Relationship Management",
                "processing_activity_name_vi": "Quản lý quan hệ khách hàng",
                "column_filter_applied": True,
                "filter_scope_statement": "Báo cáo này chỉ bao gồm các trường dữ liệu cá nhân được chỉ định (45/150 trường)",
                "filter_scope_statement_en": "This report includes only specified personal data fields (45/150 fields)",
                "total_fields_discovered": 150,
                "fields_included_in_ropa": 45,
                "processing_purpose": "Manage customer information and provide services",
                "processing_purpose_vi": "Quản lý thông tin khách hàng và cung cấp dịch vụ",
                "legal_basis": "contract",
                "legal_basis_vi": "Thực hiện hợp đồng",
                "data_categories": ["Full name", "Email", "Phone number"],
                "data_categories_vi": ["Họ và tên", "Email", "Số điện thoại"],
                "retention_period": "5 years after contract termination",
                "retention_period_vi": "5 năm sau khi kết thúc hợp đồng"
            }
        }


class ROPADocument(BaseModel):
    """
    Complete ROPA document container
    Per Decree 13/2023/ND-CP Article 12
    
    Contains multiple processing activities (ROPAEntry) with
    summary statistics and MPS submission tracking.
    
    Total fields: 16
    """
    
    # === Document Identity (2 fields) ===
    document_id: UUID
    tenant_id: UUID
    
    # === Document Metadata (4 fields) ===
    generated_date: datetime
    generated_by: UUID
    version: str = "1.0"
    status: str = Field(
        default="draft",
        description="Document status: 'draft', 'approved', or 'submitted'"
    )
    
    # === Vietnamese Business Context (1 field) ===
    veri_business_context: Dict[str, Any] = Field(
        description="VeriSyntra business intelligence context (region, industry, etc.)"
    )
    
    # === Processing Activities (1 field) ===
    entries: List[ROPAEntry] = Field(
        description="List of processing activity entries"
    )
    
    # === Summary Statistics (4 fields) ===
    total_processing_activities: int
    total_data_subjects: Optional[int] = None
    has_sensitive_data: bool = False
    has_cross_border_transfers: bool = False
    
    # === Compliance Checklist (1 field) ===
    compliance_checklist: Dict[str, bool] = Field(
        default_factory=dict,
        description="PDPL compliance verification checklist"
    )
    
    # === MPS Submission (3 fields) ===
    mps_submitted: bool = False
    mps_submission_date: Optional[datetime] = None
    mps_reference_number: Optional[str] = Field(
        default=None,
        description="MPS (Ministry of Public Security) submission reference"
    )
    
    class Config:
        """Pydantic configuration with example"""
        json_schema_extra = {
            "example": {
                "document_id": "123e4567-e89b-12d3-a456-426614174000",
                "tenant_id": "tenant-001",
                "version": "1.0",
                "status": "draft",
                "total_processing_activities": 5,
                "has_sensitive_data": True,
                "has_cross_border_transfers": False,
                "veri_business_context": {
                    "region": "south",
                    "industry": "technology",
                    "business_size": "enterprise"
                }
            }
        }


# Module exports
__all__ = [
    # Enums
    'ROPALanguage',
    'ROPAOutputFormat',
    'DataSubjectCategory',
    'RecipientCategory',
    
    # Models
    'ROPAEntry',
    'ROPADocument',
]
