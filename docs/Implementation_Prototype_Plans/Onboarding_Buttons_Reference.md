# Onboarding Page Buttons - Code Reference

## Overview
This document shows all Next, Back, and Finish buttons across the VeriPortal Cultural Onboarding flow.

---

## 1. **Cultural Introduction Step** (First Step)
**File**: `VeriCulturalIntroductionStep.tsx`

### Buttons:
- **Next Button Only** (No Back button on first step)

### Code:
```tsx
<button 
  onClick={veriProceedToNextStep}
  className="group text-white px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 flex items-center justify-center space-x-2 mx-auto"
  style={{
    background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 50%, #d4c18a 100%)',
    border: '2px solid #d4c18a',
    boxShadow: '0 4px 20px rgba(107, 142, 107, 0.25)'
  }}
  onMouseEnter={(e) => {
    e.currentTarget.style.boxShadow = '0 6px 32px rgba(107, 142, 107, 0.35)';
    e.currentTarget.style.background = 'linear-gradient(135deg, #7fa088 0%, #8bb3d3 50%, #dcc898 100%)';
  }}
  onMouseLeave={(e) => {
    e.currentTarget.style.boxShadow = '0 4px 20px rgba(107, 142, 107, 0.25)';
    e.currentTarget.style.background = 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 50%, #d4c18a 100%)';
  }}
>
  <span>{t('veriportal:culturalIntroduction.nextAction')}</span>
  <span className="text-lg group-hover:translate-x-1 transition-transform">➡️</span>
</button>
```

**Function Called**:
```tsx
const veriProceedToNextStep = () => {
  veriOnNext('business-profile-setup');
};
```

**Style**: Full-width centered button with gradient (jade green → sky blue → warm gold)

---

## 2. **Business Profile Setup Step**
**File**: `VeriBusinessProfileSetupStep.tsx`

### Buttons:
- **Back Button** (Left)
- **Next Button** (Right)

### Code:
```tsx
<div className="veri-step-actions" style={{ marginTop: '32px' }}>
  {/* BACK BUTTON */}
  <button 
    className="veri-secondary-button"
    onClick={veriGoBack}
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '12px',
      padding: '16px 32px',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: 'pointer',
      flex: 1,
      minHeight: '52px',
      background: 'white',
      color: '#495057',
      border: '2px solid #ced4da',
      boxShadow: '0 2px 10px 0 rgba(0, 0, 0, 0.1)',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      fontFamily: 'Inter, Segoe UI, system-ui, sans-serif'
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.background = '#f8f9fa';
      e.currentTarget.style.borderColor = '#6b8e6b';
      e.currentTarget.style.color = '#6b8e6b';
      e.currentTarget.style.transform = 'translateY(-3px)';
      e.currentTarget.style.boxShadow = '0 4px 14px 0 rgba(0, 0, 0, 0.15)';
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.background = 'white';
      e.currentTarget.style.borderColor = '#ced4da';
      e.currentTarget.style.color = '#495057';
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = '0 2px 10px 0 rgba(0, 0, 0, 0.1)';
    }}
  >
    <span className="veri-button-icon" style={{ fontSize: '18px' }}>⬅️</span>
    {veriContent[veriLanguage].back}
  </button>
  
  {/* NEXT BUTTON */}
  <button 
    className="veri-primary-button"
    onClick={veriProceedToNext}
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '12px',
      padding: '16px 32px',
      borderRadius: '12px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: 'pointer',
      flex: 1,
      minHeight: '52px',
      background: 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)',
      color: 'white',
      border: '2px solid rgba(107, 142, 107, 0.3)',
      boxShadow: '0 4px 14px 0 rgba(107, 142, 107, 0.4)',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      fontFamily: 'Inter, Segoe UI, system-ui, sans-serif'
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.background = 'linear-gradient(135deg, #7fa088 0%, #8bb3d3 100%)';
      e.currentTarget.style.transform = 'translateY(-3px)';
      e.currentTarget.style.boxShadow = '0 6px 20px 0 rgba(107, 142, 107, 0.5)';
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.background = 'linear-gradient(135deg, #6b8e6b 0%, #7fa3c3 100%)';
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = '0 4px 14px 0 rgba(107, 142, 107, 0.4)';
    }}
  >
    <span className="veri-button-icon" style={{ fontSize: '18px' }}>➡️</span>
    {veriContent[veriLanguage].next}
  </button>
</div>
```

**Functions Called**:
```tsx
const veriGoBack = () => {
  veriOnPrevious('cultural-introduction');
};

const veriProceedToNext = () => {
  veriOnNext('regional-adaptation');
};
```

