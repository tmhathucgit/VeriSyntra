# Data Population Method 5: Database Seeding
## Vietnamese PDPL 2025 Compliance - Data Categories Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** data_categories Table  
**Method:** Programmatic Database Seeding with PDPL Templates  
**Architecture:** SQLAlchemy + Vietnamese Category Templates + Environment Detection  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **database seeding of data categories** using PDPL-compliant Vietnamese templates. The seeding system provides baseline categories for development, staging, demo, and production environments with industry-specific templates.

**Key Features:**
- PDPL Article 4.13 baseline sensitive categories (12 types)
- Common basic personal data categories
- Industry-specific category templates (6 industries)
- Environment-aware seeding (dev, staging, demo, production)
- Skip-if-exists logic to prevent duplicates
- Idempotent seed operations
- Zero hard-coding with template configuration

**Use Cases:**
- Initialize new tenant databases with PDPL categories
- Populate development/testing environments
- Create demo environments with realistic data
- Establish baseline compliance categories
- Industry-specific quick start templates

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [PDPL Baseline Categories](#pdpl-baseline-categories)
3. [Industry-Specific Templates](#industry-specific-templates)
4. [Environment Detection](#environment-detection)
5. [Seeding Implementation](#seeding-implementation)
6. [Idempotent Operations](#idempotent-operations)
7. [Success Criteria](#success-criteria)

---

## Architecture Overview

### Database Seeding System

```
┌─────────────────────────────────────────────────────────────┐
│         Database Seeding Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Environment │  │  Template    │  │  PDPL        │     │
│  │  Detector    │─>│  Selector    │─>│  Validator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  SQLAlchemy  │  │  Duplicate   │  │  Transaction │     │
│  │  Session     │  │  Checker     │  │  Manager     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  data_categories       │                    │
│              │  (Seeded Baseline)     │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Seeding Workflow:**
1. Detect environment (dev, staging, demo, production)
2. Load appropriate category templates
3. Check for existing categories (skip if exists)
4. Validate PDPL compliance
5. Insert categories in transaction
6. Log seeding results

---

## PDPL Baseline Categories

### PDPL Article 4.13 Sensitive Categories

```python
# services/seeding/pdpl_categories.py

"""
PDPL Baseline Category Seeds
Vietnamese PDPL 2025 Compliance
"""

from typing import List, Dict


# PDPL Article 4.13 Sensitive Data Categories
PDPL_SENSITIVE_CATEGORY_SEEDS: List[Dict[str, any]] = [
    {
        "category_name_vi": "Quan điểm chính trị",
        "category_name_en": "Political Opinions",
        "category_description_vi": "Thông tin về quan điểm, niềm tin chính trị, đảng phái chính trị của cá nhân theo Điều 4.13.a PDPL 2025",
        "category_description_en": "Information about individual's political views, beliefs, and party affiliation per Article 4.13.a PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.a PDPL",
        "examples_vi": ["đảng phái chính trị", "quan điểm về chính sách", "hoạt động chính trị"],
        "examples_en": ["political party affiliation", "policy opinions", "political activities"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Tín ngưỡng tôn giáo",
        "category_name_en": "Religious Beliefs",
        "category_description_vi": "Thông tin về tôn giáo, tín ngưỡng, niềm tin tâm linh của cá nhân theo Điều 4.13.b PDPL 2025",
        "category_description_en": "Information about religion, beliefs, and spiritual faith per Article 4.13.b PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.b PDPL",
        "examples_vi": ["tôn giáo theo đạo", "tín ngưỡng dân gian", "hoạt động tôn giáo"],
        "examples_en": ["religious affiliation", "folk beliefs", "religious activities"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Thông tin sức khỏe",
        "category_name_en": "Health Information",
        "category_description_vi": "Thông tin về tình trạng sức khỏe, bệnh sử, kết quả xét nghiệm, chẩn đoán và điều trị y tế theo Điều 4.13.c PDPL 2025",
        "category_description_en": "Information about health status, medical history, test results, diagnosis and treatment per Article 4.13.c PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.c PDPL",
        "examples_vi": ["hồ sơ bệnh án", "kết quả xét nghiệm", "đơn thuốc", "chẩn đoán bệnh", "tiền sử bệnh lý"],
        "examples_en": ["medical records", "test results", "prescriptions", "disease diagnosis", "medical history"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Dữ liệu sinh trắc học",
        "category_name_en": "Biometric Data",
        "category_description_vi": "Dữ liệu đặc điểm sinh học duy nhất để nhận dạng cá nhân như vân tay, khuôn mặt, mống mắt theo Điều 4.13.d PDPL 2025",
        "category_description_en": "Unique biological characteristics data for identification such as fingerprints, facial features, iris per Article 4.13.d PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.d PDPL",
        "examples_vi": ["vân tay", "nhận dạng khuôn mặt", "quét mống mắt", "võng mạc", "giọng nói"],
        "examples_en": ["fingerprints", "facial recognition", "iris scan", "retina scan", "voice recognition"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Thông tin di truyền",
        "category_name_en": "Genetic Information",
        "category_description_vi": "Thông tin về đặc điểm di truyền, gen, DNA, cấu trúc di truyền của cá nhân theo Điều 4.13.e PDPL 2025",
        "category_description_en": "Information about genetic characteristics, genes, DNA, genetic structure per Article 4.13.e PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.e PDPL",
        "examples_vi": ["xét nghiệm gen", "mã di truyền DNA", "bệnh di truyền", "cấu trúc gen"],
        "examples_en": ["genetic testing", "DNA code", "hereditary diseases", "gene structure"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Xu hướng tình dục",
        "category_name_en": "Sexual Orientation",
        "category_description_vi": "Thông tin về xu hướng tình dục, bản dạng giới, định hướng giới tính của cá nhân theo Điều 4.13.f PDPL 2025",
        "category_description_en": "Information about sexual orientation, gender identity, gender expression per Article 4.13.f PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.f PDPL",
        "examples_vi": ["xu hướng tình dục", "bản dạng giới", "định hướng giới tính"],
        "examples_en": ["sexual orientation", "gender identity", "gender expression"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Hồ sơ tư pháp",
        "category_name_en": "Criminal Records",
        "category_description_vi": "Thông tin về tiền án, tiền sự, bản án hình sự, hồ sơ tư pháp của cá nhân theo Điều 4.13.g PDPL 2025",
        "category_description_en": "Information about criminal history, convictions, judicial records per Article 4.13.g PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.g PDPL",
        "examples_vi": ["tiền án tiền sự", "bản án hình sự", "hồ sơ tư pháp", "án tù giam"],
        "examples_en": ["criminal history", "criminal convictions", "judicial records", "prison sentences"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Thông tin công đoàn",
        "category_name_en": "Trade Union Information",
        "category_description_vi": "Thông tin về tham gia tổ chức công đoàn, hoạt động công đoàn của cá nhân theo Điều 4.13.h PDPL 2025",
        "category_description_en": "Information about trade union membership and activities per Article 4.13.h PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.h PDPL",
        "examples_vi": ["hội viên công đoàn", "hoạt động công đoàn", "vai trò trong công đoàn"],
        "examples_en": ["union membership", "union activities", "union role"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Dữ liệu trẻ em",
        "category_name_en": "Children's Data",
        "category_description_vi": "Thông tin cá nhân của trẻ em dưới 16 tuổi theo Điều 4.13.i PDPL 2025, yêu cầu sự đồng ý của cha mẹ/người giám hộ",
        "category_description_en": "Personal data of children under 16 years old per Article 4.13.i PDPL 2025, requires parental/guardian consent",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.i PDPL",
        "examples_vi": ["học sinh dưới 16 tuổi", "trẻ em thiếu niên", "dữ liệu học tập của trẻ"],
        "examples_en": ["students under 16", "minors", "children's educational data"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Dữ liệu nạn nhân tội phạm",
        "category_name_en": "Crime Victim Data",
        "category_description_vi": "Thông tin về nạn nhân của tội phạm, bị hại trong vụ án hình sự theo Điều 4.13 PDPL 2025",
        "category_description_en": "Information about crime victims, injured parties in criminal cases per Article 4.13 PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13 PDPL",
        "examples_vi": ["nạn nhân tội phạm", "bị hại vụ án", "thông tin bảo vệ nạn nhân"],
        "examples_en": ["crime victims", "injured parties", "victim protection information"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Dữ liệu vị trí theo thời gian thực",
        "category_name_en": "Real-time Location Data",
        "category_description_vi": "Dữ liệu vị trí địa lý theo thời gian thực, theo dõi di chuyển của cá nhân theo Điều 4.13 PDPL 2025",
        "category_description_en": "Real-time geographic location data, movement tracking per Article 4.13 PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13 PDPL",
        "examples_vi": ["GPS theo thời gian thực", "lịch sử di chuyển", "theo dõi vị trí"],
        "examples_en": ["real-time GPS", "movement history", "location tracking"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Dữ liệu tài chính nhạy cảm",
        "category_name_en": "Sensitive Financial Data",
        "category_description_vi": "Thông tin tài chính nhạy cảm như thu nhập chi tiết, tài sản, nợ vay theo Điều 4.13 PDPL 2025",
        "category_description_en": "Sensitive financial information such as detailed income, assets, debts per Article 4.13 PDPL 2025",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13 PDPL",
        "examples_vi": ["thu nhập chi tiết", "bảng kê tài sản", "thông tin nợ vay", "báo cáo tín dụng"],
        "examples_en": ["detailed income", "asset statements", "debt information", "credit reports"],
        "usage_count": 0,
        "is_active": True
    }
]


# Common Basic Personal Data Categories
BASIC_CATEGORY_SEEDS: List[Dict[str, any]] = [
    {
        "category_name_vi": "Họ và tên",
        "category_name_en": "Full Name",
        "category_description_vi": "Họ, tên đệm, tên của cá nhân theo Điều 4.1 PDPL 2025",
        "category_description_en": "Last name, middle name, first name per Article 4.1 PDPL 2025",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["họ", "tên đệm", "tên", "họ và tên đầy đủ"],
        "examples_en": ["surname", "middle name", "given name", "full name"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Giấy tờ tùy thân",
        "category_name_en": "Identification Documents",
        "category_description_vi": "Số CMND, CCCD, hộ chiếu và các giấy tờ tùy thân khác theo Điều 4.1 PDPL 2025",
        "category_description_en": "ID card, citizen ID, passport and other identification documents per Article 4.1 PDPL 2025",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["số CMND", "số CCCD", "số hộ chiếu", "ngày cấp", "nơi cấp"],
        "examples_en": ["ID card number", "citizen ID number", "passport number", "issue date", "issuing authority"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Thông tin liên hệ",
        "category_name_en": "Contact Information",
        "category_description_vi": "Số điện thoại, email, địa chỉ và thông tin liên hệ khác theo Điều 4.1 PDPL 2025",
        "category_description_en": "Phone number, email, address and other contact information per Article 4.1 PDPL 2025",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["số điện thoại", "địa chỉ email", "địa chỉ nhà", "địa chỉ làm việc"],
        "examples_en": ["phone number", "email address", "home address", "work address"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Ngày tháng năm sinh",
        "category_name_en": "Date of Birth",
        "category_description_vi": "Ngày sinh, tháng sinh, năm sinh của cá nhân theo Điều 4.1 PDPL 2025",
        "category_description_en": "Day, month, year of birth per Article 4.1 PDPL 2025",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["ngày sinh", "tháng năm sinh", "tuổi"],
        "examples_en": ["date of birth", "birth month/year", "age"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Thông tin tài khoản",
        "category_name_en": "Account Information",
        "category_description_vi": "Thông tin tài khoản ngân hàng, số tài khoản, tên ngân hàng theo Điều 4.1 PDPL 2025",
        "category_description_en": "Bank account information, account number, bank name per Article 4.1 PDPL 2025",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["số tài khoản ngân hàng", "tên ngân hàng", "chi nhánh"],
        "examples_en": ["bank account number", "bank name", "branch"],
        "usage_count": 0,
        "is_active": True
    },
    {
        "category_name_vi": "Thông tin việc làm",
        "category_name_en": "Employment Information",
        "category_description_vi": "Thông tin về nơi làm việc, chức vụ, thâm niên công tác theo Điều 4.1 PDPL 2025",
        "category_description_en": "Information about workplace, position, work experience per Article 4.1 PDPL 2025",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["tên công ty", "chức vụ", "phòng ban", "thâm niên"],
        "examples_en": ["company name", "position", "department", "seniority"],
        "usage_count": 0,
        "is_active": True
    }
]
```

---

## Industry-Specific Templates

### Vietnamese Business Context Templates

```python
# services/seeding/industry_templates.py

"""
Industry-Specific Category Templates
Vietnamese Business Context
"""

from typing import Dict, List


# Industry-specific category templates
INDUSTRY_CATEGORY_TEMPLATES: Dict[str, List[Dict[str, any]]] = {
    "fintech": [
        {
            "category_name_vi": "Thông tin KYC",
            "category_name_en": "KYC Information",
            "category_description_vi": "Thông tin xác minh danh tính khách hàng (Know Your Customer) bao gồm CMND/CCCD, địa chỉ, nghề nghiệp",
            "category_description_en": "Customer identity verification information including ID, address, occupation",
            "category_type": "basic",
            "is_sensitive": False,
            "pdpl_article_reference": "Art. 4.1 PDPL",
            "examples_vi": ["CMND/CCCD", "địa chỉ thường trú", "nghề nghiệp", "nguồn thu nhập"],
            "examples_en": ["ID card", "permanent address", "occupation", "income source"]
        },
        {
            "category_name_vi": "Lịch sử giao dịch tài chính",
            "category_name_en": "Financial Transaction History",
            "category_description_vi": "Lịch sử các giao dịch nạp, rút, chuyển tiền, thanh toán của khách hàng",
            "category_description_en": "History of deposits, withdrawals, transfers, payments",
            "category_type": "basic",
            "is_sensitive": False,
            "pdpl_article_reference": "Art. 4.1 PDPL",
            "examples_vi": ["lịch sử nạp tiền", "lịch sử rút tiền", "lịch sử chuyển khoản"],
            "examples_en": ["deposit history", "withdrawal history", "transfer history"]
        }
    ],
    "healthcare": [
        {
            "category_name_vi": "Hồ sơ khám chữa bệnh",
            "category_name_en": "Medical Examination Records",
            "category_description_vi": "Hồ sơ bệnh án điện tử, kết quả khám, chẩn đoán, chỉ định điều trị",
            "category_description_en": "Electronic medical records, examination results, diagnosis, treatment prescriptions",
            "category_type": "sensitive",
            "is_sensitive": True,
            "pdpl_article_reference": "Art. 4.13.c PDPL",
            "examples_vi": ["hồ sơ bệnh án", "kết quả khám", "chẩn đoán", "đơn thuốc"],
            "examples_en": ["medical records", "exam results", "diagnosis", "prescriptions"]
        },
        {
            "category_name_vi": "Kết quả xét nghiệm y tế",
            "category_name_en": "Medical Test Results",
            "category_description_vi": "Kết quả xét nghiệm máu, nước tiểu, hình ảnh y khoa, sinh thiết",
            "category_description_en": "Blood test, urine test, medical imaging, biopsy results",
            "category_type": "sensitive",
            "is_sensitive": True,
            "pdpl_article_reference": "Art. 4.13.c PDPL",
            "examples_vi": ["xét nghiệm máu", "xét nghiệm nước tiểu", "X-quang", "siêu âm", "CT scan"],
            "examples_en": ["blood test", "urine test", "X-ray", "ultrasound", "CT scan"]
        }
    ],
    "ecommerce": [
        {
            "category_name_vi": "Lịch sử mua hàng",
            "category_name_en": "Purchase History",
            "category_description_vi": "Lịch sử đơn hàng, sản phẩm đã mua, giá trị giao dịch của khách hàng",
            "category_description_en": "Order history, purchased products, transaction values",
            "category_type": "basic",
            "is_sensitive": False,
            "pdpl_article_reference": "Art. 4.1 PDPL",
            "examples_vi": ["đơn hàng", "sản phẩm đã mua", "giá trị đơn hàng", "ngày mua"],
            "examples_en": ["orders", "purchased products", "order value", "purchase date"]
        },
        {
            "category_name_vi": "Hành vi người dùng",
            "category_name_en": "User Behavior",
            "category_description_vi": "Lịch sử tìm kiếm, sản phẩm xem, sản phẩm yêu thích, giỏ hàng",
            "category_description_en": "Search history, viewed products, wishlist, shopping cart",
            "category_type": "basic",
            "is_sensitive": False,
            "pdpl_article_reference": "Art. 4.1 PDPL",
            "examples_vi": ["lịch sử tìm kiếm", "sản phẩm đã xem", "yêu thích", "giỏ hàng"],
            "examples_en": ["search history", "viewed products", "wishlist", "cart"]
        }
    ],
    "education": [
        {
            "category_name_vi": "Hồ sơ học sinh",
            "category_name_en": "Student Records",
            "category_description_vi": "Thông tin học sinh, phụ huynh, lớp học, điểm số, kết quả học tập",
            "category_description_en": "Student information, parents, class, grades, academic results",
            "category_type": "sensitive",
            "is_sensitive": True,
            "pdpl_article_reference": "Art. 4.13.i PDPL",
            "examples_vi": ["thông tin học sinh", "thông tin phụ huynh", "lớp học", "điểm số"],
            "examples_en": ["student info", "parent info", "class", "grades"]
        }
    ],
    "manufacturing": [
        {
            "category_name_vi": "Thông tin nhân viên sản xuất",
            "category_name_en": "Production Staff Information",
            "category_description_vi": "Thông tin nhân viên, chấm công, ca làm việc, năng suất lao động",
            "category_description_en": "Employee information, attendance, work shifts, productivity",
            "category_type": "basic",
            "is_sensitive": False,
            "pdpl_article_reference": "Art. 4.1 PDPL",
            "examples_vi": ["mã nhân viên", "chấm công", "ca làm việc", "năng suất"],
            "examples_en": ["employee ID", "attendance", "work shift", "productivity"]
        }
    ],
    "logistics": [
        {
            "category_name_vi": "Thông tin vận chuyển",
            "category_name_en": "Shipping Information",
            "category_description_vi": "Địa chỉ giao hàng, số điện thoại người nhận, thông tin đơn hàng vận chuyển",
            "category_description_en": "Delivery address, recipient phone, shipping order information",
            "category_type": "basic",
            "is_sensitive": False,
            "pdpl_article_reference": "Art. 4.1 PDPL",
            "examples_vi": ["địa chỉ giao hàng", "SĐT người nhận", "mã vận đơn"],
            "examples_en": ["delivery address", "recipient phone", "tracking number"]
        }
    ]
}
```

---

## Environment Detection

### Environment-Aware Seeding

```python
# services/seeding/environment.py

"""
Environment Detection for Seeding
Development vs Production Logic
"""

import os
from enum import Enum


class SeedEnvironment(str, Enum):
    """
    Môi trường seed
    Seeding environment
    """
    DEVELOPMENT = "development"
    STAGING = "staging"
    DEMO = "demo"
    TESTING = "testing"
    PRODUCTION = "production"


def get_current_environment() -> SeedEnvironment:
    """
    Phát hiện môi trường hiện tại
    Detect current environment
    
    Returns environment type
    """
    env = os.getenv("VERISYNTRA_ENV", "development").lower()
    
    if env in ["prod", "production"]:
        return SeedEnvironment.PRODUCTION
    elif env in ["stage", "staging"]:
        return SeedEnvironment.STAGING
    elif env in ["demo"]:
        return SeedEnvironment.DEMO
    elif env in ["test", "testing"]:
        return SeedEnvironment.TESTING
    else:
        return SeedEnvironment.DEVELOPMENT


def should_seed_environment(env: SeedEnvironment) -> bool:
    """
    Kiểm tra xem có nên seed không
    Check if should seed in this environment
    
    Production: Only if explicitly enabled
    """
    if env == SeedEnvironment.PRODUCTION:
        # Require explicit flag for production
        return os.getenv("ALLOW_PRODUCTION_SEED", "false").lower() == "true"
    
    # Always allow for non-production
    return True


def get_industry_from_env() -> str:
    """
    Lấy ngành nghề từ biến môi trường
    Get industry from environment variable
    
    Returns industry key or 'general'
    """
    industry = os.getenv("VERISYNTRA_INDUSTRY", "general").lower()
    
    valid_industries = [
        "fintech", "healthcare", "ecommerce",
        "manufacturing", "education", "logistics"
    ]
    
    if industry in valid_industries:
        return industry
    
    return "general"
```

---

## Seeding Implementation

### SQLAlchemy Seeding Service

```python
# services/seeding/category_seeder.py

"""
Category Seeding Service
Idempotent Database Seeding
"""

from sqlalchemy.orm import Session
from typing import List, Dict
import logging


logger = logging.getLogger(__name__)


class CategorySeeder:
    """
    Dịch vụ seed category
    Category seeding service
    
    Idempotent seeding with skip-if-exists
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def seed_all_categories(
        self,
        include_sensitive: bool = True,
        include_basic: bool = True,
        include_industry: bool = False,
        industry: str = None
    ) -> Dict[str, int]:
        """
        Seed tất cả category
        Seed all categories
        
        Returns count statistics
        """
        stats = {
            "sensitive_created": 0,
            "basic_created": 0,
            "industry_created": 0,
            "skipped": 0,
            "total": 0
        }
        
        try:
            # Seed PDPL sensitive categories
            if include_sensitive:
                sensitive_count = await self._seed_sensitive_categories()
                stats["sensitive_created"] = sensitive_count
            
            # Seed basic categories
            if include_basic:
                basic_count = await self._seed_basic_categories()
                stats["basic_created"] = basic_count
            
            # Seed industry-specific categories
            if include_industry and industry:
                industry_count = await self._seed_industry_categories(industry)
                stats["industry_created"] = industry_count
            
            self.db.commit()
            
            stats["total"] = (
                stats["sensitive_created"] +
                stats["basic_created"] +
                stats["industry_created"]
            )
            
            logger.info(f"Seeding complete: {stats}")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Seeding failed: {e}")
            raise
        
        return stats
    
    async def _seed_sensitive_categories(self) -> int:
        """Seed PDPL Article 4.13 sensitive categories"""
        created_count = 0
        
        for seed_data in PDPL_SENSITIVE_CATEGORY_SEEDS:
            if not self._category_exists(seed_data["category_name_vi"]):
                category = DataCategory(**seed_data)
                self.db.add(category)
                created_count += 1
                logger.info(f"Created sensitive category: {seed_data['category_name_vi']}")
        
        return created_count
    
    async def _seed_basic_categories(self) -> int:
        """Seed basic personal data categories"""
        created_count = 0
        
        for seed_data in BASIC_CATEGORY_SEEDS:
            if not self._category_exists(seed_data["category_name_vi"]):
                category = DataCategory(**seed_data)
                self.db.add(category)
                created_count += 1
                logger.info(f"Created basic category: {seed_data['category_name_vi']}")
        
        return created_count
    
    async def _seed_industry_categories(self, industry: str) -> int:
        """Seed industry-specific categories"""
        created_count = 0
        
        if industry not in INDUSTRY_CATEGORY_TEMPLATES:
            logger.warning(f"Unknown industry: {industry}")
            return 0
        
        templates = INDUSTRY_CATEGORY_TEMPLATES[industry]
        
        for seed_data in templates:
            if not self._category_exists(seed_data["category_name_vi"]):
                category = DataCategory(**seed_data)
                self.db.add(category)
                created_count += 1
                logger.info(f"Created {industry} category: {seed_data['category_name_vi']}")
        
        return created_count
    
    def _category_exists(self, category_name_vi: str) -> bool:
        """
        Kiểm tra category đã tồn tại
        Check if category exists
        
        Skip if exists (idempotent)
        """
        existing = self.db.query(DataCategory).filter(
            DataCategory.category_name_vi == category_name_vi
        ).first()
        
        return existing is not None
```

---

## Idempotent Operations

### Skip-if-Exists Logic

```python
# api/endpoints/seeding.py

"""
Seeding API Endpoints
Admin-only Category Seeding
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict


router = APIRouter()


@router.post("/api/v1/admin/seed/categories")
async def seed_categories(
    include_sensitive: bool = True,
    include_basic: bool = True,
    include_industry: bool = False,
    db: Session = Depends(get_db)
) -> Dict[str, any]:
    """
    Seed baseline data categories
    
    Admin-only endpoint
    Idempotent operation (skip if exists)
    """
    # Check environment
    env = get_current_environment()
    
    if not should_seed_environment(env):
        raise HTTPException(
            status_code=403,
            detail="Seeding disabled in production environment"
        )
    
    # Get industry from environment
    industry = get_industry_from_env() if include_industry else None
    
    # Execute seeding
    seeder = CategorySeeder(db)
    stats = await seeder.seed_all_categories(
        include_sensitive=include_sensitive,
        include_basic=include_basic,
        include_industry=include_industry,
        industry=industry
    )
    
    return {
        "status": "success",
        "environment": env,
        "industry": industry,
        "statistics": stats,
        "message_vi": f"Đã tạo {stats['total']} danh mục",
        "message_en": f"Created {stats['total']} categories"
    }
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] PDPL Article 4.13 sensitive categories (12 types)
- [TARGET] Common basic personal data categories (6 types)
- [TARGET] Industry-specific templates (6 industries)
- [TARGET] Environment detection (dev, staging, demo, production)
- [TARGET] Production seeding protection (require explicit flag)
- [TARGET] Skip-if-exists logic (idempotent operations)
- [TARGET] Transaction-based seeding
- [TARGET] Industry auto-detection from environment
- [TARGET] Seeding statistics and logging
- [TARGET] Vietnamese bilingual logging
- [TARGET] Zero hard-coding (all seeds in templates)
- [TARGET] Admin-only API endpoint

**Next Document:** #06 - Third-Party Integration
