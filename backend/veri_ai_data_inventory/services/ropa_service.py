"""
ROPA Service Layer - Business Logic for ROPA Generation
Vietnamese PDPL 2025 Compliance - Document #3 Section 7

This service implements the core business logic for ROPA document management:
- Generation using format-specific exporters (zero hard-coding)
- File storage and retrieval
- Metadata management
- Cleanup operations

Document #3 Section 7: API Endpoints - Service Layer
"""

import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID, uuid4
from datetime import datetime, timezone
import pytz
from sqlalchemy.ext.asyncio import AsyncSession

from models.ropa_models import (
    ROPADocument,
    ROPALanguage,
    ROPAOutputFormat
)
from models.api_models import (
    ROPAMetadata,
    ROPAPreviewResponse
)
from exporters.json_exporter import JSONExporter
from exporters.csv_exporter import CSVExporter
from exporters.pdf_generator import ROPAPDFGenerator
from exporters.mps_format import MPSFormatExporter

# Database CRUD imports - Phase 4 Integration
from crud.processing_activity import (
    get_processing_activities_for_tenant,
    build_ropa_entry_from_activity
)
from crud.ropa_document import create_ropa_document_record
from crud.audit import create_audit_log

# Named constants - Phase 4 Integration
from services.constants import (
    SYSTEM_USER_ID,
    AVG_KB_PER_ACTIVITY,
    MIN_ESTIMATED_FILE_SIZE_KB,
    AUDIT_ACTION_ROPA_GENERATED,
    AUDIT_ENTITY_ROPA_DOCUMENT,
    VIETNAM_TIMEZONE
)


