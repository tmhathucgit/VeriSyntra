"""
Export Reporting Service - Section 10
Vietnamese PDPL 2025 Compliance Report Generation

Generates compliance reports in multiple formats (JSON, PDF, XLSX) with:
- Bilingual Vietnamese-first output
- Zero hard-coding (enum-based routing)
- Config-driven report structures
- MPS Circular 09/2024 compliance

Author: VeriSyntra AI Data Inventory Team
Date: November 5, 2025
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json

# Section 7 imports - Zero hard-coding dependencies
from config.reporting_constants import (
    ReportType,
    OutputFormat,
    RiskLevel,
    ReportingConfig
)

# Section 8 imports - Data lineage integration
from services.lineage_graph_service import DataLineageGraphService

# Section 5 imports - Cross-border validation
# from compliance.cross_border_validator import CrossBorderValidator

# Section 6 imports - ROPA integration
# from compliance.processing_activity_mapper import ProcessingActivityMapper


class ExportReportingService:
    """
    PDPL 2025 Compliance Report Generation Service
    
    Generates Vietnamese-first bilingual reports in multiple formats:
    - JSON: Immediate viewing in VeriPortal UI
    - PDF: Print-ready MPS submission documents
    - XLSX: Excel workbooks for data analysis
    
    Features:
    - Zero hard-coding: All routing via ReportType enum
    - Config-driven: Uses ReportingConfig for all structures
    - Bilingual: Vietnamese-first with automatic _vi fields
    - PDPL compliant: MPS Circular 09/2024 format
    """
    
    def __init__(self, db_session=None, cultural_engine=None):
        """
        Initialize Export Reporting Service
        
        Args:
            db_session: Database session for data queries
            cultural_engine: Vietnamese cultural intelligence engine
        """
        self.db = db_session
        self.cultural_engine = cultural_engine
        self.lineage_service = DataLineageGraphService(db_session, cultural_engine)
        
        # Dictionary-based generator routing (zero hard-coding)
        self._report_generators = {
            ReportType.MPS_CIRCULAR_09_2024: self._generate_mps_report,
            ReportType.EXECUTIVE_SUMMARY: self._generate_executive_summary,
            ReportType.AUDIT_TRAIL: self._generate_audit_trail,
            ReportType.DATA_INVENTORY: self._generate_data_inventory,
            ReportType.THIRD_PARTY_TRANSFERS: self._generate_third_party_report,
            ReportType.DSR_ACTIVITY: self._generate_dsr_report
        }
        
        # Dictionary-based formatter routing (zero hard-coding)
        self._output_formatters = {
            OutputFormat.JSON: self._format_as_json,
            OutputFormat.PDF: self._format_as_pdf,
            OutputFormat.XLSX: self._format_as_xlsx
        }
    
    async def generate_report(
        self,
        veri_business_id: str,
        report_type: ReportType,
        output_format: OutputFormat = OutputFormat.JSON,
        date_range: Optional[Dict[str, datetime]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate PDPL compliance report
        
        Args:
            veri_business_id: Vietnamese business identifier
            report_type: Type of report (ReportType enum)
            output_format: Output format (OutputFormat enum)
            date_range: Optional date range filter {"start": datetime, "end": datetime}
            filters: Optional additional filters
        
        Returns:
            Dict with report data and metadata:
            {
                "report_type": str,
                "report_type_vi": str,
                "output_format": str,
                "output_format_vi": str,
                "generated_at": str,
                "data": Dict[str, Any],
                "metadata": Dict[str, Any]
            }
        """
        # Validate report type (enum ensures type safety)
        if report_type not in self._report_generators:
            raise ValueError(f"Unsupported report type: {report_type}")
        
        # Get report generator from dictionary (zero hard-coding)
        generator = self._report_generators[report_type]
        
        # Generate report data
        report_data = await generator(
            veri_business_id=veri_business_id,
            date_range=date_range,
            filters=filters
        )
        
        # Add bilingual metadata
        report_with_metadata = {
            "report_type": report_type.value,
            "report_type_vi": ReportingConfig.translate_to_vietnamese(
                report_type.value, "report_type"
            ),
            "output_format": output_format.value,
            "output_format_vi": self._translate_output_format(output_format),
            "generated_at": datetime.utcnow().isoformat(),
            "veri_business_id": veri_business_id,
            "data": report_data,
            "metadata": {
                "date_range": date_range,
                "filters": filters,
                "cultural_context": await self._get_cultural_context(veri_business_id)
            }
        }
        
        # Format output (dictionary routing)
        formatter = self._output_formatters[output_format]
        formatted_output = await formatter(report_with_metadata)
        
        return formatted_output
    
    # ========================================================================
    # REPORT GENERATORS (6 types - config-driven)
    # ========================================================================
    
    async def _generate_mps_report(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate MPS Circular 09/2024 compliance report
        Vietnamese: Báo cáo Bộ Công an (Thông tư 09/2024)
        
        Official format for Ministry of Public Security submission
        """
        config = ReportingConfig.MPS_REPORT_CONFIG
        
        # Section 1: Business Information (Thông tin Doanh nghiệp)
        business_info = await self._get_business_information(veri_business_id)
        
        # Section 2: Data Inventory (Danh mục Dữ liệu)
        data_inventory = await self._get_data_inventory(veri_business_id)
        
        # Section 3: Processing Activities (Hoạt động Xử lý)
        processing_activities = await self._get_processing_activities(veri_business_id)
        
        # Section 4: Cross-Border Transfers (Chuyển giao Xuyên biên giới)
        cross_border_transfers = await self._get_cross_border_transfers(veri_business_id)
        
        # Section 5: Security Measures (Biện pháp Bảo mật)
        security_measures = await self._get_security_measures(veri_business_id)
        
        # Section 6: DPO Information (Thông tin Cán bộ Bảo vệ Dữ liệu)
        dpo_info = await self._get_dpo_information(veri_business_id)
        
        # Compliance scoring
        compliance_score = self._calculate_compliance_score({
            "business_info": business_info,
            "data_inventory": data_inventory,
            "processing_activities": processing_activities,
            "cross_border_transfers": cross_border_transfers,
            "security_measures": security_measures,
            "dpo_info": dpo_info
        })
        
        return {
            "title": config["title"],
            "title_en": config["title_en"],
            "circular_reference": config["circular_reference"],
            "authority": config["authority"],
            "authority_en": config["authority_en"],
            "sections": {
                "business_information": business_info,
                "data_inventory": data_inventory,
                "processing_activities": processing_activities,
                "cross_border_transfers": cross_border_transfers,
                "security_measures": security_measures,
                "dpo_information": dpo_info
            },
            "compliance_score": compliance_score,
            "compliance_score_vi": self._translate_compliance_score(compliance_score),
            "recommendations": self._generate_recommendations(compliance_score),
            "recommendations_vi": self._generate_recommendations_vi(compliance_score)
        }
    
    async def _generate_executive_summary(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate executive summary report
        Vietnamese: Báo cáo Tóm tắt Điều hành
        
        High-level overview for board/management
        """
        config = ReportingConfig.EXECUTIVE_SUMMARY_CONFIG
        
        # Get key metrics
        total_data_fields = await self._count_data_fields(veri_business_id)
        total_processing_activities = await self._count_processing_activities(veri_business_id)
        cross_border_count = await self._count_cross_border_transfers(veri_business_id)
        
        # Risk assessment
        risk_score = await self._calculate_overall_risk(veri_business_id)
        risk_level = ReportingConfig.get_risk_level(risk_score)
        
        # Compliance status
        compliance_status = await self._get_compliance_status(veri_business_id)
        
        return {
            "title": config["title"],
            "title_en": config["title_en"],
            "summary": {
                "total_data_fields": total_data_fields,
                "total_processing_activities": total_processing_activities,
                "cross_border_transfers": cross_border_count,
                "risk_score": risk_score,
                "risk_level": risk_level.value,
                "risk_level_vi": ReportingConfig.translate_to_vietnamese(
                    risk_level.value, "risk_level"
                ),
                "compliance_status": compliance_status,
                "compliance_status_vi": self._translate_compliance_status(compliance_status)
            },
            "key_findings": await self._get_key_findings(veri_business_id),
            "key_findings_vi": await self._get_key_findings_vi(veri_business_id),
            "action_items": self._generate_action_items(risk_score, compliance_status),
            "action_items_vi": self._generate_action_items_vi(risk_score, compliance_status)
        }
    
    async def _generate_audit_trail(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate audit trail report
        Vietnamese: Nhật ký Kiểm toán
        
        Detailed activity logs for compliance audits
        """
        config = ReportingConfig.AUDIT_TRAIL_CONFIG
        
        # Fetch audit events
        events = await self._fetch_audit_events(
            veri_business_id,
            date_range,
            filters
        )
        
        # Categorize by event type
        events_by_type = self._categorize_events(events, config["event_types"])
        
        return {
            "title": config["title"],
            "title_en": config["title_en"],
            "retention_days": config["retention_days"],
            "event_types": config["event_types"],
            "total_events": len(events),
            "events_by_type": events_by_type,
            "events_by_type_vi": self._translate_events_by_type(events_by_type),
            "events": events,
            "date_range": date_range
        }
    
    async def _generate_data_inventory(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate data inventory report
        Vietnamese: Danh mục Dữ liệu
        
        Complete ROPA (Record of Processing Activities) export
        """
        config = ReportingConfig.DATA_INVENTORY_CONFIG
        
        # Fetch all data fields
        data_fields = await self._fetch_all_data_fields(veri_business_id, filters)
        
        # Group by category
        fields_by_category = self._group_by_category(data_fields)
        
        # Get storage locations
        storage_locations = await self._get_storage_locations(veri_business_id)
        
        return {
            "title": config["title"],
            "title_en": config["title_en"],
            "total_fields": len(data_fields),
            "fields_by_category": fields_by_category,
            "fields_by_category_vi": self._translate_fields_by_category(fields_by_category),
            "storage_locations": storage_locations,
            "storage_locations_vi": self._translate_storage_locations(storage_locations),
            "data_fields": data_fields
        }
    
    async def _generate_third_party_report(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate third-party transfer report
        Vietnamese: Chuyển giao Bên thứ ba
        
        PDPL Article 20 compliance report for external data transfers
        """
        config = ReportingConfig.THIRD_PARTY_DASHBOARD_CONFIG
        
        # Fetch third-party vendors
        vendors = await self._fetch_third_party_vendors(veri_business_id)
        
        # Calculate risk scores for each vendor
        vendors_with_risk = []
        for vendor in vendors:
            risk_score = self._calculate_vendor_risk_score(vendor, config)
            risk_level = ReportingConfig.get_risk_level(risk_score)
            
            vendors_with_risk.append({
                **vendor,
                "risk_score": risk_score,
                "risk_level": risk_level.value,
                "risk_level_vi": ReportingConfig.translate_to_vietnamese(
                    risk_level.value, "risk_level"
                )
            })
        
        # Group by risk level
        vendors_by_risk = self._group_by_risk_level(vendors_with_risk)
        
        return {
            "title": config["title"],
            "title_en": config["title_en"],
            "total_vendors": len(vendors),
            "risk_factors": config["risk_factors"],
            "risk_weights": config["risk_weights"],
            "vendors_by_risk": vendors_by_risk,
            "vendors_by_risk_vi": self._translate_vendors_by_risk(vendors_by_risk),
            "vendors": vendors_with_risk
        }
    
    async def _generate_dsr_report(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate DSR (Data Subject Rights) activity report
        Vietnamese: Hoạt động Yêu cầu Quyền Dữ liệu
        
        Track compliance with PDPL Article 19 (data subject rights)
        """
        config = ReportingConfig.DSR_REPORT_CONFIG
        
        # Fetch DSR requests
        dsr_requests = await self._fetch_dsr_requests(
            veri_business_id,
            date_range,
            filters
        )
        
        # Categorize by request type
        requests_by_type = self._categorize_dsr_requests(dsr_requests)
        
        # Calculate fulfillment metrics
        fulfillment_metrics = self._calculate_fulfillment_metrics(dsr_requests)
        
        return {
            "title": config["title"],
            "title_en": config["title_en"],
            "request_types": config["request_types"],
            "total_requests": len(dsr_requests),
            "requests_by_type": requests_by_type,
            "requests_by_type_vi": self._translate_requests_by_type(requests_by_type),
            "fulfillment_metrics": fulfillment_metrics,
            "fulfillment_metrics_vi": self._translate_fulfillment_metrics(fulfillment_metrics),
            "requests": dsr_requests
        }
    
    # ========================================================================
    # OUTPUT FORMATTERS (3 formats)
    # ========================================================================
    
    async def _format_as_json(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format report as JSON (fully functional)
        
        Returns complete bilingual report data for immediate viewing
        in VeriPortal UI with React components
        """
        return {
            "format": "json",
            "format_vi": "JSON",
            "status": "complete",
            "status_vi": "hoàn thành",
            "output": report_data
        }
    
    async def _format_as_pdf(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format report as PDF (placeholder implementation)
        
        TODO: Full implementation requires:
        - ReportLab library installation
        - Vietnamese font support (DejaVu Sans, Noto Sans)
        - MPS template design (A4, official header/footer)
        - PII redaction before output
        
        Returns placeholder with JSON data for now
        """
        return {
            "format": "pdf",
            "format_vi": "PDF",
            "status": "placeholder",
            "status_vi": "giữ chỗ",
            "message": "PDF generation requires ReportLab library - returning JSON data",
            "message_vi": "Tạo PDF yêu cầu thư viện ReportLab - trả về dữ liệu JSON",
            "output": report_data,
            "future_enhancement": {
                "library": "reportlab",
                "vietnamese_fonts": ["DejaVu Sans", "Noto Sans Vietnamese"],
                "template": "MPS Circular 09/2024 official format"
            }
        }
    
    async def _format_as_xlsx(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format report as Excel workbook (placeholder implementation)
        
        TODO: Full implementation requires:
        - openpyxl library installation
        - Multi-sheet workbook structure
        - Conditional formatting for risk levels
        - Vietnamese text encoding support
        
        Returns placeholder with JSON data for now
        """
        return {
            "format": "xlsx",
            "format_vi": "Excel",
            "status": "placeholder",
            "status_vi": "giữ chỗ",
            "message": "Excel generation requires openpyxl library - returning JSON data",
            "message_vi": "Tạo Excel yêu cầu thư viện openpyxl - trả về dữ liệu JSON",
            "output": report_data,
            "future_enhancement": {
                "library": "openpyxl",
                "features": [
                    "Multi-sheet workbooks",
                    "Conditional formatting",
                    "Vietnamese text support",
                    "Charts and graphs"
                ]
            }
        }
    
    # ========================================================================
    # HELPER METHODS (Data fetching and processing)
    # ========================================================================
    
    async def _get_business_information(self, veri_business_id: str) -> Dict[str, Any]:
        """Fetch business information from database"""
        # TODO: Implement database query
        return {
            "business_id": veri_business_id,
            "business_name": f"Business {veri_business_id}",
            "business_name_vi": f"Doanh nghiệp {veri_business_id}",
            "registration_number": "1234567890",
            "industry": "technology",
            "industry_vi": "công nghệ",
            "region": "south",
            "region_vi": "miền Nam"
        }
    
    async def _get_data_inventory(self, veri_business_id: str) -> Dict[str, Any]:
        """Fetch data inventory from database"""
        # TODO: Implement database query
        return {
            "total_fields": 0,
            "categories": [],
            "sensitivity_levels": {}
        }
    
    async def _get_processing_activities(self, veri_business_id: str) -> Dict[str, Any]:
        """Fetch processing activities from ROPA"""
        # TODO: Integrate with Section 6 ProcessingActivityMapper
        return {
            "total_activities": 0,
            "activities": []
        }
    
    async def _get_cross_border_transfers(self, veri_business_id: str) -> Dict[str, Any]:
        """Fetch cross-border transfers"""
        # TODO: Integrate with Section 5 CrossBorderValidator
        return {
            "total_transfers": 0,
            "transfers": []
        }
    
    async def _get_security_measures(self, veri_business_id: str) -> Dict[str, Any]:
        """Fetch security measures implementation"""
        # TODO: Implement database query
        return {
            "encryption_enabled": True,
            "access_control": True,
            "audit_logging": True
        }
    
    async def _get_dpo_information(self, veri_business_id: str) -> Dict[str, Any]:
        """Fetch DPO information"""
        # TODO: Implement database query
        return {
            "dpo_name": "Not assigned",
            "dpo_name_vi": "Chưa chỉ định",
            "contact_email": "",
            "contact_phone": ""
        }
    
    async def _count_data_fields(self, veri_business_id: str) -> int:
        """Count total data fields"""
        # TODO: Implement database query
        return 0
    
    async def _count_processing_activities(self, veri_business_id: str) -> int:
        """Count total processing activities"""
        # TODO: Implement database query
        return 0
    
    async def _count_cross_border_transfers(self, veri_business_id: str) -> int:
        """Count cross-border transfers"""
        # TODO: Implement database query
        return 0
    
    async def _calculate_overall_risk(self, veri_business_id: str) -> float:
        """Calculate overall risk score (0-10 scale)"""
        # TODO: Implement risk calculation algorithm
        return 5.0
    
    async def _get_compliance_status(self, veri_business_id: str) -> str:
        """Get overall compliance status"""
        # TODO: Implement compliance status logic
        return "compliant"
    
    async def _get_key_findings(self, veri_business_id: str) -> List[str]:
        """Get key findings (English)"""
        return ["No critical issues identified"]
    
    async def _get_key_findings_vi(self, veri_business_id: str) -> List[str]:
        """Get key findings (Vietnamese)"""
        return ["Không phát hiện vấn đề nghiêm trọng"]
    
    async def _fetch_audit_events(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]],
        filters: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Fetch audit trail events"""
        # TODO: Implement database query
        return []
    
    async def _fetch_all_data_fields(
        self,
        veri_business_id: str,
        filters: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Fetch all data fields"""
        # TODO: Implement database query
        return []
    
    async def _get_storage_locations(self, veri_business_id: str) -> List[Dict[str, Any]]:
        """Get storage locations"""
        # TODO: Implement database query
        return []
    
    async def _fetch_third_party_vendors(self, veri_business_id: str) -> List[Dict[str, Any]]:
        """Fetch third-party vendors"""
        # TODO: Implement database query
        return []
    
    async def _fetch_dsr_requests(
        self,
        veri_business_id: str,
        date_range: Optional[Dict[str, datetime]],
        filters: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Fetch DSR requests"""
        # TODO: Implement database query
        return []
    
    async def _get_cultural_context(self, veri_business_id: str) -> Dict[str, Any]:
        """Get Vietnamese cultural context"""
        if self.cultural_engine:
            # TODO: Integrate with cultural intelligence engine
            pass
        
        return {
            "region": "unknown",
            "business_style": "unknown"
        }
    
    # ========================================================================
    # CALCULATION METHODS (Scoring and metrics)
    # ========================================================================
    
    def _calculate_compliance_score(self, sections: Dict[str, Any]) -> float:
        """
        Calculate PDPL compliance score (0-100)
        
        Based on completeness of MPS report sections
        """
        total_sections = 6
        complete_sections = sum(
            1 for section in sections.values()
            if section and len(section) > 0
        )
        
        return (complete_sections / total_sections) * 100
    
    def _calculate_vendor_risk_score(
        self,
        vendor: Dict[str, Any],
        config: Dict[str, Any]
    ) -> float:
        """
        Calculate vendor risk score (0-10 scale)
        
        Uses weighted risk factors from ReportingConfig.THIRD_PARTY_DASHBOARD_CONFIG
        """
        risk_weights = config["risk_weights"]
        risk_score = 0.0
        
        # Data volume risk (0-10)
        data_volume = vendor.get("data_volume", 0)
        volume_risk = min(data_volume / 10000, 10.0)  # Scale to 10
        risk_score += volume_risk * risk_weights["data_volume"]
        
        # Cross-border risk (0 or 10)
        is_cross_border = vendor.get("is_cross_border", False)
        cross_border_risk = 10.0 if is_cross_border else 0.0
        risk_score += cross_border_risk * risk_weights["cross_border_status"]
        
        # Encryption risk (inverse: 10 if disabled, 0 if enabled)
        has_encryption = vendor.get("encryption_enabled", False)
        encryption_risk = 0.0 if has_encryption else 10.0
        risk_score += encryption_risk * risk_weights["encryption_enabled"]
        
        # SCC risk (inverse: 10 if unsigned, 0 if signed)
        has_scc = vendor.get("scc_signed", False)
        scc_risk = 0.0 if has_scc else 10.0
        risk_score += scc_risk * risk_weights["scc_signed"]
        
        # Compliance certification risk (inverse)
        has_certification = vendor.get("compliance_certification", False)
        cert_risk = 0.0 if has_certification else 10.0
        risk_score += cert_risk * risk_weights["compliance_certification"]
        
        # Data breach history risk
        breach_count = vendor.get("data_breach_count", 0)
        breach_risk = min(breach_count * 2.0, 10.0)  # 2 points per breach, max 10
        risk_score += breach_risk * risk_weights["data_breach_history"]
        
        return round(risk_score, 2)
    
    def _calculate_fulfillment_metrics(self, dsr_requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate DSR fulfillment metrics"""
        if not dsr_requests:
            return {
                "total": 0,
                "fulfilled": 0,
                "pending": 0,
                "rejected": 0,
                "fulfillment_rate": 0.0
            }
        
        total = len(dsr_requests)
        fulfilled = sum(1 for req in dsr_requests if req.get("status") == "fulfilled")
        pending = sum(1 for req in dsr_requests if req.get("status") == "pending")
        rejected = sum(1 for req in dsr_requests if req.get("status") == "rejected")
        
        return {
            "total": total,
            "fulfilled": fulfilled,
            "pending": pending,
            "rejected": rejected,
            "fulfillment_rate": (fulfilled / total) * 100 if total > 0 else 0.0
        }
    
    # ========================================================================
    # CATEGORIZATION METHODS (Grouping and organizing)
    # ========================================================================
    
    def _categorize_events(
        self,
        events: List[Dict[str, Any]],
        event_types: List[str]
    ) -> Dict[str, int]:
        """Categorize audit events by type"""
        categorized = {event_type: 0 for event_type in event_types}
        
        for event in events:
            event_type = event.get("event_type")
            if event_type in categorized:
                categorized[event_type] += 1
        
        return categorized
    
    def _group_by_category(self, data_fields: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group data fields by category"""
        grouped = {}
        
        for field in data_fields:
            category = field.get("category", "unknown")
            grouped[category] = grouped.get(category, 0) + 1
        
        return grouped
    
    def _group_by_risk_level(self, vendors: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group vendors by risk level"""
        grouped = {
            "high": [],
            "medium": [],
            "low": []
        }
        
        for vendor in vendors:
            risk_level = vendor.get("risk_level", "low")
            if risk_level in grouped:
                grouped[risk_level].append(vendor)
        
        return grouped
    
    def _categorize_dsr_requests(self, requests: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize DSR requests by type"""
        categorized = {}
        
        for request in requests:
            request_type = request.get("request_type", "unknown")
            categorized[request_type] = categorized.get(request_type, 0) + 1
        
        return categorized
    
    # ========================================================================
    # RECOMMENDATION METHODS (Actionable insights)
    # ========================================================================
    
    def _generate_recommendations(self, compliance_score: float) -> List[str]:
        """Generate recommendations (English)"""
        recommendations = []
        
        if compliance_score < 60:
            recommendations.append("Complete missing PDPL compliance sections")
            recommendations.append("Implement data protection impact assessment")
            recommendations.append("Assign Data Protection Officer")
        elif compliance_score < 80:
            recommendations.append("Enhance cross-border transfer documentation")
            recommendations.append("Update data retention policies")
        else:
            recommendations.append("Maintain current compliance standards")
            recommendations.append("Conduct regular compliance audits")
        
        return recommendations
    
    def _generate_recommendations_vi(self, compliance_score: float) -> List[str]:
        """Generate recommendations (Vietnamese)"""
        recommendations = []
        
        if compliance_score < 60:
            recommendations.append("Hoàn thiện các phần tuân thủ PDPL còn thiếu")
            recommendations.append("Thực hiện đánh giá tác động bảo vệ dữ liệu")
            recommendations.append("Chỉ định Cán bộ Bảo vệ Dữ liệu")
        elif compliance_score < 80:
            recommendations.append("Cải thiện tài liệu chuyển giao xuyên biên giới")
            recommendations.append("Cập nhật chính sách lưu giữ dữ liệu")
        else:
            recommendations.append("Duy trì các tiêu chuẩn tuân thủ hiện tại")
            recommendations.append("Tiến hành kiểm toán tuân thủ định kỳ")
        
        return recommendations
    
    def _generate_action_items(self, risk_score: float, compliance_status: str) -> List[str]:
        """Generate action items (English)"""
        items = []
        
        if risk_score >= 7.0:
            items.append("Immediate review of high-risk data processing")
            items.append("Implement additional security controls")
        
        if compliance_status != "compliant":
            items.append("Address non-compliance issues")
            items.append("Submit remediation plan to MPS")
        
        return items if items else ["Continue monitoring compliance"]
    
    def _generate_action_items_vi(self, risk_score: float, compliance_status: str) -> List[str]:
        """Generate action items (Vietnamese)"""
        items = []
        
        if risk_score >= 7.0:
            items.append("Xem xét ngay lập tức xử lý dữ liệu rủi ro cao")
            items.append("Triển khai các biện pháp kiểm soát bảo mật bổ sung")
        
        if compliance_status != "compliant":
            items.append("Giải quyết các vấn đề không tuân thủ")
            items.append("Gửi kế hoạch khắc phục cho Bộ Công an")
        
        return items if items else ["Tiếp tục giám sát tuân thủ"]
    
    # ========================================================================
    # TRANSLATION METHODS (Vietnamese bilingual support)
    # ========================================================================
    
    def _translate_output_format(self, output_format: OutputFormat) -> str:
        """Translate output format to Vietnamese"""
        translations = {
            OutputFormat.JSON: "JSON",
            OutputFormat.PDF: "PDF",
            OutputFormat.XLSX: "Excel"
        }
        return translations.get(output_format, output_format.value)
    
    def _translate_compliance_score(self, score: float) -> str:
        """Translate compliance score to Vietnamese description"""
        if score >= 80:
            return f"{score:.1f}% - Tuân thủ tốt"
        elif score >= 60:
            return f"{score:.1f}% - Tuân thủ cơ bản"
        else:
            return f"{score:.1f}% - Cần cải thiện"
    
    def _translate_compliance_status(self, status: str) -> str:
        """Translate compliance status to Vietnamese"""
        translations = {
            "compliant": "tuân thủ",
            "non_compliant": "không tuân thủ",
            "pending_review": "chờ xem xét",
            "unknown": "không rõ"
        }
        return translations.get(status, status)
    
    def _translate_events_by_type(self, events: Dict[str, int]) -> Dict[str, int]:
        """Add Vietnamese translations for event types"""
        translations = {
            "data_access": "truy cập dữ liệu",
            "data_modification": "chỉnh sửa dữ liệu",
            "data_deletion": "xóa dữ liệu",
            "export_report": "xuất báo cáo",
            "dsr_request": "yêu cầu quyền dữ liệu",
            "consent_update": "cập nhật đồng ý"
        }
        
        return {
            f"{key}_vi": translations.get(key, key)
            for key in events.keys()
        }
    
    def _translate_fields_by_category(self, fields: Dict[str, int]) -> Dict[str, str]:
        """Add Vietnamese translations for field categories"""
        # TODO: Implement category translations
        return {f"{key}_vi": key for key in fields.keys()}
    
    def _translate_storage_locations(self, locations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add Vietnamese translations for storage locations"""
        return [
            {
                **loc,
                "name_vi": ReportingConfig.translate_to_vietnamese(
                    loc.get("name", ""), "system"
                )
            }
            for loc in locations
        ]
    
    def _translate_vendors_by_risk(self, vendors: Dict[str, List[Dict[str, Any]]]) -> Dict[str, str]:
        """Add Vietnamese translations for risk level keys"""
        return {
            "high_vi": "Cao",
            "medium_vi": "Trung bình",
            "low_vi": "Thấp"
        }
    
    def _translate_requests_by_type(self, requests: Dict[str, int]) -> Dict[str, str]:
        """Add Vietnamese translations for DSR request types"""
        translations = {
            "access": "truy cập",
            "rectification": "chỉnh sửa",
            "erasure": "xóa",
            "restriction": "hạn chế",
            "portability": "di chuyển",
            "objection": "phản đối"
        }
        
        return {
            f"{key}_vi": translations.get(key, key)
            for key in requests.keys()
        }
    
    def _translate_fulfillment_metrics(self, metrics: Dict[str, Any]) -> Dict[str, str]:
        """Add Vietnamese translations for fulfillment metrics"""
        return {
            "total_vi": "Tổng cộng",
            "fulfilled_vi": "Đã hoàn thành",
            "pending_vi": "Đang chờ",
            "rejected_vi": "Đã từ chối",
            "fulfillment_rate_vi": "Tỷ lệ hoàn thành"
        }
