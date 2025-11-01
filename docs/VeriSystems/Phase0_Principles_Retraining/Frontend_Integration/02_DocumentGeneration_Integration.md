# Document Generation - VeriAIDPO Integration Guide

**System**: VeriPortal Document Generation  
**Component**: `VeriDocumentGenerationSystem`  
**Priority**: HIGH (Phase 1 - Week 1-2)  
**Model**: VeriAIDPO_Principles_VI v1.0 (93.75% accuracy)

---

## Overview

Integrate VeriAIDPO model to provide **intelligent document template selection** and **automated content validation** for Vietnamese PDPL compliance documents.

---

## Use Cases

### 1. Automatic Template Selection
**Context**: User starts document generation

**Problem**: 100+ templates, users don't know which one matches their needs  
**Solution**: AI analyzes user's brief description and recommends templates

**Example**:
```
User Input: "Tôi cần tạo thông báo cho khách hàng về việc thu thập dữ liệu khi đăng ký"
AI Analysis:
  - Primary Principle: Cat 6 - Transparency (95% confidence)
  - Secondary: Cat 7 - Consent (87% confidence)
Recommended Templates:
  1. "Thông báo Thu thập Dữ liệu Cá nhân" (Transparency-focused)
  2. "Mẫu Đồng ý Thu thập và Xử lý Dữ liệu" (Consent-focused)
  3. "Chính sách Bảo mật Dữ liệu Khách hàng" (General)
```

### 2. Content Validation
**Context**: User drafts document content

**Problem**: Documents missing required PDPL principle coverage  
**Solution**: AI validates each section against PDPL requirements

**Example**:
```
Document: Privacy Notice
Sections Analyzed:
  [OK] Section 1 "Mục đích thu thập" - Cat 1 (Purpose Limitation) 98%
  [OK] Section 2 "Phạm vi sử dụng" - Cat 2 (Data Minimization) 92%
  [WARNING] Section 3 "Bảo mật" - Low confidence (45%)
  [MISSING] Storage Limitation not addressed
  
Coverage Score: 6/8 principles (75%)
```

### 3. Smart Content Suggestions
**Context**: User writes document section

**Problem**: Users don't know what content to include  
**Solution**: AI suggests content based on detected principle

**Example**:
```
User Section: "2. Dữ liệu chúng tôi thu thập"
AI Detection: Cat 2 - Data Minimization (89% confidence)
AI Suggestion:
  "Khuyến nghị bổ sung: Làm rõ dữ liệu nào là 'cần thiết' và 'tùy chọn'.
   Ví dụ: Email (bắt buộc), Số điện thoại (tùy chọn)."
```

### 4. Regional Adaptation
**Context**: Document for specific Vietnamese region

**Problem**: North/South communication styles differ  
**Solution**: AI adapts document tone based on region

**Example**:
```
User Context: South Vietnam (HCMC), Technology Startup
AI Tone Adjustment:
  - More casual, friendly language
  - Shorter sentences
  - Modern terminology
  
Original: "Công ty cam kết bảo mật thông tin theo quy định pháp luật."
Adapted: "Chúng mình sẽ bảo vệ thông tin của bạn cẩn thận nhé!"
```

---

## Implementation

### Step 1: Template Recommendation Engine

