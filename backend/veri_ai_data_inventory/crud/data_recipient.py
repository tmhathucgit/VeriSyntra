"""
Data Recipient CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for data_recipients table.
Recipients represent entities receiving personal data (Articles 12.1.f, 12.1.g).

Vietnamese-First Architecture:
- recipient_name_vi is required (NOT NULL)
- safeguards_vi is primary (TEXT[] array)
- Cross-border transfer tracking per Article 20

Usage:
    from crud.data_recipient import create_data_recipient
    
    recipient = await create_data_recipient(
        db=db,
        activity_id=activity_id,
        tenant_id=tenant_id,
        recipient_name_vi="Công ty ABC",
        recipient_type="processor",
        country_code="VN"
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from models.db_models import DataRecipientDB


async def create_data_recipient(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    recipient_name_vi: str,
    recipient_type: str,
    country_code: str = "VN",
    recipient_name_en: Optional[str] = None,
    recipient_type_vi: Optional[str] = None,
    country_name_vi: Optional[str] = None,
    country_name_en: Optional[str] = None,
    is_cross_border: bool = False,
    transfer_mechanism: Optional[str] = None,
    transfer_mechanism_vi: Optional[str] = None,
    safeguards_vi: Optional[List[str]] = None,
    safeguards_en: Optional[List[str]] = None
) -> DataRecipientDB:
    """Create new data recipient"""
    if not recipient_name_vi or not recipient_name_vi.strip():
        raise ValueError("recipient_name_vi is required (Vietnamese-first architecture)")
    
    # Auto-detect cross-border if country is not Vietnam
    if country_code != "VN":
        is_cross_border = True
    
    recipient = DataRecipientDB(
        activity_id=activity_id,
        tenant_id=tenant_id,
        recipient_name_vi=recipient_name_vi.strip(),
        recipient_name_en=recipient_name_en.strip() if recipient_name_en else None,
        recipient_type=recipient_type,
        recipient_type_vi=recipient_type_vi,
        country_code=country_code,
        country_name_vi=country_name_vi,
        country_name_en=country_name_en,
        is_cross_border=is_cross_border,
        transfer_mechanism=transfer_mechanism,
        transfer_mechanism_vi=transfer_mechanism_vi,
        safeguards_vi=safeguards_vi or [],
        safeguards_en=safeguards_en or []
    )
    
    db.add(recipient)
    await db.flush()
    await db.refresh(recipient)
    
    return recipient


async def get_data_recipients_for_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> List[DataRecipientDB]:
    """Get all data recipients for an activity"""
    result = await db.execute(
        select(DataRecipientDB).where(
            DataRecipientDB.activity_id == activity_id,
            DataRecipientDB.tenant_id == tenant_id
        )
    )
    return result.scalars().all()


async def get_cross_border_transfers(
    db: AsyncSession,
    tenant_id: UUID
) -> List[DataRecipientDB]:
    """Get all cross-border data transfers for tenant"""
    result = await db.execute(
        select(DataRecipientDB).where(
            DataRecipientDB.tenant_id == tenant_id,
            DataRecipientDB.is_cross_border == True
        )
    )
    return result.scalars().all()


async def delete_data_recipient(
    db: AsyncSession,
    recipient_id: UUID,
    tenant_id: UUID
) -> bool:
    """Delete data recipient"""
    result = await db.execute(
        select(DataRecipientDB).where(
            DataRecipientDB.recipient_id == recipient_id,
            DataRecipientDB.tenant_id == tenant_id
        )
    )
    recipient = result.scalar_one_or_none()
    
    if not recipient:
        return False
    
    await db.delete(recipient)
    await db.flush()
    return True


__all__ = [
    "create_data_recipient",
    "get_data_recipients_for_activity",
    "get_cross_border_transfers",
    "delete_data_recipient"
]
