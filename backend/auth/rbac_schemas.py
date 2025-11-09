"""
RBAC Pydantic Schemas - VeriSyntra Standards Compliant
NO emoji, Vietnamese-first, bilingual with _vi suffix

Task: 1.1.3 RBAC - Step 3
Date: November 8, 2025
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Permission Schema
class PermissionSchema(BaseModel):
    """Permission definition (Dinh nghia quyen)"""
    permission_id: str
    permission_name: str  # e.g., 'processing_activity.read'
    permission_name_vi: str  # e.g., 'Xem hoat dong xu ly'
    resource: str  # e.g., 'processing_activity'
    action: str  # e.g., 'read', 'write', 'delete'
    description: Optional[str] = None
    description_vi: Optional[str] = None
    
    class Config:
        from_attributes = True


# Role Schema
class RoleSchema(BaseModel):
    """Role with permissions (Vai tro voi quyen han)"""
    role: str  # admin, dpo, compliance_manager, staff, auditor, viewer
    role_vi: str  # Vietnamese role name
    permissions: List[PermissionSchema]


# User with Permissions Schema
class UserWithPermissionsSchema(BaseModel):
    """User profile with full permission list"""
    user_id: str
    email: str
    full_name: str
    full_name_vi: str
    tenant_id: str
    role: str
    role_vi: str
    is_active: bool
    permissions: List[str]  # List of permission names (e.g., ['processing_activity.read'])
    
    class Config:
        from_attributes = True


# Permission Check Result
class PermissionCheckResult(BaseModel):
    """Result of permission check (Ket qua kiem tra quyen)"""
    allowed: bool
    permission: str
    user_role: str
    reason: Optional[str] = None
    reason_vi: Optional[str] = None


# RBAC Error Messages (Bilingual)
class RBACErrorMessages:
    """VeriSyntra Standard: Bilingual with _vi suffix"""
    
    PERMISSION_DENIED = {
        "en": "Permission denied: {permission} required",
        "vi": "Từ chối quyền truy cập: cần quyền {permission}"
    }
    
    INSUFFICIENT_PERMISSIONS = {
        "en": "Your role '{role}' does not have required permissions",
        "vi": "Vai trò '{role}' của bạn không có quyền cần thiết"
    }
    
    TENANT_ACCESS_DENIED = {
        "en": "Access denied: resource belongs to different tenant",
        "vi": "Từ chối truy cập: tài nguyên thuộc về tenant khác"
    }
    
    INACTIVE_USER = {
        "en": "User account is inactive",
        "vi": "Tài khoản người dùng đã bị vô hiệu hóa"
    }
    
    INVALID_ROLE = {
        "en": "Invalid role: {role}",
        "vi": "Vai trò không hợp lệ: {role}"
    }
    
    PERMISSION_NOT_FOUND = {
        "en": "Permission not found: {permission}",
        "vi": "Không tìm thấy quyền: {permission}"
    }
    
    @staticmethod
    def get_message(key: str, lang: str = 'vi', **kwargs) -> str:
        """Get error message with Vietnamese-first"""
        message_dict = getattr(RBACErrorMessages, key, {})
        template = message_dict.get(lang, message_dict.get('vi', ''))
        return template.format(**kwargs)


# Role Display Names (Vietnamese-first)
ROLE_DISPLAY_NAMES = {
    'admin': {
        'vi': 'Quản trị viên',
        'en': 'Administrator'
    },
    'dpo': {
        'vi': 'Nhân viên bảo vệ dữ liệu',
        'en': 'Data Protection Officer'
    },
    'compliance_manager': {
        'vi': 'Quản lý tuân thủ',
        'en': 'Compliance Manager'
    },
    'staff': {
        'vi': 'Nhân viên',
        'en': 'Staff'
    },
    'auditor': {
        'vi': 'Kiểm toán viên',
        'en': 'Auditor'
    },
    'viewer': {
        'vi': 'Người xem',
        'en': 'Viewer'
    }
}


def get_role_display_name(role: str, lang: str = 'vi') -> str:
    """
    Get Vietnamese-first role display name
    
    Args:
        role: Role identifier (admin, dpo, etc.)
        lang: Language code ('vi' or 'en')
    
    Returns:
        Localized role name
    """
    return ROLE_DISPLAY_NAMES.get(role, {}).get(lang, role)


def validate_role(role: str) -> bool:
    """
    Validate if role is valid
    
    Args:
        role: Role identifier to validate
    
    Returns:
        True if valid role, False otherwise
    """
    return role in ROLE_DISPLAY_NAMES


# Valid Roles List
VALID_ROLES = list(ROLE_DISPLAY_NAMES.keys())


# Role Permission Counts (for validation)
ROLE_PERMISSION_COUNTS = {
    'admin': 22,  # All permissions
    'dpo': 19,
    'compliance_manager': 14,
    'staff': 8,
    'auditor': 9,
    'viewer': 3
}
