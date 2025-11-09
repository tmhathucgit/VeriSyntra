"""
VeriSyntra System & Integration Test Suite

Vietnamese Context: Bo kiem thu Tich hop He thong
System-level integration tests and cross-component validation

Test Organization:
- test_auth_phase2.py - Phase 2 authentication integration
- test_admin_companies_api.py - Admin company management API
- test_company_registry.py - Company registry integration
- test_ropa_endpoints.py - ROPA API endpoints
- test_database_integration.py - Database integration and ROPA workflow
- test_visualization_reporting.py - Visualization and reporting integration
- test_vietnamese_encoding.ps1 - Database UTF-8 encoding validation
- test_swagger_ui.py - Swagger UI documentation server (manual)

Usage:
    Run via backend regression suite:
    python backend/tests/run_regression_tests.py
    
    Manual Swagger UI test:
    python backend/tests/system/test_swagger_ui.py
"""

__version__ = "1.0.0"
__author__ = "VeriSyntra System Team"

# System test suite metadata
SYSTEM_TEST_SUITE = {
    "name": "VeriSyntra System Test Suite",
    "version": __version__,
    "test_count": 8,
    "categories": [
        "Authentication Integration",
        "API Integration",
        "Database Integration",
        "ROPA Workflow",
        "Visualization & Reporting",
        "Database Encoding",
        "Manual Testing"
    ],
    "duration_estimates": {
        "full": "3-4 minutes"
    }
}
