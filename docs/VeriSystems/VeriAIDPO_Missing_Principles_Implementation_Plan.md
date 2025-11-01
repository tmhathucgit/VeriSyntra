# VeriAIDPO - Missing PDPL Principles Implementation Plan
## Comprehensive Training Plan for Enhanced DPO Role Support

**Document Version**: 1.1  
**Created**: October 13, 2025  
**Updated**: October 18, 2025 - ✅ Vietnamese v2.0 Training Notebook Created  
**Status**: � Phase 0 In Progress - Notebook Ready for Training  
**Priority**: 🚨 High - Critical for Production DPO Automation

---

## 📊 Executive Summary

**Current State**: VeriAIDPO_Principles MVP trained with 4,488 samples (90-93% accuracy on easy synthetic data)

**🇻🇳 Primary Model (Vietnamese) - REQUIRES RETRAINING**:
- **Model Name**: VeriAIDPO_Principles_VI
- **Current Version**: v1.0_MVP (4,488 samples, trained Oct 6, 2025)
  - Accuracy: 90-93% on EASY synthetic data
  - Purpose: Investor demo, proof of concept
  - Status: ✅ Working for MVP
- **Planned Version**: v2.0_Production (24,000 samples)
  - Dataset: HARD with 40% VERY_HARD + 40% HARD ambiguity
  - Target Accuracy: 78-88% (production-grade on real Vietnamese docs)
  - Status: ✅ **NOTEBOOK CREATED** - `VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`
  - Notebook Date: October 18, 2025
  - Ready for: Google Colab Pro+ training (2-3 days)
  - Features: Dynamic Company Registry, 5-layer data leak detection, company-agnostic

**🇬🇧 Secondary Model (English)**:
- **Model Name**: VeriAIDPO_Principles_EN
- **Current Version**: v1.0_20251012_214305 (needs upgrade to match Vietnamese hard dataset)
- **Planned Version**: v2.0_Production (12,000 samples)
  - Dataset: MODERATE-HARD with 30-35% VERY_HARD
  - Target Accuracy: 82-90%
  - Status: 📋 Retrain with hard dataset for consistency

**Gap Analysis**: 
1. **VeriAIDPO_Principles requires RETRAINING** (4,488 → 24,000 samples for production)
2. Missing **10 additional operational classifiers** required for comprehensive DPO role automation
- Each model requires **BOTH Vietnamese (VI) and English (EN) versions**
- Vietnamese is PRIMARY, English is SECONDARY
- Total models to train: **21 models** (1 retrain + 10 new types × 2 languages)

**Impact**: Current model cannot support:
- Legal Basis determination (Article 13.1)
- Breach notification triage (Articles 37-38)
- Cross-border transfer compliance (Articles 32-36)
- Consent validation (Article 12)
- Risk assessment automation (Article 38, 44)

**Solution**: Retrain VeriAIDPO_Principles + Train 10 additional model types, each in BOTH Vietnamese and English (21 models total)

**Timeline**: 38-52 days for complete coverage (Vietnamese priority, English secondary)
- VeriAIDPO_Principles_VI retrain (v1.0 → v2.0): 2-3 days
- VeriAIDPO_Principles_EN retrain: 2-3 days
- Vietnamese new models (PRIMARY): 17-24 days
- English new models (SECONDARY): 17-24 days (can run in parallel or sequential)

**Investment**: ~$200-340 (Google Colab Pro+ GPU hours for 21 models) + 85-170 hours technical effort

---

## 🎯 Missing PDPL Principles & Requirements

### Current VeriAIDPO Coverage ⚠️

**Status**: MVP model exists but requires retraining for production

The existing **v1.0_MVP model** (4,488 samples) classifies **8 data processing principles**:

| ID | Vietnamese | English | MVP Status | Production Status |
|----|-----------|---------|------------|-------------------|
| 0 | Tính hợp pháp, công bằng và minh bạch | Lawfulness, fairness and transparency | ✅ Trained (MVP) | 📋 **Needs Retrain** (24,000 samples) |
| 1 | Hạn chế mục đích | Purpose limitation | ✅ Trained (MVP) | 📋 **Needs Retrain** |
| 2 | Tối thiểu hóa dữ liệu | Data minimization | ✅ Trained (MVP) | 📋 **Needs Retrain** |
| 3 | Tính chính xác | Accuracy | ✅ Trained (MVP) | 📋 **Needs Retrain** |
| 4 | Hạn chế lưu trữ | Storage limitation | ✅ Trained (MVP) | 📋 **Needs Retrain** |
| 5 | Tính toàn vẹn và bảo mật | Integrity and confidentiality | ✅ Trained (MVP) | 📋 **Needs Retrain** |
| 6 | Trách nhiệm giải trình | Accountability | ✅ Trained (MVP) | 📋 **Needs Retrain** |
| 7 | Quyền của chủ thể dữ liệu | Data subject rights | ✅ Trained (MVP) | 📋 **Needs Retrain** |

**Why Retrain?**
- ❌ Current: 4,488 EASY samples (keyword-based) → 90-93% accuracy on synthetic
- ✅ Production: 24,000 HARD samples (40% VERY_HARD) → 78-88% accuracy on real Vietnamese docs
- ✅ Enterprise customers need models that handle production ambiguity
- ✅ Banks, telecom, government contractors require >85% on complex cases

---

## �️ **CRITICAL: Production Backend Integration (ALL MODELS)**

**MANDATORY REQUIREMENT FOR ALL 21 MODELS**

### **Use Production Backend Modules - NOT Inline Code**

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
```

### **Required Files for ALL Colab Notebooks**

Upload these 3 files from VeriSyntra backend to Google Colab:

1. **`backend/app/core/company_registry.py`** - Production CompanyRegistry class
2. **`backend/app/core/pdpl_normalizer.py`** - Production PDPLTextNormalizer class
3. **`backend/config/company_registry.json`** - Production company database (46+ companies)

### **Why This Matters**

| Aspect | Inline Code (❌ BAD) | Backend Modules (✅ GOOD) |
|--------|---------------------|--------------------------|
| **Production Parity** | ⚠️ Risk of drift | ✅ Identical code |
| **Company Registry** | ⚠️ Manual copy | ✅ Uses `company_registry.json` |
| **Maintenance** | ❌ Update 2 places | ✅ Update 1 place |
| **Testing** | ⚠️ Different from API | ✅ Same as API |
| **Hot-reload** | ❌ Not supported | ✅ Add companies without retrain |
| **Code Duplication** | ❌ ~200 lines per notebook | ✅ 2 import lines |

### **Benefits of Production Backend Integration**

1. **Training Code = Production Code**
   - Model trains with EXACT same company registry as API
   - Normalization logic is IDENTICAL in training and inference
   - No "worked in training, fails in production" issues

2. **Hot-Reload Capability**
   - Add new company to `company_registry.json`
   - API hot-reloads automatically
   - Model works with new company (already normalized to `[COMPANY]`)
   - **No retraining needed!**

3. **Single Source of Truth**
   - Company registry managed in ONE place
   - Update once → benefits both training and deployment
   - Version control tracks all changes

4. **Easier Maintenance**
   - Bug fix in registry → automatically applies to all models
   - No need to update 21 different notebooks
   - Consistent behavior across all classifiers

### **Setup Guide for Colab**

See detailed instructions: `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md`

**Quick Start** (Google Drive method):
1. Upload `VeriSyntra/backend/` folder to Google Drive
2. In Colab notebook, set: `BACKEND_PATH = '/content/drive/MyDrive/VeriSyntra/backend'`
3. Mount Drive and import production modules
4. Verify 46+ companies loaded

### **Verification Checklist** (Required for ALL Models)

Before training ANY model, verify:

```python
# ✅ Check 1: Files exist
import os
assert os.path.exists(f'{BACKEND_PATH}/app/core/company_registry.py')
assert os.path.exists(f'{BACKEND_PATH}/app/core/pdpl_normalizer.py')
assert os.path.exists(f'{BACKEND_PATH}/config/company_registry.json')

# ✅ Check 2: Imports work
from app.core.company_registry import get_registry
from app.core.pdpl_normalizer import get_normalizer

# ✅ Check 3: Registry loaded (46+ companies)
registry = get_registry()
stats = registry.get_statistics()
assert stats['total_companies'] >= 46, f"Only {stats['total_companies']} companies loaded!"

# ✅ Check 4: Normalizer works
normalizer = get_normalizer()
result = normalizer.normalize_text("Vietcombank thu thap du lieu")
assert '[COMPANY]' in result.normalized_text, "Normalization failed!"

print("✅ All checks passed - Production backend ready for training")
```

### **This Applies to ALL 21 Models**

- ✅ VeriAIDPO_Principles (VI + EN) - Already updated
- ✅ VeriAIDPO_LegalBasis (VI + EN) - Must use backend
- ✅ VeriAIDPO_BreachTriage (VI + EN) - Must use backend
- ✅ VeriAIDPO_CrossBorder (VI + EN) - Must use backend
- ✅ VeriAIDPO_ConsentType (VI + EN) - Must use backend
- ✅ VeriAIDPO_DataSensitivity (VI + EN) - Must use backend
- ✅ VeriAIDPO_DPOTasks (VI + EN) - Must use backend
- ✅ VeriAIDPO_RiskLevel (VI + EN) - Must use backend
- ✅ VeriAIDPO_ComplianceStatus (VI + EN) - Must use backend
- ✅ VeriAIDPO_Regional (VI + EN) - Must use backend
- ✅ VeriAIDPO_Industry (VI + EN) - Must use backend

**No exceptions - ALL models must use production backend modules.**

---

## �🎨 Hard Dataset Strategy with Ambiguity

**Critical Update**: All models use HARD datasets with controlled ambiguity (not easy keyword-based templates)

### **Why Hard Datasets?**
- ✅ **Production-Ready**: Models must handle real-world Vietnamese business documents
- ✅ **No Overfitting**: 78-88% accuracy more realistic than 100% on easy templates
- ✅ **Semantic Understanding**: Models learn context, not keywords
- ✅ **Investor Confidence**: Realistic metrics more credible

### **Dataset Difficulty Levels**

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
    'HARD': 0.40,            # 40% - No keywords, semantic
    'MEDIUM': 0.18-0.20,     # 18-20% - Subtle keywords
    'EASY': 0.07-0.10,       # 7-10% - Clear examples
}
```

### **Key Differences**

| Aspect | Vietnamese | English |
|--------|-----------|---------|
| **Regional Variations** | 3 (North/Central/South) | 0 (Standard) |
| **Formality Levels** | 4 (Legal/Formal/Business/Casual) | 2 (Formal/Business) |
| **Total Samples** | 94,100 | 56,200 |
| **Expected Accuracy** | 78-88% | 82-90% |

**See Full Documentation**:
- `VeriAIDPO_Hard_Dataset_Generation_Guide.md` - Vietnamese hard dataset strategy
- `VeriAIDPO_English_Dataset_Strategy.md` - English MODERATE-HARD strategy
- `VeriAIDPO_Dataset_Size_Strategy.md` - Complete sample count breakdown

---

## � Phase 0: Retrain VeriAIDPO_Principles (PREREQUISITE)

**Priority**: 🚨 **CRITICAL - Must complete before enterprise deployment**

### **VeriAIDPO_Principles - Production Retraining**

**Current State**:
- **Version**: v1.0_MVP (trained Oct 6, 2025)
- **Samples**: 4,488 (EASY synthetic data)
- **Accuracy**: 90-93% on simple keyword-based examples
- **Purpose**: Investor demo, proof of concept ✅
- **Limitation**: Won't handle production Vietnamese compliance documents

**Production Requirements**:
- **Version**: v2.0_Production
- **Samples**: 24,000 Vietnamese + 12,000 English = **36,000 total**
- **Difficulty**: 40% VERY_HARD + 40% HARD (production-grade ambiguity)
- **Target Accuracy**: 78-88% VI, 82-90% EN (realistic for complex docs)
- **Purpose**: Enterprise customers (banks, telecom, government)

