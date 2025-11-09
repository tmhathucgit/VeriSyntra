# VeriSyntra Unit Tests

**Fast unit tests** for core logic validation without external dependencies.

---

## 📁 Test Organization

### Unit Tests (< 1 minute total)

**Authentication & Security:**
- `test_password_utils.py` - Password hashing and validation
  - Bcrypt hashing algorithm
  - Password strength validation
  - Hash verification

- `test_jwt_handler.py` - JWT token creation and validation
  - Access token generation
  - Refresh token generation
  - Token validation and expiration
  - Claims extraction

- `test_token_blacklist.py` - Redis token blacklist management
  - Token blacklisting
  - Blacklist checking
  - Token expiration handling

**Data Processing:**
- `test_pdpl_normalizer.py` - PDPL text normalization
  - Vietnamese text normalization
  - Diacritics handling
  - Text cleaning and formatting

---

## 🚀 Running Unit Tests

### Via Regression Suite (Recommended)

```bash
# Run all tests including unit tests
python backend/tests/run_regression_tests.py
```

Unit tests are included in Priority 1 (Authentication & Security) and Priority 2 (Data Processing).

### Direct Execution

```bash
# All unit tests
pytest backend/tests/unit/ -v

# Single test file
pytest backend/tests/unit/test_password_utils.py -v

# Specific test function
pytest backend/tests/unit/test_jwt_handler.py::test_create_access_token -v

# With coverage
pytest backend/tests/unit/ --cov=backend --cov-report=html

# Watch mode (run on file changes)
pytest-watch backend/tests/unit/
```

---

## ⚙️ Characteristics of Unit Tests

### Fast Execution
- **No external dependencies** (databases, APIs, services)
- **Mocked dependencies** where necessary
- **Total duration:** < 1 minute for all tests

### Isolated Testing
- Each test is independent
- No shared state between tests
- Deterministic results

### Core Logic Focus
- Business logic validation
- Algorithm correctness
- Edge case handling
- Error conditions

---

## 📊 Test Coverage

| Test Suite | Tests | Coverage | Duration |
|------------|-------|----------|----------|
| Password Utils | 10+ | 95%+ | 5-10s |
| JWT Handler | 15+ | 95%+ | 5-10s |
| Token Blacklist | 8+ | 90%+ | 5-10s |
| PDPL Normalizer | 12+ | 90%+ | 5-10s |

**Total:** 45+ tests, < 1 minute

---

## 🎯 Unit Test Principles

### What Unit Tests Should Test

✅ **Pure functions** - Input → Output transformations
✅ **Business logic** - Core algorithms and rules
✅ **Validation** - Input validation and sanitization
✅ **Error handling** - Exception scenarios
✅ **Edge cases** - Boundary conditions

### What Unit Tests Should NOT Test

❌ **Database interactions** - Use system tests
❌ **API endpoints** - Use system tests
❌ **External services** - Use integration tests
❌ **File I/O** - Use system tests (unless mocked)
❌ **Network calls** - Use integration tests

---

## 🔧 Test Dependencies

### Required Packages

```bash
# Testing framework
pip install pytest pytest-cov pytest-mock

# Test utilities
pip install faker  # For test data generation
```

### No External Services Required

Unit tests run without:
- PostgreSQL database
- Redis server
- Running backend API
- External APIs or services

---

## 📝 Writing New Unit Tests

### Unit Test Template

```python
"""
Unit tests for [Module Name]
Tests [brief description of functionality]
"""

import pytest
from backend.app.core.your_module import YourClass


class TestYourClass:
    """Test suite for YourClass"""
    
    def test_basic_functionality(self):
        """Test basic happy path"""
        result = YourClass.method("input")
        assert result == "expected_output"
    
    def test_edge_case(self):
        """Test edge case handling"""
        result = YourClass.method("")
        assert result is None
    
    def test_error_handling(self):
        """Test error conditions"""
        with pytest.raises(ValueError):
            YourClass.method(None)
```

### Naming Conventions

- **File names:** `test_<module_name>.py`
- **Class names:** `Test<ClassName>`
- **Test functions:** `test_<what_is_being_tested>`
- **Use descriptive names** that explain the test purpose

---

## 🐛 Debugging Failed Tests

### Verbose Output

```bash
# Show detailed output
pytest backend/tests/unit/test_password_utils.py -vv

# Show print statements
pytest backend/tests/unit/test_password_utils.py -s

# Stop on first failure
pytest backend/tests/unit/ -x

# Show local variables on failure
pytest backend/tests/unit/ -l
```

### Test Isolation

```bash
# Run single test
pytest backend/tests/unit/test_jwt_handler.py::test_create_access_token -v

# Run tests matching pattern
pytest backend/tests/unit/ -k "password" -v
```

---

## 📚 Related Documentation

- **System Tests:** `backend/tests/system/README.md`
- **ML Tests:** `backend/tests/ml/README.md`
- **Backend Tests:** `backend/tests/README.md`
- **Test Standards:** `.github/copilot-instructions.md`

---

## 🔄 CI/CD Integration

Unit tests are the foundation of the CI/CD pipeline:

```yaml
# .github/workflows/tests.yml
- name: Run unit tests
  run: pytest backend/tests/unit/ -v --cov=backend
```

**Benefits:**
- Fast feedback on every commit
- High code coverage baseline
- Early detection of regressions
- No infrastructure dependencies

---

## 💡 Best Practices

### Keep Unit Tests Fast
- Mock external dependencies
- Avoid I/O operations
- Use in-memory data structures
- Aim for < 100ms per test

### Keep Unit Tests Simple
- Test one thing per test
- Clear arrange-act-assert pattern
- Minimal test data setup
- Self-documenting test names

### Keep Unit Tests Independent
- No shared state
- No test execution order dependencies
- Clean setup/teardown
- Isolated assertions

---

**Last Updated:** November 8, 2025  
**Maintainer:** VeriSyntra Backend Team  
**Test Coverage:** 4 unit test suites, 45+ tests
