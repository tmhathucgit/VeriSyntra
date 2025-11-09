"""
Processing Location CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for processing_locations table.
Processing locations represent where data is processed (Article 12.1.j).

Vietnamese-First Architecture:
- Supports Vietnamese regional context (North/Central/South)
- Cloud and on-premise locations

Usage:
    from crud.processing_location import create_processing_location
    
    location = await create_processing_location(
        db=db,
        activity_id=activity_id,
        tenant_id=tenant_id,
        location_type="cloud",
        data_center_region="south",
        cloud_provider="Viettel IDC"
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from models.db_models import ProcessingLocationDB


async def create_processing_location(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    location_type: Optional[str] = None,
    facility_name: Optional[str] = None,
    city: Optional[str] = None,
    province: Optional[str] = None,
    country_code: str = "VN",
    data_center_region: Optional[str] = None,
    cloud_provider: Optional[str] = None,
    cloud_region: Optional[str] = None
) -> ProcessingLocationDB:
    """Create new processing location"""
    location = ProcessingLocationDB(
        activity_id=activity_id,
        tenant_id=tenant_id,
        location_type=location_type,
        facility_name=facility_name,
        city=city,
        province=province,
        country_code=country_code,
        data_center_region=data_center_region,
        cloud_provider=cloud_provider,
        cloud_region=cloud_region
    )
    
    db.add(location)
    await db.flush()
    await db.refresh(location)
    
    return location


async def get_processing_locations_for_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> List[ProcessingLocationDB]:
    """Get all processing locations for an activity"""
    result = await db.execute(
        select(ProcessingLocationDB).where(
            ProcessingLocationDB.activity_id == activity_id,
            ProcessingLocationDB.tenant_id == tenant_id
        )
    )
    return result.scalars().all()


async def get_processing_locations_by_region(
    db: AsyncSession,
    tenant_id: UUID,
    data_center_region: str
) -> List[ProcessingLocationDB]:
    """Get all processing locations in a Vietnamese region"""
    result = await db.execute(
        select(ProcessingLocationDB).where(
            ProcessingLocationDB.tenant_id == tenant_id,
            ProcessingLocationDB.data_center_region == data_center_region
        )
    )
    return result.scalars().all()


async def delete_processing_location(
    db: AsyncSession,
    location_id: UUID,
    tenant_id: UUID
) -> bool:
    """Delete processing location"""
    result = await db.execute(
        select(ProcessingLocationDB).where(
            ProcessingLocationDB.location_id == location_id,
            ProcessingLocationDB.tenant_id == tenant_id
        )
    )
    location = result.scalar_one_or_none()
    
    if not location:
        return False
    
    await db.delete(location)
    await db.flush()
    return True


__all__ = [
    "create_processing_location",
    "get_processing_locations_for_activity",
    "get_processing_locations_by_region",
    "delete_processing_location"
]
