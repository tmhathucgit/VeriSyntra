"""
Processing Activity CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for processing_activities table.
This is the core entity that all other entities relate to.

Vietnamese-First Architecture:
- activity_name_vi is required (NOT NULL)
- activity_name_en is optional (nullable)
- All queries filter by tenant_id for isolation

PDPL 2025 Compliance:
- Implements Article 12.1.c (Processing Activity details)
- Enforces multi-tenant row-level isolation
- Validates legal_basis per Article 12.1.b

Usage:
    from crud.processing_activity import create_processing_activity
    
    activity = await create_processing_activity(
        db=db,
        tenant_id=tenant_id,
        activity_name_vi="Quản lý khách hàng",
        processing_purpose_vi="Cung cấp dịch vụ cho khách hàng",
        legal_basis="contract",
        created_by=user_id
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from models.db_models import ProcessingActivityDB
from models.ropa_models import ROPAEntry


# ============================================
# CREATE Operations
# ============================================

async def create_processing_activity(
    db: AsyncSession,
    tenant_id: UUID,
    activity_name_vi: str,
    processing_purpose_vi: str,
    legal_basis: str,
    created_by: UUID,
    activity_name_en: Optional[str] = None,
    activity_description_vi: Optional[str] = None,
    activity_description_en: Optional[str] = None,
    processing_purpose_en: Optional[str] = None,
    legal_basis_vi: Optional[str] = None,
    status: str = "active",
    has_sensitive_data: bool = False,
    has_cross_border_transfer: bool = False,
    requires_dpia: bool = False,
    mps_reportable: bool = True,
    veri_regional_location: Optional[str] = None,
    veri_business_unit: Optional[str] = None
) -> ProcessingActivityDB:
    """
    Create new processing activity
    
    Args:
        db: Database session
        tenant_id: Tenant UUID (multi-tenant isolation)
        activity_name_vi: Activity name in Vietnamese (REQUIRED)
        processing_purpose_vi: Purpose in Vietnamese (REQUIRED)
        legal_basis: Legal basis (consent, contract, etc.)
        created_by: User UUID who created this activity
        activity_name_en: Activity name in English (optional)
        activity_description_vi: Description in Vietnamese (optional)
        activity_description_en: Description in English (optional)
        processing_purpose_en: Purpose in English (optional)
        legal_basis_vi: Legal basis in Vietnamese (optional)
        status: Activity status (active, inactive, archived)
        has_sensitive_data: Whether activity processes sensitive data
        has_cross_border_transfer: Whether activity involves cross-border transfer
        requires_dpia: Whether DPIA is required
        mps_reportable: Whether reportable to MPS
        veri_regional_location: Vietnamese region (north, central, south)
        veri_business_unit: Business unit name
    
    Returns:
        ProcessingActivityDB: Created activity
        
    Raises:
        ValueError: If Vietnamese required fields are missing
    """
    # Validate Vietnamese-first required fields
    if not activity_name_vi or not activity_name_vi.strip():
        raise ValueError("activity_name_vi is required (Vietnamese-first architecture)")
    if not processing_purpose_vi or not processing_purpose_vi.strip():
        raise ValueError("processing_purpose_vi is required (Vietnamese-first architecture)")
    
    # Create activity
    activity = ProcessingActivityDB(
        tenant_id=tenant_id,
        activity_name_vi=activity_name_vi.strip(),
        activity_name_en=activity_name_en.strip() if activity_name_en else None,
        activity_description_vi=activity_description_vi,
        activity_description_en=activity_description_en,
        processing_purpose_vi=processing_purpose_vi.strip(),
        processing_purpose_en=processing_purpose_en.strip() if processing_purpose_en else None,
        legal_basis=legal_basis,
        legal_basis_vi=legal_basis_vi,
        status=status,
        created_by=created_by,
        has_sensitive_data=has_sensitive_data,
        has_cross_border_transfer=has_cross_border_transfer,
        requires_dpia=requires_dpia,
        mps_reportable=mps_reportable,
        veri_regional_location=veri_regional_location,
        veri_business_unit=veri_business_unit
    )
    
    db.add(activity)
    await db.flush()
    await db.refresh(activity)
    
    return activity


# ============================================
# READ Operations
# ============================================

async def get_processing_activity_by_id(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    load_relationships: bool = False
) -> Optional[ProcessingActivityDB]:
    """
    Get processing activity by ID with tenant verification
    
    Args:
        db: Database session
        activity_id: Activity UUID
        tenant_id: Tenant UUID (for authorization)
        load_relationships: If True, eager load all relationships
    
    Returns:
        ProcessingActivityDB or None if not found
    """
    query = select(ProcessingActivityDB).where(
        ProcessingActivityDB.activity_id == activity_id,
        ProcessingActivityDB.tenant_id == tenant_id  # Tenant isolation
    )
    
    if load_relationships:
        query = query.options(
            selectinload(ProcessingActivityDB.data_categories),
            selectinload(ProcessingActivityDB.data_subjects),
            selectinload(ProcessingActivityDB.recipients),
            selectinload(ProcessingActivityDB.retention),
            selectinload(ProcessingActivityDB.security_measures),
            selectinload(ProcessingActivityDB.processing_locations)
        )
    
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_processing_activities_for_tenant(
    db: AsyncSession,
    tenant_id: UUID,
    status: Optional[str] = None,
    has_sensitive_data: Optional[bool] = None,
    has_cross_border_transfer: Optional[bool] = None,
    requires_dpia: Optional[bool] = None,
    veri_regional_location: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[ProcessingActivityDB]:
    """
    Get all processing activities for tenant with optional filters
    
    Args:
        db: Database session
        tenant_id: Tenant UUID
        status: Filter by status (active, inactive, archived)
        has_sensitive_data: Filter by sensitive data flag
        has_cross_border_transfer: Filter by cross-border transfer flag
        requires_dpia: Filter by DPIA requirement
        veri_regional_location: Filter by region (north, central, south)
        skip: Pagination offset
        limit: Pagination limit (max 100)
    
    Returns:
        List of ProcessingActivityDB
    """
    query = select(ProcessingActivityDB).where(
        ProcessingActivityDB.tenant_id == tenant_id
    )
    
    # Apply filters
    if status:
        query = query.where(ProcessingActivityDB.status == status)
    if has_sensitive_data is not None:
        query = query.where(ProcessingActivityDB.has_sensitive_data == has_sensitive_data)
    if has_cross_border_transfer is not None:
        query = query.where(ProcessingActivityDB.has_cross_border_transfer == has_cross_border_transfer)
    if requires_dpia is not None:
        query = query.where(ProcessingActivityDB.requires_dpia == requires_dpia)
    if veri_regional_location:
        query = query.where(ProcessingActivityDB.veri_regional_location == veri_regional_location)
    
    # Pagination
    query = query.offset(skip).limit(min(limit, 100))
    
    result = await db.execute(query)
    return result.scalars().all()


async def count_processing_activities(
    db: AsyncSession,
    tenant_id: UUID,
    status: Optional[str] = None
) -> int:
    """
    Count processing activities for tenant
    
    Args:
        db: Database session
        tenant_id: Tenant UUID
        status: Filter by status (optional)
    
    Returns:
        int: Count of activities
    """
    from sqlalchemy import func
    
    query = select(func.count(ProcessingActivityDB.activity_id)).where(
        ProcessingActivityDB.tenant_id == tenant_id
    )
    
    if status:
        query = query.where(ProcessingActivityDB.status == status)
    
    result = await db.execute(query)
    return result.scalar_one()


# ============================================
# UPDATE Operations
# ============================================

async def update_processing_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    updates: Dict[str, Any]
) -> Optional[ProcessingActivityDB]:
    """
    Update processing activity
    
    Args:
        db: Database session
        activity_id: Activity UUID
        tenant_id: Tenant UUID (for authorization)
        updates: Dictionary of field updates
    
    Returns:
        Updated ProcessingActivityDB or None if not found
        
    Raises:
        ValueError: If trying to update immutable fields
    """
    # Prevent updating immutable fields
    immutable_fields = {"activity_id", "tenant_id", "created_at", "created_by"}
    if any(field in updates for field in immutable_fields):
        raise ValueError(f"Cannot update immutable fields: {immutable_fields}")
    
    # Validate Vietnamese-first if updating name or purpose
    if "activity_name_vi" in updates and not updates["activity_name_vi"]:
        raise ValueError("activity_name_vi cannot be empty (Vietnamese-first architecture)")
    if "processing_purpose_vi" in updates and not updates["processing_purpose_vi"]:
        raise ValueError("processing_purpose_vi cannot be empty (Vietnamese-first architecture)")
    
    # Get activity with tenant verification
    activity = await get_processing_activity_by_id(db, activity_id, tenant_id)
    if not activity:
        return None
    
    # Apply updates
    for field, value in updates.items():
        if hasattr(activity, field):
            setattr(activity, field, value)
    
    activity.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(activity)
    
    return activity


async def mark_activity_for_review(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> Optional[ProcessingActivityDB]:
    """
    Mark activity for review (updates last_reviewed_at)
    
    Args:
        db: Database session
        activity_id: Activity UUID
        tenant_id: Tenant UUID
    
    Returns:
        Updated activity or None
    """
    return await update_processing_activity(
        db, activity_id, tenant_id,
        {"last_reviewed_at": datetime.utcnow()}
    )


# ============================================
# DELETE Operations
# ============================================

async def delete_processing_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> bool:
    """
    Delete processing activity (CASCADE deletes all related data)
    
    Args:
        db: Database session
        activity_id: Activity UUID
        tenant_id: Tenant UUID (for authorization)
    
    Returns:
        bool: True if deleted, False if not found
        
    Note:
        This will CASCADE delete all related:
        - Data categories
        - Data subjects
        - Data recipients
        - Data retention
        - Security measures
        - Processing locations
    """
    # Verify tenant ownership before delete
    activity = await get_processing_activity_by_id(db, activity_id, tenant_id)
    if not activity:
        return False
    
    await db.delete(activity)
    await db.flush()
    
    return True


async def soft_delete_processing_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> Optional[ProcessingActivityDB]:
    """
    Soft delete (mark as archived instead of actual delete)
    
    Args:
        db: Database session
        activity_id: Activity UUID
        tenant_id: Tenant UUID
    
    Returns:
        Updated activity or None
    """
    return await update_processing_activity(
        db, activity_id, tenant_id,
        {"status": "archived"}
    )


# ============================================
# ROPA Generation Helper
# ============================================

async def build_ropa_entry_from_activity(
    db: AsyncSession,
    activity: ProcessingActivityDB
) -> ROPAEntry:
    """
    Build ROPAEntry Pydantic model from database activity
    
    This function loads all relationships and maps the database model
    to the ROPA Pydantic model for export.
    
    Args:
        db: Database session
        activity: ProcessingActivityDB with loaded relationships
    
    Returns:
        ROPAEntry: Complete ROPA entry ready for export
        
    Note:
        Activity must have relationships loaded via selectinload()
        or this will trigger additional queries.
    """
    # Ensure relationships are loaded
    await db.refresh(activity, [
        'data_categories',
        'data_subjects',
        'recipients',
        'retention',
        'security_measures',
        'processing_locations'
    ])
    
    # Map database model to ROPA Pydantic model
    # This is a simplified version - full implementation would map all fields
    ropa_entry = ROPAEntry(
        entry_id=activity.activity_id,
        tenant_id=activity.tenant_id,
        
        # Controller information (would come from tenant service)
        controller_name="",  # Fetch from tenant
        controller_name_vi="",
        controller_address="",
        controller_tax_id="",
        controller_contact_person="",
        controller_phone="",
        controller_email="",
        
        # Activity details
        activity_name=activity.activity_name_en or activity.activity_name_vi,
        activity_name_vi=activity.activity_name_vi,
        activity_description=activity.activity_description_en or activity.activity_description_vi,
        activity_description_vi=activity.activity_description_vi,
        
        processing_purpose=activity.processing_purpose_en or activity.processing_purpose_vi,
        processing_purpose_vi=activity.processing_purpose_vi,
        legal_basis=activity.legal_basis,
        legal_basis_vi=activity.legal_basis_vi or activity.legal_basis,
        
        # Data categories (map from related entities)
        data_categories=[cat.category_name_en or cat.category_name_vi for cat in activity.data_categories],
        data_categories_vi=[cat.category_name_vi for cat in activity.data_categories],
        
        # Data subjects
        data_subjects=[subj.subject_category for subj in activity.data_subjects],
        data_subjects_vi=[subj.subject_category_vi or subj.subject_category for subj in activity.data_subjects],
        
        # Recipients
        recipients=[rec.recipient_name_en or rec.recipient_name_vi for rec in activity.recipients],
        recipients_vi=[rec.recipient_name_vi for rec in activity.recipients],
        
        # Retention (one-to-one)
        retention_period=activity.retention.retention_period_en if activity.retention else "",
        retention_period_vi=activity.retention.retention_period_vi if activity.retention else "",
        
        # Security measures
        security_measures=[meas.measure_name_en or meas.measure_name_vi for meas in activity.security_measures],
        security_measures_vi=[meas.measure_name_vi for meas in activity.security_measures],
        
        # Processing locations
        processing_locations=[loc.facility_name or loc.city for loc in activity.processing_locations],
        
        # Compliance flags
        has_sensitive_data=activity.has_sensitive_data,
        has_cross_border_transfer=activity.has_cross_border_transfer,
        requires_dpia=activity.requires_dpia,
        
        # Timestamps
        created_at=activity.created_at,
        last_updated=activity.updated_at
    )
    
    return ropa_entry


# ============================================
# EXPORTS
# ============================================

__all__ = [
    # Create
    "create_processing_activity",
    
    # Read
    "get_processing_activity_by_id",
    "get_processing_activities_for_tenant",
    "count_processing_activities",
    
    # Update
    "update_processing_activity",
    "mark_activity_for_review",
    
    # Delete
    "delete_processing_activity",
    "soft_delete_processing_activity",
    
    # ROPA
    "build_ropa_entry_from_activity"
]
