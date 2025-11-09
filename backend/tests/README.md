# VeriSyntra Test Suite

**Consolidated test directory** for all VeriSyntra automated tests.

## 📁 Test Organization

### Unit Tests (Fast - Core Logic)

**Unit tests in `unit/` subdirectory** - See `unit/README.md`

**Authentication & Security:**
- `unit/test_password_utils.py` - Password hashing and validation
- `unit/test_jwt_handler.py` - JWT token creation and validation
- `unit/test_token_blacklist.py` - Redis token blacklist management

**Data Processing:**
- `unit/test_pdpl_normalizer.py` - PDPL text normalization

### System Tests (Integration & Database)

**System tests in `system/` subdirectory** - See `system/README.md`

**Authentication Integration:**
- `system/test_auth_phase2.py` - Phase 2 authentication API integration

**API Integration:**
- `system/test_admin_companies_api.py` - Company management API
- `system/test_company_registry.py` - Company registry functionality
- `system/test_ropa_endpoints.py` - ROPA API endpoints

**Database Integration:**
- `system/test_database_integration.py` - Database integration and ROPA workflow
- `system/test_visualization_reporting.py` - Visualization and reporting

**Database Validation:**
- `system/test_vietnamese_encoding.ps1` - UTF-8 encoding integrity and diacritics compliance

### ML Tests (Slow - Run Separately)

**Machine Learning tests in `ml/` subdirectory** - See `ml/README.md`

**Model Tests:**
- `ml/test_model_integration.py` - Model loading and inference
- `ml/test_all_model_types.py` - All model variants testing

**API Tests:**
- `ml/test_veriaidpo_classification_api.py` - VeriAiDPO classification API

**Dataset Tests:**
- `ml/test_vietnamese_hard_dataset_generator.py` - Vietnamese dataset generation

### Test Runners

**`run_regression_tests.py`** - Backend regression test suite (FAST)
- Priority 1: Authentication & Security (unit tests + system integration + company management)
- Priority 2: Data Processing (unit tests)
- Priority 3: Vietnamese UTF-8 Encoding (system tests)
- Duration: ~3-4 minutes
- Tests: 8 test suites
- Trigger: Every code change, PR, deployment

**`run_ml_tests.py`** - ML model test suite (SLOW)
- Priority 1: Model Inference & Integration
- Priority 2: VeriAiDPO Classification API
- Priority 3: Vietnamese Dataset Generation
- Duration: 10-15 minutes (3-5 min with `--quick`)
- Trigger: ML changes, model updates, scheduled/nightly

---

## 🚀 Running Tests

### Backend Regression Suite (Recommended for Development)

```bash
# Run all backend regression tests (FAST - ~2 minutes)
python backend/tests/run_regression_tests.py

# From workspace root
python backend\tests\run_regression_tests.py
```

**Output:**
- Color-coded results (green/red/yellow)
- Bilingual headers (English/Vietnamese)
- Detailed summary with pass/fail counts

### ML Test Suite (Run Separately)

```bash
# Run all ML tests (SLOW - 10-15 minutes)
python backend/tests/run_ml_tests.py

# Quick mode - skip slow dataset tests (3-5 minutes)
python backend/tests/run_ml_tests.py --quick

# Models only - fastest (1-2 minutes)
python backend/tests/run_ml_tests.py --models-only
```

See `ml/README.md` for detailed ML test documentation.

### Individual Test Suites

**Python tests (pytest):**
```bash
# Single test file
pytest backend/tests/unit/test_password_utils.py -v

# All unit tests
pytest backend/tests/unit/ -v

# All system tests
pytest backend/tests/system/ -v

# All ML tests
pytest backend/tests/ml/ -v

# All tests (unit + system, exclude ML)
pytest backend/tests/ --ignore=backend/tests/ml/ -v

# With coverage
pytest backend/tests/ --cov=backend --cov-report=html
```

**Vietnamese encoding test:**
```powershell
# Standard mode
.\backend\tests\system\test_vietnamese_encoding.ps1

# Strict mode (fail on warnings)
.\backend\tests\system\test_vietnamese_encoding.ps1 -FailOnWarnings $true

# Custom database
.\backend\tests\system\test_vietnamese_encoding.ps1 -Container "custom-pg" -Database "mydb"
```

---

## 📊 Test Results

### Expected Output - All Tests Pass

