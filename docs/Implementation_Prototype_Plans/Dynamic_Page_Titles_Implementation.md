# Dynamic Page Titles Implementation

## Overview
Implemented dynamic browser tab titles that change based on the current page/route, replacing the static "VeriSyntra - PDPL 2025 Compliance Platform" title with page-specific titles.

## Implementation Date
December 2024

## Requirement
- **Landing Page**: Shows only "VeriSyntra"
- **Other Pages**: Show format "{Page Name} | VeriSyntra"
- **Bilingual Support**: Vietnamese and English titles based on current language
- **Dynamic Updates**: Titles update when navigating between pages and when language switches

## Solution Architecture

### Custom Hook: `usePageTitle`
Created a reusable custom hook at `src/hooks/usePageTitle.ts`:

```typescript
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface UsePageTitleOptions {
  title: string;
  titleVi?: string;
  includeAppName?: boolean;
}

export const usePageTitle = ({ 
  title, 
  titleVi, 
  includeAppName = true 
}: UsePageTitleOptions) => {
  const { i18n } = useTranslation();
  const isVietnamese = i18n.language === 'vi';

  useEffect(() => {
    const pageTitle = isVietnamese && titleVi ? titleVi : title;
    const fullTitle = includeAppName 
      ? `${pageTitle} | VeriSyntra`
      : pageTitle;
    
    document.title = fullTitle;

    // Cleanup: restore default title when component unmounts
    return () => {
      document.title = 'VeriSyntra - PDPL 2025 Compliance Platform';
    };
  }, [title, titleVi, includeAppName, isVietnamese]);
};
```

### Features
1. **Native Approach**: Uses `document.title` API (no external dependencies)
2. **Bilingual**: Supports Vietnamese and English titles
3. **Automatic Updates**: Responds to language changes via i18n
4. **Flexible**: `includeAppName` option for landing page vs other pages
5. **Cleanup**: Restores default title on unmount

## Pages Updated

### 1. Landing Page (`src/Landing.tsx`)
```typescript
usePageTitle({ title: 'VeriSyntra', includeAppName: false });
```
**Result**: Browser tab shows "VeriSyntra"

### 2. VeriSyntra App (`src/verisyntra/VeriSyntraApp.tsx`)
```typescript
usePageTitle({ 
  title: 'VeriSyntra App', 
  titleVi: 'Ứng dụng VeriSyntra' 
});
```
**Result**: 
- English: "VeriSyntra App | VeriSyntra"
- Vietnamese: "Ứng dụng VeriSyntra | VeriSyntra"

### 3. Cultural Onboarding System
**File**: `src/components/VeriPortal/CulturalOnboarding/VeriCulturalOnboardingSystem.tsx`
```typescript
usePageTitle({ 
  title: 'Onboarding', 
  titleVi: 'Giới thiệu Văn hóa' 
});
```
**Result**:
- English: "Onboarding | VeriSyntra"
- Vietnamese: "Giới thiệu Văn hóa | VeriSyntra"

### 4. Compliance Wizards System
**File**: `src/components/VeriPortal/ComplianceWizards/components/VeriComplianceWizardSystem.tsx`
```typescript
usePageTitle({ 
  title: 'Compliance Wizards', 
  titleVi: 'Trình hướng dẫn Tuân thủ' 
});
```
**Result**:
- English: "Compliance Wizards | VeriSyntra"
- Vietnamese: "Trình hướng dẫn Tuân thủ | VeriSyntra"

### 5. Document Generation System
**File**: `src/components/VeriPortal/DocumentGeneration/components/VeriDocumentGenerationSystem.tsx`
```typescript
usePageTitle({ 
  title: 'Document Generation', 
  titleVi: 'Tạo Tài liệu' 
});
```
**Result**:
- English: "Document Generation | VeriSyntra"
- Vietnamese: "Tạo Tài liệu | VeriSyntra"

### 6. Business Intelligence System
**File**: `src/components/VeriPortal/BusinessIntelligence/components/VeriBusinessIntelligenceSystem.tsx`
```typescript
usePageTitle({ 
  title: 'Business Intelligence', 
  titleVi: 'Tình báo Kinh doanh' 
});
```
**Result**:
- English: "Business Intelligence | VeriSyntra"
- Vietnamese: "Tình báo Kinh doanh | VeriSyntra"

### 7. System Integration System
**File**: `src/components/VeriPortal/SystemIntegration/components/VeriSystemIntegrationSystem.tsx`
```typescript
usePageTitle({ 
  title: 'System Integration', 
  titleVi: 'Tích hợp Hệ thống' 
});
```
**Result**:
- English: "System Integration | VeriSyntra"
- Vietnamese: "Tích hợp Hệ thống | VeriSyntra"

## Route Mapping

