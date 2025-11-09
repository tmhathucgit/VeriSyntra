"""
RBAC FastAPI Dependencies - VeriSyntra Standards Compliant
Permission decorators and dependency injection for endpoint security

Task: 1.1.3 RBAC - Step 5
Date: November 8, 2025

Coding Standards:
- NO emoji characters
- Vietnamese-first bilingual errors
- Type hints on all functions
- Async/await pattern
- Multi-tenant isolation enforced

Vietnamese: Phu thuoc FastAPI RBAC cho bao mat endpoint
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database.session import get_db
from auth.jwt_handler import verify_token, TOKEN_TYPE_ACCESS
from auth.rbac_crud import (
    get_user_permissions,
    validate_tenant_access as validate_tenant_access_db,
    get_user_with_permissions
)
from auth.rbac_schemas import RBACErrorMessages, get_role_display_name

logger = logging.getLogger(__name__)
security = HTTPBearer()


# Current User Model (from JWT token)
class CurrentUser:
    """
    Current authenticated user with permissions
    
    Represents the authenticated Vietnamese business user with their
    role, permissions, and tenant context.
    
    Attributes:
        user_id: User unique identifier
        email: User email address
        tenant_id: Vietnamese business tenant ID
        role: User role (admin, dpo, compliance_manager, etc.)
        permissions: List of permission names user has
    
    Vietnamese: Nguoi dung hien tai voi quyen han
    """
    
    def __init__(
        self,
        user_id: str,
        email: str,
        tenant_id: str,
        role: str,
        permissions: List[str]
    ):
        self.user_id = user_id
        self.email = email
        self.tenant_id = tenant_id
        self.role = role
        self.permissions = permissions
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if user has specific permission
        
        Args:
            permission: Permission name (e.g., 'processing_activity.read')
        
        Returns:
            True if user has permission, False otherwise
        
        Vietnamese: Kiem tra nguoi dung co quyen khong
        """
        return permission in self.permissions
    
    def has_any_permission(self, permissions: List[str]) -> bool:
        """
        Check if user has at least one of the specified permissions
        
        Args:
            permissions: List of permission names
        
        Returns:
            True if user has at least one permission
        
        Vietnamese: Kiem tra nguoi dung co it nhat mot quyen
        """
        return any(perm in self.permissions for perm in permissions)
    
    def has_all_permissions(self, permissions: List[str]) -> bool:
        """
        Check if user has all specified permissions
        
        Args:
            permissions: List of permission names
        
        Returns:
            True if user has all permissions
        
        Vietnamese: Kiem tra nguoi dung co tat ca quyen
        """
        return all(perm in self.permissions for perm in permissions)


# Get current user from JWT token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> CurrentUser:
    """
    Extract and validate current user from JWT token
    
    This is the main authentication dependency for all protected endpoints.
    Verifies JWT token, checks user exists and is active, loads permissions.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session
    
    Returns:
        CurrentUser with permissions loaded
    
    Raises:
        HTTPException 401: Invalid or expired token
        HTTPException 403: User inactive
        HTTPException 404: User not found
    
    Usage:
        @router.get("/protected")
        async def protected_endpoint(
            current_user: CurrentUser = Depends(get_current_user)
        ):
            return {"user": current_user.email}
    
    Vietnamese: Lay nguoi dung hien tai tu JWT token
    """
    try:
        # Verify JWT token - Xac minh JWT token
        token = credentials.credentials
        payload = verify_token(token, TOKEN_TYPE_ACCESS)
        
        if not payload:
            logger.warning("[ERROR] Invalid token: payload is None")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Invalid token",
                    "error_vi": "Token khong hop le"
                }
            )
        
        # Extract user_id from token - Trích xuất user_id từ token
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("[ERROR] Invalid token payload: missing 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Invalid token payload",
                    "error_vi": "Noi dung token khong hop le"
                }
            )
        
        # Get user with permissions from database - Lay nguoi dung voi quyen tu database
        user_with_perms = get_user_with_permissions(db, user_id)
        
        if not user_with_perms:
            logger.warning(f"[ERROR] User not found: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "User not found",
                    "error_vi": "Khong tim thay nguoi dung"
                }
            )
        
        # Check if user is active - Kiem tra nguoi dung co hoat dong khong
        if not user_with_perms.is_active:
            logger.warning(f"[ERROR] Inactive user attempted access: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": RBACErrorMessages.INACTIVE_USER['en'],
                    "error_vi": RBACErrorMessages.INACTIVE_USER['vi']
                }
            )
        
        # Create CurrentUser object - Tao doi tuong CurrentUser
        current_user = CurrentUser(
            user_id=user_with_perms.user_id,
            email=user_with_perms.email,
            tenant_id=user_with_perms.tenant_id,
            role=user_with_perms.role,
            permissions=user_with_perms.permissions
        )
        
        logger.info(
            f"[OK] User authenticated -> "
            f"Email: {current_user.email}, "
            f"Role: {current_user.role}, "
            f"Permissions: {len(current_user.permissions)}"
        )
        
        return current_user
        
    except HTTPException:
        # Re-raise HTTP exceptions - Nem lai ngoai le HTTP
        raise
    
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Authentication error",
                "error_vi": "Loi xac thuc"
            }
        )


