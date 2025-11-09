"""
Authentication module for VeriAIDPO service.

This module provides JWT token validation and permission checking
for securing VeriAIDPO classification endpoints.
"""

from .jwt_validator import validate_token
from .permissions import require_permission, require_any_permission, require_all_permissions

__all__ = [
    "validate_token",
    "require_permission",
    "require_any_permission",
    "require_all_permissions"
]
