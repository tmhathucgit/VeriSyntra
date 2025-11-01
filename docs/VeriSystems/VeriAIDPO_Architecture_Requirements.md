# VeriAIDPO - Architecture Requirements
## Production Backend Integration for ALL Models

**Version**: 1.1  
**Last Updated**: October 18, 2025  
**Applies To**: ALL 21 VeriAIDPO models (Phase 0-3)  
**Status**: ✅ MANDATORY - No Exceptions

---

## 🏗️ **CRITICAL: Production Backend Integration**

**MANDATORY REQUIREMENT FOR ALL 21 MODELS**

### ⚠️ **Use Production Backend Modules - NOT Inline Code**

**ALL training notebooks MUST use VeriSyntra production backend modules:**

```python
# ✅ CORRECT: Import from VeriSyntra backend
from app.core.company_registry import get_registry, CompanyRegistry
from app.core.pdpl_normalizer import get_normalizer, PDPLTextNormalizer

registry = get_registry()      # Production registry
normalizer = get_normalizer()  # Production normalizer
```

```python
# ❌ WRONG: Do NOT recreate classes inline
class CompanyRegistry:  # DON'T DO THIS!
    def __init__(self, companies_data):
        # This creates training-production mismatch
        # ~200 lines of duplicated code...
```

---

## 📁 Required Files for ALL Colab Notebooks

Upload these **3 files** from VeriSyntra backend to Google Colab:

1. **`backend/app/core/company_registry.py`** (513 lines)
   - Production CompanyRegistry class
   - Methods: `get_registry()`, `get_statistics()`, `search_companies()`, `add_company()`, `remove_company()`

2. **`backend/app/core/pdpl_normalizer.py`** (~300 lines)
   - Production PDPLTextNormalizer class
   - Methods: `get_normalizer()`, `normalize_text()` → Returns NormalizationResult
   - Replaces company names with `[COMPANY]` token

3. **`backend/config/company_registry.json`**
   - Production company database (46+ Vietnamese companies)
   - Fields: company_id, name, industry, region, website, description
   - Industries: Technology, Finance, Manufacturing, Retail, Healthcare, etc.
   - Regions: North (Hanoi), Central (Da Nang/Hue), South (HCMC)

---

## 📊 Why This Matters

### Comparison: Inline Code vs Backend Modules

| Aspect | Inline Code (❌ BAD) | Backend Modules (✅ GOOD) |
|--------|---------------------|--------------------------|
| **Production Parity** | ⚠️ Risk of drift | ✅ Identical code |
| **Company Registry** | ⚠️ Manual copy | ✅ Uses `company_registry.json` |
| **Maintenance** | ❌ Update 21 places | ✅ Update 1 place |
| **Testing** | ⚠️ Different from API | ✅ Same as API |
| **Hot-reload** | ❌ Not supported | ✅ Add companies without retrain |
| **Code Duplication** | ❌ ~200 lines per notebook | ✅ 2 import lines |
| **Total Code** | ❌ 4,200 lines (21 notebooks) | ✅ 42 lines (21 notebooks) |

---

## ✅ Benefits of Production Backend Integration

### 1. **Training Code = Production Code**
- Model trains with **EXACT same company registry** as production API
- Normalization logic is **IDENTICAL** in training and inference
- No "worked in training, fails in production" issues
- Guaranteed consistency across all 21 models

### 2. **Hot-Reload Capability**
- Add new company to `company_registry.json`
- Production API hot-reloads automatically
- Model works with new company (already normalized to `[COMPANY]`)
- **No retraining needed!**

Example:
```json
// Add to backend/config/company_registry.json
{
  "company_id": "comp_047",
  "name": "MB Bank",
  "industry": "finance",
  "region": "north",
  "website": "https://mbbank.com.vn"
}
```
→ API reloads → Models work immediately!

### 3. **Single Source of Truth**
- Company registry managed in **ONE place**
- Update once → benefits both training and deployment
- Version control tracks all changes
- No synchronization issues

### 4. **Easier Maintenance**
- Bug fix in registry → automatically applies to all 21 models
- No need to update notebooks manually
- Consistent behavior across all classifiers
- 95% reduction in maintenance effort

---

## 🚀 Setup Guide for Google Colab

**See Detailed Instructions**: `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md`

### Method 1: Google Drive Upload (Recommended)

```python
# Step 1: Upload VeriSyntra/backend/ folder to Google Drive

# Step 2: Mount Drive in Colab
from google.colab import drive
drive.mount('/content/drive')

# Step 3: Set backend path
BACKEND_PATH = '/content/drive/MyDrive/VeriSyntra/backend'

# Step 4: Add to Python path
import sys
sys.path.insert(0, BACKEND_PATH)

# Step 5: Import production modules
from app.core.company_registry import get_registry, CompanyRegistry
from app.core.pdpl_normalizer import get_normalizer, PDPLTextNormalizer

# Step 6: Initialize
registry = get_registry()
normalizer = get_normalizer()

print(f"✅ Backend loaded: {registry.get_statistics()['total_companies']} companies")
```

