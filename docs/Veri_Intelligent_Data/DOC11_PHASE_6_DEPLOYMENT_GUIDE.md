# VeriSyntra Data Inventory - Deployment Guide

**Document:** DOC11 Phase 6 - Deployment Documentation  
**Vietnamese PDPL 2025 Compliance Platform**  
**Version:** 1.0  
**Date:** November 6, 2025

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [PostgreSQL Database Setup](#postgresql-database-setup)
3. [Environment Configuration](#environment-configuration)
4. [Schema Migration](#schema-migration)
5. [Vietnamese Timezone Configuration](#vietnamese-timezone-configuration)
6. [Multi-Tenant Setup](#multi-tenant-setup)
7. [Production Checklist](#production-checklist)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Backup and Recovery](#backup-and-recovery)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Operating System:** Ubuntu 20.04 LTS or higher, Windows Server 2019+, or macOS 10.15+
- **Python:** 3.10+ with pip
- **PostgreSQL:** 14+ (with async support)
- **Memory:** Minimum 4GB RAM (8GB recommended for production)
- **Storage:** 20GB+ available disk space
- **Network:** Stable internet connection for package installation

### Required Software
```bash
# PostgreSQL server
postgresql-14
postgresql-contrib-14

# Python dependencies
python3.10+
python3-pip
python3-venv

# Optional: Redis for caching (future enhancement)
redis-server
```

---

## PostgreSQL Database Setup

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
# Add PostgreSQL repository
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Install PostgreSQL 14
sudo apt update
sudo apt install postgresql-14 postgresql-contrib-14
```

**Windows:**
- Download installer from https://www.postgresql.org/download/windows/
- Run installer and follow wizard
- Default port: 5432
- Set strong password for postgres user

**macOS:**
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14
```

### 2. Create Database and User

```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database for VeriSyntra
CREATE DATABASE verisyntra_data_inventory
    WITH ENCODING='UTF8'
    LC_COLLATE='vi_VN.UTF-8'  -- Vietnamese locale
    LC_CTYPE='vi_VN.UTF-8'
    TEMPLATE=template0;

-- Create application user
CREATE USER verisyntra_app WITH PASSWORD 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE verisyntra_data_inventory TO verisyntra_app;

-- Connect to the database
\c verisyntra_data_inventory

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO verisyntra_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO verisyntra_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO verisyntra_app;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT ALL ON TABLES TO verisyntra_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT ALL ON SEQUENCES TO verisyntra_app;
```

### 3. Configure PostgreSQL for Async Connections

**Edit `postgresql.conf`:**
```ini
# Connection settings for async support
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB

# Performance tuning
random_page_cost = 1.1  # For SSD
effective_io_concurrency = 200

# WAL settings (for better write performance)
wal_buffers = 16MB
checkpoint_completion_target = 0.9

# Logging (for production monitoring)
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_min_duration_statement = 1000  # Log slow queries (>1s)
```

**Restart PostgreSQL:**
```bash
# Ubuntu/Debian
sudo systemctl restart postgresql

# macOS
brew services restart postgresql@14

# Windows
net stop postgresql-x64-14
net start postgresql-x64-14
```

---

## Environment Configuration

### 1. Create Environment File

Create `.env` file in `backend/veri_ai_data_inventory/`:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://verisyntra_app:your_secure_password_here@localhost:5432/verisyntra_data_inventory

# Vietnamese Timezone (CRITICAL for PDPL compliance)
TIMEZONE=Asia/Ho_Chi_Minh

# Application Settings
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# Security Settings
SECRET_KEY=your_secret_key_here_minimum_32_characters
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# ROPA Storage
ROPA_STORAGE_DIR=./ropa_storage

# Optional: Redis Cache (for future enhancement)
# REDIS_URL=redis://localhost:6379/0

# Optional: Sentry Error Tracking
# SENTRY_DSN=https://your-sentry-dsn-here
```

### 2. Install Python Dependencies

```bash
cd backend/veri_ai_data_inventory

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install additional production dependencies
pip install gunicorn uvicorn[standard] python-dotenv
```

**requirements.txt should include:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
pytz==2023.3
pytest==7.4.3
pytest-asyncio==0.21.1
aiosqlite==0.19.0  # For testing only
```

---

## Schema Migration

### 1. Initialize Alembic (if not already done)

```bash
cd backend/veri_ai_data_inventory

# Initialize Alembic
alembic init alembic

# Edit alembic.ini
# Set sqlalchemy.url to use DATABASE_URL from env
```

**Edit `alembic/env.py`:**
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your models
from database.base import Base
from models.db_models import *

# Set target metadata
target_metadata = Base.metadata

# Get database URL from environment
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
```

### 2. Run Schema Migration

**Option A: Direct SQL (Recommended for first deployment)**
```bash
# Connect to database
psql -U verisyntra_app -d verisyntra_data_inventory

# Run schema.sql
\i backend/veri_ai_data_inventory/database/schema.sql

# Verify tables created
\dt

# Expected output: 9 tables
# processing_activities
# data_categories
# data_subjects
# data_recipients
# data_retention
# security_measures
# processing_locations
# ropa_documents
# data_inventory_audit
```

**Option B: Alembic Migration (For updates)**
```bash
# Generate migration
alembic revision --autogenerate -m "Initial schema"

# Review migration file in alembic/versions/

# Apply migration
alembic upgrade head

# Verify current version
alembic current
```

### 3. Verify Schema

```sql
-- Check all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Check indexes created
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Verify Vietnamese timezone function
SELECT to_vietnamese_time(NOW());
-- Expected: Timestamp in Asia/Ho_Chi_Minh timezone
```

---

## Vietnamese Timezone Configuration

### 1. Verify System Timezone

**Linux:**
```bash
# Check current timezone
timedatectl

# Set to Vietnamese timezone
sudo timedatectl set-timezone Asia/Ho_Chi_Minh

# Verify
date
```

**Windows:**
```powershell
# Check current timezone
Get-TimeZone

# Set to Vietnamese timezone
Set-TimeZone -Id "SE Asia Standard Time"
```

### 2. PostgreSQL Timezone Configuration

**Edit `postgresql.conf`:**
```ini
# Vietnamese timezone for PDPL compliance
timezone = 'Asia/Ho_Chi_Minh'
```

**Verify in SQL:**
```sql
SHOW timezone;
-- Expected: Asia/Ho_Chi_Minh

SELECT NOW();
-- Should show Vietnamese time (UTC+7)
```

### 3. Application Timezone Configuration

Ensure all datetime operations use Vietnamese timezone:

```python
# services/constants.py
VIETNAM_TIMEZONE = 'Asia/Ho_Chi_Minh'

# All datetime conversions
import pytz
vietnam_tz = pytz.timezone(VIETNAM_TIMEZONE)
vietnam_time = datetime.now(vietnam_tz)
```

---

## Multi-Tenant Setup

### 1. Tenant Isolation Strategy

**Database Level:**
- All tables include `tenant_id` column (UUID)
- All queries MUST include `WHERE tenant_id = ?`
- Indexes on `tenant_id` for performance
- Foreign key constraints enforce data integrity

**Application Level:**
```python
# Every CRUD operation requires tenant_id
activities = await get_processing_activities_for_tenant(
    db=db,
    tenant_id=tenant_id  # REQUIRED
)

# API endpoints extract tenant_id from path
@router.get("/api/v1/data-inventory/{tenant_id}/ropa/...")
```

### 2. Create Initial Tenant

```python
# Run in Python shell or create migration script
import asyncio
from uuid import uuid4
from database.connection import get_db

async def create_initial_tenant():
    async for db in get_db():
        # Create tenant record (if tenants table exists)
        tenant_id = uuid4()
        # INSERT INTO tenants (tenant_id, name, ...) VALUES (...)
        
        print(f"Tenant created: {tenant_id}")
        return tenant_id

# Run
asyncio.run(create_initial_tenant())
```

### 3. Tenant Data Isolation Testing

```bash
# Run multi-tenant isolation tests
pytest tests/test_database_integration.py::test_multi_tenant_isolation -v
pytest tests/test_database_integration.py::test_cascade_delete_isolation -v
```

---

## Production Checklist

### Pre-Deployment

- [ ] PostgreSQL 14+ installed and running
- [ ] Database created with Vietnamese locale (vi_VN.UTF-8)
- [ ] Application user created with secure password
- [ ] All tables created (9 tables expected)
- [ ] All indexes created (30+ indexes)
- [ ] Vietnamese timezone configured (Asia/Ho_Chi_Minh)
- [ ] Environment variables configured (.env file)
- [ ] Python dependencies installed (requirements.txt)
- [ ] Schema migration completed successfully

### Security

- [ ] Strong database password set (min 16 characters)
- [ ] SECRET_KEY generated (min 32 random characters)
- [ ] Database user has minimal required privileges
- [ ] PostgreSQL configured to require password authentication
- [ ] Firewall rules limit database access to application server only
- [ ] SSL/TLS enabled for database connections (production)
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Debug mode disabled (DEBUG=false)

### Performance

- [ ] PostgreSQL tuned for production workload
- [ ] Indexes verified with `EXPLAIN ANALYZE`
- [ ] Connection pooling configured (asyncpg)
- [ ] Slow query logging enabled (log_min_duration_statement)
- [ ] Resource limits set (max_connections, shared_buffers)

### Monitoring

- [ ] PostgreSQL logs being collected
- [ ] Application logs configured (LOG_LEVEL=INFO)
- [ ] Disk space monitoring enabled
- [ ] Database connection monitoring
- [ ] Error tracking configured (optional: Sentry)

### Backup

- [ ] Automated backups scheduled (daily minimum)
- [ ] Backup retention policy defined (30 days recommended)
- [ ] Backup restoration tested successfully
- [ ] Off-site backup storage configured
- [ ] Point-in-time recovery enabled (PostgreSQL WAL archiving)

### Vietnamese PDPL Compliance

- [ ] Vietnamese timezone enforced (Asia/Ho_Chi_Minh)
- [ ] Bilingual support verified (Vietnamese primary, English fallback)
- [ ] Audit logs enabled for all operations
- [ ] MPS compliance checking functional
- [ ] Cross-border transfer detection working
- [ ] Sensitive data classification implemented
- [ ] Retention policy enforcement configured

---

## Monitoring and Maintenance

### 1. Health Checks

**Database Health:**
```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('verisyntra_data_inventory'));

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Check long-running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;
```

**Application Health:**
```bash
# Check API is responding
curl http://localhost:8010/health

# Check database connection from app
python -c "from database.connection import check_database_connection; import asyncio; asyncio.run(check_database_connection())"
```

### 2. Performance Monitoring

**Query Performance:**
```sql
-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slow queries
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- Unused indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

### 3. Maintenance Tasks

**Daily:**
- Monitor disk space usage
- Check error logs
- Verify backup completion

**Weekly:**
- Review slow query log
- Analyze database growth trends
- Check for unused indexes

**Monthly:**
- Vacuum and analyze database
- Review and optimize queries
- Update PostgreSQL statistics
- Security audit

**Quarterly:**
- Test backup restoration
- Review and update retention policies
- Performance tuning review
- Dependency updates

---

## Backup and Recovery

### 1. Automated Backup Script

**backup_database.sh:**
```bash
#!/bin/bash

# Configuration
DB_NAME="verisyntra_data_inventory"
DB_USER="verisyntra_app"
BACKUP_DIR="/var/backups/verisyntra"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U $DB_USER -Fc $DB_NAME > $BACKUP_DIR/backup_${DATE}.dump

# Compress backup
gzip $BACKUP_DIR/backup_${DATE}.dump

# Remove old backups
find $BACKUP_DIR -name "backup_*.dump.gz" -mtime +$RETENTION_DAYS -delete

# Log backup completion
echo "[OK] Backup completed: backup_${DATE}.dump.gz"
```

**Schedule with cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup_database.sh >> /var/log/verisyntra_backup.log 2>&1
```

### 2. Restore from Backup

```bash
# Restore from compressed backup
gunzip -c /var/backups/verisyntra/backup_20251106_020000.dump.gz | pg_restore -U verisyntra_app -d verisyntra_data_inventory --clean

# Verify restoration
psql -U verisyntra_app -d verisyntra_data_inventory -c "SELECT COUNT(*) FROM processing_activities;"
```

### 3. Point-in-Time Recovery (WAL Archiving)

**Enable WAL archiving in `postgresql.conf`:**
```ini
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /var/lib/postgresql/wal_archive/%f && cp %p /var/lib/postgresql/wal_archive/%f'
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Errors**

**Error:** `asyncpg.exceptions.InvalidCatalogNameError: database "verisyntra_data_inventory" does not exist`

**Solution:**
```bash
# Verify database exists
psql -U postgres -c "\l"

# Create if missing
createdb -U postgres verisyntra_data_inventory
```

**2. Permission Errors**

**Error:** `asyncpg.exceptions.InsufficientPrivilegeError: permission denied for table`

**Solution:**
```sql
-- Grant all privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO verisyntra_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO verisyntra_app;
```

**3. Timezone Issues**

**Error:** Timestamps showing wrong timezone

**Solution:**
```sql
-- Verify PostgreSQL timezone
SHOW timezone;

-- Set to Vietnamese timezone
ALTER DATABASE verisyntra_data_inventory SET timezone TO 'Asia/Ho_Chi_Minh';
```

**4. Migration Conflicts**

**Error:** Alembic migration conflicts

**Solution:**
```bash
# Check current version
alembic current

# Downgrade to previous version
alembic downgrade -1

# Fix conflicts in migration file

# Re-upgrade
alembic upgrade head
```

**5. Slow Queries**

**Error:** Queries taking too long

**Solution:**
```sql
-- Analyze query plan
EXPLAIN ANALYZE SELECT * FROM processing_activities WHERE tenant_id = 'uuid';

-- Check if index is being used
-- Expected: Index Scan on idx_pa_tenant_id

-- If not using index, recreate it
DROP INDEX IF EXISTS idx_pa_tenant_id;
CREATE INDEX idx_pa_tenant_id ON processing_activities(tenant_id);
```

### Debug Mode

**Enable debug logging temporarily:**
```env
# .env
DEBUG=true
LOG_LEVEL=DEBUG
```

```python
# In application
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Support and Resources

### Documentation
- Vietnamese PDPL 2025 Law: https://thuvienphapluat.vn/van-ban/Bo-may-hanh-chinh/Luat-bao-ve-du-lieu-ca-nhan-2024-91-2025-QH15-615833.aspx
- Decree 13/2023/ND-CP: https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Nghi-dinh-13-2023-ND-CP-bao-ve-du-lieu-ca-nhan-linh-vuc-thuong-mai-dien-tu-545748.aspx
- PostgreSQL Documentation: https://www.postgresql.org/docs/14/
- SQLAlchemy Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- FastAPI: https://fastapi.tiangolo.com/

### Contact
- Technical Support: tech@verisyntra.vn
- PDPL Compliance: compliance@verisyntra.vn
- Emergency: +84-xxx-xxx-xxxx (24/7)

---

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Next Review:** December 6, 2025
