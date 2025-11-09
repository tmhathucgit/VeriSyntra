"""
Standard CSV Exporter for ROPA Documents
Vietnamese PDPL 2025 Compliance - Document #3 Section 7

This module exports ROPA (Record of Processing Activities) to standard CSV format
with bilingual support (Vietnamese/English) and zero hard-coding patterns.

Legal Framework:
- Decree 13/2023/ND-CP Article 12 (ROPA requirements)
- PDPL 2025 Article 17 (Record keeping obligations)

Document #3 Section 7: API Endpoints - CSV Exporter
Version: 1.0.0
"""

import csv
from io import StringIO
from typing import List, Any
from pathlib import Path

from models.ropa_models import ROPADocument, ROPAEntry, ROPALanguage
from config.ropa_translations import ROPATranslations


class CSVExporter:
    """
    Standard CSV Exporter for ROPA Documents
    
    Generates CSV export with bilingual support and zero hard-coding patterns.
    
    CSV Structure (20 columns):
    1. Entry ID
    2. Controller Name
    3. Controller Tax ID
    4. DPO Name
    5. Processing Activity
    6. Purpose
    7. Legal Basis
    8. Data Categories (comma-separated)
    9. Data Subjects (comma-separated)
    10. Data Subject Count
    11. Recipients (comma-separated)
    12. Cross-Border Transfer (Yes/No)
    13. Destination Countries
    14. Retention Period
    15. Storage Location
    16. Security Measures (comma-separated)
    17. Has Sensitive Data
    18. Created Date
    19. Updated Date
    20. Last Reviewed
    
    Zero hard-coding pattern:
    - Uses ROPATranslations for headers and field selection
    - Dictionary routing for language-specific values
    - Enum-based language selection
    - Helper methods for consistent formatting
    
    Usage:
        CSVExporter.export(document, output_path, ROPALanguage.VIETNAMESE)
    """
    
    @staticmethod
    def export(
        document: ROPADocument,
        output_path: str,
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> None:
        """
        Export ROPA document to CSV file
        
        Creates a CSV file with complete ROPA data in the specified language.
        File is saved with UTF-8 BOM encoding for Excel compatibility.
        
        Args:
            document: ROPADocument instance to export
            output_path: Path where CSV file will be saved
            language: ROPALanguage.VIETNAMESE (default) or ENGLISH
        
        Example:
            CSVExporter.export(
                ropa_document,
                "ropa_export.csv",
                ROPALanguage.VIETNAMESE
            )
        """
        csv_content = CSVExporter._generate_csv_content(document, language)
        
        # Write to file with UTF-8 BOM for Excel compatibility
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(csv_content)
    
    @staticmethod
    def _generate_csv_content(
        document: ROPADocument,
        language: ROPALanguage
    ) -> str:
        """
        Generate CSV content string - ZERO HARD-CODING
        
        Args:
            document: ROPADocument instance
            language: Target language
        
        Returns:
            CSV content as string
        """
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        
        # Write headers using translations
        headers = CSVExporter._get_headers(language)
        writer.writerow(headers)
        
        # Write data rows
        for entry in document.entries:
            row = CSVExporter._entry_to_row(entry, language)
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def _get_headers(language: ROPALanguage) -> List[str]:
        """
        Get CSV headers in specified language - ZERO HARD-CODING
        
        Uses dictionary routing for header selection.
        
        Args:
            language: Target language
        
        Returns:
            List of header strings
        """
        # GOOD: Dictionary routing for headers
        headers_map = {
            ROPALanguage.VIETNAMESE: [
                "Mã hoạt động",                    # Entry ID
                "Tên tổ chức",                     # Controller Name
                "Mã số thuế",                      # Tax ID
                "Người bảo vệ dữ liệu",           # DPO Name
                "Hoạt động xử lý",                 # Processing Activity
                "Mục đích",                        # Purpose
                "Cơ sở pháp lý",                   # Legal Basis
                "Loại dữ liệu",                    # Data Categories
                "Chủ thể dữ liệu",                 # Data Subjects
                "Số lượng chủ thể",                # Subject Count
                "Người nhận",                      # Recipients
                "Chuyển giao xuyên biên giới",    # Cross-Border
                "Quốc gia đích",                   # Destination Countries
                "Thời gian lưu trữ",               # Retention Period
                "Nơi lưu trữ",                     # Storage Location
                "Biện pháp bảo mật",               # Security Measures
                "Có dữ liệu nhạy cảm",            # Has Sensitive
                "Ngày tạo",                        # Created Date
                "Ngày cập nhật",                   # Updated Date
                "Xem xét lần cuối"                 # Last Reviewed
            ],
            ROPALanguage.ENGLISH: [
                "Entry ID",
                "Controller Name",
                "Tax ID",
                "Data Protection Officer",
                "Processing Activity",
                "Purpose",
                "Legal Basis",
                "Data Categories",
                "Data Subjects",
                "Subject Count",
                "Recipients",
                "Cross-Border Transfer",
                "Destination Countries",
                "Retention Period",
                "Storage Location",
                "Security Measures",
                "Has Sensitive Data",
                "Created Date",
                "Updated Date",
                "Last Reviewed"
            ]
        }
        
        return headers_map.get(language, headers_map[ROPALanguage.ENGLISH])
    
    @staticmethod
    def _entry_to_row(
        entry: ROPAEntry,
        language: ROPALanguage
    ) -> List[str]:
        """
        Convert ROPAEntry to CSV row - ZERO HARD-CODING
        
        Uses ROPATranslations helper for field value selection.
        
        Args:
            entry: ROPAEntry instance
            language: Target language
        
        Returns:
            List of cell values (20 columns)
        """
        translations = ROPATranslations
        
        # Column 1: Entry ID
        entry_id = str(entry.entry_id)
        
        # Column 2: Controller Name (bilingual support)
        controller_name = translations.get_field_value(
            entry, 'controller_name', language
        )
        
        # Column 3: Tax ID
        tax_id = entry.controller_tax_id or ''
        
        # Column 4: DPO Name (bilingual support)
        dpo_name = translations.get_field_value(
            entry, 'dpo_name', language
        ) if entry.dpo_name else translations.NOT_SPECIFIED.get(language, 'Not specified')
        
        # Column 5: Processing Activity (bilingual support)
        processing_activity = translations.get_field_value(
            entry, 'processing_activity_name', language
        )
        
        # Column 6: Purpose (bilingual support)
        purpose = translations.get_field_value(
            entry, 'processing_purpose', language
        )
        
        # Column 7: Legal Basis (bilingual support)
        legal_basis = translations.get_field_value(
            entry, 'legal_basis', language
        )
        
        # Column 8: Data Categories (comma-separated, bilingual)
        data_categories = CSVExporter._format_list(
            entry.data_categories,
            entry.data_categories_vi,
            language
        )
        
        # Column 9: Data Subjects (enum values)
        data_subjects = ', '.join([cat.value for cat in entry.data_subject_categories])
        
        # Column 10: Subject Count
        subject_count = str(entry.estimated_data_subject_count) if entry.estimated_data_subject_count else ''
        
        # Column 11: Recipients (enum values)
        recipients = ', '.join([cat.value for cat in entry.recipient_categories])
        
        # Column 12: Cross-Border Transfer (Yes/No, bilingual)
        cross_border = CSVExporter._format_boolean(
            entry.has_cross_border_transfer,
            language
        )
        
        # Column 13: Destination Countries (comma-separated)
        destination_countries = ', '.join(
            entry.cross_border_destination_countries
        ) if entry.cross_border_destination_countries else ''
        
        # Column 14: Retention Period (bilingual)
        retention_period = translations.get_field_value(
            entry, 'retention_period', language
        )
        
        # Column 15: Storage Location (bilingual)
        storage_location = translations.get_field_value(
            entry, 'storage_location', language
        )
        
        # Column 16: Security Measures (comma-separated, bilingual)
        security_measures = CSVExporter._format_list(
            entry.security_measures,
            entry.security_measures_vi,
            language
        )
        
        # Column 17: Has Sensitive Data (Yes/No, bilingual)
        has_sensitive = CSVExporter._format_boolean(
            CSVExporter._check_sensitive_data(entry),
            language
        )
        
        # Column 18: Created Date (Vietnamese: dd/mm/yyyy, English: yyyy-mm-dd)
        created_date = entry.created_at.strftime(
            translations.DATE_FORMATS[language]
        )
        
        # Column 19: Updated Date
        updated_date = entry.updated_at.strftime(
            translations.DATE_FORMATS[language]
        )
        
        # Column 20: Last Reviewed
        last_reviewed = entry.last_reviewed_date.strftime(
            translations.DATE_FORMATS[language]
        ) if entry.last_reviewed_date else ''
        
        return [
            entry_id,
            controller_name,
            tax_id,
            dpo_name,
            processing_activity,
            purpose,
            legal_basis,
            data_categories,
            data_subjects,
            subject_count,
            recipients,
            cross_border,
            destination_countries,
            retention_period,
            storage_location,
            security_measures,
            has_sensitive,
            created_date,
            updated_date,
            last_reviewed
        ]
    
    @staticmethod
    def _format_list(
        english_list: List[str],
        vietnamese_list: List[str],
        language: ROPALanguage
    ) -> str:
        """
        Format list to comma-separated string in specified language
        
        Uses dictionary routing instead of if/else.
        
        Args:
            english_list: English values
            vietnamese_list: Vietnamese values
            language: Target language
        
        Returns:
            Comma-separated string
        """
        # GOOD: Dictionary routing
        language_map = {
            ROPALanguage.VIETNAMESE: vietnamese_list,
            ROPALanguage.ENGLISH: english_list
        }
        selected_list = language_map.get(language, english_list)
        return ', '.join(selected_list) if selected_list else ''
    
    @staticmethod
    def _format_boolean(value: bool, language: ROPALanguage) -> str:
        """
        Format boolean to Yes/No in specified language - ZERO HARD-CODING
        
        Uses dictionary routing for bilingual Yes/No.
        
        Args:
            value: Boolean value
            language: Target language
        
        Returns:
            "Yes"/"No" or "Có"/"Không"
        """
        # GOOD: Dictionary routing for bilingual Yes/No
        boolean_map = {
            ROPALanguage.VIETNAMESE: {
                True: "Có",
                False: "Không"
            },
            ROPALanguage.ENGLISH: {
                True: "Yes",
                False: "No"
            }
        }
        
        return boolean_map[language][value]
    
    @staticmethod
    def _check_sensitive_data(entry: ROPAEntry) -> bool:
        """
        Check if entry contains sensitive data categories
        
        Detects keywords indicating sensitive personal data per Vietnamese PDPL.
        
        Args:
            entry: ROPAEntry to check
        
        Returns:
            True if sensitive data detected
        """
        sensitive_keywords = [
            'sensitive', 'health', 'medical', 'biometric', 'genetic',
            'nhạy cảm', 'sức khỏe', 'y tế', 'sinh trắc học', 'di truyền'
        ]
        
        # Check Vietnamese categories
        for category in entry.data_categories_vi:
            if any(keyword in category.lower() for keyword in sensitive_keywords):
                return True
        
        # Check English categories
        for category in entry.data_categories:
            if any(keyword in category.lower() for keyword in sensitive_keywords):
                return True
        
        return False


# Export class
__all__ = ['CSVExporter']
