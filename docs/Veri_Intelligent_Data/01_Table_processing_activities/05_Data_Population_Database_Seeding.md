# Data Population Method 5: Database Seeding (Development/Demo)
## Vietnamese PDPL 2025 Compliance - Processing Activities Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** processing_activities Table  
**Method:** SQL Database Seeding for Development/Demo Environments  
**Architecture:** Vietnamese-first Sample Data with Regional Context  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **database seeding** with Vietnamese sample processing activities for development, demo, and testing environments. This method populates the database with realistic Vietnamese business scenarios across different industries and regional contexts.

**Key Features:**
- Vietnamese-first sample activities with proper diacritics
- Regional business context (North/Central/South Vietnam)
- Industry-specific templates (fintech, healthcare, e-commerce, manufacturing)
- Alembic migration integration for version control
- Environment-specific seeding (dev/staging/demo)
- Zero hard-coding with all sample data in configuration files

**Use Cases:**
- Local development environment setup
- Demo presentations for Vietnamese prospects
- Integration testing with realistic data
- Training environments for compliance officers
- QA testing with Vietnamese business scenarios

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Sample Data Configuration](#sample-data-configuration)
3. [Regional Business Templates](#regional-business-templates)
4. [Industry-Specific Seeds](#industry-specific-seeds)
5. [Alembic Migration Integration](#alembic-migration-integration)
6. [Environment-Specific Seeding](#environment-specific-seeding)
7. [Implementation Guide](#implementation-guide)

---

## Architecture Overview

### Seeding System Components

```
┌─────────────────────────────────────────────────────────────┐
│            Database Seeding Architecture                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Seed Data   │  │  Regional    │  │  Industry    │     │
│  │  Config      │─>│  Templates   │─>│  Templates   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Alembic     │  │  Environment │  │  Seeder      │     │
│  │  Migration   │  │  Detector    │  │  Service     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  processing_activities │                    │
│              │  (sample data)         │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Seeding Workflow:**
1. Detect environment (dev/staging/demo/prod)
2. Skip seeding in production
3. Load seed configuration from constants
4. Generate sample activities by industry and region
5. Insert via Alembic migration or seeder service
6. Verify inserted data count
7. Log seeding summary

---

## Sample Data Configuration

### Seed Data Constants

```python
# database/seeds/constants/seed_constants.py

"""
Database Seed Constants - Zero Hard-Coding
Vietnamese-first Sample Data Configuration
"""

from enum import Enum
from typing import Dict, List
from uuid import uuid4


# Environment Types
class SeedEnvironment(str, Enum):
    """
    Môi trường seed dữ liệu
    Seed environment types
    """
    DEVELOPMENT = "development"      # Phát triển
    STAGING = "staging"              # Dàn dựng
    DEMO = "demo"                    # Demo
    TESTING = "testing"              # Kiểm thử
    PRODUCTION = "production"        # Sản xuất (NO SEEDING)


# Environment Vietnamese Translations
SEED_ENVIRONMENT_TRANSLATIONS_VI: Dict[str, str] = {
    SeedEnvironment.DEVELOPMENT: "Môi trường phát triển",
    SeedEnvironment.STAGING: "Môi trường dàn dựng",
    SeedEnvironment.DEMO: "Môi trường demo",
    SeedEnvironment.TESTING: "Môi trường kiểm thử",
    SeedEnvironment.PRODUCTION: "Môi trường sản xuất"
}


# Environment English Translations
SEED_ENVIRONMENT_TRANSLATIONS_EN: Dict[str, str] = {
    SeedEnvironment.DEVELOPMENT: "Development Environment",
    SeedEnvironment.STAGING: "Staging Environment",
    SeedEnvironment.DEMO: "Demo Environment",
    SeedEnvironment.TESTING: "Testing Environment",
    SeedEnvironment.PRODUCTION: "Production Environment"
}


# Industries for Sample Data
class SeedIndustry(str, Enum):
    """
    Ngành công nghiệp mẫu
    Sample industries
    """
    FINTECH = "fintech"                      # Công nghệ tài chính
    HEALTHCARE = "healthcare"                # Y tế
    ECOMMERCE = "ecommerce"                  # Thương mại điện tử
    MANUFACTURING = "manufacturing"          # Sản xuất
    EDUCATION = "education"                  # Giáo dục
    LOGISTICS = "logistics"                  # Vận tải logistics


# Industry Vietnamese Translations
SEED_INDUSTRY_TRANSLATIONS_VI: Dict[str, str] = {
    SeedIndustry.FINTECH: "Công nghệ tài chính",
    SeedIndustry.HEALTHCARE: "Y tế",
    SeedIndustry.ECOMMERCE: "Thương mại điện tử",
    SeedIndustry.MANUFACTURING: "Sản xuất",
    SeedIndustry.EDUCATION: "Giáo dục",
    SeedIndustry.LOGISTICS: "Vận tải logistics"
}


# Regional Locations
class SeedRegion(str, Enum):
    """
    Vùng miền Việt Nam
    Vietnamese regions
    """
    NORTH = "north"          # Miền Bắc
    CENTRAL = "central"      # Miền Trung
    SOUTH = "south"          # Miền Nam


# Regional Vietnamese Translations
SEED_REGION_TRANSLATIONS_VI: Dict[str, str] = {
    SeedRegion.NORTH: "Miền Bắc",
    SeedRegion.CENTRAL: "Miền Trung",
    SeedRegion.SOUTH: "Miền Nam"
}


# Seeding Configuration
SEED_CONFIG: Dict[str, any] = {
    # Number of sample activities per industry
    "activities_per_industry": 3,
    
    # Total expected samples (6 industries × 3 activities = 18)
    "total_expected_samples": 18,
    
    # Skip seeding in production
    "skip_production": True,
    
    # Seed data created_by user (system user)
    "system_user_id": "00000000-0000-0000-0000-000000000001"
}
```

---

## Regional Business Templates

### Vietnamese Regional Context

```python
# database/seeds/templates/regional_templates.py

"""
Regional Business Templates
Vietnamese-first Regional Context
"""

from typing import Dict, List


# North Vietnam (Hanoi-centric) Business Templates
NORTH_VIETNAM_TEMPLATES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý hồ sơ cán bộ công chức",
        "activity_name_en": "Civil Servant Records Management",
        "processing_purpose_vi": "Lưu trữ và quản lý thông tin cán bộ, công chức để phục vụ công tác quản lý nhà nước",
        "processing_purpose_en": "Store and manage civil servant information for government administration",
        "legal_basis": "legal_obligation",
        "regional_context": "north",
        "business_context": "Government-focused, formal hierarchy, structured processes"
    },
    {
        "activity_name_vi": "Xử lý đơn hàng xuất khẩu",
        "activity_name_en": "Export Order Processing",
        "processing_purpose_vi": "Quản lý thông tin khách hàng và đơn hàng xuất khẩu để thực hiện giao dịch thương mại quốc tế",
        "processing_purpose_en": "Manage customer information and export orders for international trade",
        "legal_basis": "contract",
        "regional_context": "north",
        "business_context": "Manufacturing export, international trade focus"
    },
    {
        "activity_name_vi": "Quản lý sinh viên và học viên",
        "activity_name_en": "Student and Learner Management",
        "processing_purpose_vi": "Lưu trữ thông tin sinh viên để phục vụ hoạt động đào tạo và cấp bằng",
        "processing_purpose_en": "Store student information for education and degree issuance",
        "legal_basis": "contract",
        "regional_context": "north",
        "business_context": "Education institutions, university management"
    }
]


# Central Vietnam (Da Nang/Hue-centric) Business Templates
CENTRAL_VIETNAM_TEMPLATES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý du khách và tour du lịch",
        "activity_name_en": "Tourist and Tour Management",
        "processing_purpose_vi": "Lưu trữ thông tin du khách để tổ chức tour du lịch và cung cấp dịch vụ lưu trú",
        "processing_purpose_en": "Store tourist information for tour organization and hospitality services",
        "legal_basis": "contract",
        "regional_context": "central",
        "business_context": "Tourism industry, cultural preservation focus"
    },
    {
        "activity_name_vi": "Quản lý bệnh nhân và hồ sơ y tế",
        "activity_name_en": "Patient and Medical Records Management",
        "processing_purpose_vi": "Lưu trữ thông tin sức khỏe bệnh nhân để chẩn đoán, điều trị và theo dõi bệnh",
        "processing_purpose_en": "Store patient health information for diagnosis, treatment, and monitoring",
        "legal_basis": "vital_interest",
        "regional_context": "central",
        "business_context": "Healthcare, traditional medicine integration"
    },
    {
        "activity_name_vi": "Xử lý đơn hàng nghệ thuật truyền thống",
        "activity_name_en": "Traditional Craft Order Processing",
        "processing_purpose_vi": "Quản lý đơn hàng sản phẩm thủ công mỹ nghệ để giao hàng và thanh toán",
        "processing_purpose_en": "Manage traditional craft orders for delivery and payment",
        "legal_basis": "contract",
        "regional_context": "central",
        "business_context": "Artisan crafts, cultural products"
    }
]


# South Vietnam (HCMC-centric) Business Templates
SOUTH_VIETNAM_TEMPLATES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý tài khoản ví điện tử",
        "activity_name_en": "E-Wallet Account Management",
        "processing_purpose_vi": "Lưu trữ thông tin người dùng để cung cấp dịch vụ thanh toán điện tử và chuyển tiền",
        "processing_purpose_en": "Store user information to provide electronic payment and money transfer services",
        "legal_basis": "contract",
        "regional_context": "south",
        "business_context": "Fintech, digital payments, fast-paced innovation"
    },
    {
        "activity_name_vi": "Phân tích hành vi mua sắm trực tuyến",
        "activity_name_en": "Online Shopping Behavior Analysis",
        "processing_purpose_vi": "Phân tích dữ liệu khách hàng để cá nhân hóa trải nghiệm mua sắm và gợi ý sản phẩm",
        "processing_purpose_en": "Analyze customer data to personalize shopping experience and product recommendations",
        "legal_basis": "consent",
        "regional_context": "south",
        "business_context": "E-commerce, data-driven marketing"
    },
    {
        "activity_name_vi": "Quản lý giao hàng nhanh và tài xế",
        "activity_name_en": "Express Delivery and Driver Management",
        "processing_purpose_vi": "Theo dõi vị trí tài xế và thông tin đơn hàng để tối ưu hóa giao hàng",
        "processing_purpose_en": "Track driver location and order information to optimize delivery",
        "legal_basis": "contract",
        "regional_context": "south",
        "business_context": "Logistics, on-demand delivery services"
    }
]