**File**: `src/components/VeriPortal/DocumentGeneration/components/VeriTemplateRecommender.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { useVeriAIDPOClassifier } from '../../../../hooks/useVeriAIDPOClassifier';

interface VeriDocumentTemplate {
  veriTemplateId: string;
  veriTemplateName: string;
  veriPrimaryPrinciple: number; // PDPL category ID
  veriSecondaryPrinciples: number[];
  veriDescription: string;
  veriRegionalVariant?: 'north' | 'central' | 'south';
}

export const VeriTemplateRecommender: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriBusinessContext: VeriBusinessContext;
  veriOnTemplateSelect: (template: VeriDocumentTemplate) => void;
}> = ({ veriLanguage, veriBusinessContext, veriOnTemplateSelect }) => {
  const [veriUserIntent, setVeriUserIntent] = useState('');
  const [veriRecommendedTemplates, setVeriRecommendedTemplates] = useState<VeriDocumentTemplate[]>([]);
  const { classify, loading } = useVeriAIDPOClassifier();

  // All available templates (would come from API in production)
  const ALL_TEMPLATES: VeriDocumentTemplate[] = [
    {
      veriTemplateId: 'tmpl-001',
      veriTemplateName: 'Thông báo Thu thập Dữ liệu Cá nhân',
      veriPrimaryPrinciple: 6, // Transparency
      veriSecondaryPrinciples: [1, 2],
      veriDescription: 'Thông báo cho chủ thể dữ liệu về việc thu thập và xử lý dữ liệu'
    },
    {
      veriTemplateId: 'tmpl-002',
      veriTemplateName: 'Mẫu Đồng ý Thu thập Dữ liệu',
      veriPrimaryPrinciple: 7, // Consent
      veriSecondaryPrinciples: [0, 1],
      veriDescription: 'Biểu mẫu thu thập sự đồng ý từ chủ thể dữ liệu'
    },
    {
      veriTemplateId: 'tmpl-003',
      veriTemplateName: 'Chính sách Bảo mật Dữ liệu',
      veriPrimaryPrinciple: 5, // Security
      veriSecondaryPrinciples: [3, 4, 6],
      veriDescription: 'Chính sách toàn diện về bảo vệ dữ liệu cá nhân'
    },
    {
      veriTemplateId: 'tmpl-004',
      veriTemplateName: 'Quy định Lưu trữ và Xóa Dữ liệu',
      veriPrimaryPrinciple: 4, // Storage Limitation
      veriSecondaryPrinciples: [2, 5],
      veriDescription: 'Quy định về thời gian lưu trữ và quy trình xóa dữ liệu'
    },
    {
      veriTemplateId: 'tmpl-005',
      veriTemplateName: 'Thỏa thuận Xử lý Dữ liệu (DPA)',
      veriPrimaryPrinciple: 0, // Lawfulness
      veriSecondaryPrinciples: [1, 5],
      veriDescription: 'Hợp đồng giữa bên kiểm soát và bên xử lý dữ liệu'
    },
    {
      veriTemplateId: 'tmpl-006',
      veriTemplateName: 'Quy trình Đảm bảo Chính xác Dữ liệu',
      veriPrimaryPrinciple: 3, // Accuracy
      veriSecondaryPrinciples: [2],
      veriDescription: 'Quy trình cập nhật và duy trì độ chính xác dữ liệu'
    },
    {
      veriTemplateId: 'tmpl-007',
      veriTemplateName: 'Tuyên bố Giảm thiểu Dữ liệu',
      veriPrimaryPrinciple: 2, // Data Minimization
      veriSecondaryPrinciples: [1],
      veriDescription: 'Cam kết chỉ thu thập dữ liệu cần thiết'
    },
    {
      veriTemplateId: 'tmpl-008',
      veriTemplateName: 'Thông báo Mục đích Xử lý Dữ liệu',
      veriPrimaryPrinciple: 1, // Purpose Limitation
      veriSecondaryPrinciples: [6],
      veriDescription: 'Thông báo rõ ràng về mục đích sử dụng dữ liệu'
    }
  ];

  useEffect(() => {
    if (veriUserIntent.length < 20) return;

    const timer = setTimeout(async () => {
      const result = await classify(
        veriUserIntent,
        veriLanguage === 'vietnamese' ? 'vi' : 'en'
      );

      if (result) {
        // Find templates matching detected principle
        const matchingTemplates = ALL_TEMPLATES
          .filter(template => 
            template.veriPrimaryPrinciple === result.categoryId ||
            template.veriSecondaryPrinciples.includes(result.categoryId)
          )
          .sort((a, b) => {
            // Prioritize templates with matching primary principle
            if (a.veriPrimaryPrinciple === result.categoryId && 
                b.veriPrimaryPrinciple !== result.categoryId) return -1;
            if (a.veriPrimaryPrinciple !== result.categoryId && 
                b.veriPrimaryPrinciple === result.categoryId) return 1;
            return 0;
          })
          .slice(0, 3); // Top 3 recommendations

        setVeriRecommendedTemplates(matchingTemplates);
      }
    }, 1500);

    return () => clearTimeout(timer);
  }, [veriUserIntent, classify, veriLanguage]);

  return (
    <div className="veri-template-recommender">
      <h3 className="veri-section-title">
        {veriLanguage === 'vietnamese'
          ? 'Tìm Mẫu Tài liệu Phù hợp'
          : 'Find Suitable Document Template'}
      </h3>

      <div className="veri-input-group">
        <label className="veri-input-label">
          {veriLanguage === 'vietnamese'
            ? 'Mô tả tài liệu bạn cần tạo:'
            : 'Describe the document you need:'}
        </label>
        <textarea
          className="veri-textarea"
          value={veriUserIntent}
          onChange={(e) => setVeriUserIntent(e.target.value)}
          placeholder={veriLanguage === 'vietnamese'
            ? 'Ví dụ: Tôi cần tạo thông báo cho khách hàng về việc thu thập email và số điện thoại...'
            : 'Example: I need to create a notice for customers about collecting emails and phone numbers...'}
          rows={4}
        />
      </div>

      {loading && (
        <div className="veri-loading">
          <div className="veri-spinner"></div>
          <span>
            {veriLanguage === 'vietnamese'
              ? 'AI đang tìm kiếm mẫu phù hợp...'
              : 'AI is searching for suitable templates...'}
          </span>
        </div>
      )}

      {veriRecommendedTemplates.length > 0 && !loading && (
        <div className="veri-template-recommendations">
          <h4 className="veri-recommendations-title">
            {veriLanguage === 'vietnamese'
              ? 'Khuyến nghị từ AI'
              : 'AI Recommendations'}
          </h4>
          <div className="veri-template-grid">
            {veriRecommendedTemplates.map((template, index) => (
              <div
                key={template.veriTemplateId}
                className="veri-template-card"
                onClick={() => veriOnTemplateSelect(template)}
              >
                <div className="veri-template-header">
                  <span className="veri-template-rank">#{index + 1}</span>
                  <h5 className="veri-template-name">{template.veriTemplateName}</h5>
                </div>
                <p className="veri-template-description">
                  {template.veriDescription}
                </p>
                <div className="veri-template-principles">
                  <span className="veri-principle-badge veri-primary">
                    {getPrincipleName(template.veriPrimaryPrinciple, veriLanguage)}
                  </span>
                  {template.veriSecondaryPrinciples.slice(0, 2).map(principle => (
                    <span key={principle} className="veri-principle-badge veri-secondary">
                      {getPrincipleName(principle, veriLanguage)}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper function
function getPrincipleName(categoryId: number, language: 'vietnamese' | 'english'): string {
  const principles: Record<number, { vi: string; en: string }> = {
    0: { vi: 'Hợp pháp', en: 'Lawfulness' },
    1: { vi: 'Mục đích', en: 'Purpose' },
    2: { vi: 'Giảm thiểu', en: 'Minimization' },
    3: { vi: 'Chính xác', en: 'Accuracy' },
    4: { vi: 'Lưu trữ', en: 'Storage' },
    5: { vi: 'Bảo mật', en: 'Security' },
    6: { vi: 'Minh bạch', en: 'Transparency' },
    7: { vi: 'Đồng ý', en: 'Consent' }
  };
  return principles[categoryId]?.[language] || 'Unknown';
}
```

