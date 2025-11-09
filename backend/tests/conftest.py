"""
VeriSyntra Test Configuration
Vietnamese PDPL 2025 Compliance Platform

Pytest configuration and shared fixtures for authentication testing.
"""

import pytest
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Test configuration
TEST_JWT_SECRET = "test_secret_key_for_unit_testing_only_do_not_use_in_production"
TEST_REDIS_DB = 15  # Use separate Redis database for testing


@pytest.fixture
def sample_user_data():
    """Sample Vietnamese business user data for testing."""
    return {
        "user_id": "user123",
        "email": "nguyen.van.a@example.com",
        "tenant_id": "tenant001",
        "regional_location": "south",  # HCMC business context
        "role": "admin"
    }


@pytest.fixture
def sample_password():
    """Sample strong password for testing."""
    return "MatKhau123!@#"  # Vietnamese: Mat Khau = Password


@pytest.fixture
def sample_weak_passwords():
    """Sample weak passwords for validation testing."""
    return [
        "123456",  # Too short, no complexity
        "password",  # No uppercase, no digit, no special
        "Password",  # No digit, no special
        "Pass123",  # No special character
        "Pass@",  # Too short
        "",  # Empty
    ]


@pytest.fixture
def mock_redis_down():
    """Mock Redis connection failure for fail-secure testing."""
    return Exception("Redis connection failed")
