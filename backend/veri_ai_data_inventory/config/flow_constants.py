"""
Flow Mapping Configuration
Document #2 - Section 1: Flow Configuration

Zero hard-coding configuration for data flow mapping
Vietnamese PDPL 2025 compliance focused
"""

from typing import Dict, List, Set


class FlowMappingConfig:
    """
    Configuration for data flow mapping and cross-border transfer detection
    
    Vietnamese PDPL 2025 Article 20 compliance
    Decree 13/2023/ND-CP Article 12 MPS notification thresholds
    """
    
    # ========================================================================
    # Vietnamese Regional Patterns
    # ========================================================================
    
    VIETNAMESE_REGIONS: Dict[str, List[str]] = {
        "north": [
            "Hanoi",
            "Hai Phong", 
            "Quang Ninh",
            "Bac Ninh",
            "Hai Duong",
            "Vinh Phuc",
            "Thai Nguyen",
            "Ha Nam",
            "Nam Dinh",
            "Ninh Binh",
            "Thanh Hoa",
            "Nghe An"
        ],
        "central": [
            "Da Nang",
            "Hue",
            "Quang Nam",
            "Quang Ngai",
            "Binh Dinh",
            "Phu Yen",
            "Khanh Hoa",
            "Quang Tri",
            "Thua Thien Hue"
        ],
        "south": [
            "Ho Chi Minh",
            "Binh Duong",
            "Dong Nai",
            "Ba Ria-Vung Tau",
            "Long An",
            "Tien Giang",
            "Ben Tre",
            "Can Tho",
            "An Giang",
            "Kien Giang",
            "Ca Mau",
            "Bac Lieu"
        ]
    }
    
    # ========================================================================
    # Vietnamese IP Address Ranges (CIDR Notation)
    # ========================================================================
    
    VIETNAMESE_IP_RANGES: List[str] = [
        # Vietnam ISP ranges (examples - in production, use complete lists)
        "14.160.0.0/11",      # VNPT - Vietnam Posts and Telecommunications
        "27.64.0.0/13",       # Viettel - Military Telecom
        "42.112.0.0/13",      # FPT Telecom
        "113.160.0.0/11",     # VNPT additional range
        "115.72.0.0/13",      # Mobifone
        "117.0.0.0/13",       # VDC - Vietnam Data Communication
        "171.224.0.0/12",     # Viettel additional range
        "202.78.224.0/19",    # FPT additional range
        "203.113.128.0/18",   # VNPT additional range
    ]
    
    # ========================================================================
    # MPS (Ministry of Public Security) Notification Thresholds
    # ========================================================================
    
    # Decree 13/2023/ND-CP Article 12
    MPS_THRESHOLD_CATEGORY_1: int = 10000  # Category 1 data subjects
    MPS_THRESHOLD_CATEGORY_2: int = 1000   # Category 2 data subjects
    
    # MPS notification required if exceeding thresholds
    MPS_NOTIFICATION_REQUIRED_MESSAGE: str = (
        "MPS notification required under Decree 13/2023/ND-CP Article 12"
    )
    
    # ========================================================================
    # Country Codes for Cross-Border Transfer Detection
    # ========================================================================
    
    COUNTRY_CODES: Dict[str, str] = {
        # ASEAN countries
        "VN": "Vietnam",
        "SG": "Singapore",
        "TH": "Thailand",
        "MY": "Malaysia",
        "ID": "Indonesia",
        "PH": "Philippines",
        "MM": "Myanmar",
        "KH": "Cambodia",
        "LA": "Laos",
        "BN": "Brunei",
        
        # Major trading partners
        "US": "United States",
        "JP": "Japan",
        "KR": "South Korea",
        "CN": "China",
        "AU": "Australia",
        "NZ": "New Zealand",
        "GB": "United Kingdom",
        "DE": "Germany",
        "FR": "France",
        "CA": "Canada",
        
        # GDPR-adequate countries (for SCC reference)
        "AT": "Austria",
        "BE": "Belgium",
        "DK": "Denmark",
        "FI": "Finland",
        "IE": "Ireland",
        "IT": "Italy",
        "NL": "Netherlands",
        "ES": "Spain",
        "SE": "Sweden",
        "CH": "Switzerland",
        "NO": "Norway",
        "IS": "Iceland",
    }
    
    # Countries considered "adequate" for PDPL transfers (Vietnamese perspective)
    ADEQUATE_COUNTRIES: Set[str] = {
        "SG",  # Singapore - similar data protection framework
        "JP",  # Japan - APPI (Act on Protection of Personal Information)
        "KR",  # South Korea - PIPA (Personal Information Protection Act)
    }
    
    # ========================================================================
    # Processing Purpose Keywords (Vietnamese & English)
    # ========================================================================
    
    PROCESSING_PURPOSE_KEYWORDS: Dict[str, List[str]] = {
        "customer_management": [
            "quản lý khách hàng",
            "customer management",
            "CRM",
            "hồ sơ khách hàng",
            "customer profile",
            "dịch vụ khách hàng",
            "customer service"
        ],
        "marketing": [
            "tiếp thị",
            "marketing",
            "quảng cáo",
            "advertising",
            "khuyến mãi",
            "promotion",
            "email marketing",
            "SMS marketing"
        ],
        "analytics": [
            "phân tích",
            "analytics",
            "báo cáo",
            "reporting",
            "thống kê",
            "statistics",
            "business intelligence",
            "BI"
        ],
        "fraud_prevention": [
            "phòng chống gian lận",
            "fraud prevention",
            "bảo mật",
            "security",
            "xác thực",
            "authentication",
            "chống tiến hành",
            "anti-fraud"
        ],
        "legal_compliance": [
            "tuân thủ pháp lý",
            "legal compliance",
            "tuân thủ",
            "compliance",
            "quy định pháp luật",
            "legal requirements",
            "PDPL",
            "MPS"
        ],
        "hr_management": [
            "quản lý nhân sự",
            "HR management",
            "nhân viên",
            "employee",
            "lương",
            "payroll",
            "tuyển dụng",
            "recruitment"
        ],
        "service_delivery": [
            "cung cấp dịch vụ",
            "service delivery",
            "dịch vụ",
            "service",
            "giao hàng",
            "delivery",
            "thực hiện hợp đồng",
            "contract fulfillment"
        ],
        "research": [
            "nghiên cứu",
            "research",
            "phát triển",
            "development",
            "R&D",
            "sản phẩm mới",
            "new product"
        ],
        "third_party_sharing": [
            "chia sẻ bên thứ ba",
            "third party sharing",
            "đối tác",
            "partner",
            "nhà cung cấp",
            "vendor",
            "bên ngoài",
            "external party"
        ]
    }
    
    # ========================================================================
    # Secure Transfer Protocols
    # ========================================================================
    
    SECURE_PROTOCOLS: Set[str] = {
        "HTTPS",
        "SFTP",
        "FTPS",
        "SSH",
        "TLS",
        "SSL",
        "VPN",
        "IPSec"
    }
    
    INSECURE_PROTOCOLS: Set[str] = {
        "HTTP",
        "FTP",
        "Telnet",
        "SMTP",  # Without TLS
        "POP3",  # Without SSL
        "IMAP"   # Without SSL
    }
    
    # ========================================================================
    # Data Transfer Volume Thresholds
    # ========================================================================
    
    # Volume thresholds for risk classification
    VOLUME_THRESHOLD_LOW: int = 1000        # < 1K records
    VOLUME_THRESHOLD_MEDIUM: int = 10000    # 1K - 10K records
    VOLUME_THRESHOLD_HIGH: int = 100000     # 10K - 100K records
    # > 100K records = CRITICAL
    
    # ========================================================================
    # Vietnamese Business Hours (for flow scheduling)
    # ========================================================================
    
    VIETNAMESE_BUSINESS_HOURS: Dict[str, Dict[str, str]] = {
        "north": {
            "start": "08:00",
            "end": "17:00",
            "lunch_start": "12:00",
            "lunch_end": "13:30",
            "timezone": "Asia/Ho_Chi_Minh"
        },
        "central": {
            "start": "07:30",
            "end": "17:00",
            "lunch_start": "11:30",
            "lunch_end": "13:00",
            "timezone": "Asia/Ho_Chi_Minh"
        },
        "south": {
            "start": "08:00",
            "end": "17:30",
            "lunch_start": "12:00",
            "lunch_end": "13:00",
            "timezone": "Asia/Ho_Chi_Minh"
        }
    }
    
    # ========================================================================
    # Graph Visualization Settings
    # ========================================================================
    
    # Node colors for different asset types (Vietnamese color scheme)
    NODE_COLORS: Dict[str, str] = {
        "database": "#6b8e6b",           # Vietnamese green
        "api_endpoint": "#7fa3c3",       # Vietnamese blue
        "file_system": "#d4c18a",        # Vietnamese gold
        "cloud_storage": "#b8d4e3",      # Light blue
        "third_party_service": "#f4a460", # Orange (warning)
        "mps_system": "#dc143c",         # Red (government)
        "data_subject": "#9370db",       # Purple (user)
        "processing_activity": "#98d98e" # Light green (process)
    }
    
    # Edge colors for different flow types
    EDGE_COLORS: Dict[str, str] = {
        "data_transfer": "#808080",          # Gray (internal)
        "api_call": "#4682b4",               # Steel blue
        "file_copy": "#daa520",              # Golden rod
        "cross_border_transfer": "#ff4500",  # Orange red (alert)
        "third_party_sharing": "#ff8c00",    # Dark orange (warning)
        "mps_notification": "#dc143c",       # Crimson (government)
        "user_access": "#9370db"             # Medium purple (user)
    }
    
    # ========================================================================
    # Retention Period Defaults (Vietnamese PDPL Guidelines)
    # ========================================================================
    
    RETENTION_PERIODS: Dict[str, int] = {
        # Days to retain data based on purpose
        "customer_management": 1825,      # 5 years
        "marketing": 730,                 # 2 years
        "analytics": 365,                 # 1 year
        "fraud_prevention": 2555,         # 7 years
        "legal_compliance": 3650,         # 10 years
        "hr_management": 3650,            # 10 years (labor law)
        "service_delivery": 1095,         # 3 years
        "research": 1825,                 # 5 years
        "third_party_sharing": 730        # 2 years
    }
    
    # ========================================================================
    # Legal Basis Mapping (Vietnamese PDPL Article 8)
    # ========================================================================
    
    LEGAL_BASIS_DESCRIPTIONS: Dict[str, str] = {
        "consent": "Sự đồng ý của chủ thể dữ liệu (Consent of data subject)",
        "contract": "Thực hiện hợp đồng (Contract performance)",
        "legal_obligation": "Nghĩa vụ pháp lý (Legal obligation)",
        "vital_interests": "Lợi ích thiết yếu (Vital interests)",
        "public_task": "Nhiệm vụ công cộng (Public task)",
        "legitimate_interest": "Lợi ích chính đáng (Legitimate interest)"
    }
    
    # ========================================================================
    # Cross-Border Transfer Mechanisms (PDPL Article 20)
    # ========================================================================
    
    TRANSFER_MECHANISMS: Dict[str, str] = {
        "adequacy_decision": "Quyết định đầy đủ về bảo vệ dữ liệu (Adequacy decision)",
        "standard_contractual_clauses": "Điều khoản hợp đồng chuẩn (Standard Contractual Clauses - SCC)",
        "binding_corporate_rules": "Quy tắc doanh nghiệp ràng buộc (Binding Corporate Rules - BCR)",
        "explicit_consent": "Sự đồng ý rõ ràng (Explicit consent)",
        "mps_approval": "Chấp thuận của Bộ Công an (MPS approval)"
    }
    
    # ========================================================================
    # Data Category Patterns (Vietnamese PDPL Categories)
    # ========================================================================
    
    CATEGORY_1_KEYWORDS: List[str] = [
        "họ tên",
        "full name",
        "địa chỉ",
        "address",
        "email",
        "số điện thoại",
        "phone number",
        "ngày sinh",
        "date of birth",
        "DOB",
        "giới tính",
        "gender"
    ]
    
    CATEGORY_2_KEYWORDS: List[str] = [
        "CMND",
        "CCCD",
        "identity card",
        "hộ chiếu",
        "passport",
        "y tế",
        "health",
        "tài chính",
        "financial",
        "ngân hàng",
        "bank",
        "thẻ tín dụng",
        "credit card",
        "sinh trắc học",
        "biometric",
        "vân tay",
        "fingerprint",
        "khuôn mặt",
        "facial",
        "định danh",
        "identification"
    ]
    
    # ========================================================================
    # Flow Detection Patterns
    # ========================================================================
    
    # Common API endpoints that indicate data flows
    API_FLOW_PATTERNS: List[str] = [
        r"/api/users",
        r"/api/customers",
        r"/api/orders",
        r"/api/payments",
        r"/api/export",
        r"/api/sync",
        r"/api/transfer",
        r"/webhook",
        r"/callback"
    ]
    
    # Database query patterns indicating data movement
    DATABASE_FLOW_PATTERNS: List[str] = [
        "INSERT INTO",
        "UPDATE",
        "DELETE FROM",
        "SELECT.*INTO",
        "COPY",
        "EXPORT",
        "BACKUP",
        "RESTORE"
    ]
    
    # ========================================================================
    # Vietnamese Cultural Business Context
    # ========================================================================
    
    # Regional business communication styles (for contextual flow analysis)
    REGIONAL_COMMUNICATION_STYLES: Dict[str, str] = {
        "north": "hierarchical",      # Formal, government proximity
        "central": "collaborative",   # Consensus-building, traditional
        "south": "entrepreneurial"    # Fast-paced, international exposure
    }
    
    # ========================================================================
    # Compliance Validation Rules
    # ========================================================================
    
    COMPLIANCE_RULES: Dict[str, Dict[str, any]] = {
        "cross_border_transfer": {
            "requires_mechanism": True,
            "requires_impact_assessment": True,
            "mps_notification_category_1": 10000,
            "mps_notification_category_2": 1000
        },
        "third_party_sharing": {
            "requires_dpa": True,  # Data Processing Agreement
            "requires_audit": True,
            "audit_frequency_days": 365
        },
        "data_retention": {
            "enforce_deletion": True,
            "grace_period_days": 30,
            "requires_audit_trail": True
        }
    }