**Text Content**:
```tsx
const veriContent = {
  vietnamese: {
    next: 'Tiếp tục',
    back: 'Quay lại'
  },
  english: {
    next: 'Continue',
    back: 'Back'
  }
};
```

**Style**: Two buttons side-by-side with flexbox
- Back: White background, gray border, hover → green accent
- Next: Gradient background (jade → sky blue), hover → lighter gradient

---

## 3. **Regional Adaptation Step**
**File**: `VeriRegionalAdaptationStep.tsx`

### Buttons:
- **Back Button**
- **Next Button**

### Code:
```tsx
<button onClick={() => veriOnPrevious('business-profile-setup')}>
  {t('common:navigation.back')}
</button>
<button onClick={() => veriOnNext('cultural-preferences')}>
  {t('common:navigation.next')}
</button>
```

**Translation Keys**:
- `common:navigation.back` → "Back" / "Quay lại"
- `common:navigation.next` → "Next" / "Tiếp tục"

**Style**: Basic buttons (needs styling update to match other steps)

---

## 4. **Cultural Preferences Step**
**File**: `VeriCulturalPreferencesStep.tsx`

### Buttons:
- **Back Button**
- **Next Button**

### Code:
```tsx
<button onClick={() => veriOnPrevious('regional-adaptation')}>Back</button>
<button onClick={() => veriOnNext('compliance-readiness')}>Next</button>
```

**Style**: Basic buttons (needs styling update)

---

## 5. **Compliance Readiness Step**
**File**: `VeriComplianceReadinessStep.tsx`

### Buttons:
- **Back Button**
- **Next Button**

### Code:
```tsx
<button onClick={() => veriOnPrevious('cultural-preferences')}>Back</button>
<button onClick={() => veriOnNext('completion-summary')}>Next</button>
```

**Style**: Basic buttons (needs styling update)

---

## 6. **Completion Summary Step** (Final Step)
**File**: `VeriCompletionSummaryStep.tsx`

### Buttons:
- **Back Button**
- **Finish Button** (instead of Next)

### Code:
```tsx
<button onClick={() => veriOnPrevious('compliance-readiness')}>Back</button>
<button onClick={() => alert(veriLanguage === 'vietnamese' ? 'Đã hoàn thành!' : 'Completed!')}>
  Finish
</button>
```

**Text**:
- Button text: "Finish"
- Alert text: "Đã hoàn thành!" (Vietnamese) / "Completed!" (English)

**Style**: Basic buttons (needs styling update)

---

## Summary of Button Patterns

### Current Implementation Status:

| Step | File | Back Button | Next/Finish Button | Styled? |
|------|------|-------------|-------------------|---------|
| 1. Cultural Introduction | VeriCulturalIntroductionStep.tsx | ❌ No | ✅ Next (Fully Styled) | ✅ Yes |
| 2. Business Profile | VeriBusinessProfileSetupStep.tsx | ✅ Back | ✅ Next | ✅ Yes (Inline) |
| 3. Regional Adaptation | VeriRegionalAdaptationStep.tsx | ✅ Back | ✅ Next | ❌ Basic |
| 4. Cultural Preferences | VeriCulturalPreferencesStep.tsx | ✅ Back | ✅ Next | ❌ Basic |
| 5. Compliance Readiness | VeriComplianceReadinessStep.tsx | ✅ Back | ✅ Next | ❌ Basic |
| 6. Completion Summary | VeriCompletionSummaryStep.tsx | ✅ Back | ✅ Finish | ❌ Basic |

### Button Types:
1. **Next Button** - Used in steps 1-5 to proceed to next step
2. **Back Button** - Used in steps 2-6 to return to previous step
3. **Finish Button** - Used in final step (6) to complete onboarding

### Styling Levels:
- **Fully Styled**: Cultural Introduction (step 1), Business Profile (step 2)
- **Basic/Unstyled**: Steps 3-6 (Regional Adaptation, Cultural Preferences, Compliance Readiness, Completion Summary)

---

## Recommended Actions:

### 1. Apply Consistent Button Styling
All steps 3-6 need the same button styling as step 2 (Business Profile):
- White background for Back button
- Gradient background for Next/Finish button
- Proper sizing (52px min-height, 16px 32px padding)
- Hover effects with elevation
- Icons (⬅️ for Back, ➡️ for Next, ✅ or 🎉 for Finish)

### 2. Update Text Content
Use proper Vietnamese translations from i18n instead of hardcoded text.

### 3. Consistent Layout
Use flexbox with `display: flex; justify-content: space-between; gap: 16px;` for all button containers.

### 4. Special Finish Button
Make the Finish button more prominent with celebration emoji and possibly different gradient (e.g., green to gold for success).
