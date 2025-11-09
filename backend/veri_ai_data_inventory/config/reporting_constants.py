"""
Reporting & Visualization Configuration Constants
ZERO HARD-CODING pattern for Phase 2 (Document #9)
Vietnamese PDPL 2025 compliance reporting configuration
"""

from enum import Enum
from typing import Dict, List, Any, Literal
from dataclasses import dataclass


class ReportType(Enum):
    """Vietnamese PDPL compliance report types"""
    MPS_CIRCULAR_09_2024 = "mps_circular_09_2024"  # Bo Cong an (Ministry of Public Security)
    EXECUTIVE_SUMMARY = "executive_summary"  # Bao cao tom tat
    AUDIT_TRAIL = "audit_trail"  # Nhat ky kiem toan
    DATA_INVENTORY = "data_inventory"  # Danh muc du lieu
    THIRD_PARTY_TRANSFERS = "third_party_transfers"  # Chuyen giao ben thu ba
    DSR_ACTIVITY = "dsr_activity"  # Hoat dong yeu cau quyen du lieu


class NodeType(Enum):
    """Data lineage graph node types"""
    SOURCE = "source"  # Nguon du lieu
    PROCESSING = "processing"  # Xu ly
    STORAGE = "storage"  # Luu tru
    DESTINATION = "destination"  # Dich


class TransferType(Enum):
    """Data transfer classification types"""
    INTERNAL = "internal"  # Noi bo
    CROSS_BORDER = "cross-border"  # Xuyen bien gioi
    THIRD_PARTY = "third-party"  # Ben thu ba


class OutputFormat(Enum):
    """Export output formats"""
    PDF = "pdf"
    XLSX = "xlsx"
    JSON = "json"


class RiskLevel(Enum):
    """Vendor risk assessment levels"""
    HIGH = "high"  # Cao
    MEDIUM = "medium"  # Trung binh
    LOW = "low"  # Thap


@dataclass
class RiskThresholds:
    """Risk scoring thresholds (0-10 scale)"""
    HIGH_THRESHOLD: float = 7.5  # Scores >= 7.5 are HIGH risk
    MEDIUM_THRESHOLD: float = 5.0  # Scores >= 5.0 and < 7.5 are MEDIUM risk
    # Scores < 5.0 are LOW risk