# Regional Templates Mapping
REGIONAL_TEMPLATES_MAPPING: Dict[str, List[Dict[str, any]]] = {
    "north": NORTH_VIETNAM_TEMPLATES,
    "central": CENTRAL_VIETNAM_TEMPLATES,
    "south": SOUTH_VIETNAM_TEMPLATES
}
```

---

## Industry-Specific Seeds

### Industry Sample Activities

```python
# database/seeds/templates/industry_templates.py

"""
Industry-Specific Templates
Vietnamese-first Sample Activities by Industry
"""

from typing import Dict, List


# Fintech Industry Templates
FINTECH_SEED_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Xác thực danh tính khách hàng (KYC)",
        "activity_name_en": "Customer Identity Verification (KYC)",
        "activity_description_vi": "Thu thập và xác minh thông tin cá nhân, giấy tờ tùy thân để tuân thủ quy định chống rửa tiền",
        "activity_description_en": "Collect and verify personal information and identity documents for anti-money laundering compliance",
        "processing_purpose_vi": "Xác thực danh tính khách hàng để tuân thủ Nghị định 80/2019/NĐ-CP về chống rửa tiền",
        "processing_purpose_en": "Verify customer identity to comply with Decree 80/2019/ND-CP on anti-money laundering",
        "legal_basis": "legal_obligation",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "fintech"
    },
    {
        "activity_name_vi": "Quản lý giao dịch thanh toán điện tử",
        "activity_name_en": "Electronic Payment Transaction Management",
        "activity_description_vi": "Lưu trữ lịch sử giao dịch và thông tin thanh toán để cung cấp dịch vụ ví điện tử",
        "activity_description_en": "Store transaction history and payment information to provide e-wallet services",
        "processing_purpose_vi": "Quản lý giao dịch thanh toán để thực hiện dịch vụ chuyển tiền và thanh toán",
        "processing_purpose_en": "Manage payment transactions to provide money transfer and payment services",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": True,
        "requires_dpia": True,
        "industry": "fintech"
    },
    {
        "activity_name_vi": "Phân tích rủi ro tín dụng",
        "activity_name_en": "Credit Risk Analysis",
        "activity_description_vi": "Đánh giá khả năng trả nợ của khách hàng dựa trên lịch sử tài chính và dữ liệu cá nhân",
        "activity_description_en": "Assess customer repayment capability based on financial history and personal data",
        "processing_purpose_vi": "Phân tích rủi ro tín dụng để đưa ra quyết định cho vay hợp lý",
        "processing_purpose_en": "Analyze credit risk to make informed lending decisions",
        "legal_basis": "legitimate_interest",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "industry": "fintech"
    }
]


