# Vietnamese UTF-8 Migration - Quick Reference

## TL;DR

**Always use this for Vietnamese database migrations:**

```powershell
.\scripts\run_migration_safe.ps1 -MigrationFile "path\to\migration.sql"
```

---

## Why?

PowerShell pipes corrupt Vietnamese UTF-8:
```
Vietnamese:  "Tạo/sửa danh mục dữ liệu"
PowerShell:  "T???o/s???a danh m???c d??? li???u" ❌
Safe Script: "Tạo/sửa danh mục dữ liệu" ✓
```

---

## Quick Start

```powershell
# 1. Navigate to VeriSyntra root
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra

# 2. Run migration
.\scripts\run_migration_safe.ps1 -MigrationFile "backend\veri_ai_data_inventory\migrations\your_migration.sql"

# 3. Verify output shows:
# [OK] Vietnamese diacritics detected in file
# [OK] Migration executed successfully
# [OK] Encoding: UTF-8 with Vietnamese
```

---

## Verify Encoding After Migration

```sql
-- Check if Vietnamese UTF-8 is correct
SELECT 
    column_name,
    column_name_vi,
    length(column_name_vi) as chars,
    octet_length(column_name_vi) as bytes
FROM your_table
LIMIT 5;

-- Expected: bytes > chars for Vietnamese diacritics
-- If bytes = chars for ALL entries, UTF-8 was corrupted
```

---

## DO / DON'T

### ✓ DO

```powershell
# Use safe migration script
.\scripts\run_migration_safe.ps1 -MigrationFile "migration.sql"

# Manual alternative (docker cp)
docker cp migration.sql verisyntra-postgres:/tmp/migration.sql
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -f /tmp/migration.sql
```

### ❌ DON'T

```powershell
# NEVER use PowerShell pipe - corrupts Vietnamese
Get-Content migration.sql | docker exec -i verisyntra-postgres psql -U verisyntra -d verisyntra
```

---

## Troubleshooting

### Script not found?

```powershell
# Make sure you're in VeriSyntra root directory
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra

# Verify script exists
Test-Path .\scripts\run_migration_safe.ps1
```

### Container not running?

```powershell
# Start PostgreSQL container
docker-compose up -d postgres

# Verify running
docker ps | Select-String verisyntra-postgres
```

### Encoding looks corrupted?

```sql
-- Find corrupted entries (chars = bytes when Vietnamese expected)
SELECT permission_name, permission_name_vi, 
       length(permission_name_vi) as chars,
       octet_length(permission_name_vi) as bytes
FROM permissions
WHERE permission_name_vi ~ '[\?]';  -- Contains question marks

-- Fix: Delete and re-run with safe script
DELETE FROM permissions;
-- Then use: .\scripts\run_migration_safe.ps1 -MigrationFile "migration.sql"
```

---

## Full Documentation

- **Script Details:** `scripts/README.md`
- **Encoding Analysis:** `docs/Veri_Intelligent_Data/ENCODING_FIX_Vietnamese_Diacritics.md`
- **Implementation:** `docs/Veri_Intelligent_Data/SAFE_MIGRATION_SCRIPT_COMPLETE.md`

---

**Last Updated:** November 8, 2025  
**Mandatory for:** All migrations with Vietnamese text
