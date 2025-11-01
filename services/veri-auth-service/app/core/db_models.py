# ============================================
# VeriSyntra Auth Service - Database Models
# ============================================
# SQLAlchemy ORM models for PostgreSQL
# ============================================

from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class TenantDB(Base):
    """Vietnamese business tenant database model"""
    __tablename__ = "tenants"
    
    tenant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(200), nullable=False)
    company_name_vi = Column(String(200))
    tax_id = Column(String(13), unique=True)
    
    # Regional and industry context
    veri_regional_location = Column(String(20), default="south")
    veri_industry_type = Column(String(50), default="technology")
    
    # Subscription
    subscription_tier = Column(String(20), default="starter")
    subscription_start_date = Column(DateTime)
    subscription_end_date = Column(DateTime)
    max_users = Column(Integer, default=10)
    
    # Contact information
    primary_email = Column(String(255))
    primary_phone = Column(String(20))
    address = Column(String)
    address_vi = Column(String)
    city = Column(String(100))
    province = Column(String(100))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # PDPL compliance
    data_residency_region = Column(String(50), default="vietnam")
    pdpl_compliant = Column(Boolean, default=False)
    
    # Vietnamese business context (JSON)
    veri_business_context = Column(JSON, default={})
    
    # Relationships
    users = relationship("UserDB", back_populates="tenant", cascade="all, delete-orphan")


class UserDB(Base):
    """Vietnamese business user database model"""
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    full_name_vi = Column(String(100))
    phone_number = Column(String(20))
    
    # Multi-tenant relationship
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="CASCADE"), nullable=False)
    
    # User role
    role = Column(String(30), default="staff")
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Vietnamese preferences
    preferred_language = Column(String(5), default="vi")
    timezone = Column(String(50), default="Asia/Ho_Chi_Minh")
    
    # Relationships
    tenant = relationship("TenantDB", back_populates="users")
    refresh_tokens = relationship("RefreshTokenDB", back_populates="user", cascade="all, delete-orphan")


class RefreshTokenDB(Base):
    """JWT refresh token database model"""
    __tablename__ = "refresh_tokens"
    
    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_revoked = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("UserDB", back_populates="refresh_tokens")


class AuditLogDB(Base):
    """Vietnamese compliance audit log database model"""
    __tablename__ = "audit_log"
    
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="SET NULL"))
    action = Column(String(100), nullable=False)
    details = Column(JSON, default={})
    ip_address = Column(String(50))
    user_agent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    vietnam_time = Column(DateTime, default=lambda: datetime.utcnow())
