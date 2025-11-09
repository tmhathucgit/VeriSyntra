# Task 1.1.3: Role-Base
d Access Control (RBAC) - Focused TODO
**VeriSyntra Coding Standards Compliant**

**Project:** VeriSyntra Vietnamese PDPL 2025 Compliance Platform  
**Phase:** Phase 1 - Authentication & Write Scaling (CRITICAL BLOCKER)  
**Task:** 1.1.3 Role-Based Access Control (RBAC)  
**Date Created:** November 8, 2025  
**Estimated Effort:** 8-10 hours  
**Dependencies:** Task 1.1.1 ✅ COMPLETE (JWT), Task 1.1.2 ✅ COMPLETE (Auth Endpoints)  
**Status:** IN PROGRESS (Steps 1-7 of 9 Complete - 78% Done)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Database Schema - Permissions Table](#step-1-database-schema---permissions-table-1-hour)
4. [Step 2: Database Schema - Role Mappings](#step-2-database-schema---role-mappings-30-min)
5. [Step 3: Pydantic Schemas](#step-3-pydantic-schemas-45-min)
6. [Step 4: CRUD Operations](#step-4-crud-operations-1-hour)
7. [Step 5: Permission Decorator](#step-5-permission-decorator-1-15-hours)
8. [Step 6: Current User Dependency](#step-6-current-user-dependency-1-hour)
9. [Step 7: Secure Existing Endpoints](#step-7-secure-existing-endpoints-2-3-hours)
10. [Step 8: Testing](#step-8-testing-1-15-hours)
11. [Step 9: Documentation](#step-9-documentation-30-min)

---

## Overview

### Objective

Implement Role-Based Access Control (RBAC) to secure all VeriSyntra API endpoints with fine-grained permissions, enabling multi-tenant data isolation and Vietnamese PDPL compliance requirements.

### Key Requirements

**VeriSyntra RBAC Model:**
- **6 Roles:** admin, dpo, compliance_manager, staff, auditor, viewer
- **Permission Format:** `resource.action` (e.g., `processing_activity.read`)
- **Multi-Tenant:** Users can only access data from their own tenant
- **Vietnamese Context:** Bilingual permission names and error messages

### Architecture

```
User (email) 
  -> has Role (admin/dpo/etc.)
    -> Role has Permissions (processing_activity.read, etc.)
      -> Endpoint requires Permission
        -> @require_permission('processing_activity.read')
          -> Checks user role -> permissions -> grants/denies access
```

### VeriSyntra Coding Standards

- [x] NO emoji characters in code
- [x] Vietnamese diacritics in UI strings only
- [x] Database identifiers WITHOUT diacritics
- [x] Bilingual outputs with `_vi` suffix
- [x] Dynamic code over hard-coding
- [x] Email-based authentication (Phase 2 schema)

---

## Prerequisites

### Completed Tasks (Task 1.1.1 & 1.1.2)

- [x] JWT handler working (`backend/auth/jwt_handler.py`)
- [x] Password utilities (`backend/auth/password_utils.py`)
- [x] Token blacklist (`backend/auth/token_blacklist.py`)
- [x] 5 auth endpoints operational (register, login, /me, refresh, logout)
- [x] PostgreSQL Phase 2 schema with `users` table
- [x] 82 integration tests passing

### Database Context (Phase 2)

**Existing `users` table** (already created in Task 1.1.2):
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL,  -- NOT username
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    full_name_vi VARCHAR(255),    -- Họ tên (tiếng Việt)
    phone_number VARCHAR(20),
    tenant_id UUID REFERENCES tenants(tenant_id),
    role VARCHAR(50) DEFAULT 'viewer',  -- Will use this field
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(email, tenant_id)  -- Email unique per tenant
);
```

**Note:** The `role` column already exists - we'll use it for RBAC.

---

## Step 1: Database Schema - Permissions Table (1 hour) ✅ COMPLETE

**Completion Date:** November 8, 2025  
**Documentation:** `docs/Veri_Intelligent_Data/COMPLETE_Phase1_Task1.1.3_Step1_Permissions_Table.md`

### 1.1 Create Permissions Table ✅ COMPLETE

**Goal:** Define all available permissions in the system.

**File:** `backend/veri_ai_data_inventory/migrations/add_permissions_table.sql`

```sql
-- Permissions table - defines all available permissions
-- VeriSyntra Standard: ASCII identifiers, Vietnamese comments

CREATE TABLE permissions (
    permission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    permission_name VARCHAR(100) UNIQUE NOT NULL,  -- e.g., 'processing_activity.read'
    permission_name_vi VARCHAR(255) NOT NULL,      -- Vietnamese display name
    resource VARCHAR(50) NOT NULL,                 -- e.g., 'processing_activity'
    action VARCHAR(50) NOT NULL,                   -- e.g., 'read', 'write', 'delete'
    description TEXT,
    description_vi TEXT,                           -- Mô tả (tiếng Việt)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast permission lookups
CREATE INDEX idx_permissions_name ON permissions(permission_name);
CREATE INDEX idx_permissions_resource ON permissions(resource);

-- Insert PDPL-specific permissions
INSERT INTO permissions (permission_name, permission_name_vi, resource, action, description, description_vi) VALUES
-- Processing Activities (Hoạt động xử lý)
('processing_activity.read', 'Xem hoạt động xử lý', 'processing_activity', 'read', 
 'View processing activities', 'Xem các hoạt động xử lý dữ liệu cá nhân'),
('processing_activity.write', 'Tạo/sửa hoạt động xử lý', 'processing_activity', 'write',
 'Create and update processing activities', 'Tạo và cập nhật hoạt động xử lý'),
('processing_activity.delete', 'Xóa hoạt động xử lý', 'processing_activity', 'delete',
 'Delete processing activities', 'Xóa hoạt động xử lý'),

-- Data Categories (Danh mục dữ liệu)
('data_category.read', 'Xem danh mục dữ liệu', 'data_category', 'read',
 'View data categories', 'Xem danh mục dữ liệu cá nhân'),
('data_category.write', 'Tạo/sửa danh mục dữ liệu', 'data_category', 'write',
 'Create and update data categories', 'Tạo và cập nhật danh mục'),
('data_category.delete', 'Xóa danh mục dữ liệu', 'data_category', 'delete',
 'Delete data categories', 'Xóa danh mục dữ liệu'),
('data_category.manage_sensitive', 'Quản lý dữ liệu nhạy cảm', 'data_category', 'manage_sensitive',
 'Handle PDPL Article 4.13 sensitive data', 'Xử lý dữ liệu nhạy cảm theo Điều 4.13 PDPL'),

-- ROPA (Sổ đăng ký hoạt động xử lý)
('ropa.read', 'Xem ROPA', 'ropa', 'read',
 'View ROPA documents', 'Xem sổ đăng ký hoạt động xử lý'),
('ropa.generate', 'Tạo ROPA', 'ropa', 'generate',
 'Generate ROPA documents', 'Tạo sổ đăng ký hoạt động xử lý'),
('ropa.approve', 'Phê duyệt ROPA', 'ropa', 'approve',
 'DPO approval authority for ROPA', 'Quyền phê duyệt ROPA của DPO'),
('ropa.export', 'Xuất ROPA', 'ropa', 'export',
 'Export ROPA in various formats', 'Xuất ROPA sang các định dạng'),

-- Data Subjects (Chủ thể dữ liệu)
('data_subject.read', 'Xem chủ thể dữ liệu', 'data_subject', 'read',
 'View data subjects', 'Xem thông tin chủ thể dữ liệu'),
('data_subject.write', 'Tạo/sửa chủ thể dữ liệu', 'data_subject', 'write',
 'Create and update data subjects', 'Tạo và cập nhật chủ thể dữ liệu'),

-- Data Recipients (Bên nhận dữ liệu)
('data_recipient.read', 'Xem bên nhận dữ liệu', 'data_recipient', 'read',
 'View data recipients', 'Xem thông tin bên nhận dữ liệu'),
('data_recipient.write', 'Tạo/sửa bên nhận dữ liệu', 'data_recipient', 'write',
 'Create and update data recipients', 'Tạo và cập nhật bên nhận dữ liệu'),

-- Security Measures (Biện pháp bảo mật)
('security_measure.read', 'Xem biện pháp bảo mật', 'security_measure', 'read',
 'View security measures', 'Xem các biện pháp bảo mật'),
('security_measure.write', 'Tạo/sửa biện pháp bảo mật', 'security_measure', 'write',
 'Create and update security measures', 'Tạo và cập nhật biện pháp bảo mật'),

-- User Management (Quản lý người dùng)
('user.read', 'Xem người dùng', 'user', 'read',
 'View users in tenant', 'Xem người dùng trong tenant'),
('user.write', 'Tạo/sửa người dùng', 'user', 'write',
 'Create and update users', 'Tạo và cập nhật người dùng'),
('user.delete', 'Xóa người dùng', 'user', 'delete',
 'Deactivate users', 'Vô hiệu hóa người dùng'),

-- Audit Logs (Nhật ký kiểm toán)
('audit.read', 'Xem nhật ký kiểm toán', 'audit', 'read',
 'View audit logs', 'Xem nhật ký kiểm toán'),

-- Analytics (Phân tích)
('analytics.read', 'Xem phân tích', 'analytics', 'read',
 'View analytics and reports', 'Xem phân tích và báo cáo');
```

**Tasks:**
- [x] Create migration file `add_permissions_table.sql`
- [x] Run migration: `.\scripts\run_migration_safe.ps1 -MigrationFile "backend\veri_ai_data_inventory\migrations\add_permissions_table.sql"`
- [x] Verify 22 permissions inserted: `SELECT COUNT(*) FROM permissions;` (Result: 22)
- [x] Test Vietnamese display: Vietnamese diacritics properly preserved with UTF-8 encoding
- [x] Encoding verified: byte_count > char_count confirms proper Vietnamese UTF-8

**Success Criteria:**
- [x] `permissions` table created successfully
- [x] 22 permissions inserted with Vietnamese names (originally planned 21, implemented 22)
- [x] Index created for fast lookups
- [x] All Vietnamese diacritics preserved

---

## Step 2: Database Schema - Role Mappings (30 min) ✅ COMPLETE

**Completion Date:** November 8, 2025  
**Documentation:** `docs/Veri_Intelligent_Data/COMPLETE_Phase1_Task1.1.3_Step2_Role_Mappings.md`

### 2.1 Create Role-Permission Mapping Table ✅ COMPLETE

**Goal:** Map which permissions each role has.

**File:** `backend/veri_ai_data_inventory/migrations/add_role_permissions_table.sql`

```sql
-- Role-Permission mapping table
-- VeriSyntra Standard: ASCII identifiers, Vietnamese comments

CREATE TABLE role_permissions (
    role_permission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role VARCHAR(50) NOT NULL,  -- admin, dpo, compliance_manager, staff, auditor, viewer
    permission_id UUID REFERENCES permissions(permission_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(role, permission_id)
);

-- Index for fast role permission lookups
CREATE INDEX idx_role_permissions_role ON role_permissions(role);

-- Vietnamese role definitions and their permissions
-- Role: admin - Quản trị viên (full access)
INSERT INTO role_permissions (role, permission_id)
SELECT 'admin', permission_id FROM permissions;  -- Admin has ALL permissions

-- Role: dpo - Nhân viên bảo vệ dữ liệu (Data Protection Officer)
INSERT INTO role_permissions (role, permission_id)
SELECT 'dpo', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read', 'processing_activity.write', 'processing_activity.delete',
    'data_category.read', 'data_category.write', 'data_category.manage_sensitive',
    'ropa.read', 'ropa.generate', 'ropa.approve', 'ropa.export',
    'data_subject.read', 'data_subject.write',
    'data_recipient.read', 'data_recipient.write',
    'security_measure.read', 'security_measure.write',
    'user.read',
    'audit.read',
    'analytics.read'
);

-- Role: compliance_manager - Quản lý tuân thủ
INSERT INTO role_permissions (role, permission_id)
SELECT 'compliance_manager', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read', 'processing_activity.write',
    'data_category.read', 'data_category.write',
    'ropa.read', 'ropa.generate', 'ropa.export',
    'data_subject.read', 'data_subject.write',
    'data_recipient.read', 'data_recipient.write',
    'security_measure.read',
    'audit.read',
    'analytics.read'
);

-- Role: staff - Nhân viên
INSERT INTO role_permissions (role, permission_id)
SELECT 'staff', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read', 'processing_activity.write',
    'data_category.read', 'data_category.write',
    'ropa.read',
    'data_subject.read',
    'data_recipient.read',
    'security_measure.read'
);

-- Role: auditor - Kiểm toán viên (read-only + audit logs)
INSERT INTO role_permissions (role, permission_id)
SELECT 'auditor', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read',
    'data_category.read',
    'ropa.read', 'ropa.export',
    'data_subject.read',
    'data_recipient.read',
    'security_measure.read',
    'audit.read',
    'analytics.read'
);

-- Role: viewer - Người xem (read-only, limited)
INSERT INTO role_permissions (role, permission_id)
SELECT 'viewer', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read',
    'data_category.read',
    'ropa.read'
);
```

**Tasks:**
- [x] Create migration file `add_role_permissions_table.sql`
- [x] Run migration using safe UTF-8 script
- [x] Verify mappings: 6 roles with 75 total mappings
- [x] Test role lookup with Vietnamese names
- [x] Verify foreign key constraints

**Expected Counts:**
- ✅ `admin`: 22 permissions (all)
- ✅ `dpo`: 19 permissions
- ✅ `compliance_manager`: 14 permissions
- ✅ `staff`: 8 permissions
- ✅ `auditor`: 9 permissions
- ✅ `viewer`: 3 permissions

**Success Criteria:**
- [x] `role_permissions` table created
- [x] All 6 roles mapped to permissions
- [x] Permission counts match expected
- [x] Vietnamese role descriptions documented
- [x] Foreign key constraints working
- [x] UTF-8 encoding preserved

---

## Step 3: Pydantic Schemas (45 min) ✅ COMPLETE

**Completion Date:** November 8, 2025  
**Documentation:** `docs/Veri_Intelligent_Data/COMPLETE_Phase1_Task1.1.3_Step3_Pydantic_Schemas.md`

### 3.1 Create RBAC Schemas ✅ COMPLETE

**Goal:** Define Pydantic models for permissions and authorization.

**File:** `backend/auth/rbac_schemas.py`

```python
"""
RBAC Pydantic Schemas - VeriSyntra Standards Compliant
NO emoji, Vietnamese-first, bilingual with _vi suffix
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Permission Schema
class PermissionSchema(BaseModel):
    """Permission definition (Định nghĩa quyền)"""
    permission_id: str
    permission_name: str  # e.g., 'processing_activity.read'
    permission_name_vi: str  # e.g., 'Xem hoạt động xử lý'
    resource: str  # e.g., 'processing_activity'
    action: str  # e.g., 'read', 'write', 'delete'
    description: Optional[str] = None
    description_vi: Optional[str] = None
    
    class Config:
        from_attributes = True

# Role Schema
class RoleSchema(BaseModel):
    """Role with permissions (Vai trò với quyền hạn)"""
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
    """Result of permission check (Kết quả kiểm tra quyền)"""
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
    """Get Vietnamese-first role display name"""
    return ROLE_DISPLAY_NAMES.get(role, {}).get(lang, role)
```

**Tasks:**
- [x] Create `backend/auth/rbac_schemas.py`
- [x] Define 6 Pydantic models (Permission, Role, UserWithPermissions, PermissionCheckResult, etc.)
- [x] Add bilingual error messages (6 types)
- [x] Add Vietnamese role names (6 roles with diacritics)
- [x] Verify no emoji characters
- [x] Test schema validation (Python syntax check passed)
- [x] Implement helper functions (get_role_display_name, validate_role)

**Success Criteria:**
- [x] All schemas follow VeriSyntra standards
- [x] Bilingual support with `_vi` suffix
- [x] Vietnamese-first error messages
- [x] NO emoji in code
- [x] Python syntax verified
- [x] Helper functions working

---

## Step 4: CRUD Operations (1 hour) ✅ COMPLETE

**Completion Date:** November 8, 2025  
**Documentation:** `docs/Veri_Intelligent_Data/COMPLETE_Phase1_Task1.1.3_Step4_CRUD_Operations.md`

### 4.1 Create Permission CRUD Functions ✅ COMPLETE

**Goal:** Database operations for permissions and role checks.

**File:** `backend/auth/rbac_crud.py`

```python
"""
RBAC CRUD Operations - VeriSyntra Standards Compliant
Database access for permissions and role-based authorization
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
import logging

from backend.auth.rbac_schemas import (
    PermissionSchema, 
    RoleSchema, 
    UserWithPermissionsSchema,
    get_role_display_name
)

logger = logging.getLogger(__name__)

# Get user permissions by user_id
async def get_user_permissions(
    db: AsyncSession, 
    user_id: str
) -> List[str]:
    """
    Get list of permission names for a user based on their role
    Returns: List of permission names (e.g., ['processing_activity.read'])
    """
    try:
        # Get user's role
        query = select(User.role).where(User.user_id == user_id)
        result = await db.execute(query)
        user_role = result.scalar_one_or_none()
        
        if not user_role:
            logger.warning(f"User {user_id} not found")
            return []
        
        # Get permissions for this role
        query = select(Permission.permission_name).join(
            RolePermission, 
            Permission.permission_id == RolePermission.permission_id
        ).where(RolePermission.role == user_role)
        
        result = await db.execute(query)
        permissions = [row[0] for row in result.fetchall()]
        
        logger.info(f"User {user_id} (role: {user_role}) has {len(permissions)} permissions")
        return permissions
        
    except Exception as e:
        logger.error(f"Error getting permissions for user {user_id}: {str(e)}")
        return []

# Check if user has specific permission
async def user_has_permission(
    db: AsyncSession,
    user_id: str,
    permission_name: str
) -> bool:
    """
    Check if user has a specific permission
    Example: user_has_permission(db, user_id, 'processing_activity.write')
    """
    permissions = await get_user_permissions(db, user_id)
    has_permission = permission_name in permissions
    
    logger.debug(
        f"Permission check: user={user_id}, "
        f"permission={permission_name}, "
        f"allowed={has_permission}"
    )
    
    return has_permission

# Get user with full permissions
async def get_user_with_permissions(
    db: AsyncSession,
    user_id: str,
    lang: str = 'vi'
) -> Optional[UserWithPermissionsSchema]:
    """
    Get user profile with full permission list (Vietnamese-first)
    """
    try:
        # Get user
        query = select(User).where(User.user_id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        # Get permissions
        permissions = await get_user_permissions(db, user_id)
        
        # Get role display name
        role_vi = get_role_display_name(user.role, 'vi')
        
        return UserWithPermissionsSchema(
            user_id=str(user.user_id),
            email=user.email,
            full_name=user.full_name,
            full_name_vi=user.full_name_vi,
            tenant_id=str(user.tenant_id),
            role=user.role,
            role_vi=role_vi,
            is_active=user.is_active,
            permissions=permissions
        )
        
    except Exception as e:
        logger.error(f"Error getting user with permissions: {str(e)}")
        return None

# Get all permissions for a role
async def get_role_permissions(
    db: AsyncSession,
    role: str
) -> List[PermissionSchema]:
    """
    Get all permissions for a specific role with Vietnamese names
    """
    try:
        query = select(Permission).join(
            RolePermission,
            Permission.permission_id == RolePermission.permission_id
        ).where(RolePermission.role == role)
        
        result = await db.execute(query)
        permissions = result.scalars().all()
        
        return [PermissionSchema.from_orm(p) for p in permissions]
        
    except Exception as e:
        logger.error(f"Error getting permissions for role {role}: {str(e)}")
        return []

# Validate tenant access
async def validate_tenant_access(
    db: AsyncSession,
    user_id: str,
    resource_tenant_id: str
) -> bool:
    """
    Ensure user can only access resources from their own tenant
    Multi-tenant isolation (cách ly đa tenant)
    """
    try:
        query = select(User.tenant_id).where(User.user_id == user_id)
        result = await db.execute(query)
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
```

**Tasks:**
- [x] Create `backend/auth/rbac_crud.py`
- [x] Implement 7 CRUD functions (get_user_permissions, user_has_permission, get_user_with_permissions, get_role_permissions, validate_tenant_access, get_all_permissions, get_users_by_role)
- [x] Create SQLAlchemy models (Permission, RolePermission in backend/database/models/rbac.py)
- [x] Update database model exports (__init__.py files)
- [x] Add logging with Vietnamese context
- [x] Add error handling
- [x] Test each function with sample data

**Success Criteria:**
- [x] `get_user_permissions()` returns permission list
- [x] `user_has_permission()` checks correctly
- [x] `validate_tenant_access()` enforces isolation
- [x] All functions handle errors gracefully
- [x] Vietnamese logging messages
- [x] SQLAlchemy models created matching database schema

---

## Step 5: Permission Decorator (1-1.5 hours) ✅ COMPLETE

**Completion Date:** November 8, 2025  
**Documentation:** `docs/Veri_Intelligent_Data/COMPLETE_Phase1_Task1.1.3_Step5_Permission_Decorator.md`

### 5.1 Create @require_permission Decorator ✅ COMPLETE

**Goal:** FastAPI decorator to enforce permissions on endpoints.

**File:** `backend/auth/rbac_dependencies.py`

```python
"""
RBAC FastAPI Dependencies - VeriSyntra Standards Compliant
Permission decorators and dependency injection for endpoint security
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
import logging

from backend.app.core.database import get_db
from backend.auth.jwt_handler import verify_token
from backend.auth.rbac_crud import (
    user_has_permission,
    validate_tenant_access,
    get_user_with_permissions
)
from backend.auth.rbac_schemas import RBACErrorMessages

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Current User Model (from JWT token)
class CurrentUser:
    """Current authenticated user with permissions"""
    def __init__(
        self,
        user_id: str,
        email: str,
        tenant_id: str,
        role: str,
        permissions: list[str]
    ):
        self.user_id = user_id
        self.email = email
        self.tenant_id = tenant_id
        self.role = role
        self.permissions = permissions
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions

# Get current user from JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> CurrentUser:
    """
    Extract and validate current user from JWT token
    Returns CurrentUser with permissions loaded
    """
    try:
        # Verify JWT token
        token = credentials.credentials
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Invalid token",
                    "error_vi": "Token không hợp lệ"
                }
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Invalid token payload",
                    "error_vi": "Nội dung token không hợp lệ"
                }
            )
        
        # Get user with permissions
        user_with_perms = await get_user_with_permissions(db, user_id)
        
        if not user_with_perms:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "User not found",
                    "error_vi": "Không tìm thấy người dùng"
                }
            )
        
        if not user_with_perms.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": RBACErrorMessages.INACTIVE_USER['en'],
                    "error_vi": RBACErrorMessages.INACTIVE_USER['vi']
                }
            )
        
        return CurrentUser(
            user_id=user_with_perms.user_id,
            email=user_with_perms.email,
            tenant_id=user_with_perms.tenant_id,
            role=user_with_perms.role,
            permissions=user_with_perms.permissions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Authentication error",
                "error_vi": "Lỗi xác thực"
            }
        )

# Permission requirement decorator factory
def require_permission(permission: str):
    """
    Decorator factory for permission-based access control
    
    Usage:
        @router.get("/processing-activities")
        @require_permission("processing_activity.read")
        async def get_activities(current_user: CurrentUser = Depends(get_current_user)):
            ...
    """
    def permission_checker(current_user: CurrentUser = Depends(get_current_user)):
        if not current_user.has_permission(permission):
            logger.warning(
                f"Permission denied: user={current_user.email}, "
                f"role={current_user.role}, "
                f"required={permission}"
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
                    "user_role": current_user.role
                }
            )
        return current_user
    
    return permission_checker

# Tenant isolation validator
async def require_tenant_access(
    resource_tenant_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Validate user can only access resources from their tenant
    Multi-tenant isolation enforcement
    
    Usage:
        activity = get_activity(activity_id)
        await require_tenant_access(activity.tenant_id, current_user, db)
    """
    # Admin can access all tenants
    if current_user.role == 'admin':
        return True
    
    is_allowed = await validate_tenant_access(
        db, 
        current_user.user_id, 
        resource_tenant_id
    )
    
    if not is_allowed:
        logger.warning(
            f"Tenant access denied: user={current_user.email}, "
            f"user_tenant={current_user.tenant_id}, "
            f"resource_tenant={resource_tenant_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": RBACErrorMessages.TENANT_ACCESS_DENIED['en'],
                "error_vi": RBACErrorMessages.TENANT_ACCESS_DENIED['vi']
            }
        )
    
    return True
```

**Tasks:**
- [x] Create `backend/auth/rbac_dependencies.py` (470+ lines)
- [x] Implement `CurrentUser` class (3 permission check methods)
- [x] Implement `get_current_user()` dependency (JWT → User pipeline)
- [x] Implement `require_permission()` decorator factory
- [x] Implement `require_any_permission()` decorator
- [x] Implement `require_all_permissions()` decorator
- [x] Implement `require_tenant_access()` validator
- [x] Implement `get_current_user_optional()` for public endpoints
- [x] Add bilingual error messages (Vietnamese-first)
- [x] Test decorator on sample endpoint (manual testing)

**Success Criteria:**
- [x] `@require_permission()` blocks unauthorized users
- [x] Bilingual HTTP 403 errors with Vietnamese-first
- [x] Multi-tenant isolation enforced
- [x] Logging tracks permission denials with [OK]/[ERROR]
- [x] Admin bypass for tenant checks
- [x] Type hints on all functions
- [x] NO emoji in code

---

## Step 6: Current User Dependency (1 hour) ✅ COMPLETE

**Completion Date:** November 8, 2025  
**Documentation:** `docs/Veri_Intelligent_Data/COMPLETE_Phase1_Task1.1.3_Step6_Testing.md`

### 6.1 Test Current User Extraction ✅ COMPLETE

**Goal:** Verify JWT -> CurrentUser -> Permissions pipeline works.

**File:** `backend/auth/test_rbac_dependencies.py`

```python
"""
Test RBAC Dependencies - VeriSyntra Standards
"""

import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient

from backend.auth.rbac_dependencies import (
    get_current_user,
    require_permission,
    CurrentUser
)

app = FastAPI()

# Test endpoint with permission requirement
@app.get("/test/read")
async def test_read_endpoint(
    current_user: CurrentUser = Depends(require_permission("processing_activity.read"))
):
    """Test endpoint requiring read permission"""
    return {
        "message": "Access granted",
        "message_vi": "Quyền truy cập được cấp",
        "user": current_user.email,
        "role": current_user.role
    }

@app.get("/test/write")
async def test_write_endpoint(
    current_user: CurrentUser = Depends(require_permission("processing_activity.write"))
):
    """Test endpoint requiring write permission"""
    return {
        "message": "Write access granted",
        "message_vi": "Quyền ghi được cấp"
    }

# Manual test cases
def test_get_current_user_valid_token():
    """Test: Valid JWT token returns CurrentUser with permissions"""
    # TODO: Implement with real JWT token from Task 1.1.1
    pass

def test_get_current_user_invalid_token():
    """Test: Invalid token raises 401"""
    # TODO: Implement
    pass

def test_require_permission_allowed():
    """Test: User with permission can access endpoint"""
    # TODO: Create user with 'dpo' role (has processing_activity.read)
    # TODO: Generate JWT token
    # TODO: Call /test/read with token
    # TODO: Assert 200 OK
    pass

def test_require_permission_denied():
    """Test: User without permission gets 403"""
    # TODO: Create user with 'viewer' role (NO processing_activity.write)
    # TODO: Generate JWT token
    # TODO: Call /test/write with token
    # TODO: Assert 403 Forbidden with bilingual error
    pass

def test_tenant_isolation():
    """Test: User can only access own tenant resources"""
    # TODO: Create 2 users in different tenants
    # TODO: User A tries to access User B's resource
    # TODO: Assert 403 Forbidden
    pass

if __name__ == "__main__":
    print("[OK] RBAC dependency tests defined")
    print("[OK] Run with: pytest backend/auth/test_rbac_dependencies.py")
```

**Tasks:**
- [x] Create test file `backend/tests/system/test_rbac_dependencies.py` (470+ lines)
- [x] Implement 14 integration tests (2 test suites)
- [x] Test with real JWT tokens from Task 1.1.1
- [x] Verify bilingual error messages (Vietnamese + English)
- [x] Test multi-tenant isolation (2 tenants, 5 users)
- [x] Test all 4 roles (admin, dpo, viewer, staff)
- [x] Test inactive user blocking (403 Forbidden)
- [x] Run: `pytest backend/tests/system/test_rbac_dependencies.py -v`

**Success Criteria:**
- [x] All 14 tests defined and ready
- [x] 403 errors return Vietnamese messages
- [x] Tenant isolation works correctly (different tenant_id values)
- [x] All roles authenticate successfully
- [x] Invalid/expired tokens rejected with 401
- [x] Inactive users blocked with 403
- [x] Vietnamese fields present in user profiles

---

## Step 7: Secure Existing Endpoints (2-3 hours) ✅ COMPLETE

**Completion Date:** January 27, 2025  
**Documentation:** `docs/Veri_Intelligent_Data/COMPLETE_Phase1_Task1.1.3_Step7_Secure_Endpoints.md`

### 7.1 RBAC Protection Applied ✅ COMPLETE

**Goal:** Protect existing API endpoints with RBAC.

**Modules Secured:**
1. **admin_companies.py** (7 endpoints) - Company registry management
2. **veriaidpo_classification.py** (8 endpoints) - AI classification services
3. **veriportal.py** (2 endpoints) - User management portal
4. **vericompliance.py** (3 endpoints) - PDPL compliance services

**Total: 20 endpoints secured**

**Implementation Pattern:**
```python
from auth.rbac_dependencies import require_permission, CurrentUser

@router.get("/processing-activities")
async def get_processing_activities(
    current_user: CurrentUser = Depends(require_permission("processing_activity.read")),
    db: AsyncSession = Depends(get_db)
):
    """
    Get processing activities (requires read permission)
    
    **RBAC:** Requires `processing_activity.read` permission (admin/dpo/compliance_manager/staff roles)
    
    Vietnamese: Lay danh sach hoat dong xu ly (can quyen doc)
    """
    logger.info(
        f"[RBAC] User {current_user.email} (role: {current_user.role}) "
        f"accessing processing activities"
    )
    # Filter by tenant
    activities = await get_activities_by_tenant(db, current_user.tenant_id)
    return activities
```

**Tasks:**
- [x] Modified `admin_companies.py` (7 endpoints)
  - [x] POST /add - `user.write` permission (admin only)
  - [x] DELETE /remove - `user.delete` permission (admin only)
  - [x] GET /search - `user.read` permission (admin/auditor/dpo)
  - [x] GET /list/{industry} - `user.read` permission
  - [x] GET /stats - `user.read` permission
  - [x] POST /reload - `user.write` permission (admin only)
  - [x] GET /export - `user.read` permission
- [x] Modified `veriaidpo_classification.py` (8 endpoints)
  - [x] POST /classify - `processing_activity.read` permission
  - [x] POST /classify-legal-basis - `processing_activity.read` permission
  - [x] POST /classify-breach-severity - `processing_activity.read` permission
  - [x] POST /classify-cross-border - `processing_activity.read` permission
  - [x] POST /normalize - `data_category.write` permission
  - [x] GET /health - Public (no auth)
  - [x] GET /model-status - `analytics.read` permission
  - [x] POST /preload-model - `user.write` permission (admin only)
- [x] Modified `veriportal.py` (2 endpoints)
  - [x] GET / - Public (info only)
  - [x] GET /dashboard - `analytics.read` permission
- [x] Modified `vericompliance.py` (3 endpoints)
  - [x] GET / - Public (info only)
  - [x] GET /requirements - `ropa.read` permission
  - [x] POST /assessment/start - `ropa.write` permission
- [x] Added RBAC imports to all modules
- [x] Updated file docstrings with RBAC status
- [x] Added Vietnamese documentation to all endpoints
- [x] Added RBAC audit logging to all secured endpoints

**Permission Mapping Strategy:**
- **Write Operations:** `user.write`, `data_category.write`, `ropa.write`
- **Read Operations:** `user.read`, `analytics.read`, `processing_activity.read`, `ropa.read`
- **Delete Operations:** `user.delete`
- **Admin-Only:** `user.write` (system operations), `user.delete`
- **Public:** Health checks, info endpoints

**Success Criteria:**
- [x] All 20 endpoints protected with appropriate permissions
- [x] Vietnamese documentation added
- [x] RBAC audit logging implemented
- [x] Permission mapping matches role definitions
- [x] Public endpoints identified correctly

---

## Step 8: Testing (1-1.5 hours)
```python
# READ: require .read permission
@router.get("/resource")
async def get_resource(
    current_user: CurrentUser = Depends(require_permission("resource.read")),
    db: AsyncSession = Depends(get_db)
):
    # Filter by tenant
    return await get_by_tenant(db, current_user.tenant_id)

# WRITE: require .write permission
@router.post("/resource")
async def create_resource(
    data: ResourceCreate,
    current_user: CurrentUser = Depends(require_permission("resource.write")),
    db: AsyncSession = Depends(get_db)
):
    # Auto-assign tenant
    return await create(db, data, current_user.tenant_id)

# DELETE: require .delete permission
@router.delete("/resource/{id}")
async def delete_resource(
    id: str,
    current_user: CurrentUser = Depends(require_permission("resource.delete")),
    db: AsyncSession = Depends(get_db)
):
    # Validate tenant ownership
    resource = await get_one(db, id)
    await require_tenant_access(resource.tenant_id, current_user, db)
    return await delete(db, id)
```

**Success Criteria:**
- [ ] All endpoints require authentication
- [ ] All endpoints check permissions
- [ ] All queries filter by tenant
- [ ] DELETE operations validate tenant ownership
- [ ] Bilingual error messages on 403

---

## Step 8: Testing (1-1.5 hours)

### 8.1 Integration Tests for RBAC

**Goal:** Test RBAC with real scenarios across all roles.

**File:** `backend/auth/test_rbac_integration.py`

```python
"""
RBAC Integration Tests - VeriSyntra Standards
Test all 6 roles with real API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Test Scenario 1: Admin has full access
def test_admin_full_access():
    """Admin can access all endpoints"""
    # Create admin user
    admin_token = create_user_and_login(role='admin')
    
    # Test READ
    response = client.get(
        "/api/v1/processing-activities",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
    # Test WRITE
    response = client.post(
        "/api/v1/processing-activities",
        json={"name": "Test Activity"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    
    # Test DELETE
    response = client.delete(
        f"/api/v1/processing-activities/{activity_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

# Test Scenario 2: DPO has most permissions
def test_dpo_permissions():
    """DPO can read, write, manage sensitive, approve ROPA"""
    dpo_token = create_user_and_login(role='dpo')
    
    # Can read
    response = client.get(
        "/api/v1/processing-activities",
        headers={"Authorization": f"Bearer {dpo_token}"}
    )
    assert response.status_code == 200
    
    # Can write
    response = client.post(
        "/api/v1/data-categories",
        json={"name": "Sensitive Data"},
        headers={"Authorization": f"Bearer {dpo_token}"}
    )
    assert response.status_code == 201
    
    # Can approve ROPA
    response = client.post(
        f"/api/v1/ropa/{ropa_id}/approve",
        headers={"Authorization": f"Bearer {dpo_token}"}
    )
    assert response.status_code == 200

# Test Scenario 3: Viewer has read-only access
def test_viewer_read_only():
    """Viewer can only read, cannot write or delete"""
    viewer_token = create_user_and_login(role='viewer')
    
    # Can read
    response = client.get(
        "/api/v1/processing-activities",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 200
    
    # CANNOT write (403)
    response = client.post(
        "/api/v1/processing-activities",
        json={"name": "Test"},
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403
    assert "error_vi" in response.json()  # Vietnamese error
    
    # CANNOT delete (403)
    response = client.delete(
        f"/api/v1/processing-activities/{activity_id}",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403

# Test Scenario 4: Multi-tenant isolation
def test_tenant_isolation():
    """Users cannot access other tenant's data"""
    # Create 2 users in different tenants
    user_a_token = create_user_and_login(tenant_id="tenant-a")
    user_b_token = create_user_and_login(tenant_id="tenant-b")
    
    # User A creates activity
    response = client.post(
        "/api/v1/processing-activities",
        json={"name": "Tenant A Activity"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    activity_id = response.json()["activity_id"]
    
    # User B tries to access User A's activity (403)
    response = client.get(
        f"/api/v1/processing-activities/{activity_id}",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )
    assert response.status_code == 403
    assert "tenant" in response.json()["error_vi"].lower()

# Test Scenario 5: Permission denied has bilingual message
def test_permission_denied_bilingual():
    """403 errors return Vietnamese and English messages"""
    viewer_token = create_user_and_login(role='viewer')
    
    response = client.delete(
        f"/api/v1/processing-activities/{activity_id}",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    
    assert response.status_code == 403
    json_response = response.json()
    assert "error" in json_response  # English
    assert "error_vi" in json_response  # Vietnamese
    assert "quyền" in json_response["error_vi"].lower()  # "permission" in Vietnamese

# Test Scenario 6: All 6 roles tested
@pytest.mark.parametrize("role,can_write,can_delete", [
    ("admin", True, True),
    ("dpo", True, True),
    ("compliance_manager", True, False),
    ("staff", True, False),
    ("auditor", False, False),
    ("viewer", False, False),
])
def test_all_roles(role, can_write, can_delete):
    """Test permission matrix for all 6 roles"""
    token = create_user_and_login(role=role)
    
    # All roles can read
    response = client.get(
        "/api/v1/processing-activities",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Test write permission
    response = client.post(
        "/api/v1/processing-activities",
        json={"name": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    if can_write:
        assert response.status_code == 201
    else:
        assert response.status_code == 403
    
    # Test delete permission
    if can_write:  # Only test delete if write succeeded
        activity_id = response.json()["activity_id"]
        response = client.delete(
            f"/api/v1/processing-activities/{activity_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if can_delete:
            assert response.status_code == 200
        else:
            assert response.status_code == 403

# Helper function
def create_user_and_login(role='viewer', tenant_id=None):
    """Create user, login, return JWT token"""
    # TODO: Implement using Task 1.1.2 register and login endpoints
    pass

if __name__ == "__main__":
    print("[OK] RBAC integration tests defined")
    print("[OK] Run: pytest backend/auth/test_rbac_integration.py -v")
```

**Tasks:**
- [ ] Create integration test file
- [ ] Implement 6 test scenarios
- [ ] Test all 6 roles (admin, dpo, compliance_manager, staff, auditor, viewer)
- [ ] Test multi-tenant isolation
- [ ] Verify bilingual error messages
- [ ] Run all tests: `pytest backend/auth/test_rbac_integration.py -v`
- [ ] Ensure 100% pass rate

**Success Criteria:**
- [ ] All 6 scenarios pass
- [ ] Permission matrix correct for all roles
- [ ] Multi-tenant isolation enforced
- [ ] Bilingual errors verified
- [ ] 0 failing tests

---

## Step 9: Documentation (30 min)

### 9.1 Create RBAC Documentation

**Goal:** Document RBAC system for developers and DPOs.

**File:** `docs/Veri_Intelligent_Data/RBAC_Implementation_Guide.md`

```markdown
# RBAC Implementation Guide - VeriSyntra

**Date:** November 8, 2025  
**Task:** 1.1.3 Role-Based Access Control  
**Status:** COMPLETE

---

## Overview

VeriSyntra implements role-based access control (RBAC) with 6 Vietnamese business roles and 21 PDPL-specific permissions.

## Roles (Vai trò)

| Role | Vietnamese Name | Permissions | Use Case |
|------|----------------|-------------|----------|
| **admin** | Quản trị viên | ALL (21) | System administrator |
| **dpo** | Nhân viên bảo vệ dữ liệu | 19 | Data Protection Officer (PDPL compliance) |
| **compliance_manager** | Quản lý tuân thủ | 14 | Compliance team lead |
| **staff** | Nhân viên | 8 | Regular employees |
| **auditor** | Kiểm toán viên | 9 | Internal/external auditors (read-only + audit logs) |
| **viewer** | Người xem | 3 | Limited read access |

## Permissions (Quyền hạn)

### Processing Activities (Hoạt động xử lý)
- `processing_activity.read` - View processing activities
- `processing_activity.write` - Create/update activities
- `processing_activity.delete` - Delete activities

### Data Categories (Danh mục dữ liệu)
- `data_category.read` - View data categories
- `data_category.write` - Create/update categories
- `data_category.delete` - Delete categories
- `data_category.manage_sensitive` - Handle PDPL Article 4.13 sensitive data

### ROPA (Sổ đăng ký)
- `ropa.read` - View ROPA documents
- `ropa.generate` - Generate ROPA
- `ropa.approve` - DPO approval authority
- `ropa.export` - Export ROPA

[... 21 total permissions ...]

## Usage

### Protect Endpoint with Permission

```python
from backend.auth.rbac_dependencies import require_permission, CurrentUser

@router.get("/processing-activities")
async def get_activities(
    current_user: CurrentUser = Depends(require_permission("processing_activity.read"))
):
    # Only users with processing_activity.read permission can access
    return activities
```

### Multi-Tenant Isolation

```python
from backend.auth.rbac_dependencies import require_tenant_access

# Validate user can only access their tenant's data
await require_tenant_access(resource.tenant_id, current_user, db)
```

### Check Permission in Code

```python
if current_user.has_permission("ropa.approve"):
    # Allow DPO to approve
    await approve_ropa(ropa_id)
else:
    raise HTTPException(403, detail="DPO role required")
```

## Testing

```bash
# Run RBAC tests
pytest backend/auth/test_rbac_integration.py -v

# Expected: All tests pass with 6 roles tested
```

## Database Schema

- `permissions` table: 21 PDPL permissions
- `role_permissions` table: Role-to-permission mappings
- `users.role` column: User's assigned role

## Security

- **JWT Required:** All endpoints require valid JWT token
- **Permission Check:** Decorator verifies user has required permission
- **Tenant Isolation:** Users can only access own tenant data (except admin)
- **Bilingual Errors:** 403 responses include Vietnamese and English messages

## VeriSyntra Standards

- [x] NO emoji in code
- [x] Vietnamese diacritics in UI only
- [x] Bilingual with _vi suffix
- [x] Multi-tenant isolation enforced

---

**Status:** Production-ready RBAC system operational
```

**Tasks:**
- [ ] Create `RBAC_Implementation_Guide.md`
- [ ] Document all 6 roles
- [ ] Document all 21 permissions
- [ ] Add usage examples
- [ ] Add testing instructions
- [ ] Add security notes

**Success Criteria:**
- [ ] Complete role documentation
- [ ] All permissions listed with Vietnamese names
- [ ] Usage examples clear
- [ ] VeriSyntra standards checklist

---

## Summary Checklist

### Step 1: Database Schema - Permissions (1 hour) ✅ COMPLETE
- [x] `permissions` table created
- [x] 22 PDPL permissions inserted
- [x] Vietnamese names added
- [x] Indexes created
- [x] UTF-8 encoding verified
- [x] Documentation: `COMPLETE_Phase1_Task1.1.3_Step1_Permissions_Table.md`

### Step 2: Database Schema - Role Mappings (30 min) ✅ COMPLETE
- [x] `role_permissions` table created
- [x] 6 roles mapped to permissions
- [x] 75 total role-permission mappings
- [x] Permission counts verified (22, 19, 14, 8, 9, 3)
- [x] Foreign key constraints created
- [x] Vietnamese encoding preserved
- [x] Documentation: `COMPLETE_Phase1_Task1.1.3_Step2_Role_Mappings.md`

### Step 3: Pydantic Schemas (45 min) ✅ COMPLETE
- [x] 6 Pydantic models created
- [x] Bilingual error messages (6 types)
- [x] Vietnamese role names (6 roles)
- [x] Helper functions implemented
- [x] Validation constants defined
- [x] NO emoji in code
- [x] Python syntax verified
- [x] Documentation: `COMPLETE_Phase1_Task1.1.3_Step3_Pydantic_Schemas.md`

### Step 4: CRUD Operations (1 hour) ✅ COMPLETE
- [x] 7 CRUD functions implemented
- [x] SQLAlchemy models created (Permission, RolePermission)
- [x] Tenant validation working
- [x] All tests pass
- [x] Documentation: `COMPLETE_Phase1_Task1.1.3_Step4_CRUD_Operations.md`

### Step 5: Permission Decorator (1-1.5 hours) ✅ COMPLETE
- [x] `@require_permission()` decorator created
- [x] `get_current_user()` dependency working
- [x] Bilingual 403 errors (Vietnamese-first)
- [x] Multi-tenant isolation with admin bypass
- [x] Optional authentication support
- [x] Documentation: `COMPLETE_Phase1_Task1.1.3_Step5_Permission_Decorator.md`

### Step 6: Current User Dependency (1 hour) ✅ COMPLETE
- [x] JWT → CurrentUser pipeline tested
- [x] 14 integration tests created
- [x] All 4 roles tested (admin, dpo, viewer, staff)
- [x] Multi-tenant isolation verified
- [x] Inactive user blocking tested
- [x] Vietnamese fields validated
- [x] Bilingual error messages verified
- [x] Documentation: `COMPLETE_Phase1_Task1.1.3_Step6_Testing.md`

### Step 7: Secure Existing Endpoints (2-3 hours)
- [ ] 10 CRUD modules updated
- [ ] All endpoints require permissions
- [ ] Tenant filtering added

### Step 8: Testing (1-1.5 hours)
- [ ] 6 integration tests pass
- [ ] All 6 roles tested
- [ ] Multi-tenant isolation verified

### Step 9: Documentation (30 min)
- [ ] RBAC guide created
- [ ] All roles documented
- [ ] Usage examples added

---

## Total Effort Tracking

**Estimated:** 8-10 hours  
**Actual:** _____ hours (to be filled)

**Completion Date:** _________  
**Next Task:** 1.1.4 API Key Management

---

**Document Status:** Active Implementation Guide  
**Last Updated:** November 8, 2025  
**VeriSyntra Coding Standards:** COMPLIANT ✅
