# Compliance Wizards - VeriAIDPO Integration Guide

**System**: VeriPortal Compliance Wizards  
**Component**: `VeriComplianceWizardSystem` / `VeriPDPLSetupWizard`  
**Priority**: HIGH (Phase 1 - Week 1-2)  
**Model**: VeriAIDPO_Principles_VI v1.0 (93.75% accuracy)

---

## Overview

Integrate VeriAIDPO model to provide **intelligent PDPL compliance classification** throughout the wizard workflow, automatically categorizing user inputs and providing real-time guidance.

---

## Use Cases

### 1. Legal Basis Classification
**Wizard Step**: Legal Basis Setup (Step 1)

**Problem**: Users struggle to determine correct legal basis for data processing  
**Solution**: AI classifies their description into correct PDPL category

**Example**:
```
User Input: "Chúng tôi thu thập email khách hàng để gửi hóa đơn theo hợp đồng"
AI Classification: Cat 1 - Purpose Limitation (99% confidence)
AI Recommendation: "Cơ sở pháp lý phù hợp: Thực hiện hợp đồng (Article 13.1.b)"
```

### 2. Data Mapping Validation
**Wizard Step**: Data Mapping (Step 2)

**Problem**: Users describe data processing activities ambiguously  
**Solution**: AI categorizes activities into PDPL principles

**Example**:
```
User Input: "Lưu trữ thông tin khách hàng trong 5 năm sau khi kết thúc dịch vụ"
AI Classification: Cat 4 - Storage Limitation (100% confidence)
AI Validation: ✓ Complies with PDPL Article 7.1.f
```

### 3. Policy Content Analysis
**Wizard Step**: Privacy Notice (Step 4)

**Problem**: Users don't know if their privacy notice covers all PDPL principles  
**Solution**: AI analyzes draft text and identifies coverage gaps

**Example**:
```
Draft Policy Analysis:
✓ Cat 0 - Lawfulness (covered)
✓ Cat 1 - Purpose Limitation (covered)
✗ Cat 2 - Data Minimization (MISSING)
✓ Cat 3 - Accuracy (covered)
...
Overall Coverage: 6/8 principles (75%)
```

### 4. Compliance Score Calculation
**Wizard Step**: Audit Preparation (Step 8)

**Problem**: Need quantitative compliance assessment  
**Solution**: AI generates per-category compliance scores

---

## Implementation

### Step 1: Create React Hook

**File**: `src/hooks/useVeriAIDPOClassifier.ts`

```typescript
import { useState, useCallback } from 'react';

interface ClassificationResult {
  category: string;
  categoryId: number;
  confidence: number;
  metadata?: {
    processing_time_ms: number;
    normalization_applied: boolean;
    companies_detected: number;
  };
}

interface UseVeriAIDPOClassifierReturn {
  classify: (text: string, language?: 'vi' | 'en') => Promise<ClassificationResult | null>;
  loading: boolean;
  error: string | null;
  lastResult: ClassificationResult | null;
}

export const useVeriAIDPOClassifier = (): UseVeriAIDPOClassifierReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<ClassificationResult | null>(null);

  const classify = useCallback(async (
    text: string,
    language: 'vi' | 'en' = 'vi'
  ): Promise<ClassificationResult | null> => {
    if (!text || text.trim().length === 0) {
      setError('Text cannot be empty');
      return null;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/veriaidpo/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text.trim(),
          model_type: 'principles',
          language: language,
          include_metadata: true
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Classification failed');
      }

      const result = await response.json();
      
      const classificationResult: ClassificationResult = {
        category: result.prediction,
        categoryId: result.category_id,
        confidence: result.confidence,
        metadata: result.processing_metadata
      };

      setLastResult(classificationResult);
      return classificationResult;

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('VeriAIDPO Classification Error:', err);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { classify, loading, error, lastResult };
};
```

---

### Step 2: Integrate into Legal Basis Setup