---

### Step 2: Content Validator

**File**: `src/components/VeriPortal/DocumentGeneration/components/VeriContentValidator.tsx`

```typescript
import React, { useState } from 'react';
import { useVeriAIDPOClassifier } from '../../../../hooks/useVeriAIDPOClassifier';

interface SectionValidation {
  sectionTitle: string;
  sectionContent: string;
  detectedPrinciple: number | null;
  confidence: number;
  status: 'valid' | 'warning' | 'invalid';
  suggestions: string[];
}

export const VeriContentValidator: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriDocumentSections: Array<{ title: string; content: string }>;
  veriRequiredPrinciples: number[]; // Required PDPL principles for this document type
}> = ({ veriLanguage, veriDocumentSections, veriRequiredPrinciples }) => {
  const [veriValidationResults, setVeriValidationResults] = useState<SectionValidation[]>([]);
  const [veriValidating, setVeriValidating] = useState(false);
  const { classify } = useVeriAIDPOClassifier();

  const validateDocument = async () => {
    setVeriValidating(true);

    const results: SectionValidation[] = [];

    for (const section of veriDocumentSections) {
      if (section.content.length < 30) {
        results.push({
          sectionTitle: section.title,
          sectionContent: section.content,
          detectedPrinciple: null,
          confidence: 0,
          status: 'warning',
          suggestions: [
            veriLanguage === 'vietnamese'
              ? 'Nội dung quá ngắn để phân tích'
              : 'Content too short for analysis'
          ]
        });
        continue;
      }

      const result = await classify(
        section.content,
        veriLanguage === 'vietnamese' ? 'vi' : 'en'
      );

      if (result) {
        const status = result.confidence > 0.7 ? 'valid' :
                      result.confidence > 0.4 ? 'warning' : 'invalid';

        const suggestions = generateSuggestions(
          result.categoryId,
          result.confidence,
          veriLanguage
        );

        results.push({
          sectionTitle: section.title,
          sectionContent: section.content,
          detectedPrinciple: result.categoryId,
          confidence: result.confidence,
          status,
          suggestions
        });
      }
    }

    setVeriValidationResults(results);
    setVeriValidating(false);
  };

  // Calculate coverage
  const detectedPrinciples = new Set(
    veriValidationResults
      .filter(r => r.detectedPrinciple !== null && r.confidence > 0.6)
      .map(r => r.detectedPrinciple!)
  );

  const missingPrinciples = veriRequiredPrinciples.filter(
    p => !detectedPrinciples.has(p)
  );

  const coveragePercentage = veriRequiredPrinciples.length > 0
    ? (detectedPrinciples.size / veriRequiredPrinciples.length) * 100
    : 0;

  return (
    <div className="veri-content-validator">
      <div className="veri-validator-header">
        <h3 className="veri-validator-title">
          {veriLanguage === 'vietnamese'
            ? 'Xác thực Nội dung PDPL'
            : 'PDPL Content Validation'}
        </h3>
        <button
          className="veri-validate-button"
          onClick={validateDocument}
          disabled={veriValidating || veriDocumentSections.length === 0}
        >
          {veriValidating
            ? (veriLanguage === 'vietnamese' ? 'Đang xác thực...' : 'Validating...')
            : (veriLanguage === 'vietnamese' ? 'Xác thực Tài liệu' : 'Validate Document')}
        </button>
      </div>

      {veriValidationResults.length > 0 && (
        <>
          {/* Coverage Summary */}
          <div className="veri-coverage-summary">
            <div className="veri-coverage-bar">
              <div 
                className="veri-coverage-fill"
                style={{ width: `${coveragePercentage}%` }}
              />
            </div>
            <p className="veri-coverage-text">
              {veriLanguage === 'vietnamese'
                ? `Độ bao phủ: ${detectedPrinciples.size}/${veriRequiredPrinciples.length} nguyên tắc (${coveragePercentage.toFixed(0)}%)`
                : `Coverage: ${detectedPrinciples.size}/${veriRequiredPrinciples.length} principles (${coveragePercentage.toFixed(0)}%)`}
            </p>
          </div>

          {/* Missing Principles Alert */}
          {missingPrinciples.length > 0 && (
            <div className="veri-alert veri-alert-warning">
              <svg className="veri-alert-icon" width="20" height="20" viewBox="0 0 20 20">
                <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v4a1 1 0 002 0V7zm-1 8a1 1 0 100-2 1 1 0 000 2z"/>
              </svg>
              <div>
                <strong>
                  {veriLanguage === 'vietnamese'
                    ? 'Nguyên tắc PDPL còn thiếu:'
                    : 'Missing PDPL Principles:'}
                </strong>
                <ul className="veri-missing-list">
                  {missingPrinciples.map(p => (
                    <li key={p}>{getPrincipleName(p, veriLanguage)}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Section-by-Section Results */}
          <div className="veri-validation-results">
            {veriValidationResults.map((result, index) => (
              <div key={index} className={`veri-validation-item veri-${result.status}`}>
                <div className="veri-validation-header">
                  <h4 className="veri-section-title">{result.sectionTitle}</h4>
                  <span className={`veri-status-badge veri-${result.status}`}>
                    {result.status === 'valid' ? '✓' : result.status === 'warning' ? '!' : '✗'}
                  </span>
                </div>
                
                {result.detectedPrinciple !== null && (
                  <div className="veri-detection-info">
                    <span className="veri-principle-label">
                      {getPrincipleName(result.detectedPrinciple, veriLanguage)}
                    </span>
                    <span className="veri-confidence-label">
                      {(result.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                )}

                {result.suggestions.length > 0 && (
                  <ul className="veri-suggestions-list">
                    {result.suggestions.map((suggestion, i) => (
                      <li key={i}>{suggestion}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

// Helper functions
function getPrincipleName(categoryId: number, language: 'vietnamese' | 'english'): string {
  const principles: Record<number, { vi: string; en: string }> = {
    0: { vi: 'Tính hợp pháp', en: 'Lawfulness' },
    1: { vi: 'Giới hạn mục đích', en: 'Purpose Limitation' },
    2: { vi: 'Giảm thiểu dữ liệu', en: 'Data Minimization' },
    3: { vi: 'Chính xác', en: 'Accuracy' },
    4: { vi: 'Giới hạn lưu trữ', en: 'Storage Limitation' },
    5: { vi: 'An toàn bảo mật', en: 'Security' },
    6: { vi: 'Minh bạch', en: 'Transparency' },
    7: { vi: 'Đồng ý', en: 'Consent' }
  };
  return principles[categoryId]?.[language] || 'Unknown';
}

function generateSuggestions(
  categoryId: number,
  confidence: number,
  language: 'vietnamese' | 'english'
): string[] {
  const suggestions: string[] = [];

  if (confidence < 0.7) {
    suggestions.push(
      language === 'vietnamese'
        ? 'Nội dung chưa rõ ràng - cân nhắc bổ sung chi tiết'
        : 'Content unclear - consider adding more details'
    );
  }

  // Category-specific suggestions
  const categorySuggestions: Record<number, { vi: string[]; en: string[] }> = {
    0: {
      vi: ['Làm rõ cơ sở pháp lý (hợp đồng, pháp luật, hoặc đồng ý)'],
      en: ['Clarify legal basis (contract, law, or consent)']
    },
    1: {
      vi: ['Nêu rõ mục đích cụ thể của việc xử lý dữ liệu'],
      en: ['State specific purpose of data processing']
    },
    2: {
      vi: ['Liệt kê dữ liệu "cần thiết" và "tùy chọn"'],
      en: ['List "necessary" vs "optional" data']
    },
    3: {
      vi: ['Mô tả quy trình cập nhật và duy trì độ chính xác'],
      en: ['Describe update and accuracy maintenance process']
    },
    4: {
      vi: ['Ghi rõ thời gian lưu trữ cụ thể (tháng/năm)'],
      en: ['Specify exact retention period (months/years)']
    },
    5: {
      vi: ['Nêu các biện pháp bảo mật cụ thể (mã hóa, kiểm soát truy cập)'],
      en: ['List specific security measures (encryption, access control)']
    },
    6: {
      vi: ['Đảm bảo thông tin dễ hiểu, rõ ràng cho chủ thể dữ liệu'],
      en: ['Ensure information is clear and understandable for data subjects']
    },
    7: {
      vi: ['Làm rõ cách thức thu thập đồng ý và quyền rút lại đồng ý'],
      en: ['Clarify consent collection method and right to withdraw']
    }
  };

  suggestions.push(...(categorySuggestions[categoryId]?.[language] || []));

  return suggestions;
}
```

