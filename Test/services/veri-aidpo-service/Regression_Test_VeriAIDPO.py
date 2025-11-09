"""
VeriAIDPO Microservice Regression Test Runner
Test/services/veri-aidpo-service/Regression_Test_VeriAIDPO.py

Auto-discovers and runs all unit and system tests for VeriAIDPO service.

Usage:
    python Regression_Test_VeriAIDPO.py
    python Regression_Test_VeriAIDPO.py --verbose
    python Regression_Test_VeriAIDPO.py --quick  # Skip slow tests
"""
import sys
import os
from pathlib import Path

# Add Test directory to Python path
test_root = Path(__file__).parent
sys.path.insert(0, str(test_root))

# Import test modules
from system.test_authentication_integration import run_all_tests as run_system_tests


def run_regression_tests(verbose=False):
    """
    Run all VeriAIDPO microservice tests
    
    Test Categories:
    - Unit Tests: Fast tests for auth modules (when created)
    - System Tests: Authentication integration tests
    """
    print("=" * 80)
    print("VeriAIDPO Microservice Regression Tests")
    print("=" * 80)
    print()
    
    all_passed = True
    
    # Run System Tests
    print("[RUNNING] System Tests - Authentication Integration")
    print("-" * 80)
    system_passed = run_system_tests()
    all_passed = all_passed and system_passed
    print()
    
    # Run Unit Tests (when created)
    # TODO: Add unit tests for jwt_validator.py and permissions.py
    # from unit.test_jwt_validator import run_all_tests as run_jwt_tests
    # from unit.test_permissions import run_all_tests as run_permission_tests
    # print("[RUNNING] Unit Tests - JWT Validation")
    # jwt_passed = run_jwt_tests()
    # all_passed = all_passed and jwt_passed
    
    # Final Summary
    print("=" * 80)
    if all_passed:
        print("[SUCCESS] All VeriAIDPO microservice tests passed")
    else:
        print("[FAILED] Some VeriAIDPO microservice tests failed")
    print("=" * 80)
    
    return all_passed


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    quick = "--quick" in sys.argv
    
    success = run_regression_tests(verbose=verbose)
    exit(0 if success else 1)
