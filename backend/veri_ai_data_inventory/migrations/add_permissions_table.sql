-- Permissions table - defines all available permissions
-- VeriSyntra Standard: ASCII identifiers, Vietnamese comments
-- Task 1.1.3 RBAC - Step 1
-- Date: November 8, 2025

CREATE TABLE IF NOT EXISTS permissions (
    permission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    permission_name VARCHAR(100) UNIQUE NOT NULL,  -- e.g., 'processing_activity.read'
    permission_name_vi VARCHAR(255) NOT NULL,      -- Vietnamese display name
    resource VARCHAR(50) NOT NULL,                 -- e.g., 'processing_activity'
    action VARCHAR(50) NOT NULL,                   -- e.g., 'read', 'write', 'delete'
    description TEXT,
    description_vi TEXT,                           -- Mo ta (tieng Viet)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast permission lookups
CREATE INDEX IF NOT EXISTS idx_permissions_name ON permissions(permission_name);
CREATE INDEX IF NOT EXISTS idx_permissions_resource ON permissions(resource);

-- Insert PDPL-specific permissions
INSERT INTO permissions (permission_name, permission_name_vi, resource, action, description, description_vi) VALUES
-- Processing Activities (Hoat dong xu ly)
('processing_activity.read', 'Xem hoạt động xử lý', 'processing_activity', 'read', 
 'View processing activities', 'Xem các hoạt động xử lý dữ liệu cá nhân'),
('processing_activity.write', 'Tạo/sửa hoạt động xử lý', 'processing_activity', 'write',
 'Create and update processing activities', 'Tạo và cập nhật hoạt động xử lý'),
('processing_activity.delete', 'Xóa hoạt động xử lý', 'processing_activity', 'delete',
 'Delete processing activities', 'Xóa hoạt động xử lý'),

-- Data Categories (Danh muc du lieu)
('data_category.read', 'Xem danh mục dữ liệu', 'data_category', 'read',
 'View data categories', 'Xem danh mục dữ liệu cá nhân'),
('data_category.write', 'Tạo/sửa danh mục dữ liệu', 'data_category', 'write',
 'Create and update data categories', 'Tạo và cập nhật danh mục'),
('data_category.delete', 'Xóa danh mục dữ liệu', 'data_category', 'delete',
 'Delete data categories', 'Xóa danh mục dữ liệu'),
('data_category.manage_sensitive', 'Quản lý dữ liệu nhạy cảm', 'data_category', 'manage_sensitive',
 'Handle PDPL Article 4.13 sensitive data', 'Xử lý dữ liệu nhạy cảm theo Điều 4.13 PDPL'),

-- ROPA (So dang ky hoat dong xu ly)
('ropa.read', 'Xem ROPA', 'ropa', 'read',
 'View ROPA documents', 'Xem sổ đăng ký hoạt động xử lý'),
('ropa.generate', 'Tạo ROPA', 'ropa', 'generate',
 'Generate ROPA documents', 'Tạo sổ đăng ký hoạt động xử lý'),
('ropa.approve', 'Phê duyệt ROPA', 'ropa', 'approve',
 'DPO approval authority for ROPA', 'Quyền phê duyệt ROPA của DPO'),
('ropa.export', 'Xuất ROPA', 'ropa', 'export',
 'Export ROPA in various formats', 'Xuất ROPA sang các định dạng'),

-- Data Subjects (Chu the du lieu)
('data_subject.read', 'Xem chủ thể dữ liệu', 'data_subject', 'read',
 'View data subjects', 'Xem thông tin chủ thể dữ liệu'),
('data_subject.write', 'Tạo/sửa chủ thể dữ liệu', 'data_subject', 'write',
 'Create and update data subjects', 'Tạo và cập nhật chủ thể dữ liệu'),

-- Data Recipients (Ben nhan du lieu)
('data_recipient.read', 'Xem bên nhận dữ liệu', 'data_recipient', 'read',
 'View data recipients', 'Xem thông tin bên nhận dữ liệu'),
('data_recipient.write', 'Tạo/sửa bên nhận dữ liệu', 'data_recipient', 'write',
 'Create and update data recipients', 'Tạo và cập nhật bên nhận dữ liệu'),

-- Security Measures (Bien phap bao mat)
('security_measure.read', 'Xem biện pháp bảo mật', 'security_measure', 'read',
 'View security measures', 'Xem các biện pháp bảo mật'),
('security_measure.write', 'Tạo/sửa biện pháp bảo mật', 'security_measure', 'write',
 'Create and update security measures', 'Tạo và cập nhật biện pháp bảo mật'),

-- User Management (Quan ly nguoi dung)
('user.read', 'Xem người dùng', 'user', 'read',
 'View users in tenant', 'Xem người dùng trong tenant'),
('user.write', 'Tạo/sửa người dùng', 'user', 'write',
 'Create and update users', 'Tạo và cập nhật người dùng'),
('user.delete', 'Xóa người dùng', 'user', 'delete',
 'Deactivate users', 'Vô hiệu hóa người dùng'),

-- Audit Logs (Nhat ky kiem toan)
('audit.read', 'Xem nhật ký kiểm toán', 'audit', 'read',
 'View audit logs', 'Xem nhật ký kiểm toán'),

-- Analytics (Phan tich)
('analytics.read', 'Xem phân tích', 'analytics', 'read',
 'View analytics and reports', 'Xem phân tích và báo cáo')
ON CONFLICT (permission_name) DO NOTHING;

-- Verification query
SELECT COUNT(*) as total_permissions FROM permissions;
