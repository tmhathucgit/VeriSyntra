"""
Security Measure CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for security_measures table.
Security measures represent technical/organizational controls (Article 12.1.i).

Vietnamese-First Architecture:
- measure_name_vi is required (NOT NULL)
- Multiple measures per activity

Usage:
    from crud.security_measure import create_security_measure
    
    measure = await create_security_measure(
        db=db,
        activity_id=activity_id,
        tenant_id=tenant_id,
        measure_type="encryption",
        measure_name_vi="Mã hóa AES-256"
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
from datetime import date

from models.db_models import SecurityMeasureDB


async def create_security_measure(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    measure_type: str,
    measure_name_vi: str,
    measure_name_en: Optional[str] = None,
    measure_description: Optional[str] = None,
    is_implemented: bool = True,
    implementation_date: Optional[date] = None
) -> SecurityMeasureDB:
    """Create new security measure"""
    if not measure_name_vi or not measure_name_vi.strip():
        raise ValueError("measure_name_vi is required (Vietnamese-first architecture)")
    
    measure = SecurityMeasureDB(
        activity_id=activity_id,
        tenant_id=tenant_id,
        measure_type=measure_type,
        measure_name_vi=measure_name_vi.strip(),
        measure_name_en=measure_name_en.strip() if measure_name_en else None,
        measure_description=measure_description,
        is_implemented=is_implemented,
        implementation_date=implementation_date
    )
    
    db.add(measure)
    await db.flush()
    await db.refresh(measure)
    
    return measure


async def get_security_measures_for_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> List[SecurityMeasureDB]:
    """Get all security measures for an activity"""
    result = await db.execute(
        select(SecurityMeasureDB).where(
            SecurityMeasureDB.activity_id == activity_id,
            SecurityMeasureDB.tenant_id == tenant_id
        )
    )
    return result.scalars().all()


async def get_security_measures_by_type(
    db: AsyncSession,
    tenant_id: UUID,
    measure_type: str
) -> List[SecurityMeasureDB]:
    """Get all security measures of a specific type"""
    result = await db.execute(
        select(SecurityMeasureDB).where(
            SecurityMeasureDB.tenant_id == tenant_id,
            SecurityMeasureDB.measure_type == measure_type
        )
    )
    return result.scalars().all()


async def delete_security_measure(
    db: AsyncSession,
    measure_id: UUID,
    tenant_id: UUID
) -> bool:
    """Delete security measure"""
    result = await db.execute(
        select(SecurityMeasureDB).where(
            SecurityMeasureDB.measure_id == measure_id,
            SecurityMeasureDB.tenant_id == tenant_id
        )
    )
    measure = result.scalar_one_or_none()
    
    if not measure:
        return False
    
    await db.delete(measure)
    await db.flush()
    return True


__all__ = [
    "create_security_measure",
    "get_security_measures_for_activity",
    "get_security_measures_by_type",
    "delete_security_measure"
]