# Healthcare Industry Templates
HEALTHCARE_SEED_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý hồ sơ bệnh án điện tử",
        "activity_name_en": "Electronic Medical Records Management",
        "activity_description_vi": "Lưu trữ thông tin sức khỏe, tiền sử bệnh, kết quả xét nghiệm và hình ảnh y tế",
        "activity_description_en": "Store health information, medical history, test results, and medical images",
        "processing_purpose_vi": "Lưu trữ hồ sơ bệnh án để phục vụ chẩn đoán, điều trị và theo dõi sức khỏe bệnh nhân",
        "processing_purpose_en": "Store medical records for diagnosis, treatment, and patient health monitoring",
        "legal_basis": "vital_interest",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "industry": "healthcare"
    },
    {
        "activity_name_vi": "Đặt lịch khám bệnh trực tuyến",
        "activity_name_en": "Online Medical Appointment Scheduling",
        "activity_description_vi": "Thu thập thông tin liên hệ và triệu chứng để sắp xếp lịch khám bệnh",
        "activity_description_en": "Collect contact information and symptoms to arrange medical appointments",
        "processing_purpose_vi": "Quản lý lịch khám bệnh để tối ưu hóa thời gian và chất lượng dịch vụ y tế",
        "processing_purpose_en": "Manage appointment schedules to optimize time and healthcare service quality",
        "legal_basis": "contract",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "healthcare"
    },
    {
        "activity_name_vi": "Nghiên cứu y học và phân tích dữ liệu sức khỏe",
        "activity_name_en": "Medical Research and Health Data Analysis",
        "activity_description_vi": "Phân tích dữ liệu sức khỏe ẩn danh để nghiên cứu dịch tễ và cải thiện phương pháp điều trị",
        "activity_description_en": "Analyze anonymized health data for epidemiological research and treatment improvement",
        "processing_purpose_vi": "Nghiên cứu y học để phát triển phương pháp điều trị mới và dự phòng bệnh tật",
        "processing_purpose_en": "Medical research to develop new treatment methods and disease prevention",
        "legal_basis": "public_interest",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": True,
        "industry": "healthcare"
    }
]


