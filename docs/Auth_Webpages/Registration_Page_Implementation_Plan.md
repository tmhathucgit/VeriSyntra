# VeriSyntra Registration Page - Implementation Plan

**Date:** 2025-11-01  
**Component:** User Registration Page  
**Route:** `/register`  
**API Endpoint:** `http://localhost:8001/api/v1/auth/register`  
**Status:** Planning Phase

---

## 1. Overview

### Purpose
Create a bilingual (Vietnamese/English) registration page that allows new businesses to sign up for VeriSyntra PDPL 2025 compliance platform, creating both a tenant (company) and the first admin user account.

### User Flow
```
Landing Page (/) 
  -> Click "Get Started" / "Đăng ký ngay"
  -> Registration Page (/register) [NEW]
  -> Fill multi-step form:
     Step 1: Company Information (Vietnamese business details)
     Step 2: User Account (Admin user credentials)
     Step 3: Regional & Industry Context (Vietnamese business context)
  -> Submit registration
  -> Auth Service creates tenant + user (PostgreSQL)
  -> Redirect to Email Verification page
  -> After verification -> Login -> Dashboard
```

### Key Requirements
- [X] Multi-step form (3 steps: Company -> User -> Business Context)
- [X] Bilingual UI (Vietnamese-first with English toggle)
- [X] Integration with auth service API (`/api/v1/auth/register`)
- [X] Vietnamese business validation (tax ID, phone number format)
- [X] Regional location selection (North/Central/South Vietnam)
- [X] Industry type selection with Vietnamese context
- [X] Form validation with Vietnamese error messages
- [X] Progress indicator (Step 1 of 3, 2 of 3, 3 of 3)
- [X] Responsive design matching VeriSyntra brand colors
- [X] Password strength indicator
- [X] Terms of service acceptance
- [X] Link to login page (for existing users)

---

## 2. Technical Architecture

### File Structure
```
src/
├── components/
│   └── Auth/
│       ├── Register/
│       │   ├── RegisterPage.tsx              # Main registration component
│       │   ├── RegistrationWizard.tsx        # Multi-step wizard container
│       │   ├── steps/
│       │   │   ├── CompanyInfoStep.tsx       # Step 1: Company details
│       │   │   ├── UserAccountStep.tsx       # Step 2: Admin user
│       │   │   └── BusinessContextStep.tsx   # Step 3: Vietnamese context
│       │   ├── ProgressIndicator.tsx         # Visual step progress
│       │   ├── PasswordStrengthMeter.tsx     # Password strength UI
│       │   └── types.ts                      # TypeScript interfaces
│       └── shared/
│           └── AuthLayout.tsx                # Shared with login page
├── services/
│   └── auth/
│       └── authService.ts                    # API calls (add register method)
└── locales/
    ├── vi/
    │   └── auth.json                         # Add registration translations
    └── en/
        └── auth.json                         # Add registration translations
```

### State Management
```typescript
// Registration form state (React Hook Form + multi-step)
interface RegistrationData {
  // Step 1: Company Information
  company: {
    company_name: string;
    company_name_vi: string;
    tax_id: string;                 // Vietnamese tax ID format
    phone_number: string;           // Vietnamese phone format: +84 xxx xxx xxx
    address?: string;
    city?: string;
  };
  
  // Step 2: User Account
  user: {
    email: string;
    password: string;
    confirmPassword: string;
    full_name: string;
    full_name_vi: string;
    phone_number: string;
    preferred_language: 'vi' | 'en';
  };
  
  // Step 3: Business Context
  businessContext: {
    veri_regional_location: 'north' | 'central' | 'south';
    veri_industry_type: string;     // technology, manufacturing, finance, etc.
    company_size?: string;          // small, medium, large
    employee_count?: number;
  };
  
  // Agreements
  termsAccepted: boolean;
  privacyAccepted: boolean;
}
```

---

## 3. API Integration

### Registration Endpoint
**URL:** `POST http://localhost:8001/api/v1/auth/register`

**Request Body:**
```typescript
interface VeriUserCreate {
  // User fields
  email: string;                    // Required
  password: string;                 // Required: min 8 chars
  full_name: string;                // Required
  full_name_vi: string;             // Required
  phone_number: string;             // Required: Vietnamese format
  preferred_language?: 'vi' | 'en'; // Optional: default 'vi'
  
  // Company/Tenant fields
  company_name: string;             // Required
  company_name_vi: string;          // Required
  tax_id: string;                   // Required: Vietnamese tax ID
  
  // Business context fields
  veri_regional_location: 'north' | 'central' | 'south'; // Required
  veri_industry_type: string;       // Required
}
```