#### **Why Retraining is Critical**

| Scenario | MVP Model (4,488 samples) | Production Model (24,000 samples) |
|----------|-------------------------|----------------------------------|
| **Simple example**: "Khách hàng đồng ý nhận email marketing" | ✅ Correct (Consent) | ✅ Correct (Consent) |
| **Real bank policy**: "Căn cứ hợp đồng mở tài khoản, ngân hàng thu thập CMND để xác thực danh tính theo quy định Ngân hàng Nhà nước" | ❌ Likely wrong (sees "thu thập" → guesses Data Min) | ✅ Correct (Legal Obligation) |
| **Startup privacy**: "Chúng mình chỉ lấy thông tin cần thiết để giao hàng thôi nha! 📦" | ❌ Likely wrong (casual style not seen) | ✅ Correct (Purpose Limitation) |
| **Multi-principle overlap**: "Công ty chỉ sử dụng dữ liệu cho mục đích đã thông báo và đảm bảo bảo mật tuyệt đối" | ❌ Confused (2 principles) | ✅ Correct (identifies PRIMARY) |

**Conclusion**: MVP works for demos, but **enterprise customers need production model**

#### **Training Plan**

**Vietnamese (PRIMARY) - VeriAIDPO_Principles_VI v2.0**:
- **Total Samples**: 24,000 (8 categories × 3,000 each)
- **Difficulty Breakdown**:
  - VERY_HARD: 9,600 samples (40%) - Multi-principle overlap + no keywords
  - HARD: 9,600 samples (40%) - Regional variations + semantic only
  - MEDIUM: 3,600 samples (15%) - Subtle keywords
  - EASY: 1,200 samples (5%) - Clear examples
- **Regional Split**: 8,000 Bắc + 8,000 Trung + 8,000 Nam
- **Formality Levels**: Legal (25%), Formal (25%), Business (25%), Casual (25%)
- **Training Time**: 2-3 days
- **Cost**: $20-30 (GPU hours)

**English (SECONDARY) - VeriAIDPO_Principles_EN v2.0**:
- **Total Samples**: 12,000 (8 categories × 1,500 each)
- **Difficulty Breakdown**:
  - VERY_HARD: 3,600-4,200 samples (30-35%)
  - HARD: 4,800 samples (40%)
  - MEDIUM: 2,160-2,400 samples (18-20%)
  - EASY: 840-1,200 samples (7-10%)
- **Formality Levels**: Formal (50%), Business (50%)
- **Training Time**: 2-3 days
- **Cost**: $20-30 (GPU hours)

**Total Phase 0**: 4-6 days, $40-60, 36,000 samples

#### **✅ Vietnamese Notebook Created (v2.0)**

**Notebook File**: `docs/VeriSystems/VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`

**Key Features Implemented**:
- ✅ **Production Backend Integration** - Uses `backend/app/core/company_registry.py` and `pdpl_normalizer.py` (NOT inline code)
- ✅ Dynamic Company Registry Integration (zero hardcoded companies)
- ✅ 24,000 hard samples with 40% VERY_HARD + 40% HARD ambiguity
- ✅ 5-layer data leak detection and prevention
- ✅ Company-agnostic training ([COMPANY] token normalization)
- ✅ Regional variations (North, Central, South Vietnamese contexts)
- ✅ Company distribution balance tracking
- ✅ Train/Val/Test split with leak detection
- ✅ PhoBERT-base-v2 fine-tuning configuration
- ✅ Company-agnostic testing with NEW companies
- ✅ Model export with registry metadata

**Production Backend Files Used**:
- `backend/app/core/company_registry.py` - Production CompanyRegistry class
- `backend/app/core/pdpl_normalizer.py` - Production PDPLTextNormalizer class
- `backend/config/company_registry.json` - Production company database (46+ companies)

**Notebook Structure (22 cells)**:
1. Title and Overview (Markdown - includes backend integration architecture)
2. Environment Setup (Python - packages installation)
3. Dynamic Company Registry Setup (Markdown - upload instructions for backend files)
4. Load Production Backend Modules (Python - import from VeriSyntra backend, NOT inline code)
5. Initialize Production Normalizer (Python - uses production PDPLTextNormalizer)
6. Dataset Generator with Data Leak Detection (Python - 214 lines)
7. Generate 24,000 Production Samples (Python - 125 lines)
8. Data Leak Detection (Python - 5-layer validation, 138 lines)
9. Dataset Preparation and Split (Python - train/val/test with leak check)
10. Model Training with PhoBERT (Python - 158 lines)
11. Company-Agnostic Testing (Python - test with NEW companies)
12. Model Export with Metadata (Python - save model + registry info)
13. Completion Summary (Markdown - deployment checklist)

**Data Leak Prevention Strategy**:
- Layer 1: Template diversity analysis (>70% target)
- Layer 2: Normalized sample uniqueness (>95% target)
- Layer 3: Company distribution balance (min/max ratio >30%)
- Layer 4: Category distribution balance (<10% deviation)
- Layer 5: Train/Val/Test split overlap detection

**Next Steps**:
1. Upload notebook to Google Colab Pro+
2. Execute training (2-3 days on T4/A100 GPU)
3. Download trained model
4. Test in VeriSyntra backend
5. Deploy to production

#### **Dataset Generation**

```python
# Step 1: Generate hard dataset for VeriAIDPO_Principles v2.0
python scripts/generate_hard_dataset.py \
    --model-type VeriAIDPO_Principles \
    --language vi \
    --total-samples 24000 \
    --very-hard-ratio 0.40 \
    --hard-ratio 0.40 \
    --use-company-registry \
    --output datasets/principles_vi_v2_hard.jsonl

python scripts/generate_hard_dataset.py \
    --model-type VeriAIDPO_Principles \
    --language en \
    --total-samples 12000 \
    --very-hard-ratio 0.33 \
    --hard-ratio 0.40 \
    --output datasets/principles_en_v2_hard.jsonl

# Step 2: Train with normalization
python scripts/train_model.py \
    --dataset datasets/principles_vi_v2_hard.jsonl \
    --model-name VeriAIDPO_Principles_VI_v2.0 \
    --base-model vinai/phobert-base \
    --normalize-companies \
    --epochs 5 \
    --batch-size 32

python scripts/train_model.py \
    --dataset datasets/principles_en_v2_hard.jsonl \
    --model-name VeriAIDPO_Principles_EN_v2.0 \
    --base-model bert-base-uncased \
    --normalize-companies \
    --epochs 5 \
    --batch-size 32
```

#### **Success Criteria**

- ✅ Vietnamese accuracy: 78-88% on test set
- ✅ English accuracy: 82-90% on test set
- ✅ Handles multi-principle overlap correctly (primary principle identification)
- ✅ Works with all 3 Vietnamese regions (North, Central, South)
- ✅ Handles all 4 formality levels (Legal, Formal, Business, Casual)
- ✅ Inference speed: <50ms per classification
- ✅ Company-agnostic (normalized to [COMPANY] token)

#### **Deployment Strategy**

```python
# Zero-downtime deployment
# 1. Keep v1.0_MVP running (investor demos)
# 2. Deploy v2.0_Production (enterprise customers)
# 3. Route based on customer type

class PrinciplesClassifier:
    def __init__(self):
        self.mvp_model = load_model("VeriAIDPO_Principles_VI_v1.0")
        self.prod_model = load_model("VeriAIDPO_Principles_VI_v2.0")
    
    def classify(self, text: str, customer_tier: str = "enterprise"):
        if customer_tier == "demo":
            # Use MVP for demos (faster, simpler)
            return self.mvp_model.predict(text)
        else:
            # Use production model for paying customers
            return self.prod_model.predict(text)
```

---

## �🚨 Phase 1: Critical Operational Models (HIGH PRIORITY)

### **1. VeriAIDPO_LegalBasis - Legal Basis Classification**

**Priority**: 🚨 CRITICAL  
**PDPL Reference**: Article 13.1 (a-f)  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2-3 days
- English (EN - SECONDARY): 2-3 days
- **Total**: 4-6 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_LegalBasis_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_LegalBasis_EN` (BERT, English secondary)

**Use Cases**: Legal Basis Setup wizard, compliance validation, processing activity records

#### Categories (4 classes):
```python
LEGAL_BASIS_CATEGORIES = {
    0: {
        "en": "Consent",
        "vi": "Đồng ý của chủ thể dữ liệu",
        "pdpl_article": "Article 13.1.a",
        "description_en": "Data subject has given explicit consent for processing",
        "description_vi": "Chủ thể dữ liệu đã đồng ý rõ ràng cho việc xử lý",
        "examples_en": [
            "User subscribes to marketing newsletter",
            "Customer opts in to promotional emails",
            "Visitor accepts cookies on website"
        ],
        "examples_vi": [
            "Người dùng đăng ký nhận bản tin marketing",
            "Khách hàng chọn nhận email khuyến mãi",
            "Khách truy cập chấp nhận cookies trên website"
        ]
    },
    1: {
        "en": "Contract Performance",
        "vi": "Thực hiện hợp đồng",
        "pdpl_article": "Article 13.1.b",
        "description_en": "Processing necessary for contract execution",
        "description_vi": "Xử lý cần thiết để thực hiện hợp đồng",
        "examples_en": [
            "Processing payment for online order",
            "Shipping customer address for delivery",
            "Account management for service provision"
        ],
        "examples_vi": [
            "Xử lý thanh toán cho đơn hàng trực tuyến",
            "Giao hàng theo địa chỉ khách hàng",
            "Quản lý tài khoản để cung cấp dịch vụ"
        ]
    },
    2: {
        "en": "Legal Obligation",
        "vi": "Nghĩa vụ pháp lý",
        "pdpl_article": "Article 13.1.c",
        "description_en": "Processing required by Vietnamese law",
        "description_vi": "Xử lý theo yêu cầu của luật pháp Việt Nam",
        "examples_en": [
            "Tax reporting to Vietnamese authorities",
            "Employee salary reporting to social insurance",
            "MPS compliance reporting"
        ],
        "examples_vi": [
            "Báo cáo thuế cho cơ quan thuế Việt Nam",
            "Báo cáo lương nhân viên cho bảo hiểm xã hội",
            "Báo cáo tuân thủ cho Bộ Công an"
        ]
    },
    3: {
        "en": "Legitimate Interest",
        "vi": "Lợi ích chính đáng",
        "pdpl_article": "Article 13.1.f",
        "description_en": "Processing for legitimate business interests (with balancing test)",
        "description_vi": "Xử lý cho lợi ích kinh doanh chính đáng (cần cân nhắc)",
        "examples_en": [
            "Fraud prevention and security monitoring",
            "Network security threat detection",
            "Internal audit and compliance monitoring"
        ],
        "examples_vi": [
            "Phòng chống gian lận và giám sát bảo mật",
            "Phát hiện mối đe dọa an ninh mạng",
            "Kiểm toán nội bộ và giám sát tuân thủ"
        ]
    }
}
```

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_LegalBasis_VI**:
- **Total Samples**: 10,000 (2,500 per category)
- **Difficulty**: VERY HARD with high ambiguity
- **Dataset Composition**:
  - VERY_HARD: 1,000 samples/category (40%) - Overlapping legal bases
  - HARD: 1,000 samples/category (40%) - No legal keywords
  - MEDIUM: 350 samples/category (14%) - Subtle legal language
  - EASY: 150 samples/category (6%) - Clear legal basis
- **Regional Variations**: North (formal), Central (balanced), South (casual)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**:
  - Vietnamese e-commerce consent forms (Shopee, Tiki, Lazada)
  - Banking contract terms (VCB, Techcombank, VPBank)
  - Tax reporting documentation (GSO, MPS)
  - Security policy documents (Viettel, FPT)

**English (SECONDARY) - VeriAIDPO_LegalBasis_EN**:
- **Total Samples**: 6,000 (1,500 per category)
- **Difficulty**: MODERATE-HARD with controlled ambiguity
- **Dataset Composition**:
  - VERY_HARD: 525 samples/category (35%) - Overlapping legal bases
  - HARD: 600 samples/category (40%) - No legal keywords
  - MEDIUM: 270 samples/category (18%) - Subtle legal language
  - EASY: 105 samples/category (7%) - Clear legal basis
- **Formality Levels**: Formal, Business
- **Sources**: International compliance documents, GDPR comparisons, standard business agreements

#### Template Examples:
```python
# Consent (Category 0)
"Khách hàng đồng ý cho {company} gửi email khuyến mãi về sản phẩm mới."
"User gives permission to {company} to send promotional notifications."

