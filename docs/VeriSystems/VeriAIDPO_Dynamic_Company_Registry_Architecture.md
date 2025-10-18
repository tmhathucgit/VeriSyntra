# Dynamic Company Registry - Complete System Architecture
## Frontend ↔ Backend ↔ AI Integration Flow

**Date**: October 18, 2025  
**Version**: 2.0 (Full Stack)

---

## 🏗️ Complete Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React + TypeScript)                        │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │  useCompanyRegistry Hook (src/hooks/useCompanyRegistry.ts)          │     │
│  │                                                                      │     │
│  │  • fetchCompanies()          → GET /api/admin/companies/list        │     │
│  │  • searchCompanies(query)    → GET /api/admin/companies/search      │     │
│  │  • normalizeText(text)       → POST /api/admin/companies/normalize  │     │
│  │  • refreshRegistry()         → POST /api/admin/companies/reload     │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                              ↓                ↓                               │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │  VeriPortal Components (4 Systems)                                    │   │
│  │                                                                        │   │
│  │  1. VeriCulturalOnboarding                                           │   │
│  │     └─ handleCompanyNameSubmit(name)                                 │   │
│  │        ├─ normalizeText("Shopee Vietnam")  → "[COMPANY]"            │   │
│  │        └─ analyzeCulturalContext("[COMPANY]") → POST /api/cultural   │   │
│  │                                                                        │   │
│  │  2. VeriComplianceWizards                                            │   │
│  │     └─ handleWizardInput(field, text)                                │   │
│  │        ├─ normalizeText(text)  → { normalized, original, companies } │   │
│  │        └─ classifyPDPL(normalized) → POST /api/veriaidpo/classify    │   │
│  │                                                                        │   │
│  │  3. VeriDocumentGeneration                                           │   │
│  │     └─ generateDocument(template, companyInfo)                       │   │
│  │        ├─ normalizeText(companyInfo) → normalized inputs             │   │
│  │        ├─ POST /api/veriportal/generate-document                     │   │
│  │        └─ denormalizeDocument(result) → replace [COMPANY] with name  │   │
│  │                                                                        │   │
│  │  4. VeriBIDashboard                                                  │   │
│  │     └─ renderCompanyRegistryStats()                                  │   │
│  │        └─ Display: Total companies, Industries, Regions, Last updated│   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                                │
└────────────────────────────────────────┬───────────────────────────────────────┘
                                         │ HTTP/REST API
                                         ↓
┌───────────────────────────────────────────────────────────────────────────────┐
│                          BACKEND (FastAPI + Python)                            │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │  API Layer (backend/app/api/v1/)                                    │     │
│  │                                                                      │     │
│  │  Admin Endpoints (admin/companies.py):                              │     │
│  │  • POST /add          → registry.add_company()                      │     │
│  │  • GET  /list         → registry.get_all_companies()                │     │
│  │  • GET  /search       → registry.search_company(query)              │     │
│  │  • POST /normalize    → normalizer.normalize_for_inference()        │     │
│  │  • POST /reload       → registry.reload()                           │     │
│  │  • GET  /stats        → registry.get_stats()                        │     │
│  │                                                                      │     │
│  │  Classification Endpoints (veriaidpo.py):                           │     │
│  │  • POST /classify-legal-basis                                       │     │
│  │  • POST /classify-breach-severity                                   │     │
│  │  • POST /classify-cross-border                                      │     │
│  │    └─ All use normalizer.normalize_for_inference() before AI       │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                              ↓                ↓                               │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │  Core Services (backend/app/core/)                                  │     │
│  │                                                                      │     │
│  │  CompanyRegistry (company_registry.py):                             │     │
│  │  • _load_companies()     → Read config/company_registry.json        │     │
│  │  • add_company()         → Add new company (hot-reload)             │     │
│  │  • get_all_companies()   → Return all 150+ companies                │     │
│  │  • search_company()      → Search by name/alias                     │     │
│  │  • reload()              → Hot-reload without restart               │     │
│  │                                                                      │     │
│  │  PDPLTextNormalizer (pdpl_normalizer.py):                           │     │
│  │  • normalize_company_names(text)                                    │     │
│  │    └─ "Shopee Vietnam thu thập..." → "[COMPANY] thu thập..."       │     │
│  │  • normalize_for_inference(text)                                    │     │
│  │    └─ Complete pipeline: companies + persons + addresses            │     │
│  │  • denormalize_response(prediction)                                 │     │
│  │    └─ Add detected company metadata back to response                │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                       ↓                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │  Data Layer (config/)                                                │     │
│  │                                                                      │     │
│  │  company_registry.json (150+ Vietnamese companies):                 │     │
│  │  {                                                                   │     │
│  │    "technology": {                                                   │     │
│  │      "north": [                                                      │     │
│  │        { "name": "FPT Corporation", "aliases": ["FPT", ...] },      │     │
│  │        { "name": "Viettel Group", "aliases": ["Viettel", ...] }     │     │
│  │      ],                                                              │     │
│  │      "south": [                                                      │     │
│  │        { "name": "Shopee Vietnam", "aliases": ["Shopee VN", ...] }, │     │
│  │        { "name": "Grab Vietnam", "aliases": ["Grab VN", ...] }      │     │
│  │      ]                                                               │     │
│  │    },                                                                │     │
│  │    "finance": { ... },                                               │     │
│  │    ... (9 industries total)                                          │     │
│  │  }                                                                   │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                                                                │
└────────────────────────────────────────┬───────────────────────────────────────┘
                                         │ Normalized Text
                                         ↓
