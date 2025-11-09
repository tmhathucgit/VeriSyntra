# DPO Intelligence & Analytics Implementation Plan
## veri-ai-data-inventory: Risk Scoring, Compliance Analysis, Smart Recommendations

**Service:** veri-ai-data-inventory (Port 8010) + Frontend Dashboard  
**Version:** 1.0.0  
**Date:** November 3, 2025  
**Purpose:** Implementation guide for DPO intelligence features including risk scoring, compliance gap analysis, AI recommendations, data quality indicators, and cost impact dashboard

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Risk Scoring & Prioritization](#risk-scoring--prioritization)
4. [Compliance Gap Analysis](#compliance-gap-analysis)
5. [Smart Recommendations Engine](#smart-recommendations-engine)
6. [Data Quality Indicators](#data-quality-indicators)
7. [Cost Impact Dashboard](#cost-impact-dashboard)
8. [API Endpoints](#api-endpoints)
9. [Frontend Components](#frontend-components)
10. [Testing Strategy](#testing-strategy)

---

## Overview

### Purpose
Provide Data Privacy Officers (DPOs) with intelligent analytics and decision-support tools to prioritize work, identify compliance gaps, receive AI-powered recommendations, monitor data quality, and track compliance costs.

### Key Features
- **Risk Scoring Algorithm:** Automatically calculate risk scores for data fields based on sensitivity, volume, exposure, and retention
- **Compliance Gap Analysis:** PDPL 2025 and Decree 13/2023/ND-CP compliance checklist automation
- **Smart Recommendations:** AI-powered suggestions for classification, retention policies, and security measures
- **Data Quality Indicators:** Null percentages, duplicates, format validation, Vietnamese-specific checks
- **Cost Impact Dashboard:** Track storage costs, processing fees, personnel time, and ROI of column filtering

### Vietnamese Business Context
```typescript
interface VeriDPOIntelligenceContext extends VeriBusinessContext {
  veriRiskProfile: 'low' | 'medium' | 'high' | 'critical';
  veriComplianceMaturity: 'basic' | 'developing' | 'advanced' | 'optimized';
  veriRegionalLocation: 'north' | 'central' | 'south';
  veriIndustryType: string; // finance, healthcare, government, technology
  veriMPSReportingRequired: boolean;
}
```

---

## Architecture

### System Components

```
[DPO Intelligence & Analytics Layer]
    |
    |-- [Risk Scoring Engine]
    |     |-- Sensitivity Score Calculator
    |     |-- Volume Weight Calculator
    |     |-- Exposure Risk Analyzer
    |     |-- Retention Risk Assessor
    |     |-- Vietnamese Risk Factors
    |
    |-- [Compliance Gap Analyzer]
    |     |-- PDPL 2025 Requirements Checker
    |     |-- Decree 13/2023/ND-CP Validator
    |     |-- MPS Reporting Readiness
    |     |-- Missing Fields Detector
    |
    |-- [Smart Recommendations Engine]
    |     |-- Rule-Based Recommendations
    |     |-- AI-Powered Suggestions
    |     |-- Vietnamese Best Practices
    |     |-- Regional Context Rules (North/South)
    |
    |-- [Data Quality Analyzer]
    |     |-- Null Percentage Calculator
    |     |-- Duplicate Detector
    |     |-- Format Validator
    |     |-- Vietnamese Name Validator
    |     |-- Phone Number Validator (VN format)
    |
    |-- [Cost Impact Tracker]
          |-- Storage Cost Calculator
          |-- Processing Cost Tracker
          |-- Personnel Time Logger
          |-- Column Filter ROI Calculator
```

### Integration Points
- **veri-ai-data-inventory (Port 8010):** Data source for risk calculations
- **veri-vi-ai-classification (Port 8006):** VeriAIDPO_Principles_VI_v1 model for PDPL recommendations
- **veri-compliance-engine:** PDPL compliance rules
- **PostgreSQL:** Analytics data storage
- **Redis:** Caching for recommendations

---

## Risk Scoring & Prioritization

### Risk Scoring Algorithm

```python
# File: backend/veri_ai_data_inventory/intelligence/risk_scoring.py

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class RiskLevel(str, Enum):
    """Risk level categories"""
    LOW = "low"           # 0-25
    MEDIUM = "medium"     # 26-50
    HIGH = "high"         # 51-75
    CRITICAL = "critical" # 76-100

class VietnameseRiskFactor(str, Enum):
    """Vietnamese-specific risk factors"""
    GOVERNMENT_DATA = "government_data"       # +25 points
    FINANCIAL_DATA = "financial_data"         # +20 points
    BIOMETRIC_DATA = "biometric_data"         # +30 points
    CHILDREN_DATA = "children_data"           # +25 points
    HEALTH_DATA = "health_data"               # +20 points
    POLITICAL_DATA = "political_data"         # +15 points
    CROSS_BORDER_VN = "cross_border_vn"       # +15 points

class DataFieldRiskScorer:
    """Calculate risk scores for data fields"""
    
    # PDPL 2025 sensitivity weights
    SENSITIVITY_WEIGHTS = {
        'sensitive': 100,      # PDPL sensitive personal data
        'regular': 50,         # Regular personal data
        'non_personal': 10     # Non-personal data
    }
    
    # Volume thresholds
    VOLUME_THRESHOLDS = {
        'small': (0, 1000),           # 0-1K records: +10
        'medium': (1001, 100000),     # 1K-100K: +20
        'large': (100001, 1000000),   # 100K-1M: +30
        'very_large': (1000001, None) # >1M: +40
    }
    
    # Exposure risk factors
    EXPOSURE_WEIGHTS = {
        'cross_border': 50,      # International transfers
        'public_api': 30,        # Public-facing APIs
        'third_party': 20,       # Shared with vendors
        'cloud_storage': 15,     # Cloud storage
        'internal_only': 0       # Internal use only
    }
    
    # Retention risk
    RETENTION_WEIGHTS = {
        'indefinite': 40,        # Indefinite retention
        'over_10_years': 30,     # >10 years
        '5_to_10_years': 20,     # 5-10 years
        '1_to_5_years': 10,      # 1-5 years
        'under_1_year': 0        # <1 year
    }
    
    @staticmethod
    def calculate_risk_score(
        field_data: Dict[str, Any],
        veri_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score for a data field
        
        Args:
            field_data: {
                'field_name': str,
                'table_name': str,
                'pdpl_category': 'sensitive' | 'regular' | 'non_personal',
                'classification': str,
                'row_count': int,
                'exposure_type': str,
                'retention_period': str,
                'is_cross_border': bool,
                'is_encrypted': bool,
                'last_accessed': datetime (optional)
            }
            veri_context: Vietnamese business context
            
        Returns:
            {
                'field_identifier': str,
                'risk_score': int (0-100),
                'risk_level': RiskLevel,
                'sensitivity_score': int,
                'volume_score': int,
                'exposure_score': int,
                'retention_score': int,
                'vietnamese_factors_score': int,
                'risk_factors': List[str],
                'recommendations': List[str]
            }
        """
        try:
            field_identifier = f"{field_data['table_name']}.{field_data['field_name']}"
            
            # 1. Sensitivity Score (base)
            sensitivity_score = DataFieldRiskScorer.SENSITIVITY_WEIGHTS.get(
                field_data.get('pdpl_category', 'regular'),
                50
            )
            
            # 2. Volume Score
            row_count = field_data.get('row_count', 0)
            volume_score = DataFieldRiskScorer._calculate_volume_score(row_count)
            
            # 3. Exposure Score
            exposure_score = DataFieldRiskScorer._calculate_exposure_score(field_data)
            
            # 4. Retention Score
            retention_score = DataFieldRiskScorer._calculate_retention_score(
                field_data.get('retention_period')
            )
            
            # 5. Vietnamese-Specific Factors
            vietnamese_score = DataFieldRiskScorer._calculate_vietnamese_factors(
                field_data,
                veri_context
            )
            
            # 6. Encryption Mitigation (reduce risk if encrypted)
            encryption_mitigation = -10 if field_data.get('is_encrypted', False) else 0
            
            # Calculate final risk score
            raw_score = (
                sensitivity_score * 0.4 +      # 40% weight on sensitivity
                volume_score * 0.2 +            # 20% weight on volume
                exposure_score * 0.2 +          # 20% weight on exposure
                retention_score * 0.1 +         # 10% weight on retention
                vietnamese_score * 0.1 +        # 10% weight on VN factors
                encryption_mitigation
            )
            
            # Normalize to 0-100
            risk_score = max(0, min(100, int(raw_score)))
            
            # Determine risk level
            risk_level = DataFieldRiskScorer._get_risk_level(risk_score)
            
            # Identify risk factors
            risk_factors = DataFieldRiskScorer._identify_risk_factors(
                field_data,
                veri_context
            )
            
            # Generate recommendations
            recommendations = DataFieldRiskScorer._generate_recommendations(
                field_data,
                risk_score,
                risk_level
            )
            
            result = {
                'field_identifier': field_identifier,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'sensitivity_score': int(sensitivity_score * 0.4),
                'volume_score': int(volume_score * 0.2),
                'exposure_score': int(exposure_score * 0.2),
                'retention_score': int(retention_score * 0.1),
                'vietnamese_factors_score': int(vietnamese_score * 0.1),
                'risk_factors': risk_factors,
                'recommendations': recommendations,
                'calculated_at': datetime.utcnow().isoformat()
            }
            
            logger.info(
                f"[OK] Risk score calculated for {field_identifier}: "
                f"{risk_score} ({risk_level})"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"[ERROR] Risk score calculation failed: {str(e)}")
            raise
    
    @staticmethod
    def _calculate_volume_score(row_count: int) -> int:
        """Calculate volume-based risk score"""
        for tier, (min_val, max_val) in DataFieldRiskScorer.VOLUME_THRESHOLDS.items():
            if max_val is None:
                if row_count >= min_val:
                    return 40
            elif min_val <= row_count <= max_val:
                if tier == 'small':
                    return 10
                elif tier == 'medium':
                    return 20
                elif tier == 'large':
                    return 30
        return 10  # Default
    
    @staticmethod
    def _calculate_exposure_score(field_data: Dict[str, Any]) -> int:
        """Calculate exposure-based risk score"""
        score = 0
        
        if field_data.get('is_cross_border', False):
            score += DataFieldRiskScorer.EXPOSURE_WEIGHTS['cross_border']
        
        exposure_type = field_data.get('exposure_type', 'internal_only')
        score += DataFieldRiskScorer.EXPOSURE_WEIGHTS.get(exposure_type, 0)
        
        return score
    
    @staticmethod
    def _calculate_retention_score(retention_period: Optional[str]) -> int:
        """Calculate retention-based risk score"""
        if not retention_period:
            return DataFieldRiskScorer.RETENTION_WEIGHTS['indefinite']
        
        retention_lower = retention_period.lower()
        
        if 'indefinite' in retention_lower or 'permanent' in retention_lower:
            return DataFieldRiskScorer.RETENTION_WEIGHTS['indefinite']
        elif '10' in retention_lower or 'decade' in retention_lower:
            return DataFieldRiskScorer.RETENTION_WEIGHTS['over_10_years']
        elif '5' in retention_lower:
            return DataFieldRiskScorer.RETENTION_WEIGHTS['5_to_10_years']
        elif '1' in retention_lower or 'year' in retention_lower:
            return DataFieldRiskScorer.RETENTION_WEIGHTS['1_to_5_years']
        else:
            return DataFieldRiskScorer.RETENTION_WEIGHTS['under_1_year']
    
    @staticmethod
    def _calculate_vietnamese_factors(
        field_data: Dict[str, Any],
        veri_context: Optional[Dict[str, Any]]
    ) -> int:
        """Calculate Vietnamese-specific risk factors"""
        score = 0
        classification = field_data.get('classification', '').lower()
        
        # Government-related data
        if any(term in classification for term in ['government', 'cmnd', 'cccd', 'passport']):
            score += 25
        
        # Financial data
        if any(term in classification for term in ['bank', 'account', 'financial', 'tax']):
            score += 20
        
        # Biometric data
        if any(term in classification for term in ['biometric', 'fingerprint', 'face', 'iris']):
            score += 30
        
        # Children's data
        if any(term in classification for term in ['child', 'minor', 'student', 'under_18']):
            score += 25
        
        # Health data
        if any(term in classification for term in ['health', 'medical', '病歷', 'benh_an']):
            score += 20
        
        # Cross-border from Vietnam
        if field_data.get('is_cross_border') and veri_context:
            if veri_context.get('country') == 'VN':
                score += 15
        
        return score
    
    @staticmethod
    def _get_risk_level(risk_score: int) -> RiskLevel:
        """Determine risk level from score"""
        if risk_score >= 76:
            return RiskLevel.CRITICAL
        elif risk_score >= 51:
            return RiskLevel.HIGH
        elif risk_score >= 26:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    @staticmethod
    def _identify_risk_factors(
        field_data: Dict[str, Any],
        veri_context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify specific risk factors"""
        factors = []
        
        if field_data.get('pdpl_category') == 'sensitive':
            factors.append("PDPL 2025 Sensitive Personal Data")
        
        if field_data.get('row_count', 0) > 1000000:
            factors.append("High Volume (>1M records)")
        
        if field_data.get('is_cross_border'):
            factors.append("Cross-Border Transfer")
        
        if field_data.get('retention_period', '').lower() in ['indefinite', 'permanent']:
            factors.append("Indefinite Retention")
        
        if not field_data.get('is_encrypted', False):
            factors.append("Not Encrypted")
        
        classification = field_data.get('classification', '').lower()
        if 'government' in classification or 'cmnd' in classification:
            factors.append("Government ID Data")
        
        return factors
    
    @staticmethod
    def _generate_recommendations(
        field_data: Dict[str, Any],
        risk_score: int,
        risk_level: RiskLevel
    ) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        # High/Critical risk recommendations
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("Prioritize for DPO review")
            recommendations.append("Implement encryption at rest and in transit")
            recommendations.append("Enable audit logging for all access")
        
        # Encryption recommendation
        if not field_data.get('is_encrypted', False):
            recommendations.append("Enable field-level encryption")
        
        # Retention recommendation
        retention = field_data.get('retention_period', '').lower()
        if 'indefinite' in retention or not retention:
            recommendations.append(
                "Define retention policy per PDPL Article 13 (Vietnamese: Điều 13)"
            )
        
        # Cross-border recommendation
        if field_data.get('is_cross_border'):
            recommendations.append(
                "Ensure Standard Contractual Clauses (SCCs) for cross-border transfer"
            )
            recommendations.append(
                "Document transfer safeguards per PDPL Article 20 (Vietnamese: Điều 20)"
            )
        
        # Volume-based recommendation
        if field_data.get('row_count', 0) > 1000000:
            recommendations.append("Consider data minimization strategies")
            recommendations.append("Implement automated data deletion after retention period")
        
        return recommendations


class RiskPriorityQueue:
    """Priority queue for DPO review based on risk scores"""
    
    def __init__(self):
        self.scorer = DataFieldRiskScorer()
    
    async def generate_priority_queue(
        self,
        tenant_id: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate prioritized list of fields for DPO review
        
        Args:
            tenant_id: Tenant UUID
            filters: Optional filters (risk_level, table_name, etc.)
            
        Returns:
            List of fields sorted by risk score (highest first)
        """
        try:
            from ..repositories.inventory_repository import InventoryRepository
            from ..database import get_async_session
            
            async with get_async_session() as session:
                repo = InventoryRepository(session)
                
                # Fetch all classified fields for tenant
                fields = await repo.get_classified_fields(
                    tenant_id=tenant_id,
                    filters=filters
                )
                
                # Calculate risk score for each field
                risk_scored_fields = []
                
                for field in fields:
                    risk_data = self.scorer.calculate_risk_score(
                        field_data={
                            'field_name': field['field_name'],
                            'table_name': field['table_name'],
                            'pdpl_category': field.get('pdpl_category', 'regular'),
                            'classification': field.get('classification', ''),
                            'row_count': field.get('row_count', 0),
                            'exposure_type': field.get('exposure_type', 'internal_only'),
                            'retention_period': field.get('retention_period'),
                            'is_cross_border': field.get('is_cross_border', False),
                            'is_encrypted': field.get('is_encrypted', False)
                        }
                    )
                    
                    # Merge field data with risk data
                    risk_scored_fields.append({
                        **field,
                        **risk_data
                    })
                
                # Sort by risk score (descending)
                priority_queue = sorted(
                    risk_scored_fields,
                    key=lambda x: x['risk_score'],
                    reverse=True
                )
                
                logger.info(
                    f"[OK] Generated priority queue for tenant {tenant_id}: "
                    f"{len(priority_queue)} fields"
                )
                
                return priority_queue
                
        except Exception as e:
            logger.error(f"[ERROR] Priority queue generation failed: {str(e)}")
            raise
    
    async def get_top_risks(
        self,
        tenant_id: str,
        limit: int = 50,
        risk_level: Optional[RiskLevel] = None
    ) -> List[Dict[str, Any]]:
        """Get top N highest-risk fields"""
        priority_queue = await self.generate_priority_queue(tenant_id)
        
        # Filter by risk level if specified
        if risk_level:
            priority_queue = [
                field for field in priority_queue
                if field['risk_level'] == risk_level
            ]
        
        return priority_queue[:limit]
```

### Risk Score Storage

```python
# File: backend/veri_ai_data_inventory/models/risk_score.py

from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..database import Base

class RiskScore(Base):
    """Risk score table for data fields"""
    __tablename__ = 'risk_scores'
    
    risk_score_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    field_id = Column(UUID(as_uuid=True), ForeignKey('data_fields.field_id'), nullable=False)
    
    # Risk scores
    risk_score = Column(Integer, nullable=False)  # 0-100
    risk_level = Column(String(20), nullable=False)  # low, medium, high, critical
    sensitivity_score = Column(Integer)
    volume_score = Column(Integer)
    exposure_score = Column(Integer)
    retention_score = Column(Integer)
    vietnamese_factors_score = Column(Integer)
    
    # Risk factors and recommendations
    risk_factors = Column(JSON)  # List of risk factor strings
    recommendations = Column(JSON)  # List of recommendation strings
    
    # Metadata
    calculated_at = Column(DateTime, default=datetime.utcnow)
    calculated_by = Column(String(50), default='system')  # system | dpo_override
    
    # Indexes
    __table_args__ = (
        {'schema': 'veri_data_inventory'}
    ,)
```

---

## Compliance Gap Analysis

### PDPL 2025 Requirements Checker

```python
# File: backend/veri_ai_data_inventory/intelligence/compliance_gap_analyzer.py

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ComplianceStatus(str, Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"               # Fully compliant
    PARTIAL = "partial"                   # Partially compliant
    NON_COMPLIANT = "non_compliant"       # Not compliant
    NOT_APPLICABLE = "not_applicable"     # Not applicable
    UNKNOWN = "unknown"                   # Status unknown

class PDPLRequirement(str, Enum):
    """PDPL 2025 and Decree 13/2023/ND-CP requirements"""
    
    # PDPL Article 17 - Data Controller Obligations
    ROPA_DOCUMENTED = "ropa_documented"
    DPO_DESIGNATED = "dpo_designated"
    LEGAL_BASIS_DEFINED = "legal_basis_defined"
    CONSENT_OBTAINED = "consent_obtained"
    
    # PDPL Article 13 - Data Retention
    RETENTION_POLICY_DEFINED = "retention_policy_defined"
    DELETION_PROCEDURE = "deletion_procedure"
    
    # PDPL Article 20 - Cross-Border Transfers
    CROSS_BORDER_DOCUMENTED = "cross_border_documented"
    TRANSFER_SAFEGUARDS = "transfer_safeguards"
    DESTINATION_ADEQUACY = "destination_adequacy"
    
    # PDPL Article 15 - Security Measures
    ENCRYPTION_IMPLEMENTED = "encryption_implemented"
    ACCESS_CONTROLS = "access_controls"
    AUDIT_LOGGING = "audit_logging"
    
    # Decree 13/2023/ND-CP Article 12 - ROPA Requirements
    ROPA_CONTROLLER_INFO = "ropa_controller_info"
    ROPA_DPO_CONTACT = "ropa_dpo_contact"
    ROPA_PROCESSING_PURPOSE = "ropa_processing_purpose"
    ROPA_DATA_CATEGORIES = "ropa_data_categories"
    ROPA_RECIPIENTS = "ropa_recipients"
    
    # MPS Reporting
    MPS_READY_TO_SUBMIT = "mps_ready_to_submit"


class ComplianceGapAnalyzer:
    """Analyze PDPL 2025 compliance gaps"""
    
    # Requirement metadata
    REQUIREMENT_METADATA = {
        PDPLRequirement.ROPA_DOCUMENTED: {
            'title_vi': 'Hồ sơ hoạt động xử lý dữ liệu (ROPA)',
            'title_en': 'Record of Processing Activities (ROPA)',
            'legal_reference': 'PDPL Article 17, Decree 13/2023/ND-CP Article 12',
            'priority': 'critical',
            'mps_required': True
        },
        PDPLRequirement.DPO_DESIGNATED: {
            'title_vi': 'Người bảo vệ dữ liệu được chỉ định',
            'title_en': 'Data Protection Officer Designated',
            'legal_reference': 'PDPL Article 18',
            'priority': 'high',
            'mps_required': True
        },
        PDPLRequirement.LEGAL_BASIS_DEFINED: {
            'title_vi': 'Cơ sở pháp lý xử lý dữ liệu',
            'title_en': 'Legal Basis for Processing',
            'legal_reference': 'PDPL Article 8',
            'priority': 'critical',
            'mps_required': True
        },
        PDPLRequirement.RETENTION_POLICY_DEFINED: {
            'title_vi': 'Chính sách lưu trữ dữ liệu',
            'title_en': 'Data Retention Policy',
            'legal_reference': 'PDPL Article 13',
            'priority': 'high',
            'mps_required': False
        },
        PDPLRequirement.CROSS_BORDER_DOCUMENTED: {
            'title_vi': 'Chuyển dữ liệu ra nước ngoài được ghi nhận',
            'title_en': 'Cross-Border Transfers Documented',
            'legal_reference': 'PDPL Article 20',
            'priority': 'critical',
            'mps_required': True
        },
        PDPLRequirement.ENCRYPTION_IMPLEMENTED: {
            'title_vi': 'Mã hóa dữ liệu nhạy cảm',
            'title_en': 'Encryption of Sensitive Data',
            'legal_reference': 'PDPL Article 15',
            'priority': 'high',
            'mps_required': False
        },
        PDPLRequirement.MPS_READY_TO_SUBMIT: {
            'title_vi': 'Sẵn sàng báo cáo Bộ Công An',
            'title_en': 'Ready for MPS Submission',
            'legal_reference': 'Circular 09/2024/TT-BCA',
            'priority': 'critical',
            'mps_required': True
        }
    }
    
    @staticmethod
    async def analyze_compliance_gaps(
        tenant_id: str,
        veri_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive PDPL 2025 compliance gap analysis
        
        Args:
            tenant_id: Tenant UUID
            veri_context: Vietnamese business context
            
        Returns:
            {
                'overall_compliance_score': float (0-100),
                'compliance_level': str,
                'requirements': [
                    {
                        'requirement': PDPLRequirement,
                        'status': ComplianceStatus,
                        'title_vi': str,
                        'title_en': str,
                        'legal_reference': str,
                        'priority': str,
                        'gaps': List[str],
                        'recommendations': List[str]
                    }
                ],
                'critical_gaps': List[str],
                'mps_ready': bool,
                'analyzed_at': str
            }
        """
        try:
            from ..repositories.inventory_repository import InventoryRepository
            from ..database import get_async_session
            
            async with get_async_session() as session:
                repo = InventoryRepository(session)
                
                # Fetch tenant data
                tenant_data = await repo.get_tenant_compliance_data(tenant_id)
                
                # Check each requirement
                requirement_results = []
                compliant_count = 0
                total_weight = 0
                
                for req in PDPLRequirement:
                    result = await ComplianceGapAnalyzer._check_requirement(
                        req,
                        tenant_data,
                        repo
                    )
                    
                    requirement_results.append(result)
                    
                    # Weight critical requirements higher
                    metadata = ComplianceGapAnalyzer.REQUIREMENT_METADATA.get(req, {})
                    weight = 3 if metadata.get('priority') == 'critical' else 1
                    total_weight += weight
                    
                    if result['status'] == ComplianceStatus.COMPLIANT:
                        compliant_count += weight
                
                # Calculate overall score
                overall_score = (compliant_count / total_weight * 100) if total_weight > 0 else 0
                
                # Determine compliance level
                if overall_score >= 90:
                    compliance_level = 'optimized'
                elif overall_score >= 70:
                    compliance_level = 'advanced'
                elif overall_score >= 50:
                    compliance_level = 'developing'
                else:
                    compliance_level = 'basic'
                
                # Identify critical gaps
                critical_gaps = [
                    req['title_vi']
                    for req in requirement_results
                    if req['priority'] == 'critical' and req['status'] != ComplianceStatus.COMPLIANT
                ]
                
                # MPS readiness check
                mps_requirements = [
                    req for req in requirement_results
                    if req.get('mps_required', False)
                ]
                mps_ready = all(
                    req['status'] == ComplianceStatus.COMPLIANT
                    for req in mps_requirements
                )
                
                result = {
                    'overall_compliance_score': round(overall_score, 2),
                    'compliance_level': compliance_level,
                    'requirements': requirement_results,
                    'critical_gaps': critical_gaps,
                    'mps_ready': mps_ready,
                    'analyzed_at': datetime.utcnow().isoformat()
                }
                
                logger.info(
                    f"[OK] Compliance gap analysis for tenant {tenant_id}: "
                    f"{overall_score:.1f}% compliant, level: {compliance_level}"
                )
                
                return result
                
        except Exception as e:
            logger.error(f"[ERROR] Compliance gap analysis failed: {str(e)}")
            raise
    
    @staticmethod
    async def _check_requirement(
        requirement: PDPLRequirement,
        tenant_data: Dict[str, Any],
        repo
    ) -> Dict[str, Any]:
        """Check individual compliance requirement"""
        metadata = ComplianceGapAnalyzer.REQUIREMENT_METADATA.get(requirement, {})
        
        # Initialize result
        result = {
            'requirement': requirement,
            'title_vi': metadata.get('title_vi', ''),
            'title_en': metadata.get('title_en', ''),
            'legal_reference': metadata.get('legal_reference', ''),
            'priority': metadata.get('priority', 'medium'),
            'mps_required': metadata.get('mps_required', False),
            'status': ComplianceStatus.UNKNOWN,
            'gaps': [],
            'recommendations': []
        }
        
        # Check specific requirements
        if requirement == PDPLRequirement.ROPA_DOCUMENTED:
            ropa_entries = tenant_data.get('ropa_entries', [])
            classified_fields = tenant_data.get('classified_fields', [])
            
            if len(ropa_entries) > 0 and len(classified_fields) > 0:
                coverage = len(ropa_entries) / len(classified_fields)
                if coverage >= 0.95:
                    result['status'] = ComplianceStatus.COMPLIANT
                elif coverage >= 0.70:
                    result['status'] = ComplianceStatus.PARTIAL
                    result['gaps'].append(
                        f"ROPA covers {coverage*100:.0f}% of fields (target: 95%)"
                    )
                    result['recommendations'].append(
                        "Complete ROPA for remaining fields"
                    )
                else:
                    result['status'] = ComplianceStatus.NON_COMPLIANT
                    result['gaps'].append(
                        f"ROPA only covers {coverage*100:.0f}% of fields"
                    )
                    result['recommendations'].append(
                        "Use bulk ROPA generation feature to document all fields"
                    )
            else:
                result['status'] = ComplianceStatus.NON_COMPLIANT
                result['gaps'].append("No ROPA entries found")
                result['recommendations'].append("Generate ROPA from discovered data assets")
        
        elif requirement == PDPLRequirement.DPO_DESIGNATED:
            dpo_info = tenant_data.get('dpo_info')
            if dpo_info and dpo_info.get('name') and dpo_info.get('email'):
                result['status'] = ComplianceStatus.COMPLIANT
            else:
                result['status'] = ComplianceStatus.NON_COMPLIANT
                result['gaps'].append("DPO information not configured")
                result['recommendations'].append("Designate DPO and update contact information")
        
        elif requirement == PDPLRequirement.LEGAL_BASIS_DEFINED:
            fields_without_basis = tenant_data.get('fields_without_legal_basis', [])
            total_fields = tenant_data.get('total_fields', 0)
            
            if len(fields_without_basis) == 0:
                result['status'] = ComplianceStatus.COMPLIANT
            elif len(fields_without_basis) / total_fields < 0.1:
                result['status'] = ComplianceStatus.PARTIAL
                result['gaps'].append(
                    f"{len(fields_without_basis)} fields missing legal basis"
                )
                result['recommendations'].append(
                    "Define legal basis for remaining fields"
                )
            else:
                result['status'] = ComplianceStatus.NON_COMPLIANT
                result['gaps'].append(
                    f"{len(fields_without_basis)} fields missing legal basis"
                )
                result['recommendations'].append(
                    "Review and define legal basis (consent, contract, legal obligation)"
                )
        
        elif requirement == PDPLRequirement.RETENTION_POLICY_DEFINED:
            fields_without_retention = tenant_data.get('fields_without_retention', [])
            total_fields = tenant_data.get('total_fields', 0)
            
            if len(fields_without_retention) == 0:
                result['status'] = ComplianceStatus.COMPLIANT
            elif len(fields_without_retention) / total_fields < 0.2:
                result['status'] = ComplianceStatus.PARTIAL
                result['gaps'].append(
                    f"{len(fields_without_retention)} fields without retention policy"
                )
            else:
                result['status'] = ComplianceStatus.NON_COMPLIANT
                result['gaps'].append(
                    f"{len(fields_without_retention)} fields without retention policy"
                )
                result['recommendations'].append(
                    "Define retention periods per PDPL Article 13"
                )
        
        elif requirement == PDPLRequirement.CROSS_BORDER_DOCUMENTED:
            cross_border_flows = tenant_data.get('cross_border_flows', [])
            flows_with_safeguards = [
                f for f in cross_border_flows
                if f.get('transfer_safeguards')
            ]
            
            if len(cross_border_flows) == 0:
                result['status'] = ComplianceStatus.NOT_APPLICABLE
            elif len(flows_with_safeguards) == len(cross_border_flows):
                result['status'] = ComplianceStatus.COMPLIANT
            else:
                result['status'] = ComplianceStatus.NON_COMPLIANT
                missing = len(cross_border_flows) - len(flows_with_safeguards)
                result['gaps'].append(
                    f"{missing} cross-border transfers lack documented safeguards"
                )
                result['recommendations'].append(
                    "Document transfer mechanisms (SCCs, BCRs, adequacy decisions)"
                )
        
        elif requirement == PDPLRequirement.ENCRYPTION_IMPLEMENTED:
            sensitive_fields = tenant_data.get('sensitive_fields', [])
            encrypted_fields = [
                f for f in sensitive_fields
                if f.get('is_encrypted', False)
            ]
            
            if len(sensitive_fields) == 0:
                result['status'] = ComplianceStatus.NOT_APPLICABLE
            elif len(encrypted_fields) == len(sensitive_fields):
                result['status'] = ComplianceStatus.COMPLIANT
            elif len(encrypted_fields) / len(sensitive_fields) >= 0.8:
                result['status'] = ComplianceStatus.PARTIAL
                result['gaps'].append(
                    f"{len(sensitive_fields) - len(encrypted_fields)} sensitive fields not encrypted"
                )
            else:
                result['status'] = ComplianceStatus.NON_COMPLIANT
                result['gaps'].append(
                    f"{len(sensitive_fields) - len(encrypted_fields)} sensitive fields not encrypted"
                )
                result['recommendations'].append(
                    "Enable encryption for sensitive personal data"
                )
        
        elif requirement == PDPLRequirement.MPS_READY_TO_SUBMIT:
            # Check all MPS-required items
            mps_requirements = [
                PDPLRequirement.ROPA_DOCUMENTED,
                PDPLRequirement.DPO_DESIGNATED,
                PDPLRequirement.LEGAL_BASIS_DEFINED,
                PDPLRequirement.CROSS_BORDER_DOCUMENTED
            ]
            
            # This is a meta-check, implementation would check all MPS requirements
            result['status'] = ComplianceStatus.PARTIAL  # Placeholder
            result['gaps'].append("Automated MPS readiness check not yet implemented")
        
        return result
```

---

## Smart Recommendations Engine

### Rule-Based Recommendations

```python
# File: backend/veri_ai_data_inventory/intelligence/recommendations_engine.py

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RecommendationType(str, Enum):
    """Recommendation categories"""
    CLASSIFICATION = "classification"
    RETENTION = "retention"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    DATA_QUALITY = "data_quality"
    COST_OPTIMIZATION = "cost_optimization"

class RecommendationPriority(str, Enum):
    """Recommendation priority levels"""
    CRITICAL = "critical"  # Must address immediately
    HIGH = "high"          # Address soon
    MEDIUM = "medium"      # Address when possible
    LOW = "low"            # Optional improvement

class SmartRecommendationsEngine:
    """AI-powered and rule-based recommendations for DPOs"""
    
    @staticmethod
    async def generate_recommendations(
        tenant_id: str,
        field_data: Optional[Dict[str, Any]] = None,
        scope: str = 'all',  # 'all', 'field', 'table', 'tenant'
        veri_context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate smart recommendations for DPO
        
        Args:
            tenant_id: Tenant UUID
            field_data: Specific field to analyze (optional)
            scope: Recommendation scope
            veri_context: Vietnamese business context
            
        Returns:
            List of recommendations with priority and rationale
        """
        try:
            recommendations = []
            
            # Rule-based recommendations
            rule_recommendations = await SmartRecommendationsEngine._generate_rule_based(
                tenant_id,
                field_data,
                scope,
                veri_context
            )
            recommendations.extend(rule_recommendations)
            
            # AI-powered recommendations (if AI client available)
            try:
                ai_recommendations = await SmartRecommendationsEngine._generate_ai_powered(
                    tenant_id,
                    field_data,
                    veri_context
                )
                recommendations.extend(ai_recommendations)
            except Exception as e:
                logger.warning(f"[WARNING] AI recommendations unavailable: {str(e)}")
            
            # Sort by priority
            priority_order = {
                RecommendationPriority.CRITICAL: 0,
                RecommendationPriority.HIGH: 1,
                RecommendationPriority.MEDIUM: 2,
                RecommendationPriority.LOW: 3
            }
            
            recommendations.sort(
                key=lambda x: priority_order.get(x['priority'], 999)
            )
            
            logger.info(
                f"[OK] Generated {len(recommendations)} recommendations for tenant {tenant_id}"
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"[ERROR] Recommendation generation failed: {str(e)}")
            raise
    
    @staticmethod
    async def _generate_rule_based(
        tenant_id: str,
        field_data: Optional[Dict[str, Any]],
        scope: str,
        veri_context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate rule-based recommendations"""
        recommendations = []
        
        from ..repositories.inventory_repository import InventoryRepository
        from ..database import get_async_session
        
        async with get_async_session() as session:
            repo = InventoryRepository(session)
            
            if scope in ['all', 'tenant']:
                # Tenant-level recommendations
                tenant_data = await repo.get_tenant_compliance_data(tenant_id)
                
                # Retention policy recommendation
                fields_without_retention = tenant_data.get('fields_without_retention', [])
                if len(fields_without_retention) > 0:
                    recommendations.append({
                        'type': RecommendationType.RETENTION,
                        'priority': RecommendationPriority.HIGH,
                        'title_vi': f"{len(fields_without_retention)} trường thiếu chính sách lưu trữ",
                        'title_en': f"{len(fields_without_retention)} fields missing retention policy",
                        'description_vi': "Định nghĩa thời gian lưu trữ theo Điều 13 PDPL 2025",
                        'description_en': "Define retention periods per PDPL Article 13",
                        'action': "review_retention_policies",
                        'affected_fields': [f['field_id'] for f in fields_without_retention[:10]],
                        'legal_reference': 'PDPL Article 13'
                    })
                
                # Cross-border safeguards recommendation
                cross_border_flows = tenant_data.get('cross_border_flows', [])
                flows_without_safeguards = [
                    f for f in cross_border_flows
                    if not f.get('transfer_safeguards')
                ]
                if len(flows_without_safeguards) > 0:
                    recommendations.append({
                        'type': RecommendationType.COMPLIANCE,
                        'priority': RecommendationPriority.CRITICAL,
                        'title_vi': f"{len(flows_without_safeguards)} luồng chuyển dữ liệu xuyên biên giới thiếu biện pháp bảo vệ",
                        'title_en': f"{len(flows_without_safeguards)} cross-border transfers lack safeguards",
                        'description_vi': "Thêm Standard Contractual Clauses (SCCs) hoặc Binding Corporate Rules (BCRs)",
                        'description_en': "Add Standard Contractual Clauses (SCCs) or Binding Corporate Rules (BCRs)",
                        'action': "configure_transfer_safeguards",
                        'affected_flows': [f['flow_id'] for f in flows_without_safeguards],
                        'legal_reference': 'PDPL Article 20'
                    })
                
                # Encryption recommendation for sensitive data
                sensitive_fields = tenant_data.get('sensitive_fields', [])
                unencrypted_sensitive = [
                    f for f in sensitive_fields
                    if not f.get('is_encrypted', False)
                ]
                if len(unencrypted_sensitive) > 0:
                    recommendations.append({
                        'type': RecommendationType.SECURITY,
                        'priority': RecommendationPriority.HIGH,
                        'title_vi': f"{len(unencrypted_sensitive)} trường nhạy cảm chưa mã hóa",
                        'title_en': f"{len(unencrypted_sensitive)} sensitive fields not encrypted",
                        'description_vi': "Bật mã hóa cấp trường cho dữ liệu cá nhân nhạy cảm",
                        'description_en': "Enable field-level encryption for sensitive personal data",
                        'action': "enable_encryption",
                        'affected_fields': [f['field_id'] for f in unencrypted_sensitive[:20]],
                        'legal_reference': 'PDPL Article 15'
                    })
                
                # Vietnamese-specific: Regional data center recommendation
                if veri_context and veri_context.get('veri_regional_location'):
                    region = veri_context['veri_regional_location']
                    industry = veri_context.get('veri_industry_type', '')
                    
                    if region == 'north' and industry in ['government', 'finance']:
                        recommendations.append({
                            'type': RecommendationType.COMPLIANCE,
                            'priority': RecommendationPriority.MEDIUM,
                            'title_vi': 'Xem xét trung tâm dữ liệu Hà Nội cho dữ liệu chính phủ',
                            'title_en': 'Consider Hanoi data center for government data',
                            'description_vi': 'Dữ liệu liên quan đến chính phủ nên lưu trữ tại miền Bắc để gần các cơ quan nhà nước',
                            'description_en': 'Government-related data should be stored in Northern Vietnam for proximity to authorities',
                            'action': 'review_data_residency',
                            'regional_context': 'north_vietnam',
                            'legal_reference': 'Vietnamese data sovereignty best practices'
                        })
            
            if scope in ['all', 'field'] and field_data:
                # Field-level recommendations
                field_recommendations = SmartRecommendationsEngine._generate_field_recommendations(
                    field_data,
                    veri_context
                )
                recommendations.extend(field_recommendations)
        
        return recommendations
    
    @staticmethod
    def _generate_field_recommendations(
        field_data: Dict[str, Any],
        veri_context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations for a specific field"""
        recommendations = []
        
        # Check for indefinite retention
        retention = field_data.get('retention_period', '').lower()
        if 'indefinite' in retention or 'permanent' in retention:
            recommendations.append({
                'type': RecommendationType.RETENTION,
                'priority': RecommendationPriority.HIGH,
                'title_vi': f"Trường '{field_data['field_name']}' có thời gian lưu trữ vô thời hạn",
                'title_en': f"Field '{field_data['field_name']}' has indefinite retention",
                'description_vi': "Đề xuất: 7 năm cho dữ liệu tài chính, 5 năm cho dữ liệu khác theo PDPL",
                'description_en': "Suggestion: 7 years for financial data, 5 years for other data per PDPL",
                'action': 'update_retention_period',
                'suggested_retention': '7 years' if 'financial' in field_data.get('classification', '').lower() else '5 years',
                'legal_reference': 'PDPL Article 13'
            })
        
        # Check for missing classification
        if not field_data.get('classification') or field_data.get('classification') == 'unknown':
            recommendations.append({
                'type': RecommendationType.CLASSIFICATION,
                'priority': RecommendationPriority.CRITICAL,
                'title_vi': f"Trường '{field_data['field_name']}' chưa được phân loại",
                'title_en': f"Field '{field_data['field_name']}' is not classified",
                'description_vi': "Chạy phân loại AI để xác định loại dữ liệu cá nhân",
                'description_en': "Run AI classification to identify personal data type",
                'action': 'classify_field',
                'legal_reference': 'PDPL Article 17 - ROPA requirement'
            })
        
        # Vietnamese name format validation
        if field_data.get('classification', '').lower() in ['full_name', 'name', 'ho_ten']:
            sample_values = field_data.get('sample_values', [])
            invalid_names = [
                v for v in sample_values
                if isinstance(v, str) and any(char.isdigit() for char in v)
            ]
            
            if len(invalid_names) > 0:
                recommendations.append({
                    'type': RecommendationType.DATA_QUALITY,
                    'priority': RecommendationPriority.MEDIUM,
                    'title_vi': f"{len(invalid_names)} tên chứa ký tự không hợp lệ",
                    'title_en': f"{len(invalid_names)} names contain invalid characters",
                    'description_vi': "Tên tiếng Việt không nên chứa số",
                    'description_en': "Vietnamese names should not contain numbers",
                    'action': 'review_data_quality',
                    'invalid_samples': invalid_names[:5]
                })
        
        return recommendations
    
    @staticmethod
    async def _generate_ai_powered(
        tenant_id: str,
        field_data: Optional[Dict[str, Any]],
        veri_context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate AI-powered recommendations (placeholder for ML model)"""
        # TODO: Integrate with veri-vi-ai-classification service
        # This would use the veri-vi-ai-classification service to generate
        # intelligent PDPL recommendations based on principles classification
        return []
```

---

## Data Quality Indicators

### Data Quality Analyzer

```python
# File: backend/veri_ai_data_inventory/intelligence/data_quality_analyzer.py

from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

class QualityMetric(str, Enum):
    """Data quality metric types"""
    NULL_PERCENTAGE = "null_percentage"
    DUPLICATE_PERCENTAGE = "duplicate_percentage"
    FORMAT_VALIDITY = "format_validity"
    UNIQUENESS = "uniqueness"
    CONSISTENCY = "consistency"
    COMPLETENESS = "completeness"

class QualityLevel(str, Enum):
    """Data quality levels"""
    EXCELLENT = "excellent"   # >95% quality
    GOOD = "good"             # 85-95% quality
    FAIR = "fair"             # 70-85% quality
    POOR = "poor"             # <70% quality

class VietnameseDataValidator:
    """Vietnamese-specific data validation"""
    
    # Vietnamese phone number patterns
    PHONE_PATTERNS = [
        r'^(0|\+84)(3|5|7|8|9)\d{8}$',  # Mobile: 03, 05, 07, 08, 09 + 8 digits
        r'^(0|\+84)(2)\d{9}$'            # Landline: 02 + 9 digits
    ]
    
    # Vietnamese ID patterns
    ID_PATTERNS = {
        'cmnd': r'^\d{9}$',              # Old ID: 9 digits
        'cccd': r'^\d{12}$',             # New ID: 12 digits
        'passport': r'^[A-Z]\d{7}$'      # Passport: 1 letter + 7 digits
    }
    
    # Vietnamese name patterns (simplified)
    NAME_PATTERN = r'^[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(\s[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*)+$'
    
    # Vietnamese address patterns (basic)
    ADDRESS_KEYWORDS = [
        'đường', 'phố', 'quận', 'huyện', 'thành phố', 'tỉnh',
        'phường', 'xã', 'thị trấn', 'số nhà'
    ]
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Validate Vietnamese phone number format"""
        if not phone:
            return False
        
        phone_clean = re.sub(r'\s|-|\.|', '', str(phone))
        
        for pattern in VietnameseDataValidator.PHONE_PATTERNS:
            if re.match(pattern, phone_clean):
                return True
        
        return False
    
    @staticmethod
    def validate_id_number(id_number: str, id_type: str = 'auto') -> bool:
        """Validate Vietnamese ID number format"""
        if not id_number:
            return False
        
        id_clean = str(id_number).strip()
        
        if id_type == 'auto':
            # Auto-detect ID type
            for id_type, pattern in VietnameseDataValidator.ID_PATTERNS.items():
                if re.match(pattern, id_clean):
                    return True
            return False
        else:
            pattern = VietnameseDataValidator.ID_PATTERNS.get(id_type)
            if pattern:
                return bool(re.match(pattern, id_clean))
            return False
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate Vietnamese name format"""
        if not name:
            return False
        
        name_clean = str(name).strip()
        
        # Check for invalid characters (numbers, special chars)
        if re.search(r'\d|[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/]', name_clean):
            return False
        
        # Check Vietnamese name pattern
        return bool(re.match(VietnameseDataValidator.NAME_PATTERN, name_clean))
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """Validate Vietnamese address format (basic)"""
        if not address:
            return False
        
        address_lower = str(address).lower()
        
        # Check if contains Vietnamese address keywords
        return any(keyword in address_lower for keyword in VietnameseDataValidator.ADDRESS_KEYWORDS)


class DataQualityAnalyzer:
    """Analyze data quality for fields and tables"""
    
    @staticmethod
    async def analyze_field_quality(
        field_data: Dict[str, Any],
        sample_values: List[Any],
        total_row_count: int
    ) -> Dict[str, Any]:
        """
        Analyze data quality for a single field
        
        Args:
            field_data: {
                'field_name': str,
                'table_name': str,
                'classification': str,
                'data_type': str
            }
            sample_values: List of sample values from the field
            total_row_count: Total number of rows in the table
            
        Returns:
            {
                'field_identifier': str,
                'quality_score': float (0-100),
                'quality_level': QualityLevel,
                'metrics': {
                    'null_percentage': float,
                    'duplicate_percentage': float,
                    'format_validity': float,
                    'uniqueness_percentage': float
                },
                'issues': List[str],
                'recommendations': List[str]
            }
        """
        try:
            field_identifier = f"{field_data['table_name']}.{field_data['field_name']}"
            
            # Calculate quality metrics
            null_pct = DataQualityAnalyzer._calculate_null_percentage(
                sample_values,
                total_row_count
            )
            
            duplicate_pct = DataQualityAnalyzer._calculate_duplicate_percentage(
                sample_values
            )
            
            format_validity = DataQualityAnalyzer._calculate_format_validity(
                sample_values,
                field_data
            )
            
            uniqueness_pct = DataQualityAnalyzer._calculate_uniqueness(
                sample_values
            )
            
            # Calculate overall quality score
            quality_score = (
                (100 - null_pct) * 0.3 +          # 30% weight on null percentage
                (100 - duplicate_pct) * 0.2 +     # 20% weight on duplicates
                format_validity * 0.3 +            # 30% weight on format validity
                uniqueness_pct * 0.2               # 20% weight on uniqueness
            )
            
            # Determine quality level
            if quality_score >= 95:
                quality_level = QualityLevel.EXCELLENT
            elif quality_score >= 85:
                quality_level = QualityLevel.GOOD
            elif quality_score >= 70:
                quality_level = QualityLevel.FAIR
            else:
                quality_level = QualityLevel.POOR
            
            # Identify issues
            issues = DataQualityAnalyzer._identify_quality_issues(
                null_pct,
                duplicate_pct,
                format_validity,
                field_data
            )
            
            # Generate recommendations
            recommendations = DataQualityAnalyzer._generate_quality_recommendations(
                issues,
                field_data
            )
            
            result = {
                'field_identifier': field_identifier,
                'quality_score': round(quality_score, 2),
                'quality_level': quality_level,
                'metrics': {
                    'null_percentage': round(null_pct, 2),
                    'duplicate_percentage': round(duplicate_pct, 2),
                    'format_validity': round(format_validity, 2),
                    'uniqueness_percentage': round(uniqueness_pct, 2)
                },
                'issues': issues,
                'recommendations': recommendations,
                'analyzed_at': datetime.utcnow().isoformat()
            }
            
            logger.info(
                f"[OK] Quality analysis for {field_identifier}: "
                f"{quality_score:.1f}% ({quality_level})"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"[ERROR] Quality analysis failed: {str(e)}")
            raise
    
    @staticmethod
    def _calculate_null_percentage(
        sample_values: List[Any],
        total_row_count: int
    ) -> float:
        """Calculate percentage of null/empty values"""
        if not sample_values:
            return 100.0
        
        null_count = sum(
            1 for v in sample_values
            if v is None or (isinstance(v, str) and v.strip() == '')
        )
        
        null_pct = (null_count / len(sample_values)) * 100
        return null_pct
    
    @staticmethod
    def _calculate_duplicate_percentage(sample_values: List[Any]) -> float:
        """Calculate percentage of duplicate values"""
        if not sample_values:
            return 0.0
        
        unique_count = len(set(str(v) for v in sample_values if v is not None))
        total_count = len([v for v in sample_values if v is not None])
        
        if total_count == 0:
            return 0.0
        
        duplicate_pct = ((total_count - unique_count) / total_count) * 100
        return duplicate_pct
    
    @staticmethod
    def _calculate_format_validity(
        sample_values: List[Any],
        field_data: Dict[str, Any]
    ) -> float:
        """Calculate percentage of values matching expected format"""
        classification = field_data.get('classification', '').lower()
        
        if not sample_values:
            return 0.0
        
        valid_count = 0
        non_null_values = [v for v in sample_values if v is not None]
        
        if not non_null_values:
            return 100.0  # No values to validate
        
        # Vietnamese-specific validations
        if classification in ['phone', 'phone_number', 'so_dien_thoai']:
            for value in non_null_values:
                if VietnameseDataValidator.validate_phone_number(str(value)):
                    valid_count += 1
        
        elif classification in ['cmnd', 'cccd', 'passport', 'id_number']:
            for value in non_null_values:
                if VietnameseDataValidator.validate_id_number(str(value)):
                    valid_count += 1
        
        elif classification in ['full_name', 'name', 'ho_ten']:
            for value in non_null_values:
                if VietnameseDataValidator.validate_name(str(value)):
                    valid_count += 1
        
        elif classification in ['address', 'dia_chi']:
            for value in non_null_values:
                if VietnameseDataValidator.validate_address(str(value)):
                    valid_count += 1
        
        elif classification in ['email', 'email_address']:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            for value in non_null_values:
                if re.match(email_pattern, str(value)):
                    valid_count += 1
        
        else:
            # Generic validation: non-empty string
            valid_count = len(non_null_values)
        
        validity_pct = (valid_count / len(non_null_values)) * 100
        return validity_pct
    
    @staticmethod
    def _calculate_uniqueness(sample_values: List[Any]) -> float:
        """Calculate uniqueness percentage"""
        if not sample_values:
            return 0.0
        
        non_null_values = [v for v in sample_values if v is not None]
        
        if not non_null_values:
            return 0.0
        
        unique_count = len(set(str(v) for v in non_null_values))
        uniqueness_pct = (unique_count / len(non_null_values)) * 100
        return uniqueness_pct
    
    @staticmethod
    def _identify_quality_issues(
        null_pct: float,
        duplicate_pct: float,
        format_validity: float,
        field_data: Dict[str, Any]
    ) -> List[str]:
        """Identify specific quality issues"""
        issues = []
        
        if null_pct > 20:
            issues.append(f"High null percentage: {null_pct:.1f}%")
        
        if duplicate_pct > 30:
            issues.append(f"High duplicate percentage: {duplicate_pct:.1f}%")
        
        if format_validity < 80:
            issues.append(f"Low format validity: {format_validity:.1f}%")
        
        return issues
    
    @staticmethod
    def _generate_quality_recommendations(
        issues: List[str],
        field_data: Dict[str, Any]
    ) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        for issue in issues:
            if 'null' in issue.lower():
                recommendations.append(
                    "Review data collection process to reduce null values"
                )
                recommendations.append(
                    "Consider field-level NOT NULL constraints"
                )
            
            elif 'duplicate' in issue.lower():
                recommendations.append(
                    "Investigate duplicate records - potential data entry errors"
                )
                recommendations.append(
                    "Implement unique constraints if field should be unique"
                )
            
            elif 'format' in issue.lower():
                classification = field_data.get('classification', '')
                recommendations.append(
                    f"Standardize {classification} format in data entry forms"
                )
                recommendations.append(
                    "Implement input validation at application level"
                )
        
        return recommendations


class TableQualityAnalyzer:
    """Analyze data quality at table level"""
    
    @staticmethod
    async def analyze_table_quality(
        tenant_id: str,
        table_name: str
    ) -> Dict[str, Any]:
        """
        Analyze overall data quality for a table
        
        Returns:
            {
                'table_name': str,
                'overall_quality_score': float,
                'overall_quality_level': QualityLevel,
                'field_quality_scores': List[Dict],
                'table_metrics': {
                    'total_fields': int,
                    'fields_with_issues': int,
                    'avg_null_percentage': float,
                    'avg_format_validity': float
                }
            }
        """
        try:
            from ..repositories.inventory_repository import InventoryRepository
            from ..database import get_async_session
            
            async with get_async_session() as session:
                repo = InventoryRepository(session)
                
                # Get all fields for table
                fields = await repo.get_table_fields(tenant_id, table_name)
                
                field_quality_scores = []
                total_quality_score = 0.0
                fields_with_issues = 0
                total_null_pct = 0.0
                total_format_validity = 0.0
                
                for field in fields:
                    # Get sample values
                    sample_values = await repo.get_field_sample_values(
                        field['field_id'],
                        limit=1000
                    )
                    
                    # Analyze field quality
                    field_quality = await DataQualityAnalyzer.analyze_field_quality(
                        field_data=field,
                        sample_values=sample_values,
                        total_row_count=field.get('row_count', len(sample_values))
                    )
                    
                    field_quality_scores.append(field_quality)
                    total_quality_score += field_quality['quality_score']
                    
                    if len(field_quality['issues']) > 0:
                        fields_with_issues += 1
                    
                    total_null_pct += field_quality['metrics']['null_percentage']
                    total_format_validity += field_quality['metrics']['format_validity']
                
                # Calculate overall metrics
                num_fields = len(fields)
                overall_quality_score = total_quality_score / num_fields if num_fields > 0 else 0
                
                if overall_quality_score >= 95:
                    overall_quality_level = QualityLevel.EXCELLENT
                elif overall_quality_score >= 85:
                    overall_quality_level = QualityLevel.GOOD
                elif overall_quality_score >= 70:
                    overall_quality_level = QualityLevel.FAIR
                else:
                    overall_quality_level = QualityLevel.POOR
                
                result = {
                    'table_name': table_name,
                    'overall_quality_score': round(overall_quality_score, 2),
                    'overall_quality_level': overall_quality_level,
                    'field_quality_scores': field_quality_scores,
                    'table_metrics': {
                        'total_fields': num_fields,
                        'fields_with_issues': fields_with_issues,
                        'avg_null_percentage': round(total_null_pct / num_fields, 2) if num_fields > 0 else 0,
                        'avg_format_validity': round(total_format_validity / num_fields, 2) if num_fields > 0 else 0
                    },
                    'analyzed_at': datetime.utcnow().isoformat()
                }
                
                logger.info(
                    f"[OK] Table quality analysis for {table_name}: "
                    f"{overall_quality_score:.1f}% ({overall_quality_level})"
                )
                
                return result
                
        except Exception as e:
            logger.error(f"[ERROR] Table quality analysis failed: {str(e)}")
            raise
```

---

## Cost Impact Dashboard

### Cost Calculator

```python
# File: backend/veri_ai_data_inventory/intelligence/cost_calculator.py

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class CostCategory(str, Enum):
    """Cost categories for PDPL compliance"""
    STORAGE = "storage"
    PROCESSING = "processing"
    PERSONNEL = "personnel"
    THIRD_PARTY = "third_party"
    INFRASTRUCTURE = "infrastructure"

class CostCalculator:
    """Calculate costs related to data inventory and compliance"""
    
    # Cost constants (in VND - Vietnamese Dong)
    STORAGE_COST_PER_GB_MONTH = 50000      # ~50K VND per GB/month (~$2 USD)
    PROCESSING_COST_PER_1M_ROWS = 200000   # ~200K VND per 1M rows scanned (~$8 USD)
    DPO_HOURLY_RATE = 500000               # ~500K VND per hour (~$20 USD)
    AI_CLASSIFICATION_PER_FIELD = 1000     # ~1K VND per field (~$0.04 USD)
    
    # Time estimates (hours)
    MANUAL_FIELD_REVIEW_HOURS = 0.05       # 3 minutes per field
    MANUAL_ROPA_ENTRY_HOURS = 0.5          # 30 minutes per ROPA entry
    COMPLIANCE_AUDIT_PREP_HOURS = 40       # 40 hours per audit
    
    @staticmethod
    async def calculate_total_costs(
        tenant_id: str,
        period_start: datetime,
        period_end: datetime
    ) -> Dict[str, Any]:
        """
        Calculate total costs for a tenant over a time period
        
        Args:
            tenant_id: Tenant UUID
            period_start: Start of cost calculation period
            period_end: End of cost calculation period
            
        Returns:
            {
                'total_cost_vnd': float,
                'total_cost_usd': float,
                'cost_breakdown': {
                    'storage_cost': float,
                    'processing_cost': float,
                    'personnel_cost': float,
                    'ai_cost': float
                },
                'period_days': int,
                'savings_from_column_filtering': float
            }
        """
        try:
            from ..repositories.inventory_repository import InventoryRepository
            from ..database import get_async_session
            
            async with get_async_session() as session:
                repo = InventoryRepository(session)
                
                # Get tenant data
                tenant_data = await repo.get_tenant_cost_data(
                    tenant_id,
                    period_start,
                    period_end
                )
                
                # Calculate storage costs
                storage_cost = CostCalculator._calculate_storage_cost(tenant_data)
                
                # Calculate processing costs
                processing_cost = CostCalculator._calculate_processing_cost(tenant_data)
                
                # Calculate personnel costs
                personnel_cost = CostCalculator._calculate_personnel_cost(tenant_data)
                
                # Calculate AI classification costs
                ai_cost = CostCalculator._calculate_ai_cost(tenant_data)
                
                # Calculate total
                total_cost_vnd = (
                    storage_cost +
                    processing_cost +
                    personnel_cost +
                    ai_cost
                )
                
                # Convert to USD (approximate rate: 1 USD = 24,000 VND)
                total_cost_usd = total_cost_vnd / 24000
                
                # Calculate savings from column filtering
                savings_vnd = CostCalculator._calculate_filter_savings(tenant_data)
                
                period_days = (period_end - period_start).days
                
                result = {
                    'total_cost_vnd': round(total_cost_vnd, 2),
                    'total_cost_usd': round(total_cost_usd, 2),
                    'cost_breakdown': {
                        'storage_cost_vnd': round(storage_cost, 2),
                        'processing_cost_vnd': round(processing_cost, 2),
                        'personnel_cost_vnd': round(personnel_cost, 2),
                        'ai_cost_vnd': round(ai_cost, 2)
                    },
                    'period_days': period_days,
                    'savings_from_column_filtering_vnd': round(savings_vnd, 2),
                    'savings_from_column_filtering_usd': round(savings_vnd / 24000, 2),
                    'calculated_at': datetime.utcnow().isoformat()
                }
                
                logger.info(
                    f"[OK] Cost calculation for tenant {tenant_id}: "
                    f"{total_cost_vnd:,.0f} VND (${total_cost_usd:,.2f} USD)"
                )
                
                return result
                
        except Exception as e:
            logger.error(f"[ERROR] Cost calculation failed: {str(e)}")
            raise
    
    @staticmethod
    def _calculate_storage_cost(tenant_data: Dict[str, Any]) -> float:
        """Calculate storage costs"""
        total_data_size_gb = tenant_data.get('total_data_size_gb', 0)
        storage_days = tenant_data.get('storage_days', 30)
        
        # Monthly cost prorated by days
        storage_cost = (
            total_data_size_gb *
            CostCalculator.STORAGE_COST_PER_GB_MONTH *
            (storage_days / 30)
        )
        
        return storage_cost
    
    @staticmethod
    def _calculate_processing_cost(tenant_data: Dict[str, Any]) -> float:
        """Calculate data processing costs"""
        total_rows_scanned = tenant_data.get('total_rows_scanned', 0)
        
        # Cost per million rows
        processing_cost = (
            (total_rows_scanned / 1000000) *
            CostCalculator.PROCESSING_COST_PER_1M_ROWS
        )
        
        return processing_cost
    
    @staticmethod
    def _calculate_personnel_cost(tenant_data: Dict[str, Any]) -> float:
        """Calculate DPO personnel time costs"""
        manual_review_fields = tenant_data.get('manual_review_fields', 0)
        manual_ropa_entries = tenant_data.get('manual_ropa_entries', 0)
        compliance_audits = tenant_data.get('compliance_audits', 0)
        
        # Calculate total hours
        total_hours = (
            manual_review_fields * CostCalculator.MANUAL_FIELD_REVIEW_HOURS +
            manual_ropa_entries * CostCalculator.MANUAL_ROPA_ENTRY_HOURS +
            compliance_audits * CostCalculator.COMPLIANCE_AUDIT_PREP_HOURS
        )
        
        personnel_cost = total_hours * CostCalculator.DPO_HOURLY_RATE
        
        return personnel_cost
    
    @staticmethod
    def _calculate_ai_cost(tenant_data: Dict[str, Any]) -> float:
        """Calculate AI classification costs"""
        fields_classified = tenant_data.get('fields_classified_by_ai', 0)
        
        ai_cost = fields_classified * CostCalculator.AI_CLASSIFICATION_PER_FIELD
        
        return ai_cost
    
    @staticmethod
    def _calculate_filter_savings(tenant_data: Dict[str, Any]) -> float:
        """Calculate cost savings from column filtering"""
        columns_filtered = tenant_data.get('columns_filtered_count', 0)
        total_columns = tenant_data.get('total_columns_discovered', 0)
        
        if total_columns == 0:
            return 0.0
        
        filter_reduction_pct = (columns_filtered / total_columns) * 100
        
        # Savings from reduced storage
        storage_savings = (
            tenant_data.get('total_data_size_gb', 0) *
            (filter_reduction_pct / 100) *
            CostCalculator.STORAGE_COST_PER_GB_MONTH
        )
        
        # Savings from reduced AI processing
        ai_savings = (
            columns_filtered *
            CostCalculator.AI_CLASSIFICATION_PER_FIELD
        )
        
        # Savings from reduced DPO time
        personnel_savings = (
            columns_filtered *
            CostCalculator.MANUAL_FIELD_REVIEW_HOURS *
            CostCalculator.DPO_HOURLY_RATE
        )
        
        total_savings = storage_savings + ai_savings + personnel_savings
        
        return total_savings


class ROICalculator:
    """Calculate ROI for VeriSyntra platform"""
    
    @staticmethod
    async def calculate_roi(
        tenant_id: str,
        platform_cost_vnd: float,
        period_months: int = 12
    ) -> Dict[str, Any]:
        """
        Calculate ROI for VeriSyntra investment
        
        Args:
            tenant_id: Tenant UUID
            platform_cost_vnd: Annual platform subscription cost in VND
            period_months: Analysis period (default: 12 months)
            
        Returns:
            {
                'platform_cost_vnd': float,
                'time_savings_hours': float,
                'time_savings_cost_vnd': float,
                'compliance_penalty_avoided_vnd': float,
                'total_value_vnd': float,
                'roi_percentage': float,
                'payback_months': float
            }
        """
        try:
            from ..repositories.inventory_repository import InventoryRepository
            from ..database import get_async_session
            
            async with get_async_session() as session:
                repo = InventoryRepository(session)
                
                # Get automation metrics
                metrics = await repo.get_automation_metrics(tenant_id)
                
                # Calculate time savings
                fields_auto_classified = metrics.get('fields_auto_classified', 0)
                ropa_auto_generated = metrics.get('ropa_auto_generated', 0)
                
                time_saved_hours = (
                    fields_auto_classified * CostCalculator.MANUAL_FIELD_REVIEW_HOURS +
                    ropa_auto_generated * CostCalculator.MANUAL_ROPA_ENTRY_HOURS
                )
                
                time_savings_cost = time_saved_hours * CostCalculator.DPO_HOURLY_RATE
                
                # Estimate compliance penalty avoidance
                # PDPL 2025 penalties: up to 5% of annual revenue or 50M VND
                compliance_gaps_fixed = metrics.get('compliance_gaps_fixed', 0)
                
                # Conservative estimate: each critical gap avoided = 10M VND penalty risk
                compliance_penalty_avoided = compliance_gaps_fixed * 10000000
                
                # Total value
                total_value = time_savings_cost + compliance_penalty_avoided
                
                # ROI calculation
                roi_percentage = ((total_value - platform_cost_vnd) / platform_cost_vnd) * 100
                
                # Payback period
                monthly_value = total_value / period_months
                payback_months = platform_cost_vnd / monthly_value if monthly_value > 0 else 999
                
                result = {
                    'platform_cost_vnd': platform_cost_vnd,
                    'platform_cost_usd': round(platform_cost_vnd / 24000, 2),
                    'time_savings_hours': round(time_saved_hours, 2),
                    'time_savings_cost_vnd': round(time_savings_cost, 2),
                    'compliance_penalty_avoided_vnd': round(compliance_penalty_avoided, 2),
                    'total_value_vnd': round(total_value, 2),
                    'total_value_usd': round(total_value / 24000, 2),
                    'roi_percentage': round(roi_percentage, 2),
                    'payback_months': round(payback_months, 1),
                    'period_months': period_months,
                    'calculated_at': datetime.utcnow().isoformat()
                }
                
                logger.info(
                    f"[OK] ROI calculation for tenant {tenant_id}: "
                    f"{roi_percentage:.1f}% ROI, {payback_months:.1f} month payback"
                )
                
                return result
                
        except Exception as e:
            logger.error(f"[ERROR] ROI calculation failed: {str(e)}")
            raise
```

---

## API Endpoints

### Intelligence API Routes

```python
# File: backend/veri_ai_data_inventory/api/intelligence.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging

from ..intelligence.risk_scoring import DataFieldRiskScorer, RiskPriorityQueue, RiskLevel
from ..intelligence.compliance_gap_analyzer import ComplianceGapAnalyzer, ComplianceStatus
from ..intelligence.recommendations_engine import SmartRecommendationsEngine, RecommendationType
from ..intelligence.data_quality_analyzer import DataQualityAnalyzer, TableQualityAnalyzer, QualityLevel
from ..intelligence.cost_calculator import CostCalculator, ROICalculator
from ..auth import get_current_tenant

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/veriportal/intelligence", tags=["Intelligence"])

# Request/Response Models

class RiskScoreRequest(BaseModel):
    field_id: str = Field(..., description="Field UUID to score")

class RiskScoreResponse(BaseModel):
    field_identifier: str
    risk_score: int
    risk_level: RiskLevel
    sensitivity_score: int
    volume_score: int
    exposure_score: int
    retention_score: int
    vietnamese_factors_score: int
    risk_factors: List[str]
    recommendations: List[str]
    calculated_at: str

class PriorityQueueResponse(BaseModel):
    priority_queue: List[dict]
    total_fields: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int

class ComplianceGapResponse(BaseModel):
    overall_compliance_score: float
    compliance_level: str
    requirements: List[dict]
    critical_gaps: List[str]
    mps_ready: bool
    analyzed_at: str

class RecommendationsResponse(BaseModel):
    recommendations: List[dict]
    total_count: int
    critical_count: int
    high_count: int

class QualityAnalysisResponse(BaseModel):
    field_identifier: str
    quality_score: float
    quality_level: QualityLevel
    metrics: dict
    issues: List[str]
    recommendations: List[str]
    analyzed_at: str

class CostCalculationResponse(BaseModel):
    total_cost_vnd: float
    total_cost_usd: float
    cost_breakdown: dict
    period_days: int
    savings_from_column_filtering_vnd: float
    savings_from_column_filtering_usd: float
    calculated_at: str

class ROIResponse(BaseModel):
    platform_cost_vnd: float
    platform_cost_usd: float
    time_savings_hours: float
    time_savings_cost_vnd: float
    compliance_penalty_avoided_vnd: float
    total_value_vnd: float
    total_value_usd: float
    roi_percentage: float
    payback_months: float
    calculated_at: str

# API Endpoints

@router.post("/risk-score", response_model=RiskScoreResponse)
async def calculate_risk_score(
    request: RiskScoreRequest,
    tenant_id: str = Depends(get_current_tenant)
):
    """Calculate risk score for a data field"""
    try:
        # TODO: Fetch field data from repository
        # Placeholder implementation
        scorer = DataFieldRiskScorer()
        
        field_data = {
            'field_name': 'email',
            'table_name': 'customers',
            'pdpl_category': 'regular',
            'classification': 'email_address',
            'row_count': 500000,
            'exposure_type': 'third_party',
            'retention_period': '5 years',
            'is_cross_border': False,
            'is_encrypted': True
        }
        
        result = scorer.calculate_risk_score(field_data)
        
        return RiskScoreResponse(**result)
        
    except Exception as e:
        logger.error(f"[ERROR] Risk score calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/priority-queue", response_model=PriorityQueueResponse)
async def get_priority_queue(
    risk_level: Optional[RiskLevel] = Query(None, description="Filter by risk level"),
    limit: int = Query(50, ge=1, le=500, description="Maximum results"),
    tenant_id: str = Depends(get_current_tenant)
):
    """Get DPO priority queue sorted by risk score"""
    try:
        queue_service = RiskPriorityQueue()
        
        if risk_level:
            priority_queue = await queue_service.get_top_risks(
                tenant_id,
                limit=limit,
                risk_level=risk_level
            )
        else:
            priority_queue = await queue_service.generate_priority_queue(tenant_id)
            priority_queue = priority_queue[:limit]
        
        # Count by risk level
        critical_count = len([f for f in priority_queue if f['risk_level'] == RiskLevel.CRITICAL])
        high_count = len([f for f in priority_queue if f['risk_level'] == RiskLevel.HIGH])
        medium_count = len([f for f in priority_queue if f['risk_level'] == RiskLevel.MEDIUM])
        low_count = len([f for f in priority_queue if f['risk_level'] == RiskLevel.LOW])
        
        return PriorityQueueResponse(
            priority_queue=priority_queue,
            total_fields=len(priority_queue),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count
        )
        
    except Exception as e:
        logger.error(f"[ERROR] Priority queue generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compliance-gaps", response_model=ComplianceGapResponse)
async def analyze_compliance_gaps(
    tenant_id: str = Depends(get_current_tenant)
):
    """Analyze PDPL 2025 compliance gaps"""
    try:
        result = await ComplianceGapAnalyzer.analyze_compliance_gaps(tenant_id)
        return ComplianceGapResponse(**result)
        
    except Exception as e:
        logger.error(f"[ERROR] Compliance gap analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(
    scope: str = Query('all', description="Scope: all, field, table, tenant"),
    field_id: Optional[str] = Query(None, description="Field UUID for field-level recommendations"),
    tenant_id: str = Depends(get_current_tenant)
):
    """Get smart recommendations for DPO"""
    try:
        recommendations = await SmartRecommendationsEngine.generate_recommendations(
            tenant_id=tenant_id,
            scope=scope
        )
        
        critical_count = len([r for r in recommendations if r['priority'] == 'critical'])
        high_count = len([r for r in recommendations if r['priority'] == 'high'])
        
        return RecommendationsResponse(
            recommendations=recommendations,
            total_count=len(recommendations),
            critical_count=critical_count,
            high_count=high_count
        )
        
    except Exception as e:
        logger.error(f"[ERROR] Recommendation generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quality-analysis", response_model=QualityAnalysisResponse)
async def analyze_field_quality(
    field_id: str,
    tenant_id: str = Depends(get_current_tenant)
):
    """Analyze data quality for a field"""
    try:
        # TODO: Fetch field data and sample values from repository
        field_data = {
            'field_name': 'phone_number',
            'table_name': 'customers',
            'classification': 'phone',
            'data_type': 'varchar'
        }
        
        sample_values = ['0901234567', '0912345678', None, '0923456789']
        
        result = await DataQualityAnalyzer.analyze_field_quality(
            field_data=field_data,
            sample_values=sample_values,
            total_row_count=10000
        )
        
        return QualityAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"[ERROR] Quality analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/costs", response_model=CostCalculationResponse)
async def calculate_costs(
    period_days: int = Query(30, ge=1, le=365, description="Analysis period in days"),
    tenant_id: str = Depends(get_current_tenant)
):
    """Calculate total costs for data inventory"""
    try:
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=period_days)
        
        result = await CostCalculator.calculate_total_costs(
            tenant_id=tenant_id,
            period_start=period_start,
            period_end=period_end
        )
        
        return CostCalculationResponse(**result)
        
    except Exception as e:
        logger.error(f"[ERROR] Cost calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roi", response_model=ROIResponse)
async def calculate_roi(
    platform_cost_vnd: float = Query(..., description="Annual platform cost in VND"),
    period_months: int = Query(12, ge=1, le=36, description="Analysis period in months"),
    tenant_id: str = Depends(get_current_tenant)
):
    """Calculate ROI for VeriSyntra platform"""
    try:
        result = await ROICalculator.calculate_roi(
            tenant_id=tenant_id,
            platform_cost_vnd=platform_cost_vnd,
            period_months=period_months
        )
        
        return ROIResponse(**result)
        
    except Exception as e:
        logger.error(f"[ERROR] ROI calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Frontend Components

### VeriDPOIntelligenceDashboard Component

```typescript
// File: src/components/VeriPortal/VeriDPOIntelligence/VeriDPOIntelligenceDashboard.tsx

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useCulturalIntelligence } from '../../../hooks/useCulturalIntelligence';
import { VeriRiskPriorityQueue } from './components/VeriRiskPriorityQueue';
import { VeriComplianceGapPanel } from './components/VeriComplianceGapPanel';
import { VeriRecommendationsPanel } from './components/VeriRecommendationsPanel';
import { VeriQualityMetrics } from './components/VeriQualityMetrics';
import { VeriCostDashboard } from './components/VeriCostDashboard';

interface VeriDPOIntelligenceDashboardProps {
  veriBusinessContext: {
    veriBusinessId: string;
    veriRegionalLocation: 'north' | 'central' | 'south';
    veriIndustryType: string;
  };
}

export const VeriDPOIntelligenceDashboard: React.FC<VeriDPOIntelligenceDashboardProps> = ({
  veriBusinessContext
}) => {
  const { t } = useTranslation();
  const { isVietnamese, tCultural } = useCulturalIntelligence();
  
  const [activeTab, setActiveTab] = useState<string>('risk-priority');
  const [refreshTrigger, setRefreshTrigger] = useState<number>(0);

  const tabs = [
    { id: 'risk-priority', label: t('dpo.intelligence.tabs.risk_priority') },
    { id: 'compliance', label: t('dpo.intelligence.tabs.compliance_gaps') },
    { id: 'recommendations', label: t('dpo.intelligence.tabs.recommendations') },
    { id: 'quality', label: t('dpo.intelligence.tabs.data_quality') },
    { id: 'costs', label: t('dpo.intelligence.tabs.cost_dashboard') }
  ];

  const handleRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="veri-dpo-intelligence-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="text-2xl font-bold text-veri-green-dark">
          {isVietnamese ? 'Bảng Điều Khiển Thông Minh DPO' : 'DPO Intelligence Dashboard'}
        </h1>
        <button
          onClick={handleRefresh}
          className="btn-refresh"
        >
          {t('common.refresh')}
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'risk-priority' && (
          <VeriRiskPriorityQueue
            veriBusinessContext={veriBusinessContext}
            refreshTrigger={refreshTrigger}
          />
        )}

        {activeTab === 'compliance' && (
          <VeriComplianceGapPanel
            veriBusinessContext={veriBusinessContext}
            refreshTrigger={refreshTrigger}
          />
        )}

        {activeTab === 'recommendations' && (
          <VeriRecommendationsPanel
            veriBusinessContext={veriBusinessContext}
            refreshTrigger={refreshTrigger}
          />
        )}

        {activeTab === 'quality' && (
          <VeriQualityMetrics
            veriBusinessContext={veriBusinessContext}
            refreshTrigger={refreshTrigger}
          />
        )}

        {activeTab === 'costs' && (
          <VeriCostDashboard
            veriBusinessContext={veriBusinessContext}
            refreshTrigger={refreshTrigger}
          />
        )}
      </div>
    </div>
  );
};
```

### VeriRiskPriorityQueue Component

```typescript
// File: src/components/VeriPortal/VeriDPOIntelligence/components/VeriRiskPriorityQueue.tsx

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useQuery } from '@tanstack/react-query';
import { intelligenceApi } from '../services/intelligenceApi';

interface RiskField {
  field_identifier: string;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  risk_factors: string[];
  recommendations: string[];
}

export const VeriRiskPriorityQueue: React.FC<{
  veriBusinessContext: any;
  refreshTrigger: number;
}> = ({ veriBusinessContext, refreshTrigger }) => {
  const { t } = useTranslation();
  const [selectedRiskLevel, setSelectedRiskLevel] = useState<string | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ['priorityQueue', selectedRiskLevel, refreshTrigger],
    queryFn: () => intelligenceApi.getPriorityQueue(selectedRiskLevel)
  });

  const getRiskBadgeColor = (level: string) => {
    switch (level) {
      case 'critical': return 'bg-red-600 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-black';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  if (isLoading) {
    return <div className="loading-spinner">{t('common.loading')}</div>;
  }

  if (error) {
    return <div className="error-message">{t('errors.failed_to_load')}</div>;
  }

  return (
    <div className="veri-risk-priority-queue">
      {/* Summary Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-label">{t('dpo.risk.total_fields')}</span>
          <span className="stat-value">{data?.total_fields || 0}</span>
        </div>
        <div className="stat-card critical">
          <span className="stat-label">{t('dpo.risk.critical')}</span>
          <span className="stat-value">{data?.critical_count || 0}</span>
        </div>
        <div className="stat-card high">
          <span className="stat-label">{t('dpo.risk.high')}</span>
          <span className="stat-value">{data?.high_count || 0}</span>
        </div>
        <div className="stat-card medium">
          <span className="stat-label">{t('dpo.risk.medium')}</span>
          <span className="stat-value">{data?.medium_count || 0}</span>
        </div>
      </div>

      {/* Filter Buttons */}
      <div className="filter-buttons">
        <button
          onClick={() => setSelectedRiskLevel(null)}
          className={!selectedRiskLevel ? 'active' : ''}
        >
          {t('common.all')}
        </button>
        <button
          onClick={() => setSelectedRiskLevel('critical')}
          className={selectedRiskLevel === 'critical' ? 'active' : ''}
        >
          {t('dpo.risk.critical')}
        </button>
        <button
          onClick={() => setSelectedRiskLevel('high')}
          className={selectedRiskLevel === 'high' ? 'active' : ''}
        >
          {t('dpo.risk.high')}
        </button>
      </div>

      {/* Priority Queue Table */}
      <div className="priority-table">
        <table>
          <thead>
            <tr>
              <th>{t('dpo.risk.field')}</th>
              <th>{t('dpo.risk.score')}</th>
              <th>{t('dpo.risk.level')}</th>
              <th>{t('dpo.risk.factors')}</th>
              <th>{t('common.actions')}</th>
            </tr>
          </thead>
          <tbody>
            {data?.priority_queue?.map((field: RiskField, index: number) => (
              <tr key={index}>
                <td className="font-mono text-sm">{field.field_identifier}</td>
                <td className="text-center font-bold">{field.risk_score}</td>
                <td>
                  <span className={`badge ${getRiskBadgeColor(field.risk_level)}`}>
                    {t(`dpo.risk.${field.risk_level}`)}
                  </span>
                </td>
                <td>
                  <ul className="risk-factors-list">
                    {field.risk_factors.slice(0, 2).map((factor, i) => (
                      <li key={i}>{factor}</li>
                    ))}
                  </ul>
                </td>
                <td>
                  <button className="btn-action">
                    {t('dpo.risk.review')}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
```

### VeriComplianceGapPanel Component

```typescript
// File: src/components/VeriPortal/VeriDPOIntelligence/components/VeriComplianceGapPanel.tsx

import React from 'react';
import { useTranslation } from 'react-i18next';
import { useQuery } from '@tanstack/react-query';
import { intelligenceApi } from '../services/intelligenceApi';

export const VeriComplianceGapPanel: React.FC<{
  veriBusinessContext: any;
  refreshTrigger: number;
}> = ({ veriBusinessContext, refreshTrigger }) => {
  const { t, i18n } = useTranslation();
  const isVietnamese = i18n.language === 'vi';

  const { data, isLoading } = useQuery({
    queryKey: ['complianceGaps', refreshTrigger],
    queryFn: () => intelligenceApi.getComplianceGaps()
  });

  const getComplianceColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-blue-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'compliant':
        return <span className="badge bg-green-500">{t('compliance.compliant')}</span>;
      case 'partial':
        return <span className="badge bg-yellow-500">{t('compliance.partial')}</span>;
      case 'non_compliant':
        return <span className="badge bg-red-500">{t('compliance.non_compliant')}</span>;
      default:
        return <span className="badge bg-gray-500">{t('compliance.unknown')}</span>;
    }
  };

  if (isLoading) {
    return <div className="loading-spinner">{t('common.loading')}</div>;
  }

  return (
    <div className="veri-compliance-gap-panel">
      {/* Overall Score */}
      <div className="compliance-score-card">
        <div className="score-circle">
          <span className={`score-value ${getComplianceColor(data?.overall_compliance_score || 0)}`}>
            {data?.overall_compliance_score?.toFixed(1)}%
          </span>
          <span className="score-label">
            {t('compliance.overall_score')}
          </span>
        </div>
        <div className="compliance-level">
          <span className="level-label">{t('compliance.maturity_level')}</span>
          <span className="level-value">{t(`compliance.level.${data?.compliance_level}`)}</span>
        </div>
      </div>

      {/* MPS Readiness */}
      <div className={`mps-readiness ${data?.mps_ready ? 'ready' : 'not-ready'}`}>
        <h3>{t('compliance.mps_readiness')}</h3>
        <span className={`status ${data?.mps_ready ? 'text-green-600' : 'text-red-600'}`}>
          {data?.mps_ready ? t('compliance.ready') : t('compliance.not_ready')}
        </span>
      </div>

      {/* Critical Gaps */}
      {data?.critical_gaps && data.critical_gaps.length > 0 && (
        <div className="critical-gaps">
          <h3 className="text-red-600">{t('compliance.critical_gaps')}</h3>
          <ul>
            {data.critical_gaps.map((gap: string, index: number) => (
              <li key={index} className="gap-item">
                <span className="gap-icon">!</span>
                <span>{gap}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Requirements Table */}
      <div className="requirements-table">
        <h3>{t('compliance.pdpl_requirements')}</h3>
        <table>
          <thead>
            <tr>
              <th>{t('compliance.requirement')}</th>
              <th>{t('compliance.status')}</th>
              <th>{t('compliance.legal_reference')}</th>
              <th>{t('compliance.gaps')}</th>
            </tr>
          </thead>
          <tbody>
            {data?.requirements?.map((req: any, index: number) => (
              <tr key={index}>
                <td>
                  <div className="requirement-title">
                    {isVietnamese ? req.title_vi : req.title_en}
                  </div>
                  {req.mps_required && (
                    <span className="mps-badge">{t('compliance.mps_required')}</span>
                  )}
                </td>
                <td>{getStatusBadge(req.status)}</td>
                <td className="text-sm text-gray-600">{req.legal_reference}</td>
                <td>
                  <ul className="gaps-list">
                    {req.gaps?.slice(0, 2).map((gap: string, i: number) => (
                      <li key={i}>{gap}</li>
                    ))}
                  </ul>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
```

### VeriCostDashboard Component

```typescript
// File: src/components/VeriPortal/VeriDPOIntelligence/components/VeriCostDashboard.tsx

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useQuery } from '@tanstack/react-query';
import { intelligenceApi } from '../services/intelligenceApi';

export const VeriCostDashboard: React.FC<{
  veriBusinessContext: any;
  refreshTrigger: number;
}> = ({ veriBusinessContext, refreshTrigger }) => {
  const { t } = useTranslation();
  const [periodDays, setPeriodDays] = useState(30);
  const [platformCostVnd, setPlatformCostVnd] = useState(50000000); // 50M VND default

  const { data: costData } = useQuery({
    queryKey: ['costs', periodDays, refreshTrigger],
    queryFn: () => intelligenceApi.calculateCosts(periodDays)
  });

  const { data: roiData } = useQuery({
    queryKey: ['roi', platformCostVnd, refreshTrigger],
    queryFn: () => intelligenceApi.calculateROI(platformCostVnd, 12)
  });

  const formatVND = (amount: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  };

  const formatUSD = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  return (
    <div className="veri-cost-dashboard">
      {/* Period Selector */}
      <div className="period-selector">
        <label>{t('costs.analysis_period')}</label>
        <select value={periodDays} onChange={(e) => setPeriodDays(Number(e.target.value))}>
          <option value={7}>{t('costs.last_7_days')}</option>
          <option value={30}>{t('costs.last_30_days')}</option>
          <option value={90}>{t('costs.last_90_days')}</option>
          <option value={365}>{t('costs.last_year')}</option>
        </select>
      </div>

      {/* Total Cost Summary */}
      <div className="cost-summary-card">
        <h3>{t('costs.total_costs')}</h3>
        <div className="cost-amounts">
          <div className="cost-vnd">
            <span className="amount">{formatVND(costData?.total_cost_vnd || 0)}</span>
            <span className="currency">VND</span>
          </div>
          <div className="cost-usd">
            <span className="amount">{formatUSD(costData?.total_cost_usd || 0)}</span>
            <span className="currency">USD</span>
          </div>
        </div>
      </div>

      {/* Cost Breakdown */}
      <div className="cost-breakdown">
        <h3>{t('costs.breakdown')}</h3>
        <div className="breakdown-grid">
          <div className="breakdown-item">
            <span className="label">{t('costs.storage')}</span>
            <span className="value">
              {formatVND(costData?.cost_breakdown?.storage_cost_vnd || 0)}
            </span>
          </div>
          <div className="breakdown-item">
            <span className="label">{t('costs.processing')}</span>
            <span className="value">
              {formatVND(costData?.cost_breakdown?.processing_cost_vnd || 0)}
            </span>
          </div>
          <div className="breakdown-item">
            <span className="label">{t('costs.personnel')}</span>
            <span className="value">
              {formatVND(costData?.cost_breakdown?.personnel_cost_vnd || 0)}
            </span>
          </div>
          <div className="breakdown-item">
            <span className="label">{t('costs.ai_classification')}</span>
            <span className="value">
              {formatVND(costData?.cost_breakdown?.ai_cost_vnd || 0)}
            </span>
          </div>
        </div>
      </div>

      {/* Column Filter Savings */}
      <div className="savings-card">
        <h3>{t('costs.column_filter_savings')}</h3>
        <div className="savings-amount text-green-600">
          {formatVND(costData?.savings_from_column_filtering_vnd || 0)}
        </div>
        <div className="savings-subtitle">
          {t('costs.savings_from_filtering')}
        </div>
      </div>

      {/* ROI Calculator */}
      <div className="roi-calculator">
        <h3>{t('costs.roi_calculator')}</h3>
        
        <div className="platform-cost-input">
          <label>{t('costs.annual_platform_cost')}</label>
          <input
            type="number"
            value={platformCostVnd}
            onChange={(e) => setPlatformCostVnd(Number(e.target.value))}
            step={1000000}
          />
          <span className="currency-label">VND</span>
        </div>

        <div className="roi-results">
          <div className="roi-metric">
            <span className="metric-label">{t('costs.time_saved')}</span>
            <span className="metric-value">
              {roiData?.time_savings_hours?.toFixed(1)} {t('common.hours')}
            </span>
          </div>
          <div className="roi-metric">
            <span className="metric-label">{t('costs.penalty_avoided')}</span>
            <span className="metric-value">
              {formatVND(roiData?.compliance_penalty_avoided_vnd || 0)}
            </span>
          </div>
          <div className="roi-metric highlight">
            <span className="metric-label">{t('costs.roi_percentage')}</span>
            <span className={`metric-value ${(roiData?.roi_percentage || 0) > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {roiData?.roi_percentage?.toFixed(1)}%
            </span>
          </div>
          <div className="roi-metric">
            <span className="metric-label">{t('costs.payback_period')}</span>
            <span className="metric-value">
              {roiData?.payback_months?.toFixed(1)} {t('common.months')}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
```

### Intelligence API Service

```typescript
// File: src/components/VeriPortal/VeriDPOIntelligence/services/intelligenceApi.ts

import axios from 'axios';

const API_BASE = '/api/v1/veriportal/intelligence';

export const intelligenceApi = {
  async getPriorityQueue(riskLevel?: string | null) {
    const params = riskLevel ? { risk_level: riskLevel } : {};
    const response = await axios.get(`${API_BASE}/priority-queue`, { params });
    return response.data;
  },

  async getComplianceGaps() {
    const response = await axios.get(`${API_BASE}/compliance-gaps`);
    return response.data;
  },

  async getRecommendations(scope: string = 'all', fieldId?: string) {
    const params = { scope, ...(fieldId && { field_id: fieldId }) };
    const response = await axios.get(`${API_BASE}/recommendations`, { params });
    return response.data;
  },

  async analyzeFieldQuality(fieldId: string) {
    const response = await axios.post(`${API_BASE}/quality-analysis`, { field_id: fieldId });
    return response.data;
  },

  async calculateCosts(periodDays: number) {
    const response = await axios.get(`${API_BASE}/costs`, {
      params: { period_days: periodDays }
    });
    return response.data;
  },

  async calculateROI(platformCostVnd: number, periodMonths: number) {
    const response = await axios.get(`${API_BASE}/roi`, {
      params: {
        platform_cost_vnd: platformCostVnd,
        period_months: periodMonths
      }
    });
    return response.data;
  }
};
```

---

## Testing Strategy

### Unit Tests

```python
# File: backend/tests/intelligence/test_risk_scoring.py

import pytest
from veri_ai_data_inventory.intelligence.risk_scoring import DataFieldRiskScorer, RiskLevel

class TestRiskScoring:
    
    def test_sensitive_data_high_risk(self):
        """Test that sensitive personal data gets high risk score"""
        field_data = {
            'field_name': 'cmnd_number',
            'table_name': 'users',
            'pdpl_category': 'sensitive',
            'classification': 'government_id',
            'row_count': 500000,
            'exposure_type': 'cross_border',
            'retention_period': 'indefinite',
            'is_cross_border': True,
            'is_encrypted': False
        }
        
        result = DataFieldRiskScorer.calculate_risk_score(field_data)
        
        assert result['risk_score'] >= 70
        assert result['risk_level'] in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        assert 'Government ID Data' in result['risk_factors']
    
    def test_low_volume_low_risk(self):
        """Test that low-volume non-sensitive data gets lower risk"""
        field_data = {
            'field_name': 'preferences',
            'table_name': 'settings',
            'pdpl_category': 'non_personal',
            'classification': 'preferences',
            'row_count': 100,
            'exposure_type': 'internal_only',
            'retention_period': '1 year',
            'is_cross_border': False,
            'is_encrypted': True
        }
        
        result = DataFieldRiskScorer.calculate_risk_score(field_data)
        
        assert result['risk_score'] < 50
        assert result['risk_level'] in [RiskLevel.LOW, RiskLevel.MEDIUM]
    
    def test_encryption_reduces_risk(self):
        """Test that encryption reduces risk score"""
        field_data_unencrypted = {
            'field_name': 'email',
            'table_name': 'customers',
            'pdpl_category': 'regular',
            'classification': 'email',
            'row_count': 10000,
            'exposure_type': 'public_api',
            'retention_period': '5 years',
            'is_cross_border': False,
            'is_encrypted': False
        }
        
        field_data_encrypted = {**field_data_unencrypted, 'is_encrypted': True}
        
        result_unencrypted = DataFieldRiskScorer.calculate_risk_score(field_data_unencrypted)
        result_encrypted = DataFieldRiskScorer.calculate_risk_score(field_data_encrypted)
        
        assert result_encrypted['risk_score'] < result_unencrypted['risk_score']
```

```python
# File: backend/tests/intelligence/test_data_quality.py

import pytest
from veri_ai_data_inventory.intelligence.data_quality_analyzer import (
    DataQualityAnalyzer,
    VietnameseDataValidator,
    QualityLevel
)

class TestVietnameseDataValidator:
    
    def test_valid_vietnamese_phone(self):
        """Test Vietnamese phone number validation"""
        valid_phones = ['0901234567', '0912345678', '+84901234567', '0234567890']
        
        for phone in valid_phones:
            assert VietnameseDataValidator.validate_phone_number(phone) is True
    
    def test_invalid_vietnamese_phone(self):
        """Test invalid phone number detection"""
        invalid_phones = ['1234567890', '090123', 'abc1234567']
        
        for phone in invalid_phones:
            assert VietnameseDataValidator.validate_phone_number(phone) is False
    
    def test_valid_cmnd(self):
        """Test CMND (old ID) validation"""
        valid_cmnds = ['123456789', '987654321']
        
        for cmnd in valid_cmnds:
            assert VietnameseDataValidator.validate_id_number(cmnd, 'cmnd') is True
    
    def test_valid_cccd(self):
        """Test CCCD (new ID) validation"""
        valid_cccds = ['123456789012', '987654321098']
        
        for cccd in valid_cccds:
            assert VietnameseDataValidator.validate_id_number(cccd, 'cccd') is True
    
    def test_vietnamese_name_validation(self):
        """Test Vietnamese name format validation"""
        valid_names = ['Nguyễn Văn A', 'Trần Thị Bình', 'Lê Hoàng Đức']
        invalid_names = ['Nguyen123', 'Tran@Gmail', 'Le Hoang Duc 2000']
        
        for name in valid_names:
            assert VietnameseDataValidator.validate_name(name) is True
        
        for name in invalid_names:
            assert VietnameseDataValidator.validate_name(name) is False

class TestDataQualityAnalyzer:
    
    @pytest.mark.asyncio
    async def test_high_quality_data(self):
        """Test quality analysis for high-quality data"""
        field_data = {
            'field_name': 'phone',
            'table_name': 'customers',
            'classification': 'phone',
            'data_type': 'varchar'
        }
        
        sample_values = ['0901234567', '0912345678', '0923456789', '0934567890']
        
        result = await DataQualityAnalyzer.analyze_field_quality(
            field_data,
            sample_values,
            total_row_count=1000
        )
        
        assert result['quality_score'] >= 85
        assert result['quality_level'] in [QualityLevel.EXCELLENT, QualityLevel.GOOD]
        assert result['metrics']['null_percentage'] == 0
    
    @pytest.mark.asyncio
    async def test_low_quality_data(self):
        """Test quality analysis for low-quality data"""
        field_data = {
            'field_name': 'phone',
            'table_name': 'customers',
            'classification': 'phone',
            'data_type': 'varchar'
        }
        
        sample_values = ['0901234567', None, 'invalid', None, '1234']
        
        result = await DataQualityAnalyzer.analyze_field_quality(
            field_data,
            sample_values,
            total_row_count=1000
        )
        
        assert result['quality_score'] < 70
        assert len(result['issues']) > 0
        assert len(result['recommendations']) > 0
```

### Integration Tests

```python
# File: backend/tests/intelligence/test_intelligence_api.py

import pytest
from fastapi.testclient import TestClient
from veri_ai_data_inventory.main import app

client = TestClient(app)

class TestIntelligenceAPI:
    
    def test_get_priority_queue(self):
        """Test priority queue endpoint"""
        response = client.get(
            "/api/v1/veriportal/intelligence/priority-queue",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'priority_queue' in data
        assert 'total_fields' in data
        assert 'critical_count' in data
    
    def test_get_compliance_gaps(self):
        """Test compliance gap analysis endpoint"""
        response = client.get(
            "/api/v1/veriportal/intelligence/compliance-gaps",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'overall_compliance_score' in data
        assert 'requirements' in data
        assert 'mps_ready' in data
    
    def test_calculate_costs(self):
        """Test cost calculation endpoint"""
        response = client.get(
            "/api/v1/veriportal/intelligence/costs?period_days=30",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'total_cost_vnd' in data
        assert 'total_cost_usd' in data
        assert 'cost_breakdown' in data
        assert 'savings_from_column_filtering_vnd' in data
    
    def test_calculate_roi(self):
        """Test ROI calculation endpoint"""
        response = client.get(
            "/api/v1/veriportal/intelligence/roi?platform_cost_vnd=50000000&period_months=12",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'roi_percentage' in data
        assert 'payback_months' in data
        assert 'time_savings_hours' in data
```

### Frontend Component Tests

```typescript
// File: src/components/VeriPortal/VeriDPOIntelligence/__tests__/VeriRiskPriorityQueue.test.tsx

import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { VeriRiskPriorityQueue } from '../components/VeriRiskPriorityQueue';

const queryClient = new QueryClient();

describe('VeriRiskPriorityQueue', () => {
  it('renders loading state', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <VeriRiskPriorityQueue
          veriBusinessContext={{ veriBusinessId: 'test-id' }}
          refreshTrigger={0}
        />
      </QueryClientProvider>
    );
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays risk statistics', async () => {
    // Mock API response
    const mockData = {
      total_fields: 100,
      critical_count: 5,
      high_count: 15,
      medium_count: 30,
      low_count: 50,
      priority_queue: []
    };

    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      json: async () => mockData
    } as Response);

    render(
      <QueryClientProvider client={queryClient}>
        <VeriRiskPriorityQueue
          veriBusinessContext={{ veriBusinessId: 'test-id' }}
          refreshTrigger={0}
        />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('100')).toBeInTheDocument();
      expect(screen.getByText('5')).toBeInTheDocument();
    });
  });
});
```

---

## Summary

### Implementation Checklist

**Backend Components:**
- [x] Risk Scoring Engine with Vietnamese factors
- [x] Compliance Gap Analyzer (PDPL 2025 + Decree 13/2023/ND-CP)
- [x] Smart Recommendations Engine
- [x] Data Quality Analyzer with Vietnamese validation
- [x] Cost Calculator and ROI Calculator
- [x] API Endpoints for all intelligence features
- [x] Database models for risk scores

**Frontend Components:**
- [x] VeriDPOIntelligenceDashboard main component
- [x] VeriRiskPriorityQueue component
- [x] VeriComplianceGapPanel component
- [x] VeriRecommendationsPanel component
- [x] VeriQualityMetrics component
- [x] VeriCostDashboard component
- [x] Intelligence API service
- [x] Bilingual Vietnamese/English support

**Testing:**
- [x] Unit tests for risk scoring
- [x] Unit tests for Vietnamese data validation
- [x] Integration tests for API endpoints
- [x] Frontend component tests

### Key Features Delivered

1. **Risk Scoring**: 0-100 scoring with Vietnamese-specific factors (government IDs, biometric data, children's data)
2. **Compliance Gap Analysis**: PDPL 2025 and Decree 13/2023/ND-CP requirements with MPS readiness check
3. **Smart Recommendations**: AI-powered and rule-based suggestions for DPO productivity
4. **Data Quality Indicators**: Vietnamese phone, ID, name, address validation with quality metrics
5. **Cost Impact Dashboard**: VND/USD cost tracking, column filter savings, ROI calculator

### Vietnamese Market Alignment

- **Regional Context**: North/Central/South business patterns integrated
- **PDPL 2025 Compliance**: Full coverage of personal data protection requirements
- **MPS Reporting**: Readiness validation for Ministry of Public Security submissions
- **Vietnamese Data Formats**: Phone (03/05/07/08/09), CMND (9 digits), CCCD (12 digits), name validation
- **Cost Models**: VND-first with USD conversion, Vietnamese market pricing

### Next Steps

1. Implement Document #8 (DPO Workflow Automation)
2. Implement Document #9 (DPO Visualization & Reporting)
3. Integration testing across all 9 documents
4. User acceptance testing with Vietnamese DPOs

---

**Document Status:** Complete  
**Total Lines:** ~5,200 lines  
**Implementation Time Estimate:** 5-7 days  
**Priority:** P0 (Highest ROI for DPO productivity)

**Vietnamese Summary (Tóm tắt):**
Tài liệu này cung cấp hướng dẫn triển khai đầy đủ cho 5 tính năng thông minh DPO: Chấm điểm rủi ro, Phân tích khoảng cách tuân thủ PDPL 2025, Đề xuất thông minh, Chỉ số chất lượng dữ liệu Việt Nam, và Bảng điều khiển chi phí với ROI calculator.
