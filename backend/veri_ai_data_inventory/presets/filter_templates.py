# File: backend/veri_ai_data_inventory/presets/filter_templates.py
"""
Predefined column filter templates for Vietnamese PDPL 2025 compliance
Common use cases for DPOs to quickly configure column filtering
"""

from typing import Dict

# Flexible imports for package and standalone execution
try:
    from ..models.column_filter import ColumnFilterConfig, FilterMode
except ImportError:
    from models.column_filter import ColumnFilterConfig, FilterMode


class ColumnFilterTemplates:
    """
    Predefined column filter templates for common Vietnamese PDPL use cases
    
    Templates:
    - PERSONAL_DATA_ONLY: Vietnamese personal data fields (PDPL sensitive)
    - EXCLUDE_SYSTEM_COLUMNS: Exclude technical/system columns
    - FINANCIAL_DATA_ONLY: Financial and banking data only
    - CONTACT_INFO_ONLY: Contact information only
    - ALL_COLUMNS: Scan all columns (no filtering)
    """
    
    # Vietnamese Personal Data (PDPL sensitive data)
    PERSONAL_DATA_ONLY = ColumnFilterConfig(
        mode=FilterMode.INCLUDE,
        column_patterns=[
            # Vietnamese name fields
            "ho_ten", "ten", "ho",
            # ID card numbers (CMND/CCCD)
            "so_cmnd", "so_cccd", "cmnd", "cccd",
            # Phone numbers
            "so_dien_thoai", "dien_thoai", "phone", "mobile",
            # Email
            "email",
            # Address
            "dia_chi", "address", "dia_chi_thuong_tru", "dia_chi_tam_tru",
            # Date of birth
            "ngay_sinh", "date_of_birth", "dob",
            # Gender
            "gioi_tinh", "gender",
            # Bank account
            "so_tai_khoan", "bank_account",
            # Tax ID
            "ma_so_thue", "tax_id", "mst"
        ],
        use_regex=False,
        case_sensitive=False
    )
    
    # Exclude system/technical columns
    EXCLUDE_SYSTEM_COLUMNS = ColumnFilterConfig(
        mode=FilterMode.EXCLUDE,
        column_patterns=[
            # ID columns
            ".*_id$",
            # Timestamp columns
            ".*_timestamp$",
            ".*_created$",
            ".*_updated$",
            ".*_deleted$",
            # Version control
            ".*_version$",
            ".*_hash$",
            # Internal/system columns
            ".*_internal$",
            ".*_system$",
            ".*_temp$",
            ".*_cache$",
            # Common system fields
            "^id$",
            "^created_at$",
            "^updated_at$",
            "^deleted_at$",
            "^modified_at$"
        ],
        use_regex=True,
        case_sensitive=False
    )
    
    # Financial data only
    FINANCIAL_DATA_ONLY = ColumnFilterConfig(
        mode=FilterMode.INCLUDE,
        column_patterns=[
            # Vietnamese financial fields
            "so_tai_khoan", "account_number",
            "so_the", "card_number",
            "so_du", "balance",
            # Amount/value patterns (regex)
            ".*_amount$",
            ".*_value$",
            ".*_price$",
            # Tax ID
            "ma_so_thue", "tax_id", "mst",
            # Income/salary
            "thu_nhap", "income",
            ".*_salary$",
            "luong",
            # Transaction fields
            ".*_transaction$",
            "giao_dich"
        ],
        use_regex=True,
        case_sensitive=False
    )
    
    # Contact information only
    CONTACT_INFO_ONLY = ColumnFilterConfig(
        mode=FilterMode.INCLUDE,
        column_patterns=[
            # Email
            "email",
            # Phone numbers
            "so_dien_thoai", "phone", "mobile", "dien_thoai", "dt",
            # Address
            "dia_chi", "address",
            # Fax
            "fax",
            # Website
            "website", "url"
        ],
        use_regex=False,
        case_sensitive=False
    )
    
    # All columns (no filtering)
    ALL_COLUMNS = ColumnFilterConfig(
        mode=FilterMode.ALL,
        column_patterns=[],
        use_regex=False,
        case_sensitive=False
    )
    
    @classmethod
    def get_template(cls, template_name: str) -> ColumnFilterConfig:
        """
        Get a filter template by name
        
        Args:
            template_name: Name of the template
            
        Returns:
            ColumnFilterConfig for the template
            
        Examples:
            >>> template = ColumnFilterTemplates.get_template('personal_data_only')
            >>> template.mode
            <FilterMode.INCLUDE: 'include'>
        """
        templates = {
            'personal_data_only': cls.PERSONAL_DATA_ONLY,
            'exclude_system_columns': cls.EXCLUDE_SYSTEM_COLUMNS,
            'financial_data_only': cls.FINANCIAL_DATA_ONLY,
            'contact_info_only': cls.CONTACT_INFO_ONLY,
            'all_columns': cls.ALL_COLUMNS
        }
        
        return templates.get(template_name, cls.ALL_COLUMNS)
    
    @classmethod
    def list_templates(cls) -> Dict[str, str]:
        """
        List available templates with descriptions
        
        Returns:
            Dictionary mapping template names to descriptions
        """
        return {
            'personal_data_only': 'Vietnamese personal data fields (PDPL sensitive)',
            'exclude_system_columns': 'Exclude technical/system columns',
            'financial_data_only': 'Financial and banking data only',
            'contact_info_only': 'Contact information only',
            'all_columns': 'Scan all columns (no filtering)'
        }


# Standalone testing
if __name__ == "__main__":
    print("[OK] Column Filter Templates")
    print("\nAvailable templates:")
    for name, desc in ColumnFilterTemplates.list_templates().items():
        print(f"  - {name}: {desc}")
    
    print("\nPersonal Data Only template:")
    personal_template = ColumnFilterTemplates.PERSONAL_DATA_ONLY
    print(f"  Mode: {personal_template.mode}")
    print(f"  Patterns: {len(personal_template.column_patterns)} Vietnamese/English fields")
    print(f"  Sample patterns: {personal_template.column_patterns[:5]}")
