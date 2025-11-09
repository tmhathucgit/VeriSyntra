"""
Permission Checking Dependencies for VeriAIDPO Service

This module provides FastAPI dependencies for checking user permissions
on protected endpoints. Uses JWT token validation to extract permissions
and enforce authorization rules.
"""

from fastapi import HTTPException, Depends
from typing import Callable
from .jwt_validator import validate_token


def require_permission(permission: str) -> Callable:
    """
    Factory function to create a permission checking dependency.
    
    This creates a FastAPI dependency that validates the user has the required
    permission before allowing access to the endpoint. Returns the validated
    user information if permission is granted.
    
    Args:
        permission: The required permission string (e.g., "veriaidpo.classify")
        
    Returns:
        Callable: Async dependency function that checks user permissions
        
    Raises:
        HTTPException: 403 if user lacks required permission
        
    Example:
        ```python
        @router.post("/classify")
        async def classify(
            request: ClassificationRequest,
            user: dict = Depends(require_permission("veriaidpo.classify"))
        ):
            # User has veriaidpo.classify permission
            user_id = user["user_id"]
            tenant_id = user["tenant_id"]
            # Process classification
        ```
    """
    async def permission_checker(user: dict = Depends(validate_token)) -> dict:
        """
        Check if user has the required permission.
        
        Args:
            user: User dict from validate_token containing permissions list
            
        Returns:
            dict: User information if permission granted
            
        Raises:
            HTTPException: 403 with bilingual error if permission denied
        """
        user_permissions = user.get("permissions", [])
        
        # Check if user has required permission
        if permission not in user_permissions:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": f"Permission denied: {permission} required",
                    "error_vi": f"Từ chối quyền truy cập: cần quyền {permission}",
                    "required_permission": permission,
                    "user_role": user.get("role"),
                    "user_permissions": user_permissions
                }
            )
        
        # Permission granted, return user info
        return user
    
    return permission_checker


def require_any_permission(*permissions: str) -> Callable:
    """
    Factory function to create a permission checking dependency that accepts any of the given permissions.
    
    This is useful for endpoints that can be accessed with different permission levels.
    User needs at least ONE of the specified permissions.
    
    Args:
        *permissions: Variable number of permission strings
        
    Returns:
        Callable: Async dependency function that checks user has at least one permission
        
    Raises:
        HTTPException: 403 if user lacks all required permissions
        
    Example:
        ```python
        @router.get("/data")
        async def get_data(
            user: dict = Depends(require_any_permission("data.read", "data.admin"))
        ):
            # User has either data.read OR data.admin permission
        ```
    """
    async def permission_checker(user: dict = Depends(validate_token)) -> dict:
        """
        Check if user has at least one of the required permissions.
        
        Args:
            user: User dict from validate_token containing permissions list
            
        Returns:
            dict: User information if any permission granted
            
        Raises:
            HTTPException: 403 with bilingual error if all permissions denied
        """
        user_permissions = user.get("permissions", [])
        
        # Check if user has at least one required permission
        has_permission = any(perm in user_permissions for perm in permissions)
        
        if not has_permission:
            permissions_str = ", ".join(permissions)
            raise HTTPException(
                status_code=403,
                detail={
                    "error": f"Permission denied: requires one of [{permissions_str}]",
                    "error_vi": f"Từ chối quyền truy cập: cần một trong các quyền [{permissions_str}]",
                    "required_permissions": list(permissions),
                    "user_role": user.get("role"),
                    "user_permissions": user_permissions
                }
            )
        
        # At least one permission granted, return user info
        return user
    
    return permission_checker


def require_all_permissions(*permissions: str) -> Callable:
    """
    Factory function to create a permission checking dependency that requires all given permissions.
    
    User must have ALL of the specified permissions.
    
    Args:
        *permissions: Variable number of permission strings
        
    Returns:
        Callable: Async dependency function that checks user has all permissions
        
    Raises:
        HTTPException: 403 if user lacks any required permission
        
    Example:
        ```python
        @router.delete("/data")
        async def delete_data(
            user: dict = Depends(require_all_permissions("data.read", "data.delete"))
        ):
            # User has BOTH data.read AND data.delete permissions
        ```
    """
    async def permission_checker(user: dict = Depends(validate_token)) -> dict:
        """
        Check if user has all of the required permissions.
        
        Args:
            user: User dict from validate_token containing permissions list
            
        Returns:
            dict: User information if all permissions granted
            
        Raises:
            HTTPException: 403 with bilingual error if any permission denied
        """
        user_permissions = user.get("permissions", [])
        
        # Find missing permissions
        missing_permissions = [perm for perm in permissions if perm not in user_permissions]
        
        if missing_permissions:
            missing_str = ", ".join(missing_permissions)
            permissions_str = ", ".join(permissions)
            raise HTTPException(
                status_code=403,
                detail={
                    "error": f"Permission denied: requires all of [{permissions_str}], missing [{missing_str}]",
                    "error_vi": f"Từ chối quyền truy cập: cần tất cả quyền [{permissions_str}], thiếu [{missing_str}]",
                    "required_permissions": list(permissions),
                    "missing_permissions": missing_permissions,
                    "user_role": user.get("role"),
                    "user_permissions": user_permissions
                }
            )
        
        # All permissions granted, return user info
        return user
    
    return permission_checker
