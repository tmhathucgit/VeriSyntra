# Step 2 COMPLETE: Database Schema - Role Mappings

**Task:** 1.1.3 RBAC - Step 2  
**Date:** November 8, 2025  
**Duration:** 20 minutes  
**Status:** ✅ COMPLETE

---

## Summary

Successfully created the `role_permissions` table and mapped all 6 Vietnamese business roles to their respective permissions. Total of 75 role-permission mappings created with proper foreign key constraints and indexes.

## What Was Done

### 1. Migration File Created

- **File:** `backend/veri_ai_data_inventory/migrations/add_role_permissions_table.sql`
- **Size:** 3,923 bytes
- **Features:**
  - CREATE TABLE with UUID primary key
  - Foreign key reference to `permissions` table
  - UNIQUE constraint on (role, permission_id)
  - Index for fast role lookups
  - Idempotent INSERT statements with ON CONFLICT handling
  - 6 role definitions with Vietnamese comments

### 2. Migration Executed

**Method Used:**
```powershell
.\scripts\run_migration_safe.ps1 -MigrationFile "backend\veri_ai_data_inventory\migrations\add_role_permissions_table.sql"
```

**Results:**
- [OK] CREATE TABLE
- [OK] CREATE INDEX (idx_role_permissions_role)
- [OK] INSERT 0 22 (admin - all permissions)
- [OK] INSERT 0 19 (dpo)
- [OK] INSERT 0 14 (compliance_manager)
- [OK] INSERT 0 8 (staff)
- [OK] INSERT 0 9 (auditor)
- [OK] INSERT 0 3 (viewer)

### 3. Verification Completed

**Role Permission Counts:**
```sql
SELECT role, COUNT(*) as permission_count 
FROM role_permissions 
GROUP BY role 
ORDER BY role;
```

| Role | Vietnamese Name | Permission Count | Status |
|------|----------------|------------------|--------|
| admin | Quản trị viên | 22 | ✓ All permissions |
| auditor | Kiểm toán viên | 9 | ✓ Read-only + audit |
| compliance_manager | Quản lý tuân thủ | 14 | ✓ Compliance ops |
| dpo | Nhân viên bảo vệ dữ liệu | 19 | ✓ DPO authority |
| staff | Nhân viên | 8 | ✓ Basic operations |
| viewer | Người xem | 3 | ✓ Limited read |

**Total Mappings:** 75 role-permission relationships

**Table Structure:**
- role_permission_id (UUID, PK, auto-generated)
- role (VARCHAR(50), NOT NULL)
- permission_id (UUID, FK to permissions table)
- created_at (TIMESTAMP, DEFAULT NOW())

**Constraints:**
- Primary Key: role_permissions_pkey
- Unique Constraint: role_permissions_role_permission_id_key (role, permission_id)
- Foreign Key: role_permissions_permission_id_fkey → permissions(permission_id) ON DELETE CASCADE
- Index: idx_role_permissions_role (btree on role)

### 4. Vietnamese Encoding Verified

**Sample Query:**
```sql
SELECT rp.role, p.permission_name, p.permission_name_vi 
FROM role_permissions rp 
JOIN permissions p ON rp.permission_id = p.permission_id 
WHERE rp.role = 'dpo' 
LIMIT 5;
```

**Results:**
- ✓ Vietnamese diacritics preserved: "Quản lý dữ liệu nhạy cảm"
- ✓ UTF-8 encoding correct: "Xem nhật ký kiểm toán"
- ✓ No character corruption
- ✓ Proper multi-byte storage

## Role Permission Matrix

### Admin (Quản trị viên) - 22 permissions
**All permissions** - Full system access

### DPO (Nhân viên bảo vệ dữ liệu) - 19 permissions
- processing_activity.read, write, delete
- data_category.read, write, manage_sensitive
- ropa.read, generate, approve, export
- data_subject.read, write
- data_recipient.read, write
- security_measure.read, write
- user.read
- audit.read
- analytics.read

### Compliance Manager (Quản lý tuân thủ) - 14 permissions
- processing_activity.read, write
- data_category.read, write
- ropa.read, generate, export
- data_subject.read, write
- data_recipient.read, write
- security_measure.read
- audit.read
- analytics.read

### Staff (Nhân viên) - 8 permissions
- processing_activity.read, write
- data_category.read, write
- ropa.read
- data_subject.read
- data_recipient.read
- security_measure.read

### Auditor (Kiểm toán viên) - 9 permissions
- processing_activity.read
- data_category.read
- ropa.read, export
- data_subject.read
- data_recipient.read
- security_measure.read
- audit.read
- analytics.read

### Viewer (Người xem) - 3 permissions
- processing_activity.read
- data_category.read
- ropa.read

## VeriSyntra Standards Compliance

- ✅ ASCII-only database identifiers (role, permission_id)
- ✅ Vietnamese comments in SQL for role descriptions
- ✅ No emoji characters
- ✅ Proper foreign key constraints with CASCADE delete
- ✅ Idempotent migration (ON CONFLICT DO NOTHING)
- ✅ Performance index on role column
- ✅ UNIQUE constraint prevents duplicate mappings
- ✅ UTF-8 Vietnamese encoding preserved

## Database Integration

**Foreign Key Relationship:**
```
role_permissions (permission_id) 
  → REFERENCES permissions (permission_id) 
  → ON DELETE CASCADE
```

This ensures:
- Permission deletions automatically remove role mappings
- Referential integrity maintained
- No orphaned role-permission records

## Next Step

**Step 3:** Pydantic Schemas (45 min)
- Create `backend/auth/rbac_schemas.py`
- Define permission and role models
- Add bilingual error messages
- Expected completion: November 8, 2025

---

## Verification Queries

**Check all role counts:**
```sql
SELECT role, COUNT(*) FROM role_permissions GROUP BY role;
```

**View DPO permissions:**
```sql
SELECT p.permission_name, p.permission_name_vi 
FROM role_permissions rp 
JOIN permissions p ON rp.permission_id = p.permission_id 
WHERE rp.role = 'dpo';
```

**Verify Vietnamese encoding:**
```sql
SELECT permission_name_vi, 
       LENGTH(permission_name_vi) as chars,
       OCTET_LENGTH(permission_name_vi) as bytes
FROM permissions p
JOIN role_permissions rp ON p.permission_id = rp.permission_id
WHERE rp.role = 'dpo'
LIMIT 5;
-- Expected: bytes > chars for Vietnamese diacritics
```

---

**Checklist:**
- [x] Migration file created
- [x] Migration executed successfully
- [x] 6 roles mapped to permissions
- [x] 75 total role-permission mappings
- [x] Permission counts verified (22, 19, 14, 8, 9, 3)
- [x] Vietnamese encoding preserved
- [x] Foreign key constraints created
- [x] Indexes created
- [x] Table structure validated
- [x] Ready for Step 3 (Pydantic Schemas)

**Status:** Step 2 COMPLETE - Ready to proceed to Step 3