**Example Request:**
```json
{
  "email": "admin@acme.vn",
  "password": "SecurePass123!",
  "full_name": "Nguyen Van Admin",
  "full_name_vi": "Nguyễn Văn Admin",
  "phone_number": "+84 901 234 567",
  "preferred_language": "vi",
  "company_name": "ACME Vietnam",
  "company_name_vi": "ACME Việt Nam",
  "tax_id": "0123456789",
  "veri_regional_location": "south",
  "veri_industry_type": "technology"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Dang ky thanh cong / Registration successful",
  "english": "Registration successful",
  "user_id": "fc322cf2-4171-4854-a3f1-592b274166da",
  "tenant_id": "0511779f-b6cc-4dcb-9319-033fdb6b7d92",
  "email": "admin@acme.vn",
  "verification_required": true,
  "next_steps": {
    "vi": "Vui long xac thuc email de kich hoat tai khoan",
    "en": "Please verify your email to activate your account"
  }
}
```

**Error Response (400 Bad Request - Email exists):**
```json
{
  "detail": {
    "message": "Email da ton tai / Email already exists",
    "english": "Email already exists"
  }
}
```

**Error Response (400 Bad Request - Tax ID exists):**
```json
{
  "detail": {
    "message": "Ma so thue da ton tai / Tax ID already exists",
    "english": "Tax ID already exists"
  }
}
```

**Error Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "phone_number"],
      "msg": "String should match pattern '^\\+84\\s?\\d{3}\\s?\\d{3}\\s?\\d{3,4}$'",
      "input": "0901234567",
      "ctx": {
        "pattern": "^\\+84\\s?\\d{3}\\s?\\d{3}\\s?\\d{3,4}$"
      }
    }
  ]
}
```

---

## 4. UI/UX Design Specifications

### Multi-Step Form Layout
```
┌─────────────────────────────────────────────────────────┐
│  [VN Map Logo]  VeriSyntra                   [🇻🇳 VI ▼] │ <- Header
├─────────────────────────────────────────────────────────┤
│                                                         │
│     Đăng ký tài khoản VeriSyntra                       │ <- Title
│     Register VeriSyntra Account                        │
│                                                         │
│     [●━━━━━━━━━○━━━━━━━━━○]                           │ <- Progress
│      Công ty    Tài khoản   Ngành nghề                 │    Indicator
│                                                         │
│     ┌──────────────────────────────────────┐          │
│     │  BƯỚC 1: THÔNG TIN CÔNG TY            │          │
│     │  STEP 1: COMPANY INFORMATION          │          │
│     │                                        │          │
│     │  ┌────────────────────────────┐       │          │
│     │  │ Tên công ty (tiếng Việt) * │       │          │
│     │  │ ACME Việt Nam              │       │          │
│     │  └────────────────────────────┘       │          │
│     │                                        │          │
│     │  ┌────────────────────────────┐       │          │
│     │  │ Company name (English) *   │       │          │
│     │  │ ACME Vietnam               │       │          │
│     │  └────────────────────────────┘       │          │
│     │                                        │          │
│     │  ┌────────────────────────────┐       │          │
│     │  │ Mã số thuế *               │       │          │
│     │  │ 0123456789                 │       │          │
│     │  └────────────────────────────┘       │          │
│     │                                        │          │
│     │  ┌────────────────────────────┐       │          │
│     │  │ Số điện thoại *            │       │          │
│     │  │ +84 901 234 567            │       │          │
│     │  └────────────────────────────┘       │          │
│     │                                        │          │
│     │         [←  Quay lại]  [Tiếp tục  →]  │          │
│     │         [←  Back]      [Next  →]      │          │
│     └──────────────────────────────────────┘          │
│                                                         │
│     Đã có tài khoản? Đăng nhập ngay                    │ <- Login Link
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Step Breakdown

**Step 1: Company Information**
- Company name (Vietnamese) *required
- Company name (English) *required
- Tax ID (Mã số thuế) *required - 10 digits
- Phone number *required - Vietnamese format
- Address (optional)
- City (optional)

