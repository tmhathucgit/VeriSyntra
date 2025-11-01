-- ============================================
-- VeriSyntra Auth Service - Database Schema
-- ============================================
-- PostgreSQL initialization script
-- Vietnamese PDPL 2025 Compliance Platform
-- ============================================

-- Create database (already created by Docker, but kept for reference)
-- CREATE DATABASE verisyntra;

-- Connect to database
\c verisyntra;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Tenants Table (Vietnamese Businesses)
-- ============================================
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(200) NOT NULL,
    company_name_vi VARCHAR(200),
    tax_id VARCHAR(13),  -- Ma so thue
    
    -- Regional and industry context
    veri_regional_location VARCHAR(20) DEFAULT 'south' CHECK (veri_regional_location IN ('north', 'central', 'south')),
    veri_industry_type VARCHAR(50) DEFAULT 'technology',
    
    -- Subscription and billing
    subscription_tier VARCHAR(20) DEFAULT 'starter' CHECK (subscription_tier IN ('starter', 'professional', 'enterprise')),
    subscription_start_date TIMESTAMP,
    subscription_end_date TIMESTAMP,
    max_users INTEGER DEFAULT 10,
    
    -- Contact information
    primary_email VARCHAR(255),
    primary_phone VARCHAR(20),
    address TEXT,
    address_vi TEXT,
    city VARCHAR(100),
    province VARCHAR(100),  -- Tinh/Thanh pho
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- PDPL compliance
    data_residency_region VARCHAR(50) DEFAULT 'vietnam',
    pdpl_compliant BOOLEAN DEFAULT FALSE,
    
    -- Vietnamese business context (JSONB for flexibility)
    veri_business_context JSONB DEFAULT '{}'::JSONB,
    
    UNIQUE(tax_id)
);

-- ============================================
-- Users Table (Vietnamese Business Users)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    full_name_vi VARCHAR(100),  -- Ho va Ten
    phone_number VARCHAR(20),  -- Vietnamese phone format
    
    -- Multi-tenant relationship
    tenant_id UUID NOT NULL REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    
    -- User role
    role VARCHAR(30) DEFAULT 'staff' CHECK (role IN ('admin', 'dpo', 'compliance_manager', 'staff', 'auditor', 'viewer')),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_email_verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    
    -- Vietnamese preferences
    preferred_language VARCHAR(5) DEFAULT 'vi',
    timezone VARCHAR(50) DEFAULT 'Asia/Ho_Chi_Minh',
    
    UNIQUE(email, tenant_id)
);

-- ============================================
-- Refresh Tokens Table (JWT Token Management)
-- ============================================
CREATE TABLE IF NOT EXISTS refresh_tokens (
    token_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,  -- Hashed refresh token
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_revoked BOOLEAN DEFAULT FALSE,
    
    UNIQUE(token_hash)
);

-- ============================================
-- Audit Log Table (Vietnamese Compliance Tracking)
-- ============================================
CREATE TABLE IF NOT EXISTS audit_log (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    tenant_id UUID REFERENCES tenants(tenant_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,  -- login, logout, register, password_change, etc.
    details JSONB DEFAULT '{}'::JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    
    -- Vietnamese context
    vietnam_time TIMESTAMP DEFAULT NOW() AT TIME ZONE 'Asia/Ho_Chi_Minh'
);

-- ============================================
-- Indexes for Performance
-- ============================================

-- Users table indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON users(tenant_id);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Tenants table indexes
CREATE INDEX IF NOT EXISTS idx_tenants_tax_id ON tenants(tax_id);
CREATE INDEX IF NOT EXISTS idx_tenants_is_active ON tenants(is_active);
CREATE INDEX IF NOT EXISTS idx_tenants_subscription_tier ON tenants(subscription_tier);

-- Refresh tokens indexes
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_is_revoked ON refresh_tokens(is_revoked);

-- Audit log indexes
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_tenant_id ON audit_log(tenant_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);

-- ============================================
-- Triggers for updated_at Timestamps
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for tenants table
CREATE TRIGGER update_tenants_updated_at BEFORE UPDATE ON tenants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger for users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Insert Demo Data (Development Only)
-- ============================================

-- Demo tenant: VeriSyntra Vietnam
INSERT INTO tenants (
    tenant_id,
    company_name,
    company_name_vi,
    tax_id,
    veri_regional_location,
    veri_industry_type,
    subscription_tier,
    max_users,
    primary_email,
    primary_phone,
    city,
    province,
    is_active,
    is_verified,
    pdpl_compliant
) VALUES (
    '660e8400-e29b-41d4-a716-446655440001',
    'VeriSyntra Vietnam Co., Ltd.',
    'Cong ty TNHH VeriSyntra Viet Nam',
    '0123456789',
    'south',
    'technology',
    'professional',
    50,
    'contact@verisyntra.vn',
    '+84 28 1234 5678',
    'Ho Chi Minh City',
    'TP. Ho Chi Minh',
    TRUE,
    TRUE,
    TRUE
) ON CONFLICT DO NOTHING;

-- Demo user: Admin
-- Password: Admin123! (hashed with bcrypt)
INSERT INTO users (
    user_id,
    email,
    hashed_password,
    full_name,
    full_name_vi,
    phone_number,
    tenant_id,
    role,
    is_active,
    is_verified,
    is_email_verified,
    preferred_language
) VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'admin@verisyntra.vn',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5gyNTnLHgbxB6',  -- Admin123!
    'Nguyen Van Admin',
    'Nguyen Van Admin',
    '+84 901 234 567',
    '660e8400-e29b-41d4-a716-446655440001',
    'admin',
    TRUE,
    TRUE,
    TRUE,
    'vi'
) ON CONFLICT DO NOTHING;

-- ============================================
-- Database Info
-- ============================================

-- Display table information
SELECT 'VeriSyntra Auth Database Initialized' AS status;
SELECT 'Tables created: tenants, users, refresh_tokens, audit_log' AS info;
SELECT 'Demo tenant and admin user created' AS demo_data;
SELECT 'Admin credentials: admin@verisyntra.vn / Admin123!' AS credentials;
