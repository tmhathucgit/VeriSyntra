# VeriSyntra Database Migration Scripts

This directory contains safe migration tools for VeriSyntra PostgreSQL database operations with Vietnamese UTF-8 encoding protection.

## Scripts

### `run_migration_safe.ps1`

**Purpose:** Execute SQL migrations while preserving Vietnamese UTF-8 diacritics

**Problem Solved:** PowerShell's `Get-Content | docker exec` pipeline corrupts multi-byte Vietnamese characters (ạ, ộ, ệ, ủ, ế, ư) into ASCII replacements.

**Solution:** Uses `docker cp` to transfer files directly, preserving UTF-8 encoding.

**New Feature:** Pre-migration validation detects missing Vietnamese diacritics in SQL files before execution.

---

## Test Scripts

All test scripts are now consolidated in `backend/tests/` directory:

### `backend/tests/test_vietnamese_encoding.ps1`

**Purpose:** Automated regression testing for Vietnamese UTF-8 encoding integrity and diacritics compliance

**Location:** Moved from `scripts/` to `backend/tests/` for consolidated test management

**What It Tests:**
1. Docker container availability
2. Database connection
3. Vietnamese field discovery
4. UTF-8 encoding correctness (byte_count > char_count)
5. Corruption detection (question marks, garbled text)
6. Missing diacritics detection (common non-diacritic patterns)
7. Data quality thresholds (95%+ for users/permissions, 80%+ for tenants)
8. Sample data verification

**Use Cases:**
- Pre-deployment validation
- CI/CD pipeline integration (via `run_regression_tests.py`)
- Periodic health checks
- Post-migration verification

### `backend/tests/run_regression_tests.py`

**Purpose:** Unified regression test suite runner

**Runs:**
1. Authentication & Security tests (pytest)
2. Data Processing tests (pytest)
3. Vietnamese UTF-8 Encoding tests (PowerShell)

**Usage:**
```bash
python backend/tests/run_regression_tests.py
```

---

## Usage

### Safe Migration Execution

```powershell
# Navigate to VeriSyntra root directory
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra

# Run migration with automatic encoding verification
.\scripts\run_migration_safe.ps1 -MigrationFile "backend\veri_ai_data_inventory\migrations\add_permissions_table.sql"
```

### Vietnamese Encoding Tests

```powershell
# Run comprehensive Vietnamese encoding test suite
cd backend\tests
..\..\..\backend\tests\test_vietnamese_encoding.ps1

# Or run via Python regression suite (recommended)
python backend\tests\run_regression_tests.py

# Run with strict mode (fail on warnings) - standalone
.\backend\tests\test_vietnamese_encoding.ps1 -FailOnWarnings $true

# Custom database connection
.\backend\tests\test_vietnamese_encoding.ps1 `
    -Container "custom-postgres" `
    -Database "mydb" `
    -User "myuser"
```

### Advanced Options

```powershell
# Custom container name
.\scripts\run_migration_safe.ps1 `
    -MigrationFile "migrations\step2.sql" `
    -Container "custom-postgres" `
    -Database "mydb" `
    -User "myuser"

# Skip encoding verification (faster, but not recommended)
.\scripts\run_migration_safe.ps1 `
    -MigrationFile "migrations\step2.sql" `
    -VerifyEncoding $false

# Keep temporary file in container for debugging
.\scripts\run_migration_safe.ps1 `
    -MigrationFile "migrations\step2.sql" `
    -CleanupTemp $false