class ROPAService:
    """
    ROPA Service - ZERO HARD-CODING ARCHITECTURE
    
    Uses dictionary routing for format selection instead of if/else chains.
    All Vietnamese timezone handling through pytz.
    """
    
    # Storage configuration - can be overridden in production
    DEFAULT_STORAGE_DIR = Path("./ropa_storage")
    
    # Dictionary routing for exporters - ZERO HARD-CODING
    EXPORTER_MAP = {
        ROPAOutputFormat.JSON: JSONExporter,
        ROPAOutputFormat.CSV: CSVExporter,
        ROPAOutputFormat.PDF: ROPAPDFGenerator,
        ROPAOutputFormat.MPS_FORMAT: MPSFormatExporter
    }
    
    # File extensions mapping
    FILE_EXTENSION_MAP = {
        ROPAOutputFormat.JSON: '.json',
        ROPAOutputFormat.CSV: '.csv',
        ROPAOutputFormat.PDF: '.pdf',
        ROPAOutputFormat.MPS_FORMAT: '.mps.json'
    }
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize ROPA Service
        
        Args:
            storage_dir: Custom storage directory (default: ./ropa_storage)
        """
        self.storage_dir = storage_dir or self.DEFAULT_STORAGE_DIR
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self) -> None:
        """Create storage directory if it doesn't exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_vietnam_time(self) -> datetime:
        """Get current time in Vietnamese timezone (Asia/Ho_Chi_Minh)"""
        vietnam_tz = pytz.timezone(VIETNAM_TIMEZONE)
        return datetime.now(vietnam_tz)
    
    def _get_tenant_dir(self, tenant_id: UUID) -> Path:
        """Get tenant-specific storage directory"""
        tenant_dir = self.storage_dir / str(tenant_id)
        tenant_dir.mkdir(parents=True, exist_ok=True)
        return tenant_dir
    
    def _get_file_path(
        self,
        tenant_id: UUID,
        ropa_id: UUID,
        format: ROPAOutputFormat
    ) -> Path:
        """
        Get file path for ROPA document - ZERO HARD-CODING
        
        Uses dictionary routing for file extensions.
        """
        tenant_dir = self._get_tenant_dir(tenant_id)
        extension = self.FILE_EXTENSION_MAP[format]
        return tenant_dir / f"{ropa_id}{extension}"
    
    def _get_metadata_path(self, tenant_id: UUID, ropa_id: UUID) -> Path:
        """Get metadata file path"""
        tenant_dir = self._get_tenant_dir(tenant_id)
        return tenant_dir / f"{ropa_id}.metadata.json"
    
    async def generate_ropa_from_database(
        self,
        db: AsyncSession,
        tenant_id: UUID,
        format: ROPAOutputFormat,
        language: ROPALanguage = ROPALanguage.VIETNAMESE,
        user_id: Optional[UUID] = None,
        veri_business_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate ROPA from database - DATABASE-FIRST IMPLEMENTATION
        
        Phase 4: Replaces mock implementation with real database queries.
        Follows zero hard-coding architecture with EXPORTER_MAP routing.
        
        Args:
            db: Async database session
            tenant_id: Tenant UUID for multi-tenant isolation
            format: Output format (JSON/CSV/PDF/MPS_FORMAT)
            language: Output language (Vietnamese-first)
            user_id: User generating ROPA (defaults to SYSTEM_USER_ID)
            veri_business_context: Vietnamese business context metadata
        
        Returns:
            Dictionary with ropa_id, download_url, file_size, metadata
        
        Implementation Steps:
        1. Query processing activities from database
        2. Build ROPA entries with related data (categories, subjects, etc.)
        3. Create ROPADocument with all entries
        4. Export using EXPORTER_MAP dictionary routing
        5. Save file metadata
        6. Save ROPA document record to database
        7. Create audit log entry
        8. Return response
        """
        # Step 1: Query all active processing activities for tenant
        activities = await get_processing_activities_for_tenant(
            db=db,
            tenant_id=tenant_id,
            status="active",
            include_deleted=False
        )
        
        if not activities:
            # Return empty ROPA if no activities found
            return {
                "ropa_id": None,
                "message": "No processing activities found",
                "message_vi": "Không tìm thấy hoạt động xử lý",
                "entry_count": 0
            }
        
        # Step 2: Build ROPA entries with all related data
        entries = []
        for activity in activities:
            entry = await build_ropa_entry_from_activity(db=db, activity=activity)
            entries.append(entry)
        
        # Step 3: Create ROPADocument with aggregated metadata
        ropa_id = uuid4()
        document = ROPADocument(
            document_id=ropa_id,
            tenant_id=tenant_id,
            generated_date=self._get_vietnam_time(),
            generated_by=user_id or SYSTEM_USER_ID,
            entries=entries,
            total_processing_activities=len(entries),
            has_sensitive_data=self._has_sensitive_data_from_entries(entries),
            has_cross_border_transfers=self._has_cross_border_from_entries(entries),
            veri_business_context=veri_business_context or {},
            compliance_checklist=self._build_compliance_checklist(entries)
        )
        
        # Step 4: Export using EXPORTER_MAP dictionary routing (zero hard-coding)
        exporter_class = self.EXPORTER_MAP.get(format)
        if not exporter_class:
            raise ValueError(f"Unsupported format: {format}")
        
        file_path = self._get_file_path(tenant_id, ropa_id, format)
        exporter_class.export(document, str(file_path), language)
        
        # Get actual file size
        file_size = file_path.stat().st_size
        
        # Step 5: Save file metadata (for backward compatibility)
        metadata_dict = {
            'ropa_id': str(ropa_id),
            'tenant_id': str(tenant_id),
            'format': format.value,
            'language': language.value,
            'generated_at': self._get_vietnam_time().isoformat(),
            'file_size_bytes': file_size,
            'entry_count': len(entries),
            'mps_compliant': self._check_mps_compliance_from_entries(entries),
            'has_sensitive_data': document.has_sensitive_data,
            'has_cross_border_transfers': document.has_cross_border_transfers
        }
        
        metadata_path = self._get_metadata_path(tenant_id, ropa_id)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_dict, f, indent=2, ensure_ascii=False)
        
        # Step 6: Save ROPA document record to database
        db_record = await create_ropa_document_record(
            db=db,
            tenant_id=tenant_id,
            ropa_id=ropa_id,
            format_type=format.value,
            language=language.value,
            file_size_bytes=file_size,
            file_path=str(file_path),
            entry_count=len(entries),
            generated_by=user_id or SYSTEM_USER_ID,
            mps_submitted=False,
            metadata=metadata_dict
        )
        
        # Step 7: Create audit log entry
        await create_audit_log(
            db=db,
            tenant_id=tenant_id,
            entity_type=AUDIT_ENTITY_ROPA_DOCUMENT,
            entity_id=ropa_id,
            action=AUDIT_ACTION_ROPA_GENERATED,
            user_id=user_id or SYSTEM_USER_ID,
            changes={
                "format": format.value,
                "language": language.value,
                "entry_count": len(entries)
            },
            message=f"ROPA document generated with {len(entries)} entries",
            message_vi=f"Tạo tài liệu ROPA với {len(entries)} hoạt động xử lý"
        )
        
        # Commit all database changes
        await db.commit()
        
        # Step 8: Return response
        download_url = f"/api/v1/data-inventory/{tenant_id}/ropa/{ropa_id}/download"
        
        return {
            "ropa_id": str(ropa_id),
            "download_url": download_url,
            "file_size_bytes": file_size,
            "entry_count": len(entries),
            "format": format.value,
            "language": language.value,
            "generated_at": metadata_dict['generated_at'],
            "mps_compliant": metadata_dict['mps_compliant'],
            "has_sensitive_data": document.has_sensitive_data,
            "has_cross_border_transfers": document.has_cross_border_transfers
        }
    
    async def preview_ropa_from_database(
        self,
        db: AsyncSession,
        tenant_id: UUID
    ) -> Dict[str, Any]:
        """
        Preview ROPA from database - DATABASE-FIRST IMPLEMENTATION
        
        Phase 4: Calculates preview from actual database activities.
        
        Args:
            db: Async database session
            tenant_id: Tenant UUID
        
        Returns:
            Dictionary with preview metadata
        """
        # Query activities
        activities = await get_processing_activities_for_tenant(
            db=db,
            tenant_id=tenant_id,
            status="active",
            include_deleted=False
        )
        
        if not activities:
            return {
                "entry_count": 0,
                "data_categories": [],
                "has_sensitive_data": False,
                "has_cross_border_transfers": False,
                "compliance_checklist": {},
                "estimated_file_size_kb": MIN_ESTIMATED_FILE_SIZE_KB,
                "message": "No processing activities found",
                "message_vi": "Không tìm thấy hoạt động xử lý"
            }
        
        # Build entries for analysis
        entries = []
        for activity in activities:
            entry = await build_ropa_entry_from_activity(db=db, activity=activity)
            entries.append(entry)
        
        # Extract unique data categories
        data_categories = set()
        for entry in entries:
            if hasattr(entry, 'data_categories') and entry.data_categories:
                data_categories.update(entry.data_categories)
        
        # Build compliance checklist
        compliance_checklist = self._build_compliance_checklist(entries)
        
        # Estimate file size
        estimated_size_kb = max(
            MIN_ESTIMATED_FILE_SIZE_KB,
            len(entries) * AVG_KB_PER_ACTIVITY
        )
        
        return {
            "entry_count": len(entries),
            "data_categories": sorted(data_categories),
            "has_sensitive_data": self._has_sensitive_data_from_entries(entries),
            "has_cross_border_transfers": self._has_cross_border_from_entries(entries),
            "compliance_checklist": compliance_checklist,
            "estimated_file_size_kb": estimated_size_kb
        }
    
    def generate_ropa(
        self,
        tenant_id: UUID,
        document: ROPADocument,
        format: ROPAOutputFormat,
        language: ROPALanguage
    ) -> Tuple[UUID, Path, int]:
        """
        Generate ROPA document using appropriate exporter - ZERO HARD-CODING
        
        Uses dictionary routing to select exporter instead of if/else chains.
        
        Args:
            tenant_id: Tenant UUID
            document: ROPA document data
            format: Output format (from enum)
            language: Output language (from enum)
        
        Returns:
            Tuple of (ropa_id, file_path, file_size_bytes)
        
        Raises:
            ValueError: If format is not supported
        """
        # Generate unique ROPA ID
        ropa_id = uuid4()
        
        # Get exporter using dictionary routing - ZERO HARD-CODING
        exporter_class = self.EXPORTER_MAP.get(format)
        if not exporter_class:
            raise ValueError(f"Unsupported format: {format}")
        
        # Generate file path
        file_path = self._get_file_path(tenant_id, ropa_id, format)
        
        # Export using selected exporter
        exporter_class.export(document, str(file_path), language)
        
        # Get file size
        file_size = file_path.stat().st_size
        
        # Save metadata
        metadata = {
            'ropa_id': str(ropa_id),
            'tenant_id': str(tenant_id),
            'format': format.value,
            'language': language.value,
            'generated_at': self._get_vietnam_time().isoformat(),
            'file_size_bytes': file_size,
            'entry_count': len(document.entries),
            'mps_compliant': self._check_mps_compliance(document),
            'has_sensitive_data': self._has_sensitive_data(document),
            'has_cross_border_transfers': self._has_cross_border_transfers(document)
        }
        
        metadata_path = self._get_metadata_path(tenant_id, ropa_id)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return ropa_id, file_path, file_size
    
    def get_ropa_file(
        self,
        tenant_id: UUID,
        ropa_id: UUID,
        format: ROPAOutputFormat
    ) -> Optional[Path]:
        """
        Retrieve ROPA document file path
        
        Returns:
            Path to file if exists, None otherwise
        """
        file_path = self._get_file_path(tenant_id, ropa_id, format)
        return file_path if file_path.exists() else None
    
    def get_ropa_metadata(
        self,
        tenant_id: UUID,
        ropa_id: UUID
    ) -> Optional[ROPAMetadata]:
        """
        Retrieve ROPA metadata
        
        Returns:
            ROPAMetadata if exists, None otherwise
        """
        metadata_path = self._get_metadata_path(tenant_id, ropa_id)
        if not metadata_path.exists():
            return None
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Construct download URL
        download_url = f"/api/v1/data-inventory/{tenant_id}/ropa/{ropa_id}/download"
        
        return ROPAMetadata(
            ropa_id=UUID(data['ropa_id']),
            tenant_id=UUID(data['tenant_id']),
            format=ROPAOutputFormat(data['format']),
            language=ROPALanguage(data['language']),
            generated_at=datetime.fromisoformat(data['generated_at']),
            file_size_bytes=data['file_size_bytes'],
            download_url=download_url,
            entry_count=data['entry_count'],
            mps_compliant=data['mps_compliant'],
            has_sensitive_data=data['has_sensitive_data'],
            has_cross_border_transfers=data['has_cross_border_transfers']
        )
    
    def list_ropa_documents(
        self,
        tenant_id: UUID,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[ROPAMetadata], int]:
        """
        List ROPA documents for tenant with pagination
        
        Args:
            tenant_id: Tenant UUID
            page: Page number (1-indexed)
            page_size: Number of items per page
        
        Returns:
            Tuple of (metadata_list, total_count)
        """
        tenant_dir = self._get_tenant_dir(tenant_id)
        
        # Find all metadata files
        metadata_files = list(tenant_dir.glob("*.metadata.json"))
        total_count = len(metadata_files)
        
        # Calculate pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Load metadata for current page
        metadata_list = []
        for metadata_file in metadata_files[start_idx:end_idx]:
            ropa_id = UUID(metadata_file.stem.replace('.metadata', ''))
            metadata = self.get_ropa_metadata(tenant_id, ropa_id)
            if metadata:
                metadata_list.append(metadata)
        
        # Sort by generation time (newest first)
        metadata_list.sort(key=lambda m: m.generated_at, reverse=True)
        
        return metadata_list, total_count
    
    def delete_ropa(self, tenant_id: UUID, ropa_id: UUID) -> bool:
        """
        Delete ROPA document and metadata
        
        Returns:
            True if deleted, False if not found
        """
        deleted = False
        
        # Delete all format variations
        for format in ROPAOutputFormat:
            file_path = self._get_file_path(tenant_id, ropa_id, format)
            if file_path.exists():
                file_path.unlink()
                deleted = True
        
        # Delete metadata
        metadata_path = self._get_metadata_path(tenant_id, ropa_id)
        if metadata_path.exists():
            metadata_path.unlink()
            deleted = True
        
        return deleted
    
    def preview_ropa(self, document: ROPADocument) -> ROPAPreviewResponse:
        """
        Generate preview information without creating full document
        
        Args:
            document: ROPA document data
        
        Returns:
            ROPAPreviewResponse with metadata
        """
        # Extract unique data categories
        data_categories = set()
        for entry in document.entries:
            data_categories.update(entry.data_categories)
        
        # Check compliance requirements
        compliance_checklist = {
            'has_controller_info': bool(document.controller.name),
            'has_dpo': bool(document.dpo and document.dpo.name),
            'has_legal_basis': all(entry.legal_basis for entry in document.entries),
            'has_retention_period': all(entry.retention_period for entry in document.entries),
            'has_security_measures': all(entry.security_measures for entry in document.entries)
        }
        
        # Estimate file size (rough approximation)
        estimated_size_kb = max(MIN_ESTIMATED_FILE_SIZE_KB, len(document.entries) * AVG_KB_PER_ACTIVITY)
        
        return ROPAPreviewResponse(
            entry_count=len(document.entries),
            data_categories=sorted(data_categories),
            has_sensitive_data=self._has_sensitive_data(document),
            has_cross_border_transfers=self._has_cross_border_transfers(document),
            compliance_checklist=compliance_checklist,
            estimated_file_size_kb=estimated_size_kb
        )
    
    def _build_compliance_checklist(self, entries: List[Any]) -> Dict[str, bool]:
        """
        Build compliance checklist from ROPA entries
        
        Args:
            entries: List of ROPA entries
        
        Returns:
            Dictionary with compliance checks
        """
        if not entries:
            return {
                'has_legal_basis': False,
                'has_retention_period': False,
                'has_security_measures': False,
                'has_data_categories': False,
                'has_data_subjects': False
            }
        
        return {
            'has_legal_basis': all(
                hasattr(e, 'legal_basis') and e.legal_basis for e in entries
            ),
            'has_retention_period': all(
                hasattr(e, 'retention_period') and e.retention_period for e in entries
            ),
            'has_security_measures': all(
                hasattr(e, 'security_measures') and e.security_measures for e in entries
            ),
            'has_data_categories': all(
                hasattr(e, 'data_categories') and e.data_categories for e in entries
            ),
            'has_data_subjects': all(
                hasattr(e, 'data_subjects') and e.data_subjects for e in entries
            )
        }
    
    def _has_sensitive_data_from_entries(self, entries: List[Any]) -> bool:
        """
        Check if entries contain sensitive data categories
        
        Args:
            entries: List of ROPA entries
        
        Returns:
            True if sensitive data found
        """
        sensitive_keywords = [
            'sensitive', 'health', 'medical', 'biometric', 'genetic',
            'nhạy cảm', 'sức khỏe', 'y tế', 'sinh trắc học', 'di truyền'
        ]
        
        for entry in entries:
            if hasattr(entry, 'data_categories') and entry.data_categories:
                for category in entry.data_categories:
                    if any(keyword in str(category).lower() for keyword in sensitive_keywords):
                        return True
        
        return False
    
    def _has_cross_border_from_entries(self, entries: List[Any]) -> bool:
        """
        Check if entries have cross-border transfers
        
        Args:
            entries: List of ROPA entries
        
        Returns:
            True if cross-border transfers found
        """
        for entry in entries:
            if hasattr(entry, 'cross_border_transfer') and entry.cross_border_transfer:
                if hasattr(entry.cross_border_transfer, 'is_cross_border'):
                    if entry.cross_border_transfer.is_cross_border:
                        return True
        
        return False
    
    def _check_mps_compliance_from_entries(self, entries: List[Any]) -> bool:
        """
        Check if entries meet MPS (Bộ Công an) compliance requirements
        
        Vietnamese PDPL 2025 requires:
        - Legal basis for all processing
        - Security measures for all activities
        - Retention periods defined
        
        Args:
            entries: List of ROPA entries
        
        Returns:
            True if compliant
        """
        if not entries:
            return False
        
        has_legal_basis = all(
            hasattr(e, 'legal_basis') and e.legal_basis for e in entries
        )
        has_security = all(
            hasattr(e, 'security_measures') and e.security_measures for e in entries
        )
        has_retention = all(
            hasattr(e, 'retention_period') and e.retention_period for e in entries
        )
        
        return has_legal_basis and has_security and has_retention
    
    def _check_mps_compliance(self, document: ROPADocument) -> bool:
        """
        Check if document meets MPS (Bộ Công an) compliance requirements
        
        Vietnamese PDPL 2025 requires:
        - Controller information
        - DPO information
        - Legal basis for all processing
        - Security measures
        """
        has_controller = bool(document.controller.name)
        has_dpo = bool(document.dpo and document.dpo.name)
        has_legal_basis = all(entry.legal_basis for entry in document.entries)
        has_security = all(entry.security_measures for entry in document.entries)
        
        return has_controller and has_dpo and has_legal_basis and has_security
    
    def _has_sensitive_data(self, document: ROPADocument) -> bool:
        """Check if document contains sensitive data categories"""
        sensitive_keywords = [
            'sensitive', 'health', 'medical', 'biometric', 'genetic',
            'nhạy cảm', 'sức khỏe', 'y tế', 'sinh trắc học', 'di truyền'
        ]
        
        for entry in document.entries:
            for category in entry.data_categories:
                if any(keyword in category.lower() for keyword in sensitive_keywords):
                    return True
        
        return False
    
    def _has_cross_border_transfers(self, document: ROPADocument) -> bool:
        """Check if document has cross-border transfers"""
        return any(
            entry.cross_border_transfer and entry.cross_border_transfer.is_cross_border
            for entry in document.entries
        )


# Export service class
__all__ = ['ROPAService']