# Contract (Category 1)
"{company} xử lý thông tin thanh toán để hoàn tất giao dịch mua hàng của khách."
"{company} processes payment information to complete customer purchase transaction."

# Legal Obligation (Category 2)
"{company} báo cáo dữ liệu lương nhân viên cho cơ quan bảo hiểm xã hội theo luật."
"{company} reports employee salary data to social insurance as required by law."

# Legitimate Interest (Category 3)
"{company} giám sát truy cập hệ thống để phát hiện hoạt động đáng ngờ và bảo vệ khách hàng."
"{company} monitors system access to detect suspicious activity and protect customers."
```

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_LegalBasis_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"  # Vietnamese PhoBERT
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 10000  # 2,500 per category
DATASET_DIFFICULTY = "VERY_HARD"  # 40% VERY_HARD, 40% HARD, 14% MEDIUM, 6% EASY
EPOCHS = 8-10  # More epochs for hard dataset
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256  # Longer for complex Vietnamese sentences
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_LegalBasis_EN)**:
```python
MODEL_NAME = "bert-base-uncased"  # English BERT
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 6000  # 1,500 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 35% VERY_HARD, 40% HARD, 18% MEDIUM, 7% EASY
EPOCHS = 6-8  # Fewer epochs (BERT has more pre-training)
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128  # Standard for English
FORMALITY_LEVELS = ['formal', 'business']
```

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_LegalBasis_VI)**:
- **Target Accuracy**: 82-88% (production-grade with hard dataset)
- **Confidence**: 78-85% average
- **Inference Speed**: <50ms per request
- **Dataset**: 10,000 samples with 40% VERY_HARD ambiguity

**English Model (VeriAIDPO_LegalBasis_EN)**:
- **Target Accuracy**: 85-90% (production-grade with moderate-hard dataset)
- **Confidence**: 82-88% average
- **Inference Speed**: <50ms per request
- **Dataset**: 6,000 samples with 35% VERY_HARD ambiguity

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

### **2. VeriAIDPO_BreachTriage - Breach Notification Classification**

**Priority**: 🚨 CRITICAL  
**PDPL Reference**: Articles 37-38, Decree 13/2023 Article 18  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2-3 days
- English (EN - SECONDARY): 2-3 days
- **Total**: 4-6 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_BreachTriage_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_BreachTriage_EN` (BERT, English secondary)

**Use Cases**: Incident response automation, breach triage, MPS notification triggers

#### Categories (4 classes):
```python
BREACH_SEVERITY_CATEGORIES = {
    0: {
        "en": "Low Risk",
        "vi": "Rủi ro Thấp",
        "notification": "Internal only - Document and monitor",
        "notification_vi": "Nội bộ - Ghi chép và theo dõi",
        "timeline": "None required",
        "examples_en": [
            "Minor configuration error affecting non-sensitive data",
            "Brief system downtime with no data exposure",
            "Isolated access log anomaly"
        ],
        "examples_vi": [
            "Lỗi cấu hình nhỏ ảnh hưởng dữ liệu không nhạy cảm",
            "Hệ thống gián đoạn ngắn không lộ dữ liệu",
            "Log truy cập bất thường đơn lẻ"
        ]
    },
    1: {
        "en": "Medium Risk",
        "vi": "Rủi ro Trung bình",
        "notification": "Internal notification + DPO review",
        "notification_vi": "Thông báo nội bộ + DPO xem xét",
        "timeline": "Within 7 days",
        "examples_en": [
            "Unauthorized access to limited personal data",
            "Email sent to wrong recipient list (small scale)",
            "Temporary exposure of non-sensitive customer data"
        ],
        "examples_vi": [
            "Truy cập trái phép vào dữ liệu cá nhân hạn chế",
            "Email gửi nhầm danh sách người nhận (quy mô nhỏ)",
            "Lộ tạm thời dữ liệu khách hàng không nhạy cảm"
        ]
    },
    2: {
        "en": "High Risk",
        "vi": "Rủi ro Cao",
        "notification": "MPS notification required within 72 hours + Data subject notification",
        "notification_vi": "Báo cáo Bộ Công an trong 72 giờ + Thông báo chủ thể dữ liệu",
        "timeline": "Within 72 hours",
        "examples_en": [
            "Exposure of sensitive personal data (health, financial)",
            "Large-scale data breach affecting 1000+ individuals",
            "Ransomware attack encrypting customer database"
        ],
        "examples_vi": [
            "Lộ dữ liệu cá nhân nhạy cảm (sức khỏe, tài chính)",
            "Vi phạm dữ liệu quy mô lớn ảnh hưởng 1000+ người",
            "Tấn công ransomware mã hóa cơ sở dữ liệu khách hàng"
        ]
    },
    3: {
        "en": "Critical Risk",
        "vi": "Rủi ro Nghiêm trọng",
        "notification": "Immediate MPS notification + Public disclosure + Data subject notification",
        "notification_vi": "Báo cáo Bộ Công an ngay lập tức + Công bố công khai + Thông báo chủ thể",
        "timeline": "Immediate (within 24 hours)",
        "examples_en": [
            "National security implications",
            "Banking/financial system breach",
            "Children's data exposure at scale",
            "Systematic data exfiltration by foreign entities"
        ],
        "examples_vi": [
            "Liên quan đến an ninh quốc gia",
            "Vi phạm hệ thống ngân hàng/tài chính",
            "Lộ dữ liệu trẻ em quy mô lớn",
            "Đánh cắp dữ liệu có hệ thống bởi tổ chức nước ngoài"
        ]
    }
}
```

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_BreachTriage_VI**:
- **Total Samples**: 10,000 (2,500 per severity level)
- **Difficulty**: VERY HARD (critical safety task)
- **Dataset Composition**:
  - VERY_HARD: 1,000 samples/category (40%) - Borderline severity cases
  - HARD: 1,000 samples/category (40%) - No severity keywords
  - MEDIUM: 350 samples/category (14%) - Subtle severity indicators
  - EASY: 150 samples/category (6%) - Clear severity examples
- **Regional Variations**: North (formal), Central (balanced), South (casual)
- **Sources**:
  - Vietnamese breach reports (anonymized)
  - Security incident scenarios
  - MPS guidelines and case studies
  - International breach databases (translated to Vietnamese)

**English (SECONDARY) - VeriAIDPO_BreachTriage_EN**:
- **Total Samples**: 6,000 (1,500 per severity level)
- **Difficulty**: MODERATE-HARD (critical safety task)
- **Dataset Composition**:
  - VERY_HARD: 525 samples/category (35%) - Borderline severity cases
  - HARD: 600 samples/category (40%) - No severity keywords
  - MEDIUM: 270 samples/category (18%) - Subtle severity indicators
  - EASY: 105 samples/category (7%) - Clear severity examples
- **Sources**: International breach reports, security incident databases, GDPR breach examples

#### Template Examples:
```python
# Low Risk (Category 0)
"Hệ thống {company} bị lỗi trong 10 phút nhưng không có dữ liệu nào bị truy cập trái phép."
"{company} system error for 10 minutes but no unauthorized data access occurred."

# Medium Risk (Category 1)
"Nhân viên {company} vô tình gửi email chứa 50 địa chỉ khách hàng cho người không liên quan."
"{company} employee accidentally sent email with 50 customer addresses to unrelated person."

# High Risk (Category 2)
"Tin tặc xâm nhập hệ thống {company} và truy cập thông tin thẻ tín dụng của 5,000 khách hàng."
"Hackers breached {company} system and accessed credit card info of 5,000 customers."

# Critical Risk (Category 3)
"Dữ liệu nhạy cảm về an ninh quốc gia bị rò rỉ từ hệ thống của {company}."
"Sensitive national security data leaked from {company} system."
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

### **3. VeriAIDPO_CrossBorder - Cross-Border Transfer Classification**

**Priority**: 🚨 CRITICAL  
**PDPL Reference**: Articles 32-36, Decree 13/2023 Articles 10-11  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 3-4 days
- English (EN - SECONDARY): 3-4 days
- **Total**: 6-8 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_CrossBorder_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_CrossBorder_EN` (BERT, English secondary)

**Use Cases**: Cross-border transfer wizard, data flow monitoring, MPS approval automation

#### Categories (5 classes):
```python
CROSS_BORDER_CATEGORIES = {
    0: {
        "en": "Domestic Only",
        "vi": "Chỉ trong nước",
        "mps_approval": "Not required",
        "risk_level": "Low",
        "examples_en": [
            "Data stored on Viettel IDC servers in Hanoi",
            "Processing within Vietnam using VNG Cloud",
            "Local backup to FPT Data Center in HCMC"
        ],
        "examples_vi": [
            "Dữ liệu lưu trữ trên máy chủ Viettel IDC tại Hà Nội",
            "Xử lý trong nước sử dụng VNG Cloud",
            "Sao lưu cục bộ tại FPT Data Center TP.HCM"
        ]
    },
    1: {
        "en": "Approved Country Transfer",
        "vi": "Chuyển sang Quốc gia Được phê duyệt",
        "mps_approval": "General approval (notification only)",
        "risk_level": "Low",
        "examples_en": [
            "Transfer to Singapore data center (ASEAN adequacy)",
            "Backup to approved ASEAN cloud provider",
            "Processing by approved international partner"
        ],
        "examples_vi": [
            "Chuyển sang trung tâm dữ liệu Singapore (ASEAN được phê duyệt)",
            "Sao lưu sang nhà cung cấp cloud ASEAN được phê duyệt",
            "Xử lý bởi đối tác quốc tế được phê duyệt"
        ]
    },
    2: {
        "en": "Requires MPS Approval",
        "vi": "Yêu cầu Phê duyệt Bộ Công an",
        "mps_approval": "Required - DTIA submission",
        "risk_level": "Medium",
        "examples_en": [
            "Transfer to US cloud provider (AWS, Google, Azure)",
            "European data processing center",
            "International vendor without adequacy decision"
        ],
        "examples_vi": [
            "Chuyển sang nhà cung cấp cloud Mỹ (AWS, Google, Azure)",
            "Trung tâm xử lý dữ liệu châu Âu",
            "Nhà cung cấp quốc tế chưa có quyết định tương đương"
        ]
    },
    3: {
        "en": "Prohibited Transfer",
        "vi": "Chuyển bị Cấm",
        "mps_approval": "Not allowed",
        "risk_level": "Critical",
        "examples_en": [
            "Transfer to embargoed country",
            "Sensitive national security data export",
            "Transfer without legal basis or safeguards"
        ],
        "examples_vi": [
            "Chuyển sang quốc gia bị cấm vận",
            "Xuất khẩu dữ liệu nhạy cảm an ninh quốc gia",
            "Chuyển không có cơ sở pháp lý hoặc biện pháp bảo vệ"
        ]
    },
    4: {
        "en": "Unknown/Needs Assessment",
        "vi": "Chưa rõ/Cần Đánh giá",
        "mps_approval": "Assessment required",
        "risk_level": "Medium",
        "examples_en": [
            "New vendor with unclear data location",
            "Third-party service with unknown sub-processors",
            "Cloud service without data residency commitment"
        ],
        "examples_vi": [
            "Nhà cung cấp mới với vị trí dữ liệu không rõ",
            "Dịch vụ bên thứ ba với sub-processor không rõ",
            "Dịch vụ cloud không cam kết data residency"
        ]
    }
}
```

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_CrossBorder_VI**:
- **Total Samples**: 10,000 (2,000 per category)
- **Difficulty**: HARD (MPS context, country variations)
- **Dataset Composition**:
  - VERY_HARD: 700 samples/category (35%) - Unclear country adequacy
  - HARD: 800 samples/category (40%) - No location keywords
  - MEDIUM: 350 samples/category (17.5%) - Subtle location hints
  - EASY: 150 samples/category (7.5%) - Clear location examples