# E-commerce Industry Templates
ECOMMERCE_SEED_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý tài khoản khách hàng",
        "activity_name_en": "Customer Account Management",
        "activity_description_vi": "Lưu trữ thông tin đăng ký, lịch sử mua hàng và sở thích của khách hàng",
        "activity_description_en": "Store registration information, purchase history, and customer preferences",
        "processing_purpose_vi": "Quản lý tài khoản để cung cấp dịch vụ mua sắm trực tuyến và hỗ trợ khách hàng",
        "processing_purpose_en": "Manage accounts to provide online shopping services and customer support",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "ecommerce"
    },
    {
        "activity_name_vi": "Marketing và quảng cáo cá nhân hóa",
        "activity_name_en": "Personalized Marketing and Advertising",
        "activity_description_vi": "Phân tích hành vi duyệt web và mua sắm để gửi ưu đãi và quảng cáo phù hợp",
        "activity_description_en": "Analyze browsing and shopping behavior to send relevant offers and advertisements",
        "processing_purpose_vi": "Cá nhân hóa trải nghiệm mua sắm và gửi ưu đãi phù hợp với sở thích khách hàng",
        "processing_purpose_en": "Personalize shopping experience and send offers matching customer preferences",
        "legal_basis": "consent",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "ecommerce"
    },
    {
        "activity_name_vi": "Xử lý và giao hàng",
        "activity_name_en": "Order Processing and Delivery",
        "activity_description_vi": "Thu thập địa chỉ giao hàng và thông tin liên hệ để vận chuyển sản phẩm",
        "activity_description_en": "Collect delivery address and contact information for product shipping",
        "processing_purpose_vi": "Xử lý đơn hàng và giao hàng đến địa chỉ khách hàng",
        "processing_purpose_en": "Process orders and deliver products to customer addresses",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "ecommerce"
    }
]


