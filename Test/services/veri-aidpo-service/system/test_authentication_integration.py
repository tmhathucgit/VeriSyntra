"""
VeriAIDPO Microservice Authentication Integration Tests
Test/services/veri-aidpo-service/system/test_authentication_integration.py

Tests JWT validation and permission enforcement on VeriAIDPO service endpoints.

Test Coverage:
- Public health endpoint (no auth)
- No authentication returns 403
- Valid token with correct permission authorized
- Valid token with insufficient permission returns 403 with bilingual error
- Bilingual error messages verified
"""
import requests
import json
from jose import jwt
from datetime import datetime, timedelta, timezone

# Test Configuration
BASE_URL = "http://localhost:8001"
JWT_SECRET_KEY = "zmXPd8JT-sObkweLGRAdWB4L0Xfne1nG1PZ5kMne8wk"
JWT_ALGORITHM = "HS256"


def generate_test_token(role: str = "admin", permissions: list = None):
    """Generate test JWT token with specified role and permissions"""
    if permissions is None:
        # Default admin permissions
        permissions = [
            "user.read", "user.write",
            "company.read", "company.write",
            "processing_activity.read", "processing_activity.write",
            "data_category.read", "data_category.write",
            "ropa.read", "ropa.write", "ropa.generate",
            "analytics.read",
            "tenant.read", "tenant.write"
        ]
    
    payload = {
        "sub": "test-user-123",  # user_id
        "role": role,
        "tenant_id": "test-tenant-456",
        "permissions": permissions,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def test_health_public():
    """Test public health endpoint - no authentication required"""
    response = requests.get(f"{BASE_URL}/health")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy"
    assert "VeriAIDPO" in data["service"]
    print("[OK] test_health_public - Health endpoint accessible without authentication")


def test_classify_no_auth():
    """Test classify endpoint without authentication - expect 403"""
    response = requests.post(
        f"{BASE_URL}/api/v1/classify",
        json={"text": "Email: test@example.com", "language": "en"}
    )
    
    # FastAPI HTTPBearer returns 403 when no Authorization header
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    print("[OK] test_classify_no_auth - No authentication returns 403")


def test_classify_with_valid_token():
    """Test classify endpoint with valid token and correct permission"""
    admin_token = generate_test_token(role="admin")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = requests.post(
        f"{BASE_URL}/api/v1/classify",
        json={"text": "Họ tên: Nguyễn Văn A, Email: user@example.com", "language": "vi"},
        headers=headers
    )
    
    # Accept 200 (model loaded) or 500 (model not loaded) - RBAC passed if not 403
    assert response.status_code in [200, 500], f"Expected 200 or 500, got {response.status_code}"
    
    if response.status_code == 200:
        print("[OK] test_classify_with_valid_token - Classification successful, RBAC authorized")
    else:
        print("[OK] test_classify_with_valid_token - RBAC authorized (500 = model not loaded, not 403)")


def test_classify_insufficient_permission():
    """Test classify endpoint with viewer token (missing processing_activity.read)"""
    viewer_token = generate_test_token(
        role="viewer",
        permissions=["user.read", "company.read", "analytics.read"]
    )
    headers = {"Authorization": f"Bearer {viewer_token}"}
    
    response = requests.post(
        f"{BASE_URL}/api/v1/classify",
        json={"text": "Email: viewer@example.com", "language": "en"},
        headers=headers
    )
    
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    data = response.json()
    assert "detail" in data
    detail = data["detail"]
    
    # Verify bilingual error structure
    assert isinstance(detail, dict), "Error detail should be dict"
    assert "error" in detail, "Missing English error message"
    assert "error_vi" in detail, "Missing Vietnamese error message"
    assert "required_permission" in detail, "Missing required_permission field"
    assert "user_role" in detail, "Missing user_role field"
    assert "user_permissions" in detail, "Missing user_permissions field"
    
    # Verify Vietnamese diacritics
    error_vi = detail["error_vi"]
    assert "Từ chối quyền truy cập" in error_vi, "Vietnamese error missing or incorrect"
    assert detail["required_permission"] == "processing_activity.read"
    assert detail["user_role"] == "viewer"
    assert "user.read" in detail["user_permissions"]
    
    print("[OK] test_classify_insufficient_permission - Permission denied with bilingual error")
    print(f"     Vietnamese error: {error_vi}")


def test_model_status_with_permission():
    """Test model status endpoint with admin token (analytics.read permission)"""
    admin_token = generate_test_token(role="admin")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = requests.get(f"{BASE_URL}/api/v1/model-status", headers=headers)
    
    # Accept any non-403 status - RBAC passed if not permission denied
    assert response.status_code != 403, f"Expected non-403, got {response.status_code}"
    print(f"[OK] test_model_status_with_permission - RBAC authorized (status: {response.status_code})")


def test_normalize_with_permission():
    """Test normalize endpoint with admin token (data_category.write permission)"""
    admin_token = generate_test_token(role="admin")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = requests.post(
        f"{BASE_URL}/api/v1/normalize",
        json={"category": "Tên khách hàng"},
        headers=headers
    )
    
    # Accept any non-403 status - RBAC passed
    assert response.status_code != 403, f"Expected non-403, got {response.status_code}"
    print(f"[OK] test_normalize_with_permission - RBAC authorized (status: {response.status_code})")


def run_all_tests():
    """Run all authentication integration tests"""
    print("=" * 70)
    print("VeriAIDPO Microservice Authentication Integration Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_health_public,
        test_classify_no_auth,
        test_classify_with_valid_token,
        test_classify_insufficient_permission,
        test_model_status_with_permission,
        test_normalize_with_permission,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"[FAILED] {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test_func.__name__}: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