┌───────────────────────────────────────────────────────────────────────────────┐
│                            AI MODELS (VeriAIDPO)                               │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │  VeriAIDPO Models (PhoBERT / BERT)                                  │     │
│  │                                                                      │     │
│  │  Input: "[COMPANY] thu thập số CMND của khách hàng"                │     │
│  │         ↓                                                            │     │
│  │  Tokenization: [101, 5234, 8901, ...] (company = generic token)     │     │
│  │         ↓                                                            │     │
│  │  Classification: Analyze PDPL context (company-agnostic)            │     │
│  │         ↓                                                            │     │
│  │  Output: {                                                           │     │
│  │    "category": "Collection Limitation",                              │     │
│  │    "category_id": 2,                                                 │     │
│  │    "confidence": 0.89                                                │     │
│  │  }                                                                   │     │
│  │                                                                      │     │
│  │  Models:                                                             │     │
│  │  • VeriAIDPO_Principles_VI/EN (8 PDPL principles)                   │     │
│  │  • VeriAIDPO_LegalBasis_VI/EN (6 legal bases)                       │     │
│  │  • VeriAIDPO_BreachTriage_VI/EN (5 severity levels)                 │     │
│  │  • VeriAIDPO_CrossBorder_VI/EN (6 jurisdictions)                    │     │
│  │  • ... (21 models total in Phase 0-3)                               │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Complete User Flow Example

### **Scenario**: User classifies PDPL compliance in VeriComplianceWizards

**Step 1: User Input**
```typescript
// User types in wizard:
const userInput = "Shopee Vietnam thu thập số điện thoại khách hàng để giao hàng";
```

**Step 2: Frontend Normalization**
```typescript
// VeriComplianceWizardSystem.tsx
const { normalizeText } = useCompanyRegistry();
const { normalizedText, detectedCompanies } = await normalizeText(userInput);

// Result:
// normalizedText: "[COMPANY] thu thập số điện thoại khách hàng để giao hàng"
// detectedCompanies: ["Shopee Vietnam"]
```

**Step 3: Store Dual Versions**
```typescript
const fieldData = {
  original: userInput,                          // For display
  normalized: normalizedText,                   // For AI
  companies: detectedCompanies                  // Metadata
};
```

**Step 4: Send to Backend**
```typescript
const response = await fetch('/api/v1/veriaidpo/classify-legal-basis', {
  method: 'POST',
  body: JSON.stringify({
    text: fieldData.normalized,  // ← Normalized version
    language: 'vi'
  })
});
```

**Step 5: Backend Processing**
```python
# backend/app/api/v1/veriaidpo.py
from app.core.pdpl_normalizer import get_text_normalizer

normalizer = get_text_normalizer()
normalized_text = normalizer.normalize_for_inference(request.text)
# normalized_text: "[COMPANY] thu thập số điện thoại..."

# Already normalized from frontend, but double-check for consistency
```

**Step 6: AI Inference**
```python
from app.ml.models import VeriAIDPO_LegalBasis_VI

model = VeriAIDPO_LegalBasis_VI()
prediction = model.predict(normalized_text)

# Model sees: "[COMPANY] thu thập số điện thoại khách hàng để giao hàng"
# Model output: {
#   "category": "Contract Performance",
#   "category_id": 1,
#   "confidence": 0.91,
#   "reasoning": "Giao hàng là nghĩa vụ hợp đồng"
# }
```

