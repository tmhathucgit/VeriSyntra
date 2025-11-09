"""
Data Retention CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for data_retention table.
Retention represents data retention periods and deletion procedures (Article 12.1.h).

Vietnamese-First Architecture:
- retention_period_vi is required (NOT NULL)
- deletion_procedure_vi is primary
- One-to-one relationship with processing activities

Usage:
    from crud.data_retention import create_data_retention
    
    retention = await create_data_retention(
        db=db,
        activity_id=activity_id,
        tenant_id=tenant_id,
        retention_period_vi="5 năm",
        retention_period_days=1825,
        deletion_method="secure_deletion"
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from datetime import date

from models.db_models import DataRetentionDB


async def create_data_retention(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    retention_period_vi: str,
    retention_period_en: Optional[str] = None,
    retention_period_days: Optional[int] = None,
    deletion_procedure_vi: Optional[str] = None,
    deletion_procedure_en: Optional[str] = None,
    deletion_method: Optional[str] = None,
    review_frequency_months: int = 12,
    next_review_date: Optional[date] = None
) -> DataRetentionDB:
    """Create new data retention policy (one per activity)"""
    if not retention_period_vi or not retention_period_vi.strip():
        raise ValueError("retention_period_vi is required (Vietnamese-first architecture)")
    
    retention = DataRetentionDB(
        activity_id=activity_id,
        tenant_id=tenant_id,
        retention_period_vi=retention_period_vi.strip(),
        retention_period_en=retention_period_en.strip() if retention_period_en else None,
        retention_period_days=retention_period_days,
        deletion_procedure_vi=deletion_procedure_vi,
        deletion_procedure_en=deletion_procedure_en,
        deletion_method=deletion_method,
        review_frequency_months=review_frequency_months,
        next_review_date=next_review_date
    )
    
    db.add(retention)
    await db.flush()
    await db.refresh(retention)
    
    return retention


async def get_data_retention_for_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> Optional[DataRetentionDB]:
    """Get data retention policy for activity (one-to-one)"""
    result = await db.execute(
        select(DataRetentionDB).where(
            DataRetentionDB.activity_id == activity_id,
            DataRetentionDB.tenant_id == tenant_id
        )
    )
    return result.scalar_one_or_none()


async def update_data_retention(
    db: AsyncSession,
    retention_id: UUID,
    tenant_id: UUID,
    updates: dict
) -> Optional[DataRetentionDB]:
    """Update data retention policy"""
    result = await db.execute(
        select(DataRetentionDB).where(
            DataRetentionDB.retention_id == retention_id,
            DataRetentionDB.tenant_id == tenant_id
        )
    )
    retention = result.scalar_one_or_none()
    
    if not retention:
        return None
    
    for field, value in updates.items():
        if hasattr(retention, field):
            setattr(retention, field, value)
    
    await db.flush()
    await db.refresh(retention)
    
    return retention


async def delete_data_retention(
    db: AsyncSession,
    retention_id: UUID,
    tenant_id: UUID
) -> bool:
    """Delete data retention policy"""
    result = await db.execute(
        select(DataRetentionDB).where(
            DataRetentionDB.retention_id == retention_id,
            DataRetentionDB.tenant_id == tenant_id
        )
    )
    retention = result.scalar_one_or_none()
    
    if not retention:
        return False
    
    await db.delete(retention)
    await db.flush()
    return True


__all__ = [
    "create_data_retention",
    "get_data_retention_for_activity",
    "update_data_retention",
    "delete_data_retention"
]