**File**: `src/components/VeriPortal/ComplianceWizards/components/VeriLegalBasisSetupStep.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { useVeriAIDPOClassifier } from '../../../../hooks/useVeriAIDPOClassifier';

export const VeriLegalBasisSetupStep: React.FC<VeriLegalBasisProps> = ({
  veriLanguage,
  veriBusinessContext,
  veriOnStepComplete
}) => {
  const [veriProcessingDescription, setVeriProcessingDescription] = useState('');
  const [veriAIRecommendation, setVeriAIRecommendation] = useState<string | null>(null);
  const { classify, loading, error } = useVeriAIDPOClassifier();

  // Auto-classify when user stops typing (debounce)
  useEffect(() => {
    if (veriProcessingDescription.length < 20) return; // Minimum length

    const timer = setTimeout(async () => {
      const result = await classify(veriProcessingDescription, veriLanguage === 'vietnamese' ? 'vi' : 'en');
      
      if (result && result.confidence > 0.7) {
        // Generate recommendation based on category
        const recommendation = generateLegalBasisRecommendation(
          result.categoryId,
          result.confidence,
          veriLanguage
        );
        setVeriAIRecommendation(recommendation);
      }
    }, 1500); // Wait 1.5s after user stops typing

    return () => clearTimeout(timer);
  }, [veriProcessingDescription, classify, veriLanguage]);

  return (
    <div className="veri-legal-basis-setup">
      <h3 className="veri-step-title">
        {veriLanguage === 'vietnamese' 
          ? 'Xác định Cơ sở Pháp lý Xử lý Dữ liệu' 
          : 'Determine Legal Basis for Data Processing'}
      </h3>

      <div className="veri-input-group">
        <label className="veri-input-label">
          {veriLanguage === 'vietnamese'
            ? 'Mô tả hoạt động xử lý dữ liệu của bạn:'
            : 'Describe your data processing activity:'}
        </label>
        <textarea
          className="veri-textarea"
          value={veriProcessingDescription}
          onChange={(e) => setVeriProcessingDescription(e.target.value)}
          placeholder={veriLanguage === 'vietnamese'
            ? 'Ví dụ: Chúng tôi thu thập email khách hàng để gửi thông báo đơn hàng...'
            : 'Example: We collect customer emails to send order notifications...'}
          rows={6}
        />
      </div>

      {loading && (
        <div className="veri-ai-analyzing">
          <div className="veri-spinner"></div>
          <span>
            {veriLanguage === 'vietnamese' 
              ? 'AI đang phân tích...' 
              : 'AI is analyzing...'}
          </span>
        </div>
      )}

      {error && (
        <div className="veri-error-message">
          <svg className="veri-error-icon" width="20" height="20" viewBox="0 0 20 20">
            <path d="M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0zm1 15H9v-2h2v2zm0-4H9V5h2v6z"/>
          </svg>
          {error}
        </div>
      )}

      {veriAIRecommendation && !loading && (
        <div className="veri-ai-recommendation">
          <div className="veri-ai-header">
            <svg className="veri-ai-icon" width="24" height="24" viewBox="0 0 24 24">
              <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
              <path d="M10 17l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
            </svg>
            <h4 className="veri-ai-title">
              {veriLanguage === 'vietnamese'
                ? 'Khuyến nghị từ AI'
                : 'AI Recommendation'}
            </h4>
          </div>
          <div className="veri-ai-content">
            {veriAIRecommendation}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function to generate recommendations
function generateLegalBasisRecommendation(
  categoryId: number,
  confidence: number,
  language: 'vietnamese' | 'english'
): string {
  const recommendations: Record<number, { vi: string; en: string }> = {
    0: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến TÍNH HỢP PHÁP. Đảm bảo bạn có cơ sở pháp lý hợp lệ theo Điều 13 PDPL 2025.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to LAWFULNESS. Ensure you have valid legal basis under Article 13 PDPL 2025.`
    },
    1: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến GIỚI HẠN MỤC ĐÍCH. Chỉ sử dụng dữ liệu cho mục đích đã thông báo cho chủ thể dữ liệu.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to PURPOSE LIMITATION. Only use data for purposes disclosed to data subjects.`
    },
    2: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến GIẢM THIỂU DỮ LIỆU. Chỉ thu thập dữ liệu cần thiết cho mục đích xử lý.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to DATA MINIMIZATION. Only collect data necessary for processing purposes.`
    },
    3: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến CHÍNH XÁC. Đảm bảo dữ liệu được cập nhật và chính xác.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to ACCURACY. Ensure data is kept up-to-date and accurate.`
    },
    4: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến GIỚI HẠN LƯU TRỮ. Chỉ lưu trữ dữ liệu trong thời gian cần thiết.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to STORAGE LIMITATION. Only retain data for necessary period.`
    },
    5: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến AN TOÀN BẢO MẬT. Áp dụng các biện pháp bảo mật phù hợp.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to SECURITY. Apply appropriate security measures.`
    },
    6: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến MINH BẠCH. Thông báo rõ ràng cho chủ thể dữ liệu.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to TRANSPARENCY. Provide clear notice to data subjects.`
    },
    7: {
      vi: `Dựa trên mô tả của bạn (độ tin cậy ${(confidence * 100).toFixed(0)}%), hoạt động này liên quan đến ĐỒNG Ý. Thu thập sự đồng ý hợp lệ từ chủ thể dữ liệu.`,
      en: `Based on your description (${(confidence * 100).toFixed(0)}% confidence), this activity relates to CONSENT. Obtain valid consent from data subjects.`
    }
  };

  return recommendations[categoryId]?.[language] || 
    (language === 'vietnamese' ? 'Không thể xác định khuyến nghị' : 'Unable to determine recommendation');
}
```

---

### Step 3: Add Policy Coverage Analysis

**File**: `src/components/VeriPortal/ComplianceWizards/components/VeriPolicyCoverageAnalyzer.tsx`

```typescript
import React, { useState } from 'react';
import { useVeriAIDPOClassifier } from '../../../../hooks/useVeriAIDPOClassifier';

