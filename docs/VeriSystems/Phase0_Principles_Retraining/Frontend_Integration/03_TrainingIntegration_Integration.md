# Training Integration - VeriAIDPO Integration Guide

**System**: VeriPortal Training Integration  
**Component**: `VeriTrainingIntegrationSystem`  
**Priority**: MEDIUM (Phase 1 - Week 1-2)  
**Model**: VeriAIDPO_Principles_VI v1.0 (93.75% accuracy)

---

## Overview

Integrate VeriAIDPO model to provide **automated quiz grading**, **intelligent content categorization**, and **personalized learning paths** for PDPL 2025 training programs.

---

## Use Cases

### 1. Automatic Quiz Grading
**Context**: Employee training quiz submission

**Problem**: Manual grading of open-ended PDPL questions is time-consuming  
**Solution**: AI automatically grades free-text answers

**Example**:
```
Question: "Công ty nên làm gì để tuân thủ nguyên tắc giảm thiểu dữ liệu?"

Student Answer: "Chỉ thu thập email và số điện thoại nếu cần thiết cho giao hàng"

AI Analysis:
  - Detected Principle: Cat 2 - Data Minimization (92% confidence)
  - Correct Principle: Cat 2 - Data Minimization
  - Score: 9/10 (Good understanding, missing retention policy mention)
  
AI Feedback: "Câu trả lời tốt! Bạn đã hiểu đúng về giảm thiểu dữ liệu. 
              Có thể bổ sung: Nên xóa dữ liệu sau khi hoàn tất giao hàng."
```

### 2. Content Categorization
**Context**: Admin uploads training materials

**Problem**: 500+ training modules, need automatic tagging by PDPL principle  
**Solution**: AI categorizes content into principle categories

**Example**:
```
Upload: "Module 07 - Quyền của Chủ thể Dữ liệu.pdf"

AI Analysis:
  Primary: Cat 6 - Transparency (88% confidence)
  Secondary: Cat 7 - Consent (76% confidence)
  
Auto-Tags: #transparency #consent #data-subject-rights
Recommended Course: "PDPL Foundations Track"
Difficulty Level: Intermediate
```

### 3. Knowledge Gap Detection
**Context**: Employee completes multiple quizzes

**Problem**: Don't know which PDPL areas employee is weak in  
**Solution**: AI identifies patterns in incorrect answers

**Example**:
```
Employee: Nguyen Van A
Quiz History (10 quizzes):

Principle Performance:
  Cat 0 (Lawfulness): 90% - Strong
  Cat 1 (Purpose): 85% - Strong
  Cat 2 (Minimization): 45% - WEAK ← Gap detected
  Cat 3 (Accuracy): 80% - Good
  Cat 4 (Storage): 50% - WEAK ← Gap detected
  ...

AI Recommendation:
  "Nhân viên cần học thêm về Giảm thiểu Dữ liệu và Giới hạn Lưu trữ.
   Khuyến nghị: Module 03 (Data Minimization) và Module 05 (Storage Policies)"
```

### 4. Personalized Learning Paths
**Context**: New employee starts training

**Problem**: One-size-fits-all training isn't effective  
**Solution**: AI creates custom learning sequence based on role and region

**Example**:
```
Employee Profile:
  - Role: Marketing Manager
  - Region: South Vietnam (HCMC)
  - Industry: E-commerce
  
AI Learning Path:
  1. Cat 7 (Consent) - HIGH PRIORITY
     Reason: Marketing needs strong consent practices
  
  2. Cat 1 (Purpose Limitation) - HIGH PRIORITY
     Reason: Email campaigns must respect stated purposes
  
  3. Cat 6 (Transparency) - MEDIUM
     Reason: Customer-facing role needs clear communication
  
  4. Cat 2 (Data Minimization) - MEDIUM
     Reason: Reduce liability in marketing databases
  
  ... (Other principles as foundational knowledge)
```

---

## Implementation

### Step 1: Auto-Grading Engine

**File**: `src/components/VeriPortal/TrainingIntegration/components/VeriQuizAutoGrader.tsx`