- **Regional Variations**: North (formal), Central (balanced), South (casual)
- **Sources**:
  - Vietnamese cloud provider documentation (Viettel, FPT, VNG)
  - International transfer agreements
  - MPS adequacy decisions
  - Data processing agreements (DPAs)

**English (SECONDARY) - VeriAIDPO_CrossBorder_EN**:
- **Total Samples**: 6,000 (1,200 per category)
- **Difficulty**: MODERATE-HARD (international context)
- **Dataset Composition**:
  - VERY_HARD: 420 samples/category (35%) - Unclear country adequacy
  - HARD: 480 samples/category (40%) - No location keywords
  - MEDIUM: 216 samples/category (18%) - Subtle location hints
  - EASY: 84 samples/category (7%) - Clear location examples
- **Sources**: International data transfer agreements, GDPR adequacy decisions, cloud provider documentation

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

## ⚠️ Phase 2: Validation & Assessment Models (MEDIUM PRIORITY)

### **4. VeriAIDPO_ConsentType - Consent Mechanism Classification**

**Priority**: ⚠️ MEDIUM  
**PDPL Reference**: Article 12, Decree 13/2023 Article 4  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 1-2 days
- English (EN - SECONDARY): 1-2 days
- **Total**: 2-4 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_ConsentType_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_ConsentType_EN` (BERT, English secondary)

**Classes**: 4 (Explicit, Implied, Parental, Invalid)

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_ConsentType_VI**:
- **Total Samples**: 6,000 (1,500 per category)
- **Difficulty**: MODERATE-HARD (consent ambiguity)
- **Dataset Composition**:
  - **VERY_HARD**: 450/category (30%) - Borderline explicit/implied consent, unclear parental authority
  - **HARD**: 600/category (40%) - No consent keywords, semantic understanding required
  - **MEDIUM**: 300/category (20%) - Subtle consent language hints
  - **EASY**: 150/category (10%) - Clear consent examples
- **Regional Variations**: North (formal consent), Central (balanced), South (casual consent)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**: Vietnamese e-commerce consent forms, banking agreements, healthcare consent, mobile app permissions

**English (SECONDARY) - VeriAIDPO_ConsentType_EN**:
- **Total Samples**: 4,000 (1,000 per category)
- **Difficulty**: MODERATE-HARD
- **Dataset Composition**:
  - **VERY_HARD**: 300/category (30%) - Borderline consent mechanisms
  - **HARD**: 400/category (40%) - No explicit consent keywords
  - **MEDIUM**: 200/category (20%) - Subtle consent indicators
  - **EASY**: 100/category (10%) - Clear consent examples
- **Formality Levels**: Formal, Business
- **Sources**: International consent forms, GDPR consent examples, cookie consent patterns

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_ConsentType_VI)**:
- Target Accuracy: 78-85% (production-grade with consent ambiguity)
- Confidence: 75-82% average
- Inference Speed: <50ms
- Dataset: 6,000 samples with 30% VERY_HARD ambiguity

**English Model (VeriAIDPO_ConsentType_EN)**:
- Target Accuracy: 82-88% (production-grade)
- Confidence: 80-85% average
- Inference Speed: <50ms
- Dataset: 4,000 samples with 30% VERY_HARD ambiguity

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_ConsentType_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 6000  # 1,500 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
EPOCHS = 6-8
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_ConsentType_EN)**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 4000  # 1,000 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
EPOCHS = 5-7
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

### **5. VeriAIDPO_DataSensitivity - Data Category Classification**

**Priority**: ⚠️ MEDIUM  
**PDPL Reference**: Article 4, Article 11  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2 days
- English (EN - SECONDARY): 2 days
- **Total**: 4 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_DataSensitivity_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_DataSensitivity_EN` (BERT, English secondary)

**Classes**: 4 (Basic, Personal, Sensitive, Special Category)

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_DataSensitivity_VI**:
- **Total Samples**: 6,000 (1,500 per category)
- **Difficulty**: MODERATE-HARD (data classification ambiguity)
- **Dataset Composition**:
  - **VERY_HARD**: 450/category (30%) - Borderline personal/sensitive, unclear special category
  - **HARD**: 600/category (40%) - No data type keywords, contextual classification required
  - **MEDIUM**: 300/category (20%) - Subtle data sensitivity indicators
  - **EASY**: 150/category (10%) - Clear data category examples
- **Regional Variations**: North (strict classification), Central (balanced), South (flexible)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**: Vietnamese HR systems, healthcare records, financial services, e-commerce platforms

**English (SECONDARY) - VeriAIDPO_DataSensitivity_EN**:
- **Total Samples**: 4,000 (1,000 per category)
- **Difficulty**: MODERATE-HARD
- **Dataset Composition**:
  - **VERY_HARD**: 300/category (30%) - Borderline data categories
  - **HARD**: 400/category (40%) - No explicit data type keywords
  - **MEDIUM**: 200/category (20%) - Subtle sensitivity indicators
  - **EASY**: 100/category (10%) - Clear category examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR data categories, international data classification standards

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_DataSensitivity_VI)**:
- Target Accuracy: 78-85% (production-grade with classification ambiguity)
- Confidence: 75-82% average
- Inference Speed: <50ms
- Dataset: 6,000 samples with 30% VERY_HARD ambiguity

**English Model (VeriAIDPO_DataSensitivity_EN)**:
- Target Accuracy: 82-88% (production-grade)
- Confidence: 80-85% average
- Inference Speed: <50ms
- Dataset: 4,000 samples with 30% VERY_HARD ambiguity

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_DataSensitivity_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 6000  # 1,500 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
EPOCHS = 6-8
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_DataSensitivity_EN)**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 4000  # 1,000 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
EPOCHS = 5-7
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

### **6. VeriAIDPO_DPOTasks - DPO Task Type Classification**

**Priority**: ⚠️ MEDIUM  
**PDPL Reference**: Articles 35-38  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2 days
- English (EN - SECONDARY): 2 days
- **Total**: 4 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_DPOTasks_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_DPOTasks_EN` (BERT, English secondary)

**Classes**: 5 (Advisory, Policy, Training, Audit, Regulatory)

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_DPOTasks_VI**:
- **Total Samples**: 6,000 (1,200 per category)
- **Difficulty**: MODERATE (clear task categories, some overlap)
- **Dataset Composition**:
  - **VERY_HARD**: 360/category (30%) - Overlapping DPO tasks (advisory + policy)
  - **HARD**: 480/category (40%) - No task keywords, contextual task identification
  - **MEDIUM**: 240/category (20%) - Subtle task type indicators
  - **EASY**: 120/category (10%) - Clear DPO task examples
- **Regional Variations**: North (formal DPO structure), Central (balanced), South (flexible)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**: Vietnamese DPO job descriptions, PDPL compliance guides, MPS requirements

**English (SECONDARY) - VeriAIDPO_DPOTasks_EN**:
- **Total Samples**: 4,000 (800 per category)
- **Difficulty**: MODERATE
- **Dataset Composition**:
  - **VERY_HARD**: 240/category (30%) - Overlapping task types
  - **HARD**: 320/category (40%) - No task keywords
  - **MEDIUM**: 160/category (20%) - Subtle task indicators
  - **EASY**: 80/category (10%) - Clear task examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR DPO tasks, international data protection officer guides

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_DPOTasks_VI)**:
- Target Accuracy: 80-87% (production-grade with task overlap)
- Confidence: 78-85% average
- Inference Speed: <50ms
- Dataset: 6,000 samples with 30% VERY_HARD ambiguity

**English Model (VeriAIDPO_DPOTasks_EN)**:
- Target Accuracy: 83-90% (production-grade)
- Confidence: 82-88% average
- Inference Speed: <50ms
- Dataset: 4,000 samples with 30% VERY_HARD ambiguity

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_DPOTasks_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 5
TOTAL_SAMPLES = 6000  # 1,200 per category
DATASET_DIFFICULTY = "MODERATE"  # 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
EPOCHS = 6-8
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_DPOTasks_EN)**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 5
TOTAL_SAMPLES = 4000  # 800 per category
DATASET_DIFFICULTY = "MODERATE"  # 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
EPOCHS = 5-7
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

### **7. VeriAIDPO_RiskLevel - Risk Assessment Classification**

**Priority**: ⚠️ MEDIUM  
**PDPL Reference**: Articles 38, 44  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 1-2 days
- English (EN - SECONDARY): 1-2 days
- **Total**: 2-4 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_RiskLevel_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_RiskLevel_EN` (BERT, English secondary)

**Classes**: 4 (Low, Medium, High-DPIA Required, Critical)

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_RiskLevel_VI**:
- **Total Samples**: 8,000 (2,000 per category)
- **Difficulty**: HARD (critical risk assessment, high stakes)
- **Dataset Composition**:
  - **VERY_HARD**: 700/category (35%) - Borderline risk levels (medium vs high, high vs critical)
  - **HARD**: 800/category (40%) - No risk keywords, judgment-based assessment
  - **MEDIUM**: 350/category (17.5%) - Subtle risk indicators
  - **EASY**: 150/category (7.5%) - Clear risk level examples
- **Regional Variations**: North (conservative risk), Central (balanced), South (pragmatic risk)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**: Vietnamese data breach reports, DPIA examples, MPS risk guidelines, industry risk assessments

**English (SECONDARY) - VeriAIDPO_RiskLevel_EN**:
- **Total Samples**: 4,800 (1,200 per category)
- **Difficulty**: MODERATE-HARD (critical judgment required)
- **Dataset Composition**:
  - **VERY_HARD**: 420/category (35%) - Borderline risk assessments
  - **HARD**: 480/category (40%) - No risk keywords
  - **MEDIUM**: 216/category (18%) - Subtle risk signals
  - **EASY**: 84/category (7%) - Clear risk examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR risk assessment guides, international DPIA frameworks

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_RiskLevel_VI)**:
- Target Accuracy: 75-83% (production-grade with high judgment complexity)
- Confidence: 72-80% average
- Inference Speed: <50ms
- Dataset: 8,000 samples with 35% VERY_HARD ambiguity

**English Model (VeriAIDPO_RiskLevel_EN)**:
- Target Accuracy: 80-88% (production-grade)
- Confidence: 78-85% average
- Inference Speed: <50ms
- Dataset: 4,800 samples with 35% VERY_HARD ambiguity

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_RiskLevel_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 8000  # 2,000 per category
DATASET_DIFFICULTY = "HARD"  # 35% VERY_HARD, 40% HARD, 17.5% MEDIUM, 7.5% EASY
EPOCHS = 8-10  # More epochs for hard judgment task
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_RiskLevel_EN)**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 4800  # 1,200 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 35% VERY_HARD, 40% HARD, 18% MEDIUM, 7% EASY
EPOCHS = 6-8
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

## 🔵 Phase 3: Enhanced UX Models (LOW PRIORITY)

### **8. VeriAIDPO_ComplianceStatus - Overall Compliance Classification**

