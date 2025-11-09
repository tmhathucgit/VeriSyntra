-- Users table for authentication and authorization
-- Vietnamese business context: Supports multi-tenant isolation and regional preferences
-- PDPL 2025 Compliance: Secure password storage, audit logging

CREATE TABLE IF NOT EXISTS users (
    -- Primary key
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Authentication credentials
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Multi-tenant isolation
    tenant_id UUID NOT NULL,
    
    -- User profile (Vietnamese business context)
    full_name VARCHAR(255) NOT NULL,
    regional_location VARCHAR(20) CHECK (regional_location IN ('north', 'central', 'south')),
    
    -- Role-based access control (for Task 1.1.3)
    role VARCHAR(50) NOT NULL DEFAULT 'viewer' CHECK (role IN ('admin', 'compliance_officer', 'data_processor', 'viewer')),
    
    -- Account status
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_verified BOOLEAN NOT NULL DEFAULT false,
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by UUID,
    updated_by UUID,
    
    -- Foreign key constraints
    CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL,
    CONSTRAINT fk_updated_by FOREIGN KEY (updated_by) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Indexes for performance
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Comments (Vietnamese-first with proper diacritics)
COMMENT ON TABLE users IS 'Bảng người dùng - User authentication and authorization table';
COMMENT ON COLUMN users.user_id IS 'Mã người dùng - User unique identifier';
COMMENT ON COLUMN users.username IS 'Tên đăng nhập - Login username (unique)';
COMMENT ON COLUMN users.email IS 'Địa chỉ email - Email address (unique)';
COMMENT ON COLUMN users.password_hash IS 'Mật khẩu đã mã hóa - Bcrypt hashed password';
COMMENT ON COLUMN users.tenant_id IS 'Mã tổ chức - Multi-tenant isolation identifier';
COMMENT ON COLUMN users.full_name IS 'Họ tên - Full name with Vietnamese diacritics';
COMMENT ON COLUMN users.regional_location IS 'Khu vực - Regional business context (North/Central/South Vietnam)';
COMMENT ON COLUMN users.role IS 'Vai trò - User role for RBAC';
COMMENT ON COLUMN users.is_active IS 'Trạng thái hoạt động - Account active status';
COMMENT ON COLUMN users.is_verified IS 'Đã xác thực - Email verification status';
COMMENT ON COLUMN users.last_login_at IS 'Lần đăng nhập cuối - Last successful login timestamp';
COMMENT ON COLUMN users.failed_login_attempts IS 'Số lần đăng nhập thất bại - Failed login attempt count';
COMMENT ON COLUMN users.locked_until IS 'Khóa đến - Account lock expiration timestamp';
COMMENT ON COLUMN users.created_at IS 'Ngày tạo - Record creation timestamp';
COMMENT ON COLUMN users.updated_at IS 'Ngày cập nhật - Record last update timestamp';
COMMENT ON COLUMN users.created_by IS 'Người tạo - User ID who created this record';
COMMENT ON COLUMN users.updated_by IS 'Người cập nhật - User ID who last updated this record';