```
======================================================================
VeriSyntra Phase 2 Regression Test Suite
Kiem thu Hoi quy VeriSyntra Phase 2
======================================================================

======================================================================
PRIORITY 1: Authentication & Security Tests
UU TIEN 1: Kiem thu Xac thuc & Bao mat
======================================================================

--- Password Hashing & Validation ---
[OK] Password Hashing & Validation - Tests passed

--- JWT Token Creation & Validation ---
[OK] JWT Token Creation & Validation - Tests passed

======================================================================
PRIORITY 3: Vietnamese UTF-8 Encoding Tests
UU TIEN 3: Kiem thu Ma hoa UTF-8 Tieng Viet
======================================================================

--- Vietnamese UTF-8 Encoding & Diacritics Compliance ---
[OK] Vietnamese UTF-8 Encoding & Diacritics Compliance - All tests passed

======================================================================
Regression Test Summary / Tong ket Kiem thu Hoi quy
======================================================================

Overall Results:
  Total Tests: 6
  Passed: 6
  Failed: 0
  Errors: 0

[OK] All critical regression tests passed!
[OK] Tat ca kiem thu hoi quy thanh cong!
```

---

## 🔧 Test Configuration

### pytest Configuration

**File:** `conftest.py`

Provides:
- Test database fixtures
- Redis connection fixtures
- Mock data generators
- Test client setup

### Environment Variables

Required for tests:
```bash
# Database
DATABASE_URL=postgresql://verisyntra:password@localhost:5432/verisyntra

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
```

---

## 🎯 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/tests.yml
name: VeriSyntra Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  tests:
    runs-on: windows-latest
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: verisyntra
          POSTGRES_USER: verisyntra
          POSTGRES_PASSWORD: ${{ secrets.DB_PASSWORD }}
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov
      
      - name: Run regression tests
        run: python backend\tests\run_regression_tests.py
        env:
          DATABASE_URL: postgresql://verisyntra:password@localhost:5432/verisyntra
          REDIS_HOST: localhost
          REDIS_PORT: 6379
      
      - name: Upload coverage reports
        if: always()
        uses: codecov/codecov-action@v3
```

---

## 🧪 Test Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| Authentication | 90%+ | ✓ |
| JWT Handling | 90%+ | ✓ |
| Password Utils | 95%+ | ✓ |
| Vietnamese Encoding | 100% | ✓ |
| PDPL Normalization | 85%+ | ✓ |

---

## 📝 Adding New Tests

### Python Test Template

```python
"""
Test module for [Feature Name]
Vietnamese Context: [Vietnamese description]
"""

import pytest
from backend.app.core.your_module import YourClass


def test_feature_basic():
    """Test basic functionality"""
    result = YourClass.method()
    assert result is not None


def test_feature_vietnamese():
    """Test Vietnamese-specific behavior"""
    vietnamese_input = "Nguyễn Văn An"
    result = YourClass.process(vietnamese_input)
    assert "ễ" in result  # Ensure diacritics preserved
```

### PowerShell Test Template

```powershell
# Test Vietnamese [Feature]
Write-Host "[TEST] Vietnamese [Feature]" -ForegroundColor Cyan

$result = Test-Feature -Input "Vietnamese data"

if ($result -match "expected pattern") {
    Write-Host "[PASS] Test passed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Test failed" -ForegroundColor Red
    exit 1
}
```

---

## 🔍 Debugging Failed Tests

### View Detailed Output

```bash
# Pytest verbose mode
pytest backend/tests/test_auth_phase2.py -vv

# Show print statements
pytest backend/tests/test_auth_phase2.py -s

# Stop on first failure
pytest backend/tests/ -x

# Run specific test
pytest backend/tests/test_jwt_handler.py::test_create_access_token
```

### Vietnamese Encoding Test Debugging

```powershell
# Run with output to file
.\backend\tests\test_vietnamese_encoding.ps1 > encoding_results.txt

# Check specific table
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "
    SELECT permission_name, permission_name_vi, 
           length(permission_name_vi) as chars,
           octet_length(permission_name_vi) as bytes
    FROM permissions
    LIMIT 10;
"
```

---

## 📚 Related Documentation

- **Migration Standards:** `../.github/copilot-instructions.md` - Database Migration Standards section
- **Safe Migrations:** `../scripts/README.md` - Vietnamese UTF-8 encoding protection
- **Encoding Fix:** `../docs/Veri_Intelligent_Data/ENCODING_FIX_Vietnamese_Diacritics.md`

---

**Last Updated:** November 8, 2025  
**Maintainer:** VeriSyntra Development Team  
**Test Coverage:** 10 test suites, 100+ individual tests
