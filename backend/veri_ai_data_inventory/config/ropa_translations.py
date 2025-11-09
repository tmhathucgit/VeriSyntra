"""
ROPA Translations Configuration - ZERO HARD-CODING PATTERN
All translation strings, labels, and language-specific values centralized here

This module provides the single source of truth for all ROPA (Record of Processing
Activities) bilingual content used in MPS reporting, PDF generation, and API responses.

Legal References:
- Decree 13/2023/ND-CP Article 12: ROPA mandatory fields
- Circular 09/2024/TT-BCA: MPS reporting technical specifications
- PDPL Article 17: Data controller obligations

ZERO HARD-CODING:
- All translations in dictionaries (NO if/else chains)
- ROPALanguage enum for type safety (NO 'vi'/'en' strings)
- Helper methods for common formatting patterns
- Single source of truth (183+ translation pairs)

Translation Coverage:
- MPS CSV headers (17 columns × 2 languages = 34)
- MPS JSON keys (13 fields × 2 languages = 26)
- PDF titles and headers (14 translations)
- PDF field labels (40+ translations)
- Common values (booleans, N/A, dates)
- Total: 124+ translation pairs
"""

from typing import Dict, Any, List, Optional
from models.ropa_models import ROPAEntry, ROPALanguage


class ROPATranslations:
    """
    Centralized translation configuration for ROPA generation
    
    This class eliminates all hard-coded language checks and translation strings
    from ROPA exporters and generators. Instead of scattering `if language == 'vi'`
    throughout the codebase, all translations are defined here and accessed via
    dictionary routing.
    
    Pattern:
        # WRONG (hard-coded):
        if language == 'vi':
            header = "Tên tổ chức"
        else:
            header = "Organization Name"
        
        # RIGHT (config-driven):
        headers = ROPATranslations.MPS_CSV_HEADERS[language]
    """
    
    # =============================================================================
    # COMMON TRANSLATION STRINGS
    # =============================================================================
    
    BOOLEAN_VALUES: Dict[ROPALanguage, Dict[bool, str]] = {
        ROPALanguage.VIETNAMESE: {
            True: "Có",
            False: "Không"
        },
        ROPALanguage.ENGLISH: {
            True: "Yes",
            False: "No"
        }
    }
    
    NOT_SPECIFIED: Dict[ROPALanguage, str] = {
        ROPALanguage.VIETNAMESE: "Chưa xác định",
        ROPALanguage.ENGLISH: "Not specified"
    }
    
    NONE_VALUE: Dict[ROPALanguage, str] = {
        ROPALanguage.VIETNAMESE: "Không",
        ROPALanguage.ENGLISH: "None"
    }
    
    N_A_VALUE: Dict[ROPALanguage, str] = {
        ROPALanguage.VIETNAMESE: "N/A",
        ROPALanguage.ENGLISH: "N/A"
    }
    
    # =============================================================================
    # MPS REPORTING - CSV FORMAT
    # =============================================================================
    
    MPS_CSV_HEADERS: Dict[ROPALanguage, List[str]] = {
        ROPALanguage.VIETNAMESE: [
            "STT",  # Serial number
            "Tên tổ chức",  # Organization name
            "Mã số thuế",  # Tax ID
            "Hoạt động xử lý",  # Processing activity
            "Mục đích xử lý",  # Purpose
            "Cơ sở pháp lý",  # Legal basis
            "Loại dữ liệu",  # Data categories
            "Dữ liệu nhạy cảm",  # Sensitive data
            "Số lượng chủ thể",  # Number of subjects
            "Bên nhận dữ liệu",  # Recipients
            "Chuyển ra nước ngoài",  # Cross-border (Yes/No)
            "Quốc gia đích",  # Destination country
            "Biện pháp bảo vệ",  # Safeguards
            "Thời gian lưu trữ",  # Retention period
            "Biện pháp bảo mật",  # Security measures
            "Vị trí xử lý",  # Processing location
            "Ngày cập nhật"  # Last updated
        ],
        ROPALanguage.ENGLISH: [
            "No",
            "Organization Name",
            "Tax ID",
            "Processing Activity",
            "Purpose",
            "Legal Basis",
            "Data Categories",
            "Sensitive Data",
            "Number of Subjects",
            "Recipients",
            "Cross-Border",
            "Destination Country",
            "Safeguards",
            "Retention Period",
            "Security Measures",
            "Processing Location",
            "Last Updated"
        ]
    }
    
    # =============================================================================
    # MPS REPORTING - JSON FORMAT
    # =============================================================================
    
    MPS_JSON_KEYS: Dict[ROPALanguage, Dict[str, str]] = {
        ROPALanguage.VIETNAMESE: {
            "controller_name": "ten_to_chuc",
            "tax_id": "ma_so_thue",
            "activity": "hoat_dong_xu_ly",
            "purpose": "muc_dich",
            "legal_basis": "co_so_phap_ly",
            "data_categories": "loai_du_lieu",
            "data_subjects": "chu_the_du_lieu",
            "recipients": "ben_nhan",
            "cross_border": "chuyen_nuoc_ngoai",
            "destination_countries": "quoc_gia_dich",
            "retention": "luu_tru",
            "security": "bao_mat",
            "updated_date": "ngay_cap_nhat"
        },
        ROPALanguage.ENGLISH: {
            "controller_name": "organization_name",
            "tax_id": "tax_id",
            "activity": "processing_activity",
            "purpose": "purpose",
            "legal_basis": "legal_basis",
            "data_categories": "data_categories",
            "data_subjects": "data_subjects",
            "recipients": "recipients",
            "cross_border": "cross_border",
            "destination_countries": "destination_countries",
            "retention": "retention_period",
            "security": "security_measures",
            "updated_date": "last_updated"
        }
    }
    
    # =============================================================================
    # PDF DOCUMENT - TITLES
    # =============================================================================
    
    PDF_TITLES: Dict[ROPALanguage, Dict[str, str]] = {
        ROPALanguage.VIETNAMESE: {
            "title": "SỔ ĐĂNG KÝ HOẠT ĐỘNG XỬ LÝ DỮ LIỆU CÁ NHÂN",
            "subtitle": "Record of Processing Activities (ROPA)"
        },
        ROPALanguage.ENGLISH: {
            "title": "RECORD OF PROCESSING ACTIVITIES",
            "subtitle": "Per Vietnamese PDPL Decree 13/2023/ND-CP"
        }
    }
    
    # =============================================================================
    # PDF DOCUMENT - SECTION HEADERS
    # =============================================================================
    
    PDF_SECTION_HEADERS: Dict[ROPALanguage, Dict[str, str]] = {
        ROPALanguage.VIETNAMESE: {
            "controller": "Thông tin Bên Kiểm Soát Dữ Liệu",
            "dpo": "Người Bảo Vệ Dữ Liệu (DPO)",
            "summary": "Thống Kê Tổng Quan",
            "activities": "Hoạt Động Xử Lý Dữ Liệu"
        },
        ROPALanguage.ENGLISH: {
            "controller": "Data Controller Information",
            "dpo": "Data Protection Officer (DPO)",
            "summary": "Summary Statistics",
            "activities": "Processing Activities"
        }
    }
    
    # =============================================================================
    # PDF DOCUMENT - FIELD LABELS
    # =============================================================================
    
    PDF_FIELD_LABELS: Dict[ROPALanguage, Dict[str, str]] = {
        ROPALanguage.VIETNAMESE: {
            "org_name": "Tên tổ chức:",
            "tax_id": "Mã số thuế:",
            "address": "Địa chỉ:",
            "contact_person": "Người liên hệ:",
            "phone": "Điện thoại:",
            "email": "Email:",
            "dpo_name": "Họ tên:",
            "dpo_email": "Email:",
            "dpo_phone": "Điện thoại:",
            "total_activities": "Tổng số hoạt động xử lý:",
            "total_subjects": "Tổng số chủ thể dữ liệu:",
            "has_sensitive": "Có dữ liệu nhạy cảm:",
            "has_cross_border": "Có chuyển dữ liệu ra nước ngoài:",
            "generated_date": "Ngày tạo:",
            "serial_no": "STT",
            "activity": "Hoạt động",
            "purpose": "Mục đích",
            "legal_basis": "Cơ sở pháp lý",
            "data_categories": "Loại dữ liệu",
            "subjects": "Số chủ thể"
        },
        ROPALanguage.ENGLISH: {
            "org_name": "Organization name:",
            "tax_id": "Tax ID:",
            "address": "Address:",
            "contact_person": "Contact person:",
            "phone": "Phone:",
            "email": "Email:",
            "dpo_name": "Name:",
            "dpo_email": "Email:",
            "dpo_phone": "Phone:",
            "total_activities": "Total processing activities:",
            "total_subjects": "Total data subjects:",
            "has_sensitive": "Has sensitive data:",
            "has_cross_border": "Has cross-border transfers:",
            "generated_date": "Generated date:",
            "serial_no": "No",
            "activity": "Activity",
            "purpose": "Purpose",
            "legal_basis": "Legal Basis",
            "data_categories": "Data Categories",
            "subjects": "Subjects"
        }
    }
    
    # =============================================================================
    # DATE FORMATTING
    # =============================================================================
    
    DATE_FORMATS: Dict[ROPALanguage, str] = {
        ROPALanguage.VIETNAMESE: "%d/%m/%Y",  # Vietnamese format: 05/11/2025
        ROPALanguage.ENGLISH: "%Y-%m-%d"     # ISO format: 2025-11-05
    }
    
    # =============================================================================
    # HELPER METHODS - FIELD ACCESS
    # =============================================================================
    
    @staticmethod
    def get_field_value(
        entry: ROPAEntry,
        field_name: str,
        language: ROPALanguage
    ) -> Any:
        """
        Get field value with language awareness - ZERO HARD-CODING
        
        Automatically selects field_name or field_name_vi based on language.
        Eliminates need for if/else chains in exporters.
        
        Args:
            entry: ROPAEntry instance
            field_name: Base field name (without _vi suffix)
            language: ROPALanguage enum
            
        Returns:
            Field value in requested language
            
        Example:
            >>> get_field_value(entry, 'controller_name', ROPALanguage.VIETNAMESE)
            'Công ty TNHH ABC'  # Returns entry.controller_name_vi
            
            >>> get_field_value(entry, 'controller_name', ROPALanguage.ENGLISH)
            'ABC Company Ltd'  # Returns entry.controller_name
        """
        if language == ROPALanguage.VIETNAMESE:
            # Try _vi suffix first for Vietnamese
            vi_field = f"{field_name}_vi"
            if hasattr(entry, vi_field):
                value = getattr(entry, vi_field)
                if value is not None:
                    return value
        
        # Fallback to base field name
        if hasattr(entry, field_name):
            return getattr(entry, field_name)
        
        return None
    
    # =============================================================================
    # HELPER METHODS - FORMATTING
    # =============================================================================
    
    @staticmethod
    def format_list(
        items: Optional[List[str]],
        separator: str = "; ",
        empty_value: str = "",
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> str:
        """
        Format list with language-aware empty value
        
        Args:
            items: List of strings to join
            separator: Join separator (default: "; ")
            empty_value: Value for empty list (default: language-specific "None")
            language: ROPALanguage enum
            
        Returns:
            Formatted string
            
        Example:
            >>> format_list(["Họ và tên", "Email"], language=ROPALanguage.VIETNAMESE)
            "Họ và tên; Email"
            
            >>> format_list([], language=ROPALanguage.VIETNAMESE)
            "Không"
        """
        if not items:
            return empty_value if empty_value else ROPATranslations.NONE_VALUE[language]
        return separator.join(items)
    
    @staticmethod
    def format_boolean(value: bool, language: ROPALanguage) -> str:
        """
        Format boolean with language-aware Yes/No - ZERO HARD-CODING
        
        Args:
            value: Boolean value
            language: ROPALanguage enum
            
        Returns:
            "Có"/"Không" for Vietnamese, "Yes"/"No" for English
            
        Example:
            >>> format_boolean(True, ROPALanguage.VIETNAMESE)
            "Có"
            
            >>> format_boolean(False, ROPALanguage.ENGLISH)
            "No"
        """
        return ROPATranslations.BOOLEAN_VALUES[language][value]
    
    @staticmethod
    def format_optional_int(
        value: Optional[int],
        language: ROPALanguage
    ) -> str:
        """
        Format optional integer with language-aware 'Not specified'
        
        Args:
            value: Integer value or None
            language: ROPALanguage enum
            
        Returns:
            String representation or "Chưa xác định"/"Not specified"
            
        Example:
            >>> format_optional_int(1000, ROPALanguage.VIETNAMESE)
            "1000"
            
            >>> format_optional_int(None, ROPALanguage.VIETNAMESE)
            "Chưa xác định"
        """
        if value is None:
            return ROPATranslations.NOT_SPECIFIED[language]
        return str(value)


# Module exports
__all__ = [
    'ROPATranslations',
]
