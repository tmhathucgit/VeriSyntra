"""
RBAC CRUD Operations - VeriSyntra Standards Compliant
Database access for permissions and role-based authorization

Task: 1.1.3 RBAC - Step 4
Date: November 8, 2025
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import List, Optional
import logging

from auth.rbac_schemas import (
    PermissionSchema, 
    RoleSchema, 
    UserWithPermissionsSchema,
    get_role_display_name
)
from database.models.user import User
from database.models.rbac import Permission, RolePermission

logger = logging.getLogger(__name__)


def get_user_permissions(
    db: Session, 
    user_id: str
) -> List[str]:
    """
    Get list of permission names for a user based on their role
    
    Args:
        db: Database session
        user_id: User UUID
    
    Returns:
        List of permission names (e.g., ['processing_activity.read'])
    
    Vietnamese: Lay danh sach quyen cua nguoi dung
    """
    try:
        # Get user's role
        query = select(User.role).where(User.user_id == user_id)
        result = db.execute(query)
        user_role = result.scalar_one_or_none()
        
        if not user_role:
            logger.warning(f"User {user_id} not found")
            return []
        
        # Get permissions for this role
        query = select(Permission.permission_name).join(
            RolePermission, 
            Permission.permission_id == RolePermission.permission_id
        ).where(RolePermission.role == user_role)
        
        result = db.execute(query)
        permissions = [row[0] for row in result.fetchall()]
        
        logger.info(f"User {user_id} (role: {user_role}) has {len(permissions)} permissions")
        return permissions
        
    except Exception as e:
        logger.error(f"Error getting permissions for user {user_id}: {str(e)}")
        return []


def user_has_permission(
    db: Session,
    user_id: str,
    permission_name: str
) -> bool:
    """
    Check if user has a specific permission
    
    Args:
        db: Database session
        user_id: User UUID
        permission_name: Permission to check (e.g., 'processing_activity.write')
    
    Returns:
        True if user has permission, False otherwise
    
    Vietnamese: Kiem tra nguoi dung co quyen khong
    
    Example:
        has_perm = user_has_permission(db, user_id, 'processing_activity.write')
    """
    permissions = get_user_permissions(db, user_id)
    has_permission = permission_name in permissions
    
    logger.debug(
        f"Permission check: user={user_id}, "
        f"permission={permission_name}, "
        f"allowed={has_permission}"
    )
    
    return has_permission


def get_user_with_permissions(
    db: Session,
    user_id: str,
    lang: str = 'vi'
) -> Optional[UserWithPermissionsSchema]:
    """
    Get user profile with full permission list (Vietnamese-first)
    
    Args:
        db: Database session
        user_id: User UUID
        lang: Language code ('vi' or 'en')
    
    Returns:
        UserWithPermissionsSchema or None if user not found
    
    Vietnamese: Lay ho so nguoi dung voi danh sach quyen
    """
    try:
        # Get user
        query = select(User).where(User.user_id == user_id)
        result = db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"User {user_id} not found")
            return None
        
        # Get permissions
        permissions = get_user_permissions(db, user_id)
        
        # Get role display name
        role_vi = get_role_display_name(user.role, 'vi')
        
        return UserWithPermissionsSchema(
            user_id=str(user.user_id),
            email=user.email,
            full_name=user.full_name or "",
            full_name_vi=user.full_name_vi or "",
            tenant_id=str(user.tenant_id),
            role=user.role,
            role_vi=role_vi,
            is_active=user.is_active,
            permissions=permissions
        )
        
    except Exception as e:
        logger.error(f"Error getting user with permissions: {str(e)}")
        return None


def get_role_permissions(
    db: Session,
    role: str
) -> List[PermissionSchema]:
    """
    Get all permissions for a specific role with Vietnamese names
    
    Args:
        db: Database session
        role: Role identifier (admin, dpo, etc.)
    
    Returns:
        List of PermissionSchema objects
    
    Vietnamese: Lay tat ca quyen cua vai tro
    """
    try:
        query = select(Permission).join(
            RolePermission,
            Permission.permission_id == RolePermission.permission_id
        ).where(RolePermission.role == role)
        
        result = db.execute(query)
        permissions = result.scalars().all()
        
        return [
            PermissionSchema(
                permission_id=str(p.permission_id),
                permission_name=p.permission_name,
                permission_name_vi=p.permission_name_vi,
                resource=p.resource,
                action=p.action,
                description=p.description,
                description_vi=p.description_vi
            )
            for p in permissions
        ]
        
    except Exception as e:
        logger.error(f"Error getting permissions for role {role}: {str(e)}")
        return []


def validate_tenant_access(
    db: Session,
    user_id: str,
    resource_tenant_id: str
) -> bool:
    """
    Ensure user can only access resources from their own tenant
    Multi-tenant isolation (Cach ly da tenant)
    
    Args:
        db: Database session
        user_id: User UUID
        resource_tenant_id: Tenant ID of the resource being accessed
    
    Returns:
        True if access allowed, False otherwise
    
    Vietnamese: Xac thuc nguoi dung chi truy cap du lieu cua tenant cua ho
    """
    try:
        query = select(User.tenant_id).where(User.user_id == user_id)
        result = db.execute(query)
        user_tenant_id = result.scalar_one_or_none()
        
        if not user_tenant_id:
            logger.warning(f"User {user_id} not found for tenant validation")
            return False
        
        allowed = str(user_tenant_id) == str(resource_tenant_id)
        
        if not allowed:
            logger.warning(
                f"Tenant access denied: user tenant={user_tenant_id}, "
                f"resource tenant={resource_tenant_id}"
            )
        
        return allowed
        
    except Exception as e:
        logger.error(f"Error validating tenant access: {str(e)}")
        return False


def get_all_permissions(
    db: Session
) -> List[PermissionSchema]:
    """
    Get all permissions in the system
    
    Args:
        db: Database session
    
    Returns:
        List of all PermissionSchema objects
    
    Vietnamese: Lay tat ca quyen trong he thong
    """
    try:
        query = select(Permission).order_by(Permission.resource, Permission.action)
        result = db.execute(query)
        permissions = result.scalars().all()
        
        return [
            PermissionSchema(
                permission_id=str(p.permission_id),
                permission_name=p.permission_name,
                permission_name_vi=p.permission_name_vi,
                resource=p.resource,
                action=p.action,
                description=p.description,
                description_vi=p.description_vi
            )
            for p in permissions
        ]
        
    except Exception as e:
        logger.error(f"Error getting all permissions: {str(e)}")
        return []


def get_users_by_role(
    db: Session,
    role: str,
    tenant_id: Optional[str] = None
) -> List[UserWithPermissionsSchema]:
    """
    Get all users with a specific role
    
    Args:
        db: Database session
        role: Role identifier (admin, dpo, etc.)
        tenant_id: Optional tenant ID filter
    
    Returns:
        List of UserWithPermissionsSchema objects
    
    Vietnamese: Lay tat ca nguoi dung co vai tro cu the
    """
    try:
        query = select(User).where(User.role == role)
        
        if tenant_id:
            query = query.where(User.tenant_id == tenant_id)
        
        result = db.execute(query)
        users = result.scalars().all()
        
        # Get permissions for this role (same for all users with this role)
        permissions = get_user_permissions(db, str(users[0].user_id)) if users else []
        role_vi = get_role_display_name(role, 'vi')
        
        return [
            UserWithPermissionsSchema(
                user_id=str(u.user_id),
                email=u.email,
                full_name=u.full_name or "",
                full_name_vi=u.full_name_vi or "",
                tenant_id=str(u.tenant_id),
                role=u.role,
                role_vi=role_vi,
                is_active=u.is_active,
                permissions=permissions
            )
            for u in users
        ]
        
    except Exception as e:
        logger.error(f"Error getting users by role {role}: {str(e)}")
        return []
