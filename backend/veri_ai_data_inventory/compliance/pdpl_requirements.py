"""
Vietnamese PDPL Requirements
ROPA Mandatory Fields per Decree 13/2023/ND-CP Article 12

This module defines the mandatory fields and data categories required for
Vietnamese PDPL-compliant Record of Processing Activities (ROPA) generation.

Legal References:
- Decree 13/2023/ND-CP Article 12: ROPA mandatory fields
- Decree 13/2023/ND-CP Article 3: Personal data categories
- PDPL Article 17: Data controller obligations
- Circular 09/2024/TT-BCA: MPS reporting specifications

ZERO HARD-CODING:
- All field names defined as enums
- All categories configured in dictionaries
- Bilingual support (Vietnamese primary, English secondary)
"""

from typing import Dict, List
from enum import Enum


class PDPLROPAField(str, Enum):
    """
    Mandatory ROPA fields per Decree 13/2023/ND-CP Article 12
    
    These fields are required for Vietnamese PDPL compliance and MPS reporting.
    Each field has Vietnamese and English identifiers for bilingual support.
    """
    
    # Article 12.1.a - Controller information
    CONTROLLER_NAME = "ten_to_chuc_xu_ly"  # Organization name
    CONTROLLER_NAME_EN = "controller_name"
    CONTROLLER_ADDRESS = "dia_chi_to_chuc"
    CONTROLLER_TAX_ID = "ma_so_thue"
    CONTROLLER_CONTACT = "nguoi_lien_he"
    
    # Article 12.1.b - DPO information
    DPO_NAME = "ten_nguoi_bao_ve_du_lieu"
    DPO_EMAIL = "email_nguoi_bao_ve_du_lieu"
    DPO_PHONE = "dien_thoai_nguoi_bao_ve_du_lieu"
    
    # Article 12.1.c - Processing activities
    PROCESSING_PURPOSE = "muc_dich_xu_ly"
    PROCESSING_PURPOSE_EN = "processing_purpose"
    LEGAL_BASIS = "co_so_phap_ly"
    LEGAL_BASIS_EN = "legal_basis"
    
    # Article 12.1.d - Data categories
    DATA_CATEGORIES = "loai_du_lieu_ca_nhan"
    DATA_CATEGORIES_EN = "personal_data_categories"
    SENSITIVE_DATA = "du_lieu_ca_nhan_nhay_cam"
    
    # Article 12.1.e - Data subjects
    DATA_SUBJECTS = "chu_the_du_lieu"
    DATA_SUBJECTS_EN = "data_subjects"
    SUBJECT_COUNT = "so_luong_chu_the"
    
    # Article 12.1.f - Recipients
    RECIPIENTS = "ben_nhan_du_lieu"
    RECIPIENTS_EN = "data_recipients"
    RECIPIENT_TYPE = "loai_ben_nhan"
    
    # Article 12.1.g - Cross-border transfers
    CROSS_BORDER = "chuyen_du_lieu_ra_nuoc_ngoai"
    DESTINATION_COUNTRY = "quoc_gia_nhan_du_lieu"
    TRANSFER_SAFEGUARDS = "bien_phap_bao_ve"
    
    # Article 12.1.h - Retention period
    RETENTION_PERIOD = "thoi_gian_luu_tru"
    RETENTION_PERIOD_EN = "retention_period"
    
    # Article 12.1.i - Security measures
    SECURITY_MEASURES = "bien_phap_bao_mat"
    SECURITY_MEASURES_EN = "security_measures"
    
    # Article 12.1.j - Processing location
    PROCESSING_LOCATION = "dia_diem_xu_ly"
    DATA_CENTER_REGION = "khu_vuc_trung_tam_du_lieu"


