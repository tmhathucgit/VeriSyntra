"""
Standard JSON Exporter for ROPA Documents
Vietnamese PDPL 2025 Compliance - Document #3 Section 7

This module exports ROPA (Record of Processing Activities) to standard JSON format
with bilingual support (Vietnamese/English) and zero hard-coding patterns.

Legal Framework:
- Decree 13/2023/ND-CP Article 12 (ROPA requirements)
- PDPL 2025 Article 17 (Record keeping obligations)

Document #3 Section 7: API Endpoints - JSON Exporter
Version: 1.0.0
"""

import json
from typing import Dict, Any, List
from pathlib import Path

from models.ropa_models import ROPADocument, ROPAEntry, ROPALanguage
from config.ropa_translations import ROPATranslations


class JSONExporter:
    """
    Standard JSON Exporter for ROPA Documents
    
    Generates JSON export with bilingual support and zero hard-coding patterns.
    
    Zero hard-coding pattern:
    - Uses ROPATranslations for field selection (no hardcoded _vi suffix checks)
    - Dictionary routing for language-specific values
    - Enum-based language selection (ROPALanguage.VIETNAMESE/ENGLISH)
    - Helper methods for consistent formatting
    
    Usage:
        JSONExporter.export(document, output_path, ROPALanguage.VIETNAMESE)
    """
    
    @staticmethod
    def export(
        document: ROPADocument,
        output_path: str,
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> None:
        """
        Export ROPA document to JSON file
        
        Creates a JSON file with complete ROPA data in the specified language.
        File is saved with UTF-8 encoding and proper Vietnamese diacritics.
        
        Args:
            document: ROPADocument instance to export
            output_path: Path where JSON file will be saved
            language: ROPALanguage.VIETNAMESE (default) or ENGLISH
        
        Example:
            JSONExporter.export(
                ropa_document,
                "ropa_export.json",
                ROPALanguage.VIETNAMESE
            )
        """
        json_data = JSONExporter._document_to_dict(document, language)
        
        # Write to file with proper encoding for Vietnamese diacritics
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def _document_to_dict(
        document: ROPADocument,
        language: ROPALanguage
    ) -> Dict[str, Any]:
        """
        Convert ROPADocument to dictionary - ZERO HARD-CODING
        
        Uses ROPATranslations helper to get language-specific field values.
        
        Args:
            document: ROPADocument instance
            language: Target language
        
        Returns:
            Dictionary with complete ROPA data
        """
        # Document metadata
        json_data = {
            "document_metadata": {
                "document_id": str(document.document_id),
                "tenant_id": str(document.tenant_id),
                "generated_date": document.generated_date.isoformat(),
                "generated_by": str(document.generated_by),
                "version": document.version,
                "status": document.status,
                "total_processing_activities": document.total_processing_activities,
                "total_data_subjects": document.total_data_subjects,
                "has_sensitive_data": document.has_sensitive_data,
                "has_cross_border_transfers": document.has_cross_border_transfers,
                "mps_submitted": document.mps_submitted,
                "mps_submission_date": document.mps_submission_date.isoformat() if document.mps_submission_date else None,
                "mps_reference_number": document.mps_reference_number
            },
            "business_context": document.veri_business_context,
            "compliance_checklist": document.compliance_checklist,
            "processing_activities": []
        }
        
        # Convert each entry
        for entry in document.entries:
            entry_dict = JSONExporter._entry_to_dict(entry, language)
            json_data["processing_activities"].append(entry_dict)
        
        return json_data
    
    @staticmethod
    def _entry_to_dict(
        entry: ROPAEntry,
        language: ROPALanguage
    ) -> Dict[str, Any]:
        """
        Convert ROPAEntry to dictionary with language-specific values
        
        Uses ROPATranslations.get_field_value() for zero hard-coding.
        
        Args:
            entry: ROPAEntry instance
            language: Target language
        
        Returns:
            Dictionary with entry data in specified language
        """
        translations = ROPATranslations
        
        # GOOD: Use helper method instead of hardcoded _vi suffix checks
        entry_dict = {
            # Identity
            "entry_id": str(entry.entry_id),
            "tenant_id": str(entry.tenant_id),
            
            # Controller Information
            "controller": {
                "name": translations.get_field_value(entry, 'controller_name', language),
                "address": entry.controller_address,
                "tax_id": entry.controller_tax_id,
                "contact_person": entry.controller_contact_person,
                "phone": entry.controller_phone,
                "email": entry.controller_email
            },
            
            # DPO Information (if exists)
            "data_protection_officer": {
                "name": translations.get_field_value(entry, 'dpo_name', language) if entry.dpo_name else None,
                "email": entry.dpo_email,
                "phone": entry.dpo_phone
            } if entry.dpo_name else None,
            
            # Processing Activity Details
            "processing_activity": {
                "name": translations.get_field_value(entry, 'processing_activity_name', language),
                "description": translations.get_field_value(entry, 'processing_activity_description', language),
                "purpose": translations.get_field_value(entry, 'processing_purpose', language),
                "legal_basis": translations.get_field_value(entry, 'legal_basis', language),
                "legal_basis_details": translations.get_field_value(entry, 'legal_basis_details', language)
            },
            
            # Data Categories
            "data_categories": JSONExporter._get_list_values(
                entry.data_categories,
                entry.data_categories_vi,
                language
            ),
            
            # Data Subjects
            "data_subjects": {
                "categories": [cat.value for cat in entry.data_subject_categories],
                "estimated_count": entry.estimated_data_subject_count,
                "description": translations.get_field_value(entry, 'data_subject_description', language)
            },
            
            # Recipients
            "recipients": {
                "categories": [cat.value for cat in entry.recipient_categories],
                "description": translations.get_field_value(entry, 'recipient_description', language)
            },
            
            # Cross-Border Transfer
            "cross_border_transfer": JSONExporter._format_cross_border(
                entry, language
            ) if entry.has_cross_border_transfer else None,
            
            # Data Storage and Retention
            "storage_and_retention": {
                "retention_period": translations.get_field_value(entry, 'retention_period', language),
                "retention_justification": translations.get_field_value(entry, 'retention_justification', language),
                "storage_location": translations.get_field_value(entry, 'storage_location', language),
                "storage_method": translations.get_field_value(entry, 'storage_method', language)
            },
            
            # Security Measures
            "security_measures": JSONExporter._get_list_values(
                entry.security_measures,
                entry.security_measures_vi,
                language
            ),
            
            # Data Subject Rights
            "data_subject_rights": {
                "access_procedure": translations.get_field_value(entry, 'access_procedure', language),
                "correction_procedure": translations.get_field_value(entry, 'correction_procedure', language),
                "deletion_procedure": translations.get_field_value(entry, 'deletion_procedure', language)
            },
            
            # Audit Information
            "audit": {
                "created_at": entry.created_at.isoformat(),
                "created_by": str(entry.created_by),
                "updated_at": entry.updated_at.isoformat(),
                "updated_by": str(entry.updated_by),
                "last_reviewed_date": entry.last_reviewed_date.isoformat() if entry.last_reviewed_date else None,
                "next_review_date": entry.next_review_date.isoformat() if entry.next_review_date else None
            },
            
            # Vietnamese Business Context
            "veri_business_context": entry.veri_activity_context
        }
        
        return entry_dict
    
    @staticmethod
    def _get_list_values(
        english_list: List[str],
        vietnamese_list: List[str],
        language: ROPALanguage
    ) -> List[str]:
        """
        Get list values in specified language - ZERO HARD-CODING
        
        Uses dictionary routing instead of if/else.
        
        Args:
            english_list: English values
            vietnamese_list: Vietnamese values
            language: Target language
        
        Returns:
            List in specified language
        """
        # GOOD: Dictionary routing instead of if language == "vi"
        language_map = {
            ROPALanguage.VIETNAMESE: vietnamese_list,
            ROPALanguage.ENGLISH: english_list
        }
        return language_map.get(language, english_list)
    
    @staticmethod
    def _format_cross_border(
        entry: ROPAEntry,
        language: ROPALanguage
    ) -> Dict[str, Any]:
        """
        Format cross-border transfer information
        
        Args:
            entry: ROPAEntry with cross-border data
            language: Target language
        
        Returns:
            Formatted cross-border transfer dict
        """
        translations = ROPATranslations
        
        return {
            "is_cross_border": entry.has_cross_border_transfer,
            "destination_countries": entry.cross_border_destination_countries,
            "transfer_mechanism": translations.get_field_value(
                entry, 'cross_border_mechanism', language
            ),
            "adequacy_decision": entry.cross_border_adequacy_decision,
            "safeguards": translations.get_field_value(
                entry, 'cross_border_safeguards', language
            ),
            "date_of_transfer": entry.cross_border_transfer_date.isoformat() if entry.cross_border_transfer_date else None
        }


# Export class
__all__ = ['JSONExporter']