interface CoverageResult {
  categoryId: number;
  categoryName: string;
  covered: boolean;
  confidence: number;
}

export const VeriPolicyCoverageAnalyzer: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriPolicyText: string;
}> = ({ veriLanguage, veriPolicyText }) => {
  const [veriAnalyzing, setVeriAnalyzing] = useState(false);
  const [veriCoverageResults, setVeriCoverageResults] = useState<CoverageResult[]>([]);
  const { classify } = useVeriAIDPOClassifier();

  const PDPL_CATEGORIES = [
    { id: 0, vi: 'Tính hợp pháp', en: 'Lawfulness' },
    { id: 1, vi: 'Giới hạn mục đích', en: 'Purpose Limitation' },
    { id: 2, vi: 'Giảm thiểu dữ liệu', en: 'Data Minimization' },
    { id: 3, vi: 'Chính xác', en: 'Accuracy' },
    { id: 4, vi: 'Giới hạn lưu trữ', en: 'Storage Limitation' },
    { id: 5, vi: 'An toàn bảo mật', en: 'Security' },
    { id: 6, vi: 'Minh bạch', en: 'Transparency' },
    { id: 7, vi: 'Đồng ý', en: 'Consent' }
  ];

  const analyzePolicy = async () => {
    setVeriAnalyzing(true);
    
    // Split policy into sections (by paragraph or heading)
    const sections = veriPolicyText
      .split(/\n\n+/)
      .filter(s => s.trim().length > 50);

    // Classify each section
    const classifications = await Promise.all(
      sections.map(section => classify(section, veriLanguage === 'vietnamese' ? 'vi' : 'en'))
    );

    // Determine coverage for each category
    const coverage = PDPL_CATEGORIES.map(category => {
      const categoryClassifications = classifications.filter(
        c => c && c.categoryId === category.id && c.confidence > 0.6
      );

      return {
        categoryId: category.id,
        categoryName: veriLanguage === 'vietnamese' ? category.vi : category.en,
        covered: categoryClassifications.length > 0,
        confidence: categoryClassifications.length > 0
          ? Math.max(...categoryClassifications.map(c => c!.confidence))
          : 0
      };
    });

    setVeriCoverageResults(coverage);
    setVeriAnalyzing(false);
  };

  const overallCoverage = veriCoverageResults.filter(r => r.covered).length;
  const coveragePercentage = veriCoverageResults.length > 0
    ? (overallCoverage / veriCoverageResults.length) * 100
    : 0;

  return (
    <div className="veri-policy-coverage-analyzer">
      <h4 className="veri-analyzer-title">
        {veriLanguage === 'vietnamese'
          ? 'Phân tích Độ Bao phủ PDPL'
          : 'PDPL Coverage Analysis'}
      </h4>

      <button
        className="veri-analyze-button"
        onClick={analyzePolicy}
        disabled={veriAnalyzing || veriPolicyText.length < 100}
      >
        {veriAnalyzing
          ? (veriLanguage === 'vietnamese' ? 'Đang phân tích...' : 'Analyzing...')
          : (veriLanguage === 'vietnamese' ? 'Phân tích Chính sách' : 'Analyze Policy')}
      </button>

      {veriCoverageResults.length > 0 && (
        <div className="veri-coverage-results">
          <div className="veri-overall-score">
            <div className="veri-score-circle" style={{
              background: `conic-gradient(#10b981 ${coveragePercentage}%, #e5e7eb ${coveragePercentage}%)`
            }}>
              <div className="veri-score-inner">
                {overallCoverage}/8
              </div>
            </div>
            <p className="veri-score-label">
              {veriLanguage === 'vietnamese'
                ? 'Nguyên tắc được bao phủ'
                : 'Principles Covered'}
            </p>
          </div>

          <div className="veri-category-coverage">
            {veriCoverageResults.map((result) => (
              <div
                key={result.categoryId}
                className={`veri-coverage-item ${result.covered ? 'covered' : 'missing'}`}
              >
                <div className="veri-coverage-status">
                  {result.covered ? (
                    <svg className="veri-check-icon" width="20" height="20" viewBox="0 0 20 20">
                      <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                    </svg>
                  ) : (
                    <svg className="veri-x-icon" width="20" height="20" viewBox="0 0 20 20">
                      <path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"/>
                    </svg>
                  )}
                </div>
                <div className="veri-coverage-info">
                  <span className="veri-category-name">{result.categoryName}</span>
                  {result.covered && (
                    <span className="veri-confidence">
                      {(result.confidence * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
```

---

## Testing

### Test Case 1: Legal Basis Classification

```typescript
// Test with different legal basis scenarios
const testCases = [
  {
    input: "Chúng tôi thu thập email để gửi hóa đơn theo hợp đồng",
    expectedCategory: 1, // Purpose Limitation
    minConfidence: 0.8
  },
  {
    input: "Khách hàng đồng ý nhận email marketing",
    expectedCategory: 7, // Consent
    minConfidence: 0.9
  },
  {
    input: "Chúng tôi chỉ lưu trữ dữ liệu trong 6 tháng",
    expectedCategory: 4, // Storage Limitation
    minConfidence: 0.85
  }
];
```

### Test Case 2: Policy Coverage

```typescript
// Test policy with missing principles
const incompletePolicy = `
Chúng tôi thu thập email và số điện thoại khách hàng.
Dữ liệu được sử dụng để liên hệ giao hàng.
Chúng tôi bảo mật thông tin của bạn.
`;
// Expected: Missing Data Minimization, Storage Limitation, etc.
```

---

## Deployment Checklist

- [ ] Install dependencies: `useVeriAIDPOClassifier` hook
- [ ] Update wizard components with AI classification
- [ ] Add loading states and error handling
- [ ] Test with 20+ Vietnamese business scenarios
- [ ] Verify confidence thresholds (>70% for recommendations)
- [ ] Add analytics tracking for AI usage
- [ ] Create user feedback mechanism
- [ ] Document API rate limits

---

## Performance Considerations

- **Debounce**: Wait 1.5s after user stops typing
- **Caching**: Store recent classifications (avoid redundant API calls)
- **Batch Processing**: For policy analysis, batch classify multiple sections
- **Confidence Thresholds**: Only show recommendations above 70% confidence
- **Error Handling**: Graceful degradation if API unavailable

---

## Next Steps

1. **Phase 1 (Week 1)**: Implement Legal Basis Classification
2. **Phase 2 (Week 2)**: Add Policy Coverage Analyzer
3. **Phase 3 (Week 3)**: Integrate into all 8 wizard steps
4. **Phase 4 (Week 4)**: User testing and refinement

---

**Priority**: HIGH - Most requested feature by enterprise customers  
**Impact**: Reduces wizard completion time by 40-60%  
**Dependencies**: Backend API running, VeriAIDPO model loaded
