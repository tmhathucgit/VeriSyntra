# ============================================
# VeriSyntra Auth Service - CRUD Operations
# ============================================
# Database CRUD operations for users and tenants
# ============================================

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional
from uuid import UUID
from datetime import datetime
import pytz

from app.core.db_models import UserDB, TenantDB
from app.models.user import VeriUserCreate
from app.models.tenant import VeriTenantCreate
from app.core.security import hash_password


# ============================================
# Tenant CRUD Operations
# ============================================

async def create_tenant(
    db: AsyncSession,
    tenant_data: VeriTenantCreate
) -> TenantDB:
    """
    Create new Vietnamese business tenant
    
    Args:
        db: Database session
        tenant_data: Tenant creation data
        
    Returns:
        Created tenant database object
    """
    db_tenant = TenantDB(
        company_name=tenant_data.company_name,
        company_name_vi=tenant_data.company_name_vi or tenant_data.company_name,
        tax_id=tenant_data.tax_id,
        veri_regional_location=tenant_data.veri_regional_location.value,
        veri_industry_type=tenant_data.veri_industry_type.value,
        subscription_tier=tenant_data.subscription_tier.value,
        primary_email=tenant_data.primary_email,
        primary_phone=tenant_data.primary_phone,
        address=tenant_data.address,
        address_vi=tenant_data.address_vi,
        city=tenant_data.city,
        province=tenant_data.province,
        is_active=True,
        is_verified=False,
        pdpl_compliant=False
    )
    
    db.add(db_tenant)
    await db.flush()
    await db.refresh(db_tenant)
    
    return db_tenant


async def get_tenant_by_id(
    db: AsyncSession,
    tenant_id: UUID
) -> Optional[TenantDB]:
    """Get tenant by ID"""
    result = await db.execute(
        select(TenantDB).where(TenantDB.tenant_id == tenant_id)
    )
    return result.scalar_one_or_none()


async def get_tenant_by_tax_id(
    db: AsyncSession,
    tax_id: str
) -> Optional[TenantDB]:
    """Get tenant by Vietnamese tax ID"""
    result = await db.execute(
        select(TenantDB).where(TenantDB.tax_id == tax_id)
    )
    return result.scalar_one_or_none()


# ============================================
# User CRUD Operations
# ============================================

async def create_user(
    db: AsyncSession,
    user_data: VeriUserCreate,
    tenant_id: UUID,
    role: str = "admin"
) -> UserDB:
    """
    Create new Vietnamese business user
    
    Args:
        db: Database session
        user_data: User creation data
        tenant_id: Associated tenant ID
        role: User role (default: admin for first user)
        
    Returns:
        Created user database object
    """
    hashed_pwd = hash_password(user_data.password)
    
    db_user = UserDB(
        email=user_data.email,
        hashed_password=hashed_pwd,
        full_name=user_data.full_name,
        full_name_vi=user_data.full_name_vi or user_data.full_name,
        phone_number=user_data.phone_number,
        tenant_id=tenant_id,
        role=role,
        is_active=True,
        is_verified=False,
        is_email_verified=False,
        preferred_language=user_data.preferred_language,
        timezone="Asia/Ho_Chi_Minh"
    )
    
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    
    return db_user


async def get_user_by_email(
    db: AsyncSession,
    email: str,
    tenant_id: Optional[UUID] = None
) -> Optional[UserDB]:
    """
    Get user by email (optionally filtered by tenant)
    
    Args:
        db: Database session
        email: User email
        tenant_id: Optional tenant ID for multi-tenant filtering
        
    Returns:
        User database object or None
    """
    query = select(UserDB).where(UserDB.email == email)
    
    if tenant_id:
        query = query.where(UserDB.tenant_id == tenant_id)
    
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(
    db: AsyncSession,
    user_id: UUID
) -> Optional[UserDB]:
    """Get user by ID"""
    result = await db.execute(
        select(UserDB).where(UserDB.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def update_user_last_login(
    db: AsyncSession,
    user_id: UUID
) -> None:
    """Update user's last login timestamp"""
    user = await get_user_by_id(db, user_id)
    if user:
        # Get Vietnamese time and convert to naive datetime for PostgreSQL
        vietnam_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        user.last_login = vietnam_time.replace(tzinfo=None)
        await db.flush()


async def update_user_password(
    db: AsyncSession,
    user_id: UUID,
    new_password: str
) -> None:
    """Update user's password"""
    user = await get_user_by_id(db, user_id)
    if user:
        user.hashed_password = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        await db.flush()


async def count_tenant_users(
    db: AsyncSession,
    tenant_id: UUID
) -> int:
    """Count number of users in a tenant"""
    result = await db.execute(
        select(UserDB).where(UserDB.tenant_id == tenant_id)
    )
    users = result.scalars().all()
    return len(users)
