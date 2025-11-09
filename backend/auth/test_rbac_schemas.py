"""
Test RBAC Schemas - VeriSyntra Standards
Verify Pydantic models and bilingual error messages

Task: 1.1.3 RBAC - Step 3
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from auth.rbac_schemas import (
    PermissionSchema,
    RoleSchema,
    UserWithPermissionsSchema,
    PermissionCheckResult,
    RBACErrorMessages,
    get_role_display_name,
    validate_role,
    VALID_ROLES,
    ROLE_PERMISSION_COUNTS
)


def test_permission_schema():
    """Test PermissionSchema creation"""
    print("\n[TEST] PermissionSchema")
    
    permission = PermissionSchema(
        permission_id="123e4567-e89b-12d3-a456-426614174000",
        permission_name="processing_activity.read",
        permission_name_vi="Xem hoạt động xử lý",
        resource="processing_activity",
        action="read",
        description="View processing activities",
        description_vi="Xem các hoạt động xử lý dữ liệu cá nhân"
    )
    
    assert permission.permission_name == "processing_activity.read"
    assert permission.permission_name_vi == "Xem hoạt động xử lý"
    assert permission.resource == "processing_activity"
    assert permission.action == "read"
    print("[OK] PermissionSchema creation successful")
    print(f"  Permission: {permission.permission_name}")
    print(f"  Vietnamese: {permission.permission_name_vi}")


def test_user_with_permissions_schema():
    """Test UserWithPermissionsSchema"""
    print("\n[TEST] UserWithPermissionsSchema")
    
    user = UserWithPermissionsSchema(
        user_id="user-123",
        email="dpo@verisyntra.vn",
        full_name="Nguyen Van A",
        full_name_vi="Nguyễn Văn A",
        tenant_id="tenant-123",
        role="dpo",
        role_vi="Nhân viên bảo vệ dữ liệu",
        is_active=True,
        permissions=[
            "processing_activity.read",
            "processing_activity.write",
            "ropa.approve"
        ]
    )
    
    assert user.role == "dpo"
    assert user.role_vi == "Nhân viên bảo vệ dữ liệu"
    assert len(user.permissions) == 3
    assert "ropa.approve" in user.permissions
    print("[OK] UserWithPermissionsSchema creation successful")
    print(f"  User: {user.email}")
    print(f"  Role: {user.role_vi}")
    print(f"  Permissions: {len(user.permissions)}")


def test_permission_check_result():
    """Test PermissionCheckResult"""
    print("\n[TEST] PermissionCheckResult")
    
    # Allowed case
    result_allowed = PermissionCheckResult(
        allowed=True,
        permission="processing_activity.read",
        user_role="dpo",
        reason="User has required permission",
        reason_vi="Người dùng có quyền cần thiết"
    )
    
    assert result_allowed.allowed is True
    assert result_allowed.user_role == "dpo"
    print("[OK] PermissionCheckResult (allowed) creation successful")
    
    # Denied case
    result_denied = PermissionCheckResult(
        allowed=False,
        permission="processing_activity.delete",
        user_role="viewer",
        reason="Permission denied",
        reason_vi="Từ chối quyền truy cập"
    )
    
    assert result_denied.allowed is False
    assert result_denied.reason_vi == "Từ chối quyền truy cập"
    print("[OK] PermissionCheckResult (denied) creation successful")


def test_rbac_error_messages():
    """Test bilingual error messages"""
    print("\n[TEST] RBACErrorMessages")
    
    # Test Vietnamese message
    msg_vi = RBACErrorMessages.get_message(
        'PERMISSION_DENIED',
        'vi',
        permission='processing_activity.write'
    )
    assert "Từ chối quyền truy cập" in msg_vi
    assert "processing_activity.write" in msg_vi
    print(f"[OK] Vietnamese: {msg_vi}")
    
    # Test English message
    msg_en = RBACErrorMessages.get_message(
        'PERMISSION_DENIED',
        'en',
        permission='processing_activity.write'
    )
    assert "Permission denied" in msg_en
    assert "processing_activity.write" in msg_en
    print(f"[OK] English: {msg_en}")
    
    # Test TENANT_ACCESS_DENIED
    tenant_msg_vi = RBACErrorMessages.get_message('TENANT_ACCESS_DENIED', 'vi')
    assert "tenant" in tenant_msg_vi.lower()
    print(f"[OK] Tenant access denied: {tenant_msg_vi}")
    
    # Test INACTIVE_USER
    inactive_msg = RBACErrorMessages.get_message('INACTIVE_USER', 'vi')
    assert "vô hiệu hóa" in inactive_msg
    print(f"[OK] Inactive user: {inactive_msg}")


def test_role_display_names():
    """Test role display name retrieval"""
    print("\n[TEST] Role Display Names")
    
    # Test all roles in Vietnamese
    roles_vi = {
        'admin': 'Quản trị viên',
        'dpo': 'Nhân viên bảo vệ dữ liệu',
        'compliance_manager': 'Quản lý tuân thủ',
        'staff': 'Nhân viên',
        'auditor': 'Kiểm toán viên',
        'viewer': 'Người xem'
    }
    
    for role, expected_vi in roles_vi.items():
        actual_vi = get_role_display_name(role, 'vi')
        assert actual_vi == expected_vi, f"Expected {expected_vi}, got {actual_vi}"
        print(f"[OK] {role} -> {actual_vi}")
    
    # Test English
    admin_en = get_role_display_name('admin', 'en')
    assert admin_en == 'Administrator'
    print(f"[OK] Admin (EN): {admin_en}")


def test_role_validation():
    """Test role validation"""
    print("\n[TEST] Role Validation")
    
    # Valid roles
    valid_test_roles = ['admin', 'dpo', 'viewer', 'staff']
    for role in valid_test_roles:
        assert validate_role(role) is True
        print(f"[OK] Valid role: {role}")
    
    # Invalid roles
    invalid_test_roles = ['superadmin', 'guest', 'unknown']
    for role in invalid_test_roles:
        assert validate_role(role) is False
        print(f"[OK] Invalid role detected: {role}")


def test_valid_roles_list():
    """Test VALID_ROLES constant"""
    print("\n[TEST] VALID_ROLES List")
    
    assert len(VALID_ROLES) == 6
    expected_roles = ['admin', 'dpo', 'compliance_manager', 'staff', 'auditor', 'viewer']
    
    for role in expected_roles:
        assert role in VALID_ROLES
        print(f"[OK] {role} in VALID_ROLES")


def test_role_permission_counts():
    """Test ROLE_PERMISSION_COUNTS"""
    print("\n[TEST] Role Permission Counts")
    
    expected_counts = {
        'admin': 22,
        'dpo': 19,
        'compliance_manager': 14,
        'staff': 8,
        'auditor': 9,
        'viewer': 3
    }
    
    for role, expected_count in expected_counts.items():
        actual_count = ROLE_PERMISSION_COUNTS.get(role)
        assert actual_count == expected_count, f"{role}: expected {expected_count}, got {actual_count}"
        print(f"[OK] {role}: {actual_count} permissions")


def test_vietnamese_diacritics():
    """Test Vietnamese diacritics preservation"""
    print("\n[TEST] Vietnamese Diacritics")
    
    test_cases = [
        ("dpo", "Nhân viên bảo vệ dữ liệu"),
        ("compliance_manager", "Quản lý tuân thủ"),
        ("auditor", "Kiểm toán viên"),
        ("viewer", "Người xem")
    ]
    
    for role, expected_vi in test_cases:
        actual_vi = get_role_display_name(role, 'vi')
        # Check for Vietnamese diacritics
        has_diacritics = any(char in actual_vi for char in ['ả', 'ã', 'á', 'à', 'ạ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 
                                                              'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'đ', 'é', 'è', 'ẻ', 'ẽ', 'ẹ',
                                                              'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'í', 'ì', 'ỉ', 'ĩ', 'ị',
                                                              'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ',
                                                              'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'ú', 'ù', 'ủ', 'ũ', 'ụ',
                                                              'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ'])
        if has_diacritics:
            print(f"[OK] {role} has Vietnamese diacritics: {actual_vi}")
        else:
            print(f"[WARNING] {role} may not have diacritics: {actual_vi}")


def main():
    """Run all tests"""
    print("=" * 70)
    print("RBAC Schemas Test Suite - VeriSyntra Standards")
    print("=" * 70)
    
    try:
        test_permission_schema()
        test_user_with_permissions_schema()
        test_permission_check_result()
        test_rbac_error_messages()
        test_role_display_names()
        test_role_validation()
        test_valid_roles_list()
        test_role_permission_counts()
        test_vietnamese_diacritics()
        
        print("\n" + "=" * 70)
        print("[SUCCESS] All RBAC schema tests passed!")
        print("=" * 70)
        print("\n[OK] Pydantic schemas validated")
        print("[OK] Bilingual error messages working")
        print("[OK] Vietnamese diacritics preserved")
        print("[OK] Role validation working")
        print("[OK] Ready for Step 4 (CRUD Operations)")
        
        return 0
        
    except AssertionError as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