**Priority**: 🔵 LOW  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 1 day
- English (EN - SECONDARY): 1 day
- **Total**: 2 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_ComplianceStatus_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_ComplianceStatus_EN` (BERT, English secondary)

**Classes**: 4 (Compliant, Partial, Non-Compliant, Unknown)

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_ComplianceStatus_VI**:
- **Total Samples**: 4,800 (1,200 per category)
- **Difficulty**: MODERATE (lower complexity UX enhancement)
- **Dataset Composition**:
  - **VERY_HARD**: 300/category (25%) - Borderline compliance status
  - **HARD**: 480/category (40%) - No status keywords, contextual assessment
  - **MEDIUM**: 300/category (25%) - Subtle compliance indicators
  - **EASY**: 120/category (10%) - Clear compliance status
- **Regional Variations**: North (strict compliance), Central (balanced), South (flexible)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**: Vietnamese compliance audits, MPS reports, internal assessments

**English (SECONDARY) - VeriAIDPO_ComplianceStatus_EN**:
- **Total Samples**: 3,200 (800 per category)
- **Difficulty**: MODERATE
- **Dataset Composition**:
  - **VERY_HARD**: 200/category (25%) - Borderline status
  - **HARD**: 320/category (40%) - No status keywords
  - **MEDIUM**: 200/category (25%) - Subtle indicators
  - **EASY**: 80/category (10%) - Clear examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR compliance reports, international audit frameworks

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_ComplianceStatus_VI)**:
- Target Accuracy: 82-88% (production-grade for UX)
- Confidence: 80-87% average
- Inference Speed: <50ms
- Dataset: 4,800 samples with 25% VERY_HARD ambiguity

**English Model (VeriAIDPO_ComplianceStatus_EN)**:
- Target Accuracy: 85-92% (production-grade)
- Confidence: 83-90% average
- Inference Speed: <50ms
- Dataset: 3,200 samples with 25% VERY_HARD ambiguity

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_ComplianceStatus_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 4800  # 1,200 per category
DATASET_DIFFICULTY = "MODERATE"  # 25% VERY_HARD, 40% HARD, 25% MEDIUM, 10% EASY
EPOCHS = 5-7
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_ComplianceStatus_EN)**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 3200  # 800 per category
DATASET_DIFFICULTY = "MODERATE"  # 25% VERY_HARD, 40% HARD, 25% MEDIUM, 10% EASY
EPOCHS = 4-6
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

### **9. VeriAIDPO_Regional - Vietnamese Regional Context**

**Priority**: 🔵 LOW  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 1 day
- English (EN - SECONDARY): 1 day
- **Total**: 2 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_Regional_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_Regional_EN` (BERT, English secondary)

**Classes**: 3 (North, Central, South)

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_Regional_VI**:
- **Total Samples**: 4,500 (1,500 per category)
- **Difficulty**: MODERATE (clear regional patterns)
- **Dataset Composition**:
  - **VERY_HARD**: 375/category (25%) - Borderline regional context (North-Central, Central-South overlap)
  - **HARD**: 600/category (40%) - No location keywords, cultural context required
  - **MEDIUM**: 375/category (25%) - Subtle regional indicators
  - **EASY**: 150/category (10%) - Clear regional examples
- **Regional Variations**: North (Hanoi), Central (Da Nang/Hue), South (HCMC)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**: Vietnamese business documents by region, regional compliance patterns, local government interactions

**English (SECONDARY) - VeriAIDPO_Regional_EN**:
- **Total Samples**: 3,000 (1,000 per category)
- **Difficulty**: MODERATE (for international context understanding)
- **Dataset Composition**:
  - **VERY_HARD**: 250/category (25%) - Borderline regional context
  - **HARD**: 400/category (40%) - No location keywords
  - **MEDIUM**: 250/category (25%) - Subtle indicators
  - **EASY**: 100/category (10%) - Clear examples
- **Formality Levels**: Formal, Business
- **Sources**: Vietnamese regional business descriptions in English, international documentation

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_Regional_VI)**:
- Target Accuracy: 85-92% (production-grade for cultural context)
- Confidence: 83-90% average
- Inference Speed: <50ms
- Dataset: 4,500 samples with 25% VERY_HARD ambiguity

**English Model (VeriAIDPO_Regional_EN)**:
- Target Accuracy: 88-93% (production-grade)
- Confidence: 85-91% average
- Inference Speed: <50ms
- Dataset: 3,000 samples with 25% VERY_HARD ambiguity

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_Regional_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 3
TOTAL_SAMPLES = 4500  # 1,500 per category
DATASET_DIFFICULTY = "MODERATE"  # 25% VERY_HARD, 40% HARD, 25% MEDIUM, 10% EASY
EPOCHS = 5-7
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_Regional_EN)**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 3
TOTAL_SAMPLES = 3000  # 1,000 per category
DATASET_DIFFICULTY = "MODERATE"  # 25% VERY_HARD, 40% HARD, 25% MEDIUM, 10% EASY
EPOCHS = 4-6
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

### **10. VeriAIDPO_Industry - Industry-Specific Requirements**

**Priority**: 🔵 LOW  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2 days
- English (EN - SECONDARY): 2 days
- **Total**: 4 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_Industry_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_Industry_EN` (BERT, English secondary)

**Classes**: 4 (Finance, Healthcare, Education, Technology)

#### Training Dataset Requirements:

**Vietnamese (PRIMARY) - VeriAIDPO_Industry_VI**:
- **Total Samples**: 4,800 (1,200 per category)
- **Difficulty**: MODERATE (clear industry patterns)
- **Dataset Composition**:
  - **VERY_HARD**: 300/category (25%) - Cross-industry scenarios (fintech, healthtech)
  - **HARD**: 480/category (40%) - No industry keywords, contextual identification
  - **MEDIUM**: 300/category (25%) - Subtle industry indicators
  - **EASY**: 120/category (10%) - Clear industry examples
- **Regional Variations**: North (government-focused), Central (balanced), South (tech-focused)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**: Vietnamese industry compliance guides, sector-specific PDPL requirements, MPS industry circulars

**English (SECONDARY) - VeriAIDPO_Industry_EN**:
- **Total Samples**: 3,200 (800 per category)
- **Difficulty**: MODERATE
- **Dataset Composition**:
  - **VERY_HARD**: 200/category (25%) - Cross-industry scenarios
  - **HARD**: 320/category (40%) - No industry keywords
  - **MEDIUM**: 200/category (25%) - Subtle indicators
  - **EASY**: 80/category (10%) - Clear examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR industry-specific guidelines, international sector requirements

#### Success Metrics:

**Vietnamese Model (VeriAIDPO_Industry_VI)**:
- Target Accuracy: 83-90% (production-grade for industry context)
- Confidence: 80-88% average
- Inference Speed: <50ms
- Dataset: 4,800 samples with 25% VERY_HARD ambiguity

**English Model (VeriAIDPO_Industry_EN)**:
- Target Accuracy: 85-92% (production-grade)
- Confidence: 83-90% average
- Inference Speed: <50ms
- Dataset: 3,200 samples with 25% VERY_HARD ambiguity

#### Training Configuration:

**Vietnamese Model (VeriAIDPO_Industry_VI)**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 4800  # 1,200 per category
DATASET_DIFFICULTY = "MODERATE"  # 25% VERY_HARD, 40% HARD, 25% MEDIUM, 10% EASY
EPOCHS = 5-7
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**English Model (VeriAIDPO_Industry_EN)**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 3200  # 800 per category
DATASET_DIFFICULTY = "MODERATE"  # 25% VERY_HARD, 40% HARD, 25% MEDIUM, 10% EASY
EPOCHS = 4-6
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

#### 📋 Training Notebook Requirements

**CRITICAL - Architecture Compliance**:
✅ **MUST use production backend modules** (see Architecture Requirements section above)
- Import `CompanyRegistry` from `backend/app/core/company_registry.py`
- Import `PDPLTextNormalizer` from `backend/app/core/pdpl_normalizer.py`
- Upload `backend/config/company_registry.json` to Colab
- **NEVER recreate these classes inline in the notebook**

**Training-Production Parity Benefits**:
- ✅ Same normalization logic in training and production
- ✅ Same company registry data source
- ✅ Zero risk of code drift between training and deployment
- ✅ Single source of truth for updates

**Colab Setup**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md` for upload instructions

---

## 🏗️ Technical Architecture Options

### **Option A: Separate Models (Recommended for MVP)**

**Architecture**:
```
VeriAIDPO_Principles (existing)     → 8 classes
VeriAIDPO_LegalBasis (new)          → 4 classes
VeriAIDPO_BreachTriage (new)        → 4 classes
VeriAIDPO_CrossBorder (new)         → 5 classes
... (7 more models)
```

**Advantages**:
- ✅ Independent training and deployment
- ✅ Easy to update individual models
- ✅ Can prioritize critical models first
- ✅ Simpler debugging and monitoring

**Disadvantages**:
- ❌ Multiple inference calls (latency)
- ❌ Higher deployment cost (10 models)
- ❌ No cross-task learning

---

### **Option B: Multi-Task Model (Recommended for Production)**

**Architecture**:
```python
class VeriAIDPO_Complete(nn.Module):
    def __init__(self):
        self.bert = PhoBERT()  # Shared Vietnamese encoder
        
        # Multiple classification heads
        self.head_principles = nn.Linear(768, 8)      # PDPL principles
        self.head_legal_basis = nn.Linear(768, 4)     # Legal basis
        self.head_breach = nn.Linear(768, 4)          # Breach severity
        self.head_cross_border = nn.Linear(768, 5)    # Cross-border
        self.head_consent = nn.Linear(768, 4)         # Consent type
        self.head_sensitivity = nn.Linear(768, 4)     # Data sensitivity
        self.head_dpo_task = nn.Linear(768, 5)        # DPO task
        self.head_risk = nn.Linear(768, 4)            # Risk level
        self.head_compliance = nn.Linear(768, 4)      # Compliance status
        self.head_region = nn.Linear(768, 3)          # Regional context
        self.head_industry = nn.Linear(768, 4)        # Industry
    
    def forward(self, input_ids, attention_mask):
        # Shared representation
        outputs = self.bert(input_ids, attention_mask)
        pooled = outputs.pooler_output
        
        # Multiple predictions
        return {
            'principles': self.head_principles(pooled),
            'legal_basis': self.head_legal_basis(pooled),
            'breach': self.head_breach(pooled),
            'cross_border': self.head_cross_border(pooled),
            'consent': self.head_consent(pooled),
            'sensitivity': self.head_sensitivity(pooled),
            'dpo_task': self.head_dpo_task(pooled),
            'risk': self.head_risk(pooled),
            'compliance': self.head_compliance(pooled),
            'region': self.head_region(pooled),
            'industry': self.head_industry(pooled)
        }
```

**Advantages**:
- ✅ Single inference call (low latency)
- ✅ Shared Vietnamese language understanding
- ✅ Cross-task learning (better accuracy)
- ✅ Lower deployment cost (1 model)
- ✅ More efficient GPU utilization

**Disadvantages**:
- ❌ More complex training
- ❌ Harder to update individual tasks
- ❌ Requires more training data upfront

---

## 📅 Implementation Timeline

### **Phased Rollout (Recommended) - Bilingual Sequential Training**

**Note**: Each model type requires BOTH Vietnamese (VI - PRIMARY) and English (EN - SECONDARY) versions trained separately.

#### **Phase 1: Critical MVP (Weeks 1-3)** - 14-20 days
```
Week 1:
  Day 1-3:   VeriAIDPO_LegalBasis_VI training & validation (PRIMARY)
  Day 4-6:   VeriAIDPO_LegalBasis_EN training & validation (SECONDARY)
  Day 7:     Integration testing

Week 2:
  Day 8-10:  VeriAIDPO_BreachTriage_VI training & validation (PRIMARY)
  Day 11-13: VeriAIDPO_BreachTriage_EN training & validation (SECONDARY)
  Day 14:    Integration testing

Week 3:
  Day 15-18: VeriAIDPO_CrossBorder_VI training & validation (PRIMARY)
  Day 19-22: VeriAIDPO_CrossBorder_EN training & validation (SECONDARY)
  Day 23-24: Backend API integration & deployment
```

