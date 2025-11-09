# Data Population Method 7: Alembic Migration Initial Data
## Vietnamese PDPL 2025 Compliance - Processing Activities Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** processing_activities Table  
**Method:** Alembic Migration Scripts for Initial Data Seeding  
**Architecture:** Vietnamese-first Migration-Based Data Population  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **Alembic migration-based initial data seeding** for processing_activities table. This method uses database migration version control to manage initial data, common Vietnamese business activity templates, and industry-specific baseline configurations.

**Key Features:**
- Version-controlled data seeding via Alembic migrations
- Common Vietnamese business activity templates
- Industry-specific baseline configurations
- Tenant-specific conditional seeding
- Rollback support for data migrations
- Zero hard-coding with template configuration files

**Use Cases:**
- Initial database setup with baseline activities
- Multi-tenant onboarding with industry templates
- Version-controlled reference data management
- Standardized activity templates across tenants
- Migration-based data consistency

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Migration Structure](#migration-structure)
3. [Common Activity Templates](#common-activity-templates)
4. [Industry-Specific Baselines](#industry-specific-baselines)
5. [Tenant-Specific Seeding](#tenant-specific-seeding)
6. [Rollback Procedures](#rollback-procedures)
7. [Implementation Guide](#implementation-guide)

---

## Architecture Overview

### Migration-Based Seeding System

```
┌─────────────────────────────────────────────────────────────┐
│         Alembic Migration Seeding Architecture              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Migration   │  │  Template    │  │  Industry    │     │
│  │  Scripts     │─>│  Config      │─>│  Baselines   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Tenant      │  │  Conditional │  │  Version     │     │
│  │  Detection   │  │  Logic       │  │  Control     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  processing_activities │                    │
│              │  (baseline data)       │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Migration Workflow:**
1. Alembic migration executed during deployment
2. Load template configuration from constants
3. Detect tenant context (if applicable)
4. Apply conditional seeding logic
5. Insert baseline activities per industry
6. Track migration version in alembic_version table
7. Enable rollback if needed

---

## Migration Structure

### Migration File Organization

```python
# alembic/versions/0004_seed_baseline_activities.py

"""
Seed baseline processing activities for all industries

Revision ID: 0004_seed_baseline
Revises: 0003_seed_sample_activities
Create Date: 2025-11-06 18:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from datetime import datetime
import os

from database.migrations.templates.baseline_templates import (
    COMMON_ACTIVITY_TEMPLATES,
    INDUSTRY_BASELINE_TEMPLATES
)
from database.migrations.constants.migration_constants import (
    MIGRATION_CONFIG,
    MigrationEnvironment
)


# Revision identifiers
revision = '0004_seed_baseline'
down_revision = '0003_seed_sample_activities'
branch_labels = None
depends_on = None


# Migration Configuration
BASELINE_CONFIG = {
    "system_user_id": "00000000-0000-0000-0000-000000000001",
    "baseline_tenant_id": "00000000-0000-0000-0000-000000000002",
    "seed_common_activities": True,
    "seed_industry_baselines": True,
    "skip_if_exists": True
}
```

---

## Common Activity Templates

### Universal Vietnamese Business Activities

```python
# database/migrations/templates/baseline_templates.py

"""
Baseline Activity Templates
Vietnamese-first Common Business Activities
"""

from typing import Dict, List


# Common Vietnamese Business Activity Templates
COMMON_ACTIVITY_TEMPLATES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý thông tin nhân viên",
        "activity_name_en": "Employee Information Management",
        "activity_description_vi": "Lưu trữ và quản lý thông tin cá nhân, hợp đồng lao động và hồ sơ nhân sự của nhân viên",
        "activity_description_en": "Store and manage personal information, employment contracts, and HR records of employees",
        "processing_purpose_vi": "Quản lý nhân sự để thực hiện nghĩa vụ lao động, tính lương và cung cấp phúc lợi",
        "processing_purpose_en": "Manage HR to fulfill employment obligations, calculate payroll, and provide benefits",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "is_common": True,
        "applicable_industries": ["all"]
    },
    {
        "activity_name_vi": "Quản lý tài khoản người dùng",
        "activity_name_en": "User Account Management",
        "activity_description_vi": "Tạo và quản lý tài khoản người dùng để truy cập hệ thống và dịch vụ",
        "activity_description_en": "Create and manage user accounts for system and service access",
        "processing_purpose_vi": "Quản lý tài khoản để cung cấp dịch vụ và hỗ trợ người dùng",
        "processing_purpose_en": "Manage accounts to provide services and support users",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "is_common": True,
        "applicable_industries": ["all"]
    },
    {
        "activity_name_vi": "Xử lý yêu cầu hỗ trợ khách hàng",
        "activity_name_en": "Customer Support Request Processing",
        "activity_description_vi": "Tiếp nhận và xử lý yêu cầu hỗ trợ, khiếu nại của khách hàng",
        "activity_description_en": "Receive and process customer support requests and complaints",
        "processing_purpose_vi": "Xử lý yêu cầu hỗ trợ để giải quyết vấn đề và cải thiện dịch vụ",
        "processing_purpose_en": "Process support requests to resolve issues and improve service",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "is_common": True,
        "applicable_industries": ["all"]
    },
    {
        "activity_name_vi": "Tuân thủ nghĩa vụ thuế và kế toán",
        "activity_name_en": "Tax and Accounting Compliance",
        "activity_description_vi": "Lưu trữ thông tin tài chính và giao dịch để tuân thủ quy định thuế",
        "activity_description_en": "Store financial information and transactions for tax compliance",
        "processing_purpose_vi": "Tuân thủ nghĩa vụ thuế và lập báo cáo tài chính theo quy định pháp luật",
        "processing_purpose_en": "Comply with tax obligations and prepare financial reports per legal requirements",
        "legal_basis": "legal_obligation",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "is_common": True,
        "applicable_industries": ["all"]
    },
    {
        "activity_name_vi": "An ninh và kiểm soát truy cập",
        "activity_name_en": "Security and Access Control",
        "activity_description_vi": "Theo dõi hoạt động đăng nhập và truy cập hệ thống để đảm bảo an ninh",
        "activity_description_en": "Monitor login activities and system access for security purposes",
        "processing_purpose_vi": "Bảo vệ hệ thống và dữ liệu khỏi truy cập trái phép",
        "processing_purpose_en": "Protect system and data from unauthorized access",
        "legal_basis": "legitimate_interest",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "is_common": True,
        "applicable_industries": ["all"]
    },
    {
        "activity_name_vi": "Sao lưu và phục hồi dữ liệu",
        "activity_name_en": "Data Backup and Recovery",
        "activity_description_vi": "Sao lưu định kỳ dữ liệu để phòng ngừa mất mát và khôi phục khi cần",
        "activity_description_en": "Periodically backup data to prevent loss and enable recovery",
        "processing_purpose_vi": "Đảm bảo tính liên tục của hoạt động kinh doanh và bảo vệ dữ liệu",
        "processing_purpose_en": "Ensure business continuity and data protection",
        "legal_basis": "legitimate_interest",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "is_common": True,
        "applicable_industries": ["all"]
    },
    {
        "activity_name_vi": "Báo cáo tuân thủ pháp lý",
        "activity_name_en": "Legal Compliance Reporting",
        "activity_description_vi": "Chuẩn bị và nộp báo cáo tuân thủ cho cơ quan nhà nước",
        "activity_description_en": "Prepare and submit compliance reports to government authorities",
        "processing_purpose_vi": "Tuân thủ yêu cầu báo cáo của cơ quan quản lý nhà nước",
        "processing_purpose_en": "Comply with reporting requirements of government regulatory authorities",
        "legal_basis": "legal_obligation",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "is_common": True,
        "applicable_industries": ["all"]
    },
    {
        "activity_name_vi": "Phòng chống gian lận và rửa tiền",
        "activity_name_en": "Fraud Prevention and Anti-Money Laundering",
        "activity_description_vi": "Giám sát giao dịch để phát hiện và ngăn chặn gian lận, rửa tiền",
        "activity_description_en": "Monitor transactions to detect and prevent fraud and money laundering",
        "processing_purpose_vi": "Tuân thủ quy định chống rửa tiền và bảo vệ tài sản tổ chức",
        "processing_purpose_en": "Comply with anti-money laundering regulations and protect organizational assets",
        "legal_basis": "legal_obligation",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "is_common": True,
        "applicable_industries": ["fintech", "banking", "insurance"]
    }
]
```

---

## Industry-Specific Baselines

### Industry Baseline Configuration

```python
# database/migrations/templates/baseline_templates.py (continued)

"""
Industry-Specific Baseline Templates
Vietnamese-first Industry Templates
"""


# Fintech Industry Baseline Activities
FINTECH_BASELINE_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Xác thực danh tính điện tử (eKYC)",
        "activity_name_en": "Electronic Identity Verification (eKYC)",
        "activity_description_vi": "Xác minh danh tính khách hàng qua sinh trắc học và giấy tờ điện tử",
        "activity_description_en": "Verify customer identity through biometrics and electronic documents",
        "processing_purpose_vi": "Xác thực danh tính để tuân thủ quy định chống rửa tiền (Nghị định 80/2019/NĐ-CP)",
        "processing_purpose_en": "Verify identity to comply with anti-money laundering regulations (Decree 80/2019/ND-CP)",
        "legal_basis": "legal_obligation",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "industry": "fintech"
    },
    {
        "activity_name_vi": "Quản lý ví điện tử và số dư",
        "activity_name_en": "E-Wallet and Balance Management",
        "activity_description_vi": "Quản lý số dư tài khoản và lịch sử giao dịch ví điện tử",
        "activity_description_en": "Manage account balance and e-wallet transaction history",
        "processing_purpose_vi": "Cung cấp dịch vụ thanh toán điện tử và quản lý tài khoản",
        "processing_purpose_en": "Provide electronic payment services and account management",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "fintech"
    },
    {
        "activity_name_vi": "Đánh giá tín dụng và rủi ro",
        "activity_name_en": "Credit and Risk Assessment",
        "activity_description_vi": "Phân tích dữ liệu tài chính để đánh giá khả năng trả nợ",
        "activity_description_en": "Analyze financial data to assess repayment capability",
        "processing_purpose_vi": "Đánh giá rủi ro tín dụng để đưa ra quyết định cho vay hợp lý",
        "processing_purpose_en": "Assess credit risk to make informed lending decisions",
        "legal_basis": "legitimate_interest",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "industry": "fintech"
    }
]


# Healthcare Industry Baseline Activities
HEALTHCARE_BASELINE_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý bệnh án điện tử (EMR)",
        "activity_name_en": "Electronic Medical Records (EMR) Management",
        "activity_description_vi": "Lưu trữ hồ sơ bệnh án, kết quả xét nghiệm và lịch sử điều trị",
        "activity_description_en": "Store medical records, test results, and treatment history",
        "processing_purpose_vi": "Lưu trữ hồ sơ y tế để chẩn đoán, điều trị và theo dõi sức khỏe bệnh nhân",
        "processing_purpose_en": "Store medical records for diagnosis, treatment, and patient health monitoring",
        "legal_basis": "vital_interest",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "industry": "healthcare"
    },
    {
        "activity_name_vi": "Đặt lịch và quản lý khám bệnh",
        "activity_name_en": "Appointment Scheduling and Management",
        "activity_description_vi": "Quản lý lịch hẹn khám bệnh và thông tin bệnh nhân",
        "activity_description_en": "Manage medical appointment schedules and patient information",
        "processing_purpose_vi": "Tối ưu hóa lịch khám và cung cấp dịch vụ y tế chất lượng",
        "processing_purpose_en": "Optimize appointment schedules and provide quality healthcare services",
        "legal_basis": "contract",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "healthcare"
    },
    {
        "activity_name_vi": "Kê đơn thuốc điện tử",
        "activity_name_en": "Electronic Prescription Management",
        "activity_description_vi": "Tạo và quản lý đơn thuốc điện tử cho bệnh nhân",
        "activity_description_en": "Create and manage electronic prescriptions for patients",
        "processing_purpose_vi": "Kê đơn thuốc chính xác và theo dõi điều trị của bệnh nhân",
        "processing_purpose_en": "Prescribe medication accurately and monitor patient treatment",
        "legal_basis": "vital_interest",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "healthcare"
    }
]


# E-commerce Industry Baseline Activities
ECOMMERCE_BASELINE_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý đơn hàng trực tuyến",
        "activity_name_en": "Online Order Management",
        "activity_description_vi": "Xử lý đơn hàng từ giỏ hàng đến giao hàng",
        "activity_description_en": "Process orders from cart to delivery",
        "processing_purpose_vi": "Xử lý đơn hàng để giao sản phẩm và hoàn tất giao dịch",
        "processing_purpose_en": "Process orders to deliver products and complete transactions",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "ecommerce"
    },
    {
        "activity_name_vi": "Phân tích hành vi người dùng",
        "activity_name_en": "User Behavior Analytics",
        "activity_description_vi": "Theo dõi và phân tích hành vi duyệt web và mua sắm",
        "activity_description_en": "Track and analyze browsing and shopping behavior",
        "processing_purpose_vi": "Cải thiện trải nghiệm người dùng và cá nhân hóa gợi ý sản phẩm",
        "processing_purpose_en": "Improve user experience and personalize product recommendations",
        "legal_basis": "consent",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "industry": "ecommerce"
    },
    {
        "activity_name_vi": "Xử lý thanh toán và hoàn tiền",
        "activity_name_en": "Payment and Refund Processing",
        "activity_description_vi": "Xử lý giao dịch thanh toán và yêu cầu hoàn tiền",
        "activity_description_en": "Process payment transactions and refund requests",
        "processing_purpose_vi": "Thực hiện thanh toán và hoàn tiền theo chính sách",
        "processing_purpose_en": "Execute payments and refunds per policy",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": True,
        "requires_dpia": False,
        "industry": "ecommerce"
    }
]


# Manufacturing Industry Baseline Activities
MANUFACTURING_BASELINE_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý chấm công và ca làm việc",
        "activity_name_en": "Attendance and Shift Management",
        "activity_description_vi": "Theo dõi giờ làm việc và ca làm việc của công nhân",
        "activity_description_en": "Track working hours and shifts of workers",
        "processing_purpose_vi": "Tính lương chính xác và quản lý lực lượng lao động",
        "processing_purpose_en": "Calculate accurate payroll and manage workforce",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "manufacturing"
    },
    {
        "activity_name_vi": "Theo dõi an toàn lao động",
        "activity_name_en": "Workplace Safety Monitoring",
        "activity_description_vi": "Ghi nhận tai nạn lao động và theo dõi sức khỏe nghề nghiệp",
        "activity_description_en": "Record workplace accidents and monitor occupational health",
        "processing_purpose_vi": "Đảm bảo an toàn lao động và tuân thủ quy định sức khỏe",
        "processing_purpose_en": "Ensure workplace safety and comply with health regulations",
        "legal_basis": "legal_obligation",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "manufacturing"
    }
]


# Education Industry Baseline Activities
EDUCATION_BASELINE_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý hồ sơ học sinh/sinh viên",
        "activity_name_en": "Student Records Management",
        "activity_description_vi": "Lưu trữ hồ sơ tuyển sinh, kết quả học tập và thông tin cá nhân",
        "activity_description_en": "Store admission records, academic results, and personal information",
        "processing_purpose_vi": "Quản lý hồ sơ học sinh để phục vụ hoạt động đào tạo",
        "processing_purpose_en": "Manage student records for educational activities",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "education"
    },
    {
        "activity_name_vi": "Học trực tuyến và đánh giá",
        "activity_name_en": "Online Learning and Assessment",
        "activity_description_vi": "Theo dõi tiến độ học tập và kết quả thi trên nền tảng trực tuyến",
        "activity_description_en": "Track learning progress and exam results on online platform",
        "processing_purpose_vi": "Cung cấp giáo dục trực tuyến và đánh giá kết quả học tập",
        "processing_purpose_en": "Provide online education and assess learning outcomes",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "education"
    }
]


# Logistics Industry Baseline Activities
LOGISTICS_BASELINE_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý vận đơn và giao hàng",
        "activity_name_en": "Waybill and Delivery Management",
        "activity_description_vi": "Theo dõi thông tin vận đơn và trạng thái giao hàng",
        "activity_description_en": "Track waybill information and delivery status",
        "processing_purpose_vi": "Quản lý vận chuyển và cung cấp thông tin theo dõi",
        "processing_purpose_en": "Manage shipping and provide tracking information",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "logistics"
    },
    {
        "activity_name_vi": "Theo dõi GPS và tối ưu tuyến đường",
        "activity_name_en": "GPS Tracking and Route Optimization",
        "activity_description_vi": "Theo dõi vị trí xe và tối ưu hóa tuyến đường giao hàng",
        "activity_description_en": "Track vehicle location and optimize delivery routes",
        "processing_purpose_vi": "Tối ưu hóa chi phí vận chuyển và thời gian giao hàng",
        "processing_purpose_en": "Optimize shipping costs and delivery time",
        "legal_basis": "legitimate_interest",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "logistics"
    }
]


# Industry Baseline Mapping
INDUSTRY_BASELINE_TEMPLATES: Dict[str, List[Dict[str, any]]] = {
    "fintech": FINTECH_BASELINE_ACTIVITIES,
    "healthcare": HEALTHCARE_BASELINE_ACTIVITIES,
    "ecommerce": ECOMMERCE_BASELINE_ACTIVITIES,
    "manufacturing": MANUFACTURING_BASELINE_ACTIVITIES,
    "education": EDUCATION_BASELINE_ACTIVITIES,
    "logistics": LOGISTICS_BASELINE_ACTIVITIES
}
```

---

## Tenant-Specific Seeding

### Conditional Seeding Logic

```python
# alembic/versions/0004_seed_baseline_activities.py (continued)

"""
Conditional Tenant-Specific Seeding
Vietnamese-first Baseline Data
"""


def detect_tenant_industry(tenant_id: str) -> str:
    """
    Phát hiện ngành công nghiệp của tenant
    Detect tenant industry from configuration
    
    Returns industry type
    """
    # In production, this would query tenant configuration
    # For migration, use environment variable or config file
    industry = os.getenv('TENANT_INDUSTRY', 'general').lower()
    
    valid_industries = [
        'fintech', 'healthcare', 'ecommerce',
        'manufacturing', 'education', 'logistics'
    ]
    
    if industry in valid_industries:
        return industry
    else:
        return 'general'


def upgrade():
    """
    Nâng cấp: Thêm dữ liệu baseline
    Upgrade: Add baseline data
    
    Vietnamese-first baseline seeding
    """
    system_user_id = BASELINE_CONFIG["system_user_id"]
    baseline_tenant_id = BASELINE_CONFIG["baseline_tenant_id"]
    current_time = datetime.now()
    
    print("[START] Bắt đầu seeding baseline activities")
    print("[START] Starting baseline activities seeding")
    
    inserted_count = 0
    
    # Step 1: Seed common activities (applicable to all)
    if BASELINE_CONFIG["seed_common_activities"]:
        print("[PROGRESS] Đang seed hoạt động chung...")
        print("[PROGRESS] Seeding common activities...")
        
        for template in COMMON_ACTIVITY_TEMPLATES:
            # Check if already exists (if skip_if_exists enabled)
            if BASELINE_CONFIG["skip_if_exists"]:
                existing = op.get_bind().execute(
                    sa.text("""
                        SELECT COUNT(*) FROM processing_activities
                        WHERE activity_name_vi = :name_vi
                        AND tenant_id = :tenant_id
                    """),
                    {
                        "name_vi": template["activity_name_vi"],
                        "tenant_id": baseline_tenant_id
                    }
                ).scalar()
                
                if existing > 0:
                    print(f"[SKIP] Bỏ qua: {template['activity_name_vi']} (đã tồn tại)")
                    continue
            
            activity_data = {
                "activity_id": str(uuid4()),
                "tenant_id": baseline_tenant_id,
                "activity_name_vi": template["activity_name_vi"],
                "activity_name_en": template.get("activity_name_en"),
                "activity_description_vi": template.get("activity_description_vi"),
                "activity_description_en": template.get("activity_description_en"),
                "processing_purpose_vi": template["processing_purpose_vi"],
                "processing_purpose_en": template.get("processing_purpose_en"),
                "legal_basis": template["legal_basis"],
                "has_sensitive_data": template.get("has_sensitive_data", False),
                "has_cross_border_transfer": template.get("has_cross_border_transfer", False),
                "requires_dpia": template.get("requires_dpia", False),
                "is_active": True,
                "created_at": current_time,
                "updated_at": current_time,
                "created_by": system_user_id,
                "updated_by": system_user_id
            }
            
            op.execute(
                sa.text("""
                    INSERT INTO processing_activities (
                        activity_id, tenant_id,
                        activity_name_vi, activity_name_en,
                        activity_description_vi, activity_description_en,
                        processing_purpose_vi, processing_purpose_en,
                        legal_basis,
                        has_sensitive_data, has_cross_border_transfer, requires_dpia,
                        is_active, created_at, updated_at, created_by, updated_by
                    ) VALUES (
                        :activity_id, :tenant_id,
                        :activity_name_vi, :activity_name_en,
                        :activity_description_vi, :activity_description_en,
                        :processing_purpose_vi, :processing_purpose_en,
                        :legal_basis,
                        :has_sensitive_data, :has_cross_border_transfer, :requires_dpia,
                        :is_active, :created_at, :updated_at, :created_by, :updated_by
                    )
                """),
                activity_data
            )
            inserted_count += 1
    
    # Step 2: Seed industry-specific baselines
    if BASELINE_CONFIG["seed_industry_baselines"]:
        tenant_industry = detect_tenant_industry(baseline_tenant_id)
        
        if tenant_industry != 'general' and tenant_industry in INDUSTRY_BASELINE_TEMPLATES:
            print(f"[PROGRESS] Đang seed baseline cho ngành {tenant_industry}...")
            print(f"[PROGRESS] Seeding baseline for {tenant_industry} industry...")
            
            industry_templates = INDUSTRY_BASELINE_TEMPLATES[tenant_industry]
            
            for template in industry_templates:
                activity_data = {
                    "activity_id": str(uuid4()),
                    "tenant_id": baseline_tenant_id,
                    "activity_name_vi": template["activity_name_vi"],
                    "activity_name_en": template.get("activity_name_en"),
                    "activity_description_vi": template.get("activity_description_vi"),
                    "activity_description_en": template.get("activity_description_en"),
                    "processing_purpose_vi": template["processing_purpose_vi"],
                    "processing_purpose_en": template.get("processing_purpose_en"),
                    "legal_basis": template["legal_basis"],
                    "has_sensitive_data": template.get("has_sensitive_data", False),
                    "has_cross_border_transfer": template.get("has_cross_border_transfer", False),
                    "requires_dpia": template.get("requires_dpia", False),
                    "is_active": True,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "created_by": system_user_id,
                    "updated_by": system_user_id
                }
                
                op.execute(
                    sa.text("""
                        INSERT INTO processing_activities (
                            activity_id, tenant_id,
                            activity_name_vi, activity_name_en,
                            activity_description_vi, activity_description_en,
                            processing_purpose_vi, processing_purpose_en,
                            legal_basis,
                            has_sensitive_data, has_cross_border_transfer, requires_dpia,
                            is_active, created_at, updated_at, created_by, updated_by
                        ) VALUES (
                            :activity_id, :tenant_id,
                            :activity_name_vi, :activity_name_en,
                            :activity_description_vi, :activity_description_en,
                            :processing_purpose_vi, :processing_purpose_en,
                            :legal_basis,
                            :has_sensitive_data, :has_cross_border_transfer, :requires_dpia,
                            :is_active, :created_at, :updated_at, :created_by, :updated_by
                        )
                    """),
                    activity_data
                )
                inserted_count += 1
    
    print(f"[SUCCESS] Đã seed {inserted_count} baseline activities")
    print(f"[SUCCESS] Seeded {inserted_count} baseline activities")
```

---

## Rollback Procedures

### Migration Downgrade

```python
# alembic/versions/0004_seed_baseline_activities.py (continued)

"""
Rollback Baseline Seeding
Vietnamese-first Data Removal
"""


def downgrade():
    """
    Hạ cấp: Xóa dữ liệu baseline
    Downgrade: Remove baseline data
    
    Clean up baseline activities
    """
    system_user_id = BASELINE_CONFIG["system_user_id"]
    baseline_tenant_id = BASELINE_CONFIG["baseline_tenant_id"]
    
    print("[START] Xóa baseline activities")
    print("[START] Removing baseline activities")
    
    # Delete all baseline activities
    result = op.get_bind().execute(
        sa.text("""
            DELETE FROM processing_activities
            WHERE tenant_id = :tenant_id
            AND created_by = :system_user_id
        """),
        {
            "tenant_id": baseline_tenant_id,
            "system_user_id": system_user_id
        }
    )
    
    deleted_count = result.rowcount
    
    print(f"[SUCCESS] Đã xóa {deleted_count} baseline activities")
    print(f"[SUCCESS] Removed {deleted_count} baseline activities")
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] 8 common Vietnamese business activity templates
- [TARGET] Industry-specific baselines for 6 industries (18 activities)
- [TARGET] Alembic migration script with version control
- [TARGET] Tenant industry detection logic
- [TARGET] Conditional seeding per tenant context
- [TARGET] Skip-if-exists logic to prevent duplicates
- [TARGET] Rollback support in migration downgrade
- [TARGET] Bilingual seeding logs and messages
- [TARGET] All templates in configuration files (zero hard-coding)
- [TARGET] Migration tested with upgrade/downgrade cycle

**Completion Status:** 7 Data Population Methods Documented [OK]

**Table:** processing_activities - COMPLETE  
**Next:** Create folders and documents for remaining 5 tables