**Step 2: User Account**
- Full name (Vietnamese) *required
- Full name (English) *required
- Email *required
- Phone number *required - Vietnamese format
- Password *required - min 8 chars, with strength meter
- Confirm password *required - must match
- Preferred language (Vietnamese/English)

**Step 3: Business Context**
- Regional location *required - Radio buttons:
  ```
  ○ Miền Bắc (North) - Formal, hierarchical
  ○ Miền Trung (Central) - Traditional, consensus
  ○ Miền Nam (South) - Entrepreneurial, fast-paced
  ```
- Industry type *required - Dropdown:
  ```
  - Công nghệ / Technology
  - Sản xuất / Manufacturing
  - Tài chính / Finance
  - Y tế / Healthcare
  - Giáo dục / Education
  - Bán lẻ / Retail
  - Du lịch / Tourism
  - Khác / Other
  ```
- Company size (optional)
- Employee count (optional)
- Terms of service checkbox *required
- Privacy policy checkbox *required

---

## 5. Form Validation Rules

### Vietnamese-Specific Validation

**Tax ID (Mã số thuế)**
```typescript
const validateTaxId = (value: string): boolean | string => {
  // Vietnamese tax ID: 10 or 13 digits
  const pattern = /^\d{10}(\d{3})?$/;
  if (!pattern.test(value)) {
    return isVietnamese 
      ? 'Mã số thuế phải có 10 hoặc 13 chữ số'
      : 'Tax ID must be 10 or 13 digits';
  }
  return true;
};
```

**Phone Number (Vietnamese format)**
```typescript
const validateVietnamesePhone = (value: string): boolean | string => {
  // Format: +84 xxx xxx xxx or +84 xxx xxx xxxx
  const pattern = /^\+84\s?\d{3}\s?\d{3}\s?\d{3,4}$/;
  if (!pattern.test(value)) {
    return isVietnamese
      ? 'Số điện thoại phải theo định dạng +84 xxx xxx xxx'
      : 'Phone number must be in format +84 xxx xxx xxx';
  }
  return true;
};

// Auto-format phone number
const formatPhoneNumber = (value: string): string => {
  // Remove all non-digits
  const digits = value.replace(/\D/g, '');
  
  // If starts with 0, replace with +84
  if (digits.startsWith('0')) {
    return '+84 ' + digits.slice(1).replace(/(\d{3})(\d{3})(\d{3,4})/, '$1 $2 $3');
  }
  
  // If starts with 84, add +
  if (digits.startsWith('84')) {
    return '+' + digits.replace(/(\d{2})(\d{3})(\d{3})(\d{3,4})/, '$1 $2 $3 $4');
  }
  
  return value;
};
```

**Password Strength**
```typescript
interface PasswordStrength {
  score: 0 | 1 | 2 | 3 | 4;
  label: {
    vi: string;
    en: string;
  };
  color: string;
  suggestions: string[];
}

const evaluatePasswordStrength = (password: string): PasswordStrength => {
  let score = 0;
  const suggestions: string[] = [];
  
  // Length check
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  else suggestions.push(
    isVietnamese 
      ? 'Sử dụng ít nhất 12 ký tự'
      : 'Use at least 12 characters'
  );
  
  // Complexity checks
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
  else suggestions.push(
    isVietnamese
      ? 'Kết hợp chữ hoa và chữ thường'
      : 'Mix uppercase and lowercase'
  );
  
  if (/\d/.test(password)) score++;
  else suggestions.push(
    isVietnamese ? 'Thêm số' : 'Add numbers'
  );
  
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;
  else suggestions.push(
    isVietnamese ? 'Thêm ký tự đặc biệt' : 'Add special characters'
  );
  
  // Score to label mapping
  const labels = {
    0: { vi: 'Rất yếu', en: 'Very Weak', color: '#c17a7a' },
    1: { vi: 'Yếu', en: 'Weak', color: '#d4c18a' },
    2: { vi: 'Trung bình', en: 'Fair', color: '#9db09d' },
    3: { vi: 'Mạnh', en: 'Strong', color: '#7fa3c3' },
    4: { vi: 'Rất mạnh', en: 'Very Strong', color: '#6b8e6b' }
  };
  
  return {
    score: Math.min(score, 4) as 0 | 1 | 2 | 3 | 4,
    label: labels[Math.min(score, 4)],
    color: labels[Math.min(score, 4)].color,
    suggestions: score < 4 ? suggestions : []
  };
};
```

