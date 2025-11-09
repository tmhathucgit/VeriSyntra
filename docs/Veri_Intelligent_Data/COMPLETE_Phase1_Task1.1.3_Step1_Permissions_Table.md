# Step 1 COMPLETE: Database Schema - Permissions Table

**Task:** 1.1.3 RBAC - Step 1  
**Date:** November 8, 2025  
**Duration:** 15 minutes + 10 minutes (encoding fix)  
**Status:** ✅ COMPLETE (UTF-8 Encoding Fixed)

---

## Summary

Successfully created the `permissions` table with 22 PDPL-specific permissions, complete with Vietnamese translations and performance indexes. **Vietnamese diacritics properly stored** using UTF-8 encoding after resolving PowerShell pipeline corruption issue.

## Encoding Issue Resolution

**Problem Identified:**
- Initial migration via PowerShell pipeline corrupted Vietnamese diacritics
- **Symptom:** char_count = byte_count (34 = 34) indicated ASCII corruption
- **Expected:** UTF-8 Vietnamese should have byte_count > char_count
- **Root Cause:** PowerShell `Get-Content` pipe to `docker exec` corrupted multi-byte characters

**Solution Applied:**
1. Deleted corrupted data: `DELETE FROM permissions;` (22 rows removed)
2. Copied SQL file to container: `docker cp migrations/add_permissions_table.sql verisyntra-postgres:/tmp/`
3. Executed inside container: `docker exec verisyntra-postgres psql -f /tmp/add_permissions_table.sql`

**Verification Results:**
```
Permission: data_category.write
- permission_name_vi: "Tạo/sửa danh mục dữ liệu" (Vietnamese with proper diacritics)
- char_count: 24 (character count)
- byte_count: 34 (UTF-8 multi-byte encoding)
- Status: ✓ CORRECT (bytes > chars confirms proper Vietnamese diacritics)

Additional verification samples:
- audit.read: 21 chars, 27 bytes (+6 byte difference)
- ropa.approve: 14 chars, 17 bytes (+3 byte difference)
- security_measure.write: 25 chars, 36 bytes (+11 byte difference)
```

**Lesson Learned:** For Windows PowerShell migrations with Vietnamese text:
- ❌ AVOID: `Get-Content file.sql | docker exec -i container psql` (corrupts UTF-8)
- ✓ USE: `docker cp file.sql container:/tmp/ && docker exec container psql -f /tmp/file.sql`

## What Was Done

### 1. Migration File Created
- **File:** `backend/veri_ai_data_inventory/migrations/add_permissions_table.sql`
- **Size:** 91 lines
- **Features:**
  - CREATE TABLE with proper data types
  - 2 indexes for fast lookups
  - 22 permission INSERT statements with Vietnamese names
  - ON CONFLICT handling for idempotency

### 2. Migration Executed (Corrected Method)
```bash
# Step 1: Copy SQL file to container (preserves UTF-8)
docker cp backend/veri_ai_data_inventory/migrations/add_permissions_table.sql verisyntra-postgres:/tmp/add_permissions_table.sql

# Step 2: Execute inside container
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -f /tmp/add_permissions_table.sql
```

**Results:**
- [OK] CREATE TABLE
- [OK] CREATE INDEX (idx_permissions_name)
- [OK] CREATE INDEX (idx_permissions_resource)
- [OK] INSERT 0 22 (22 permissions inserted)

### 3. Verification Completed

**Permission Count:**
```sql
SELECT COUNT(*) FROM permissions;
-- Result: 22 permissions
```

**Vietnamese Diacritics Preserved:**
```sql
SELECT permission_name, permission_name_vi FROM permissions LIMIT 5;
-- Results show proper Vietnamese characters: ạ, ấ, ế, ệ, ị, ộ, ơ, ủ, ư, ứ, ự, ỹ, ỵ, đ
```

**Table Structure:**
- permission_id (UUID, PK, auto-generated)
- permission_name (VARCHAR(100), UNIQUE) - ASCII identifier
- permission_name_vi (VARCHAR(255), NOT NULL) - Vietnamese display name with diacritics
- resource (VARCHAR(50), NOT NULL)
- action (VARCHAR(50), NOT NULL)
- description (TEXT)
- description_vi (TEXT) - Vietnamese description
- created_at (TIMESTAMP, DEFAULT NOW())

**Indexes Created:**
- Primary Key: permissions_pkey (permission_id)
- Unique Constraint: permissions_permission_name_key (permission_name)
- Performance Index: idx_permissions_name (permission_name)
- Performance Index: idx_permissions_resource (resource)

## Permissions Inserted (22 total)

### Processing Activities (3)
- processing_activity.read - Xem hoạt động xử lý
- processing_activity.write - Tạo/sửa hoạt động xử lý
- processing_activity.delete - Xóa hoạt động xử lý

### Data Categories (4)
- data_category.read - Xem danh mục dữ liệu
- data_category.write - Tạo/sửa danh mục dữ liệu
- data_category.delete - Xóa danh mục dữ liệu
- data_category.manage_sensitive - Quản lý dữ liệu nhạy cảm

### ROPA (4)
- ropa.read - Xem ROPA
- ropa.generate - Tạo ROPA
- ropa.approve - Phê duyệt ROPA
- ropa.export - Xuất ROPA

### Data Subjects (2)
- data_subject.read - Xem chủ thể dữ liệu
- data_subject.write - Tạo/sửa chủ thể dữ liệu

### Data Recipients (2)
- data_recipient.read - Xem bên nhận dữ liệu
- data_recipient.write - Tạo/sửa bên nhận dữ liệu

### Security Measures (2)
- security_measure.read - Xem biện pháp bảo mật
- security_measure.write - Tạo/sửa biện pháp bảo mật

### User Management (3)
- user.read - Xem người dùng
- user.write - Tạo/sửa người dùng
- user.delete - Xóa người dùng

### Audit Logs (1)
- audit.read - Xem nhật ký kiểm toán

### Analytics (1)
- analytics.read - Xem phân tích

## VeriSyntra Standards Compliance

- ✅ ASCII-only database identifiers (permission_name, resource, action)
- ✅ Vietnamese diacritics preserved in display fields (permission_name_vi, description_vi)
- ✅ No emoji characters
- ✅ Proper indexing for performance
- ✅ Idempotent migration (ON CONFLICT DO NOTHING)
- ✅ Bilingual support (English description + Vietnamese description_vi)

## Next Step

**Step 2:** Database Schema - Role Mappings (30 min)
- Create `role_permissions` table
- Map 6 roles to permissions
- Expected completion: November 8, 2025

---

**Checklist:**
- [x] Migration file created
- [x] Migration executed successfully
- [x] 22 permissions inserted
- [x] Vietnamese diacritics verified
- [x] Indexes created
- [x] Table structure validated
- [x] Ready for Step 2
