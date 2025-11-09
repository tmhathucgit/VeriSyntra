"""
Permission and RolePermission SQLAlchemy Models
VeriSyntra RBAC Database Models

Task: 1.1.3 RBAC - Step 4
Date: November 8, 2025
"""

from sqlalchemy import Column, String, Text, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.sql import func
from database.models.base import Base
import uuid


class Permission(Base):
    """
    Permission model - Defines all available permissions in the system
    Vietnamese: Mo hinh quyen - Dinh nghia tat ca quyen trong he thong
    """
    __tablename__ = "permissions"
    
    permission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_name = Column(String(100), unique=True, nullable=False, index=True)
    permission_name_vi = Column(String(255), nullable=False)
    resource = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    description_vi = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    def __repr__(self):
        return f"<Permission {self.permission_name}>"


class RolePermission(Base):
    """
    RolePermission model - Maps roles to permissions
    Vietnamese: Mo hinh anh xa vai tro den quyen
    """
    __tablename__ = "role_permissions"
    
    role_permission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String(50), nullable=False, index=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.permission_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    def __repr__(self):
        return f"<RolePermission role={self.role}>"
