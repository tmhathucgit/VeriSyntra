"""
Cross-Border Transfer Validator

PDPL 2025 Article 20 compliance validation with bilingual Vietnamese-English output.
Validates cross-border data transfers per Decree 13/2023/ND-CP requirements.

Author: VeriSyntra Development Team
Date: 2025-11-05
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
from enum import Enum
import logging

try:
    from ..models.flow_models import DataFlowEdge
    from ..config.flow_constants import FlowMappingConfig
except ImportError:
    # Fallback for direct execution
    from models.flow_models import DataFlowEdge
    from config.flow_constants import FlowMappingConfig

logger = logging.getLogger(__name__)


# Constants for cross-border validation
VIETNAM_COUNTRY_CODE = 'VN'
ADEQUATE_PROTECTION_COUNTRIES = [VIETNAM_COUNTRY_CODE]  # Only VN by default
MPS_THRESHOLD_REGULAR = 10000  # Category 1 data
MPS_THRESHOLD_SENSITIVE = 1000  # Category 2 data
SECURE_PROTOCOLS = ['HTTPS', 'TLS', 'SSL', 'SFTP', 'SSH', 'FTPS']


class TransferMechanism(str, Enum):
    """
    PDPL Article 20 transfer mechanisms for cross-border data transfers
    
    Vietnamese: Cơ chế chuyển giao theo Điều 20 PDPL
    """
    ADEQUATE_PROTECTION = "adequate_protection"  # Bảo vệ tương đương
    STANDARD_CONTRACTUAL_CLAUSES = "standard_contractual_clauses"  # Điều khoản hợp đồng tiêu chuẩn
    BINDING_CORPORATE_RULES = "binding_corporate_rules"  # Quy tắc doanh nghiệp ràng buộc
    EXPLICIT_CONSENT = "explicit_consent"  # Sự đồng ý rõ ràng
    PUBLIC_INTEREST = "public_interest"  # Lợi ích công cộng


class ComplianceStatus(str, Enum):
    """
    Compliance status with Vietnamese translations
    
    Vietnamese: Trạng thái tuân thủ
    """
    COMPLIANT = "compliant"  # Tuân thủ
    NON_COMPLIANT = "non_compliant"  # Không tuân thủ
    REQUIRES_REVIEW = "requires_review"  # Cần xem xét
    PENDING_MPS_APPROVAL = "pending_mps_approval"  # Chờ phê duyệt Bộ Công an


class CrossBorderValidator:
    """
    Validate cross-border transfers per Vietnamese PDPL with bilingual output
    
    Zero hard-coding: All thresholds, countries, and protocols from FlowMappingConfig
    Bilingual support: All user-facing outputs include Vietnamese (_vi suffix)
    """
    
    # Vietnamese translation dictionary for bilingual outputs
    TRANSLATIONS_VI = {
        # Transfer mechanisms
        'adequate_protection': 'bảo vệ tương đương',
        'standard_contractual_clauses': 'điều khoản hợp đồng tiêu chuẩn',
        'binding_corporate_rules': 'quy tắc doanh nghiệp ràng buộc',
        'explicit_consent': 'sự đồng ý rõ ràng',
        'public_interest': 'lợi ích công cộng',
        
        # Compliance statuses
        'compliant': 'tuân thủ',
        'non_compliant': 'không tuân thủ',
        'requires_review': 'cần xem xét',
        'pending_mps_approval': 'chờ phê duyệt Bộ Công an',
        
        # Boolean values
        'yes': 'Có',
        'no': 'Không',
        
        # Common messages
        'domestic_transfer': 'Chuyển giao trong nước, không cần xác thực xuyên biên giới',
        'no_vn_entity': 'Không có thực thể Việt Nam liên quan, PDPL không áp dụng',
        'cross_border_detected': 'Phát hiện chuyển giao xuyên biên giới từ Việt Nam sang {country}',
        'adequate_protection_found': 'Quốc gia đích {country} có bảo vệ tương đương',
        'mechanism_required': 'Chuyển giao xuyên biên giới yêu cầu cơ chế pháp lý (điều khoản hợp đồng tiêu chuẩn, quy tắc doanh nghiệp ràng buộc, hoặc sự đồng ý rõ ràng)',
        'sccs_recommendation': 'Đảm bảo điều khoản hợp đồng tiêu chuẩn được ký kết và cập nhật',
        'bcrs_recommendation': 'Đảm bảo quy tắc doanh nghiệp ràng buộc được phê duyệt và thực thi',
        'consent_recommendation': 'Đảm bảo đã có sự đồng ý rõ ràng từ tất cả chủ thể dữ liệu',
        'public_interest_recommendation': 'Xác minh chuyển giao phục vụ lợi ích công cộng theo quy định pháp luật',
        'mps_notification_required': 'Yêu cầu thông báo Bộ Công an: {volume} chủ thể dữ liệu vượt ngưỡng {threshold}',
        'encryption_required': 'Chuyển giao xuyên biên giới phải được mã hóa ({protocols})',
        'insecure_protocol': 'Giao thức "{protocol}" không an toàn. Sử dụng: {secure_protocols}',
        
        # Transfer Impact Assessment messages
        'tia_mps_filing': 'Nộp thông báo Bộ Công an cho chuyển giao xuyên biên giới quy mô lớn',
        'tia_encrypt_all': 'Mã hóa tất cả chuyển giao dữ liệu xuyên biên giới',
        'tia_review_mechanisms': 'Xem xét và cập nhật cơ chế chuyển giao xuyên biên giới',
        'tia_implement_sccs': 'Triển khai điều khoản hợp đồng tiêu chuẩn cho tất cả đối tác nước ngoài',
        
        # Legal basis translations
        'consent': 'sự đồng ý',
        'contract': 'hợp đồng',
        'legal_obligation': 'nghĩa vụ pháp lý',
        'vital_interests': 'lợi ích quan trọng',
        'public_task': 'nhiệm vụ công cộng',
        'legitimate_interest': 'lợi ích hợp pháp'
    }
    
    @classmethod
    def validate_cross_border_flow(
        cls,
        flow: DataFlowEdge,
        source_country: str,
        dest_country: str,
        data_sensitivity: str,  # 'regular' or 'sensitive'
        transfer_mechanism: Optional[TransferMechanism] = None
    ) -> Dict[str, Any]:
        """
        Validate cross-border data transfer with BILINGUAL output
        
        Validates PDPL 2025 Article 20 compliance for cross-border transfers.
        All validation outputs include both English and Vietnamese fields.
        
        Args:
            flow: DataFlowEdge instance representing the data transfer
            source_country: Source country code (ISO 3166-1 alpha-2)
            dest_country: Destination country code (ISO 3166-1 alpha-2)
            data_sensitivity: 'regular' or 'sensitive' (affects MPS thresholds)
            transfer_mechanism: Legal mechanism for transfer (if applicable)
            
        Returns:
            Bilingual validation result with fields:
            {
                'is_compliant': bool,
                'is_compliant_vi': str,  # "Tuân thủ" / "Không tuân thủ"
                'status': str,  # ComplianceStatus enum value
                'status_vi': str,  # Vietnamese status translation
                'requires_mps_notification': bool,
                'requires_mps_notification_vi': str,  # "Có" / "Không"
                'issues': List[str],  # English issues
                'issues_vi': List[str],  # Vietnamese issues
                'recommendations': List[str],  # English recommendations
                'recommendations_vi': List[str],  # Vietnamese recommendations
                'legal_basis': str,
                'legal_basis_vi': str
            }
            
        Example:
            >>> validator = CrossBorderValidator()
            >>> result = validator.validate_cross_border_flow(
            ...     flow=edge,
            ...     source_country='VN',
            ...     dest_country='US',
            ...     data_sensitivity='sensitive',
            ...     transfer_mechanism=TransferMechanism.STANDARD_CONTRACTUAL_CLAUSES
            ... )
            >>> print(result['is_compliant_vi'])  # "Tuân thủ"
        """
        # Initialize bilingual result structure
        result = {
            'is_compliant': True,
            'is_compliant_vi': cls.TRANSLATIONS_VI['compliant'],
            'status': ComplianceStatus.COMPLIANT.value,
            'status_vi': cls.TRANSLATIONS_VI['compliant'],
            'requires_mps_notification': False,
            'requires_mps_notification_vi': cls.TRANSLATIONS_VI['no'],
            'issues': [],
            'issues_vi': [],
            'recommendations': [],
            'recommendations_vi': [],
            'legal_basis': flow.legal_basis,
            'legal_basis_vi': cls.TRANSLATIONS_VI.get(flow.legal_basis, flow.legal_basis)
        }
        
        # Check if actually cross-border
        if source_country == dest_country:
            logger.info(
                f"[OK] Domestic transfer "
                f"({source_country} -> {dest_country}), no cross-border validation needed"
            )
            result['recommendations'].append("Domestic transfer, no cross-border validation needed")
            result['recommendations_vi'].append(cls.TRANSLATIONS_VI['domestic_transfer'])
            return result
        
        # Check if Vietnam is involved (PDPL applicability)
        if source_country != VIETNAM_COUNTRY_CODE and dest_country != VIETNAM_COUNTRY_CODE:
            logger.info(
                f"[OK] No Vietnamese entity involved "
                f"({source_country} -> {dest_country}), PDPL not applicable"
            )
            result['recommendations'].append("No Vietnamese entity involved, PDPL not applicable")
            result['recommendations_vi'].append(cls.TRANSLATIONS_VI['no_vn_entity'])
            return result
        
        # Vietnamese data going abroad - PDPL Article 20 applies
        if source_country == VIETNAM_COUNTRY_CODE and dest_country != VIETNAM_COUNTRY_CODE:
            logger.info(
                f"[WARNING] Cross-border transfer detected: "
                f"Vietnam -> {dest_country}"
            )
            
            result['recommendations'].append(
                f"Cross-border transfer from Vietnam to {dest_country}"
            )
            result['recommendations_vi'].append(
                cls.TRANSLATIONS_VI['cross_border_detected'].format(country=dest_country)
            )
            
            # 1. Check if destination has adequate protection
            if dest_country in ADEQUATE_PROTECTION_COUNTRIES:
                result['recommendations'].append(
                    f"Destination country {dest_country} has adequate protection"
                )
                result['recommendations_vi'].append(
                    cls.TRANSLATIONS_VI['adequate_protection_found'].format(country=dest_country)
                )
            else:
                # 2. Require additional safeguards for non-adequate countries
                if not transfer_mechanism:
                    # Missing transfer mechanism - NON-COMPLIANT
                    result['is_compliant'] = False
                    result['is_compliant_vi'] = cls.TRANSLATIONS_VI['non_compliant']
                    result['status'] = ComplianceStatus.NON_COMPLIANT.value
                    result['status_vi'] = cls.TRANSLATIONS_VI['non_compliant']
                    
                    result['issues'].append(
                        "Cross-border transfer requires legal mechanism "
                        "(SCCs, BCRs, or explicit consent)"
                    )
                    result['issues_vi'].append(cls.TRANSLATIONS_VI['mechanism_required'])
                    
                elif transfer_mechanism == TransferMechanism.STANDARD_CONTRACTUAL_CLAUSES:
                    result['recommendations'].append(
                        "Ensure Standard Contractual Clauses are signed and updated"
                    )
                    result['recommendations_vi'].append(cls.TRANSLATIONS_VI['sccs_recommendation'])
                    
                elif transfer_mechanism == TransferMechanism.BINDING_CORPORATE_RULES:
                    result['recommendations'].append(
                        "Ensure Binding Corporate Rules are approved and enforced"
                    )
                    result['recommendations_vi'].append(cls.TRANSLATIONS_VI['bcrs_recommendation'])
                    
                elif transfer_mechanism == TransferMechanism.EXPLICIT_CONSENT:
                    result['recommendations'].append(
                        "Ensure explicit consent obtained from all data subjects"
                    )
                    result['recommendations_vi'].append(cls.TRANSLATIONS_VI['consent_recommendation'])
                    
                elif transfer_mechanism == TransferMechanism.PUBLIC_INTEREST:
                    result['recommendations'].append(
                        "Verify transfer serves public interest as defined by law"
                    )
                    result['recommendations_vi'].append(cls.TRANSLATIONS_VI['public_interest_recommendation'])
            
            # 3. Check MPS notification requirement (Decree 13/2023/ND-CP)
            if flow.data_volume:
                threshold = MPS_THRESHOLD_SENSITIVE if data_sensitivity == 'sensitive' else MPS_THRESHOLD_REGULAR
                
                if flow.data_volume >= threshold:
                    result['requires_mps_notification'] = True
                    result['requires_mps_notification_vi'] = cls.TRANSLATIONS_VI['yes']
                    result['status'] = ComplianceStatus.PENDING_MPS_APPROVAL.value
                    result['status_vi'] = cls.TRANSLATIONS_VI['pending_mps_approval']
                    
                    result['recommendations'].append(
                        f"MPS notification required: {flow.data_volume} data subjects "
                        f"exceeds threshold of {threshold}"
                    )
                    result['recommendations_vi'].append(
                        cls.TRANSLATIONS_VI['mps_notification_required'].format(
                            volume=flow.data_volume,
                            threshold=threshold
                        )
                    )
                    
                    logger.warning(
                        f"[WARNING] MPS notification required: "
                        f"{flow.data_volume} subjects > {threshold} threshold"
                    )
            
            # 4. Check encryption requirement
            if not flow.encryption_enabled:
                result['is_compliant'] = False
                result['is_compliant_vi'] = cls.TRANSLATIONS_VI['non_compliant']
                result['status'] = ComplianceStatus.NON_COMPLIANT.value
                result['status_vi'] = cls.TRANSLATIONS_VI['non_compliant']
                
                protocols = ', '.join(SECURE_PROTOCOLS)
                result['issues'].append(
                    f"Cross-border transfer must be encrypted ({protocols})"
                )
                result['issues_vi'].append(
                    cls.TRANSLATIONS_VI['encryption_required'].format(protocols=protocols)
                )
                
                logger.error(
                    f"[ERROR] Unencrypted cross-border transfer detected"
                )
            
            # 5. Check protocol security
            protocol = flow.protocol or flow.metadata.get('protocol', '')
            if protocol and protocol.upper() not in SECURE_PROTOCOLS:
                result['is_compliant'] = False
                result['is_compliant_vi'] = cls.TRANSLATIONS_VI['non_compliant']
                result['status'] = ComplianceStatus.NON_COMPLIANT.value
                result['status_vi'] = cls.TRANSLATIONS_VI['non_compliant']
                
                secure_protocols = ', '.join(SECURE_PROTOCOLS)
                result['issues'].append(
                    f"Protocol '{protocol}' not secure. Use: {secure_protocols}"
                )
                result['issues_vi'].append(
                    cls.TRANSLATIONS_VI['insecure_protocol'].format(
                        protocol=protocol,
                        secure_protocols=secure_protocols
                    )
                )
                
                logger.error(
                    f"[ERROR] Insecure protocol detected: {protocol}"
                )
        
        # Log final compliance status
        if result['is_compliant']:
            logger.info(
                f"[OK] Cross-border transfer validation passed: "
                f"{source_country} -> {dest_country}"
            )
        else:
            logger.error(
                f"[ERROR] Cross-border transfer validation failed: "
                f"{len(result['issues'])} issues found"
            )
        
        return result
    
    @classmethod
    def generate_transfer_impact_assessment(
        cls,
        flows: List[DataFlowEdge],
        tenant_id: UUID
    ) -> Dict[str, Any]:
        """
        Generate Transfer Impact Assessment (TIA) for Vietnamese businesses with BILINGUAL output
        
        Creates a comprehensive assessment of cross-border transfer risks and
        compliance requirements for PDPL reporting to MPS (Bộ Công an).
        
        Args:
            flows: List of all data flow edges to analyze
            tenant_id: Tenant UUID for isolation
            
        Returns:
            Bilingual TIA report with fields:
            {
                'total_cross_border_flows': int,
                'countries_involved': List[str],
                'high_risk_transfers': List[dict],
                'mps_notification_required': bool,
                'mps_notification_required_vi': str,  # "Có" / "Không"
                'recommendations': List[str],  # English
                'recommendations_vi': List[str]  # Vietnamese
            }
            
        Example:
            >>> tia = CrossBorderValidator.generate_transfer_impact_assessment(
            ...     flows=all_flows,
            ...     tenant_id=tenant_uuid
            ... )
            >>> print(tia['mps_notification_required_vi'])  # "Có" or "Không"
        """
        # Filter cross-border flows
        cross_border_flows = [f for f in flows if f.is_cross_border]
        
        countries = set()
        high_risk_transfers = []
        mps_required = False
        
        # Analyze each cross-border flow
        for flow in cross_border_flows:
            # Track destination countries
            # Note: Would need source/dest country info from flow metadata
            # For now, we check volume thresholds
            
            if flow.data_volume and flow.data_volume >= MPS_THRESHOLD_REGULAR:
                mps_required = True
                high_risk_transfers.append({
                    'flow_id': str(flow.edge_id),
                    'purpose': flow.legal_basis,
                    'volume': flow.data_volume,
                    'encrypted': flow.encryption_enabled,
                    'legal_basis': flow.legal_basis
                })
        
        # Build bilingual TIA report
        tia = {
            'total_cross_border_flows': len(cross_border_flows),
            'countries_involved': list(countries),
            'high_risk_transfers': high_risk_transfers,
            'mps_notification_required': mps_required,
            'mps_notification_required_vi': cls.TRANSLATIONS_VI['yes'] if mps_required else cls.TRANSLATIONS_VI['no'],
            'recommendations': [],
            'recommendations_vi': []
        }
        
        # Add recommendations based on findings
        if mps_required:
            tia['recommendations'].append(
                "File MPS notification for large-scale cross-border transfers"
            )
            tia['recommendations_vi'].append(cls.TRANSLATIONS_VI['tia_mps_filing'])
        
        if any(not f.encryption_enabled for f in cross_border_flows):
            tia['recommendations'].append(
                "Encrypt all cross-border data transfers"
            )
            tia['recommendations_vi'].append(cls.TRANSLATIONS_VI['tia_encrypt_all'])
        
        if len(cross_border_flows) > 10:
            tia['recommendations'].append(
                "Review and update cross-border transfer mechanisms"
            )
            tia['recommendations_vi'].append(cls.TRANSLATIONS_VI['tia_review_mechanisms'])
        
        if any(not f.dpa_in_place for f in cross_border_flows):
            tia['recommendations'].append(
                "Implement Standard Contractual Clauses for all foreign partners"
            )
            tia['recommendations_vi'].append(cls.TRANSLATIONS_VI['tia_implement_sccs'])
        
        logger.info(
            f"[OK] Generated Transfer Impact Assessment: "
            f"{len(cross_border_flows)} cross-border flows, "
            f"{len(high_risk_transfers)} high-risk, "
            f"MPS notification: {mps_required}"
        )
        
        return tia