```

---

## Features

### ✓ UTF-8 Encoding Protection

- Uses `docker cp` instead of PowerShell pipes
- Preserves Vietnamese diacritics during file transfer
- No character corruption from PowerShell text processing

### ✓ Automatic Validation

1. **File Validation**
   - Checks if migration file exists
   - Detects Vietnamese diacritics in source file
   - Reports file size and encoding

2. **Container Validation**
   - Verifies Docker container is running
   - Tests database connection before migration
   - Provides helpful error messages

3. **Encoding Verification** (optional)
   - Compares character count vs byte count
   - Detects UTF-8 corruption (when `char_count = byte_count`)
   - Reports encoding health of Vietnamese data

### ✓ Clean Execution

- Colored output for easy status tracking
  - `[OK]` Green: Success messages
  - `[INFO]` Cyan: Informational messages
  - `[WARNING]` Yellow: Potential issues
  - `[ERROR]` Red: Failures
- Automatic cleanup of temporary files
- Detailed execution summary

---

## How It Works

### Step-by-Step Process

```
1. Validate migration file exists
   -> Check file path
   -> Detect Vietnamese diacritics
   -> Report file info

2. Check Docker container
   -> Verify container is running
   -> Provide start command if not

3. Test database connection
   -> Execute test query
   -> Verify credentials work

4. Copy file to container
   -> Use docker cp (preserves UTF-8)
   -> Generate unique temp filename
   -> Confirm successful copy

5. Execute migration
   -> Run psql -f inside container
   -> Display all output
   -> Check for errors

6. Verify encoding (optional)
   -> Query Vietnamese fields
   -> Compare char_count vs byte_count
   -> Report any corruption detected

7. Cleanup
   -> Remove temporary file
   -> Display execution summary
```

---

## Encoding Verification Details

### What It Checks

The script runs this query after migration:

```sql
SELECT 
    COUNT(*) FILTER (WHERE octet_length(permission_name_vi) > length(permission_name_vi)) as utf8_correct,
    COUNT(*) FILTER (WHERE octet_length(permission_name_vi) = length(permission_name_vi)) as possibly_corrupted,
    COUNT(*) as total
FROM permissions
WHERE permission_name_vi IS NOT NULL;
```

### Expected Results

**✓ CORRECT UTF-8 Encoding:**
```
UTF-8 Vietnamese: 22 records
Possibly corrupted: 0 records
Total: 22 records
```

**❌ CORRUPTED Encoding:**
```
UTF-8 Vietnamese: 0 records
Possibly corrupted: 22 records
Total: 22 records
```

### Why This Works

Vietnamese characters with diacritics use multiple bytes in UTF-8:
- `ạ` = 3 bytes (e1 ba a1)
- `ộ` = 3 bytes (e1 bb 99)
- `ữ` = 3 bytes (e1 bb af)

**Important:** Some Vietnamese text may not have diacritics (e.g., "Xem ROPA" is all ASCII), so `char_count = byte_count` is normal for those entries.

If **most** entries show `char_count = byte_count`, database corruption likely occurred.

If **most** entries show `byte_count > char_count`, proper multi-byte UTF-8 Vietnamese characters are stored.

---

## Troubleshooting

### Error: "Docker container is not running"

```powershell
# Start the container
docker-compose up -d postgres

# Verify it's running
docker ps
```

### Error: "Cannot connect to database"

Check your connection settings:

```powershell
# Test connection manually
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "SELECT 1;"

# Check database exists
docker exec verisyntra-postgres psql -U verisyntra -l
```

### Warning: "Possibly corrupted records detected"

If encoding verification fails:

```powershell
# Investigate corruption
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "
    SELECT 
        permission_name,
        permission_name_vi,
        length(permission_name_vi) as chars,
        octet_length(permission_name_vi) as bytes
    FROM permissions
    WHERE permission_name_vi LIKE '%?%'  -- Likely corrupted
    LIMIT 10;
"

# Fix: Delete corrupted data and re-run migration
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "DELETE FROM permissions;"
.\scripts\run_migration_safe.ps1 -MigrationFile "your_migration.sql"
```

---

## VeriSyntra Coding Standards Compliance

### ✓ NO Emoji Characters

Script uses ASCII status indicators:
- `[OK]` instead of ✓
- `[ERROR]` instead of ✗
- `[WARNING]` instead of ⚠️
- `->` instead of →

### ✓ Vietnamese Diacritics in UI

Script properly detects and preserves Vietnamese diacritics:
- Detection: `[ạảãàáậặẵằắếềểễệộổỗồốợờởỡớụủũùúứừửữựỳỷỹý]`
- Preservation: Uses `docker cp` to avoid corruption
- Verification: Checks `octet_length() > length()`

### ✓ Dynamic Code

- No hard-coded paths
- Configurable parameters
- Reusable validation functions
- Template for future enhancements

---

## Integration with TODO Workflow

### Step 2: Role Mappings Example

```powershell
# When you reach Step 2 of RBAC implementation
cd C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra

# Create migration: backend\veri_ai_data_inventory\migrations\add_role_permissions_table.sql

# Execute safely
.\scripts\run_migration_safe.ps1 `
    -MigrationFile "backend\veri_ai_data_inventory\migrations\add_role_permissions_table.sql"
```

### Future Migrations with Vietnamese

Any migration with Vietnamese text should use this script:

```powershell
# ROPA templates with Vietnamese descriptions
.\scripts\run_migration_safe.ps1 -MigrationFile "migrations\add_ropa_templates.sql"

# Security measures with Vietnamese names
.\scripts\run_migration_safe.ps1 -MigrationFile "migrations\add_security_measures.sql"

# Vietnamese legal terminology
.\scripts\run_migration_safe.ps1 -MigrationFile "migrations\add_pdpl_articles.sql"
```

---

## Future Enhancements

Potential additions to this script:

1. **Backup before migration:** Automatic pg_dump before execution
2. **Rollback support:** Track migration versions for reversal
3. **Dry-run mode:** Preview migration without executing
4. **Multi-file support:** Execute multiple migrations in sequence
5. **Email notifications:** Alert team of migration completion
6. **Slack integration:** Post results to VeriSyntra dev channel

---

## Related Documentation

- `docs/Veri_Intelligent_Data/ENCODING_FIX_Vietnamese_Diacritics.md` - Detailed encoding issue analysis
- `docs/Veri_Intelligent_Data/STEP1_COMPLETE_RBAC_Permissions_Table.md` - Step 1 completion with encoding fix
- `docs/Veri_Intelligent_Data/TODO_Phase1_Task1.1.3_RBAC.md` - Full RBAC implementation plan

---

## Regression Testing Integration

### Add to CI/CD Pipeline

```yaml
# .github/workflows/database-tests.yml
name: Database Vietnamese Encoding Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  vietnamese-encoding:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start PostgreSQL container
        run: docker-compose up -d postgres
      
      - name: Wait for database
        run: Start-Sleep -Seconds 10
      
      - name: Run all regression tests (includes Vietnamese encoding)
        run: python backend\tests\run_regression_tests.py
      
      - name: Stop containers
        if: always()
        run: docker-compose down
```

### Local Regression Testing

Add Vietnamese encoding tests to your regular test suite:

```powershell
# Run all regression tests (recommended)
python backend\tests\run_regression_tests.py

# Or run Vietnamese encoding tests standalone
.\backend\tests\test_vietnamese_encoding.ps1

# Run with strict mode in CI/CD
.\backend\tests\test_vietnamese_encoding.ps1 -FailOnWarnings $true
```

### Pre-Deployment Checklist

Before deploying to production, run:

```powershell
# 1. Run full regression suite (includes Vietnamese encoding validation)
python backend\tests\run_regression_tests.py

# 2. Safe migration execution (if needed)
.\scripts\run_migration_safe.ps1 -MigrationFile "path\to\migration.sql"

# 3. Re-verify after migration (standalone)
.\backend\tests\test_vietnamese_encoding.ps1
```

---

## Support

For issues or questions:

1. Check troubleshooting section above
2. Review `ENCODING_FIX_Vietnamese_Diacritics.md` for detailed encoding analysis
3. Test manually with `docker cp` method shown in documentation
4. Consult VeriSyntra team lead

---

**Last Updated:** November 8, 2025  
**Maintainer:** VeriSyntra Development Team  
**Purpose:** Vietnamese UTF-8 encoding protection for PDPL 2025 compliance platform