### Complete Validation Rules
```typescript
const validationRules = {
  // Step 1: Company
  company_name_vi: {
    required: {
      vi: 'Vui lòng nhập tên công ty (tiếng Việt)',
      en: 'Company name (Vietnamese) is required'
    },
    minLength: {
      value: 2,
      message: {
        vi: 'Tên công ty phải có ít nhất 2 ký tự',
        en: 'Company name must be at least 2 characters'
      }
    }
  },
  company_name: {
    required: {
      vi: 'Vui lòng nhập tên công ty (tiếng Anh)',
      en: 'Company name (English) is required'
    }
  },
  tax_id: {
    required: {
      vi: 'Vui lòng nhập mã số thuế',
      en: 'Tax ID is required'
    },
    validate: validateTaxId
  },
  company_phone: {
    required: {
      vi: 'Vui lòng nhập số điện thoại công ty',
      en: 'Company phone number is required'
    },
    validate: validateVietnamesePhone
  },
  
  // Step 2: User Account
  full_name_vi: {
    required: {
      vi: 'Vui lòng nhập họ tên (tiếng Việt)',
      en: 'Full name (Vietnamese) is required'
    }
  },
  full_name: {
    required: {
      vi: 'Vui lòng nhập họ tên (tiếng Anh)',
      en: 'Full name (English) is required'
    }
  },
  email: {
    required: {
      vi: 'Vui lòng nhập địa chỉ email',
      en: 'Email address is required'
    },
    pattern: {
      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
      message: {
        vi: 'Địa chỉ email không hợp lệ',
        en: 'Invalid email address'
      }
    }
  },
  password: {
    required: {
      vi: 'Vui lòng nhập mật khẩu',
      en: 'Password is required'
    },
    minLength: {
      value: 8,
      message: {
        vi: 'Mật khẩu phải có ít nhất 8 ký tự',
        en: 'Password must be at least 8 characters'
      }
    },
    validate: (value: string) => {
      const strength = evaluatePasswordStrength(value);
      if (strength.score < 2) {
        return isVietnamese
          ? 'Mật khẩu quá yếu. Vui lòng chọn mật khẩu mạnh hơn.'
          : 'Password is too weak. Please choose a stronger password.';
      }
      return true;
    }
  },
  confirmPassword: {
    required: {
      vi: 'Vui lòng xác nhận mật khẩu',
      en: 'Please confirm your password'
    },
    validate: (value: string, formValues: any) => {
      return value === formValues.password || (
        isVietnamese
          ? 'Mật khẩu xác nhận không khớp'
          : 'Passwords do not match'
      );
    }
  },
  
  // Step 3: Business Context
  veri_regional_location: {
    required: {
      vi: 'Vui lòng chọn khu vực kinh doanh',
      en: 'Please select business region'
    }
  },
  veri_industry_type: {
    required: {
      vi: 'Vui lòng chọn ngành nghề',
      en: 'Please select industry type'
    }
  },
  termsAccepted: {
    required: {
      vi: 'Bạn phải đồng ý với điều khoản sử dụng',
      en: 'You must accept the terms of service'
    }
  },
  privacyAccepted: {
    required: {
      vi: 'Bạn phải đồng ý với chính sách bảo mật',
      en: 'You must accept the privacy policy'
    }
  }
};
```

---

## 6. Vietnamese Regional Context UI

