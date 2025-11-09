# VeriSyntra System & Integration Tests

**System-level integration tests** for cross-component validation and database integrity checks.

---

## 📁 Test Organization

### System Integration Tests

**Authentication:**
- `test_auth_phase2.py` - Phase 2 authentication API integration
  - Login/logout flows
  - Token management
  - Session handling
  - User authentication end-to-end

**API Integration:**
- `test_admin_companies_api.py` - Admin company management API
  - Company CRUD operations
  - Vietnamese company data handling
  - API endpoint validation

- `test_company_registry.py` - Company registry integration
  - Vietnamese company lookups
  - Regional business context
  - Industry categorization

- `test_ropa_endpoints.py` - ROPA (Record of Processing Activities) API
  - ROPA generation endpoints
  - Service initialization and storage
  - Document lifecycle management
  - Vietnamese PDPL 2025 compliance

**Database Integration:**
- `test_database_integration.py` - Database integration and ROPA workflow
  - End-to-end ROPA generation from database
  - Multi-tenant data isolation
  - Vietnamese-first architecture validation
  - CRUD operations with real database queries
  - MPS compliance and audit trail

**Visualization & Reporting:**
- `test_visualization_reporting.py` - Visualization and reporting integration
  - Report generation and formatting
  - Data lineage graph creation
  - Bilingual Vietnamese-first output
  - Export reporting service

**Database Validation:**
- `test_vietnamese_encoding.ps1` - Vietnamese UTF-8 encoding validation
  - Database encoding integrity
  - Missing diacritics detection
  - Corruption detection
  - Multi-table validation (permissions, tenants, users)

**Manual Testing & Documentation:**
- `test_swagger_ui.py` - Swagger UI documentation server
  - Manual API documentation validation
  - OpenAPI/Swagger UI testing
  - Development server for API exploration
  - Run manually: `python backend/tests/system/test_swagger_ui.py`

---

## 🚀 Running System Tests

### Via Regression Suite (Recommended)

```bash
# Run all tests including system tests
python backend/tests/run_regression_tests.py
```

System tests are automatically included in the regression suite as Priority 1 and Priority 3.

### Individual System Tests

**Python tests:**
```bash
# Single test file
pytest backend/tests/system/test_auth_phase2.py -v

# All system tests
pytest backend/tests/system/ -v

# Specific test function
pytest backend/tests/system/test_company_registry.py::test_company_lookup -v
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

## ⚙️ Prerequisites

### Running Backend

Most system tests require the backend server to be running:

```bash
# Start backend server
cd backend
python main_prototype.py

# Server runs on http://localhost:8000
```

### Database

Vietnamese encoding tests require PostgreSQL container:

```bash
# Start via Docker Compose
docker-compose up -d postgres

# Verify container running
docker ps | grep verisyntra-postgres
```

---

## 📊 Test Coverage

| Test Suite | Coverage | Duration |
|------------|----------|----------|
| Authentication Integration | Login, logout, tokens | 30-45s |
| Admin Companies API | CRUD, Vietnamese data | 20-30s |
| Company Registry | Lookups, regional data | 15-20s |
| ROPA Endpoints | API, storage, generation | 30-45s |
| Database Integration | Multi-tenant, CRUD, ROPA | 45-60s |
| Visualization & Reporting | Reports, graphs, export | 30-45s |
| Vietnamese Encoding | UTF-8, diacritics | 30-45s |

**Total Duration:** ~3-4 minutes

---

## 🎯 Test Categories

### Integration Tests

System tests validate interactions between components:
- **API → Database:** Data persistence and retrieval
- **Authentication → Session:** Token lifecycle
- **Vietnamese Data → Encoding:** UTF-8 integrity

### Database Integrity

Vietnamese encoding test validates:
- UTF-8 multi-byte characters (á, ồ, ệ, ữ, etc.)
- Proper diacritics in all Vietnamese fields
- No corruption (?, ???, garbled text)
- Byte count > character count for Vietnamese text

---

## 🔧 Configuration

### Environment Variables

```bash
# Database connection
DATABASE_URL=postgresql://verisyntra:password@localhost:5432/verisyntra

# Backend API
BACKEND_URL=http://localhost:8000

# Redis (for token blacklist)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Test Data

System tests use:
- Test companies with Vietnamese names
- Vietnamese user data
- PDPL categories with Vietnamese translations
- Regional business contexts (North, Central, South)

---

## 🐛 Troubleshooting

### Backend Connection Issues

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check backend logs
cd backend
python main_prototype.py
```

### Database Connection Issues

```bash
# Verify PostgreSQL container
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "SELECT version();"

# Check database encoding
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "SHOW server_encoding;"
```

### Vietnamese Encoding Issues

```powershell
# Run encoding diagnostic
.\backend\tests\system\test_vietnamese_encoding.ps1 -Verbose

# Check specific table
docker exec verisyntra-postgres psql -U verisyntra -d verisyntra -c "
    SELECT permission_name_vi, 
           length(permission_name_vi) as chars,
           octet_length(permission_name_vi) as bytes
    FROM permissions LIMIT 5;
"
```

---

## 📚 Related Documentation

- **Backend Tests:** `backend/tests/README.md`
- **ML Tests:** `backend/tests/ml/README.md`
- **Vietnamese Encoding Fix:** `docs/Veri_Intelligent_Data/ENCODING_FIX_Vietnamese_Diacritics.md`
- **Safe Migrations:** `scripts/README.md`

---

## 🔄 CI/CD Integration

System tests are included in the main regression suite:

```yaml
# .github/workflows/tests.yml
- name: Run regression tests (includes system tests)
  run: python backend/tests/run_regression_tests.py
```

System tests validate:
- End-to-end authentication flows
- Vietnamese data integrity
- API contract compliance
- Database encoding standards

---

**Last Updated:** November 8, 2025  
**Maintainer:** VeriSyntra System Team  
**Test Coverage:** 4 system test suites
