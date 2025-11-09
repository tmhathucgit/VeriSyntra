"""
VeriSyntra Unit Test Suite

Vietnamese Context: Bo kiem thu Don vi
Fast unit tests for core logic validation without external dependencies

Test Organization:
- test_password_utils.py - Password hashing and validation
- test_jwt_handler.py - JWT token creation and validation
- test_token_blacklist.py - Redis token blacklist management
- test_pdpl_normalizer.py - PDPL text normalization

Usage:
    Run via backend regression suite:
    python backend/tests/run_regression_tests.py
    
    Or run directly:
    pytest backend/tests/unit/ -v
"""

__version__ = "1.0.0"
__author__ = "VeriSyntra Backend Team"

# Unit test suite metadata
UNIT_TEST_SUITE = {
    "name": "VeriSyntra Unit Test Suite",
    "version": __version__,
    "test_count": 4,
    "categories": [
        "Password Security",
        "JWT Authentication",
        "Token Management",
        "Data Normalization"
    ],
    "duration_estimates": {
        "full": "< 1 minute"
    }
}
