-- Role-Permission mapping table
-- VeriSyntra Standard: ASCII identifiers, Vietnamese comments
-- Task 1.1.3 RBAC - Step 2
-- Date: November 8, 2025

CREATE TABLE IF NOT EXISTS role_permissions (
    role_permission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role VARCHAR(50) NOT NULL,  -- admin, dpo, compliance_manager, staff, auditor, viewer
    permission_id UUID REFERENCES permissions(permission_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(role, permission_id)
);

-- Index for fast role permission lookups
CREATE INDEX IF NOT EXISTS idx_role_permissions_role ON role_permissions(role);

-- Vietnamese role definitions and their permissions
-- Role: admin - Quản trị viên (full access)
INSERT INTO role_permissions (role, permission_id)
SELECT 'admin', permission_id FROM permissions
ON CONFLICT (role, permission_id) DO NOTHING;  -- Admin has ALL permissions

-- Role: dpo - Nhân viên bảo vệ dữ liệu (Data Protection Officer)
INSERT INTO role_permissions (role, permission_id)
SELECT 'dpo', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read', 'processing_activity.write', 'processing_activity.delete',
    'data_category.read', 'data_category.write', 'data_category.manage_sensitive',
    'ropa.read', 'ropa.generate', 'ropa.approve', 'ropa.export',
    'data_subject.read', 'data_subject.write',
    'data_recipient.read', 'data_recipient.write',
    'security_measure.read', 'security_measure.write',
    'user.read',
    'audit.read',
    'analytics.read'
)
ON CONFLICT (role, permission_id) DO NOTHING;

-- Role: compliance_manager - Quản lý tuân thủ
INSERT INTO role_permissions (role, permission_id)
SELECT 'compliance_manager', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read', 'processing_activity.write',
    'data_category.read', 'data_category.write',
    'ropa.read', 'ropa.generate', 'ropa.export',
    'data_subject.read', 'data_subject.write',
    'data_recipient.read', 'data_recipient.write',
    'security_measure.read',
    'audit.read',
    'analytics.read'
)
ON CONFLICT (role, permission_id) DO NOTHING;

-- Role: staff - Nhân viên
INSERT INTO role_permissions (role, permission_id)
SELECT 'staff', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read', 'processing_activity.write',
    'data_category.read', 'data_category.write',
    'ropa.read',
    'data_subject.read',
    'data_recipient.read',
    'security_measure.read'
)
ON CONFLICT (role, permission_id) DO NOTHING;

-- Role: auditor - Kiểm toán viên (read-only + audit logs)
INSERT INTO role_permissions (role, permission_id)
SELECT 'auditor', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read',
    'data_category.read',
    'ropa.read', 'ropa.export',
    'data_subject.read',
    'data_recipient.read',
    'security_measure.read',
    'audit.read',
    'analytics.read'
)
ON CONFLICT (role, permission_id) DO NOTHING;

-- Role: viewer - Người xem (read-only, limited)
INSERT INTO role_permissions (role, permission_id)
SELECT 'viewer', permission_id FROM permissions WHERE permission_name IN (
    'processing_activity.read',
    'data_category.read',
    'ropa.read'
)
ON CONFLICT (role, permission_id) DO NOTHING;

-- Verify role mappings
DO $$
DECLARE
    role_count INTEGER;
BEGIN
    SELECT COUNT(DISTINCT role) INTO role_count FROM role_permissions;
    RAISE NOTICE 'Role-Permission mappings created for % roles', role_count;
    
    -- Display counts per role
    FOR role_count IN 
        SELECT role, COUNT(*) as perm_count 
        FROM role_permissions 
        GROUP BY role 
        ORDER BY role
    LOOP
        RAISE NOTICE 'Role: %, Permissions: %', role_count;
    END LOOP;
END $$;