class VietnamesePDPLCategories:
    """
    Vietnamese PDPL data categories per Decree 13/2023/ND-CP Article 3
    
    This class provides bilingual configuration for:
    - Regular personal data categories
    - Sensitive personal data categories
    - Legal bases for processing
    
    All strings use proper Vietnamese diacritics for compliance.
    """
    
    REGULAR_DATA = {
        "vi": "Dữ liệu cá nhân thông thường",
        "en": "Regular personal data",
        "article": "Decree 13/2023/ND-CP Article 3.1",
        "examples_vi": [
            "Họ và tên",
            "Địa chỉ email",
            "Số điện thoại",
            "Địa chỉ liên lạc",
            "Ngày sinh"
        ],
        "examples_en": [
            "Full name",
            "Email address",
            "Phone number",
            "Contact address",
            "Date of birth"
        ]
    }
    
    SENSITIVE_DATA = {
        "vi": "Dữ liệu cá nhân nhạy cảm",
        "en": "Sensitive personal data",
        "article": "Decree 13/2023/ND-CP Article 3.2",
        "categories_vi": [
            "Quan điểm chính trị",
            "Tín ngưỡng, tôn giáo",
            "Tình trạng sức khỏe, bệnh tật",
            "Đời sống tình dục",
            "Dữ liệu sinh trắc học",
            "Dữ liệu di truyền",
            "Dữ liệu vị trí",
            "Hồ sơ tư pháp, hành chính",
            "Thông tin tài chính cá nhân",
            "Thông tin về trẻ em dưới 16 tuổi"
        ],
        "categories_en": [
            "Political opinions",
            "Religious or philosophical beliefs",
            "Health status, medical conditions",
            "Sexual life",
            "Biometric data",
            "Genetic data",
            "Location data",
            "Judicial or administrative records",
            "Personal financial information",
            "Information about children under 16"
        ]
    }
    
    LEGAL_BASES_VI = {
        "consent": "Sự đồng ý của chủ thể dữ liệu",
        "contract": "Thực hiện hợp đồng",
        "legal_obligation": "Nghĩa vụ pháp lý",
        "vital_interests": "Bảo vệ lợi ích quan trọng",
        "public_interest": "Lợi ích công cộng",
        "legitimate_interest": "Lợi ích hợp pháp"
    }
    
    LEGAL_BASES_EN = {
        "consent": "Data subject consent",
        "contract": "Contract performance",
        "legal_obligation": "Legal obligation",
        "vital_interests": "Vital interests protection",
        "public_interest": "Public interest",
        "legitimate_interest": "Legitimate interest"
    }
    
    @classmethod
    def get_legal_basis_translation(cls, basis_key: str, language: str = "vi") -> str:
        """
        Get legal basis translation in specified language
        
        Args:
            basis_key: Legal basis key (e.g., 'consent', 'contract')
            language: Language code ('vi' or 'en')
            
        Returns:
            Translated legal basis string
            
        Example:
            >>> VietnamesePDPLCategories.get_legal_basis_translation('consent', 'vi')
            'Sự đồng ý của chủ thể dữ liệu'
        """
        if language == "vi":
            return cls.LEGAL_BASES_VI.get(basis_key, basis_key)
        else:
            return cls.LEGAL_BASES_EN.get(basis_key, basis_key)
    
    @classmethod
    def get_all_legal_bases(cls, language: str = "vi") -> List[str]:
        """
        Get all legal bases in specified language
        
        Args:
            language: Language code ('vi' or 'en')
            
        Returns:
            List of all legal basis translations
        """
        if language == "vi":
            return list(cls.LEGAL_BASES_VI.values())
        else:
            return list(cls.LEGAL_BASES_EN.values())
    
    @classmethod
    def is_sensitive_category(cls, category_name: str) -> bool:
        """
        Check if a data category is considered sensitive
        
        Args:
            category_name: Category name (Vietnamese or English)
            
        Returns:
            True if category is sensitive, False otherwise
            
        Example:
            >>> VietnamesePDPLCategories.is_sensitive_category('Dữ liệu sinh trắc học')
            True
        """
        category_lower = category_name.lower()
        
        # Check Vietnamese sensitive categories
        for vi_cat in cls.SENSITIVE_DATA["categories_vi"]:
            if vi_cat.lower() in category_lower or category_lower in vi_cat.lower():
                return True
        
        # Check English sensitive categories
        for en_cat in cls.SENSITIVE_DATA["categories_en"]:
            if en_cat.lower() in category_lower or category_lower in en_cat.lower():
                return True
        
        return False


# Module exports
__all__ = [
    'PDPLROPAField',
    'VietnamesePDPLCategories',
]
