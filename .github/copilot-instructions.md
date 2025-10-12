# VeriSyntra AI Coding Agent Instructions

VeriSyntra is a **Vietnamese PDPL 2025 compliance platform** serving Vietnamese enterprises with culturally-intelligent microservices architecture. This system uniquely combines Vietnamese cultural business intelligence with data protection compliance.

## 🏗️ System Architecture

**Hybrid Frontend/Backend:** React + TypeScript frontend (`src/`) with FastAPI Python backend (`backend/`)
- **Frontend:** Vite + React + TypeScript with modular VeriPortal components
- **Backend:** FastAPI + Vietnamese Cultural Intelligence Engine + PDPL compliance services
- **Internationalization:** Bilingual (Vietnamese-first) using react-i18next with cultural context

**Key Directories:**
- `src/components/VeriPortal/` - Core compliance modules (5 systems: Cultural Onboarding, Compliance Wizards, Document Generation, Training, Business Intelligence)
- `backend/app/core/vietnamese_cultural_intelligence.py` - Cultural AI engine for regional business contexts
- `src/hooks/useCulturalIntelligence.ts` - Frontend cultural context integration
- `docs/VeriSystems/` - System documentation and Jupyter notebooks for AI training

## 🇻🇳 Vietnamese Cultural Intelligence Patterns

**Essential Concept:** Every component must respect Vietnamese business contexts through `VeriBusinessContext`:

```typescript
interface VeriBusinessContext {
  veriBusinessId: string;
  veriRegionalLocation: 'north' | 'central' | 'south'; // Critical for UI/UX
  veriIndustryType: 'technology' | 'manufacturing' | 'finance' | ...;
  veriCulturalPreferences: {
    veriCommunicationStyle: 'collaborative' | 'formal' | 'hierarchical';
    veriDecisionMakingStyle: 'data-driven' | 'consensus' | 'authority';
    // ... more cultural dimensions
  };
}
```

**Regional Business Patterns:**
- **North (Hanoi):** Formal hierarchy, government proximity, structured decision-making
- **South (HCMC):** Entrepreneurial, faster decisions, international business exposure  
- **Central (Da Nang/Hue):** Traditional values, consensus-building, cultural preservation

## 🔧 Development Workflows

**Frontend Development:**
```bash
npm run dev          # Start Vite dev server (localhost:5173)
npm run build        # Production build
npm run typecheck    # TypeScript validation
```

**Backend Development:**
```bash
cd backend
python main_prototype.py  # FastAPI server (localhost:8000)
# View API docs at http://localhost:8000/docs
```

**VeriPortal Component Pattern:**
Each VeriPortal module follows this structure:
```
VeriPortal/ModuleName/
├── components/VeriModuleNameSystem.tsx  # Main component
├── types.ts                            # Vietnamese business types
├── services/                           # API integration
└── styles/                            # Cultural CSS
```

## 🎯 PDPL 2025 Compliance Integration

**Critical:** All data handling must consider PDPL 2025 Vietnamese data protection law:
- Use `VeriBusinessContext` for compliance-aware UI rendering
- Cultural AI engine (`VietnameseCulturalIntelligence`) provides contextual guidance
- Bilingual error messages and audit trails required

**Compliance Wizard Pattern:**
```typescript
const veriWizardTypes = [
  'pdpl-2025-setup',     // Primary compliance wizard
  'data-mapping',        // Vietnamese data categorization
  'policy-generation',   // Culturally appropriate policies
  'audit-preparation'    // MPS reporting integration
];
```

## 🌐 Internationalization Conventions

**Language Priority:** Vietnamese-first with English fallback
```typescript
// In components, use cultural hooks
const { isVietnamese, tCultural } = useCulturalIntelligence();

// Cultural translations with regional context
const title = tCultural('compliance.title', { 
  region: veriBusinessContext.veriRegionalLocation 
});
```

**File Structure:**
- `src/locales/vi/` - Vietnamese translations (primary)
- `src/locales/en/` - English translations (fallback)
- Cultural context embedded in translation keys

## 📊 Data Intelligence Patterns

**VeriAnalytics Dashboard Context:**
```typescript
type VeriAnalyticsScope = 
  | 'compliance-performance'  // PDPL compliance metrics
  | 'cultural-alignment'      // Vietnamese business fit
  | 'regulatory-tracking'     // Government requirement changes
  | 'predictive-analytics';   // Vietnamese market predictions
```

**Vietnamese Business Calendar Integration:**
- Use `Asia/Ho_Chi_Minh` timezone throughout
- Cultural holiday and business cycle awareness in analytics
- Regional business hour optimization (North vs South patterns)

## 🔄 System Integration Points

**Government Systems:** MPS (Ministry of Public Security) integration for PDPL reporting
**Cultural Engine:** All UI decisions routed through Vietnamese cultural intelligence
**AI Training Pipeline:** Jupyter notebooks in `docs/VeriSystems/` for PDPL compliance model training using PhoBERT

## 🎨 UI/UX Cultural Guidelines

**Vietnamese Color Palette:**
- Primary: `#6b8e6b` (Vietnamese green)
- Secondary: `#7fa3c3` (Vietnamese blue)  
- Accent: `#d4c18a` (Vietnamese gold)

**Component Naming Convention:**
- Prefix all Vietnamese-specific components with `Veri`
- Cultural context props always include `veriBusinessContext`
- Bilingual prop interfaces required

## 🚨 Critical Integration Notes

**Backend API Integration:**
- Cultural intelligence API at `/api/v1/veriportal/cultural-context`
- All Vietnamese datetime formatting through cultural engine
- Regional business validation for Vietnamese provinces/cities

**Development Environment:**
- Python environment setup required for Jupyter notebooks
- VnCoreNLP integration for Vietnamese NLP processing
- GPU setup for PhoBERT model training pipelines

When working on this codebase, always consider the Vietnamese business cultural context first, then implement technical solutions that respect these cultural patterns while maintaining PDPL 2025 compliance requirements.