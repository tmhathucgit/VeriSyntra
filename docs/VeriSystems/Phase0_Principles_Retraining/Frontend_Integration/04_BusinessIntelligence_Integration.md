# Business Intelligence - VeriAIDPO Integration Guide

**System**: VeriPortal Business Intelligence  
**Component**: `VeriBusinessIntelligenceSystem`  
**Priority**: MEDIUM (Phase 2 - Week 3-4)  
**Model**: VeriAIDPO_Principles_VI v1.0 (93.75% accuracy)

---

## Overview

Integrate VeriAIDPO model to provide **intelligent compliance gap analysis**, **risk assessment**, **predictive analytics**, and **automated MPS reporting** for Vietnamese enterprises.

---

## Use Cases

### 1. Compliance Gap Analysis
**Context**: Enterprise compliance audit

**Problem**: Need to identify which PDPL principles are poorly implemented  
**Solution**: AI analyzes all compliance documents and identifies gaps

**Example**:
```
Company: VNG Corporation
Documents Analyzed: 47 policies, 120 procedures, 8 contracts

AI Gap Analysis:
  Cat 0 (Lawfulness): 95% coverage [OK]
    - 42 documents reference legal basis
    - DPA contracts in place
  
  Cat 1 (Purpose): 88% coverage [OK]
    - All data collection has stated purposes
  
  Cat 2 (Minimization): 45% coverage [WARNING]
    - Only 21/47 policies mention minimization
    - Marketing DB collects unnecessary fields
    - RECOMMENDATION: Audit marketing database
  
  Cat 4 (Storage): 38% coverage [CRITICAL]
    - No retention schedules found
    - 15/47 policies missing deletion procedures
    - RECOMMENDATION: Create retention policy URGENTLY
  
Overall Compliance Score: 72/100 (Needs Improvement)
Priority Action: Address Cat 4 (Storage Limitation)
```

### 2. Risk Assessment by Business Unit
**Context**: Quarterly risk review

**Problem**: Which departments have highest PDPL compliance risk?  
**Solution**: AI analyzes department-level compliance and calculates risk scores

**Example**:
```
Q4 2025 Risk Assessment:

High Risk Departments:
  1. Marketing (Risk Score: 78/100)
     - Weak: Cat 7 (Consent) - 45% compliance
     - Issue: Email campaigns without proper consent records
     - Impact: Potential MPS fine up to 5% revenue
     - Action: Implement consent management platform
  
  2. HR (Risk Score: 65/100)
     - Weak: Cat 4 (Storage) - 38% compliance
     - Issue: Employee records retained indefinitely
     - Impact: PDPL Article 7.1.f violation
     - Action: Create employee data retention schedule

Medium Risk Departments:
  3. Sales (Risk Score: 52/100)
     - Weak: Cat 2 (Minimization) - 58% compliance
  
  4. IT (Risk Score: 48/100)
     - Generally compliant, minor gaps in Cat 6 (Transparency)

Low Risk Departments:
  5. Finance (Risk Score: 25/100) - Strong compliance
  6. Legal (Risk Score: 18/100) - Strong compliance
```

### 3. Predictive Compliance Trends
**Context**: Executive dashboard

**Problem**: Will we pass MPS audit next quarter?  
**Solution**: AI predicts future compliance based on current trajectory

**Example**:
```
Compliance Trend Forecast (Next 6 Months):

Current Overall Score: 72/100

Predicted Score (6 months):
  - Best Case: 85/100 (if all recommendations implemented)
  - Most Likely: 76/100 (current improvement rate)
  - Worst Case: 68/100 (if no action taken)

Critical Predictions:
  ✓ Cat 0 (Lawfulness): Will improve to 98% (DPA renewal scheduled)
  ✓ Cat 1 (Purpose): Stable at 88% (good baseline)
  ✗ Cat 4 (Storage): Will decline to 32% if no action
     ALERT: MPS audit risk increases 45% in Q1 2026

Recommended Actions to Achieve 85% Target:
  1. [URGENT] Implement retention policy (Cat 4) - Est. +12 points
  2. [HIGH] Audit marketing consents (Cat 7) - Est. +8 points
  3. [MEDIUM] Review data collection forms (Cat 2) - Est. +5 points
```

### 4. Automated MPS Report Generation
**Context**: Quarterly MPS compliance report due

**Problem**: Manual report compilation takes 40+ hours  
**Solution**: AI auto-generates structured report from system data

