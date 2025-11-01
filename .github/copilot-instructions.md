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

## 🔤 Code Style Requirements

**CRITICAL - No Emoji Characters:**
- **NEVER use emoji characters** in any code (✓, ✗, ⚠️, •, →, 🔧, etc.)
- Use ASCII alternatives: `[OK]`, `[ERROR]`, `[WARNING]`, `>`, `->`
- Applies to: Python, TypeScript, JavaScript, JSON, Markdown, comments
- Reason: Terminal compatibility, CI/CD systems, cross-platform support

**Status Indicator Standards:**
```python
# CORRECT - ASCII only
print("[OK] Operation successful")
print("[ERROR] Operation failed")
print("[WARNING] Potential issue detected")
print("  > Item 1")  # Use > for bullet points
print("Step 1 -> Step 2")  # Use -> for arrows

# WRONG - Do not use
print("✓ Operation successful")  # NO EMOJI
print("✗ Operation failed")      # NO EMOJI
print("⚠️ Warning")              # NO EMOJI
print("  • Item 1")              # NO EMOJI
print("Step 1 → Step 2")         # NO EMOJI
```

**CRITICAL - Dynamic Code Over Hard-Coding:**
- **ALWAYS prefer dynamic, reusable code** over hard-coded values
- **Use functions, classes, and configuration** instead of duplicating code
- **Follow DRY (Don't Repeat Yourself)** principle strictly
- **Single source of truth** for data definitions and constants

**Dynamic Coding Standards:**
```python
# CORRECT - Dynamic approach
def calculate_total(items):
    """Reusable function with parameters"""
    return sum(item['price'] for item in items)

# Use existing definitions instead of redefining
if 'PDPL_CATEGORIES' in globals():
    print(f"[OK] Using {len(PDPL_CATEGORIES)} categories")
else:
    raise ValueError("Run Step 2 first to define PDPL_CATEGORIES")

# Dynamic validation with detailed feedback
cat2_total = sum(len(v) for v in CAT2_DISTINCTIVE_PHRASES.values())
print(f"[OK] {cat2_total} markers across {len(CAT2_DISTINCTIVE_PHRASES)} categories")

# WRONG - Hard-coded approach
total = items[0]['price'] + items[1]['price'] + items[2]['price']  # NO - not reusable

# Duplicate definitions (violates DRY)
PDPL_CATEGORIES = {...}  # Defined in Step 2
PDPL_CATEGORIES = {...}  # NO - Redefining in Step 4 (use Step 2's definition)

# Hard-coded counts
print("18 markers loaded")  # NO - calculate dynamically
```

**Code Reusability Checklist:**
- [ ] Check if data/function already exists before creating new
- [ ] Use dependency validation (check prerequisites exist)
- [ ] Calculate values dynamically instead of hard-coding numbers
- [ ] Add clear error messages pointing to dependencies
- [ ] Make functions accept parameters instead of using globals
- [ ] Use configuration files/objects for constants

When working on this codebase, always consider the Vietnamese business cultural context first, then implement technical solutions that respect these cultural patterns while maintaining PDPL 2025 compliance requirements.