# Permission requirement decorator factory
def require_permission(permission: str):
    """
    Decorator factory for permission-based access control
    
    Creates a FastAPI dependency that checks if the current user
    has the required permission. Raises 403 with bilingual error
    if permission is denied.
    
    Args:
        permission: Required permission name (e.g., 'processing_activity.read')
    
    Returns:
        FastAPI dependency function that validates permission
    
    Usage:
        @router.get("/processing-activities")
        async def get_activities(
            current_user: CurrentUser = Depends(require_permission("processing_activity.read"))
        ):
            return activities
    
    Vietnamese: Tao decorator yeu cau quyen
    """
    def permission_checker(current_user: CurrentUser = Depends(get_current_user)):
        """
        Check if current user has required permission
        
        Args:
            current_user: Authenticated user from get_current_user
        
        Returns:
            CurrentUser if permission granted
        
        Raises:
            HTTPException 403: Permission denied
        
        Vietnamese: Kiem tra nguoi dung hien tai co quyen yeu cau
        """
        if not current_user.has_permission(permission):
            logger.warning(
                f"[ERROR] Permission denied -> "
                f"User: {current_user.email}, "
                f"Role: {current_user.role}, "
                f"Required: {permission}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": RBACErrorMessages.get_message(
                        'PERMISSION_DENIED', 
                        'en', 
                        permission=permission
                    ),
                    "error_vi": RBACErrorMessages.get_message(
                        'PERMISSION_DENIED', 
                        'vi', 
                        permission=permission
                    ),
                    "required_permission": permission,
                    "user_role": current_user.role,
                    "user_role_vi": get_role_display_name(current_user.role, 'vi')
                }
            )
        
        logger.debug(
            f"[OK] Permission granted -> "
            f"User: {current_user.email}, "
            f"Permission: {permission}"
        )
        
        return current_user
    
    return permission_checker


# Require any of multiple permissions
def require_any_permission(permissions: List[str]):
    """
    Decorator factory requiring at least one of multiple permissions
    
    Args:
        permissions: List of acceptable permissions
    
    Returns:
        FastAPI dependency function
    
    Usage:
        @router.get("/reports")
        async def get_reports(
            current_user: CurrentUser = Depends(
                require_any_permission(["ropa.read", "analytics.read"])
            )
        ):
            return reports
    
    Vietnamese: Yeu cau it nhat mot quyen trong danh sach
    """
    def permission_checker(current_user: CurrentUser = Depends(get_current_user)):
        if not current_user.has_any_permission(permissions):
            logger.warning(
                f"[ERROR] Permission denied (any required) -> "
                f"User: {current_user.email}, "
                f"Role: {current_user.role}, "
                f"Required one of: {permissions}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": f"One of these permissions required: {', '.join(permissions)}",
                    "error_vi": f"Can mot trong cac quyen: {', '.join(permissions)}",
                    "required_permissions": permissions,
                    "user_role": current_user.role,
                    "user_role_vi": get_role_display_name(current_user.role, 'vi')
                }
            )
        
        return current_user
    
    return permission_checker


