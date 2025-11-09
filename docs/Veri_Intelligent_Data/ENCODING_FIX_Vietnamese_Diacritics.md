# Vietnamese UTF-8 Encoding Fix - Permissions Table

**Date:** November 8, 2025  
**Issue:** Vietnamese diacritics corrupted during database migration  
**Status:** ✓ RESOLVED  

---

## Problem Summary

Vietnamese characters with diacritics were not properly stored in the PostgreSQL `permissions` table during initial migration.

### Detection

**Symptom:** User noticed garbled Vietnamese text in terminal output:
```
Expected: "Tạo/sửa danh mục dữ liệu"
Actual:   "T???o/s???a danh m???c d??? li???u"
```

**Diagnostic Query:**
```sql
SELECT permission_name, 
       length(permission_name_vi) as char_count, 
       octet_length(permission_name_vi) as byte_count 
FROM permissions 
WHERE permission_name = 'data_category.write';
```

**Initial Result (CORRUPTED):**
```
permission_name     | char_count | byte_count
--------------------+------------+-----------
data_category.write |         34 |         34
```

**Analysis:** `char_count = byte_count` indicates single-byte ASCII characters, not multi-byte UTF-8 Vietnamese diacritics.

### Root Cause

**PowerShell Pipeline UTF-8 Corruption:**

```bash
# PROBLEMATIC METHOD (used initially)
Get-Content migrations/add_permissions_table.sql | docker exec -i verisyntra-postgres psql -U verisyntra -d verisyntra
```

**Why it failed:**
- PowerShell `Get-Content` reads file with default encoding
- Pipe to `docker exec -i` converts multi-byte Vietnamese characters to ASCII replacements
- Vietnamese diacritics (ạ, ộ, ệ, ủ, ế, ư) corrupted to question marks or similar

---

## Solution

### Step 1: Delete Corrupted Data

```bash
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "DELETE FROM permissions;"
```

**Result:** Removed 22 corrupted permission records

### Step 2: Copy SQL File to Container

```bash
docker cp backend/veri_ai_data_inventory/migrations/add_permissions_table.sql verisyntra-postgres:/tmp/add_permissions_table.sql
```

**Why this works:** `docker cp` preserves file encoding as-is without conversion

### Step 3: Execute Inside Container

```bash
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -f /tmp/add_permissions_table.sql
```

**Result:** 22 permissions inserted with proper UTF-8 Vietnamese diacritics

---

## Verification

### Byte Count Test (CORRECT)

```sql
SELECT permission_name, 
       length(permission_name_vi) as char_count, 
       octet_length(permission_name_vi) as byte_count 
FROM permissions 
WHERE permission_name = 'data_category.write';
```

**Result:**
```
permission_name     | char_count | byte_count
--------------------+------------+-----------
data_category.write |         24 |         34
```

✓ **CORRECT:** `byte_count > char_count` confirms UTF-8 multi-byte Vietnamese diacritics

### Multiple Entry Verification

```sql
SELECT permission_name, permission_name_vi, 
       length(permission_name_vi) as chars, 
       octet_length(permission_name_vi) as bytes 
FROM permissions 
WHERE permission_name IN ('ropa.approve', 'security_measure.write', 'audit.read') 
ORDER BY permission_name;
```

**Results:**
```
permission_name        | permission_name_vi        | chars | bytes
-----------------------+---------------------------+-------+-------
audit.read             | Xem nhật ký kiểm toán     |    21 |    27  (+6)
ropa.approve           | Phê duyệt ROPA            |    14 |    17  (+3)
security_measure.write | Tạo/sửa biện pháp bảo mật |    25 |    36  (+11)
```

✓ All entries show proper byte overhead for Vietnamese diacritics

---

## Best Practices for Future Migrations

### ❌ AVOID: PowerShell Pipeline

```bash
# DO NOT USE - Corrupts UTF-8
Get-Content file.sql | docker exec -i container psql -U user -d db
```

### ✓ RECOMMENDED: Docker Copy + Execute

```bash
# Method 1: Copy then execute (PREFERRED)
docker cp file.sql container:/tmp/file.sql
docker exec container psql -U user -d db -f /tmp/file.sql

# Method 2: PowerShell with explicit UTF-8 (alternative)
Get-Content -Encoding UTF8 -Raw file.sql | docker exec -i container psql -U user -d db
```

### Verification Template

After any Vietnamese data insertion, verify encoding:

```sql
-- Check a sample Vietnamese field
SELECT 
    your_column,
    length(your_column) as char_count,
    octet_length(your_column) as byte_count
FROM your_table
WHERE your_column LIKE '%ạ%'  -- Contains Vietnamese diacritic
   OR your_column LIKE '%ộ%'
   OR your_column LIKE '%ệ%';

-- Expected: byte_count > char_count
-- If equal: UTF-8 corruption detected
```

---

## VeriSyntra Coding Standard Compliance

✓ **ASCII Identifiers:** `permission_name` uses non-diacritic identifiers (`data_category.write`)  
✓ **Vietnamese UI Fields:** `permission_name_vi` contains proper diacritics (`Tạo/sửa danh mục dữ liệu`)  
✓ **Bilingual Support:** Both English and Vietnamese fields present  
✓ **UTF-8 Storage:** Database properly configured with `server_encoding=UTF8`  
✓ **Data Integrity:** Verified with char/byte length tests  

---

## Impact

**Files Affected:**
- `backend/veri_ai_data_inventory/migrations/add_permissions_table.sql` (source file - no changes needed)
- `permissions` table (22 records re-inserted with correct encoding)
- `docs/Veri_Intelligent_Data/STEP1_COMPLETE_RBAC_Permissions_Table.md` (updated documentation)

**Time Cost:**
- Detection: 5 minutes
- Root cause analysis: 5 minutes
- Fix implementation: 5 minutes
- Verification: 3 minutes
- Documentation: 7 minutes
- **Total:** 25 minutes

**Future Savings:** Prevents similar encoding issues in:
- Step 2: Role-permission mappings (will have Vietnamese role names)
- Future migrations with Vietnamese legal terminology
- PDPL compliance text (Vietnamese law citations)
- User-facing error messages and audit logs