### Method 2: Direct File Upload

```python
# Step 1: Upload files using Colab file browser
# Upload to: /content/backend/app/core/ and /content/backend/config/

# Step 2: Set backend path
BACKEND_PATH = '/content/backend'

# Step 3: Continue with steps 4-6 from Method 1
```

### Method 3: GitHub Clone

```python
# Step 1: Clone VeriSyntra repository
!git clone https://github.com/tmhathucgit/VeriSyntra.git /content/VeriSyntra

# Step 2: Set backend path
BACKEND_PATH = '/content/VeriSyntra/backend'

# Step 3: Continue with steps 4-6 from Method 1
```

---

## ✅ Verification Checklist (Required for ALL Models)

**Before training ANY model, verify:**

```python
import os
import sys

# ✅ Check 1: Files exist
assert os.path.exists(f'{BACKEND_PATH}/app/core/company_registry.py'), \
    "company_registry.py not found!"
assert os.path.exists(f'{BACKEND_PATH}/app/core/pdpl_normalizer.py'), \
    "pdpl_normalizer.py not found!"
assert os.path.exists(f'{BACKEND_PATH}/config/company_registry.json'), \
    "company_registry.json not found!"

print("✅ Check 1 PASSED: All backend files exist")

# ✅ Check 2: Python path configured
sys.path.insert(0, BACKEND_PATH)
print(f"✅ Check 2 PASSED: Backend path added: {BACKEND_PATH}")

# ✅ Check 3: Imports work
try:
    from app.core.company_registry import get_registry, CompanyRegistry
    from app.core.pdpl_normalizer import get_normalizer, PDPLTextNormalizer
    print("✅ Check 3 PASSED: Imports successful")
except ImportError as e:
    print(f"❌ Check 3 FAILED: {e}")
    raise

# ✅ Check 4: Registry loaded (46+ companies)
registry = get_registry()
stats = registry.get_statistics()
assert stats['total_companies'] >= 46, \
    f"❌ Only {stats['total_companies']} companies loaded (expected 46+)"

print(f"✅ Check 4 PASSED: {stats['total_companies']} companies loaded")
print(f"   Industries: {stats['industries']}")
print(f"   Regions: {stats['regions']}")

# ✅ Check 5: Normalizer works
normalizer = get_normalizer()
test_text = "Vietcombank thu thập dữ liệu khách hàng"
result = normalizer.normalize_text(test_text)

assert '[COMPANY]' in result.normalized_text, \
    "❌ Normalization failed - [COMPANY] token not found"

print(f"✅ Check 5 PASSED: Normalizer working")
print(f"   Original: {test_text}")
print(f"   Normalized: {result.normalized_text}")

print("\n" + "="*60)
print("✅ ALL CHECKS PASSED - Production backend ready for training")
print("="*60)
```

---

## 📋 Applies to ALL 21 Models

| Model Type | Vietnamese | English | Backend Required |
|-----------|-----------|---------|------------------|
| **Phase 0** |||
| VeriAIDPO_Principles | ✅ VI | ✅ EN | ✅ MANDATORY |
| **Phase 1 (Critical)** |||
| VeriAIDPO_LegalBasis | ✅ VI | ✅ EN | ✅ MANDATORY |
| VeriAIDPO_BreachTriage | ✅ VI | ✅ EN | ✅ MANDATORY |
| VeriAIDPO_CrossBorder | ✅ VI | ✅ EN | ✅ MANDATORY |
| **Phase 2 (Validation)** |||
| VeriAIDPO_ConsentType | ✅ VI | ✅ EN | ✅ MANDATORY |
| VeriAIDPO_DataSensitivity | ✅ VI | ✅ EN | ✅ MANDATORY |
| VeriAIDPO_DPOTasks | ✅ VI | ✅ EN | ✅ MANDATORY |
| VeriAIDPO_RiskLevel | ✅ VI | ✅ EN | ✅ MANDATORY |
| **Phase 3 (Enhanced UX)** |||
| VeriAIDPO_ComplianceStatus | ✅ VI | ✅ EN | ✅ MANDATORY |
| VeriAIDPO_Regional | ✅ VI | ✅ EN | ✅ MANDATORY |
| VeriAIDPO_Industry | ✅ VI | ✅ EN | ✅ MANDATORY |

**No exceptions - ALL models must use production backend modules.**

---

## 🎨 Hard Dataset Strategy

**All models use HARD datasets with controlled ambiguity (not easy keyword-based templates)**

### Why Hard Datasets?

- ✅ **Production-Ready**: Models must handle real-world Vietnamese business documents
- ✅ **No Overfitting**: 78-88% accuracy more realistic than 100% on easy templates
- ✅ **Semantic Understanding**: Models learn context, not keywords
- ✅ **Investor Confidence**: Realistic metrics more credible than inflated numbers

### Dataset Difficulty Levels

**Vietnamese Models (PRIMARY)**:
```python
VIETNAMESE_COMPOSITION = {
    'VERY_HARD': 0.40,    # 40% - Multi-principle overlap + regional variations
    'HARD': 0.40,         # 40% - No keywords + cultural context
    'MEDIUM': 0.15,       # 15% - Subtle keywords + formality
    'EASY': 0.05,         # 5% - Clear examples (minimal)
}
```

