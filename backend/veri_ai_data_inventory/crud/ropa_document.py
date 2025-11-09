"""
ROPA Document CRUD Operations
Vietnamese PDPL 2025 Compliance

Provides async CRUD operations for ropa_documents table.
ROPA documents track generated ROPA exports with MPS submission tracking.

Vietnamese-First Architecture:
- Bilingual support via language field
- Vietnamese business context in JSONB

Usage:
    from crud.ropa_document import create_ropa_document_record
    
    doc = await create_ropa_document_record(
        db=db,
        tenant_id=tenant_id,
        document_format="pdf",
        language="vi",
        file_path="/exports/ropa_2025.pdf",
        generated_by=user_id
    )
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from models.db_models import ROPADocumentDB


async def create_ropa_document_record(
    db: AsyncSession,
    tenant_id: UUID,
    document_format: str,
    language: str,
    generated_by: UUID,
    file_path: Optional[str] = None,
    file_size_bytes: Optional[int] = None,
    generation_parameters: Optional[Dict[str, Any]] = None,
    entry_count: int = 0,
    has_sensitive_data: bool = False,
    has_cross_border_transfers: bool = False,
    mps_compliant: bool = False,
    veri_business_context: Optional[Dict[str, Any]] = None
) -> ROPADocumentDB:
    """Create new ROPA document record"""
    doc = ROPADocumentDB(
        tenant_id=tenant_id,
        document_format=document_format,
        language=language,
        generated_by=generated_by,
        file_path=file_path,
        file_size_bytes=file_size_bytes,
        generation_parameters=generation_parameters or {},
        entry_count=entry_count,
        has_sensitive_data=has_sensitive_data,
        has_cross_border_transfers=has_cross_border_transfers,
        mps_compliant=mps_compliant,
        veri_business_context=veri_business_context or {}
    )
    
    db.add(doc)
    await db.flush()
    await db.refresh(doc)
    
    return doc


async def get_ropa_document_by_id(
    db: AsyncSession,
    ropa_id: UUID,
    tenant_id: UUID
) -> Optional[ROPADocumentDB]:
    """Get ROPA document by ID"""
    result = await db.execute(
        select(ROPADocumentDB).where(
            ROPADocumentDB.ropa_id == ropa_id,
            ROPADocumentDB.tenant_id == tenant_id
        )
    )
    return result.scalar_one_or_none()


async def list_ropa_documents(
    db: AsyncSession,
    tenant_id: UUID,
    status: Optional[str] = None,
    document_format: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
) -> List[ROPADocumentDB]:
    """List ROPA documents with pagination"""
    query = select(ROPADocumentDB).where(
        ROPADocumentDB.tenant_id == tenant_id
    )
    
    if status:
        query = query.where(ROPADocumentDB.status == status)
    if document_format:
        query = query.where(ROPADocumentDB.document_format == document_format)
    
    query = query.order_by(ROPADocumentDB.generated_at.desc())
    query = query.offset(skip).limit(min(limit, 100))
    
    result = await db.execute(query)
    return result.scalars().all()


async def update_ropa_document_status(
    db: AsyncSession,
    ropa_id: UUID,
    tenant_id: UUID,
    status: str,
    approved_by: Optional[UUID] = None
) -> Optional[ROPADocumentDB]:
    """Update ROPA document status"""
    doc = await get_ropa_document_by_id(db, ropa_id, tenant_id)
    if not doc:
        return None
    
    doc.status = status
    if status == "approved":
        doc.approved_at = datetime.utcnow()
        doc.approved_by = approved_by
    
    await db.flush()
    await db.refresh(doc)
    
    return doc


async def update_mps_submission(
    db: AsyncSession,
    ropa_id: UUID,
    tenant_id: UUID,
    mps_reference_number: str
) -> Optional[ROPADocumentDB]:
    """Update MPS submission details"""
    doc = await get_ropa_document_by_id(db, ropa_id, tenant_id)
    if not doc:
        return None
    
    doc.mps_submitted = True
    doc.mps_submission_date = datetime.utcnow()
    doc.mps_reference_number = mps_reference_number
    doc.status = "submitted"
    
    await db.flush()
    await db.refresh(doc)
    
    return doc


async def delete_ropa_document_record(
    db: AsyncSession,
    ropa_id: UUID,
    tenant_id: UUID
) -> bool:
    """Delete ROPA document record (not the file)"""
    doc = await get_ropa_document_by_id(db, ropa_id, tenant_id)
    if not doc:
        return False
    
    await db.delete(doc)
    await db.flush()
    return True


__all__ = [
    "create_ropa_document_record",
    "get_ropa_document_by_id",
    "list_ropa_documents",
    "update_ropa_document_status",
    "update_mps_submission",
    "delete_ropa_document_record"
]