### Regional Location Selector
```typescript
const regionalLocations = [
  {
    value: 'north',
    label: { vi: 'Miền Bắc', en: 'Northern Vietnam' },
    description: {
      vi: 'Hà Nội và các tỉnh phía Bắc - Phong cách chính thống, thứ bậc rõ ràng',
      en: 'Hanoi and Northern provinces - Formal, hierarchical style'
    },
    icon: '🏛️',
    characteristics: {
      vi: ['Quyết định có cấu trúc', 'Giao tiếp chính thống', 'Tuân thủ nghiêm ngặt'],
      en: ['Structured decisions', 'Formal communication', 'Strict compliance']
    }
  },
  {
    value: 'central',
    label: { vi: 'Miền Trung', en: 'Central Vietnam' },
    description: {
      vi: 'Đà Nẵng, Huế và các tỉnh miền Trung - Bảo tồn văn hóa, xây dựng đồng thuận',
      en: 'Da Nang, Hue and Central provinces - Cultural preservation, consensus-building'
    },
    icon: '🏯',
    characteristics: {
      vi: ['Quyết định đồng thuận', 'Giá trị truyền thống', 'Kỹ lưỡng cẩn thận'],
      en: ['Consensus decisions', 'Traditional values', 'Thorough approach']
    }
  },
  {
    value: 'south',
    label: { vi: 'Miền Nam', en: 'Southern Vietnam' },
    description: {
      vi: 'TP. Hồ Chí Minh và các tỉnh phía Nam - Năng động, đổi mới, quốc tế hóa',
      en: 'Ho Chi Minh City and Southern provinces - Dynamic, innovative, international'
    },
    icon: '🏙️',
    characteristics: {
      vi: ['Quyết định nhanh', 'Tinh thần khởi nghiệp', 'Hội nhập quốc tế'],
      en: ['Fast decisions', 'Entrepreneurial spirit', 'International integration']
    }
  }
];

// UI Component
<div className="space-y-4">
  {regionalLocations.map((region) => (
    <label
      key={region.value}
      className={`veri-radio-card ${
        selectedRegion === region.value ? 'selected' : ''
      }`}
    >
      <input
        type="radio"
        value={region.value}
        {...register('veri_regional_location')}
        className="veri-radio"
      />
      <div className="flex items-start space-x-4">
        <span className="text-4xl">{region.icon}</span>
        <div className="flex-1">
          <div className="font-semibold text-lg">
            {isVietnamese ? region.label.vi : region.label.en}
          </div>
          <p className="text-sm text-gray-600 mt-1">
            {isVietnamese ? region.description.vi : region.description.en}
          </p>
          <div className="flex flex-wrap gap-2 mt-2">
            {(isVietnamese ? region.characteristics.vi : region.characteristics.en).map((char, idx) => (
              <span
                key={idx}
                className="text-xs px-2 py-1 rounded-full"
                style={{
                  backgroundColor: 'rgba(107, 142, 107, 0.1)',
                  color: '#6b8e6b'
                }}
              >
                {char}
              </span>
            ))}
          </div>
        </div>
      </div>
    </label>
  ))}
</div>
```

### Industry Type Selector
```typescript
const industryTypes = [
  { value: 'technology', label: { vi: 'Công nghệ', en: 'Technology' }, icon: '💻' },
  { value: 'manufacturing', label: { vi: 'Sản xuất', en: 'Manufacturing' }, icon: '🏭' },
  { value: 'finance', label: { vi: 'Tài chính', en: 'Finance' }, icon: '💰' },
  { value: 'healthcare', label: { vi: 'Y tế', en: 'Healthcare' }, icon: '🏥' },
  { value: 'education', label: { vi: 'Giáo dục', en: 'Education' }, icon: '🎓' },
  { value: 'retail', label: { vi: 'Bán lẻ', en: 'Retail' }, icon: '🛒' },
  { value: 'tourism', label: { vi: 'Du lịch', en: 'Tourism' }, icon: '✈️' },
  { value: 'food_beverage', label: { vi: 'Thực phẩm & Đồ uống', en: 'Food & Beverage' }, icon: '🍽️' },
  { value: 'real_estate', label: { vi: 'Bất động sản', en: 'Real Estate' }, icon: '🏢' },
  { value: 'logistics', label: { vi: 'Vận tải & Logistics', en: 'Logistics' }, icon: '🚚' },
  { value: 'other', label: { vi: 'Khác', en: 'Other' }, icon: '📋' }
];
```

---

## 7. Code Templates

