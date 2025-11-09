"""
SQLAlchemy ORM Models for Data Inventory
Vietnamese PDPL 2025 Compliance Database Models

This module provides database models for ROPA generation per 
Decree 13/2023/ND-CP Article 12.

Vietnamese-First Architecture:
- All *_vi fields: NOT NULL (Vietnamese primary)
- All *_en fields: Nullable (English fallback)
- Database identifiers: ASCII-safe (no diacritics)

PDPL 2025 Compliance:
- Implements all Article 12.1.a through 12.1.j requirements
- Multi-tenant row-level isolation via tenant_id
- Complete audit trail per Article 43
- Cross-border transfer tracking per Article 20

Usage:
    from models.db_models import ProcessingActivityDB
    from database.connection import get_db
    
    async def get_activities(db: AsyncSession, tenant_id: UUID):
        result = await db.execute(
            select(ProcessingActivityDB).where(
                ProcessingActivityDB.tenant_id == tenant_id
            )
        )
        return result.scalars().all()
"""

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text, ForeignKey, CheckConstraint, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database.base import Base


# ============================================
# CORE MODELS (Tables 1-2)
# ============================================

class ProcessingActivityDB(Base):
    """
    Processing Activity Database Model
    Decree 13/2023/ND-CP Article 12.1.c
    
    Represents a processing activity as defined by PDPL 2025.
    This is the core entity that all other entities relate to.
    
    Relationships:
        - One-to-many with data_categories
        - One-to-many with data_subjects
        - One-to-many with data_recipients
        - One-to-one with data_retention
        - One-to-many with security_measures
        - One-to-many with processing_locations
    """
    __tablename__ = "processing_activities"
    
    # Identity
    activity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Activity Details (Article 12.1.c) - Vietnamese-first
    activity_name_vi = Column(String(200), nullable=False)  # Vietnamese primary
    activity_name_en = Column(String(200))                  # English fallback
    activity_description_vi = Column(Text)
    activity_description_en = Column(Text)
    
    # Processing Details (Article 12.1.a, 12.1.b) - Vietnamese-first
    processing_purpose_vi = Column(Text, nullable=False)  # Vietnamese primary (Art. 12.1.a)
    processing_purpose_en = Column(Text)                  # English fallback
    legal_basis = Column(String(100), nullable=False)     # Art. 12.1.b
    legal_basis_vi = Column(String(100))
    
    # Status and Lifecycle
    status = Column(String(30), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    last_reviewed_at = Column(DateTime)
    
    # Compliance Flags
    has_sensitive_data = Column(Boolean, default=False)
    has_cross_border_transfer = Column(Boolean, default=False)
    requires_dpia = Column(Boolean, default=False)
    mps_reportable = Column(Boolean, default=True)
    
    # Vietnamese Business Context
    veri_regional_location = Column(String(20))  # north, central, south
    veri_business_unit = Column(String(100))
    
    # Relationships - All with CASCADE delete
    data_categories = relationship(
        "DataCategoryDB",
        back_populates="activity",
        cascade="all, delete-orphan"
    )
    data_subjects = relationship(
        "DataSubjectDB",
        back_populates="activity",
        cascade="all, delete-orphan"
    )
    recipients = relationship(
        "DataRecipientDB",
        back_populates="activity",
        cascade="all, delete-orphan"
    )
    retention = relationship(
        "DataRetentionDB",
        back_populates="activity",
        uselist=False,  # One-to-one relationship
        cascade="all, delete-orphan"
    )
    security_measures = relationship(
        "SecurityMeasureDB",
        back_populates="activity",
        cascade="all, delete-orphan"
    )
    processing_locations = relationship(
        "ProcessingLocationDB",
        back_populates="activity",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<ProcessingActivityDB(activity_id={self.activity_id}, name_vi='{self.activity_name_vi}')>"


class DataCategoryDB(Base):
    """
    Data Category Database Model
    Article 12.1.d: Data Categories
    
    Represents categories of personal data processed in an activity.
    Uses TEXT[] arrays for bilingual field name lists.
    """
    __tablename__ = "data_categories"
    
    # Identity
    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("processing_activities.activity_id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Category Details - Vietnamese-first
    category_name_vi = Column(String(100), nullable=False)  # Vietnamese primary
    category_name_en = Column(String(100))                  # English fallback
    category_type = Column(String(50), nullable=False)
    
    # Data Fields - Vietnamese-first (PostgreSQL TEXT[] arrays)
    data_fields_vi = Column(ARRAY(Text), default=list)  # Vietnamese primary
    data_fields_en = Column(ARRAY(Text), default=list)  # English fallback
    
    # Sensitivity Classification
    is_sensitive = Column(Boolean, default=False)  # Sensitive per Article 4.8 PDPL
    sensitivity_reason = Column(String(200))
    
    # Column Filter Transparency (Document #3 Integration) - Vietnamese-first
    total_fields_discovered = Column(Integer)
    fields_included = Column(Integer)
    filter_scope_statement_vi = Column(Text)  # Vietnamese primary
    filter_scope_statement_en = Column(Text)  # English fallback
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    activity = relationship("ProcessingActivityDB", back_populates="data_categories")
    
    def __repr__(self):
        return f"<DataCategoryDB(category_id={self.category_id}, name_vi='{self.category_name_vi}')>"


# ============================================
# RELATIONSHIP MODELS (Tables 3-5)
# ============================================

class DataSubjectDB(Base):
    """
    Data Subject Database Model
    Article 12.1.e: Data Subject Categories
    
    Represents categories of data subjects (individuals) whose data is processed.
    """
    __tablename__ = "data_subjects"
    
    # Identity
    subject_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("processing_activities.activity_id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Subject Category
    subject_category = Column(String(50), nullable=False)
    subject_category_vi = Column(String(50))
    
    # Volume Estimates
    estimated_count = Column(Integer)
    count_basis = Column(String(100))  # actual, estimated, range
    
    # Special Categories
    includes_children = Column(Boolean, default=False)  # Under 16 per Vietnamese law
    includes_vulnerable = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    activity = relationship("ProcessingActivityDB", back_populates="data_subjects")
    
    def __repr__(self):
        return f"<DataSubjectDB(subject_id={self.subject_id}, category='{self.subject_category}')>"


class DataRecipientDB(Base):
    """
    Data Recipient Database Model
    Article 12.1.f: Recipients
    Article 12.1.g: Cross-Border Transfers
    
    Represents recipients of personal data, including cross-border transfers.
    Uses TEXT[] arrays for bilingual safeguard lists.
    """
    __tablename__ = "data_recipients"
    
    # Identity
    recipient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("processing_activities.activity_id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Recipient Information - Vietnamese-first
    recipient_name_vi = Column(String(200), nullable=False)  # Vietnamese primary
    recipient_name_en = Column(String(200))                  # English fallback
    recipient_type = Column(String(50), nullable=False)
    recipient_type_vi = Column(String(50))
    
    # Location (Article 12.1.g - Cross-Border) - Vietnamese-first
    country_code = Column(String(2), default='VN')
    country_name_vi = Column(String(100))  # Vietnamese primary
    country_name_en = Column(String(100))  # English fallback
    is_cross_border = Column(Boolean, default=False)
    
    # Transfer Safeguards (if cross-border) - Article 20
    transfer_mechanism = Column(String(100))
    transfer_mechanism_vi = Column(String(100))
    safeguards_vi = Column(ARRAY(Text), default=list)  # Vietnamese primary (PostgreSQL TEXT[])
    safeguards_en = Column(ARRAY(Text), default=list)  # English fallback (PostgreSQL TEXT[])
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    activity = relationship("ProcessingActivityDB", back_populates="recipients")
    
    def __repr__(self):
        return f"<DataRecipientDB(recipient_id={self.recipient_id}, name_vi='{self.recipient_name_vi}')>"


class DataRetentionDB(Base):
    """
    Data Retention Database Model
    Article 12.1.h: Retention Period
    
    Represents retention periods and deletion procedures.
    One-to-one relationship with processing activities.
    """
    __tablename__ = "data_retention"
    
    # Identity
    retention_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("processing_activities.activity_id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Retention Period - Vietnamese-first
    retention_period_vi = Column(String(100), nullable=False)  # "5 nam", "Den khi cham dut hop dong + 2 nam"
    retention_period_en = Column(String(100))                  # "5 years", "Until contract termination + 2 years"
    retention_period_days = Column(Integer)  # Normalized to days for calculations
    
    # Deletion Procedures - Vietnamese-first
    deletion_procedure_vi = Column(Text)  # Vietnamese primary
    deletion_procedure_en = Column(Text)  # English fallback
    deletion_method = Column(String(50))
    
    # Review Requirements
    review_frequency_months = Column(Integer, default=12)
    next_review_date = Column(Date)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship (one-to-one)
    activity = relationship("ProcessingActivityDB", back_populates="retention")
    
    def __repr__(self):
        return f"<DataRetentionDB(retention_id={self.retention_id}, period_vi='{self.retention_period_vi}')>"


# ============================================
# SUPPORTING MODELS (Tables 6-9)
# ============================================

class SecurityMeasureDB(Base):
    """
    Security Measure Database Model
    Article 12.1.i: Security Measures
    
    Represents technical and organizational security measures.
    """
    __tablename__ = "security_measures"
    
    # Identity
    measure_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("processing_activities.activity_id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Measure Details - Vietnamese-first
    measure_type = Column(String(50), nullable=False)
    measure_name_vi = Column(String(200), nullable=False)  # Vietnamese primary
    measure_name_en = Column(String(200))                  # English fallback
    measure_description = Column(Text)
    
    # Implementation Status
    is_implemented = Column(Boolean, default=True)
    implementation_date = Column(Date)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    activity = relationship("ProcessingActivityDB", back_populates="security_measures")
    
    def __repr__(self):
        return f"<SecurityMeasureDB(measure_id={self.measure_id}, name_vi='{self.measure_name_vi}')>"


class ProcessingLocationDB(Base):
    """
    Processing Location Database Model
    Article 12.1.j: Processing Locations
    
    Represents physical/cloud locations where data is processed.
    Includes Vietnamese regional context (North/Central/South).
    """
    __tablename__ = "processing_locations"
    
    # Identity
    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("processing_activities.activity_id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Location Details
    location_type = Column(String(50))
    facility_name = Column(String(200))
    city = Column(String(100))
    province = Column(String(100))
    country_code = Column(String(2), default='VN')
    
    # Vietnamese Regional Context
    data_center_region = Column(String(20))  # north, central, south
    
    # Cloud Provider Details (if applicable)
    cloud_provider = Column(String(100))  # AWS, Azure, GCP, Viettel IDC, FPT Telecom
    cloud_region = Column(String(100))    # ap-southeast-1, etc.
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    activity = relationship("ProcessingActivityDB", back_populates="processing_locations")
    
    def __repr__(self):
        return f"<ProcessingLocationDB(location_id={self.location_id}, facility='{self.facility_name}')>"


class ROPADocumentDB(Base):
    """
    ROPA Document Database Model
    Tracks generated ROPA documents
    
    Stores metadata about generated ROPA documents, including:
    - Format (JSON, CSV, PDF, MPS format)
    - MPS submission tracking
    - Document lifecycle (draft, approved, submitted, archived)
    """
    __tablename__ = "ropa_documents"
    
    # Identity
    ropa_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Document Metadata
    document_format = Column(String(20), nullable=False)
    language = Column(String(5), nullable=False)
    file_path = Column(String(500))
    file_size_bytes = Column(Integer)
    
    # Generation Details
    generated_at = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(UUID(as_uuid=True), nullable=False)
    generation_parameters = Column(JSONB, default=dict)
    
    # Content Summary
    entry_count = Column(Integer, default=0)
    has_sensitive_data = Column(Boolean, default=False)
    has_cross_border_transfers = Column(Boolean, default=False)
    
    # MPS Submission Tracking
    mps_compliant = Column(Boolean, default=False)
    mps_submitted = Column(Boolean, default=False)
    mps_submission_date = Column(DateTime)
    mps_reference_number = Column(String(100))
    
    # Lifecycle
    status = Column(String(30), default='draft')
    approved_at = Column(DateTime)
    approved_by = Column(UUID(as_uuid=True))
    
    # Vietnamese Business Context
    veri_business_context = Column(JSONB, default=dict)
    
    def __repr__(self):
        return f"<ROPADocumentDB(ropa_id={self.ropa_id}, format='{self.document_format}', status='{self.status}')>"


class DataInventoryAuditDB(Base):
    """
    Data Inventory Audit Trail
    PDPL Compliance Requirement (Article 43)
    
    Complete audit log for all data inventory operations.
    Tracks who did what, when, and what changed.
    """
    __tablename__ = "data_inventory_audit"
    
    # Identity
    audit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # Action Details
    action_type = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    
    # User and Context
    user_id = Column(UUID(as_uuid=True), nullable=False)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    
    # Changes (for update actions) - JSONB for flexibility
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    
    # Bilingual Audit Message - Vietnamese-first
    audit_message_vi = Column(Text)  # Vietnamese primary
    audit_message_en = Column(Text)  # English fallback
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow)
    vietnam_time = Column(DateTime)  # Populated via trigger in database
    
    def __repr__(self):
        return f"<DataInventoryAuditDB(audit_id={self.audit_id}, action='{self.action_type}', entity='{self.entity_type}')>"


# ============================================
# EXPORTS
# ============================================

__all__ = [
    # Core models
    "ProcessingActivityDB",
    "DataCategoryDB",
    
    # Relationship models
    "DataSubjectDB",
    "DataRecipientDB",
    "DataRetentionDB",
    
    # Supporting models
    "SecurityMeasureDB",
    "ProcessingLocationDB",
    "ROPADocumentDB",
    "DataInventoryAuditDB"
]