# Require all of multiple permissions
def require_all_permissions(permissions: List[str]):
    """
    Decorator factory requiring all specified permissions
    
    Args:
        permissions: List of required permissions
    
    Returns:
        FastAPI dependency function
    
    Usage:
        @router.post("/sensitive-data")
        async def handle_sensitive(
            current_user: CurrentUser = Depends(
                require_all_permissions([
                    "data_category.write",
                    "data_category.manage_sensitive"
                ])
            )
        ):
            return result
    
    Vietnamese: Yeu cau tat ca quyen trong danh sach
    """
    def permission_checker(current_user: CurrentUser = Depends(get_current_user)):
        if not current_user.has_all_permissions(permissions):
            missing = [p for p in permissions if p not in current_user.permissions]
            logger.warning(
                f"[ERROR] Permission denied (all required) -> "
                f"User: {current_user.email}, "
                f"Role: {current_user.role}, "
                f"Missing: {missing}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": f"All permissions required: {', '.join(permissions)}",
                    "error_vi": f"Can tat ca cac quyen: {', '.join(permissions)}",
                    "required_permissions": permissions,
                    "missing_permissions": missing,
                    "user_role": current_user.role,
                    "user_role_vi": get_role_display_name(current_user.role, 'vi')
                }
            )
        
        return current_user
    
    return permission_checker


# Tenant isolation validator
def require_tenant_access(
    resource_tenant_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> bool:
    """
    Validate user can only access resources from their tenant
    Multi-tenant isolation enforcement
    
    Args:
        resource_tenant_id: Tenant ID of the resource being accessed
        current_user: Authenticated user
        db: Database session
    
    Returns:
        True if access allowed
    
    Raises:
        HTTPException 403: Tenant access denied
    
    Usage:
        activity = get_activity(activity_id)
        await require_tenant_access(activity.tenant_id, current_user, db)
    
    Vietnamese: Xac thuc nguoi dung chi truy cap tai nguyen cua tenant cua ho
    """
    # Admin can access all tenants - Admin co the truy cap tat ca tenant
    if current_user.role == 'admin':
        logger.debug(f"[OK] Admin bypass tenant check -> User: {current_user.email}")
        return True
    
    # Validate tenant access - Xac thuc truy cap tenant
    is_allowed = validate_tenant_access_db(
        db, 
        current_user.user_id, 
        resource_tenant_id
    )
    
    if not is_allowed:
        logger.warning(
            f"[ERROR] Tenant access denied -> "
            f"User: {current_user.email}, "
            f"User tenant: {current_user.tenant_id}, "
            f"Resource tenant: {resource_tenant_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": RBACErrorMessages.TENANT_ACCESS_DENIED['en'],
                "error_vi": RBACErrorMessages.TENANT_ACCESS_DENIED['vi'],
                "user_tenant_id": current_user.tenant_id,
                "resource_tenant_id": resource_tenant_id
            }
        )
    
    logger.debug(
        f"[OK] Tenant access granted -> "
        f"User: {current_user.email}, "
        f"Tenant: {current_user.tenant_id}"
    )
    
    return True


# Optional authentication (allow anonymous or authenticated)
def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[CurrentUser]:
    """
    Get current user if token provided, otherwise return None
    
    Useful for endpoints that work for both authenticated and
    anonymous users (e.g., public data with enhanced features for logged-in users).
    
    Args:
        credentials: Optional HTTP Bearer token
        db: Database session
    
    Returns:
        CurrentUser if authenticated, None otherwise
    
    Usage:
        @router.get("/public-data")
        async def get_public_data(
            current_user: Optional[CurrentUser] = Depends(get_current_user_optional)
        ):
            if current_user:
                return enhanced_data  # Authenticated user gets more
            return basic_data  # Anonymous user gets basic
    
    Vietnamese: Lay nguoi dung hien tai tuy chon (cho phep anonim)
    """
    if not credentials:
        logger.debug("[OK] Anonymous access -> No credentials provided")
        return None
    
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        logger.debug("[OK] Anonymous access -> Invalid credentials")
        return None
