"""
Data Category CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for data_categories table.
Data categories represent types of personal data processed (Article 12.1.d).

Vietnamese-First Architecture:
- category_name_vi is required (NOT NULL)
- data_fields_vi is primary (TEXT[] array)
- English fields are optional fallbacks

Usage:
    from crud.data_category import create_data_category
    
    category = await create_data_category(
        db=db,
        activity_id=activity_id,
        tenant_id=tenant_id,
        category_name_vi="Thông tin cá nhân",
        category_type="personal_identifiers",
        data_fields_vi=["họ tên", "địa chỉ", "số điện thoại"]
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from uuid import UUID

from models.db_models import DataCategoryDB


async def create_data_category(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID,
    category_name_vi: str,
    category_type: str,
    data_fields_vi: List[str],
    category_name_en: Optional[str] = None,
    data_fields_en: Optional[List[str]] = None,
    is_sensitive: bool = False,
    sensitivity_reason: Optional[str] = None,
    total_fields_discovered: Optional[int] = None,
    fields_included: Optional[int] = None,
    filter_scope_statement_vi: Optional[str] = None,
    filter_scope_statement_en: Optional[str] = None
) -> DataCategoryDB:
    """Create new data category"""
    if not category_name_vi or not category_name_vi.strip():
        raise ValueError("category_name_vi is required (Vietnamese-first architecture)")
    
    category = DataCategoryDB(
        activity_id=activity_id,
        tenant_id=tenant_id,
        category_name_vi=category_name_vi.strip(),
        category_name_en=category_name_en.strip() if category_name_en else None,
        category_type=category_type,
        data_fields_vi=data_fields_vi or [],
        data_fields_en=data_fields_en or [],
        is_sensitive=is_sensitive,
        sensitivity_reason=sensitivity_reason,
        total_fields_discovered=total_fields_discovered,
        fields_included=fields_included,
        filter_scope_statement_vi=filter_scope_statement_vi,
        filter_scope_statement_en=filter_scope_statement_en
    )
    
    db.add(category)
    await db.flush()
    await db.refresh(category)
    
    return category


async def get_data_categories_for_activity(
    db: AsyncSession,
    activity_id: UUID,
    tenant_id: UUID
) -> List[DataCategoryDB]:
    """Get all data categories for an activity"""
    result = await db.execute(
        select(DataCategoryDB).where(
            DataCategoryDB.activity_id == activity_id,
            DataCategoryDB.tenant_id == tenant_id
        )
    )
    return result.scalars().all()


async def get_sensitive_data_categories(
    db: AsyncSession,
    tenant_id: UUID
) -> List[DataCategoryDB]:
    """Get all sensitive data categories for tenant"""
    result = await db.execute(
        select(DataCategoryDB).where(
            DataCategoryDB.tenant_id == tenant_id,
            DataCategoryDB.is_sensitive == True
        )
    )
    return result.scalars().all()


async def delete_data_category(
    db: AsyncSession,
    category_id: UUID,
    tenant_id: UUID
) -> bool:
    """Delete data category"""
    result = await db.execute(
        select(DataCategoryDB).where(
            DataCategoryDB.category_id == category_id,
            DataCategoryDB.tenant_id == tenant_id
        )
    )
    category = result.scalar_one_or_none()
    
    if not category:
        return False
    
    await db.delete(category)
    await db.flush()
    return True


__all__ = [
    "create_data_category",
    "get_data_categories_for_activity",
    "get_sensitive_data_categories",
    "delete_data_category"
]