**Deliverables**:
- ✅ Legal Basis Setup wizard fully functional (Vietnamese + English)
- ✅ Breach notification automation working (Vietnamese + English)
- ✅ Cross-border transfer detection operational (Vietnamese + English)

---

#### **Phase 2: Enhanced Validation (Weeks 4-6)** - 10-16 days
```
Week 4:
  Day 25-26: VeriAIDPO_ConsentType_VI (PRIMARY)
  Day 27-28: VeriAIDPO_ConsentType_EN (SECONDARY)

Week 5:
  Day 29-30: VeriAIDPO_DataSensitivity_VI (PRIMARY)
  Day 31-32: VeriAIDPO_DataSensitivity_EN (SECONDARY)
  Day 33-34: VeriAIDPO_DPOTasks_VI (PRIMARY)
  Day 35-36: VeriAIDPO_DPOTasks_EN (SECONDARY)
  Day 37:    Integration testing

Week 6:
  Day 38-40: VeriAIDPO_RiskLevel_VI (PRIMARY)
  Day 41-43: VeriAIDPO_RiskLevel_EN (SECONDARY)
  Day 44-46: API enhancements & full system testing
```

**Deliverables**:
- ✅ Consent validation operational (Vietnamese + English)
- ✅ Data mapping automation enhanced (Vietnamese + English)
- ✅ DPO task prioritization working (Vietnamese + English)
- ✅ Risk assessment with DPIA triggers (Vietnamese + English)

---

#### **Phase 3: Production Polish (Weeks 7-8)** - 8-10 days
```
Week 7:
  Day 47-48: VeriAIDPO_ComplianceStatus_VI (PRIMARY)
  Day 49-50: VeriAIDPO_ComplianceStatus_EN (SECONDARY)
  Day 51:    VeriAIDPO_Regional_VI (PRIMARY)
  Day 52:    VeriAIDPO_Regional_EN (SECONDARY)

Week 8:
  Day 53-54: VeriAIDPO_Industry_VI (PRIMARY)
  Day 55-56: VeriAIDPO_Industry_EN (SECONDARY)
  Day 57-60: Final testing & comprehensive documentation
```

**Deliverables**:
- ✅ Complete VeriAIDPO suite operational (20 models total)
- ✅ All VeriPortal wizards AI-enhanced with bilingual support
- ✅ Production-ready deployment (Vietnamese PRIMARY, English SECONDARY)
- ✅ Comprehensive documentation

**Total Timeline**: 57-60 days (8-9 weeks) for sequential bilingual training

---

### **Parallel Training Timeline (If Resources Available)** - 30-34 days

Train Vietnamese (PRIMARY) and English (SECONDARY) models in parallel for each model type:

```
Weeks 1-2:  
  Parallel: VeriAIDPO_LegalBasis_VI + VeriAIDPO_LegalBasis_EN (4-6 days)
  Parallel: VeriAIDPO_BreachTriage_VI + VeriAIDPO_BreachTriage_EN (4-6 days)

Weeks 3-4:
  Parallel: VeriAIDPO_CrossBorder_VI + VeriAIDPO_CrossBorder_EN (6-8 days)
  Parallel: VeriAIDPO_ConsentType_VI + VeriAIDPO_ConsentType_EN (2-4 days)

Weeks 5-6:
  Parallel: VeriAIDPO_DataSensitivity_VI + VeriAIDPO_DataSensitivity_EN (4 days)
  Parallel: VeriAIDPO_DPOTasks_VI + VeriAIDPO_DPOTasks_EN (4 days)
  Parallel: VeriAIDPO_RiskLevel_VI + VeriAIDPO_RiskLevel_EN (2-4 days)

Week 7:
  Parallel: VeriAIDPO_ComplianceStatus_VI + VeriAIDPO_ComplianceStatus_EN (2 days)
  Parallel: VeriAIDPO_Regional_VI + VeriAIDPO_Regional_EN (2 days)
  Parallel: VeriAIDPO_Industry_VI + VeriAIDPO_Industry_EN (4 days)

Week 8:
  Integration & testing (all 20 models)
```

**Requirements**:
- 2 simultaneous GPU instances (double cost)
- 2 ML engineers working in parallel
- Better resource utilization

**Trade-offs**:
- ✅ Cuts timeline in half (30-34 days vs 57-60 days)
- ✅ Faster time-to-market
- ❌ Doubles GPU costs ($360-600 vs $180-300)
- ❌ Requires 2 ML engineers simultaneously

---

## 💰 Cost Estimation

### **Sequential Bilingual Training (Recommended)**

| Phase | Model Types | Total Models (VI+EN) | Total Samples | Dataset Gen | Training Days | GPU Hours | Cost (@ $2/hr) |
|-------|-------------|---------------------|---------------|-------------|---------------|-----------|----------------|
| Phase 1 (Critical) | 3 types | 6 models | 72,000 (48K VI + 24K EN) | 18-24 hours | 14-20 days | 50-70 hours | $100-140 |
| Phase 2 (Validation) | 4 types | 8 models | 52,800 (32K VI + 20.8K EN) | 15-18 hours | 10-16 days | 35-55 hours | $70-110 |
| Phase 3 (Polish) | 3 types | 6 models | 25,500 (14.1K VI + 11.4K EN) | 8-12 hours | 8-10 days | 25-35 hours | $50-70 |
| **Total** | **10 types** | **20 models** | **150,300 samples** | **41-54 hours** | **32-46 days** | **110-160 hours** | **$220-320** |

**Note**: 
- Each model type requires TWO models (Vietnamese PRIMARY + English SECONDARY)
- Hard dataset generation time included (41-54 hours for 150,300 samples)
- GPU hours increased due to larger datasets and more epochs for hard training

### **Parallel Bilingual Training (If Resources Available)**

| Phase | Model Types | Total Models (VI+EN) | Total Samples | Dataset Gen | Training Days | GPU Hours | Cost (@ $2/hr) |
|-------|-------------|---------------------|---------------|-------------|---------------|-----------|----------------|
| Phase 1 (Critical) | 3 types | 6 models | 72,000 (48K VI + 24K EN) | 18-24 hours | 7-10 days | 100-140 hours | $200-280 |
| Phase 2 (Validation) | 4 types | 8 models | 52,800 (32K VI + 20.8K EN) | 15-18 hours | 5-8 days | 70-110 hours | $140-220 |
| Phase 3 (Polish) | 3 types | 6 models | 25,500 (14.1K VI + 11.4K EN) | 8-12 hours | 4-5 days | 50-70 hours | $100-140 |
| **Total** | **10 types** | **20 models** | **150,300 samples** | **41-54 hours** | **16-23 days** | **220-320 hours** | **$440-640** |

**Note**: Requires 2 simultaneous GPU instances (2x cost but 50% faster)

### **Human Effort (Bilingual Training with Hard Datasets)**

| Role | Hours (Sequential) | Hours (Parallel) | Rate | Cost |
|------|-------------------|------------------|------|------|
| ML Engineer (hard dataset generation - both languages) | 120-160 hours | 120-160 hours | - | Internal |
| ML Engineer (training - both languages) | 50-70 hours | 50-70 hours | - | Internal |
| Vietnamese Linguist (regional/formality validation) | 40-60 hours | 40-60 hours | - | Internal |
| Backend Developer (bilingual API integration) | 50-70 hours | 50-70 hours | - | Internal |
| QA Engineer (bilingual testing with hard cases) | 60-80 hours | 60-80 hours | - | Internal |
| **Total Effort** | **320-440 hours** | **320-440 hours** | - | - |

**Note**: 
- Human effort increased for hard dataset generation (120-160 hours vs 80-120 hours)
- QA effort increased for hard case validation (60-80 hours vs 40-60 hours)
- Hard datasets require more careful review and validation
- Total effort: **320-440 hours** (vs 240-350 hours for easy datasets)

**Hard Dataset Strategy Impact**:
- ✅ **+80-90 hours**: Hard dataset generation with ambiguity
- ✅ **+20-30 hours**: GPU training (more epochs, larger datasets)
- ✅ **Total increase**: ~30% more effort
- ✅ **Benefit**: Production-ready models (78-93% realistic accuracy vs 100% overfitting)

---

## 📊 Success Metrics

### **Model Performance Targets (Per Language)**

**Note**: Targets apply to BOTH Vietnamese (VI - PRIMARY) and English (EN - SECONDARY) models trained with HARD datasets

| Model Type | VI Accuracy | EN Accuracy | VI Samples | EN Samples | Confidence | Inference Speed |
|------------|-------------|-------------|------------|------------|------------|-----------------|
| VeriAIDPO_Principles | 78-88% | 82-90% | 24,000 | 12,000 | 75-85% | <50ms |
| VeriAIDPO_LegalBasis | 82-88% | 85-90% | 10,000 | 6,000 | 78-85% | <50ms |
| VeriAIDPO_BreachTriage | 82-88% | 85-90% | 10,000 | 6,000 | 78-85% | <50ms |
| VeriAIDPO_CrossBorder | 80-87% | 82-90% | 10,000 | 6,000 | 75-85% | <50ms |
| VeriAIDPO_ConsentType | 78-85% | 82-88% | 6,000 | 4,000 | 75-82% | <50ms |
| VeriAIDPO_DataSensitivity | 78-85% | 82-88% | 6,000 | 4,000 | 75-82% | <50ms |
| VeriAIDPO_DPOTasks | 80-87% | 83-90% | 6,000 | 4,000 | 78-85% | <50ms |
| VeriAIDPO_RiskLevel | 75-83% | 80-88% | 8,000 | 4,800 | 72-80% | <50ms |
| VeriAIDPO_ComplianceStatus | 82-88% | 85-92% | 4,800 | 3,200 | 80-87% | <50ms |
| VeriAIDPO_Regional | 85-92% | 88-93% | 4,500 | 3,000 | 83-90% | <50ms |
| VeriAIDPO_Industry | 83-90% | 85-92% | 4,800 | 3,200 | 80-88% | <50ms |

**Total Models**: 20 models (10 model types × 2 languages)
**Total Samples**: Vietnamese: 94,100 | English: 56,200 | **Grand Total: 150,300**

**Why NOT 100% Accuracy?**
- ✅ **Hard datasets with ambiguity** prevent overfitting
- ✅ **Production-ready** for real Vietnamese business documents
- ✅ **Realistic metrics** more credible for investors
- ✅ **Generalizable** to unseen data

### **Business Impact Metrics**

| KPI | Target | Measurement |
|-----|--------|-------------|
| Legal Basis Setup Time | 15 min → 5 min | 66% reduction |
| Breach Triage Time | 2 hours → 15 min | 87% reduction |
| Cross-border Compliance | Manual → Automated | 100% coverage |
| DPO Task Automation | 30% → 70% | 40% improvement |
| Compliance Accuracy | 75% → 90% | 15% improvement |

---

## 🚀 Immediate Next Steps

### **Week 1 Actions (Start Immediately)**

