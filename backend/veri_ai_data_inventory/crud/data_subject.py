"""
Data Subject CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for data_subjects table.
Data subjects represent categories of individuals (Article 12.1.e).

Vietnamese-First Architecture:
- subject_category_vi provides Vietnamese translations
- Special handling for children (under 16 per PDPL)

Usage:
    from crud.data_subject import create_data_subject
    
    subject = await create_data_subject(
        db=db,
        activity_id=activity_id,
        tenant_id=tenant_id,
        subject_category="customers",
        subject_category_vi="Khách hàng",
        estimated_count=10000
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from models.db_models import DataSubjectDB


async def create_data_subject(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    subject_category: str,
    subject_category_vi: Optional[str] = None,
    estimated_count: Optional[int] = None,
    count_basis: Optional[str] = None,
    includes_children: bool = False,
    includes_vulnerable: bool = False
) -> DataSubjectDB:
    """Create new data subject category"""
    subject = DataSubjectDB(
        activity_id=activity_id,
        tenant_id=tenant_id,
        subject_category=subject_category,
        subject_category_vi=subject_category_vi,
        estimated_count=estimated_count,
        count_basis=count_basis,
        includes_children=includes_children,
        includes_vulnerable=includes_vulnerable
    )
    
    db.add(subject)
    await db.flush()
    await db.refresh(subject)
    
    return subject


async def get_data_subjects_for_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> List[DataSubjectDB]:
    """Get all data subjects for an activity"""
    result = await db.execute(
        select(DataSubjectDB).where(
            DataSubjectDB.activity_id == activity_id,
            DataSubjectDB.tenant_id == tenant_id
        )
    )
    return result.scalars().all()


async def get_activities_processing_children_data(
    db: AsyncSession,
    tenant_id: UUID
) -> List[DataSubjectDB]:
    """Get all data subjects involving children (under 16)"""
    result = await db.execute(
        select(DataSubjectDB).where(
            DataSubjectDB.tenant_id == tenant_id,
            DataSubjectDB.includes_children == True
        )
    )
    return result.scalars().all()


async def delete_data_subject(
    db: AsyncSession,
    subject_id: UUID,
    tenant_id: UUID
) -> bool:
    """Delete data subject"""
    result = await db.execute(
        select(DataSubjectDB).where(
            DataSubjectDB.subject_id == subject_id,
            DataSubjectDB.tenant_id == tenant_id
        )
    )
    subject = result.scalar_one_or_none()
    
    if not subject:
        return False
    
    await db.delete(subject)
    await db.flush()
    return True


__all__ = [
    "create_data_subject",
    "get_data_subjects_for_activity",
    "get_activities_processing_children_data",
    "delete_data_subject"
]