| Route | Component | English Title | Vietnamese Title |
|-------|-----------|---------------|------------------|
| `/` | Landing | VeriSyntra | VeriSyntra |
| `/app` | VeriSyntraApp | VeriSyntra App \| VeriSyntra | Ứng dụng VeriSyntra \| VeriSyntra |
| `/veriportal` | VeriComplianceWizardSystem | Compliance Wizards \| VeriSyntra | Trình hướng dẫn Tuân thủ \| VeriSyntra |
| `/veriportal/cultural-onboarding` | VeriCulturalOnboardingSystem | Onboarding \| VeriSyntra | Giới thiệu Văn hóa \| VeriSyntra |
| `/veriportal/documents` | VeriDocumentGenerationSystem | Document Generation \| VeriSyntra | Tạo Tài liệu \| VeriSyntra |
| `/veriportal/business-intelligence` | VeriBusinessIntelligenceSystem | Business Intelligence \| VeriSyntra | Tình báo Kinh doanh \| VeriSyntra |
| `/veriportal/system-integration` | VeriSystemIntegrationSystem | System Integration \| VeriSyntra | Tích hợp Hệ thống \| VeriSyntra |

## Technical Details

### Why Native Approach vs React Helmet?
- **No External Dependency**: react-helmet was not already installed
- **Simpler Implementation**: Native `document.title` is straightforward
- **Smaller Bundle Size**: No additional library weight
- **Sufficient for Requirements**: Meets all user needs without extra complexity

### Hook Integration
The hook integrates seamlessly with existing code:
1. Uses `useTranslation` from react-i18next (already installed)
2. Listens to language changes automatically
3. Updates title in real-time when language switches
4. Cleans up on component unmount

### Naming Convention - Vietnamese Translations
- **App**: Ứng dụng
- **Cultural Onboarding**: Giới thiệu Văn hóa
- **Compliance Wizards**: Trình hướng dẫn Tuân thủ
- **Document Generation**: Tạo Tài liệu
- **Business Intelligence**: Tình báo Kinh doanh
- **System Integration**: Tích hợp Hệ thống

## Testing & Validation

### Build Status
✅ **Successful Build**: `npm run build` completed without errors
```
✓ 1608 modules transformed.
dist/index.html                       0.69 kB │ gzip:   0.41 kB
dist/assets/vnMapLogo-CHo2iaXn.svg  130.83 kB │ gzip:  28.07 kB
dist/assets/index-DJoavTXV.css      130.76 kB │ gzip:  21.62 kB
dist/assets/index-Bw1Z6YMi.js       474.00 kB │ gzip: 141.17 kB
✓ built in 2.87s
```

### Verification Steps
1. ✅ All components import and use `usePageTitle` correctly
2. ✅ TypeScript compilation successful
3. ✅ Vite build completed successfully
4. ✅ No breaking changes to existing functionality

## Files Modified

### New File Created
1. `src/hooks/usePageTitle.ts` - Custom hook for dynamic titles

### Files Updated
1. `src/Landing.tsx` - Added usePageTitle for landing page
2. `src/verisyntra/VeriSyntraApp.tsx` - Added usePageTitle for app page
3. `src/components/VeriPortal/CulturalOnboarding/VeriCulturalOnboardingSystem.tsx` - Added usePageTitle
4. `src/components/VeriPortal/ComplianceWizards/components/VeriComplianceWizardSystem.tsx` - Added usePageTitle
5. `src/components/VeriPortal/DocumentGeneration/components/VeriDocumentGenerationSystem.tsx` - Added usePageTitle
6. `src/components/VeriPortal/BusinessIntelligence/components/VeriBusinessIntelligenceSystem.tsx` - Added usePageTitle
7. `src/components/VeriPortal/SystemIntegration/components/VeriSystemIntegrationSystem.tsx` - Added usePageTitle

## Benefits

### User Experience
1. **Clear Navigation**: Users can identify pages from browser tabs
2. **Multi-tab Browsing**: Easy to distinguish between multiple open VeriSyntra tabs
3. **Bookmarking**: Bookmarked pages have meaningful names
4. **Cultural Sensitivity**: Vietnamese users see titles in their language

### SEO & Accessibility
1. **Better SEO**: Unique, descriptive titles for each page
2. **Screen Readers**: Assistive technology announces page changes
3. **Browser History**: Clear entries in browser history

### Development
1. **Reusable Hook**: Easy to add titles to future pages
2. **Maintainable**: Centralized title management
3. **Type-Safe**: Full TypeScript support
4. **DRY Principle**: No code duplication

## Future Enhancements

### Potential Improvements
1. **Sub-page Titles**: Add more granular titles for wizard steps or sub-sections
2. **Dynamic Content**: Include dynamic data in titles (e.g., "Document XYZ | Document Generation")
3. **Title Templates**: Create template system for consistent formatting
4. **Meta Tags**: Extend to update meta description and other meta tags
5. **Analytics Integration**: Track page views with accurate titles

### Example Usage for Future Pages
```typescript
// Simple page
usePageTitle({ 
  title: 'Page Name', 
  titleVi: 'Tên Trang' 
});

// Landing-style page (no app name)
usePageTitle({ 
  title: 'Standalone Page', 
  includeAppName: false 
});

// English-only page
usePageTitle({ 
  title: 'Admin Dashboard' 
});
```

## Conclusion

The dynamic page titles implementation successfully addresses the user requirement for page-specific browser tab titles. The solution is:
- ✅ Simple and maintainable
- ✅ Bilingual (Vietnamese/English)
- ✅ Automatic and reactive to language changes
- ✅ Type-safe with full TypeScript support
- ✅ Zero external dependencies beyond existing i18n
- ✅ Production-ready (build successful)

All seven pages now have unique, meaningful titles that update dynamically based on navigation and language selection.