### RegisterPage.tsx (Main Component)
```typescript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useForm, FormProvider } from 'react-hook-form';
import AuthLayout from '../shared/AuthLayout';
import ProgressIndicator from './ProgressIndicator';
import CompanyInfoStep from './steps/CompanyInfoStep';
import UserAccountStep from './steps/UserAccountStep';
import BusinessContextStep from './steps/BusinessContextStep';
import { authService } from '../../services/auth/authService';

interface RegistrationFormData {
  // Step 1
  company_name_vi: string;
  company_name: string;
  tax_id: string;
  company_phone: string;
  
  // Step 2
  full_name_vi: string;
  full_name: string;
  email: string;
  user_phone: string;
  password: string;
  confirmPassword: string;
  preferred_language: 'vi' | 'en';
  
  // Step 3
  veri_regional_location: 'north' | 'central' | 'south';
  veri_industry_type: string;
  termsAccepted: boolean;
  privacyAccepted: boolean;
}

function RegisterPage() {
  const { t } = useTranslation('auth');
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const methods = useForm<RegistrationFormData>({
    mode: 'onBlur',
    defaultValues: {
      preferred_language: 'vi',
      termsAccepted: false,
      privacyAccepted: false
    }
  });

  const { handleSubmit, trigger } = methods;

  const steps = [
    {
      number: 1,
      title: { vi: 'Thông tin công ty', en: 'Company Info' },
      component: CompanyInfoStep
    },
    {
      number: 2,
      title: { vi: 'Tài khoản', en: 'Account' },
      component: UserAccountStep
    },
    {
      number: 3,
      title: { vi: 'Ngành nghề', en: 'Business Context' },
      component: BusinessContextStep
    }
  ];

  const handleNext = async () => {
    const fieldsToValidate = getFieldsForStep(currentStep);
    const isValid = await trigger(fieldsToValidate);
    
    if (isValid) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    setCurrentStep(currentStep - 1);
  };

  const onSubmit = async (data: RegistrationFormData) => {
    setIsSubmitting(true);
    setError(null);

    try {
      // Transform form data to API format
      const registrationData = {
        email: data.email,
        password: data.password,
        full_name: data.full_name,
        full_name_vi: data.full_name_vi,
        phone_number: data.user_phone,
        preferred_language: data.preferred_language,
        company_name: data.company_name,
        company_name_vi: data.company_name_vi,
        tax_id: data.tax_id,
        veri_regional_location: data.veri_regional_location,
        veri_industry_type: data.veri_industry_type
      };

      const response = await authService.register(registrationData);

      // Success - redirect to email verification page
      navigate('/verify-email', {
        state: {
          email: data.email,
          userId: response.user_id,
          message: response.message
        }
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Registration failed';
      setError(message);
      setIsSubmitting(false);
    }
  };

  const CurrentStepComponent = steps[currentStep - 1].component;

  return (
    <AuthLayout
      title={t('register.title')}
      subtitle={t('register.subtitle')}
    >
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
          {/* Progress Indicator */}
          <ProgressIndicator
            steps={steps}
            currentStep={currentStep}
          />

          {/* Current Step Content */}
          <CurrentStepComponent />

          {/* Error Message */}
          {error && (
            <div className="veri-error-banner">
              {error}
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between pt-6">
            <button
              type="button"
              onClick={handleBack}
              disabled={currentStep === 1}
              className="veri-button-secondary"
            >
              {t('register.navigation.back')}
            </button>

            {currentStep < 3 ? (
              <button
                type="button"
                onClick={handleNext}
                className="veri-button-primary"
              >
                {t('register.navigation.next')}
              </button>
            ) : (
              <button
                type="submit"
                disabled={isSubmitting}
                className="veri-button-primary"
              >
                {isSubmitting 
                  ? t('register.navigation.submitting')
                  : t('register.navigation.submit')
                }
              </button>
            )}
          </div>

          {/* Login Link */}
          <p className="text-center text-sm text-gray-600 pt-4">
            {t('register.hasAccount')}{' '}
            <Link
              to="/login"
              className="font-medium hover:underline"
              style={{ color: 'var(--veri-green)' }}
            >
              {t('register.loginLink')}
            </Link>
          </p>
        </form>
      </FormProvider>
    </AuthLayout>
  );
}

export default RegisterPage;
```