**Example**:
```
MPS Quarterly Compliance Report - Q4 2025
Generated: 2025-10-19 14:30

Executive Summary:
  Overall Compliance: 72/100 (Adequate)
  Risk Level: MEDIUM
  Critical Issues: 2 (Cat 4, Cat 7)
  
Section 1: PDPL Principle Implementation
  [AI analyzes all 8 principles with supporting evidence]
  
  Cat 0 - Lawfulness (95% compliant):
    Evidence:
      - 42/47 policies reference legal basis
      - 8 DPA contracts with processors
      - Lawful basis register maintained
    Supporting Documents:
      - doc_001_legal_basis_register.pdf
      - doc_002_dpa_vendor_a.pdf
      ...
  
  Cat 4 - Storage Limitation (38% compliant) [CRITICAL]:
    Gaps Identified:
      - No enterprise-wide retention schedule
      - 15/47 policies missing deletion procedures
      - Marketing DB retains data >5 years without justification
    Remediation Plan:
      - Action 1: Create retention policy (Target: Q1 2026)
      - Action 2: Implement automated deletion (Target: Q2 2026)

Section 2: Data Breach Incidents
  [Pulled from VeriBreachTriage system]
  
Section 3: Training Completion
  [Pulled from VeriTraining system]
  
Attestation:
  I hereby certify this report accurately reflects our compliance status.
  
  Signature: _____________________
  Name: Nguyễn Văn A (DPO)
  Date: 2025-10-19
```

---

## Implementation

### Step 1: Compliance Gap Analyzer

**File**: `src/components/VeriPortal/BusinessIntelligence/components/VeriComplianceGapAnalyzer.tsx`

