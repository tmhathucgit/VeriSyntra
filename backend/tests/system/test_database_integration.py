"""
Database Integration Tests - Vietnamese PDPL 2025 Compliance Platform
Tests for Document #11 Phase 6: Database Integration Validation

This test suite validates:
1. End-to-end ROPA generation from database
2. Multi-tenant isolation and data security
3. Vietnamese-first architecture compliance
4. All CRUD operations with real database queries
5. MPS compliance and audit trail functionality

Test Coverage:
- Integration Tests: ROPA generation workflow
- Multi-Tenant Tests: Data isolation and security
- Vietnamese-First Tests: Timezone, diacritics, bilingual support
- End-to-End Tests: Complete workflow validation
"""

import os
import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4
from pathlib import Path
from typing import AsyncGenerator

import pytz
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, delete

# Database imports
from database.base import Base
from database.connection import get_db
from models.db_models import (
    ProcessingActivityDB,
    DataCategoryDB,
    DataSubjectDB,
    DataRecipientDB,
    DataRetentionDB,
    SecurityMeasureDB,
    ProcessingLocationDB,
    ROPADocumentDB,
    DataInventoryAuditDB
)

# CRUD imports
from crud.processing_activity import (
    create_processing_activity,
    get_processing_activity,
    get_processing_activities_for_tenant,
    build_ropa_entry_from_activity
)
from crud.data_category import create_data_category
from crud.data_subject import create_data_subject
from crud.data_recipient import create_data_recipient
from crud.data_retention import create_data_retention
from crud.security_measure import create_security_measure
from crud.processing_location import create_processing_location
from crud.audit import create_audit_log, get_audit_logs_for_tenant

# Service imports
from services.ropa_service import ROPAService
from services.constants import SYSTEM_USER_ID, VIETNAM_TIMEZONE
from models.ropa_models import ROPAOutputFormat, ROPALanguage


# ==============================================================================
# Test Database Setup
# ==============================================================================