---

## Testing

### Test Case 1: Template Recommendation

```typescript
const testInputs = [
  {
    input: "Tôi cần tạo thông báo cho khách hàng về việc thu thập email",
    expectedPrimary: 6, // Transparency
    expectedTemplates: ['tmpl-001', 'tmpl-002']
  },
  {
    input: "Cần mẫu hợp đồng với đối tác xử lý dữ liệu",
    expectedPrimary: 0, // Lawfulness
    expectedTemplates: ['tmpl-005']
  }
];
```

### Test Case 2: Content Validation

```typescript
const testDocument = {
  sections: [
    { title: "1. Mục đích", content: "Chúng tôi sử dụng dữ liệu để giao hàng..." },
    { title: "2. Bảo mật", content: "Dữ liệu được mã hóa AES-256..." },
  ],
  requiredPrinciples: [1, 2, 5, 6], // Purpose, Minimization, Security, Transparency
  expectedCoverage: 50 // Only 2/4 covered
};
```

---

## Deployment Checklist

- [ ] Implement template recommender component
- [ ] Implement content validator component
- [ ] Create template database with principle mappings
- [ ] Test with 30+ Vietnamese document scenarios
- [ ] Add regional tone adaptation (North/South)
- [ ] Integrate with existing document editor
- [ ] Add export functionality (PDF/DOCX)
- [ ] Create user tutorial videos

---

## Performance Considerations

- **Caching**: Cache template recommendations for 24 hours
- **Batch Validation**: Validate all sections in parallel
- **Progressive Disclosure**: Show validation results section-by-section
- **Auto-save**: Save draft every 30 seconds during editing

---

## Next Steps

1. **Week 1**: Implement template recommender
2. **Week 2**: Implement content validator
3. **Week 3**: Add regional tone adaptation
4. **Week 4**: User testing with 10 enterprise customers

---

**Priority**: HIGH - Critical for document compliance  
**Impact**: Reduces document creation time by 50-70%  
**Dependencies**: VeriAIDPO model, document template database