```typescript
import React, { useState } from 'react';
import { useVeriAIDPOClassifier } from '../../../../hooks/useVeriAIDPOClassifier';

interface QuizQuestion {
  veriQuestionId: string;
  veriQuestionText: string;
  veriCorrectPrinciple: number; // Expected PDPL category
  veriPoints: number;
}

interface QuizAnswer {
  veriQuestionId: string;
  veriStudentAnswer: string;
  veriDetectedPrinciple: number | null;
  veriConfidence: number;
  veriScore: number;
  veriFeedback: string;
}

export const VeriQuizAutoGrader: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriQuestions: QuizQuestion[];
  veriStudentAnswers: Record<string, string>; // questionId -> answer text
  veriOnGradingComplete: (results: QuizAnswer[]) => void;
}> = ({ veriLanguage, veriQuestions, veriStudentAnswers, veriOnGradingComplete }) => {
  const [veriGrading, setVeriGrading] = useState(false);
  const [veriProgress, setVeriProgress] = useState(0);
  const { classify } = useVeriAIDPOClassifier();

  const gradeQuiz = async () => {
    setVeriGrading(true);
    setVeriProgress(0);

    const results: QuizAnswer[] = [];

    for (let i = 0; i < veriQuestions.length; i++) {
      const question = veriQuestions[i];
      const studentAnswer = veriStudentAnswers[question.veriQuestionId] || '';

      if (studentAnswer.trim().length < 10) {
        // Too short to grade
        results.push({
          veriQuestionId: question.veriQuestionId,
          veriStudentAnswer: studentAnswer,
          veriDetectedPrinciple: null,
          veriConfidence: 0,
          veriScore: 0,
          veriFeedback: veriLanguage === 'vietnamese'
            ? 'Câu trả lời quá ngắn. Vui lòng trả lời chi tiết hơn.'
            : 'Answer too short. Please provide more details.'
        });
      } else {
        // Classify student answer
        const result = await classify(
          studentAnswer,
          veriLanguage === 'vietnamese' ? 'vi' : 'en'
        );

        if (result) {
          const isCorrect = result.categoryId === question.veriCorrectPrinciple;
          const score = calculateScore(
            isCorrect,
            result.confidence,
            question.veriPoints
          );

          const feedback = generateFeedback(
            isCorrect,
            result.categoryId,
            question.veriCorrectPrinciple,
            result.confidence,
            veriLanguage
          );

          results.push({
            veriQuestionId: question.veriQuestionId,
            veriStudentAnswer: studentAnswer,
            veriDetectedPrinciple: result.categoryId,
            veriConfidence: result.confidence,
            veriScore: score,
            veriFeedback: feedback
          });
        }
      }

      setVeriProgress(((i + 1) / veriQuestions.length) * 100);
    }

    setVeriGrading(false);
    veriOnGradingComplete(results);
  };

  return (
    <div className="veri-quiz-auto-grader">
      <div className="veri-grader-header">
        <h3 className="veri-grader-title">
          {veriLanguage === 'vietnamese'
            ? 'Chấm điểm Tự động bằng AI'
            : 'AI Auto-Grading'}
        </h3>
        <button
          className="veri-grade-button"
          onClick={gradeQuiz}
          disabled={veriGrading || Object.keys(veriStudentAnswers).length === 0}
        >
          {veriGrading
            ? (veriLanguage === 'vietnamese' ? 'Đang chấm điểm...' : 'Grading...')
            : (veriLanguage === 'vietnamese' ? 'Chấm điểm Bài thi' : 'Grade Quiz')}
        </button>
      </div>

      {veriGrading && (
        <div className="veri-grading-progress">
          <div className="veri-progress-bar">
            <div 
              className="veri-progress-fill"
              style={{ width: `${veriProgress}%` }}
            />
          </div>
          <p className="veri-progress-text">
            {veriLanguage === 'vietnamese'
              ? `Đang chấm: ${veriProgress.toFixed(0)}%`
              : `Grading: ${veriProgress.toFixed(0)}%`}
          </p>
        </div>
      )}
    </div>
  );
};

// Helper functions
function calculateScore(
  isCorrect: boolean,
  confidence: number,
  maxPoints: number
): number {
  if (!isCorrect) return 0;
  
  // Full points if high confidence, partial if medium
  if (confidence >= 0.8) return maxPoints;
  if (confidence >= 0.6) return maxPoints * 0.8;
  return maxPoints * 0.5;
}

function generateFeedback(
  isCorrect: boolean,
  detectedPrinciple: number,
  correctPrinciple: number,
  confidence: number,
  language: 'vietnamese' | 'english'
): string {
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

  if (isCorrect) {
    if (confidence >= 0.8) {
      return language === 'vietnamese'
        ? `✓ Chính xác! Bạn đã hiểu rõ về ${principleNames[correctPrinciple].vi}.`
        : `✓ Correct! You understand ${principleNames[correctPrinciple].en} well.`;
    } else {
      return language === 'vietnamese'
        ? `✓ Đúng, nhưng có thể giải thích rõ hơn về ${principleNames[correctPrinciple].vi}.`
        : `✓ Correct, but could explain ${principleNames[correctPrinciple].en} more clearly.`;
    }
  } else {
    return language === 'vietnamese'
      ? `✗ Chưa chính xác. Câu trả lời liên quan đến ${principleNames[detectedPrinciple].vi}, nhưng câu hỏi hỏi về ${principleNames[correctPrinciple].vi}.`
      : `✗ Incorrect. Answer relates to ${principleNames[detectedPrinciple].en}, but question asks about ${principleNames[correctPrinciple].en}.`;
  }
}
```