class ReportingConfig:
    """
    Centralized configuration for Phase 2 visualization & reporting
    Follows ZERO HARD-CODING pattern established in Phase 1
    """
    
    # Report Types (Vietnamese PDPL compliance)
    REPORT_TYPES: List[str] = [rt.value for rt in ReportType]
    
    # Node Types for Data Lineage Graphs
    NODE_TYPES: List[str] = [nt.value for nt in NodeType]
    
    # Transfer Types
    TRANSFER_TYPES: List[str] = [tt.value for tt in TransferType]
    
    # Output Formats
    OUTPUT_FORMATS: List[str] = [of.value for of in OutputFormat]
    
    # Risk Thresholds
    RISK_THRESHOLDS = RiskThresholds()
    
    # Default System Names (can be overridden by database)
    DEFAULT_SOURCE_SYSTEMS: List[str] = [
        "web_forms",
        "mobile_app",
        "crm_system",
        "api_integrations"
    ]
    
    DEFAULT_STORAGE_LOCATIONS: List[str] = [
        "postgresql_vietnam",
        "mongodb_vietnam",
        "redis_cache",
        "s3_vietnam"
    ]
    
    # Vietnamese Redaction Patterns (compiled regex)
    REDACTION_PATTERNS: Dict[str, str] = {
        # Vietnamese phone numbers
        "vietnamese_phone": r"\b(0|\+84)[1-9]\d{8,9}\b",
        
        # Vietnamese Citizen ID (CCCD - 12 digits)
        "cccd": r"\b\d{12}\b",
        
        # Vietnamese email addresses
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        
        # Vietnamese addresses (keywords-based)
        "address": r"(?i)(số|đường|phường|quận|thành phố|tỉnh)\s+[\w\s,.-]+",
        
        # Vietnamese full names (Họ tên - pattern detection)
        "full_name": r"\b[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+){1,3}\b",
        
        # Bank account numbers (Vietnamese format)
        "bank_account": r"\b\d{10,16}\b"
    }
    
    # Redaction Replacement Masks
    REDACTION_MASKS: Dict[str, str] = {
        "vietnamese_phone": "[SĐT]",  # So dien thoai
        "cccd": "[CCCD]",  # Can cuoc cong dan
        "email": "[EMAIL]",
        "address": "[ĐỊA CHỈ]",  # Dia chi
        "full_name": "[HỌ TÊN]",  # Ho ten
        "bank_account": "[TÀI KHOẢN]"  # Tai khoan
    }
    
    # System Name Translations (Vietnamese)
    SYSTEM_TRANSLATIONS_VI: Dict[str, str] = {
        "web_forms": "Biểu mẫu Web",
        "mobile_app": "Ứng dụng Di động",
        "crm_system": "Hệ thống CRM",
        "api_integrations": "Tích hợp API",
        "postgresql_vietnam": "Cơ sở dữ liệu PostgreSQL (Việt Nam)",
        "mongodb_vietnam": "Cơ sở dữ liệu MongoDB (Việt Nam)",
        "redis_cache": "Bộ nhớ đệm Redis",
        "s3_vietnam": "Lưu trữ S3 (Việt Nam)"
    }
    
    # Report Type Translations (Vietnamese)
    REPORT_TYPE_TRANSLATIONS_VI: Dict[str, str] = {
        "mps_circular_09_2024": "Báo cáo Bộ Công an (Thông tư 09/2024)",
        "executive_summary": "Báo cáo Tóm tắt Điều hành",
        "audit_trail": "Nhật ký Kiểm toán",
        "data_inventory": "Danh mục Dữ liệu",
        "third_party_transfers": "Chuyển giao Bên thứ ba",
        "dsr_activity": "Hoạt động Yêu cầu Quyền Dữ liệu"
    }
    
    # Node Type Translations (Vietnamese)
    NODE_TYPE_TRANSLATIONS_VI: Dict[str, str] = {
        "source": "Nguồn",
        "processing": "Xử lý",
        "storage": "Lưu trữ",
        "destination": "Đích"
    }
    
    # Transfer Type Translations (Vietnamese)
    TRANSFER_TYPE_TRANSLATIONS_VI: Dict[str, str] = {
        "internal": "Nội bộ",
        "cross-border": "Xuyên biên giới",
        "third-party": "Bên thứ ba"
    }
    
    # Risk Level Translations (Vietnamese)
    RISK_LEVEL_TRANSLATIONS_VI: Dict[str, str] = {
        "high": "Cao",
        "medium": "Trung bình",
        "low": "Thấp"
    }
    
    # MPS Report Format Configuration
    MPS_REPORT_CONFIG: Dict[str, Any] = {
        "title": "Báo cáo Bảo vệ Dữ liệu Cá nhân - PDPL 2025",
        "title_en": "Personal Data Protection Report - PDPL 2025",
        "circular_reference": "Thông tư 09/2024/TT-BCA",
        "authority": "Bộ Công an Việt Nam",
        "authority_en": "Ministry of Public Security - Vietnam",
        "required_sections": [
            "business_information",  # Thong tin doanh nghiep
            "data_inventory",  # Danh muc du lieu
            "processing_activities",  # Hoat dong xu ly
            "cross_border_transfers",  # Chuyen giao xuyen bien gioi
            "security_measures",  # Bien phap bao mat
            "dpo_information"  # Thong tin DPO
        ]
    }
    
    # Executive Summary Configuration
    EXECUTIVE_SUMMARY_CONFIG: Dict[str, Any] = {
        "title": "Báo cáo Tuân thủ PDPL - Tóm tắt Điều hành",
        "title_en": "PDPL Compliance - Executive Summary",
        "target_audience": "board_of_directors",  # Hoi dong quan tri
        "key_metrics": [
            "total_data_fields",  # Tong so truong du lieu
            "category_1_count",  # So truong loai 1
            "category_2_count",  # So truong loai 2
            "cross_border_transfers",  # Chuyen giao xuyen bien gioi
            "third_party_vendors",  # Nha cung cap ben thu ba
            "compliance_score"  # Diem tuan thu
        ]
    }
    
    # Audit Trail Configuration
    AUDIT_TRAIL_CONFIG: Dict[str, Any] = {
        "title": "Nhật ký Kiểm toán - PDPL 2025",
        "title_en": "Audit Trail - PDPL 2025",
        "event_types": [
            "data_access",  # Truy cap du lieu
            "data_modification",  # Chinh sua du lieu
            "data_deletion",  # Xoa du lieu
            "export_report",  # Xuat bao cao
            "dsr_request",  # Yeu cau quyen du lieu
            "consent_update"  # Cap nhat dong y
        ],
        "retention_days": 730  # 2 years per PDPL Article 13
    }
    
    # Third-Party Dashboard Configuration
    THIRD_PARTY_DASHBOARD_CONFIG: Dict[str, Any] = {
        "title": "Bảng điều khiển Bên thứ ba",
        "title_en": "Third-Party Dashboard",
        "risk_factors": [
            "data_volume",  # Luong du lieu
            "cross_border_status",  # Trang thai xuyen bien gioi
            "encryption_enabled",  # Ma hoa kich hoat
            "scc_signed",  # Hop dong SCC ky ket
            "compliance_certification",  # Chung nhan tuan thu
            "data_breach_history"  # Lich su vi pham du lieu
        ],
        "risk_weights": {
            "data_volume": 0.20,
            "cross_border_status": 0.25,
            "encryption_enabled": 0.15,
            "scc_signed": 0.20,
            "compliance_certification": 0.15,
            "data_breach_history": 0.05
        }
    }
    
    @staticmethod
    def get_report_types() -> List[str]:
        """Get all available report types"""
        return ReportingConfig.REPORT_TYPES
    
    @staticmethod
    def get_node_types() -> List[str]:
        """Get all node types for data lineage graphs"""
        return ReportingConfig.NODE_TYPES
    
    @staticmethod
    def validate_report_type(report_type: str) -> bool:
        """Validate if report type is supported"""
        return report_type in ReportingConfig.REPORT_TYPES
    
    @staticmethod
    def validate_node_type(node_type: str) -> bool:
        """Validate if node type is supported"""
        return node_type in ReportingConfig.NODE_TYPES
    
    @staticmethod
    def get_risk_level(score: float) -> RiskLevel:
        """
        Determine risk level from score (0-10 scale)
        
        Args:
            score: Risk score (0-10)
        
        Returns:
            RiskLevel enum
        """
        if score >= ReportingConfig.RISK_THRESHOLDS.HIGH_THRESHOLD:
            return RiskLevel.HIGH
        elif score >= ReportingConfig.RISK_THRESHOLDS.MEDIUM_THRESHOLD:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    @staticmethod
    def translate_to_vietnamese(key: str, category: str) -> str:
        """
        Get Vietnamese translation for a key
        
        Args:
            key: English key to translate
            category: Translation category (report_type, node_type, etc.)
        
        Returns:
            Vietnamese translation or original key if not found
        """
        translation_maps = {
            "report_type": ReportingConfig.REPORT_TYPE_TRANSLATIONS_VI,
            "node_type": ReportingConfig.NODE_TYPE_TRANSLATIONS_VI,
            "transfer_type": ReportingConfig.TRANSFER_TYPE_TRANSLATIONS_VI,
            "risk_level": ReportingConfig.RISK_LEVEL_TRANSLATIONS_VI,
            "system": ReportingConfig.SYSTEM_TRANSLATIONS_VI
        }
        
        translation_map = translation_maps.get(category, {})
        return translation_map.get(key, key)