#### **Day 1: Hard Dataset Generator Setup**
```bash
# 1. Create VietnameseHardDatasetGenerator class
# - Based on VeriAIDPO_Hard_Dataset_Generation_Guide.md
# - Implement multi-principle overlap (40% VERY_HARD)
# - Add regional variations (North/Central/South)
# - Add formality levels (Legal/Formal/Business/Casual)

# 2. Create Google Colab notebooks with hard dataset generation
- VeriAIDPO_LegalBasis_Training_VI.ipynb (Vietnamese PRIMARY)
- VeriAIDPO_LegalBasis_Training_EN.ipynb (English SECONDARY)
- VeriAIDPO_BreachTriage_Training_VI.ipynb
- VeriAIDPO_BreachTriage_Training_EN.ipynb
- VeriAIDPO_CrossBorder_Training_VI.ipynb
- VeriAIDPO_CrossBorder_Training_EN.ipynb

# 3. Prepare dataset directories (BILINGUAL)
vietnamese_pdpl_legal_basis_vi/  # Vietnamese PRIMARY
  ├── train.jsonl (8,000 samples - 40% VERY_HARD)
  ├── val.jsonl (1,500 samples)
  └── test.jsonl (500 samples)

vietnamese_pdpl_legal_basis_en/  # English SECONDARY
  ├── train.jsonl (4,800 samples - 35% VERY_HARD)
  ├── val.jsonl (900 samples)
  └── test.jsonl (300 samples)
```

#### **Day 2-4: Hard Dataset Generation - LegalBasis (BILINGUAL)**
```python
# Generate Vietnamese PRIMARY dataset (10,000 samples)
from vietnamese_hard_dataset_generator import VietnameseHardDatasetGenerator

generator = VietnameseHardDatasetGenerator()

# 40% VERY_HARD: Multi-principle overlap, no keywords
# 40% HARD: Semantic understanding required
# 14% MEDIUM: Subtle legal language
# 6% EASY: Clear legal basis

python generate_legal_basis_dataset_vi.py --samples 10000 --difficulty VERY_HARD
# Expected: 18-24 hours generation time for Vietnamese
# Regional variations: North (formal), Central (balanced), South (casual)

# Generate English SECONDARY dataset (6,000 samples)
python generate_legal_basis_dataset_en.py --samples 6000 --difficulty MODERATE_HARD
# Expected: 12-18 hours generation time for English
# 35% VERY_HARD, 40% HARD, 18% MEDIUM, 7% EASY

# Quality validation:
# - Check ambiguity distribution
# - Verify regional balance
# - Validate formality levels
# - Test for keyword memorization (should NOT rely on keywords)
```

#### **Day 5-7: Begin Training - LegalBasis (BILINGUAL)**
```python
# VIETNAMESE PRIMARY (PhoBERT)
# Upload to Google Colab
# Start training VeriAIDPO_LegalBasis_VI
# Monitor accuracy (target: 82-88% - NOT 100%!)
# Confidence: 78-85%
# 8-10 epochs for hard dataset
# Export model after completion

# ENGLISH SECONDARY (BERT)
# Upload to Google Colab
# Start training VeriAIDPO_LegalBasis_EN
# Monitor accuracy (target: 85-90% - realistic)
# Confidence: 82-88%
# 6-8 epochs
# Export model after completion
```

#### **Day 8-10: Hard Dataset Generation - BreachTriage (BILINGUAL)**
While LegalBasis models train in background:
```python
# Vietnamese PRIMARY: 10,000 samples (40% VERY_HARD - borderline severity)
python generate_breach_triage_dataset_vi.py --samples 10000 --difficulty VERY_HARD
# Critical safety task - high ambiguity required

# English SECONDARY: 6,000 samples (35% VERY_HARD)
python generate_breach_triage_dataset_en.py --samples 6000 --difficulty MODERATE_HARD
```

#### **Day 11-14: Hard Dataset Generation - CrossBorder (BILINGUAL)**
```python
# Vietnamese PRIMARY: 10,000 samples (35% VERY_HARD - unclear country adequacy)
python generate_cross_border_dataset_vi.py --samples 10000 --difficulty HARD
# MPS context, Vietnamese cloud providers

# English SECONDARY: 6,000 samples (35% VERY_HARD)
python generate_cross_border_dataset_en.py --samples 6000 --difficulty MODERATE_HARD
```

---

### **Deliverables by Week 3 End (Phase 1 Complete)**

✅ **6 trained models (3 types × 2 languages)**:
- **VeriAIDPO_LegalBasis_VI** (4 classes, 82-88% accuracy, 10,000 samples)
- **VeriAIDPO_LegalBasis_EN** (4 classes, 85-90% accuracy, 6,000 samples)
- **VeriAIDPO_BreachTriage_VI** (4 classes, 82-88% accuracy, 10,000 samples)
- **VeriAIDPO_BreachTriage_EN** (4 classes, 85-90% accuracy, 6,000 samples)
- **VeriAIDPO_CrossBorder_VI** (5 classes, 80-87% accuracy, 10,000 samples)
- **VeriAIDPO_CrossBorder_EN** (5 classes, 82-90% accuracy, 6,000 samples)

✅ **Hard datasets generated**:
- Total: 72,000 samples (48,000 VI + 24,000 EN)
- Vietnamese: 40% VERY_HARD ambiguity
- English: 35% VERY_HARD ambiguity
- Regional variations (VI only): North/Central/South
- Formality levels: 4 for VI, 2 for EN

✅ **Backend API integration (BILINGUAL)**:
```python
# New bilingual endpoints:
POST /api/v1/veriaidpo/classify-legal-basis
  # Auto-detects Vietnamese vs English
  # Routes to VeriAIDPO_LegalBasis_VI or _EN

POST /api/v1/veriaidpo/classify-breach-severity
  # Bilingual breach triage
  
POST /api/v1/veriaidpo/classify-cross-border
  # Vietnamese + English cross-border compliance
```

✅ **Frontend integration (BILINGUAL)**:
```typescript
// New bilingual hooks:
const { isVietnamese } = useCulturalIntelligence();

useVeriAIDPO_LegalBasis(text, isVietnamese ? 'vi' : 'en')
useVeriAIDPO_BreachTriage(incident, language)
useVeriAIDPO_CrossBorder(transfer, language)
```

✅ **Enhanced wizards with hard case handling**:
- Legal Basis Setup: AI-powered recommendations (handles ambiguous cases)
- Incident Response: Automated breach triage (borderline severity detection)
- Cross-Border Transfer: Compliance validation (unclear country adequacy)

✅ **Production-ready quality**:
- ❌ NO 100% overfitting
- ✅ 78-90% realistic accuracy
- ✅ Generalizable to unseen Vietnamese business documents
- ✅ Hard cases validated (multi-principle overlap, no keywords)

---

## 📚 Training Notebook Templates

### **VeriAIDPO_LegalBasis_Training_VI.ipynb Structure (Vietnamese PRIMARY)**

```python
# Step 1: Environment Setup
!pip install transformers datasets torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from vietnamese_hard_dataset_generator import VietnameseHardDatasetGenerator

# Step 2: Configuration
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 10000  # 2,500 per category
SAMPLES_PER_CATEGORY = 2500
MODEL_NAME = "vinai/phobert-base-v2"  # Vietnamese PhoBERT
DATASET_DIFFICULTY = "VERY_HARD"

# Hard Dataset Composition
DATASET_COMPOSITION = {
    'VERY_HARD': 0.40,    # Multi-principle overlap, no keywords
    'HARD': 0.40,         # Semantic understanding required
    'MEDIUM': 0.14,       # Subtle legal language
    'EASY': 0.06,         # Clear legal basis
}

# Regional Variations (Vietnamese-specific)
REGIONAL_VARIATIONS = ['north', 'central', 'south']

# Formality Levels (Vietnamese-specific)
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']

# Step 3: Category Definition
LEGAL_BASIS_CATEGORIES = {
    0: {"en": "Consent", "vi": "Đồng ý"},
    1: {"en": "Contract", "vi": "Hợp đồng"},
    2: {"en": "Legal Obligation", "vi": "Nghĩa vụ pháp lý"},
    3: {"en": "Legitimate Interest", "vi": "Lợi ích hợp pháp"}
}

# Step 4: Hard Dataset Generation
generator = VietnameseHardDatasetGenerator()

hard_samples = []
for category_id in range(NUM_CATEGORIES):
    for i in range(SAMPLES_PER_CATEGORY):
        # Determine difficulty level based on composition
        if i < int(SAMPLES_PER_CATEGORY * 0.40):
            difficulty = 'VERY_HARD'
        elif i < int(SAMPLES_PER_CATEGORY * 0.80):
            difficulty = 'HARD'
        elif i < int(SAMPLES_PER_CATEGORY * 0.94):
            difficulty = 'MEDIUM'
        else:
            difficulty = 'EASY'
        
        # Generate with regional and formality variation
        region = REGIONAL_VARIATIONS[i % 3]
        formality = FORMALITY_LEVELS[i % 4]
        
        sample = generator.generate_hard_sample(
            category_id=category_id,
            ambiguity=difficulty,
            region=region,
            formality=formality
        )
        hard_samples.append(sample)

# Step 5: Data Quality Validation
# - Verify NO keyword memorization possible
# - Check ambiguity distribution (40% VERY_HARD)
# - Validate regional balance
# - Test formality level distribution

# Step 6: Model Training (8-10 epochs for hard dataset)
EPOCHS = 8
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256  # Longer for complex Vietnamese

# Step 7: Evaluation (Target: 82-88% accuracy - NOT 100%!)
# Step 8: Export model
# Step 9: Deployment Package
```

### **VeriAIDPO_LegalBasis_Training_EN.ipynb Structure (English SECONDARY)**

```python
# Step 1: Environment Setup
!pip install transformers datasets torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from english_hard_dataset_generator import EnglishHardDatasetGenerator

# Step 2: Configuration
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 6000  # 1,500 per category
SAMPLES_PER_CATEGORY = 1500
MODEL_NAME = "bert-base-uncased"  # English BERT
DATASET_DIFFICULTY = "MODERATE_HARD"

# Hard Dataset Composition (MODERATE-HARD for English)
DATASET_COMPOSITION = {
    'VERY_HARD': 0.35,    # Multi-principle overlap (less than VI)
    'HARD': 0.40,         # Semantic understanding
    'MEDIUM': 0.18,       # Subtle language
    'EASY': 0.07,         # Clear examples
}

# Formality Levels (English - simplified)
FORMALITY_LEVELS = ['formal', 'business']

# Step 3: Category Definition (Same as Vietnamese)
LEGAL_BASIS_CATEGORIES = {
    0: {"en": "Consent"},
    1: {"en": "Contract"},
    2: {"en": "Legal Obligation"},
    3: {"en": "Legitimate Interest"}
}

# Step 4: Hard Dataset Generation (NO regional variations for English)
generator = EnglishHardDatasetGenerator()

hard_samples = []
for category_id in range(NUM_CATEGORIES):
    for i in range(SAMPLES_PER_CATEGORY):
        # Determine difficulty (35% VERY_HARD vs 40% for Vietnamese)
        if i < int(SAMPLES_PER_CATEGORY * 0.35):
            difficulty = 'VERY_HARD'
        elif i < int(SAMPLES_PER_CATEGORY * 0.75):
            difficulty = 'HARD'
        elif i < int(SAMPLES_PER_CATEGORY * 0.93):
            difficulty = 'MEDIUM'
        else:
            difficulty = 'EASY'
        
        # Formality only (NO regional variations)
        formality = FORMALITY_LEVELS[i % 2]
        
        sample = generator.generate_hard_sample(
            category_id=category_id,
            ambiguity=difficulty,
            formality=formality
        )
        hard_samples.append(sample)

# Step 5: Data Quality Validation
# - Verify NO keyword memorization
# - Check ambiguity distribution (35% VERY_HARD)
# - Test PDPL context understanding (unknown to BERT)

# Step 6: Model Training (6-8 epochs - fewer than Vietnamese)
EPOCHS = 6
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128  # Standard for English

# Step 7: Evaluation (Target: 85-90% accuracy - realistic)
# Step 8: Export model
# Step 9: Deployment Package
```

**See Also**:
- `VeriAIDPO_Hard_Dataset_Generation_Guide.md` - Vietnamese hard dataset strategy
- `VeriAIDPO_Dataset_Size_Strategy.md` - Sample count rationale
- `VeriAIDPO_English_Dataset_Strategy.md` - English MODERATE-HARD approach