### PasswordStrengthMeter.tsx
```typescript
import { useTranslation } from 'react-i18next';

interface PasswordStrengthMeterProps {
  password: string;
}

function PasswordStrengthMeter({ password }: PasswordStrengthMeterProps) {
  const { t, i18n } = useTranslation('auth');
  const isVietnamese = i18n.language === 'vi';

  const evaluateStrength = (pwd: string) => {
    let score = 0;
    if (pwd.length >= 8) score++;
    if (pwd.length >= 12) score++;
    if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) score++;
    if (/\d/.test(pwd)) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) score++;
    return Math.min(score, 4);
  };

  const strength = evaluateStrength(password);

  const strengthLabels = [
    { vi: 'Rất yếu', en: 'Very Weak', color: '#c17a7a' },
    { vi: 'Yếu', en: 'Weak', color: '#d4c18a' },
    { vi: 'Trung bình', en: 'Fair', color: '#9db09d' },
    { vi: 'Mạnh', en: 'Strong', color: '#7fa3c3' },
    { vi: 'Rất mạnh', en: 'Very Strong', color: '#6b8e6b' }
  ];

  if (!password) return null;

  return (
    <div className="mt-2">
      <div className="flex gap-1 mb-2">
        {[0, 1, 2, 3, 4].map((level) => (
          <div
            key={level}
            className="h-1.5 flex-1 rounded-full transition-all"
            style={{
              backgroundColor: level <= strength 
                ? strengthLabels[strength].color 
                : '#e5e7eb'
            }}
          />
        ))}
      </div>
      <p
        className="text-sm font-medium"
        style={{ color: strengthLabels[strength].color }}
      >
        {isVietnamese 
          ? strengthLabels[strength].vi 
          : strengthLabels[strength].en
        }
      </p>
    </div>
  );
}

export default PasswordStrengthMeter;
```

---

## 8. Translation Keys

### Vietnamese (`locales/vi/auth.json`)
```json
{
  "register": {
    "title": "Đăng ký tài khoản",
    "subtitle": "Tạo tài khoản VeriSyntra mới",
    "steps": {
      "company": "Thông tin công ty",
      "account": "Tài khoản",
      "context": "Ngành nghề"
    },
    "companyStep": {
      "title": "Thông tin công ty",
      "companyNameVi": "Tên công ty (tiếng Việt)",
      "companyNameViPlaceholder": "VD: Công ty TNHH ABC",
      "companyName": "Tên công ty (tiếng Anh)",
      "companyNamePlaceholder": "e.g., ABC Company Ltd",
      "taxId": "Mã số thuế",
      "taxIdPlaceholder": "10 hoặc 13 chữ số",
      "taxIdHelp": "Mã số thuế doanh nghiệp do Cục Thuế cấp",
      "phone": "Số điện thoại công ty",
      "phonePlaceholder": "+84 901 234 567"
    },
    "accountStep": {
      "title": "Tạo tài khoản quản trị",
      "fullNameVi": "Họ và tên (tiếng Việt)",
      "fullNameViPlaceholder": "Nguyễn Văn A",
      "fullName": "Họ và tên (tiếng Anh)",
      "fullNamePlaceholder": "Nguyen Van A",
      "email": "Địa chỉ email",
      "emailPlaceholder": "admin@congty.vn",
      "phone": "Số điện thoại",
      "phonePlaceholder": "+84 901 234 567",
      "password": "Mật khẩu",
      "passwordPlaceholder": "Tối thiểu 8 ký tự",
      "confirmPassword": "Xác nhận mật khẩu",
      "confirmPasswordPlaceholder": "Nhập lại mật khẩu",
      "preferredLanguage": "Ngôn ngữ ưa thích",
      "languageVi": "Tiếng Việt",
      "languageEn": "English"
    },
    "contextStep": {
      "title": "Thông tin ngành nghề",
      "regionalLocation": "Khu vực kinh doanh",
      "regionalLocationHelp": "Chọn khu vực chính mà doanh nghiệp hoạt động",
      "north": "Miền Bắc",
      "central": "Miền Trung",
      "south": "Miền Nam",
      "industryType": "Ngành nghề",
      "industryTypeHelp": "Chọn ngành nghề chính của doanh nghiệp",
      "termsAccept": "Tôi đồng ý với",
      "termsLink": "Điều khoản sử dụng",
      "privacyAccept": "Tôi đồng ý với",
      "privacyLink": "Chính sách bảo mật"
    },
    "navigation": {
      "back": "Quay lại",
      "next": "Tiếp tục",
      "submit": "Hoàn tất đăng ký",
      "submitting": "Đang xử lý..."
    },
    "hasAccount": "Đã có tài khoản?",
    "loginLink": "Đăng nhập ngay",
    "errors": {
      "companyNameViRequired": "Vui lòng nhập tên công ty (tiếng Việt)",
      "companyNameRequired": "Vui lòng nhập tên công ty (tiếng Anh)",
      "taxIdRequired": "Vui lòng nhập mã số thuế",
      "taxIdInvalid": "Mã số thuế phải có 10 hoặc 13 chữ số",
      "phoneRequired": "Vui lòng nhập số điện thoại",
      "phoneInvalid": "Số điện thoại phải theo định dạng +84 xxx xxx xxx",
      "emailExists": "Email đã tồn tại trong hệ thống",
      "taxIdExists": "Mã số thuế đã được đăng ký",
      "passwordsDontMatch": "Mật khẩu xác nhận không khớp",
      "termsRequired": "Bạn phải đồng ý với điều khoản sử dụng",
      "privacyRequired": "Bạn phải đồng ý với chính sách bảo mật"
    },
    "success": {
      "title": "Đăng ký thành công!",
      "message": "Tài khoản của bạn đã được tạo. Vui lòng xác thực email để hoàn tất.",
      "checkEmail": "Chúng tôi đã gửi email xác thực đến {email}"
    }
  }
}
```

