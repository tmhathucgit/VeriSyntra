"""
Integration Tests for Phase 2 Authentication
Email-based authentication with tenant support

Vietnamese Context: Tests multi-tenant authentication with Vietnamese business context
Phase 2 Schema: Email-only login, requires existing tenants
"""

import pytest
import requests
from uuid import uuid4
import psycopg2

# Base URL for API
BASE_URL = "http://127.0.0.1:8000"
AUTH_URL = f"{BASE_URL}/api/v1/auth"

# Database connection
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "verisyntra",
    "user": "verisyntra",
    "password": "verisyntra_dev_password"
}


def create_test_tenant():
    """Create a test tenant in database - Tạo tổ chức test"""
    tenant_id = str(uuid4())  # Convert to string for psycopg2
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    tax_id = f"TEST{uuid4().hex[:9].upper()}"
    
    cur.execute(
        """
        INSERT INTO tenants (
            tenant_id, company_name, company_name_vi, tax_id,
            veri_regional_location, veri_industry_type,
            is_active, is_verified, pdpl_compliant
        ) VALUES (%s::uuid, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING tenant_id
        """,
        (
            tenant_id,
            "VeriSyntra Test Company",
            "Công ty Kiểm thử VeriSyntra",
            tax_id,
            "south",
            "technology",
            True,
            True,
            True
        )
    )
    
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return str(result[0])


