"""
User CRUD Operations
Vietnamese Business Context: Multi-tenant user management
PDPL 2025 Compliance: Secure password handling, audit logging
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from auth.password_utils import hash_password, verify_password
from database.models.user import User


class UserCRUD:
    """User CRUD operations with Vietnamese business context - Quản lý người dùng"""
    
    @staticmethod
    def create_user(
        db: Session,
        email: str,
        password: str,
        full_name: str,
        tenant_id: UUID,
        full_name_vi: Optional[str] = None,
        phone_number: Optional[str] = None,
        role: str = 'staff',
        regional_location: Optional[str] = None  # For backwards compatibility
    ) -> User:
        """
        Create new user with hashed password - Tạo người dùng mới
        
        Vietnamese Context: Supports bilingual names and Vietnamese phone numbers
        Security: Uses bcrypt password hashing
        
        Args:
            db: Database session
            email: Email address (unique per tenant)
            password: Plain text password (will be hashed)
            full_name: Full name (English or Vietnamese)
            tenant_id: Tenant UUID for multi-tenant isolation
            full_name_vi: Vietnamese name with proper diacritics
            phone_number: Vietnamese phone number format
            role: User role (admin, dpo, compliance_manager, staff, auditor, viewer)
            regional_location: Optional, for backwards compatibility (stored in context)
            
        Returns:
            Created User object
        """
        # Hash password using bcrypt
        hashed_password = hash_password(password)
        
        # Create user
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            full_name_vi=full_name_vi or full_name,
            phone_number=phone_number,
            tenant_id=tenant_id,
            role=role,
            is_active=True,
            is_verified=False,
            is_email_verified=False,
            preferred_language='vi',
            timezone='Asia/Ho_Chi_Minh',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """
        Get user by ID - Lấy người dùng theo ID
        
        Args:
            db: Database session
            user_id: User UUID
            
        Returns:
            User object or None
        """
        return db.query(User).filter(User.user_id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str, tenant_id: Optional[UUID] = None) -> Optional[User]:
        """
        Get user by email - Lấy người dùng theo email
        
        Multi-tenant aware: Can filter by tenant_id if provided
        
        Args:
            db: Database session
            email: Email address
            tenant_id: Optional tenant filter for multi-tenant isolation
            
        Returns:
            User object or None
        """
        query = db.query(User).filter(User.email == email)
        if tenant_id:
            query = query.filter(User.tenant_id == tenant_id)
        return query.first()
    
    @staticmethod
    def verify_user_password(db: Session, email: str, password: str, tenant_id: Optional[UUID] = None) -> Optional[User]:
        """
        Verify user credentials - Xác thực thông tin đăng nhập
        
        Security Features:
        - Email-based authentication (no username)
        - Password verification using bcrypt
        - Multi-tenant isolation support
        
        Args:
            db: Database session
            email: Email address
            password: Plain text password
            tenant_id: Optional tenant filter
            
        Returns:
            User object if valid, None if invalid
        """
        user = UserCRUD.get_user_by_email(db, email, tenant_id)
        
        if not user:
            return None
        
        # Verify password using Phase 2 hashed_password column - Xác thực mật khẩu
        if not verify_password(password, user.hashed_password):
            db.commit()
            return None
        
        # Update last login on successful authentication - Cập nhật thời gian đăng nhập cuối
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def update_last_login(db: Session, user_id: UUID) -> None:
        """
        Update last login timestamp - Cập nhật thời gian đăng nhập cuối
        
        Args:
            db: Database session
            user_id: User UUID
        """
        user = UserCRUD.get_user_by_id(db, user_id)
        if user:
            user.last_login = datetime.utcnow()
            db.commit()