# Manufacturing Industry Templates
MANUFACTURING_SEED_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý nhân sự và chấm công",
        "activity_name_en": "HR and Attendance Management",
        "activity_description_vi": "Lưu trữ thông tin nhân viên, hợp đồng lao động và dữ liệu chấm công",
        "activity_description_en": "Store employee information, labor contracts, and attendance data",
        "processing_purpose_vi": "Quản lý nhân sự để tính lương, phúc lợi và tuân thủ luật lao động",
        "processing_purpose_en": "Manage HR for payroll, benefits, and labor law compliance",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "manufacturing"
    },
    {
        "activity_name_vi": "An toàn lao động và sức khỏe nghề nghiệp",
        "activity_name_en": "Workplace Safety and Occupational Health",
        "activity_description_vi": "Theo dõi tình trạng sức khỏe và tai nạn lao động của công nhân",
        "activity_description_en": "Monitor health status and workplace accidents of workers",
        "processing_purpose_vi": "Đảm bảo an toàn lao động và tuân thủ quy định về sức khỏe nghề nghiệp",
        "processing_purpose_en": "Ensure workplace safety and comply with occupational health regulations",
        "legal_basis": "legal_obligation",
        "has_sensitive_data": True,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "manufacturing"
    },
    {
        "activity_name_vi": "Quản lý chuỗi cung ứng và đối tác",
        "activity_name_en": "Supply Chain and Partner Management",
        "activity_description_vi": "Lưu trữ thông tin nhà cung cấp và đối tác kinh doanh",
        "activity_description_en": "Store supplier and business partner information",
        "processing_purpose_vi": "Quản lý quan hệ đối tác để tối ưu hóa chuỗi cung ứng",
        "processing_purpose_en": "Manage partnerships to optimize supply chain",
        "legal_basis": "legitimate_interest",
        "has_sensitive_data": False,
        "has_cross_border_transfer": True,
        "requires_dpia": False,
        "industry": "manufacturing"
    }
]


# Education Industry Templates
EDUCATION_SEED_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Tuyển sinh và quản lý hồ sơ sinh viên",
        "activity_name_en": "Admission and Student Records Management",
        "activity_description_vi": "Thu thập hồ sơ tuyển sinh và thông tin cá nhân của sinh viên",
        "activity_description_en": "Collect admission documents and student personal information",
        "processing_purpose_vi": "Quản lý hồ sơ sinh viên để phục vụ hoạt động đào tạo và cấp bằng",
        "processing_purpose_en": "Manage student records for education activities and degree issuance",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "education"
    },
    {
        "activity_name_vi": "Học trực tuyến và theo dõi tiến độ",
        "activity_name_en": "Online Learning and Progress Tracking",
        "activity_description_vi": "Theo dõi hoạt động học tập và kết quả thi của sinh viên trên nền tảng trực tuyến",
        "activity_description_en": "Track learning activities and exam results of students on online platform",
        "processing_purpose_vi": "Theo dõi tiến độ học tập để hỗ trợ và cải thiện chất lượng giảng dạy",
        "processing_purpose_en": "Track learning progress to support and improve teaching quality",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "education"
    },
    {
        "activity_name_vi": "Tư vấn học tập và nghề nghiệp",
        "activity_name_en": "Academic and Career Counseling",
        "activity_description_vi": "Phân tích năng lực và sở thích để tư vấn hướng nghiệp cho sinh viên",
        "activity_description_en": "Analyze capabilities and interests to provide career counseling for students",
        "processing_purpose_vi": "Tư vấn nghề nghiệp để hỗ trợ sinh viên phát triển sự nghiệp",
        "processing_purpose_en": "Career counseling to support student career development",
        "legal_basis": "consent",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "education"
    }
]