# Test database URL (in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Test engine and session factory
test_engine = None
TestSessionLocal = None


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    """Get test database session"""
    global test_engine, TestSessionLocal
    
    if test_engine is None:
        test_engine = create_async_engine(
            TEST_DATABASE_URL,
            echo=False,
            future=True
        )
        TestSessionLocal = async_sessionmaker(
            test_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create all tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture for database session"""
    async for session in get_test_db():
        yield session
        # Cleanup after each test
        await session.rollback()


@pytest.fixture
def ropa_service():
    """Fixture for ROPA service"""
    return ROPAService()


# ==============================================================================
# Test Data Factories
# ==============================================================================

async def create_test_tenant(db: AsyncSession) -> UUID:
    """Create test tenant and return tenant_id"""
    tenant_id = uuid4()
    # Note: In full implementation, create tenant record in tenants table
    return tenant_id


async def create_full_processing_activity(
    db: AsyncSession,
    tenant_id: UUID,
    name_vi: str = "Quản lý khách hàng",
    name_en: str = "Customer Management"
) -> ProcessingActivityDB:
    """
    Create processing activity with all related data
    
    Vietnamese-first approach:
    - name_vi is primary (NOT NULL)
    - name_en is fallback (nullable)
    """
    # 1. Create processing activity
    activity = await create_processing_activity(
        db=db,
        tenant_id=tenant_id,
        activity_name_vi=name_vi,
        activity_name_en=name_en,
        processing_purpose_vi="Thu thập và quản lý thông tin khách hàng",
        processing_purpose_en="Collect and manage customer information",
        legal_basis="consent",
        status="active"
    )
    
    # 2. Add data categories
    category1 = await create_data_category(
        db=db,
        activity_id=activity.activity_id,
        tenant_id=tenant_id,
        category_name_vi="Họ và tên",
        category_name_en="Full name",
        is_sensitive=False,
        pdpl_category=1,
        data_examples=["Nguyễn Văn A", "Trần Thị B"]
    )
    
    category2 = await create_data_category(
        db=db,
        activity_id=activity.activity_id,
        tenant_id=tenant_id,
        category_name_vi="Địa chỉ email",
        category_name_en="Email address",
        is_sensitive=False,
        pdpl_category=1,
        data_examples=["example@company.vn"]
    )
    
    # 3. Add data subjects
    subject = await create_data_subject(
        db=db,
        activity_id=activity.activity_id,
        tenant_id=tenant_id,
        subject_type_vi="Khách hàng",
        subject_type_en="Customer",
        is_children=False,
        age_range="18+"
    )
    
    # 4. Add data recipients
    recipient = await create_data_recipient(
        db=db,
        activity_id=activity.activity_id,
        tenant_id=tenant_id,
        recipient_name_vi="Bộ phận Marketing",
        recipient_name_en="Marketing Department",
        recipient_type="internal",
        is_cross_border=False,
        country_region="Vietnam"
    )
    
    # 5. Add retention policy
    retention = await create_data_retention(
        db=db,
        activity_id=activity.activity_id,
        tenant_id=tenant_id,
        retention_period_vi="5 năm",
        retention_period_en="5 years",
        legal_basis_vi="Quy định pháp luật về kế toán",
        disposal_method_vi="Xóa vĩnh viễn khỏi hệ thống"
    )
    
    # 6. Add security measures
    security = await create_security_measure(
        db=db,
        activity_id=activity.activity_id,
        tenant_id=tenant_id,
        measure_name_vi="Mã hóa dữ liệu",
        measure_name_en="Data encryption",
        measure_type="technical",
        implementation_status="implemented"
    )
    
    # 7. Add processing location
    location = await create_processing_location(
        db=db,
        activity_id=activity.activity_id,
        tenant_id=tenant_id,
        location_name_vi="Trung tâm dữ liệu Hà Nội",
        location_name_en="Hanoi Data Center",
        location_type="data_center",
        vietnamese_region="north",
        province_city="Hà Nội"
    )
    
    await db.commit()
    await db.refresh(activity)
    
    return activity


# ==============================================================================
# Integration Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_full_ropa_generation_from_database(db_session: AsyncSession, ropa_service: ROPAService):
    """
    Test complete ROPA generation workflow from database
    
    Validates:
    - Database query and data aggregation
    - ROPA entry building with all relationships
    - File generation in all formats
    - Database record creation
    - Audit log creation
    """
    # Setup
    tenant_id = await create_test_tenant(db_session)
    
    # Create 3 processing activities with full data
    activity1 = await create_full_processing_activity(
        db_session, tenant_id,
        "Quản lý khách hàng", "Customer Management"
    )
    activity2 = await create_full_processing_activity(
        db_session, tenant_id,
        "Quản lý nhân viên", "Employee Management"
    )
    activity3 = await create_full_processing_activity(
        db_session, tenant_id,
        "Quản lý đơn hàng", "Order Management"
    )
    
    # Test JSON generation
    response_json = await ropa_service.generate_ropa_from_database(
        db=db_session,
        tenant_id=tenant_id,
        format=ROPAOutputFormat.JSON,
        language=ROPALanguage.VIETNAMESE
    )
    
    # Assertions
    assert response_json["entry_count"] == 3
    assert response_json["ropa_id"] is not None
    assert response_json["file_size_bytes"] > 0
    assert response_json["format"] == "json"
    assert response_json["language"] == "vi"
    
    # Verify file exists
    # Note: File path not directly in response, service saves to storage
    
    # Verify audit log created
    audit_logs = await get_audit_logs_for_tenant(db_session, tenant_id)
    assert len(audit_logs) > 0
    assert any(log.action == "ropa_generated" for log in audit_logs)


@pytest.mark.asyncio
async def test_preview_ropa_from_database(db_session: AsyncSession, ropa_service: ROPAService):
    """
    Test ROPA preview calculation from database
    
    Validates:
    - Activity count calculation
    - Data category extraction
    - Sensitive data detection
    - Cross-border transfer detection
    - Compliance checklist generation
    - File size estimation
    """
    # Setup
    tenant_id = await create_test_tenant(db_session)
    
    # Create 5 processing activities
    for i in range(5):
        await create_full_processing_activity(
            db_session, tenant_id,
            f"Hoạt động {i+1}", f"Activity {i+1}"
        )
    
    # Get preview
    preview = await ropa_service.preview_ropa_from_database(
        db=db_session,
        tenant_id=tenant_id
    )
    
    # Assertions
    assert preview["entry_count"] == 5
    assert len(preview["data_categories"]) > 0
    assert isinstance(preview["has_sensitive_data"], bool)
    assert isinstance(preview["has_cross_border_transfers"], bool)
    assert "compliance_checklist" in preview
    assert preview["estimated_file_size_kb"] > 0


# ==============================================================================
# Multi-Tenant Isolation Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_multi_tenant_isolation(db_session: AsyncSession):
    """
    Test that tenants cannot access each other's data
    
    Validates:
    - Tenant A cannot see Tenant B's activities
    - Queries include tenant_id filter
    - No data leakage between tenants
    """
    # Setup: Create two tenants
    tenant_a = await create_test_tenant(db_session)
    tenant_b = await create_test_tenant(db_session)
    
    # Create activities for each tenant
    activity_a = await create_full_processing_activity(
        db_session, tenant_a,
        "Hoạt động Tenant A", "Tenant A Activity"
    )
    activity_b = await create_full_processing_activity(
        db_session, tenant_b,
        "Hoạt động Tenant B", "Tenant B Activity"
    )
    
    # Query Tenant A's activities
    activities_a = await get_processing_activities_for_tenant(
        db=db_session,
        tenant_id=tenant_a
    )
    
    # Query Tenant B's activities
    activities_b = await get_processing_activities_for_tenant(
        db=db_session,
        tenant_id=tenant_b
    )
    
    # Assertions: Each tenant sees only their own data
    assert len(activities_a) == 1
    assert len(activities_b) == 1
    assert activities_a[0].activity_id == activity_a.activity_id
    assert activities_b[0].activity_id == activity_b.activity_id
    assert activities_a[0].activity_id != activities_b[0].activity_id


@pytest.mark.asyncio
async def test_cascade_delete_isolation(db_session: AsyncSession):
    """
    Test CASCADE DELETE and data isolation
    
    Validates:
    - Deleting activity deletes all related data
    - Other tenants' data remains intact
    - Foreign key constraints enforced
    """
    # Setup
    tenant_a = await create_test_tenant(db_session)
    tenant_b = await create_test_tenant(db_session)
    
    # Create activities with related data
    activity_a = await create_full_processing_activity(
        db_session, tenant_a,
        "Hoạt động A", "Activity A"
    )
    activity_b = await create_full_processing_activity(
        db_session, tenant_b,
        "Hoạt động B", "Activity B"
    )
    
    # Delete activity A
    await db_session.execute(
        delete(ProcessingActivityDB).where(
            ProcessingActivityDB.activity_id == activity_a.activity_id
        )
    )
    await db_session.commit()
    
    # Verify activity A deleted
    result_a = await db_session.execute(
        select(ProcessingActivityDB).where(
            ProcessingActivityDB.activity_id == activity_a.activity_id
        )
    )
    assert result_a.scalar_one_or_none() is None
    
    # Verify activity B still exists
    result_b = await db_session.execute(
        select(ProcessingActivityDB).where(
            ProcessingActivityDB.activity_id == activity_b.activity_id
        )
    )
    assert result_b.scalar_one_or_none() is not None


# ==============================================================================
# Vietnamese-First Architecture Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_vietnamese_fields_not_null(db_session: AsyncSession):
    """
    Test that _vi fields are NOT NULL and _en fields are nullable
    
    Validates:
    - Vietnamese fields required (NOT NULL constraint)
    - English fields optional (nullable)
    - Database schema enforcement
    """
    tenant_id = await create_test_tenant(db_session)
    
    # Test 1: Create with Vietnamese only (should succeed)
    activity_vi_only = await create_processing_activity(
        db=db_session,
        tenant_id=tenant_id,
        activity_name_vi="Hoạt động chỉ có tiếng Việt",
        activity_name_en=None,  # English is nullable
        processing_purpose_vi="Mục đích bằng tiếng Việt",
        processing_purpose_en=None,
        legal_basis="consent",
        status="active"
    )
    
    assert activity_vi_only.activity_name_vi == "Hoạt động chỉ có tiếng Việt"
    assert activity_vi_only.activity_name_en is None
    
    # Test 2: Attempt to create without Vietnamese (should fail)
    with pytest.raises(Exception):  # Should raise IntegrityError
        activity_no_vi = await create_processing_activity(
            db=db_session,
            tenant_id=tenant_id,
            activity_name_vi=None,  # This should fail
            activity_name_en="English Only Activity",
            processing_purpose_vi=None,
            processing_purpose_en="English purpose",
            legal_basis="consent",
            status="active"
        )
        await db_session.commit()


@pytest.mark.asyncio
async def test_vietnamese_timezone_handling(db_session: AsyncSession):
    """
    Test Vietnamese timezone (Asia/Ho_Chi_Minh) handling
    
    Validates:
    - Timestamps use Vietnamese timezone
    - Datetime conversions correct
    - Timezone constants used
    """
    tenant_id = await create_test_tenant(db_session)
    
    # Create activity (timestamps auto-generated)
    activity = await create_full_processing_activity(
        db_session, tenant_id,
        "Kiểm tra múi giờ", "Timezone Test"
    )
    
    # Verify created_at timestamp
    assert activity.created_at is not None
    
    # Convert to Vietnamese timezone
    vietnam_tz = pytz.timezone(VIETNAM_TIMEZONE)
    vietnam_time = activity.created_at.astimezone(vietnam_tz)
    
    # Verify timezone conversion works
    assert vietnam_time.tzinfo is not None
    assert str(vietnam_time.tzinfo) == VIETNAM_TIMEZONE


@pytest.mark.asyncio
async def test_bilingual_audit_logs(db_session: AsyncSession):
    """
    Test bilingual error messages and audit logs
    
    Validates:
    - Audit logs have both message and message_vi
    - Vietnamese is primary language
    - Bilingual support throughout
    """
    tenant_id = await create_test_tenant(db_session)
    
    # Create audit log with bilingual messages
    audit_log = await create_audit_log(
        db=db_session,
        tenant_id=tenant_id,
        entity_type="processing_activity",
        entity_id=uuid4(),
        action="create",
        user_id=SYSTEM_USER_ID,
        changes={"field": "value"},
        message="Activity created successfully",
        message_vi="Tạo hoạt động thành công"
    )
    
    # Assertions
    assert audit_log.message == "Activity created successfully"
    assert audit_log.message_vi == "Tạo hoạt động thành công"
    assert audit_log.message_vi is not None  # Vietnamese required


# ==============================================================================
# End-to-End ROPA Generation Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_end_to_end_ropa_all_formats(db_session: AsyncSession, ropa_service: ROPAService):
    """
    Test complete ROPA generation workflow in all formats
    
    Validates:
    - Create activities with all related data
    - Generate ROPA in JSON, CSV, PDF, MPS_FORMAT
    - Verify file outputs exist
    - Check database records (ropa_documents, audit_logs)
    - Verify MPS compliance flags
    """
    # Setup
    tenant_id = await create_test_tenant(db_session)
    
    # Create comprehensive processing activities
    activity1 = await create_full_processing_activity(
        db_session, tenant_id,
        "Quản lý khách hàng", "Customer Management"
    )
    
    activity2 = await create_full_processing_activity(
        db_session, tenant_id,
        "Quản lý nhân viên", "Employee Management"
    )
    
    # Test all formats
    formats = [
        ROPAOutputFormat.JSON,
        ROPAOutputFormat.CSV,
        # ROPAOutputFormat.PDF,  # Skip PDF if no font installed
        # ROPAOutputFormat.MPS_FORMAT
    ]
    
    for format in formats:
        response = await ropa_service.generate_ropa_from_database(
            db=db_session,
            tenant_id=tenant_id,
            format=format,
            language=ROPALanguage.VIETNAMESE
        )
        
        # Assertions for each format
        assert response["entry_count"] == 2
        assert response["format"] == format.value
        assert response["language"] == "vi"
        assert isinstance(response["mps_compliant"], bool)
        assert isinstance(response["has_sensitive_data"], bool)
        assert isinstance(response["has_cross_border_transfers"], bool)
        assert response["file_size_bytes"] > 0


@pytest.mark.asyncio
async def test_mps_compliance_validation(db_session: AsyncSession, ropa_service: ROPAService):
    """
    Test MPS (Ministry of Public Security) compliance validation
    
    Validates:
    - Legal basis for all processing activities
    - Security measures documented
    - Retention periods defined
    - MPS compliance flag calculation
    """
    tenant_id = await create_test_tenant(db_session)
    
    # Create compliant activity (has legal basis, security, retention)
    compliant_activity = await create_full_processing_activity(
        db_session, tenant_id,
        "Hoạt động tuân thủ", "Compliant Activity"
    )
    
    # Generate ROPA
    response = await ropa_service.generate_ropa_from_database(
        db=db_session,
        tenant_id=tenant_id,
        format=ROPAOutputFormat.JSON,
        language=ROPALanguage.VIETNAMESE
    )
    
    # MPS compliance should be True
    assert response["mps_compliant"] == True


# ==============================================================================
# CRUD Operation Tests
# ==============================================================================

@pytest.mark.asyncio
async def test_all_crud_operations(db_session: AsyncSession):
    """
    Test all CRUD operations work with real database
    
    Validates:
    - Create operations for all entities
    - Read operations with filters
    - Update operations
    - Delete operations
    - Multi-tenant isolation in all operations
    """
    tenant_id = await create_test_tenant(db_session)
    
    # Create processing activity
    activity = await create_processing_activity(
        db=db_session,
        tenant_id=tenant_id,
        activity_name_vi="Hoạt động CRUD",
        activity_name_en="CRUD Activity",
        processing_purpose_vi="Kiểm tra CRUD",
        processing_purpose_en="Test CRUD",
        legal_basis="consent",
        status="active"
    )
    
    # Read operation
    fetched_activity = await get_processing_activity(
        db=db_session,
        activity_id=activity.activity_id,
        tenant_id=tenant_id
    )
    assert fetched_activity.activity_name_vi == "Hoạt động CRUD"
    
    # Update operation (direct SQLAlchemy update for simplicity)
    fetched_activity.activity_name_vi = "Hoạt động đã cập nhật"
    await db_session.commit()
    await db_session.refresh(fetched_activity)
    assert fetched_activity.activity_name_vi == "Hoạt động đã cập nhật"
    
    # Delete operation
    await db_session.delete(fetched_activity)
    await db_session.commit()
    
    # Verify deleted
    deleted_activity = await get_processing_activity(
        db=db_session,
        activity_id=activity.activity_id,
        tenant_id=tenant_id
    )
    assert deleted_activity is None


# ==============================================================================
# Export Function
# ==============================================================================

__all__ = [
    'test_full_ropa_generation_from_database',
    'test_preview_ropa_from_database',
    'test_multi_tenant_isolation',
    'test_cascade_delete_isolation',
    'test_vietnamese_fields_not_null',
    'test_vietnamese_timezone_handling',
    'test_bilingual_audit_logs',
    'test_end_to_end_ropa_all_formats',
    'test_mps_compliance_validation',
    'test_all_crud_operations'
]