**English Models (SECONDARY)**:
```python
ENGLISH_COMPOSITION = {
    'VERY_HARD': 0.30-0.35,  # 30-35% - Multi-principle overlap
    'HARD': 0.40,            # 40% - No keywords, semantic only
    'MEDIUM': 0.18-0.20,     # 18-20% - Subtle keywords
    'EASY': 0.07-0.10,       # 7-10% - Clear examples
}
```

### Key Differences

| Aspect | Vietnamese | English |
|--------|-----------|---------|
| **Regional Variations** | 3 (North/Central/South) | 0 (Standard) |
| **Formality Levels** | 4 (Legal/Formal/Business/Casual) | 2 (Formal/Business) |
| **Total Samples** | 93,600 | 56,200 |
| **Expected Accuracy** | 78-88% | 82-90% |
| **VERY_HARD Ratio** | 40% | 30-35% |
| **Dataset Difficulty** | HARD | MODERATE-HARD |

---

## 🔧 Production Backend Module Details

### CompanyRegistry Class

**File**: `backend/app/core/company_registry.py` (513 lines)

**Key Methods**:
```python
class CompanyRegistry:
    def get_statistics() -> dict:
        """Returns company counts by industry and region"""
        
    def search_companies(query: str, industry: str = None, region: str = None) -> list:
        """Search companies by name, industry, or region"""
        
    def add_company(company_data: dict) -> bool:
        """Add new company to registry"""
        
    def remove_company(company_id: str) -> bool:
        """Remove company from registry"""
        
def get_registry() -> CompanyRegistry:
    """Singleton pattern - returns same instance"""
```

**Usage in Training**:
```python
registry = get_registry()
companies = registry.get_companies_by_industry('finance')
# Use companies for template generation
```

### PDPLTextNormalizer Class

**File**: `backend/app/core/pdpl_normalizer.py` (~300 lines)

**Key Methods**:
```python
class PDPLTextNormalizer:
    def normalize_text(text: str) -> NormalizationResult:
        """Replace company names with [COMPANY] token"""
        
def get_normalizer() -> PDPLTextNormalizer:
    """Singleton pattern - returns same instance"""
```

**NormalizationResult**:
```python
@dataclass
class NormalizationResult:
    original_text: str
    normalized_text: str
    companies_found: list[str]
    replacement_count: int
```

**Usage in Training**:
```python
normalizer = get_normalizer()
result = normalizer.normalize_text("VCB thu thập dữ liệu")
# result.normalized_text = "[COMPANY] thu thập dữ liệu"
# Use result.normalized_text for training
```

---

## 📚 Related Documentation

- **Colab Setup Guide**: `VeriAIDPO_Colab_Setup_Guide.md` (detailed upload instructions)
- **Implementation Overview**: `VeriAIDPO_Implementation_Overview.md` (executive summary)
- **Phase 0 Details**: `VeriAIDPO_Phase0_Principles_Retraining.md` (Principles v2.0)
- **Model Specifications**: See `Phase1_Critical_Models/`, `Phase2_Validation_Models/`, `Phase3_Enhanced_UX_Models/`

---

## ⚠️ Common Mistakes to Avoid

### ❌ Mistake 1: Recreating Classes Inline

```python
# ❌ DON'T DO THIS
class CompanyRegistry:
    def __init__(self, companies_data):
        # ~200 lines of code...
```

**Impact**: Training-production drift, maintenance nightmare

### ❌ Mistake 2: Hardcoding Company Names

```python
# ❌ DON'T DO THIS
companies = ["Vietcombank", "Viettel", "FPT"]
```

**Impact**: Cannot hot-reload new companies, rigid system

### ❌ Mistake 3: Using Different Registry Format

```python
# ❌ DON'T DO THIS
companies = {
    "VCB": {"name": "Vietcombank", "type": "bank"},
    # Different format from production...
}
```

**Impact**: Normalization mismatch between training and production

### ❌ Mistake 4: Skipping Verification Checks

```python
# ❌ DON'T DO THIS
from app.core.company_registry import get_registry
registry = get_registry()
# No verification - might fail silently
```

**Impact**: Training with incomplete/wrong data

---

## ✅ Checklist for Every New Model

Before creating a training notebook:

- [ ] Upload 3 backend files to Colab
- [ ] Set `BACKEND_PATH` variable
- [ ] Add backend to `sys.path`
- [ ] Import `get_registry()` and `get_normalizer()`
- [ ] Run ALL 5 verification checks
- [ ] Verify 46+ companies loaded
- [ ] Test normalization with sample text
- [ ] Use `registry` for company selection in templates
- [ ] Use `normalizer` for text normalization before training
- [ ] Document backend version used in notebook metadata

---

**Last Updated**: October 18, 2025  
**Mandatory Compliance**: ALL 21 models must follow these requirements  
**No Exceptions**: Production backend integration is non-negotiable