```typescript
import React, { useState } from 'react';
import { useVeriAIDPOClassifier } from '../../../../hooks/useVeriAIDPOClassifier';

interface ComplianceDocument {
  veriDocumentId: string;
  veriDocumentName: string;
  veriDocumentType: 'policy' | 'procedure' | 'contract' | 'notice';
  veriContent: string;
  veriDepartment?: string;
}

interface PrincipleGap {
  veriPrinciple: number;
  veriPrincipleName: string;
  veriCoverageScore: number; // 0-100
  veriDocumentCount: number;
  veriStatus: 'excellent' | 'good' | 'warning' | 'critical';
  veriRecommendations: string[];
  veriSupportingDocs: string[];
}

export const VeriComplianceGapAnalyzer: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext: VeriBusinessContext;
  veriDocuments: ComplianceDocument[];
}> = ({ veriLanguage, veriBusinessContext, veriDocuments }) => {
  const [veriAnalyzing, setVeriAnalyzing] = useState(false);
  const [veriGapReport, setVeriGapReport] = useState<PrincipleGap[]>([]);
  const { classify } = useVeriAIDPOClassifier();

  const analyzeComplianceGaps = async () => {
    setVeriAnalyzing(true);

    // Initialize principle tracking
    const principleTracker: Record<number, {
      documents: string[];
      totalConfidence: number;
      count: number;
    }> = {};

    for (let i = 0; i < 8; i++) {
      principleTracker[i] = { documents: [], totalConfidence: 0, count: 0 };
    }

    // Analyze each document
    for (const doc of veriDocuments) {
      if (doc.veriContent.length < 100) continue;

      // Split long documents into sections
      const sections = splitIntoSections(doc.veriContent, 512);

      for (const section of sections) {
        const result = await classify(
          section,
          veriLanguage === 'vietnamese' ? 'vi' : 'en'
        );

        if (result && result.confidence > 0.6) {
          const principle = result.categoryId;
          
          if (!principleTracker[principle].documents.includes(doc.veriDocumentId)) {
            principleTracker[principle].documents.push(doc.veriDocumentId);
          }
          
          principleTracker[principle].totalConfidence += result.confidence;
          principleTracker[principle].count++;
        }
      }
    }

    // Calculate gaps
    const gaps: PrincipleGap[] = [];
    const principleNames: Record<number, { vi: string; en: string }> = {
      0: { vi: 'Tính hợp pháp', en: 'Lawfulness' },
      1: { vi: 'Giới hạn mục đích', en: 'Purpose Limitation' },
      2: { vi: 'Giảm thiểu dữ liệu', en: 'Data Minimization' },
      3: { vi: 'Chính xác', en: 'Accuracy' },
      4: { vi: 'Giới hạn lưu trữ', en: 'Storage Limitation' },
      5: { vi: 'An toàn bảo mật', en: 'Security' },
      6: { vi: 'Minh bạch', en: 'Transparency' },
      7: { vi: 'Đồng ý', en: 'Consent' }
    };

    for (let i = 0; i < 8; i++) {
      const tracker = principleTracker[i];
      const documentCoverage = (tracker.documents.length / veriDocuments.length) * 100;
      const avgConfidence = tracker.count > 0 
        ? (tracker.totalConfidence / tracker.count) * 100 
        : 0;
      
      // Combined score: 60% document coverage + 40% confidence
      const coverageScore = (documentCoverage * 0.6) + (avgConfidence * 0.4);

      let status: 'excellent' | 'good' | 'warning' | 'critical';
      if (coverageScore >= 85) status = 'excellent';
      else if (coverageScore >= 70) status = 'good';
      else if (coverageScore >= 50) status = 'warning';
      else status = 'critical';

      gaps.push({
        veriPrinciple: i,
        veriPrincipleName: principleNames[i][veriLanguage],
        veriCoverageScore: coverageScore,
        veriDocumentCount: tracker.documents.length,
        veriStatus: status,
        veriRecommendations: generateGapRecommendations(
          i,
          status,
          veriLanguage,
          veriBusinessContext
        ),
        veriSupportingDocs: tracker.documents.slice(0, 5) // Top 5 docs
      });
    }

    // Sort by coverage (worst first)
    gaps.sort((a, b) => a.veriCoverageScore - b.veriCoverageScore);

    setVeriGapReport(gaps);
    setVeriAnalyzing(false);
  };

  const overallScore = veriGapReport.length > 0
    ? veriGapReport.reduce((sum, gap) => sum + gap.veriCoverageScore, 0) / 8
    : 0;

  return (
    <div className="veri-compliance-gap-analyzer">
      <div className="veri-analyzer-header">
        <h2 className="veri-analyzer-title">
          {veriLanguage === 'vietnamese'
            ? 'Phân tích Khoảng Cách Tuân thủ PDPL'
            : 'PDPL Compliance Gap Analysis'}
        </h2>
        <button
          className="veri-analyze-button"
          onClick={analyzeComplianceGaps}
          disabled={veriAnalyzing || veriDocuments.length === 0}
        >
          {veriAnalyzing
            ? (veriLanguage === 'vietnamese' 
                ? `Đang phân tích ${veriDocuments.length} tài liệu...` 
                : `Analyzing ${veriDocuments.length} documents...`)
            : (veriLanguage === 'vietnamese' 
                ? 'Phân tích Độ Tuân thủ' 
                : 'Analyze Compliance')}
        </button>
      </div>

      {veriGapReport.length > 0 && (
        <>
          {/* Overall Score Dashboard */}
          <div className="veri-overall-dashboard">
            <div className="veri-score-card veri-main">
              <h3 className="veri-score-label">
                {veriLanguage === 'vietnamese' ? 'Điểm Tuân thủ Tổng thể' : 'Overall Compliance Score'}
              </h3>
              <div className="veri-score-value" style={{
                color: overallScore >= 85 ? '#10b981' : 
                       overallScore >= 70 ? '#3b82f6' : 
                       overallScore >= 50 ? '#f59e0b' : '#ef4444'
              }}>
                {overallScore.toFixed(0)}/100
              </div>
              <p className="veri-score-description">
                {overallScore >= 85 
                  ? (veriLanguage === 'vietnamese' ? 'Xuất sắc' : 'Excellent')
                  : overallScore >= 70
                  ? (veriLanguage === 'vietnamese' ? 'Tốt' : 'Good')
                  : overallScore >= 50
                  ? (veriLanguage === 'vietnamese' ? 'Cần Cải thiện' : 'Needs Improvement')
                  : (veriLanguage === 'vietnamese' ? 'Nghiêm trọng' : 'Critical')}
              </p>
            </div>

            <div className="veri-score-card">
              <h3 className="veri-score-label">
                {veriLanguage === 'vietnamese' ? 'Tài liệu Phân tích' : 'Documents Analyzed'}
              </h3>
              <div className="veri-score-value">{veriDocuments.length}</div>
            </div>

            <div className="veri-score-card">
              <h3 className="veri-score-label">
                {veriLanguage === 'vietnamese' ? 'Vấn đề Nghiêm trọng' : 'Critical Issues'}
              </h3>
              <div className="veri-score-value" style={{ color: '#ef4444' }}>
                {veriGapReport.filter(g => g.veriStatus === 'critical').length}
              </div>
            </div>

            <div className="veri-score-card">
              <h3 className="veri-score-label">
                {veriLanguage === 'vietnamese' ? 'Cảnh báo' : 'Warnings'}
              </h3>
              <div className="veri-score-value" style={{ color: '#f59e0b' }}>
                {veriGapReport.filter(g => g.veriStatus === 'warning').length}
              </div>
            </div>
          </div>

          {/* Principle-by-Principle Breakdown */}
          <div className="veri-gap-breakdown">
            <h3 className="veri-breakdown-title">
              {veriLanguage === 'vietnamese' 
                ? 'Chi tiết theo Nguyên tắc PDPL' 
                : 'Breakdown by PDPL Principle'}
            </h3>
            
            {veriGapReport.map((gap) => (
              <div key={gap.veriPrinciple} className={`veri-gap-card veri-${gap.veriStatus}`}>
                <div className="veri-gap-header">
                  <div className="veri-gap-info">
                    <h4 className="veri-principle-name">{gap.veriPrincipleName}</h4>
                    <span className="veri-doc-count">
                      {gap.veriDocumentCount}/{veriDocuments.length} {veriLanguage === 'vietnamese' ? 'tài liệu' : 'documents'}
                    </span>
                  </div>
                  <div className="veri-gap-score">
                    <span className="veri-score-number">{gap.veriCoverageScore.toFixed(0)}</span>
                    <span className="veri-score-max">/100</span>
                  </div>
                </div>

                <div className="veri-gap-progress">
                  <div 
                    className="veri-gap-progress-bar"
                    style={{ 
                      width: `${gap.veriCoverageScore}%`,
                      backgroundColor: gap.veriStatus === 'excellent' ? '#10b981' :
                                      gap.veriStatus === 'good' ? '#3b82f6' :
                                      gap.veriStatus === 'warning' ? '#f59e0b' : '#ef4444'
                    }}
                  />
                </div>

                {gap.veriRecommendations.length > 0 && (
                  <div className="veri-gap-recommendations">
                    <h5 className="veri-recommendations-title">
                      {veriLanguage === 'vietnamese' ? 'Khuyến nghị Hành động:' : 'Action Recommendations:'}
                    </h5>
                    <ul className="veri-recommendations-list">
                      {gap.veriRecommendations.map((rec, i) => (
                        <li key={i}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {gap.veriSupportingDocs.length > 0 && (
                  <div className="veri-supporting-docs">
                    <button 
                      className="veri-toggle-docs"
                      onClick={() => {/* Toggle document list */}}
                    >
                      {veriLanguage === 'vietnamese' 
                        ? `Xem ${gap.veriSupportingDocs.length} tài liệu liên quan` 
                        : `View ${gap.veriSupportingDocs.length} related documents`}
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Export Report */}
          <div className="veri-export-actions">
            <button className="veri-export-button veri-export-pdf">
              {veriLanguage === 'vietnamese' ? 'Xuất Báo cáo PDF' : 'Export PDF Report'}
            </button>
            <button className="veri-export-button veri-export-mps">
              {veriLanguage === 'vietnamese' ? 'Tạo Báo cáo MPS' : 'Generate MPS Report'}
            </button>
          </div>
        </>
      )}
    </div>
  );
};

// Helper functions
function splitIntoSections(text: string, maxLength: number): string[] {
  const sections: string[] = [];
  let currentSection = '';
  
  const sentences = text.split(/[.!?]\s+/);
  
  for (const sentence of sentences) {
    if ((currentSection + sentence).length > maxLength) {
      if (currentSection) sections.push(currentSection);
      currentSection = sentence;
    } else {
      currentSection += (currentSection ? '. ' : '') + sentence;
    }
  }
  
  if (currentSection) sections.push(currentSection);
  
  return sections;
}

function generateGapRecommendations(
  principle: number,
  status: string,
  language: 'vietnamese' | 'english',
  context: VeriBusinessContext
): string[] {
  if (status === 'excellent') return [];

  const recommendations: Record<number, { vi: string[]; en: string[] }> = {
    0: {
      vi: [
        'Tạo Legal Basis Register cho tất cả hoạt động xử lý dữ liệu',
        'Ký kết Data Processing Agreement (DPA) với các đối tác',
        'Xem xét cơ sở pháp lý cho từng mục đích xử lý'
      ],
      en: [
        'Create Legal Basis Register for all data processing activities',
        'Sign Data Processing Agreements (DPA) with partners',
        'Review legal basis for each processing purpose'
      ]
    },
    1: {
      vi: [
        'Ghi rõ mục đích xử lý trong tất cả Privacy Notice',
        'Đảm bảo không sử dụng dữ liệu ngoài mục đích đã thông báo',
        'Tạo danh sách mục đích được phép cho từng loại dữ liệu'
      ],
      en: [
        'Clearly state processing purposes in all Privacy Notices',
        'Ensure data not used beyond stated purposes',
        'Create list of permitted purposes for each data type'
      ]
    },
    2: {
      vi: [
        '[URGENT] Kiểm tra database Marketing - xóa dữ liệu không cần thiết',
        'Phân loại dữ liệu: "Bắt buộc" vs "Tùy chọn"',
        'Xem xét tất cả form thu thập dữ liệu'
      ],
      en: [
        '[URGENT] Audit Marketing database - delete unnecessary data',
        'Classify data: "Required" vs "Optional"',
        'Review all data collection forms'
      ]
    },
    3: {
      vi: [
        'Thiết lập quy trình cập nhật dữ liệu định kỳ',
        'Cho phép khách hàng tự cập nhật thông tin',
        'Xác minh độ chính xác dữ liệu quan trọng'
      ],
      en: [
        'Establish periodic data update procedures',
        'Allow customers to self-update information',
        'Verify accuracy of critical data'
      ]
    },
    4: {
      vi: [
        '[CRITICAL] Tạo Retention Schedule ngay lập tức',
        'Thiết lập quy trình xóa dữ liệu tự động',
        'Ghi rõ thời hạn lưu trữ trong Privacy Policy'
      ],
      en: [
        '[CRITICAL] Create Retention Schedule immediately',
        'Implement automated data deletion procedures',
        'Specify retention periods in Privacy Policy'
      ]
    },
    5: {
      vi: [
        'Tăng cường mã hóa dữ liệu nhạy cảm',
        'Kiểm soát quyền truy cập theo vai trò (RBAC)',
        'Thực hiện đánh giá rủi ro bảo mật định kỳ'
      ],
      en: [
        'Strengthen encryption for sensitive data',
        'Implement role-based access control (RBAC)',
        'Conduct periodic security risk assessments'
      ]
    },
    6: {
      vi: [
        'Viết lại Privacy Notice dễ hiểu hơn',
        'Thông báo rõ ràng về quyền của chủ thể dữ liệu',
        'Tạo FAQ về xử lý dữ liệu cá nhân'
      ],
      en: [
        'Rewrite Privacy Notice for clarity',
        'Clearly communicate data subject rights',
        'Create FAQ about personal data processing'
      ]
    },
    7: {
      vi: [
        '[HIGH PRIORITY] Triển khai Consent Management Platform',
        'Kiểm tra tất cả email marketing campaigns',
        'Tạo biểu mẫu đồng ý rõ ràng và tách biệt'
      ],
      en: [
        '[HIGH PRIORITY] Deploy Consent Management Platform',
        'Audit all email marketing campaigns',
        'Create clear and separate consent forms'
      ]
    }
  };

  // Industry-specific recommendations
  if (context.veriIndustryType === 'finance' && principle === 5) {
    recommendations[5].vi.unshift('Tuân thủ Circular 44/2018/TT-NHNN về bảo mật ngân hàng');
    recommendations[5].en.unshift('Comply with Circular 44/2018/TT-NHNN on banking security');
  }

  return recommendations[principle]?.[language] || [];
}
```