**Step 7: Backend Response**
```python
return {
  "prediction": "Contract Performance",
  "confidence": 0.91,
  "category_id": 1,
  "normalized_text": normalized_text,
  "detected_companies": ["Shopee Vietnam"]
}
```

**Step 8: Frontend Display**
```typescript
// VeriComplianceWizardSystem.tsx
const result = await response.json();

// Display to user:
<div className="classification-result">
  <p>Văn bản gốc: "{fieldData.original}"</p>
  {/* Shows: "Shopee Vietnam thu thập..." */}
  
  <p>Công ty phát hiện: {result.detected_companies.join(', ')}</p>
  {/* Shows: "Shopee Vietnam" */}
  
  <p>Căn cứ pháp lý: {result.prediction}</p>
  {/* Shows: "Contract Performance" */}
  
  <p>Độ tin cậy: {(result.confidence * 100).toFixed(0)}%</p>
  {/* Shows: "91%" */}
</div>
```

---

## 🎯 Key Integration Points

### **1. Frontend → Backend**
- **Hook**: `useCompanyRegistry` provides `normalizeText()` function
- **Components**: All VeriPortal components call `normalizeText()` before AI requests
- **Storage**: Dual storage pattern (`original` + `normalized` + `companies`)

### **2. Backend → AI**
- **Normalizer**: `PDPLTextNormalizer.normalize_for_inference()` ensures `[COMPANY]` tokens
- **Consistency**: Same normalization in training and inference
- **Models**: All 21 VeriAIDPO models trained with `[COMPANY]` normalization

### **3. AI → Backend → Frontend**
- **Metadata**: Backend adds `detected_companies` to response
- **Denormalization**: Frontend shows original company names to users
- **Transparency**: Users see which companies were detected in their input

---

## 💾 Data Flow Summary

```
User Input (Real Company Name)
    ↓
Frontend: Normalize → [COMPANY]
    ↓
Backend: Validate normalization
    ↓
AI Model: Classify (company-agnostic)
    ↓
Backend: Add metadata (detected companies)
    ↓
Frontend: Display original company name
    ↓
User sees: Real company name + AI classification
```

---

## 🔐 Key Benefits

### **For Users**
- ✅ Seamless experience (never see `[COMPANY]` tokens)
- ✅ Real company names displayed everywhere
- ✅ Transparent detection (shows which companies found)
- ✅ Fast response (<100ms normalization overhead)

### **For System**
- ✅ Scalable (add unlimited companies without retraining)
- ✅ Consistent (same normalization in training and inference)
- ✅ Cost-effective ($0 per new company vs $220-320)
- ✅ Future-proof (works with companies that don't exist yet)

### **For Developers**
- ✅ Single hook (`useCompanyRegistry`) for all components
- ✅ Consistent pattern across VeriPortal
- ✅ Type-safe (TypeScript definitions)
- ✅ Hot-reload capability (update registry without deployment)

---

## 📊 Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Normalization Time (Frontend) | <50ms | TBD |
| API Response Time (Backend) | <100ms | TBD |
| AI Inference Time | <50ms | TBD |
| Total User Wait Time | <200ms | TBD |
| Registry Reload Time | <5 minutes | TBD |
| Company Detection Accuracy | 99.9%+ | TBD |

---

## 🚀 Next Steps

1. ✅ **Backend Implementation** (Week 1-2)
   - Create CompanyRegistry + PDPLTextNormalizer
   - Build Admin API endpoints
   
2. ✅ **Frontend Implementation** (Week 2-3)
   - Create `useCompanyRegistry` hook
   - Update all VeriPortal components
   
3. ✅ **Integration Testing** (Week 3)
   - End-to-end user flows
   - Performance benchmarking
   
4. ✅ **Phase 0 Training** (Week 4-5)
   - Train VeriAIDPO_Principles v2.0 with normalized datasets
   - Validate 78-88% accuracy target

---

**Document Owner**: VeriSyntra Architecture Team  
**Last Updated**: October 18, 2025  
**Status**: ✅ Architecture Complete - Ready for Implementation  
**Version**: 2.0 (Full Stack Integration)
