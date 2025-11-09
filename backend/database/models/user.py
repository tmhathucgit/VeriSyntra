"""
SQLAlchemy User model for authentication and authorization
Vietnamese business context: Multi-tenant user management with regional preferences
PDPL 2025 Compliance: Secure password storage, audit logging
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import (
    Column, String, Boolean, Integer, DateTime, ForeignKey, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..base import Base


class User(Base):
    """
    User model - Người dùng
    
    Supports multi-tenant isolation and Vietnamese business contexts.
    """
    
    __tablename__ = 'users'
    
    # Table-level constraints - match existing database schema
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'dpo', 'compliance_manager', 'staff', 'auditor', 'viewer')", name='users_role_check'),
    )
    
    # Primary key - Khóa chính
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication credentials - Thông tin xác thực
    email = Column(String(255), unique=False, nullable=False, index=True)  # Unique with tenant_id
    hashed_password = Column(String(255), nullable=False)  # Match actual DB column name
    
    # Multi-tenant isolation - Cách ly đa tổ chức
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # User profile - Hồ sơ người dùng
    full_name = Column(String(100), nullable=False)  # Họ tên (English)
    full_name_vi = Column(String(100))  # Họ tên (Vietnamese with diacritics)
    phone_number = Column(String(20))  # Số điện thoại
    
    # Role-based access control - Kiểm soát truy cập dựa trên vai trò
    role = Column(String(30), nullable=True, default='staff', index=True)  # Vai trò
    
    # Account status - Trạng thái tài khoản
    is_active = Column(Boolean, nullable=True, default=True, index=True)  # Hoạt động
    is_verified = Column(Boolean, nullable=True, default=False)  # Đã xác thực
    is_email_verified = Column(Boolean, nullable=True, default=False)  # Đã xác thực email
    
    # Timestamps and login tracking
    created_at = Column(DateTime(timezone=False), nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=False), nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime(timezone=False))  # Match DB column name
    
    # Vietnamese-specific fields
    preferred_language = Column(String(5), default='vi')  # Ngôn ngữ ưa thích
    timezone = Column(String(50), default='Asia/Ho_Chi_Minh')  # Múi giờ
    
    def __repr__(self) -> str:
        """String representation - Biểu diễn chuỗi"""
        return f"<User(email='{self.email}', role='{self.role}')>"
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        Convert model to dictionary - Chuyển đổi model thành dictionary
        
        Args:
            include_sensitive: Include sensitive fields like hashed_password
            
        Returns:
            Dictionary representation of user
        """
        data = {
            'user_id': str(self.user_id),
            'email': self.email,
            'tenant_id': str(self.tenant_id),
            'full_name': self.full_name,
            'full_name_vi': self.full_name_vi,
            'phone_number': self.phone_number,
            'role': self.role,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'is_email_verified': self.is_email_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'preferred_language': self.preferred_language,
            'timezone': self.timezone,
        }
        
        if include_sensitive:
            data['hashed_password'] = self.hashed_password
        
        return data
