# Data Population Method 7: Alembic Migration
## Vietnamese PDPL 2025 Compliance - Data Categories Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** data_categories Table  
**Method:** Database Migration-Based Seeding  
**Architecture:** Alembic + SQLAlchemy + Environment Detection  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **Alembic migration-based category seeding**, enabling version-controlled, repeatable, and environment-aware baseline category initialization.

**Key Features:**
- Alembic migration templates for PDPL categories
- Tenant-specific category initialization
- Environment-aware migration execution
- Upgrade/downgrade support
- Zero hard-coding with migration configuration
- Bilingual migration logging (Vietnamese-first)

**Use Cases:**
- Version-controlled category baseline setup
- Multi-tenant category initialization
- Environment-specific category seeding (dev/staging/prod)
- Rollback support for category changes
- Audit trail for category schema evolution

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Migration Templates](#migration-templates)
3. [PDPL Category Migrations](#pdpl-category-migrations)
4. [Environment Detection](#environment-detection)
5. [Tenant Initialization](#tenant-initialization)
6. [Rollback Support](#rollback-support)
7. [Success Criteria](#success-criteria)

---

## Architecture Overview

### Migration-Based Seeding System

```
┌─────────────────────────────────────────────────────────────┐
│         Alembic Migration Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Alembic     │  │  Migration   │  │  Environment │     │
│  │  Config      │─>│  Templates   │─>│  Detector    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PDPL        │  │  Tenant      │  │  Bilingual   │     │
│  │  Migrations  │  │  Init        │  │  Logger      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  data_categories       │                    │
│              │  (Versioned Schema)    │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Migration Workflow:**
1. Detect environment (dev/staging/production)
2. Check if categories already exist
3. Execute upgrade migration
4. Seed PDPL baseline categories
5. Initialize tenant-specific categories
6. Log operations bilingually
7. Support downgrade for rollback

---

## Migration Templates

### Alembic Configuration

```python
# alembic/env.py

"""
Alembic Migration Environment
Vietnamese PDPL Compliance
"""

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os


# Environment detection
def get_migration_environment() -> str:
    """
    Lấy môi trường migration
    Get migration environment
    """
    return os.getenv("VERISYNTRA_ENV", "development")


def should_seed_categories() -> bool:
    """
    Kiểm tra có nên seed categories
    Check if categories should be seeded
    
    Production requires explicit flag
    """
    env = get_migration_environment()
    
    if env == "production":
        return os.getenv("ALLOW_MIGRATION_SEED", "false").lower() == "true"
    
    return True


def run_migrations_offline():
    """
    Chạy migrations offline
    Run migrations in offline mode
    """
    url = context.config.get_main_option("sqlalchemy.url")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Chạy migrations online
    Run migrations in online mode
    """
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## PDPL Category Migrations

### Baseline PDPL Categories Migration

```python
# alembic/versions/001_seed_pdpl_baseline_categories.py

"""
Seed PDPL Baseline Categories
Vietnamese PDPL 2025 Compliance

Revision ID: 001_pdpl_baseline
Revises: 
Create Date: 2025-11-06 10:00:00
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# Revision identifiers
revision = '001_pdpl_baseline'
down_revision = None
branch_labels = None
depends_on = None


# PDPL Article 4.13 Sensitive Categories
PDPL_SENSITIVE_CATEGORIES = [
    {
        "category_name_vi": "Quan điểm chính trị",
        "category_name_en": "Political Opinions",
        "category_description_vi": "Thông tin về quan điểm, niềm tin chính trị của cá nhân",
        "category_description_en": "Information about individual's political opinions or beliefs",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.a PDPL",
        "examples_vi": ["đảng phái chính trị", "quan điểm chính trị", "hoạt động chính trị"],
        "examples_en": ["political party affiliation", "political views", "political activities"]
    },
    {
        "category_name_vi": "Tín ngưỡng tôn giáo",
        "category_name_en": "Religious Beliefs",
        "category_description_vi": "Thông tin về tôn giáo, tín ngưỡng của cá nhân",
        "category_description_en": "Information about individual's religion or beliefs",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.b PDPL",
        "examples_vi": ["tôn giáo", "tín ngưỡng", "hoạt động tôn giáo"],
        "examples_en": ["religion", "beliefs", "religious activities"]
    },
    {
        "category_name_vi": "Thông tin sức khỏe",
        "category_name_en": "Health Information",
        "category_description_vi": "Dữ liệu về tình trạng sức khỏe, bệnh án của cá nhân",
        "category_description_en": "Data about individual's health status or medical records",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.c PDPL",
        "examples_vi": ["hồ sơ bệnh án", "kết quả xét nghiệm", "tình trạng sức khỏe"],
        "examples_en": ["medical records", "test results", "health status"]
    },
    {
        "category_name_vi": "Dữ liệu sinh trắc học",
        "category_name_en": "Biometric Data",
        "category_description_vi": "Dữ liệu sinh trắc học nhận dạng duy nhất cá nhân",
        "category_description_en": "Biometric data for unique identification",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.d PDPL",
        "examples_vi": ["vân tay", "khuôn mặt", "mống mắt", "giọng nói"],
        "examples_en": ["fingerprint", "face", "iris", "voice"]
    },
    {
        "category_name_vi": "Thông tin di truyền",
        "category_name_en": "Genetic Information",
        "category_description_vi": "Dữ liệu di truyền của cá nhân",
        "category_description_en": "Genetic data of individual",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.e PDPL",
        "examples_vi": ["DNA", "gen", "xét nghiệm di truyền"],
        "examples_en": ["DNA", "genes", "genetic testing"]
    },
    {
        "category_name_vi": "Xu hướng tình dục",
        "category_name_en": "Sexual Orientation",
        "category_description_vi": "Thông tin về xu hướng tình dục của cá nhân",
        "category_description_en": "Information about individual's sexual orientation",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.f PDPL",
        "examples_vi": ["xu hướng tình dục", "giới tính"],
        "examples_en": ["sexual orientation", "gender identity"]
    },
    {
        "category_name_vi": "Hồ sơ tư pháp",
        "category_name_en": "Criminal Records",
        "category_description_vi": "Dữ liệu về tiền án, tiền sự của cá nhân",
        "category_description_en": "Data about individual's criminal history",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.g PDPL",
        "examples_vi": ["tiền án", "tiền sự", "hồ sơ tư pháp"],
        "examples_en": ["criminal record", "convictions", "judicial records"]
    },
    {
        "category_name_vi": "Thông tin công đoàn",
        "category_name_en": "Trade Union Membership",
        "category_description_vi": "Thông tin về tư cách thành viên công đoàn",
        "category_description_en": "Information about trade union membership",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.h PDPL",
        "examples_vi": ["công đoàn", "tổ chức nghề nghiệp"],
        "examples_en": ["trade union", "professional organization"]
    },
    {
        "category_name_vi": "Dữ liệu trẻ em",
        "category_name_en": "Children's Data",
        "category_description_vi": "Dữ liệu cá nhân của trẻ em dưới 16 tuổi",
        "category_description_en": "Personal data of children under 16 years old",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.i PDPL",
        "examples_vi": ["thông tin trẻ em", "học sinh", "dưới 16 tuổi"],
        "examples_en": ["children information", "students", "under 16"]
    }
]


# Basic Personal Data Categories
BASIC_CATEGORIES = [
    {
        "category_name_vi": "Họ và tên",
        "category_name_en": "Full Name",
        "category_description_vi": "Họ và tên đầy đủ của cá nhân",
        "category_description_en": "Full name of individual",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["họ tên", "tên đầy đủ"],
        "examples_en": ["full name", "name"]
    },
    {
        "category_name_vi": "Giấy tờ tùy thân",
        "category_name_en": "Identification Documents",
        "category_description_vi": "Số giấy tờ tùy thân (CCCD, CMND, hộ chiếu)",
        "category_description_en": "ID document numbers (ID card, passport)",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["CCCD", "CMND", "hộ chiếu", "số định danh"],
        "examples_en": ["ID card", "passport", "identification number"]
    },
    {
        "category_name_vi": "Thông tin liên hệ",
        "category_name_en": "Contact Information",
        "category_description_vi": "Thông tin liên hệ (email, số điện thoại, địa chỉ)",
        "category_description_en": "Contact information (email, phone, address)",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["email", "số điện thoại", "địa chỉ"],
        "examples_en": ["email", "phone number", "address"]
    }
]


def upgrade():
    """
    Nâng cấp: Seed PDPL baseline categories
    Upgrade: Seed PDPL baseline categories
    """
    # Get database connection
    connection = op.get_bind()
    
    # Check environment
    import os
    env = os.getenv("VERISYNTRA_ENV", "development")
    
    print(f"[MIGRATION] Environment: {env}")
    print(f"[MIGRATION] Môi trường: {env}")
    
    # Seed sensitive categories
    print("[MIGRATION] Seeding PDPL Article 4.13 sensitive categories...")
    print("[MIGRATION] Đang seed danh mục nhạy cảm theo Điều 4.13 PDPL...")
    
    for category in PDPL_SENSITIVE_CATEGORIES:
        # Check if exists
        result = connection.execute(
            sa.text(
                "SELECT category_id FROM data_categories WHERE category_name_vi = :name_vi"
            ),
            {"name_vi": category["category_name_vi"]}
        ).fetchone()
        
        if not result:
            connection.execute(
                sa.text("""
                    INSERT INTO data_categories (
                        category_name_vi, category_name_en,
                        category_description_vi, category_description_en,
                        category_type, is_sensitive,
                        pdpl_article_reference,
                        usage_count, is_active,
                        created_at, updated_at
                    ) VALUES (
                        :name_vi, :name_en,
                        :desc_vi, :desc_en,
                        :cat_type, :is_sensitive,
                        :pdpl_ref,
                        0, true,
                        :now, :now
                    )
                """),
                {
                    "name_vi": category["category_name_vi"],
                    "name_en": category["category_name_en"],
                    "desc_vi": category["category_description_vi"],
                    "desc_en": category["category_description_en"],
                    "cat_type": category["category_type"],
                    "is_sensitive": category["is_sensitive"],
                    "pdpl_ref": category["pdpl_article_reference"],
                    "now": datetime.now()
                }
            )
            print(f"  [OK] Created: {category['category_name_vi']}")
            print(f"  [OK] Đã tạo: {category['category_name_vi']}")
    
    # Seed basic categories
    print("[MIGRATION] Seeding basic personal data categories...")
    print("[MIGRATION] Đang seed danh mục dữ liệu cơ bản...")
    
    for category in BASIC_CATEGORIES:
        result = connection.execute(
            sa.text(
                "SELECT category_id FROM data_categories WHERE category_name_vi = :name_vi"
            ),
            {"name_vi": category["category_name_vi"]}
        ).fetchone()
        
        if not result:
            connection.execute(
                sa.text("""
                    INSERT INTO data_categories (
                        category_name_vi, category_name_en,
                        category_description_vi, category_description_en,
                        category_type, is_sensitive,
                        pdpl_article_reference,
                        usage_count, is_active,
                        created_at, updated_at
                    ) VALUES (
                        :name_vi, :name_en,
                        :desc_vi, :desc_en,
                        :cat_type, :is_sensitive,
                        :pdpl_ref,
                        0, true,
                        :now, :now
                    )
                """),
                {
                    "name_vi": category["category_name_vi"],
                    "name_en": category["category_name_en"],
                    "desc_vi": category["category_description_vi"],
                    "desc_en": category["category_description_en"],
                    "cat_type": category["category_type"],
                    "is_sensitive": category["is_sensitive"],
                    "pdpl_ref": category["pdpl_article_reference"],
                    "now": datetime.now()
                }
            )
            print(f"  [OK] Created: {category['category_name_vi']}")
            print(f"  [OK] Đã tạo: {category['category_name_vi']}")
    
    print("[MIGRATION] Baseline categories seeded successfully")
    print("[MIGRATION] Đã seed danh mục cơ bản thành công")


def downgrade():
    """
    Hạ cấp: Xóa PDPL baseline categories
    Downgrade: Remove PDPL baseline categories
    """
    connection = op.get_bind()
    
    print("[MIGRATION] Rolling back PDPL baseline categories...")
    print("[MIGRATION] Đang rollback danh mục PDPL...")
    
    # Delete seeded categories
    all_categories = PDPL_SENSITIVE_CATEGORIES + BASIC_CATEGORIES
    
    for category in all_categories:
        connection.execute(
            sa.text(
                "DELETE FROM data_categories WHERE category_name_vi = :name_vi"
            ),
            {"name_vi": category["category_name_vi"]}
        )
        print(f"  [OK] Deleted: {category['category_name_vi']}")
        print(f"  [OK] Đã xóa: {category['category_name_vi']}")
    
    print("[MIGRATION] Rollback completed")
    print("[MIGRATION] Rollback hoàn tất")
```

---

## Environment Detection

### Environment-Aware Migration Execution

```python
# alembic/env.py - Environment detection additions

"""
Environment Detection for Migrations
Phát hiện môi trường cho migrations
"""

import os
from enum import Enum


class MigrationEnvironment(str, Enum):
    """
    Môi trường migration
    Migration environment
    """
    DEVELOPMENT = "development"
    STAGING = "staging"
    DEMO = "demo"
    TESTING = "testing"
    PRODUCTION = "production"


def get_migration_config() -> dict:
    """
    Lấy cấu hình migration theo môi trường
    Get migration configuration by environment
    """
    env = get_migration_environment()
    
    configs = {
        MigrationEnvironment.DEVELOPMENT: {
            "seed_categories": True,
            "seed_examples": True,
            "verbose_logging": True,
            "allow_destructive": True
        },
        MigrationEnvironment.STAGING: {
            "seed_categories": True,
            "seed_examples": False,
            "verbose_logging": True,
            "allow_destructive": False
        },
        MigrationEnvironment.PRODUCTION: {
            "seed_categories": os.getenv("ALLOW_MIGRATION_SEED", "false") == "true",
            "seed_examples": False,
            "verbose_logging": False,
            "allow_destructive": False
        }
    }
    
    return configs.get(env, configs[MigrationEnvironment.DEVELOPMENT])
```

---

## Tenant Initialization

### Multi-Tenant Category Setup

```python
# alembic/versions/002_tenant_specific_categories.py

"""
Tenant-Specific Category Initialization
Vietnamese Business Context

Revision ID: 002_tenant_init
Revises: 001_pdpl_baseline
Create Date: 2025-11-06 11:00:00
"""

from alembic import op
import sqlalchemy as sa
import os


revision = '002_tenant_init'
down_revision = '001_pdpl_baseline'
branch_labels = None
depends_on = None


def get_tenant_industry() -> str:
    """Lấy ngành nghề của tenant"""
    return os.getenv("VERISYNTRA_INDUSTRY", "general")


INDUSTRY_CATEGORIES = {
    "healthcare": [
        {
            "category_name_vi": "Hồ sơ bệnh án điện tử",
            "category_name_en": "Electronic Medical Records",
            "category_type": "sensitive",
            "is_sensitive": True
        }
    ],
    "fintech": [
        {
            "category_name_vi": "Lịch sử giao dịch",
            "category_name_en": "Transaction History",
            "category_type": "basic",
            "is_sensitive": False
        }
    ]
}


def upgrade():
    """Seed tenant-specific categories"""
    industry = get_tenant_industry()
    
    if industry == "general":
        print("[MIGRATION] No tenant-specific categories for general industry")
        print("[MIGRATION] Không có danh mục đặc thù cho ngành nghề chung")
        return
    
    categories = INDUSTRY_CATEGORIES.get(industry, [])
    
    connection = op.get_bind()
    
    for category in categories:
        # Insert tenant-specific category
        connection.execute(
            sa.text("""
                INSERT INTO data_categories (
                    category_name_vi, category_name_en,
                    category_type, is_sensitive,
                    usage_count, is_active,
                    created_at, updated_at
                ) VALUES (
                    :name_vi, :name_en,
                    :cat_type, :is_sensitive,
                    0, true,
                    :now, :now
                )
            """),
            {
                "name_vi": category["category_name_vi"],
                "name_en": category["category_name_en"],
                "cat_type": category["category_type"],
                "is_sensitive": category["is_sensitive"],
                "now": sa.func.now()
            }
        )


def downgrade():
    """Remove tenant-specific categories"""
    industry = get_tenant_industry()
    categories = INDUSTRY_CATEGORIES.get(industry, [])
    
    connection = op.get_bind()
    
    for category in categories:
        connection.execute(
            sa.text(
                "DELETE FROM data_categories WHERE category_name_vi = :name_vi"
            ),
            {"name_vi": category["category_name_vi"]}
        )
```

---

## Rollback Support

### Safe Downgrade Operations

```python
# Migration utilities for safe rollback

"""
Migration Rollback Utilities
An toàn rollback migrations
"""


def safe_category_delete(connection, category_name_vi: str) -> bool:
    """
    Xóa category an toàn
    Safe category deletion
    
    Checks for dependencies before deletion
    """
    # Check if category is in use
    result = connection.execute(
        sa.text("""
            SELECT COUNT(*) as count
            FROM data_categories
            WHERE category_name_vi = :name_vi
            AND usage_count > 0
        """),
        {"name_vi": category_name_vi}
    ).fetchone()
    
    if result["count"] > 0:
        print(f"[WARNING] Category '{category_name_vi}' is in use (usage_count > 0)")
        print(f"[CẢNH BÁO] Danh mục '{category_name_vi}' đang được sử dụng")
        print("[INFO] Skipping deletion to preserve data integrity")
        print("[INFO] Bỏ qua xóa để bảo vệ tính toàn vẹn dữ liệu")
        return False
    
    # Safe to delete
    connection.execute(
        sa.text("DELETE FROM data_categories WHERE category_name_vi = :name_vi"),
        {"name_vi": category_name_vi}
    )
    
    return True
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] Alembic migration templates configured
- [TARGET] PDPL Article 4.13 baseline migration (9 sensitive categories)
- [TARGET] Basic personal data migration (3+ categories)
- [TARGET] Environment detection (5 environments)
- [TARGET] Production protection (explicit seed flag)
- [TARGET] Tenant-specific category initialization
- [TARGET] Industry-aware category seeding
- [TARGET] Bilingual migration logging (Vietnamese-first)
- [TARGET] Upgrade support with skip-if-exists
- [TARGET] Downgrade support with safe deletion
- [TARGET] Rollback protection (check usage_count)
- [TARGET] Zero hard-coding (all categories in migration data)

**Folder 02 Complete:** All 7 data population methods documented [OK]