---

## 9. Implementation Steps

### Phase 1: Setup (Day 1)
- [STEP] Create folder structure: `src/components/Auth/Register/`
- [STEP] Add registration translations to `locales/vi/auth.json` and `locales/en/auth.json`
- [STEP] Create RegistrationFormData TypeScript interface
- [STEP] Add register method to authService.ts

### Phase 2: Components (Day 2-3)
- [STEP] Build ProgressIndicator component
- [STEP] Build CompanyInfoStep component (Step 1)
- [STEP] Build UserAccountStep component (Step 2)
- [STEP] Build BusinessContextStep component (Step 3)
- [STEP] Build PasswordStrengthMeter component
- [STEP] Create Vietnamese phone/tax ID validators

### Phase 3: Integration (Day 4)
- [STEP] Connect RegisterPage to auth service API
- [STEP] Implement multi-step form navigation
- [STEP] Add form validation with react-hook-form
- [STEP] Test API integration with localhost:8001

### Phase 4: Routing & Polish (Day 5)
- [STEP] Update AppRouter.tsx to add `/register` route
- [STEP] Create email verification page (`/verify-email`)
- [STEP] Add success/error notifications
- [STEP] Test responsive design
- [STEP] Test Vietnamese/English language switching

---

## 10. Estimated Timeline

**Total Time:** 4-6 days (1 developer)

| Phase | Time | Status |
|-------|------|--------|
| Setup & Architecture | 4 hours | [PENDING] |
| Step 1: Company Info | 4 hours | [PENDING] |
| Step 2: User Account | 6 hours | [PENDING] |
| Step 3: Business Context | 6 hours | [PENDING] |
| Validation & Password Strength | 4 hours | [PENDING] |
| API Integration | 4 hours | [PENDING] |
| Testing & Polish | 6 hours | [PENDING] |
| **Total** | **34 hours** | **[PENDING]** |

---

## 11. Security Considerations

- Password strength enforcement (minimum score 2/4)
- HTTPS only in production
- Rate limiting on registration endpoint (prevent abuse)
- Email verification required before login
- Tax ID uniqueness check (prevent duplicate companies)
- Sanitize all user inputs

---

## 12. Accessibility Requirements

- [STEP] All form inputs have labels
- [STEP] Error messages announced to screen readers
- [STEP] Keyboard navigation (Tab, Enter, Arrow keys)
- [STEP] Focus management between steps
- [STEP] ARIA labels for progress indicator
- [STEP] Color contrast meets WCAG AA

---

## 13. Testing Checklist

### Functional Testing
- [TEST] Complete 3-step registration flow
- [TEST] Vietnamese phone validation
- [TEST] Tax ID format validation
- [TEST] Password strength meter updates
- [TEST] Password confirmation matching
- [TEST] Email uniqueness check
- [TEST] Tax ID uniqueness check
- [TEST] Terms/privacy acceptance required
- [TEST] Language switching maintains form data
- [TEST] Back button preserves previous steps

### Edge Cases
- [TEST] Empty required fields
- [TEST] Invalid email format
- [TEST] Invalid tax ID format
- [TEST] Invalid phone format
- [TEST] Weak password rejection
- [TEST] Network error handling
- [TEST] API timeout handling

---

## 14. Next Steps After Registration

1. **Email Verification Page** - User clicks link in email
2. **Welcome Onboarding** - First-time user tour
3. **Profile Completion** - Additional business details
4. **Dashboard Access** - Full access to VeriSyntra features

---

**Status:** Ready for implementation  
**Priority:** HIGH (blocking new user acquisition)  
**Dependencies:** 
- Phase 2 auth service (COMPLETED ✅)
- Login page (PENDING - to be implemented first)
