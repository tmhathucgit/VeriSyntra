"""
MPS (Ministry of Public Security) ROPA Format Exporter
Vietnamese PDPL 2025 - Circular 09/2024/TT-BCA Compliance

This module exports ROPA (Record of Processing Activities) to formats required
by the Vietnamese Ministry of Public Security (Bo Cong an) for PDPL compliance reporting.

Legal Framework:
- Decree 13/2023/ND-CP Article 12 (ROPA requirements)
- PDPL 2025 Article 17 (Record keeping obligations)
- MPS Circular 09/2024/TT-BCA (Reporting format specifications)

Supported Formats:
- CSV: 17-column format for MPS submission
- JSON: 13-field structured format for digital submission

Document #3 Section 5: MPS Reporting Format - COMPLETE
Version: 1.0.0
"""

from models import ROPADocument, ROPAEntry, ROPALanguage, DataSubjectCategory, RecipientCategory
from config import ROPATranslations
import csv
from io import StringIO
from typing import Dict, List, Any, Optional


class MPSFormatExporter:
    """
    Ministry of Public Security (Bộ Công an) ROPA format exporter
    
    Generates CSV and JSON exports compliant with MPS Circular 09/2024/TT-BCA
    requirements for Vietnamese PDPL 2025 Record of Processing Activities reporting.
    
    Zero hard-coding pattern:
    - Uses ROPATranslations for all headers/keys (no string literals)
    - Dictionary routing instead of if/else chains for language switching
    - Enum-based language selection (ROPALanguage.VIETNAMESE/ENGLISH)
    - Helper methods for consistent formatting
    
    Usage:
        exporter = MPSFormatExporter()
        csv_data = exporter.export_to_mps_csv(document, ROPALanguage.VIETNAMESE)
        json_data = exporter.export_to_mps_json(document, ROPALanguage.VIETNAMESE)
    """
    
    def __init__(self):
        """Initialize exporter with translation configuration"""
        self.translations = ROPATranslations
    
    def export_to_mps_csv(
        self, 
        document: ROPADocument, 
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> str:
        """
        Export ROPA to MPS CSV format per Circular 09/2024/TT-BCA
        
        MPS CSV Structure (17 columns):
        1. STT (No) - Sequential number
        2. Tên tổ chức (Organization Name)
        3. Mã số thuế (Tax ID)
        4. Hoạt động xử lý (Processing Activity)
        5. Mục đích (Purpose)
        6. Cơ sở pháp lý (Legal Basis)
        7. Loại dữ liệu (Data Categories)
        8. Chủ thể dữ liệu (Data Subjects)
        9. Người nhận (Recipients)
        10. Chuyển giao XBG (Cross-Border Transfer - Yes/No)
        11. Nước đích (Destination Country)
        12. Thời gian lưu trữ (Retention Period)
        13. Biện pháp bảo mật (Security Measures)
        14. Nơi xử lý (Processing Location)
        15. Người bảo vệ DL (DPO - Data Protection Officer)
        16. Ngày tạo (Created Date)
        17. Ngày cập nhật (Updated Date)
        
        Args:
            document: ROPADocument with processing activity entries
            language: ROPALanguage.VIETNAMESE (default) or ROPALanguage.ENGLISH
        
        Returns:
            CSV string with headers and data rows
            
        Example:
            exporter = MPSFormatExporter()
            csv_output = exporter.export_to_mps_csv(document, ROPALanguage.VIETNAMESE)
            with open('ropa_mps.csv', 'w', encoding='utf-8-sig') as f:
                f.write(csv_output)
        """
        
        # GOOD: Use dictionary routing instead of if/else
        headers = self.translations.MPS_CSV_HEADERS[language]
        
        # Build CSV rows from document entries
        rows = []
        for idx, entry in enumerate(document.entries, start=1):
            row = self._entry_to_mps_csv_row(entry, idx, language)
            rows.append(row)
        
        # Convert to CSV string
        output = StringIO()
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(headers)  # Header row
        writer.writerows(rows)    # Data rows
        
        return output.getvalue()
    
    def _entry_to_mps_csv_row(
        self, 
        entry: ROPAEntry, 
        row_number: int,
        language: ROPALanguage
    ) -> List[str]:
        """
        Convert single ROPAEntry to MPS CSV row (17 columns)
        
        Zero hard-coding pattern:
        - Uses ROPATranslations.get_field_value() for automatic _vi field selection
        - Uses ROPATranslations helper methods for formatting
        - No if/else chains for language switching
        
        Args:
            entry: ROPAEntry Pydantic model
            row_number: Sequential row number (STT)
            language: ROPALanguage enum
        
        Returns:
            List of 17 string values for CSV row
        """
        
        # GOOD: Dynamic field access (auto handles _vi suffix based on language)
        controller_name = self.translations.get_field_value(
            entry, 'controller_name', language
        )
        
        processing_activity = self.translations.get_field_value(
            entry, 'processing_activity_name', language
        )
        
        processing_purpose = self.translations.get_field_value(
            entry, 'processing_purpose', language
        )
        
        legal_basis = self.translations.get_field_value(
            entry, 'legal_basis', language
        )
        
        # GOOD: Use helper method for list formatting
        data_categories = self.translations.format_list(
            self.translations.get_field_value(entry, 'data_categories', language) or [],
            separator=', ',
            empty_value=self.translations.NOT_SPECIFIED[language],
            language=language
        )
        
        # Format data subjects (convert enum to Vietnamese/English)
        data_subjects = self._format_data_subjects(
            entry.data_subject_categories, 
            language
        )
        
        # Format recipients (convert enum to Vietnamese/English)
        recipients = self._format_recipients_list(
            entry.recipients,
            language
        )
        
        # GOOD: Use helper method for boolean formatting
        has_cross_border = self.translations.format_boolean(
            entry.has_cross_border_transfer,
            language
        )
        
        # Cross-border destination (only if transfer exists)
        destination_country = ', '.join(entry.destination_countries) if entry.destination_countries else ''
        
        # Retention period
        retention_period = self.translations.get_field_value(
            entry, 'retention_period', language
        ) or self.translations.NOT_SPECIFIED[language]
        
        # Security measures
        security_measures = self.translations.format_list(
            self.translations.get_field_value(entry, 'security_measures', language) or [],
            separator=', ',
            empty_value=self.translations.NOT_SPECIFIED[language],
            language=language
        )
        
        # Processing location
        processing_location = self.translations.format_list(
            entry.processing_locations or [],
            separator=', ',
            empty_value=self.translations.NOT_SPECIFIED[language],
            language=language
        )
        
        # DPO name
        dpo_name = self.translations.get_field_value(
            entry, 'dpo_name', language
        ) or self.translations.NOT_SPECIFIED[language]
        
        # GOOD: Use date format from translations (Vietnamese: dd/mm/yyyy, English: yyyy-mm-dd)
        created_date = entry.created_at.strftime(
            self.translations.DATE_FORMATS[language]
        )
        
        updated_date = entry.updated_at.strftime(
            self.translations.DATE_FORMATS[language]
        )
        
        # Return 17-column row
        return [
            str(row_number),              # Column 1: STT
            controller_name,              # Column 2: Tên tổ chức
            entry.controller_tax_id or '',# Column 3: Mã số thuế
            processing_activity,          # Column 4: Hoạt động xử lý
            processing_purpose,           # Column 5: Mục đích
            legal_basis,                  # Column 6: Cơ sở pháp lý
            data_categories,              # Column 7: Loại dữ liệu
            data_subjects,                # Column 8: Chủ thể dữ liệu
            recipients,                   # Column 9: Người nhận
            has_cross_border,             # Column 10: Chuyển giao XBG
            destination_country,          # Column 11: Nước đích
            retention_period,             # Column 12: Thời gian lưu trữ
            security_measures,            # Column 13: Biện pháp bảo mật
            processing_location,          # Column 14: Nơi xử lý
            dpo_name,                     # Column 15: Người bảo vệ DL
            created_date,                 # Column 16: Ngày tạo
            updated_date                  # Column 17: Ngày cập nhật
        ]
    
    def export_to_mps_json(
        self, 
        document: ROPADocument, 
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> Dict[str, Any]:
        """
        Export ROPA to MPS JSON format per Circular 09/2024/TT-BCA
        
        MPS JSON Structure:
        {
            "metadata": {
                "document_id": "uuid-string",
                "tenant_id": "uuid-string",
                "generated_date": "dd/mm/yyyy",
                "generated_by": "uuid-string",
                "version": "1.0.0",
                "total_activities": 10,
                "language": "vi"
            },
            "entries": [
                {
                    "ten_to_chuc": "Công ty TNHH ABC",  # Vietnamese keys
                    "ma_so_thue": "0123456789",
                    "hoat_dong_xu_ly": "Quản lý khách hàng",
                    ... (13 fields total)
                }
            ],
            "summary": {
                "total_data_subjects": 5,
                "has_sensitive_data": true,
                "has_cross_border_transfers": false
            }
        }
        
        Args:
            document: ROPADocument with processing activity entries
            language: ROPALanguage.VIETNAMESE (default) or ROPALanguage.ENGLISH
        
        Returns:
            Dictionary with MPS-compliant JSON structure
            
        Example:
            exporter = MPSFormatExporter()
            json_output = exporter.export_to_mps_json(document, ROPALanguage.VIETNAMESE)
            import json
            with open('ropa_mps.json', 'w', encoding='utf-8') as f:
                json.dump(json_output, f, ensure_ascii=False, indent=2)
        """
        
        # GOOD: Use date format from translations
        generated_date = document.generated_date.strftime(
            self.translations.DATE_FORMATS[language]
        )
        
        # Build metadata section
        metadata = {
            "document_id": str(document.document_id),
            "tenant_id": str(document.tenant_id),
            "generated_date": generated_date,
            "generated_by": str(document.generated_by),
            "version": document.version,
            "total_activities": document.total_processing_activities,
            "language": language.value
        }
        
        # Convert entries to JSON objects
        entries = [
            self._entry_to_mps_json_object(entry, language)
            for entry in document.entries
        ]
        
        # Build summary section
        summary = {
            "total_data_subjects": document.total_data_subjects,
            "has_sensitive_data": document.has_sensitive_data,
            "has_cross_border_transfers": document.has_cross_border_transfers
        }
        
        # Return complete JSON structure
        return {
            "metadata": metadata,
            "entries": entries,
            "summary": summary
        }
    
    def _entry_to_mps_json_object(
        self, 
        entry: ROPAEntry, 
        language: ROPALanguage
    ) -> Dict[str, Any]:
        """
        Convert single ROPAEntry to MPS JSON object
        
        MPS JSON uses Vietnamese/English field names from MPS_JSON_KEYS:
        - Vietnamese: ten_to_chuc, ma_so_thue, hoat_dong_xu_ly, etc.
        - English: organization_name, tax_id, processing_activity, etc.
        
        Args:
            entry: ROPAEntry Pydantic model
            language: ROPALanguage enum
        
        Returns:
            Dictionary with MPS JSON field structure (13 fields)
        """
        
        # GOOD: Get Vietnamese/English keys from translations (no hard-coding)
        keys = self.translations.MPS_JSON_KEYS[language]
        
        # Format data categories list
        data_categories = self.translations.format_list(
            self.translations.get_field_value(entry, 'data_categories', language) or [],
            separator=', ',
            empty_value=self.translations.NOT_SPECIFIED[language],
            language=language
        )
        
        # Format data subjects
        data_subjects = self._format_data_subjects(
            entry.data_subject_categories,
            language
        )
        
        # Format recipients
        recipients = self._format_recipients_list(
            entry.recipients,
            language
        )
        
        # Format boolean
        has_cross_border = self.translations.format_boolean(
            entry.has_cross_border_transfer,
            language
        )
        
        # Format security measures
        security_measures = self.translations.format_list(
            self.translations.get_field_value(entry, 'security_measures', language) or [],
            separator=', ',
            empty_value=self.translations.NOT_SPECIFIED[language],
            language=language
        )
        
        # Format date
        updated_date = entry.updated_at.strftime(
            self.translations.DATE_FORMATS[language]
        )
        
        # GOOD: Build dictionary using translation keys (supports Vietnamese and English)
        return {
            keys["controller_name"]: self.translations.get_field_value(entry, 'controller_name', language),
            keys["tax_id"]: entry.controller_tax_id or '',
            keys["activity"]: self.translations.get_field_value(entry, 'processing_activity_name', language),
            keys["purpose"]: self.translations.get_field_value(entry, 'processing_purpose', language),
            keys["legal_basis"]: self.translations.get_field_value(entry, 'legal_basis', language),
            keys["data_categories"]: data_categories,
            keys["data_subjects"]: data_subjects,
            keys["recipients"]: recipients,
            keys["cross_border"]: has_cross_border,
            keys["destination_countries"]: ', '.join(entry.destination_countries) if entry.destination_countries else '',
            keys["retention"]: self.translations.get_field_value(entry, 'retention_period', language) or self.translations.NOT_SPECIFIED[language],
            keys["security"]: security_measures,
            keys["updated_date"]: updated_date
        }
    
    def validate_mps_compliance(
        self, 
        document: ROPADocument
    ) -> Dict[str, Any]:
        """
        Validate ROPA document for MPS submission readiness
        
        MPS Requirements per Circular 09/2024/TT-BCA:
        - All mandatory fields present (Decree 13 Article 12)
        - DPO appointed if required (organizations with >50,000 data subjects)
        - Cross-border transfers documented with destination and legal basis
        - Legal basis specified for all processing activities
        - Retention period defined for all data categories
        
        Args:
            document: ROPADocument to validate
        
        Returns:
            Bilingual validation result:
            {
                'is_compliant': bool,
                'is_compliant_vi': str ('Tuan thu' or 'Khong tuan thu'),
                'missing_fields': list[str],
                'missing_fields_vi': list[str],
                'warnings': list[str],
                'warnings_vi': list[str],
                'recommendations': list[str],
                'recommendations_vi': list[str]
            }
            
        Example:
            exporter = MPSFormatExporter()
            validation = exporter.validate_mps_compliance(document)
            if not validation['is_compliant']:
                print(f"Missing fields: {validation['missing_fields_vi']}")
        """
        
        missing_fields = []
        missing_fields_vi = []
        warnings = []
        warnings_vi = []
        recommendations = []
        recommendations_vi = []
        
        # Check document-level requirements
        if not document.entries or len(document.entries) == 0:
            missing_fields.append("No processing activities recorded")
            missing_fields_vi.append("Không có hoạt động xử lý nào được ghi nhận")
        
        # Check each entry for mandatory fields
        for idx, entry in enumerate(document.entries, start=1):
            entry_num = f"Entry {idx}"
            entry_num_vi = f"Mục {idx}"
            
            # Article 12.1.a - Controller information
            if not entry.controller_name or not entry.controller_name_vi:
                missing_fields.append(f"{entry_num}: Controller name missing")
                missing_fields_vi.append(f"{entry_num_vi}: Thiếu tên tổ chức xử lý")
            
            if not entry.controller_tax_id:
                warnings.append(f"{entry_num}: Tax ID not specified")
                warnings_vi.append(f"{entry_num_vi}: Chưa xác định mã số thuế")
            
            # Article 12.1.c - Processing activity and purpose
            if not entry.processing_activity_name or not entry.processing_activity_name_vi:
                missing_fields.append(f"{entry_num}: Processing activity name missing")
                missing_fields_vi.append(f"{entry_num_vi}: Thiếu tên hoạt động xử lý")
            
            if not entry.processing_purpose or not entry.processing_purpose_vi:
                missing_fields.append(f"{entry_num}: Processing purpose missing")
                missing_fields_vi.append(f"{entry_num_vi}: Thiếu mục đích xử lý")
            
            if not entry.legal_basis or not entry.legal_basis_vi:
                missing_fields.append(f"{entry_num}: Legal basis missing")
                missing_fields_vi.append(f"{entry_num_vi}: Thiếu cơ sở pháp lý")
            
            # Article 12.1.d - Data categories
            if not entry.data_categories or len(entry.data_categories) == 0:
                missing_fields.append(f"{entry_num}: Data categories not specified")
                missing_fields_vi.append(f"{entry_num_vi}: Chưa xác định loại dữ liệu")
            
            if not entry.data_categories_vi or len(entry.data_categories_vi) == 0:
                missing_fields.append(f"{entry_num}: Vietnamese data categories missing")
                missing_fields_vi.append(f"{entry_num_vi}: Thiếu loại dữ liệu tiếng Việt")
            
            # Article 12.1.g - Cross-border transfer
            if entry.has_cross_border_transfer:
                if not entry.destination_countries or len(entry.destination_countries) == 0:
                    warnings.append(f"{entry_num}: Cross-border destination country not specified")
                    warnings_vi.append(f"{entry_num_vi}: Chưa xác định nước đích chuyển giao")
                
                if not entry.transfer_mechanism:
                    warnings.append(f"{entry_num}: Cross-border transfer mechanism not documented")
                    warnings_vi.append(f"{entry_num_vi}: Chưa ghi nhận cơ chế chuyển giao XBG")
                
                recommendations.append(f"{entry_num}: Ensure Article 20 compliance for cross-border transfer")
                recommendations_vi.append(f"{entry_num_vi}: Đảm bảo tuân thủ Điều 20 cho chuyển giao xuyên biên giới")
            
            # Article 12.1.h - Retention period
            if not entry.retention_period or not entry.retention_period_vi:
                warnings.append(f"{entry_num}: Retention period not specified")
                warnings_vi.append(f"{entry_num_vi}: Chưa xác định thời gian lưu trữ")
            
            # Article 12.1.i - Security measures
            if not entry.security_measures or len(entry.security_measures) == 0:
                warnings.append(f"{entry_num}: Security measures not documented")
                warnings_vi.append(f"{entry_num_vi}: Chưa ghi nhận biện pháp bảo mật")
            
            # Article 12.1.b - DPO (required if handling sensitive data or >50k subjects)
            if entry.has_sensitive_data or document.total_data_subjects > 50000:
                if not entry.dpo_name and not entry.dpo_name_vi:
                    recommendations.append(f"{entry_num}: DPO appointment recommended for sensitive data")
                    recommendations_vi.append(f"{entry_num_vi}: Nên bổ nhiệm người bảo vệ dữ liệu cho dữ liệu nhạy cảm")
        
        # Overall compliance determination
        is_compliant = len(missing_fields) == 0
        
        return {
            'is_compliant': is_compliant,
            'is_compliant_vi': 'Tuân thủ' if is_compliant else 'Không tuân thủ',
            'status': 'compliant' if is_compliant else ('requires_review' if len(warnings) > 0 else 'non_compliant'),
            'status_vi': 'tuân thủ' if is_compliant else ('cần xem xét' if len(warnings) > 0 else 'không tuân thủ'),
            'missing_fields': missing_fields,
            'missing_fields_vi': missing_fields_vi,
            'warnings': warnings,
            'warnings_vi': warnings_vi,
            'recommendations': recommendations,
            'recommendations_vi': recommendations_vi,
            'total_issues': len(missing_fields) + len(warnings),
            'mps_submission_ready': is_compliant and len(warnings) == 0
        }
    
    def _format_data_subjects(
        self, 
        categories: List[DataSubjectCategory],
        language: ROPALanguage
    ) -> str:
        """
        Format data subject categories for display
        
        Converts DataSubjectCategory enums to Vietnamese/English text:
        - CUSTOMERS -> "Khach hang" (VI) or "Customers" (EN)
        - EMPLOYEES -> "Nhan vien" (VI) or "Employees" (EN)
        
        Args:
            categories: List of DataSubjectCategory enums
            language: ROPALanguage enum
        
        Returns:
            Formatted string (comma-separated)
        """
        if not categories or len(categories) == 0:
            return self.translations.NOT_SPECIFIED[language]
        
        # GOOD: Use dictionary mapping instead of if/else chains
        vietnamese_mapping = {
            DataSubjectCategory.CUSTOMERS: "Khách hàng",
            DataSubjectCategory.EMPLOYEES: "Nhân viên",
            DataSubjectCategory.SUPPLIERS: "Nhà cung cấp",
            DataSubjectCategory.PARTNERS: "Đối tác",
            DataSubjectCategory.WEBSITE_VISITORS: "Người truy cập website",
            DataSubjectCategory.CHILDREN: "Trẻ em"
        }
        
        english_mapping = {
            DataSubjectCategory.CUSTOMERS: "Customers",
            DataSubjectCategory.EMPLOYEES: "Employees",
            DataSubjectCategory.SUPPLIERS: "Suppliers",
            DataSubjectCategory.PARTNERS: "Partners",
            DataSubjectCategory.WEBSITE_VISITORS: "Website Visitors",
            DataSubjectCategory.CHILDREN: "Children"
        }
        
        # GOOD: Dictionary routing
        mapping = vietnamese_mapping if language == ROPALanguage.VIETNAMESE else english_mapping
        
        formatted_categories = [mapping.get(cat, str(cat)) for cat in categories]
        return ', '.join(formatted_categories)
    
    def _format_recipients(
        self,
        categories: List[RecipientCategory],
        language: ROPALanguage
    ) -> str:
        """
        Format recipient categories for display
        
        Converts RecipientCategory enums to Vietnamese/English text:
        - INTERNAL -> "Noi bo" (VI) or "Internal" (EN)
        - PROCESSOR -> "Ben xu ly" (VI) or "Data Processors" (EN)
        
        Args:
            categories: List of RecipientCategory enums
            language: ROPALanguage enum
        
        Returns:
            Formatted string (comma-separated)
        """
        if not categories or len(categories) == 0:
            return self.translations.NOT_SPECIFIED[language]
        
        # GOOD: Use dictionary mapping
        vietnamese_mapping = {
            RecipientCategory.INTERNAL: "Nội bộ",
            RecipientCategory.PROCESSOR: "Bên xử lý",
            RecipientCategory.THIRD_PARTY: "Bên thứ ba",
            RecipientCategory.PUBLIC_AUTHORITY: "Cơ quan nhà nước",
            RecipientCategory.FOREIGN_ENTITY: "Tổ chức nước ngoài"
        }
        
        english_mapping = {
            RecipientCategory.INTERNAL: "Internal",
            RecipientCategory.PROCESSOR: "Data Processors",
            RecipientCategory.THIRD_PARTY: "Third Parties",
            RecipientCategory.PUBLIC_AUTHORITY: "Public Authorities",
            RecipientCategory.FOREIGN_ENTITY: "Foreign Entities"
        }
        
        # GOOD: Dictionary routing
        mapping = vietnamese_mapping if language == ROPALanguage.VIETNAMESE else english_mapping
        
        formatted_categories = [mapping.get(cat, str(cat)) for cat in categories]
        return ', '.join(formatted_categories)
    
    def _format_recipients_list(
        self,
        recipients: List[Dict[str, Any]],
        language: ROPALanguage
    ) -> str:
        """
        Format recipients list from ROPAEntry
        
        Converts recipients list to formatted string:
        - recipients: [{"name": "AWS", "type": "processor", "country": "SG"}]
        - Output (VI): "AWS (Ben xu ly - SG)"
        - Output (EN): "AWS (Data Processors - SG)"
        
        Args:
            recipients: List of recipient dictionaries from ROPAEntry
            language: ROPALanguage enum
        
        Returns:
            Formatted string (comma-separated)
        """
        if not recipients or len(recipients) == 0:
            return self.translations.NOT_SPECIFIED[language]
        
        # GOOD: Use dictionary mapping for recipient types
        vietnamese_type_mapping = {
            "internal": "Nội bộ",
            "processor": "Bên xử lý",
            "third_party": "Bên thứ ba",
            "public_authority": "Cơ quan nhà nước",
            "foreign_entity": "Tổ chức nước ngoài"
        }
        
        english_type_mapping = {
            "internal": "Internal",
            "processor": "Data Processors",
            "third_party": "Third Parties",
            "public_authority": "Public Authorities",
            "foreign_entity": "Foreign Entities"
        }
        
        # GOOD: Dictionary routing
        type_mapping = vietnamese_type_mapping if language == ROPALanguage.VIETNAMESE else english_type_mapping
        
        formatted_recipients = []
        for recipient in recipients:
            name = recipient.get("name", "")
            recipient_type = recipient.get("type", "")
            country = recipient.get("country", "")
            
            type_label = type_mapping.get(recipient_type, recipient_type)
            
            if country:
                formatted = f"{name} ({type_label} - {country})"
            else:
                formatted = f"{name} ({type_label})"
            
            formatted_recipients.append(formatted)
        
        return ', '.join(formatted_recipients)


    @staticmethod
    def export(
        document: ROPADocument,
        output_path: str,
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> None:
        """
        Export ROPA to MPS JSON format - Unified interface for service layer
        
        This method provides a unified interface matching JSON/CSV exporters.
        Exports to MPS JSON format per Circular 09/2024/TT-BCA.
        
        Args:
            document: ROPADocument instance
            output_path: Path where JSON file will be saved
            language: ROPALanguage enum (VIETNAMESE or ENGLISH)
        
        Example:
            MPSFormatExporter.export(
                ropa_document,
                "ropa_mps.json",
                ROPALanguage.VIETNAMESE
            )
        """
        exporter = MPSFormatExporter()
        json_data = exporter.export_to_mps_json(document, language)
        
        # Write to file with proper encoding for Vietnamese diacritics
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)


__all__ = ['MPSFormatExporter']
