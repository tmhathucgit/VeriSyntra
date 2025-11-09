# Data Population Method 4: VeriPortal Wizards
## Vietnamese PDPL 2025 Compliance - Data Categories Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** data_categories Table  
**Method:** Guided UI Wizard with PDPL Article 4.13 Help  
**Architecture:** React Frontend + Vietnamese Cultural Intelligence + Step-by-Step Guidance  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **VeriPortal wizard-based data category creation**. The wizard guides Vietnamese users through PDPL Article 4.13 sensitive data classification with contextual help, examples, and validation at each step.

**Key Features:**
- 7-step guided wizard for category creation
- PDPL Article 4.13 contextual help and examples
- Vietnamese-first UI with cultural intelligence
- Real-time validation with Vietnamese error messages
- Category templates with PDPL compliance guidance
- Save draft and resume functionality
- Progress tracking with completion percentage
- Zero hard-coding with step configuration

**Use Cases:**
- First-time PDPL compliance setup
- Guided category creation for non-technical users
- PDPL Article 4.13 educational workflow
- Vietnamese business context category setup
- Interactive learning with compliance examples

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Wizard Step Configuration](#wizard-step-configuration)
3. [PDPL Article 4.13 Help Context](#pdpl-article-413-help-context)
4. [Vietnamese UI Components](#vietnamese-ui-components)
5. [Validation and Error Handling](#validation-and-error-handling)
6. [Draft Management](#draft-management)
7. [Success Criteria](#success-criteria)

---

## Architecture Overview

### Wizard System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         VeriPortal Wizard Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Wizard      │  │  Step        │  │  PDPL        │     │
│  │  Controller  │─>│  Navigator   │─>│  Help        │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Cultural    │  │  Validator   │  │  Draft       │     │
│  │  Context     │  │  Real-time   │  │  Manager     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  data_categories       │                    │
│              │  (Wizard Created)      │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Wizard Workflow:**
1. Select category type (basic or sensitive)
2. Enter Vietnamese category name
3. Enter Vietnamese description
4. If sensitive: Select PDPL Article 4.13 type
5. Add examples (Vietnamese and English)
6. Review and validate
7. Submit or save draft

---

## Wizard Step Configuration

### Step Definitions and Flow

```python
# services/wizard/wizard_config.py

"""
VeriPortal Wizard Configuration
Vietnamese-first Category Creation
"""

from enum import Enum
from typing import Dict, List, Optional


class WizardType(str, Enum):
    """
    Loại wizard
    Wizard type
    """
    CATEGORY_CREATION = "category_creation"          # Tạo danh mục dữ liệu
    CATEGORY_BULK_SETUP = "category_bulk_setup"      # Thiết lập hàng loạt
    PDPL_CLASSIFICATION = "pdpl_classification"      # Phân loại PDPL


class WizardStepStatus(str, Enum):
    """
    Trạng thái bước wizard
    Wizard step status
    """
    NOT_STARTED = "not_started"      # Chưa bắt đầu
    IN_PROGRESS = "in_progress"      # Đang thực hiện
    COMPLETED = "completed"          # Hoàn thành
    SKIPPED = "skipped"              # Bỏ qua
    ERROR = "error"                  # Lỗi


# Wizard step configuration
CATEGORY_WIZARD_STEPS: List[Dict[str, any]] = [
    {
        "step_number": 1,
        "step_key": "category_type_selection",
        "step_name_vi": "Chọn loại danh mục",
        "step_name_en": "Select Category Type",
        "description_vi": "Chọn loại danh mục: Cơ bản hoặc Nhạy cảm theo PDPL",
        "description_en": "Choose category type: Basic or Sensitive per PDPL",
        "required": True,
        "pdpl_article": "Art. 4.1 & 4.13 PDPL",
        "help_text_vi": "Dữ liệu nhạy cảm theo Điều 4.13 PDPL bao gồm: chính trị, tôn giáo, sức khỏe, sinh trắc học...",
        "validation_rules": ["category_type_required"]
    },
    {
        "step_number": 2,
        "step_key": "category_name_vi",
        "step_name_vi": "Tên danh mục tiếng Việt",
        "step_name_en": "Vietnamese Category Name",
        "description_vi": "Nhập tên danh mục bằng tiếng Việt có dấu",
        "description_en": "Enter category name in Vietnamese with diacritics",
        "required": True,
        "pdpl_article": "Art. 4.1 PDPL",
        "help_text_vi": "Ví dụ: Thông tin sức khỏe, Dữ liệu sinh trắc học, Thông tin liên hệ",
        "validation_rules": [
            "vietnamese_diacritics_required",
            "min_length_3",
            "max_length_200"
        ]
    },
    {
        "step_number": 3,
        "step_key": "category_name_en",
        "step_name_vi": "Tên danh mục tiếng Anh (Tùy chọn)",
        "step_name_en": "English Category Name (Optional)",
        "description_vi": "Nhập tên danh mục bằng tiếng Anh",
        "description_en": "Enter category name in English",
        "required": False,
        "pdpl_article": "Art. 4.1 PDPL",
        "help_text_vi": "Ví dụ: Health Information, Biometric Data, Contact Information",
        "validation_rules": ["max_length_200"]
    },
    {
        "step_number": 4,
        "step_key": "category_description",
        "step_name_vi": "Mô tả danh mục",
        "step_name_en": "Category Description",
        "description_vi": "Mô tả chi tiết danh mục dữ liệu",
        "description_en": "Detailed category description",
        "required": True,
        "pdpl_article": "Art. 4.1 PDPL",
        "help_text_vi": "Mô tả rõ ràng loại dữ liệu thuộc danh mục này, bao gồm ví dụ cụ thể",
        "validation_rules": [
            "min_length_10",
            "max_length_2000"
        ]
    },
    {
        "step_number": 5,
        "step_key": "sensitive_data_type",
        "step_name_vi": "Loại dữ liệu nhạy cảm (Nếu áp dụng)",
        "step_name_en": "Sensitive Data Type (If Applicable)",
        "description_vi": "Chọn loại dữ liệu nhạy cảm theo Điều 4.13 PDPL",
        "description_en": "Select sensitive data type per Article 4.13 PDPL",
        "required": False,
        "conditional": "category_type == 'sensitive'",
        "pdpl_article": "Art. 4.13 PDPL",
        "help_text_vi": "12 loại dữ liệu nhạy cảm: chính trị, tôn giáo, sức khỏe, sinh trắc học...",
        "validation_rules": ["required_if_sensitive"]
    },
    {
        "step_number": 6,
        "step_key": "examples",
        "step_name_vi": "Ví dụ về dữ liệu",
        "step_name_en": "Data Examples",
        "description_vi": "Nhập các ví dụ cụ thể về dữ liệu thuộc danh mục này",
        "description_en": "Enter specific examples of data in this category",
        "required": False,
        "pdpl_article": "Art. 4.1 PDPL",
        "help_text_vi": "Ví dụ cho 'Thông tin sức khỏe': hồ sơ bệnh án, kết quả xét nghiệm, đơn thuốc",
        "validation_rules": ["max_examples_10"]
    },
    {
        "step_number": 7,
        "step_key": "review_and_submit",
        "step_name_vi": "Xem lại và Gửi",
        "step_name_en": "Review and Submit",
        "description_vi": "Kiểm tra thông tin và tạo danh mục",
        "description_en": "Review information and create category",
        "required": True,
        "pdpl_article": "Art. 4.1 & 4.13 PDPL",
        "help_text_vi": "Kiểm tra kỹ thông tin trước khi tạo danh mục",
        "validation_rules": ["all_required_fields_completed"]
    }
]


# Step status translations
STEP_STATUS_TRANSLATIONS_VI: Dict[str, str] = {
    "not_started": "Chưa bắt đầu",
    "in_progress": "Đang thực hiện",
    "completed": "Hoàn thành",
    "skipped": "Bỏ qua",
    "error": "Lỗi"
}

STEP_STATUS_TRANSLATIONS_EN: Dict[str, str] = {
    "not_started": "Not Started",
    "in_progress": "In Progress",
    "completed": "Completed",
    "skipped": "Skipped",
    "error": "Error"
}
```

---

## PDPL Article 4.13 Help Context

### Contextual Help and Examples

```python
# services/wizard/pdpl_help.py

"""
PDPL Article 4.13 Help Context
Vietnamese Educational Content
"""

from typing import Dict, List


# PDPL Article 4.13 sensitive data types with help
PDPL_SENSITIVE_DATA_HELP: Dict[str, Dict[str, any]] = {
    "political_opinions": {
        "name_vi": "Quan điểm chính trị",
        "name_en": "Political Opinions",
        "pdpl_article": "Art. 4.13.a PDPL",
        "description_vi": "Thông tin về quan điểm, niềm tin chính trị của cá nhân",
        "description_en": "Information about individual's political views and beliefs",
        "examples_vi": [
            "Đảng phái chính trị",
            "Quan điểm về chính sách",
            "Hoạt động chính trị"
        ],
        "examples_en": [
            "Political party affiliation",
            "Policy opinions",
            "Political activities"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "warning_vi": "Dữ liệu nhạy cảm - Yêu cầu bảo vệ cao"
    },
    "religious_beliefs": {
        "name_vi": "Tín ngưỡng, tôn giáo",
        "name_en": "Religious Beliefs",
        "pdpl_article": "Art. 4.13.b PDPL",
        "description_vi": "Thông tin về tôn giáo, tín ngưỡng, niềm tin tâm linh",
        "description_en": "Information about religion, beliefs, spiritual faith",
        "examples_vi": [
            "Tôn giáo theo đạo",
            "Tín ngưỡng dân gian",
            "Hoạt động tôn giáo"
        ],
        "examples_en": [
            "Religious affiliation",
            "Folk beliefs",
            "Religious activities"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "warning_vi": "Dữ liệu nhạy cảm - Yêu cầu bảo vệ cao"
    },
    "health_data": {
        "name_vi": "Thông tin sức khỏe",
        "name_en": "Health Information",
        "pdpl_article": "Art. 4.13.c PDPL",
        "description_vi": "Thông tin về tình trạng sức khỏe, bệnh sử, điều trị y tế",
        "description_en": "Information about health status, medical history, treatment",
        "examples_vi": [
            "Hồ sơ bệnh án",
            "Kết quả xét nghiệm",
            "Đơn thuốc",
            "Tiền sử bệnh lý",
            "Chẩn đoán bệnh"
        ],
        "examples_en": [
            "Medical records",
            "Test results",
            "Prescriptions",
            "Medical history",
            "Disease diagnosis"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "special_rules_vi": "Tuân thủ Luật Khám chữa bệnh 2009",
        "warning_vi": "Dữ liệu y tế - Bảo mật cao nhất"
    },
    "biometric_data": {
        "name_vi": "Dữ liệu sinh trắc học",
        "name_en": "Biometric Data",
        "pdpl_article": "Art. 4.13.d PDPL",
        "description_vi": "Dữ liệu đặc điểm sinh học để xác định danh tính cá nhân",
        "description_en": "Biological characteristics data for identification",
        "examples_vi": [
            "Vân tay",
            "Khuôn mặt",
            "Mống mắt/võng mạc",
            "Giọng nói",
            "DNA sinh trắc học"
        ],
        "examples_en": [
            "Fingerprints",
            "Facial recognition",
            "Iris/retina scan",
            "Voice recognition",
            "Biometric DNA"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "special_rules_vi": "Yêu cầu mã hóa và bảo mật đặc biệt",
        "warning_vi": "Dữ liệu sinh trắc học - Không thể thay đổi"
    },
    "genetic_data": {
        "name_vi": "Thông tin di truyền",
        "name_en": "Genetic Information",
        "pdpl_article": "Art. 4.13.e PDPL",
        "description_vi": "Thông tin về đặc điểm di truyền, gen, DNA",
        "description_en": "Information about genetic characteristics, genes, DNA",
        "examples_vi": [
            "Xét nghiệm gen",
            "Mã di truyền DNA",
            "Bệnh di truyền",
            "Cấu trúc gen"
        ],
        "examples_en": [
            "Genetic testing",
            "DNA code",
            "Hereditary diseases",
            "Gene structure"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "warning_vi": "Dữ liệu di truyền - Bảo mật tuyệt đối"
    },
    "sexual_orientation": {
        "name_vi": "Xu hướng tình dục",
        "name_en": "Sexual Orientation",
        "pdpl_article": "Art. 4.13.f PDPL",
        "description_vi": "Thông tin về xu hướng tình dục, giới tính cá nhân",
        "description_en": "Information about sexual orientation, gender identity",
        "examples_vi": [
            "Xu hướng tình dục",
            "Bản dạng giới",
            "Định hướng giới tính"
        ],
        "examples_en": [
            "Sexual orientation",
            "Gender identity",
            "Gender expression"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "warning_vi": "Dữ liệu nhạy cảm - Yêu cầu bảo vệ cao"
    },
    "criminal_records": {
        "name_vi": "Hồ sơ tư pháp",
        "name_en": "Criminal Records",
        "pdpl_article": "Art. 4.13.g PDPL",
        "description_vi": "Thông tin về tiền án, tiền sự, bản án hình sự",
        "description_en": "Information about criminal history, convictions",
        "examples_vi": [
            "Tiền án tiền sự",
            "Bản án hình sự",
            "Hồ sơ tư pháp",
            "Án tù giam"
        ],
        "examples_en": [
            "Criminal history",
            "Criminal convictions",
            "Judicial records",
            "Prison sentences"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "special_rules_vi": "Tuân thủ Luật Hình sự",
        "warning_vi": "Dữ liệu tư pháp - Bảo vệ đặc biệt"
    },
    "trade_union": {
        "name_vi": "Thông tin công đoàn",
        "name_en": "Trade Union Information",
        "pdpl_article": "Art. 4.13.h PDPL",
        "description_vi": "Thông tin về tham gia tổ chức công đoàn",
        "description_en": "Information about trade union membership",
        "examples_vi": [
            "Hội viên công đoàn",
            "Hoạt động công đoàn",
            "Vai trò trong công đoàn"
        ],
        "examples_en": [
            "Union membership",
            "Union activities",
            "Union role"
        ],
        "processing_requirements_vi": "Cần sự đồng ý rõ ràng (Điều 13.1 PDPL)",
        "warning_vi": "Dữ liệu nhạy cảm - Yêu cầu bảo vệ cao"
    },
    "children_data": {
        "name_vi": "Dữ liệu trẻ em",
        "name_en": "Children's Data",
        "pdpl_article": "Art. 4.13.i PDPL",
        "description_vi": "Thông tin cá nhân của trẻ em dưới 16 tuổi",
        "description_en": "Personal data of children under 16 years old",
        "examples_vi": [
            "Học sinh dưới 16 tuổi",
            "Trẻ em thiếu niên",
            "Dữ liệu học tập của trẻ"
        ],
        "examples_en": [
            "Students under 16",
            "Minors",
            "Children's educational data"
        ],
        "processing_requirements_vi": "Cần sự đồng ý của cha mẹ/người giám hộ (Điều 13.2 PDPL)",
        "special_rules_vi": "Yêu cầu sự đồng ý của cha mẹ hoặc người giám hộ hợp pháp",
        "warning_vi": "Dữ liệu trẻ em - Bảo vệ đặc biệt theo PDPL"
    }
}


# Category templates for wizard
WIZARD_CATEGORY_TEMPLATES: List[Dict[str, any]] = [
    {
        "template_key": "health_information",
        "category_name_vi": "Thông tin sức khỏe",
        "category_name_en": "Health Information",
        "category_description_vi": "Thông tin về tình trạng sức khỏe, bệnh sử, kết quả xét nghiệm, chẩn đoán và điều trị y tế của cá nhân",
        "category_description_en": "Information about health status, medical history, test results, diagnosis and medical treatment",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.c PDPL",
        "examples_vi": ["hồ sơ bệnh án", "kết quả xét nghiệm", "đơn thuốc", "chẩn đoán bệnh"],
        "examples_en": ["medical records", "test results", "prescriptions", "disease diagnosis"]
    },
    {
        "template_key": "biometric_data",
        "category_name_vi": "Dữ liệu sinh trắc học",
        "category_name_en": "Biometric Data",
        "category_description_vi": "Dữ liệu đặc điểm sinh học dùng để nhận dạng cá nhân như vân tay, khuôn mặt, mống mắt, giọng nói",
        "category_description_en": "Biological characteristics data for identification such as fingerprints, facial features, iris, voice",
        "category_type": "sensitive",
        "is_sensitive": True,
        "pdpl_article_reference": "Art. 4.13.d PDPL",
        "examples_vi": ["vân tay", "nhận dạng khuôn mặt", "quét mống mắt", "giọng nói"],
        "examples_en": ["fingerprints", "facial recognition", "iris scan", "voice recognition"]
    },
    {
        "template_key": "contact_information",
        "category_name_vi": "Thông tin liên hệ",
        "category_name_en": "Contact Information",
        "category_description_vi": "Thông tin để liên hệ với cá nhân bao gồm số điện thoại, email, địa chỉ",
        "category_description_en": "Contact information including phone number, email, address",
        "category_type": "basic",
        "is_sensitive": False,
        "pdpl_article_reference": "Art. 4.1 PDPL",
        "examples_vi": ["số điện thoại", "địa chỉ email", "địa chỉ nhà"],
        "examples_en": ["phone number", "email address", "home address"]
    }
]
```

---

## Vietnamese UI Components

### React Wizard Components

```typescript
// components/VeriPortal/VeriCategoryWizard/types.ts

/**
 * Category Wizard Types
 * Vietnamese-first Type Definitions
 */

export interface WizardStep {
  stepNumber: number;
  stepKey: string;
  stepNameVi: string;
  stepNameEn: string;
  descriptionVi: string;
  descriptionEn: string;
  required: boolean;
  pdplArticle: string;
  helpTextVi: string;
  validationRules: string[];
  conditional?: string;
}

export interface WizardState {
  currentStep: number;
  totalSteps: number;
  completedSteps: number[];
  stepData: Record<string, any>;
  validationErrors: Record<string, string>;
  isDraft: boolean;
  draftId?: string;
}

export interface CategoryFormData {
  categoryType: 'basic' | 'sensitive';
  categoryNameVi: string;
  categoryNameEn?: string;
  categoryDescriptionVi: string;
  categoryDescriptionEn?: string;
  sensitiveDataType?: string;
  examplesVi?: string[];
  examplesEn?: string[];
  pdplArticleReference?: string;
}

export interface PDPLHelpContext {
  nameVi: string;
  nameEn: string;
  pdplArticle: string;
  descriptionVi: string;
  descriptionEn: string;
  examplesVi: string[];
  examplesEn: string[];
  processingRequirementsVi: string;
  warningVi: string;
  specialRulesVi?: string;
}
```

```typescript
// components/VeriPortal/VeriCategoryWizard/VeriCategoryWizardSystem.tsx

/**
 * VeriPortal Category Creation Wizard
 * Vietnamese-first Guided UI
 */

import React, { useState } from 'react';
import { useCulturalIntelligence } from '../../../hooks/useCulturalIntelligence';
import type { WizardStep, WizardState, CategoryFormData } from './types';

export const VeriCategoryWizardSystem: React.FC = () => {
  const { isVietnamese, tCultural } = useCulturalIntelligence();
  
  const [wizardState, setWizardState] = useState<WizardState>({
    currentStep: 1,
    totalSteps: 7,
    completedSteps: [],
    stepData: {},
    validationErrors: {},
    isDraft: false
  });
  
  const [formData, setFormData] = useState<CategoryFormData>({
    categoryType: 'basic',
    categoryNameVi: '',
    categoryDescriptionVi: ''
  });
  
  // Step navigation
  const handleNextStep = () => {
    if (validateCurrentStep()) {
      setWizardState(prev => ({
        ...prev,
        currentStep: prev.currentStep + 1,
        completedSteps: [...prev.completedSteps, prev.currentStep]
      }));
    }
  };
  
  const handlePreviousStep = () => {
    setWizardState(prev => ({
      ...prev,
      currentStep: Math.max(1, prev.currentStep - 1)
    }));
  };
  
  // Validation
  const validateCurrentStep = (): boolean => {
    const errors: Record<string, string> = {};
    
    // Step-specific validation
    switch (wizardState.currentStep) {
      case 1:
        if (!formData.categoryType) {
          errors.categoryType = isVietnamese
            ? 'Vui lòng chọn loại danh mục'
            : 'Please select category type';
        }
        break;
      
      case 2:
        if (!formData.categoryNameVi || formData.categoryNameVi.length < 3) {
          errors.categoryNameVi = isVietnamese
            ? 'Tên danh mục phải có ít nhất 3 ký tự'
            : 'Category name must be at least 3 characters';
        }
        // Check Vietnamese diacritics
        if (!/[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i.test(formData.categoryNameVi)) {
          errors.categoryNameVi = isVietnamese
            ? 'Tên danh mục tiếng Việt phải có dấu'
            : 'Vietnamese category name must have diacritics';
        }
        break;
      
      case 4:
        if (!formData.categoryDescriptionVi || formData.categoryDescriptionVi.length < 10) {
          errors.categoryDescriptionVi = isVietnamese
            ? 'Mô tả phải có ít nhất 10 ký tự'
            : 'Description must be at least 10 characters';
        }
        break;
      
      case 5:
        if (formData.categoryType === 'sensitive' && !formData.sensitiveDataType) {
          errors.sensitiveDataType = isVietnamese
            ? 'Vui lòng chọn loại dữ liệu nhạy cảm theo PDPL'
            : 'Please select PDPL sensitive data type';
        }
        break;
    }
    
    setWizardState(prev => ({ ...prev, validationErrors: errors }));
    return Object.keys(errors).length === 0;
  };
  
  // Draft management
  const handleSaveDraft = async () => {
    // Save to backend
    const draftId = await saveDraft(formData);
    setWizardState(prev => ({ ...prev, isDraft: true, draftId }));
  };
  
  // Progress calculation
  const progressPercentage = (wizardState.completedSteps.length / wizardState.totalSteps) * 100;
  
  return (
    <div className="veri-category-wizard">
      {/* Progress bar */}
      <div className="wizard-progress">
        <div className="progress-bar" style={{ width: `${progressPercentage}%` }} />
        <span className="progress-text">
          {isVietnamese 
            ? `Bước ${wizardState.currentStep}/${wizardState.totalSteps}` 
            : `Step ${wizardState.currentStep}/${wizardState.totalSteps}`}
        </span>
      </div>
      
      {/* Step content */}
      <div className="wizard-step-content">
        {renderStepContent()}
      </div>
      
      {/* Navigation buttons */}
      <div className="wizard-navigation">
        {wizardState.currentStep > 1 && (
          <button onClick={handlePreviousStep}>
            {isVietnamese ? 'Quay lại' : 'Previous'}
          </button>
        )}
        
        <button onClick={handleSaveDraft} className="save-draft">
          {isVietnamese ? 'Lưu nháp' : 'Save Draft'}
        </button>
        
        {wizardState.currentStep < wizardState.totalSteps ? (
          <button onClick={handleNextStep} className="primary">
            {isVietnamese ? 'Tiếp theo' : 'Next'}
          </button>
        ) : (
          <button onClick={handleSubmit} className="primary">
            {isVietnamese ? 'Tạo danh mục' : 'Create Category'}
          </button>
        )}
      </div>
    </div>
  );
};
```

---

## Validation and Error Handling

### Real-time Validation

```python
# api/models/wizard_models.py

"""
Wizard Models
Vietnamese-first Wizard Data
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
import re


class WizardDraftData(BaseModel):
    """
    Dữ liệu wizard draft
    Wizard draft data
    
    Saves in-progress wizard state
    """
    
    draft_id: UUID
    wizard_type: WizardType
    current_step: int
    
    form_data: Dict[str, any] = Field(
        ...,
        description="Dữ liệu form | Form data"
    )
    
    completed_steps: List[int] = Field(
        default_factory=list,
        description="Các bước đã hoàn thành | Completed steps"
    )
    
    validation_errors: Dict[str, str] = Field(
        default_factory=dict,
        description="Lỗi validation | Validation errors"
    )
    
    created_at: datetime
    updated_at: datetime
    expires_at: datetime  # Auto-delete after 7 days
    
    class Config:
        json_schema_extra = {
            "example": {
                "draft_id": "ff0e8400-e29b-41d4-a716-446655440030",
                "wizard_type": "category_creation",
                "current_step": 4,
                "form_data": {
                    "categoryType": "sensitive",
                    "categoryNameVi": "Thông tin sức khỏe",
                    "categoryDescriptionVi": "Thông tin về tình trạng sức khỏe..."
                },
                "completed_steps": [1, 2, 3],
                "validation_errors": {},
                "created_at": "2025-11-06T22:00:00+07:00",
                "updated_at": "2025-11-06T22:15:00+07:00",
                "expires_at": "2025-11-13T22:00:00+07:00"
            }
        }


class WizardSubmissionRequest(BaseModel):
    """
    Yêu cầu gửi wizard
    Wizard submission request
    
    Final wizard submission
    """
    
    wizard_type: WizardType
    category_type: str
    
    category_name_vi: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Tên danh mục tiếng Việt | Vietnamese category name"
    )
    
    category_name_en: Optional[str] = Field(
        None,
        max_length=200,
        description="Tên danh mục tiếng Anh | English category name"
    )
    
    category_description_vi: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Mô tả danh mục tiếng Việt | Vietnamese category description"
    )
    
    category_description_en: Optional[str] = Field(
        None,
        max_length=2000,
        description="Mô tả danh mục tiếng Anh | English category description"
    )
    
    sensitive_data_type: Optional[str]
    examples_vi: Optional[List[str]]
    examples_en: Optional[List[str]]
    
    draft_id: Optional[UUID]
    
    @validator('category_name_vi')
    def validate_vietnamese_diacritics(cls, v):
        """Kiểm tra dấu tiếng Việt"""
        vietnamese_pattern = re.compile(
            r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]',
            re.IGNORECASE
        )
        if not vietnamese_pattern.search(v):
            raise ValueError(
                "Tên danh mục tiếng Việt phải có dấu (Vietnamese name must have diacritics)"
            )
        return v
    
    @validator('category_type')
    def validate_sensitive_consistency(cls, v, values):
        """Kiểm tra tính nhất quán sensitive"""
        if v == 'sensitive' and 'sensitive_data_type' not in values:
            raise ValueError(
                "Danh mục nhạy cảm phải chọn loại dữ liệu theo PDPL (Sensitive category must select PDPL data type)"
            )
        return v
```

---

## Draft Management

### Auto-save and Resume

```python
# services/wizard/draft_manager.py

"""
Wizard Draft Manager
Auto-save and Resume Functionality
"""

from typing import Optional
from datetime import datetime, timedelta
from uuid import UUID


class WizardDraftManager:
    """
    Quản lý wizard draft
    Wizard draft manager
    
    Auto-save and resume wizards
    """
    
    # Auto-save interval (seconds)
    AUTO_SAVE_INTERVAL = 30
    
    # Draft expiration (days)
    DRAFT_EXPIRATION_DAYS = 7
    
    async def save_draft(
        self,
        wizard_type: WizardType,
        form_data: Dict[str, any],
        current_step: int,
        user_id: UUID,
        draft_id: Optional[UUID] = None
    ) -> UUID:
        """
        Lưu draft
        Save wizard draft
        
        Returns draft_id
        """
        expires_at = datetime.now() + timedelta(days=self.DRAFT_EXPIRATION_DAYS)
        
        if draft_id:
            # Update existing draft
            await self._update_draft(draft_id, form_data, current_step)
        else:
            # Create new draft
            draft_id = await self._create_draft(
                wizard_type=wizard_type,
                form_data=form_data,
                current_step=current_step,
                user_id=user_id,
                expires_at=expires_at
            )
        
        return draft_id
    
    async def load_draft(self, draft_id: UUID) -> Optional[WizardDraftData]:
        """
        Tải draft
        Load wizard draft
        
        Returns draft data or None if expired
        """
        draft = await self._get_draft(draft_id)
        
        if draft and draft.expires_at > datetime.now():
            return draft
        
        return None
    
    async def delete_draft(self, draft_id: UUID) -> bool:
        """
        Xóa draft
        Delete wizard draft
        """
        return await self._delete_draft(draft_id)
    
    async def cleanup_expired_drafts(self) -> int:
        """
        Dọn dẹp draft hết hạn
        Cleanup expired drafts
        
        Returns number of deleted drafts
        """
        return await self._delete_expired_drafts()
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] 7-step wizard flow configuration
- [TARGET] PDPL Article 4.13 help context (9 sensitive data types)
- [TARGET] Vietnamese-first React components
- [TARGET] Real-time validation with Vietnamese diacritics check
- [TARGET] Category templates with examples
- [TARGET] Draft save/resume functionality
- [TARGET] Auto-save every 30 seconds
- [TARGET] Progress tracking with completion percentage
- [TARGET] Conditional step logic (sensitive data type selection)
- [TARGET] Vietnamese error messages
- [TARGET] Zero hard-coding (all steps in configuration)
- [TARGET] Bilingual UI support

**Next Document:** #05 - Database Seeding