---

### Step 2: Content Categorization System

**File**: `src/components/VeriPortal/TrainingIntegration/components/VeriContentCategorizer.tsx`

```typescript
import React, { useState } from 'react';
import { useVeriAIDPOClassifier } from '../../../../hooks/useVeriAIDPOClassifier';

interface TrainingModule {
  veriModuleId: string;
  veriModuleName: string;
  veriDescription: string;
  veriContent?: string; // Full text for analysis
}

interface CategorizedModule extends TrainingModule {
  veriPrimaryPrinciple: number;
  veriSecondaryPrinciples: number[];
  veriConfidence: number;
  veriAutoTags: string[];
  veriDifficulty: 'beginner' | 'intermediate' | 'advanced';
}

export const VeriContentCategorizer: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriModules: TrainingModule[];
  veriOnCategorizationComplete: (modules: CategorizedModule[]) => void;
}> = ({ veriLanguage, veriModules, veriOnCategorizationComplete }) => {
  const [veriCategorizing, setVeriCategorizing] = useState(false);
  const [veriProgress, setVeriProgress] = useState(0);
  const { classify } = useVeriAIDPOClassifier();

  const categorizeModules = async () => {
    setVeriCategorizing(true);
    setVeriProgress(0);

    const categorizedModules: CategorizedModule[] = [];

    for (let i = 0; i < veriModules.length; i++) {
      const module = veriModules[i];
      
      // Analyze module description + first 500 chars of content
      const textToAnalyze = `${module.veriDescription} ${module.veriContent?.substring(0, 500) || ''}`;

      const result = await classify(
        textToAnalyze,
        veriLanguage === 'vietnamese' ? 'vi' : 'en'
      );

      if (result) {
        const autoTags = generateTags(result.categoryId, veriLanguage);
        const difficulty = estimateDifficulty(module.veriContent || '');

        categorizedModules.push({
          ...module,
          veriPrimaryPrinciple: result.categoryId,
          veriSecondaryPrinciples: [], // Could do multi-label classification
          veriConfidence: result.confidence,
          veriAutoTags: autoTags,
          veriDifficulty: difficulty
        });
      }

      setVeriProgress(((i + 1) / veriModules.length) * 100);
    }

    setVeriCategorizing(false);
    veriOnCategorizationComplete(categorizedModules);
  };

  return (
    <div className="veri-content-categorizer">
      <h3 className="veri-categorizer-title">
        {veriLanguage === 'vietnamese'
          ? 'Phân loại Nội dung Tự động'
          : 'Automatic Content Categorization'}
      </h3>

      <button
        className="veri-categorize-button"
        onClick={categorizeModules}
        disabled={veriCategorizing || veriModules.length === 0}
      >
        {veriCategorizing
          ? (veriLanguage === 'vietnamese' ? `Đang phân loại... ${veriProgress.toFixed(0)}%` : `Categorizing... ${veriProgress.toFixed(0)}%`)
          : (veriLanguage === 'vietnamese' ? `Phân loại ${veriModules.length} Module` : `Categorize ${veriModules.length} Modules`)}
      </button>
    </div>
  );
};

// Helper functions
function generateTags(categoryId: number, language: 'vietnamese' | 'english'): string[] {
  const tagsByCategory: Record<number, { vi: string[]; en: string[] }> = {
    0: {
      vi: ['hợp pháp', 'cơ sở pháp lý', 'tuân thủ'],
      en: ['lawfulness', 'legal-basis', 'compliance']
    },
    1: {
      vi: ['mục đích', 'giới hạn', 'sử dụng dữ liệu'],
      en: ['purpose', 'limitation', 'data-use']
    },
    2: {
      vi: ['giảm thiểu', 'thu thập', 'cần thiết'],
      en: ['minimization', 'collection', 'necessary']
    },
    3: {
      vi: ['chính xác', 'cập nhật', 'duy trì'],
      en: ['accuracy', 'update', 'maintenance']
    },
    4: {
      vi: ['lưu trữ', 'xóa', 'thời hạn'],
      en: ['storage', 'deletion', 'retention']
    },
    5: {
      vi: ['bảo mật', 'an toàn', 'mã hóa'],
      en: ['security', 'safety', 'encryption']
    },
    6: {
      vi: ['minh bạch', 'thông báo', 'rõ ràng'],
      en: ['transparency', 'notice', 'clarity']
    },
    7: {
      vi: ['đồng ý', 'cho phép', 'rút lại'],
      en: ['consent', 'permission', 'withdrawal']
    }
  };

  return tagsByCategory[categoryId]?.[language] || [];
}

function estimateDifficulty(content: string): 'beginner' | 'intermediate' | 'advanced' {
  // Simple heuristic based on content length and complexity
  const length = content.length;
  const complexWords = ['quy định', 'điều khoản', 'thực thi', 'xử phạt', 'pháp lý'];
  const complexWordCount = complexWords.filter(word => content.includes(word)).length;

  if (length < 1000 && complexWordCount < 3) return 'beginner';
  if (length < 3000 && complexWordCount < 6) return 'intermediate';
  return 'advanced';
}
```