# Logistics Industry Templates
LOGISTICS_SEED_ACTIVITIES: List[Dict[str, any]] = [
    {
        "activity_name_vi": "Quản lý vận đơn và theo dõi hàng hóa",
        "activity_name_en": "Waybill Management and Cargo Tracking",
        "activity_description_vi": "Lưu trữ thông tin người gửi, người nhận và theo dõi vị trí hàng hóa",
        "activity_description_en": "Store sender and recipient information and track cargo location",
        "processing_purpose_vi": "Quản lý vận chuyển và cung cấp thông tin tra cứu cho khách hàng",
        "processing_purpose_en": "Manage shipping and provide tracking information for customers",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "logistics"
    },
    {
        "activity_name_vi": "Quản lý tài xế và phương tiện",
        "activity_name_en": "Driver and Vehicle Management",
        "activity_description_vi": "Theo dõi vị trí GPS và thông tin tài xế để điều phối vận chuyển",
        "activity_description_en": "Track GPS location and driver information for shipping coordination",
        "processing_purpose_vi": "Tối ưu hóa tuyến đường và điều phối tài xế hiệu quả",
        "processing_purpose_en": "Optimize routes and efficiently coordinate drivers",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "logistics"
    },
    {
        "activity_name_vi": "Quản lý kho và kiểm kê",
        "activity_name_en": "Warehouse and Inventory Management",
        "activity_description_vi": "Lưu trữ thông tin hàng hóa và chủ sở hữu để quản lý kho",
        "activity_description_en": "Store cargo information and owner details for warehouse management",
        "processing_purpose_vi": "Quản lý kho bãi và theo dõi hàng tồn kho",
        "processing_purpose_en": "Manage warehouses and track inventory",
        "legal_basis": "contract",
        "has_sensitive_data": False,
        "has_cross_border_transfer": False,
        "requires_dpia": False,
        "industry": "logistics"
    }
]


# Industry Templates Mapping
INDUSTRY_TEMPLATES_MAPPING: Dict[str, List[Dict[str, any]]] = {
    "fintech": FINTECH_SEED_ACTIVITIES,
    "healthcare": HEALTHCARE_SEED_ACTIVITIES,
    "ecommerce": ECOMMERCE_SEED_ACTIVITIES,
    "manufacturing": MANUFACTURING_SEED_ACTIVITIES,
    "education": EDUCATION_SEED_ACTIVITIES,
    "logistics": LOGISTICS_SEED_ACTIVITIES
}
```

---

## Alembic Migration Integration

### Migration Script for Seeding

```python
# alembic/versions/0003_seed_sample_activities.py