# ============================================================================
# Module-level convenience functions
# ============================================================================

def get_vietnamese_region(location: str) -> str:
    """
    Determine Vietnamese region from location string
    
    Args:
        location: City or province name (Vietnamese or English)
    
    Returns:
        Region name: 'north', 'central', 'south', or 'unknown'
    """
    config = FlowMappingConfig()
    location_lower = location.lower().strip()
    
    for region, cities in config.VIETNAMESE_REGIONS.items():
        for city in cities:
            if city.lower() in location_lower or location_lower in city.lower():
                return region
    
    return "unknown"


def is_cross_border_transfer(source_country: str, destination_country: str) -> bool:
    """
    Check if data flow is a cross-border transfer
    
    Args:
        source_country: ISO country code of source
        destination_country: ISO country code of destination
    
    Returns:
        True if cross-border transfer (requires PDPL Article 20 compliance)
    """
    # Normalize country codes
    source = source_country.upper().strip()
    destination = destination_country.upper().strip()
    
    # Transfer from Vietnam to another country = cross-border
    if source == "VN" and destination != "VN":
        return True
    
    # Transfer to Vietnam from another country = cross-border
    if source != "VN" and destination == "VN":
        return True
    
    return False


def requires_mps_notification(data_subject_count: int, is_category_2: bool = False) -> bool:
    """
    Check if MPS notification required under Decree 13/2023/ND-CP Article 12
    
    Args:
        data_subject_count: Number of data subjects affected
        is_category_2: True if processing Category 2 (sensitive) data
    
    Returns:
        True if MPS notification required
    """
    config = FlowMappingConfig()
    
    if is_category_2:
        return data_subject_count >= config.MPS_THRESHOLD_CATEGORY_2
    else:
        return data_subject_count >= config.MPS_THRESHOLD_CATEGORY_1


def get_retention_period(processing_purpose: str) -> int:
    """
    Get recommended retention period for processing purpose
    
    Args:
        processing_purpose: Processing purpose key
    
    Returns:
        Retention period in days
    """
    config = FlowMappingConfig()
    return config.RETENTION_PERIODS.get(processing_purpose, 365)  # Default 1 year


def is_secure_protocol(protocol: str) -> bool:
    """
    Check if data transfer protocol is secure
    
    Args:
        protocol: Transfer protocol name (e.g., 'HTTPS', 'FTP')
    
    Returns:
        True if protocol is considered secure
    """
    config = FlowMappingConfig()
    protocol_upper = protocol.upper().strip()
    return protocol_upper in config.SECURE_PROTOCOLS