---

### Step 3: Knowledge Gap Analyzer

**File**: `src/components/VeriPortal/TrainingIntegration/components/VeriKnowledgeGapAnalyzer.tsx`

```typescript
import React, { useEffect, useState } from 'react';

interface QuizHistory {
  veriQuizId: string;
  veriQuizDate: Date;
  veriAnswers: Array<{
    veriPrinciple: number;
    veriIsCorrect: boolean;
    veriScore: number;
  }>;
}

interface KnowledgeGap {
  veriPrinciple: number;
  veriPrincipleName: string;
  veriPerformance: number; // Percentage
  veriStatus: 'strong' | 'good' | 'weak' | 'critical';
  veriRecommendations: string[];
}

export const VeriKnowledgeGapAnalyzer: React.FC<{
  veriLanguage: 'vietnamese' | 'english';
  veriQuizHistory: QuizHistory[];
  veriEmployeeRole?: string;
}> = ({ veriLanguage, veriQuizHistory, veriEmployeeRole }) => {
  const [veriGaps, setVeriGaps] = useState<KnowledgeGap[]>([]);

  useEffect(() => {
    analyzeGaps();
  }, [veriQuizHistory]);

  const analyzeGaps = () => {
    const principleStats: Record<number, { correct: number; total: number }> = {};

    // Initialize all 8 principles
    for (let i = 0; i < 8; i++) {
      principleStats[i] = { correct: 0, total: 0 };
    }

    // Aggregate quiz history
    veriQuizHistory.forEach(quiz => {
      quiz.veriAnswers.forEach(answer => {
        principleStats[answer.veriPrinciple].total++;
        if (answer.veriIsCorrect) {
          principleStats[answer.veriPrinciple].correct++;
        }
      });
    });

    // Calculate gaps
    const gaps: KnowledgeGap[] = [];
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
      const stats = principleStats[i];
      const performance = stats.total > 0 ? (stats.correct / stats.total) * 100 : 0;

      let status: 'strong' | 'good' | 'weak' | 'critical';
      if (performance >= 85) status = 'strong';
      else if (performance >= 70) status = 'good';
      else if (performance >= 50) status = 'weak';
      else status = 'critical';

      gaps.push({
        veriPrinciple: i,
        veriPrincipleName: principleNames[i][veriLanguage],
        veriPerformance: performance,
        veriStatus: status,
        veriRecommendations: generateRecommendations(i, status, veriLanguage, veriEmployeeRole)
      });
    }

    // Sort by performance (weakest first)
    gaps.sort((a, b) => a.veriPerformance - b.veriPerformance);

    setVeriGaps(gaps);
  };

  const overallPerformance = veriGaps.length > 0
    ? veriGaps.reduce((sum, gap) => sum + gap.veriPerformance, 0) / veriGaps.length
    : 0;

  return (
    <div className="veri-knowledge-gap-analyzer">
      <h3 className="veri-analyzer-title">
        {veriLanguage === 'vietnamese'
          ? 'Phân tích Điểm Yếu Kiến thức'
          : 'Knowledge Gap Analysis'}
      </h3>

      <div className="veri-overall-performance">
        <div className="veri-performance-circle">
          <svg width="120" height="120">
            <circle cx="60" cy="60" r="50" fill="none" stroke="#e5e7eb" strokeWidth="10"/>
            <circle
              cx="60"
              cy="60"
              r="50"
              fill="none"
              stroke="#10b981"
              strokeWidth="10"
              strokeDasharray={`${(overallPerformance / 100) * 314} 314`}
              transform="rotate(-90 60 60)"
            />
            <text x="60" y="65" textAnchor="middle" fontSize="24" fontWeight="bold">
              {overallPerformance.toFixed(0)}%
            </text>
          </svg>
        </div>
        <p className="veri-performance-label">
          {veriLanguage === 'vietnamese' ? 'Hiểu biết Tổng thể' : 'Overall Understanding'}
        </p>
      </div>

      <div className="veri-gap-list">
        {veriGaps.map(gap => (
          <div key={gap.veriPrinciple} className={`veri-gap-item veri-${gap.veriStatus}`}>
            <div className="veri-gap-header">
              <span className="veri-principle-name">{gap.veriPrincipleName}</span>
              <span className="veri-performance-badge">
                {gap.veriPerformance.toFixed(0)}%
              </span>
            </div>
            <div className="veri-gap-bar">
              <div 
                className="veri-gap-fill"
                style={{ width: `${gap.veriPerformance}%` }}
              />
            </div>
            {gap.veriStatus !== 'strong' && (
              <div className="veri-recommendations">
                <h5 className="veri-recommendations-title">
                  {veriLanguage === 'vietnamese' ? 'Khuyến nghị:' : 'Recommendations:'}
                </h5>
                <ul className="veri-recommendations-list">
                  {gap.veriRecommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// Helper function
function generateRecommendations(
  principle: number,
  status: string,
  language: 'vietnamese' | 'english',
  role?: string
): string[] {
  if (status === 'strong') return [];

  const recommendations: Record<number, { vi: string[]; en: string[] }> = {
    0: {
      vi: ['Học Module: Cơ sở Pháp lý Xử lý Dữ liệu', 'Tham khảo Điều 13 PDPL 2025'],
      en: ['Study Module: Legal Basis for Data Processing', 'Review Article 13 PDPL 2025']
    },
    1: {
      vi: ['Học Module: Giới hạn Mục đích Sử dụng', 'Thực hành: Xác định mục đích cụ thể'],
      en: ['Study Module: Purpose Limitation', 'Practice: Identify specific purposes']
    },
    2: {
      vi: ['Học Module: Giảm thiểu Thu thập Dữ liệu', 'Bài tập: Phân biệt dữ liệu cần thiết/không cần thiết'],
      en: ['Study Module: Data Minimization', 'Exercise: Distinguish necessary/unnecessary data']
    },
    3: {
      vi: ['Học Module: Duy trì Độ Chính xác', 'Thực hành: Quy trình cập nhật dữ liệu'],
      en: ['Study Module: Maintaining Accuracy', 'Practice: Data update procedures']
    },
    4: {
      vi: ['Học Module: Chính sách Lưu trữ', 'Bài tập: Xác định thời hạn lưu trữ phù hợp'],
      en: ['Study Module: Storage Policies', 'Exercise: Determine appropriate retention periods']
    },
    5: {
      vi: ['Học Module: An toàn Bảo mật Dữ liệu', 'Thực hành: Biện pháp bảo vệ kỹ thuật'],
      en: ['Study Module: Data Security', 'Practice: Technical protection measures']
    },
    6: {
      vi: ['Học Module: Minh bạch và Thông báo', 'Bài tập: Viết thông báo rõ ràng cho khách hàng'],
      en: ['Study Module: Transparency and Notice', 'Exercise: Write clear customer notices']
    },
    7: {
      vi: ['Học Module: Thu thập Đồng ý Hợp lệ', 'Thực hành: Thiết kế biểu mẫu đồng ý'],
      en: ['Study Module: Valid Consent Collection', 'Practice: Design consent forms']
    }
  };

  // Role-specific recommendations
  if (role === 'marketing' && principle === 7) {
    recommendations[7].vi.push('Đặc biệt quan trọng cho Marketing: Email marketing campaigns');
    recommendations[7].en.push('Critical for Marketing: Email marketing campaigns');
  }

  return recommendations[principle]?.[language] || [];
}
```