"""
Seed sample processing activities for dev/demo environments

Revision ID: 0003_seed_activities
Revises: 0002_create_tables
Create Date: 2025-11-06 17:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from datetime import datetime
import os

from database.seeds.templates.industry_templates import INDUSTRY_TEMPLATES_MAPPING
from database.seeds.constants.seed_constants import (
    SEED_CONFIG,
    SeedEnvironment
)


# Revision identifiers
revision = '0003_seed_activities'
down_revision = '0002_create_tables'
branch_labels = None
depends_on = None


def detect_environment() -> str:
    """
    Phát hiện môi trường
    Detect environment from ENV variables
    
    Returns environment name
    """
    env = os.getenv('APP_ENV', 'development').lower()
    
    if env in ['prod', 'production']:
        return SeedEnvironment.PRODUCTION
    elif env in ['staging', 'stage']:
        return SeedEnvironment.STAGING
    elif env in ['demo']:
        return SeedEnvironment.DEMO
    elif env in ['test', 'testing']:
        return SeedEnvironment.TESTING
    else:
        return SeedEnvironment.DEVELOPMENT


def upgrade():
    """
    Nâng cấp: Thêm dữ liệu mẫu
    Upgrade: Add sample data
    
    Vietnamese-first seeding
    """
    current_env = detect_environment()
    
    # Skip seeding in production
    if current_env == SeedEnvironment.PRODUCTION and SEED_CONFIG["skip_production"]:
        print(f"[SKIP] Bỏ qua seeding trong môi trường {current_env}")
        print(f"[SKIP] Skipping seeding in {current_env} environment")
        return
    
    print(f"[START] Bắt đầu seeding trong môi trường {current_env}")
    print(f"[START] Starting seeding in {current_env} environment")
    
    # System user ID for created_by
    system_user_id = SEED_CONFIG["system_user_id"]
    current_time = datetime.now()
    
    # Seed data for each industry
    inserted_count = 0
    
    for industry, templates in INDUSTRY_TEMPLATES_MAPPING.items():
        print(f"[PROGRESS] Đang seed ngành {industry}...")
        print(f"[PROGRESS] Seeding industry {industry}...")
        
        for template in templates:
            activity_data = {
                "activity_id": str(uuid4()),
                "tenant_id": system_user_id,  # Use system tenant for demo
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
    
    print(f"[SUCCESS] Đã seed {inserted_count} hoạt động xử lý mẫu")
    print(f"[SUCCESS] Seeded {inserted_count} sample processing activities")


def downgrade():
    """
    Hạ cấp: Xóa dữ liệu mẫu
    Downgrade: Remove sample data
    
    Clean up seeded data
    """
    current_env = detect_environment()
    
    if current_env == SeedEnvironment.PRODUCTION and SEED_CONFIG["skip_production"]:
        print(f"[SKIP] Bỏ qua xóa seeding trong môi trường {current_env}")
        print(f"[SKIP] Skipping seeding removal in {current_env} environment")
        return
    
    system_user_id = SEED_CONFIG["system_user_id"]
    
    print(f"[START] Xóa dữ liệu mẫu trong môi trường {current_env}")
    print(f"[START] Removing sample data in {current_env} environment")
    
    # Delete all activities created by system user
    op.execute(
        sa.text("""
            DELETE FROM processing_activities
            WHERE created_by = :system_user_id
        """),
        {"system_user_id": system_user_id}
    )
    
    print(f"[SUCCESS] Đã xóa tất cả dữ liệu mẫu")
    print(f"[SUCCESS] Removed all sample data")
```

---

## Environment-Specific Seeding

### Seeder Service for Programmatic Seeding

```python
# services/seeding/seeder_service.py

"""
Seeder Service
Vietnamese-first Programmatic Database Seeding
"""

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime
from typing import Dict, List
import os

from database.seeds.templates.industry_templates import INDUSTRY_TEMPLATES_MAPPING
from database.seeds.constants.seed_constants import (
    SEED_CONFIG,
    SeedEnvironment,
    SEED_ENVIRONMENT_TRANSLATIONS_VI
)


class SeederService:
    """
    Dịch vụ seed dữ liệu
    Database seeding service
    
    Programmatic seeding for dev/demo
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.current_env = self._detect_environment()
    
    def _detect_environment(self) -> str:
        """Phát hiện môi trường hiện tại"""
        env = os.getenv('APP_ENV', 'development').lower()
        
        if env in ['prod', 'production']:
            return SeedEnvironment.PRODUCTION
        elif env in ['staging', 'stage']:
            return SeedEnvironment.STAGING
        elif env in ['demo']:
            return SeedEnvironment.DEMO
        elif env in ['test', 'testing']:
            return SeedEnvironment.TESTING
        else:
            return SeedEnvironment.DEVELOPMENT
    
    async def seed_all_industries(
        self,
        tenant_id: str
    ) -> Dict[str, any]:
        """
        Seed tất cả ngành công nghiệp
        Seed all industries
        
        Returns seeding summary
        """
        if self.current_env == SeedEnvironment.PRODUCTION and SEED_CONFIG["skip_production"]:
            return {
                "seeded": False,
                "reason_vi": f"Bỏ qua seeding trong môi trường {SEED_ENVIRONMENT_TRANSLATIONS_VI[self.current_env]}",
                "reason_en": f"Skipping seeding in {self.current_env} environment"
            }
        
        inserted_count = 0
        system_user_id = SEED_CONFIG["system_user_id"]
        
        for industry, templates in INDUSTRY_TEMPLATES_MAPPING.items():
            for template in templates:
                await self._insert_activity(tenant_id, template, system_user_id)
                inserted_count += 1
        
        await self.db.commit()
        
        return {
            "seeded": True,
            "environment": self.current_env,
            "inserted_count": inserted_count,
            "expected_count": SEED_CONFIG["total_expected_samples"],
            "message_vi": f"Đã seed {inserted_count} hoạt động xử lý mẫu",
            "message_en": f"Seeded {inserted_count} sample processing activities"
        }
    
    async def _insert_activity(
        self,
        tenant_id: str,
        template: Dict[str, any],
        created_by: str
    ):
        """Chèn một hoạt động vào database"""
        from sqlalchemy import text
        
        activity_data = {
            "activity_id": str(uuid4()),
            "tenant_id": tenant_id,
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
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "created_by": created_by,
            "updated_by": created_by
        }
        
        await self.db.execute(
            text("""
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
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] Sample data configuration with zero hard-coding
- [TARGET] Vietnamese-first sample activities with proper diacritics
- [TARGET] Regional templates (North/Central/South Vietnam)
- [TARGET] 6 industry-specific templates (18 total activities)
- [TARGET] Alembic migration script for seeding
- [TARGET] Environment detection (skip production)
- [TARGET] Seeder service for programmatic seeding
- [TARGET] Rollback capability in migration downgrade
- [TARGET] Bilingual seeding logs and messages
- [TARGET] All sample data in named constants (no hard-coding)

**Next Document:** #06 - Third-Party System Integration
