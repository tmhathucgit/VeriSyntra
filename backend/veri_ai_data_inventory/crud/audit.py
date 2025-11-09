"""
Audit Trail CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for data_inventory_audit table.
Audit trail tracks all changes for PDPL Article 43 compliance.

Vietnamese-First Architecture:
- audit_message_vi is primary
- Bilingual audit messages for compliance

Usage:
    from crud.audit import create_audit_log
    
    await create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action_type="create",
        entity_type="processing_activity",
        entity_id=activity_id,
        user_id=user_id,
        audit_message_vi="Tạo hoạt động xử lý mới",
        audit_message_en="Created new processing activity"
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from models.db_models import DataInventoryAuditDB


async def create_audit_log(
    db: AsyncSession,
    tenant_id: UUID,
    action_type: str,
    entity_type: str,
    entity_id: UUID,
    user_id: UUID,
    audit_message_vi: str,
    audit_message_en: Optional[str] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> DataInventoryAuditDB:
    """
    Create audit log entry
    
    Args:
        db: Database session
        tenant_id: Tenant UUID
        action_type: Action (create, update, delete, generate_ropa, etc.)
        entity_type: Entity type (processing_activity, data_category, etc.)
        entity_id: Entity UUID
        user_id: User UUID who performed action
        audit_message_vi: Audit message in Vietnamese (REQUIRED)
        audit_message_en: Audit message in English (optional)
        old_values: Old values before update (for update actions)
        new_values: New values after update (for update actions)
        ip_address: User IP address
        user_agent: User agent string
    
    Returns:
        DataInventoryAuditDB: Created audit log
    """
    if not audit_message_vi or not audit_message_vi.strip():
        raise ValueError("audit_message_vi is required (Vietnamese-first architecture)")
    
    audit = DataInventoryAuditDB(
        tenant_id=tenant_id,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        audit_message_vi=audit_message_vi.strip(),
        audit_message_en=audit_message_en.strip() if audit_message_en else None,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(audit)
    await db.flush()
    await db.refresh(audit)
    
    return audit


async def get_audit_logs_for_tenant(
    db: AsyncSession,
    tenant_id: UUID,
    action_type: Optional[str] = None,
    entity_type: Optional[str] = None,
    user_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> List[DataInventoryAuditDB]:
    """
    Get audit logs for tenant with filters
    
    Args:
        db: Database session
        tenant_id: Tenant UUID
        action_type: Filter by action type
        entity_type: Filter by entity type
        user_id: Filter by user
        start_date: Filter by start date
        end_date: Filter by end date
        skip: Pagination offset
        limit: Pagination limit
    
    Returns:
        List of DataInventoryAuditDB
    """
    query = select(DataInventoryAuditDB).where(
        DataInventoryAuditDB.tenant_id == tenant_id
    )
    
    # Apply filters
    if action_type:
        query = query.where(DataInventoryAuditDB.action_type == action_type)
    if entity_type:
        query = query.where(DataInventoryAuditDB.entity_type == entity_type)
    if user_id:
        query = query.where(DataInventoryAuditDB.user_id == user_id)
    if start_date:
        query = query.where(DataInventoryAuditDB.timestamp >= start_date)
    if end_date:
        query = query.where(DataInventoryAuditDB.timestamp <= end_date)
    
    # Order by timestamp descending (newest first)
    query = query.order_by(DataInventoryAuditDB.timestamp.desc())
    
    # Pagination
    query = query.offset(skip).limit(min(limit, 1000))
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_audit_logs_for_entity(
    db: AsyncSession,
    entity_type: str,
    entity_id: UUID,
    tenant_id: UUID
) -> List[DataInventoryAuditDB]:
    """
    Get all audit logs for a specific entity
    
    Args:
        db: Database session
        entity_type: Entity type (processing_activity, etc.)
        entity_id: Entity UUID
        tenant_id: Tenant UUID
    
    Returns:
        List of DataInventoryAuditDB for the entity
    """
    result = await db.execute(
        select(DataInventoryAuditDB).where(
            DataInventoryAuditDB.entity_type == entity_type,
            DataInventoryAuditDB.entity_id == entity_id,
            DataInventoryAuditDB.tenant_id == tenant_id
        ).order_by(DataInventoryAuditDB.timestamp.desc())
    )
    return result.scalars().all()


async def get_recent_audit_logs(
    db: AsyncSession,
    tenant_id: UUID,
    limit: int = 50
) -> List[DataInventoryAuditDB]:
    """
    Get recent audit logs for tenant
    
    Args:
        db: Database session
        tenant_id: Tenant UUID
        limit: Number of recent logs (default 50)
    
    Returns:
        List of recent DataInventoryAuditDB
    """
    result = await db.execute(
        select(DataInventoryAuditDB).where(
            DataInventoryAuditDB.tenant_id == tenant_id
        ).order_by(
            DataInventoryAuditDB.timestamp.desc()
        ).limit(min(limit, 100))
    )
    return result.scalars().all()


__all__ = [
    "create_audit_log",
    "get_audit_logs_for_tenant",
    "get_audit_logs_for_entity",
    "get_recent_audit_logs"
]