---

## 🎯 Success Criteria

### **Phase 1 Success (Week 3 - Extended for Hard Datasets)**
- [ ] 6 models trained (3 types × 2 languages) with 78-90% accuracy (NOT 100%)
- [ ] Hard datasets generated (72,000 samples: 48,000 VI + 24,000 EN)
- [ ] Vietnamese models: 40% VERY_HARD ambiguity validated
- [ ] English models: 35% VERY_HARD ambiguity validated
- [ ] Backend API operational (bilingual routing)
- [ ] Legal Basis Setup wizard AI-enhanced (handles ambiguous cases)
- [ ] Breach notification automation working (borderline severity detection)
- [ ] Cross-border transfer detection active (unclear country adequacy)
- [ ] Production-ready quality (no overfitting, generalizable)

### **Phase 2 Success (Week 5 - Extended for Hard Datasets)**
- [ ] 14 models operational (7 types × 2 languages) with 75-90% accuracy
- [ ] Hard datasets for Phase 2 generated (52,800 samples: 32K VI + 20.8K EN)
- [ ] Consent validation working (handles borderline explicit/implied)
- [ ] Data mapping AI-enhanced (ambiguous personal/sensitive classification)
- [ ] DPO task automation 70%+ (overlapping task detection)
- [ ] Risk assessment with DPIA triggers (borderline risk levels)
- [ ] Regional/formality variations validated

### **Phase 3 Success (Week 7 - Extended for Hard Datasets)**
- [ ] All 20 models in production (10 types × 2 languages)
- [ ] Total hard datasets: 150,300 samples (94,100 VI + 56,200 EN)
- [ ] Complete VeriPortal AI integration (bilingual)
- [ ] Hard case testing passed (multi-principle overlap, no keywords)
- [ ] Documentation complete (includes hard dataset guides)
- [ ] Production deployment ready (realistic accuracy, no overfitting)
- [ ] Vietnamese regional variations validated (North/Central/South)
- [ ] Formality level handling confirmed (4 levels VI, 2 levels EN)

---

## 🔄 Continuous Improvement Plan

### **Post-Launch (Month 2+)**

#### **Data Collection from Production (Hard Cases)**
```python
# Collect real Vietnamese compliance text from:
- Customer queries (especially ambiguous cases)
- DPO task descriptions (overlapping tasks)
- Compliance documents (multi-principle scenarios)
- Regulatory updates (borderline classifications)

# Focus on HARD CASES that models struggled with:
- Low confidence predictions (<75%)
- User corrections (indicates ambiguity)
- Multi-principle overlap scenarios
- Regional/formality edge cases

# Retrain quarterly with real hard data
# Target: 85-93% accuracy (from initial 78-88%)
# Maintain ambiguity in training (don't make it easy!)
```

#### **Model Monitoring (Hard Dataset Validation)**
```python
# Track metrics specific to hard datasets:
- Prediction confidence trends (should stay 75-85%, not 99%)
- User correction rates (target: <12% for hard cases)
- False positive/negative rates (higher acceptable for ambiguous cases)
- Edge case discovery (continuous hard case mining)
- Ambiguity handling effectiveness

# Automated retraining triggers:
- Accuracy drops below 75% (realistic for hard datasets)
- Confidence drops below 70% (indicates confusion)
- High user correction rate (>15% sustained)
- New PDPL guidance introduces new ambiguities

# Quality checks:
- Ensure models DON'T achieve 100% (indicates overfitting)
- Verify hard case distribution maintained (40% VERY_HARD)
- Validate regional variation handling
```

#### **Regulatory Updates (Hard Dataset Evolution)**
```python
# Monitor PDPL changes:
- MPS guidance updates (new ambiguous scenarios)
- New adequacy decisions (cross-border edge cases)
- Article amendments (legal basis evolution)
- Court rulings (real-world ambiguity resolution)

# Update hard datasets with new ambiguities:
- Add new VERY_HARD scenarios from MPS guidance
- Incorporate court ruling edge cases
- Update regional variations based on enforcement patterns
- Maintain 40% VERY_HARD composition
- Industry-specific rules

# Update training data quarterly
# Retrain affected models
```

---

## 📞 Support & Resources

### **Training Support**
- **Technical Issues**: GitHub Issues
- **Dataset Questions**: [Your email]
- **Model Performance**: ML team Slack channel

### **Documentation**
- Training notebooks: `docs/VeriSystems/training_notebooks/`
- Dataset generation: `docs/VeriSystems/dataset_generation/`
- API integration: `docs/Implementation_Prototype_Plans/VeriAIDPO_Integration.md`
- **Hard Dataset Strategy**: `docs/VeriSystems/VeriAIDPO_Hard_Dataset_Generation_Guide.md`
- **Sample Count Strategy**: `docs/VeriSystems/VeriAIDPO_Dataset_Size_Strategy.md`
- **English Dataset Strategy**: `docs/VeriSystems/VeriAIDPO_English_Dataset_Strategy.md`

### **External Resources**
- PhoBERT documentation: https://github.com/VinAIResearch/PhoBERT
- BERT documentation: https://huggingface.co/bert-base-uncased
- Transformers library: https://huggingface.co/docs/transformers
- PDPL 2025 text: [Vietnamese government portal]

---

## 📝 Implementation Plan Summary

### **Hard Dataset Strategy Overview**

This implementation plan reflects **production-ready hard dataset training** with ambiguity, preventing overfitting and ensuring real-world Vietnamese business document handling.

**CRITICAL UPDATE**: VeriAIDPO_Principles requires **retraining** from MVP (4,488 samples) to Production (24,000 samples)

**Key Changes from Original Plan**:

| Aspect | Original (Easy) | Updated (Hard) | Impact |
|--------|----------------|----------------|--------|
| **VeriAIDPO_Principles** | 4,488 MVP samples | **24,000 Production** | 🔄 **RETRAIN REQUIRED** |
| **Sample Count** | 500/category uniform | Variable (1,200-3,000/category) | +200-500% per model |
| **Ambiguity Level** | 0% (keyword-based) | 25-40% VERY_HARD | Production-ready |
| **Total Samples** | ~20,000 | **150,300** (94,100 VI + 56,200 EN) | +650% total |
| **Total Models** | 20 new models | **1 retrain + 20 new = 21 models** | Principles upgrade |
| **Expected Accuracy** | 100% (overfitting) | 75-93% (realistic) | Generalizable |
| **Vietnamese Priority** | Equal | 67% more samples than EN | Cultural focus |
| **Regional Variations** | None | 3 (North/Central/South) | Vietnamese-specific |
| **Formality Levels** | None | 4 for VI, 2 for EN | Business context |
| **Generation Time** | 10-15 hours | 41-54 hours | +300% effort |
| **Training Epochs** | 5-6 | 6-10 (harder to learn) | +30% GPU time |
| **Total Cost** | $180-280 | **$260-380** (with Principles retrain) | Principles: +$40-60 |
| **Human Effort** | 240-350 hours | **325-450 hours** | Principles: +5-10h |
| **Timeline** | 34-48 days | **38-52 days** (includes Phase 0) | Principles: +4-6 days |

**Vietnamese Hard Dataset Composition (PRIMARY - 94,100 samples)**:
- 40% VERY_HARD: Multi-principle overlap, unclear legal basis, borderline severity
- 40% HARD: No keywords, semantic understanding required
- 14-15% MEDIUM: Subtle language hints, formality variations
- 5-6% EASY: Clear examples for baseline

**English Hard Dataset Composition (SECONDARY - 56,200 samples)**:
- 30-35% VERY_HARD: Multi-principle overlap (less than Vietnamese)
- 40% HARD: No keywords, PDPL context understanding
- 18-20% MEDIUM: Subtle language hints
- 7-10% EASY: Clear examples

**Why Hard Datasets Matter**:
1. ✅ **No Overfitting**: 78-93% accuracy (not 100%) proves generalization
2. ✅ **Production-Ready**: Handles real Vietnamese business documents
3. ✅ **Investor Credibility**: Realistic metrics more trustworthy
4. ✅ **Vietnamese Cultural Context**: Regional and formality variations
5. ✅ **Long-term Value**: Models don't break on edge cases

**Total Investment**:
- **Datasets**: 150,300 hard samples (41-54 hours generation)
- **Models**: 20 bilingual models (10 types × 2 languages)
- **Timeline**: 7 weeks (vs 5 weeks for easy datasets)
- **Cost**: $220-320 sequential, $440-640 parallel
- **Human Effort**: 320-440 hours (vs 240-350 for easy)
- **Benefit**: Production-grade AI that handles Vietnamese compliance ambiguity

**Supporting Documentation**:
- 📄 `VeriAIDPO_Hard_Dataset_Generation_Guide.md` - Vietnamese VERY HARD strategy (663 lines)
- 📄 `VeriAIDPO_Dataset_Size_Strategy.md` - Variable sample count rationale (700 lines)
- 📄 `VeriAIDPO_English_Dataset_Strategy.md` - English MODERATE-HARD approach (663 lines)
- 📄 `VeriAIDPO_Dynamic_Company_Registry_Implementation.md` - Zero-retraining scalability (2,500 lines)

**Dynamic Company Registry Integration**:
All `{company}` template placeholders throughout this document now use the **Dynamic Company Registry** approach:
- **Generation**: Real Vietnamese companies (150+) selected by industry context
- **Training**: Normalized to `[COMPANY]` token for company-agnostic models
- **Inference**: Works with ANY company (trained or unseen)
- **Scalability**: Add unlimited companies via JSON config (zero retraining)
- **Cost Savings**: $440-640 + 14 weeks saved for just 3 company additions

**Implementation Timeline Update**:
- **Week 1**: Add CompanyRegistry and normalization to dataset generators
- **Weeks 2-7**: Continue as planned with company-agnostic training

**Next Steps**: Start with **Phase 0: VeriAIDPO_Principles retraining** (Day 1-6), then proceed to Phase 1 critical models (LegalBasis, BreachTriage, CrossBorder) with bilingual training.

---

---

## 🎉 Conclusion

This implementation plan provides a **comprehensive roadmap** to upgrade VeriAIDPO_Principles to production-grade AND add 10 additional specialized classifiers for **full DPO operational support**.

**Key Takeaways**:
- 🔄 **Phase 0 CRITICAL**: Retrain VeriAIDPO_Principles (4,488 → 24,000 samples) for enterprise readiness
- ✅ **Phased approach** allows for incremental value delivery
- ✅ **Critical models first** ensures high-impact features launch early
- ✅ **38-52 days total** (includes Principles retraining) is achievable with focused effort
- ✅ **$260-380 cost** is minimal investment for production-grade AI (21 models)
- ✅ **Hard datasets** ensure models handle real Vietnamese business documents (78-88% realistic accuracy)
- ✅ **Multi-task option** available for faster completion at slightly higher cost

**Next Immediate Action**: Begin **Phase 0: VeriAIDPO_Principles v2.0 dataset generation** (24,000 samples) to upgrade MVP model for enterprise deployment.

**Why Start with Principles Retraining**:
- ✅ Core model used across all VeriPortal features
- ✅ Enterprise customers need production accuracy (not MVP demo accuracy)
- ✅ Blocks enterprise sales until upgraded
- ✅ Only 4-6 days investment, $40-60 cost
- ✅ Demonstrates production readiness to investors

---

**Document Owner**: VeriSyntra ML Team  
**Last Updated**: October 14, 2025  
**Version**: 2.0 (Dynamic Company Registry Integration + Principles Retraining Plan)  
**Status**: 📋 Ready for Implementation  
**Changes**: 
- Added Phase 0 for VeriAIDPO_Principles retraining (4,488 → 24,000 samples)
- Updated timeline (38-52 days), cost ($260-380), total models (21)
- Added Dynamic Company Registry reference and Week 1 setup task