---

## Testing

### Test Case 1: Auto-Grading Accuracy

```typescript
const testQuizzes = [
  {
    question: "Nguyên tắc nào yêu cầu chỉ thu thập dữ liệu cần thiết?",
    correctPrinciple: 2, // Data Minimization
    studentAnswer: "Chỉ lấy email và số điện thoại nếu cần",
    expectedScore: 8 // Out of 10
  },
  {
    question: "Công ty phải làm gì để tuân thủ nguyên tắc minh bạch?",
    correctPrinciple: 6, // Transparency
    studentAnswer: "Thông báo rõ ràng cho khách hàng về việc sử dụng dữ liệu",
    expectedScore: 10
  }
];
```

### Test Case 2: Knowledge Gap Detection

```typescript
const mockQuizHistory = [
  {
    quizId: 'quiz-001',
    answers: [
      { principle: 0, isCorrect: true },
      { principle: 1, isCorrect: true },
      { principle: 2, isCorrect: false }, // Weak in Data Minimization
      { principle: 2, isCorrect: false },
    ]
  }
];
// Expected: Cat 2 flagged as knowledge gap
```

---

## Deployment Checklist

- [ ] Implement auto-grading component
- [ ] Implement content categorizer
- [ ] Implement knowledge gap analyzer
- [ ] Create training module database
- [ ] Test grading accuracy (>80% match with human graders)
- [ ] Add personalized learning path generator
- [ ] Integrate with LMS (Learning Management System)
- [ ] Create admin dashboard for training analytics

---

## Performance Considerations

- **Batch Grading**: Grade all quiz answers in parallel
- **Caching**: Cache categorization results for modules
- **Real-time Feedback**: Show grading progress to students
- **Analytics**: Track grading accuracy over time

---

## Next Steps

1. **Week 1**: Implement auto-grading engine
2. **Week 2**: Implement content categorization
3. **Week 3**: Implement knowledge gap analyzer
4. **Week 4**: User testing with HR departments

---

**Priority**: MEDIUM - High value for training efficiency  
**Impact**: Reduces training administration time by 60-80%  
**Dependencies**: VeriAIDPO model, quiz database, training modules