class TestPhase2Authentication:
    """Phase 2 authentication integration tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data"""
        self.tenant_id = create_test_tenant()
        self.test_user = {
            "email": f"test_{uuid4().hex[:8]}@verisyntra.com",
            "password": "SecurePass123!",
            "full_name": "Nguyễn Văn Test",
            "full_name_vi": "Nguyễn Văn Test",
            "phone_number": "+84 901 234 567",
            "tenant_id": self.tenant_id
        }
        self.access_token = None
        self.refresh_token = None
    
    def test_01_server_health(self):
        """Test 1: Server health check"""
        response = requests.get(f"{BASE_URL}/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        
        print("[OK] Server is healthy and running")
        print(f"[OK] Server đang chạy: {data['service']}")
    
    def test_02_user_registration(self):
        """Test 2: User registration with email"""
        response = requests.post(
            f"{AUTH_URL}/register",
            json=self.test_user
        )
        
        assert response.status_code == 201, f"Registration should return 201, got {response.status_code}"
        data = response.json()
        
        assert "user_id" in data
        assert "email" in data
        assert data["email"] == self.test_user["email"]
        assert "message_vi" in data
        
        print(f"[OK] User registered successfully: {data['email']}")
        print(f"[OK] Đăng ký thành công: {data['message_vi']}")
    
    def test_03_duplicate_email(self):
        """Test 3: Duplicate email prevention"""
        user1 = {
            "email": f"dup_{uuid4().hex[:8]}@verisyntra.com",
            "password": "SecurePass123!",
            "full_name": "Nguyễn Văn Dup",
            "tenant_id": self.tenant_id
        }
        
        response1 = requests.post(f"{AUTH_URL}/register", json=user1)
        assert response1.status_code == 201
        
        response2 = requests.post(f"{AUTH_URL}/register", json=user1)
        assert response2.status_code == 400
        
        print("[OK] Duplicate email validation works")
    
    def test_04_user_login(self):
        """Test 4: Email-based login"""
        user = {
            "email": f"login_{uuid4().hex[:8]}@verisyntra.com",
            "password": "SecurePass123!",
            "full_name": "Nguyễn Thị Login",
            "tenant_id": self.tenant_id
        }
        
        requests.post(f"{AUTH_URL}/register", json=user)
        
        login_data = {
            "email": user["email"],
            "password": user["password"]
        }
        
        response = requests.post(f"{AUTH_URL}/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        
        self.access_token = data["access_token"]
        
        print("[OK] Login successful")
        print(f"[OK] {data['message_vi']}")
    
    def test_05_invalid_login(self):
        """Test 5: Invalid credentials"""
        login_data = {
            "email": "nonexistent@verisyntra.com",
            "password": "WrongPassword"
        }
        
        response = requests.post(f"{AUTH_URL}/login", json=login_data)
        
        assert response.status_code == 401
        print("[OK] Invalid login correctly rejected")
    
    def test_06_protected_endpoint_no_token(self):
        """Test 6: Protected endpoint without token"""
        response = requests.get(f"{AUTH_URL}/me")
        
        assert response.status_code == 401
        print("[OK] Protected endpoint requires authentication")
    
    def test_07_protected_endpoint_with_token(self):
        """Test 7: Protected endpoint with valid token"""
        user = {
            "email": f"protected_{uuid4().hex[:8]}@verisyntra.com",
            "password": "SecurePass123!",
            "full_name": "Nguyễn Văn Protected",
            "tenant_id": self.tenant_id
        }
        
        requests.post(f"{AUTH_URL}/register", json=user)
        
        login_response = requests.post(
            f"{AUTH_URL}/login",
            json={"email": user["email"], "password": user["password"]}
        )
        
        token = login_response.json()["access_token"]
        
        response = requests.get(
            f"{AUTH_URL}/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["email"] == user["email"]
        assert "tenant_id" in data
        
        print("[OK] Protected endpoint access successful")
    
    def test_08_token_refresh(self):
        """Test 8: Token refresh"""
        user = {
            "email": f"refresh_{uuid4().hex[:8]}@verisyntra.com",
            "password": "SecurePass123!",
            "full_name": "Lê Thị Refresh",
            "tenant_id": self.tenant_id
        }
        
        requests.post(f"{AUTH_URL}/register", json=user)
        
        login_response = requests.post(
            f"{AUTH_URL}/login",
            json={"email": user["email"], "password": user["password"]}
        )
        
        refresh_token = login_response.json()["refresh_token"]
        
        response = requests.post(
            f"{AUTH_URL}/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        print("[OK] Token refresh successful")
    
    def test_09_user_logout(self):
        """Test 9: User logout"""
        user = {
            "email": f"logout_{uuid4().hex[:8]}@verisyntra.com",
            "password": "SecurePass123!",
            "full_name": "Phạm Văn Logout",
            "tenant_id": self.tenant_id
        }
        
        requests.post(f"{AUTH_URL}/register", json=user)
        
        login_response = requests.post(
            f"{AUTH_URL}/login",
            json={"email": user["email"], "password": user["password"]}
        )
        
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]
        
        response = requests.post(
            f"{AUTH_URL}/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )
        
        assert response.status_code == 200
        
        print("[OK] Logout successful")
    
    def test_10_regional_validation(self):
        """Test 10: Regional location validation"""
        user = {
            "email": f"regional_{uuid4().hex[:8]}@verisyntra.com",
            "password": "SecurePass123!",
            "full_name": "Vũ Thị Regional",
            "tenant_id": self.tenant_id,
            "regional_location": "invalid_region"
        }
        
        response = requests.post(f"{AUTH_URL}/register", json=user)
        
        assert response.status_code == 422
        print("[OK] Invalid regional_location correctly rejected")


if __name__ == "__main__":
    # Run tests standalone
    print("=" * 70)
    print("VeriSyntra Phase 2 Authentication Integration Tests")
    print("Kiểm thử tích hợp xác thực VeriSyntra Phase 2")
    print("=" * 70)
    print()
    
    test = TestPhase2Authentication()
    # Manually call setup logic (not the pytest fixture)
    test.tenant_id = create_test_tenant()
    test.test_user = {
        "email": f"test_{uuid4().hex[:8]}@verisyntra.com",
        "password": "SecurePass123!",
        "full_name": "Nguyễn Văn Test",
        "full_name_vi": "Nguyễn Văn Test",
        "phone_number": "+84 901 234 567",
        "tenant_id": test.tenant_id
    }
    test.access_token = None
    test.refresh_token = None
    
    tests = [
        ("Server Health Check", test.test_01_server_health),
        ("User Registration", test.test_02_user_registration),
        ("Duplicate Email Prevention", test.test_03_duplicate_email),
        ("User Login", test.test_04_user_login),
        ("Invalid Login", test.test_05_invalid_login),
        ("Protected Endpoint No Token", test.test_06_protected_endpoint_no_token),
        ("Protected Endpoint With Token", test.test_07_protected_endpoint_with_token),
        ("Token Refresh", test.test_08_token_refresh),
        ("User Logout", test.test_09_user_logout),
        ("Regional Location Validation", test.test_10_regional_validation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"--- Test: {test_name} ---")
        try:
            test_func()
            print(f"[PASSED] {test_name}")
            passed += 1
        except Exception as e:
            print(f"[FAILED] {test_name}")
            print(f"[ERROR] {str(e)}")
            failed += 1
        print()
    
    print("=" * 70)
    print("Test Results | Kết quả kiểm thử")
    print("=" * 70)
    print(f"Total: {len(tests)} | Passed: {passed} | Failed: {failed}")
    print(f"Tổng: {len(tests)} | Thành công: {passed} | Thất bại: {failed}")
    print("=" * 70)