---

## Testing

### Test Case 1: Gap Analysis Accuracy

```typescript
const testDocuments = [
  {
    name: "Privacy Policy v1.0",
    content: "Chúng tôi chỉ sử dụng dữ liệu cho mục đích giao hàng...", // Cat 1
    expectedPrinciples: [1, 6]
  },
  {
    name: "DPA with Vendor A",
    content: "Căn cứ hợp đồng, đối tác chỉ xử lý dữ liệu theo chỉ đạo...", // Cat 0
    expectedPrinciples: [0, 1]
  }
];
// Expected: Strong Cat 0, Cat 1; Weak Cat 4, Cat 7
```

---

## Deployment Checklist

- [ ] Implement compliance gap analyzer
- [ ] Implement risk assessment dashboard
- [ ] Implement MPS report generator
- [ ] Create executive dashboard
- [ ] Test with real enterprise compliance data
- [ ] Add trend prediction algorithms
- [ ] Integrate with document management system
- [ ] Create automated alerting for critical gaps

---

## Next Steps

1. **Week 3**: Implement gap analyzer
2. **Week 4**: Implement risk dashboard
3. **Week 5**: Add predictive analytics
4. **Week 6**: MPS report automation

---

**Priority**: MEDIUM - High executive value  
**Impact**: Reduces audit preparation time from 40+ hours to 2 hours  
**Dependencies**: VeriAIDPO model, document database, compliance tracking system
