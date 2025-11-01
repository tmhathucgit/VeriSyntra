# VeriAIDPO Phase 0 - Principles Model Retraining
## Production Upgrade: v1.0 MVP → v2.0 Production

**Priority**: 🚨 **CRITICAL - Must complete before enterprise deployment**  
**Status**: 🔄 Vietnamese v2.0 Notebook Created - Ready for Training  
**Timeline**: 4-6 days (VI 2-3 days + EN 2-3 days)  
**Cost**: $40-60 (Google Colab Pro+ GPU hours)

---

## 📊 Current State vs Production Requirements

### **VeriAIDPO_Principles - Overview**

**Current State (v1.0 MVP)**:
- **Version**: v1.0_MVP (trained October 6, 2025)
- **Samples**: 4,488 (EASY synthetic data)
- **Accuracy**: 90-93% on simple keyword-based examples
- **Purpose**: Investor demo, proof of concept ✅
- **Limitation**: Won't handle production Vietnamese compliance documents
- **Status**: Deployed for demos only

**Production Requirements (v2.0)**:
- **Version**: v2.0_Production
- **Samples**: 24,000 Vietnamese + 12,000 English = **36,000 total**
- **Difficulty**: 40% VERY_HARD + 40% HARD (production-grade ambiguity)
- **Target Accuracy**: 78-88% VI, 82-90% EN (realistic for complex docs)
- **Purpose**: Enterprise customers (banks, telecom, government contractors)
- **Status**: Vietnamese notebook created, ready for training

---

## 🎯 Why Retraining is Critical

### Performance Comparison: MVP vs Production

| Scenario | MVP Model (4,488 samples) | Production Model (24,000 samples) |
|----------|-------------------------|----------------------------------|
| **Simple example**<br>"Khách hàng đồng ý nhận email marketing" | ✅ **Correct** (Consent)<br>Easy keyword detection | ✅ **Correct** (Consent)<br>Semantic understanding |
| **Real bank policy**<br>"Căn cứ hợp đồng mở tài khoản, ngân hàng thu thập CMND để xác thực danh tính theo quy định Ngân hàng Nhà nước" | ❌ **Likely wrong**<br>Sees "thu thập" → guesses Data Minimization | ✅ **Correct** (Legal Obligation)<br>Understands legal requirement context |
| **Startup privacy policy**<br>"Chúng mình chỉ lấy thông tin cần thiết để giao hàng thôi nha! 📦" | ❌ **Likely wrong**<br>Casual style not in training | ✅ **Correct** (Purpose Limitation)<br>Handles all 4 formality levels |
| **Multi-principle overlap**<br>"Công ty chỉ sử dụng dữ liệu cho mục đích đã thông báo và đảm bảo bảo mật tuyệt đối" | ❌ **Confused**<br>Can't handle 2 principles | ✅ **Correct** (Purpose Limitation)<br>Identifies PRIMARY principle |

**Conclusion**: MVP works for investor demos, but **enterprise customers need production model** to handle real-world Vietnamese compliance documents.

---

## 📋 Training Plan

### **Vietnamese Model (PRIMARY) - VeriAIDPO_Principles_VI v2.0**

**Dataset Specifications**:
- **Total Samples**: 24,000 (8 categories × 3,000 samples each)
- **Difficulty Breakdown**:
  - **VERY_HARD**: 9,600 samples (40%)
    - Multi-principle overlap (no clear winner)
    - Zero keywords (pure semantic understanding)
    - Ambiguous phrasing
  - **HARD**: 9,600 samples (40%)
    - Regional variations (North/Central/South)
    - Semantic-only classification
    - Formality mixing
  - **MEDIUM**: 3,600 samples (15%)
    - Subtle keywords
    - Context-dependent meaning
  - **EASY**: 1,200 samples (5%)
    - Clear examples with keywords

**Regional Distribution**:
- **North (Hà Nội)**: 8,000 samples (33.3%)
  - Formal, hierarchical language
  - Government/legal terminology
- **Central (Đà Nẵng/Huế)**: 8,000 samples (33.3%)
  - Balanced formal/casual
  - Traditional business contexts
- **South (TP.HCM)**: 8,000 samples (33.3%)
  - Entrepreneurial, casual language
  - International business exposure

**Formality Levels**:
- **Legal**: 6,000 samples (25%) - PDPL article citations, legal terminology
- **Formal**: 6,000 samples (25%) - Business correspondence, official policies
- **Business**: 6,000 samples (25%) - Internal communications, standard docs
- **Casual**: 6,000 samples (25%) - Startup policies, customer-facing text

**Training Configuration**:
```python
MODEL_NAME = "vinai/phobert-base-v2"
NUM_CATEGORIES = 8
TOTAL_SAMPLES = 24000
DATASET_DIFFICULTY = "HARD"  # 40% VERY_HARD + 40% HARD
EPOCHS = 8-10
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

**Training Time**: 2-3 days  
**Cost**: $20-30 (Google Colab Pro+ GPU hours)

---

### **English Model (SECONDARY) - VeriAIDPO_Principles_EN v2.0**

**Dataset Specifications**:
- **Total Samples**: 12,000 (8 categories × 1,500 samples each)
- **Difficulty Breakdown**:
  - **VERY_HARD**: 3,600-4,200 samples (30-35%)
    - Multi-principle overlap
    - No keywords
  - **HARD**: 4,800 samples (40%)
    - Semantic-only classification
    - Context-dependent
  - **MEDIUM**: 2,160-2,400 samples (18-20%)
    - Subtle keywords
  - **EASY**: 840-1,200 samples (7-10%)
    - Clear examples

**Formality Levels**:
- **Formal**: 6,000 samples (50%) - Legal documents, official policies
- **Business**: 6,000 samples (50%) - Standard business communications

**Training Configuration**:
```python
MODEL_NAME = "bert-base-uncased"
NUM_CATEGORIES = 8
TOTAL_SAMPLES = 12000
DATASET_DIFFICULTY = "MODERATE-HARD"  # 30-35% VERY_HARD + 40% HARD
EPOCHS = 6-8
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
FORMALITY_LEVELS = ['formal', 'business']
```

**Training Time**: 2-3 days  
**Cost**: $20-30 (Google Colab Pro+ GPU hours)

---

## ✅ Vietnamese v2.0 Notebook - Created and Ready

### **Notebook Details**

**File**: `docs/VeriSystems/VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`  
**Created**: October 18, 2025  
**Status**: ✅ Ready for upload to Google Colab Pro+  
**Total Cells**: 22 (11 Markdown + 11 Python)  
**Lines**: 1,402

### **Key Features Implemented**

#### ✅ **Production Backend Integration**
- **Uses**: `backend/app/core/company_registry.py` (NOT recreated inline)
- **Uses**: `backend/app/core/pdpl_normalizer.py` (NOT recreated inline)
- **Data Source**: `backend/config/company_registry.json` (46+ companies)
- **Benefit**: Training-production parity guaranteed

#### ✅ **Dynamic Company Registry**
- Zero hardcoded company names
- Imports from production backend
- Hot-reload capability (add companies without retraining)
- Company-agnostic training ([COMPANY] token)

#### ✅ **Hard Dataset Generation**
- 24,000 samples with controlled ambiguity
- 40% VERY_HARD + 40% HARD + 15% MEDIUM + 5% EASY
- Regional variations (North/Central/South)
- 4 formality levels (Legal/Formal/Business/Casual)

#### ✅ **5-Layer Data Leak Detection**
- **Layer 1**: Template diversity (>70% unique templates)
- **Layer 2**: Normalized sample uniqueness (>95%)
- **Layer 3**: Company distribution balance (min/max ratio >30%)
- **Layer 4**: Category distribution balance (<10% deviation)
- **Layer 5**: Train/Val/Test split overlap detection

#### ✅ **Company-Agnostic Testing**
- Tests with NEW companies not seen in training
- Validates [COMPANY] token generalization
- Ensures model doesn't memorize specific company names

#### ✅ **Model Export with Metadata**
- Saves trained model
- Exports company registry version used
- Documents training date, samples, accuracy
- Ready for production deployment

### **Notebook Structure (22 Cells)**

1. **Title and Overview** (Markdown)
   - Includes backend integration architecture explanation
   
2. **Environment Setup** (Python)
   - Package installation (transformers, datasets, torch, etc.)
   - NO EMOJI characters (Colab-safe)

3. **Backend Files Upload Instructions** (Markdown)
   - 3 methods: Google Drive, Direct Upload, GitHub Clone
   - Upload `company_registry.py`, `pdpl_normalizer.py`, `company_registry.json`

4. **Load Production CompanyRegistry** (Python)
   - Import from `app.core.company_registry`
   - Verify 46+ companies loaded

5. **Load Production Normalizer** (Python)
   - Import from `app.core.pdpl_normalizer`
   - Test normalization

6. **Dataset Generator** (Python, 214 lines)
   - Hard template generation
   - Regional variations
   - Formality levels
   - Company selection from registry
   - Data leak prevention

7. **Generate 24,000 Samples** (Python, 125 lines)
   - 8 categories × 3,000 samples
   - Difficulty distribution (40% VERY_HARD)
   - Company distribution tracking

8. **Data Leak Detection** (Python, 138 lines)
   - 5-layer validation
   - Alerts if thresholds not met

9. **Dataset Preparation** (Python)
   - Train/Val/Test split (80/10/10)
   - Leak detection between splits

10. **PhoBERT Training** (Python, 158 lines)
    - Model: vinai/phobert-base-v2
    - 8-10 epochs, batch size 16
    - Learning rate 2e-5

11. **Company-Agnostic Testing** (Python)
    - Test with NEW companies
    - Validate generalization

12. **Model Export** (Python)
    - Save model checkpoint
    - Export metadata

13. **Completion Summary** (Markdown)
    - Deployment checklist

### **Production Backend Files Required**

Upload these 3 files to Google Colab:

1. **`backend/app/core/company_registry.py`** (513 lines)
   - CompanyRegistry class
   - Methods: `get_registry()`, `get_statistics()`, `search_companies()`

2. **`backend/app/core/pdpl_normalizer.py`** (~300 lines)
   - PDPLTextNormalizer class
   - Method: `normalize_text()` → NormalizationResult

3. **`backend/config/company_registry.json`**
   - 46+ Vietnamese companies
   - Industries: Technology, Finance, Manufacturing, etc.
   - Regions: North, Central, South

**See Setup Guide**: `VeriAIDPO_Colab_Setup_Guide.md`

---

## 🚀 Next Steps

### **Immediate Actions (Vietnamese v2.0)**

1. **Upload Notebook to Colab Pro+**
   - Open Google Colab Pro+
   - Upload `VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`
   - Verify runtime type (GPU: T4 or A100)

2. **Upload Backend Files**
   - Follow `VeriAIDPO_Colab_Setup_Guide.md`
   - Upload 3 files to Colab
   - Run verification checks (5 steps)

3. **Execute Training**
   - Run all cells sequentially
   - Monitor training progress (2-3 days)
   - Save checkpoints

4. **Download Trained Model**
   - Download model checkpoint
   - Download training metadata
   - Download test results

5. **Deploy to Production**
   - Test in VeriSyntra backend
   - A/B test with v1.0 MVP
   - Route enterprise customers to v2.0

### **English v2.0 Notebook** (Next)

1. **Create English Notebook**
   - Adapt Vietnamese notebook structure
   - 12,000 samples (vs 24,000 VI)
   - 2 formality levels (vs 4 VI)
   - Base model: bert-base-uncased

2. **Execute Training**
   - Upload to Colab Pro+
   - Train 2-3 days
   - Download model

3. **Deploy Bilingual Support**
   - Vietnamese v2.0 (PRIMARY)
   - English v2.0 (SECONDARY)
   - Language detection → route to correct model

---

## 📊 Success Criteria

### **Vietnamese Model (VeriAIDPO_Principles_VI v2.0)**

**Performance Targets**:
- ✅ **Accuracy**: 78-88% on test set (production-grade)
- ✅ **Confidence**: 75-85% average
- ✅ **Inference Speed**: <50ms per classification
- ✅ **Dataset Quality**: Pass all 5 data leak detection layers

**Functional Requirements**:
- ✅ Handles multi-principle overlap (identifies primary)
- ✅ Works with all 3 Vietnamese regions (North, Central, South)
- ✅ Handles all 4 formality levels (Legal, Formal, Business, Casual)
- ✅ Company-agnostic (works with NEW companies via [COMPANY] token)
- ✅ Regional variation support (Bắc, Trung, Nam contexts)

**Production Readiness**:
- ✅ Backend integration verified (uses production modules)
- ✅ Hot-reload compatible (company registry updates)
- ✅ Zero training-production drift risk
- ✅ Deployment-ready format

### **English Model (VeriAIDPO_Principles_EN v2.0)**

**Performance Targets**:
- ✅ **Accuracy**: 82-90% on test set
- ✅ **Confidence**: 80-88% average
- ✅ **Inference Speed**: <50ms per classification
- ✅ **Dataset Quality**: Pass all 5 data leak detection layers

**Functional Requirements**:
- ✅ Handles multi-principle overlap
- ✅ Works with 2 formality levels (Formal, Business)
- ✅ Company-agnostic training
- ✅ Semantic understanding (no keyword reliance)

---

## 💻 Dataset Generation Scripts

### Vietnamese Dataset

```bash
# Generate hard dataset for Vietnamese v2.0
python scripts/generate_hard_dataset.py \
    --model-type VeriAIDPO_Principles \
    --language vi \
    --total-samples 24000 \
    --very-hard-ratio 0.40 \
    --hard-ratio 0.40 \
    --medium-ratio 0.15 \
    --easy-ratio 0.05 \
    --use-company-registry \
    --regional-variations north,central,south \
    --formality-levels legal,formal,business,casual \
    --output datasets/principles_vi_v2_hard.jsonl
```

### English Dataset

```bash
# Generate moderate-hard dataset for English v2.0
python scripts/generate_hard_dataset.py \
    --model-type VeriAIDPO_Principles \
    --language en \
    --total-samples 12000 \
    --very-hard-ratio 0.33 \
    --hard-ratio 0.40 \
    --medium-ratio 0.18 \
    --easy-ratio 0.09 \
    --use-company-registry \
    --formality-levels formal,business \
    --output datasets/principles_en_v2_hard.jsonl
```

---

## 🔄 Deployment Strategy

### Zero-Downtime Migration

```python
class PrinciplesClassifier:
    """Dual-model deployment with customer tier routing"""
    
    def __init__(self):
        self.mvp_model = load_model("VeriAIDPO_Principles_VI_v1.0")
        self.prod_model = load_model("VeriAIDPO_Principles_VI_v2.0")
    
    def classify(self, text: str, customer_tier: str = "enterprise"):
        """
        Route based on customer type:
        - demo: v1.0 MVP (investor demos)
        - enterprise: v2.0 Production (paying customers)
        """
        if customer_tier == "demo":
            return self.mvp_model.predict(text)
        else:
            return self.prod_model.predict(text)
```

### A/B Testing Strategy

**Phase 1: Shadow Mode** (Week 1)
- v2.0 runs alongside v1.0
- v2.0 results logged but not returned
- Compare predictions
- Measure accuracy difference

**Phase 2: Gradual Rollout** (Week 2-3)
- 10% enterprise customers → v2.0
- 90% enterprise customers → v1.0
- Monitor performance metrics
- Collect feedback

**Phase 3: Full Production** (Week 4+)
- 100% enterprise customers → v2.0
- Demos continue using v1.0
- Deprecate v1.0 after 30 days

---

## 📋 Checklist

### Before Training
- [ ] Vietnamese notebook uploaded to Colab Pro+
- [ ] 3 backend files uploaded and verified
- [ ] GPU runtime selected (T4 or A100)
- [ ] All 5 verification checks passed
- [ ] Google Drive mounted (if using Drive method)

### During Training
- [ ] Monitor training progress (2-3 days)
- [ ] Check for errors or warnings
- [ ] Verify data leak detection passes
- [ ] Review intermediate metrics
- [ ] Save checkpoints regularly

### After Training
- [ ] Download trained model checkpoint
- [ ] Download training metadata
- [ ] Review test results (78-88% accuracy target)
- [ ] Test company-agnostic functionality
- [ ] Verify backend integration

### Deployment
- [ ] Test in VeriSyntra backend locally
- [ ] Verify production backend integration
- [ ] Run shadow mode (1 week)
- [ ] Gradual rollout (10% → 50% → 100%)
- [ ] Full production deployment
- [ ] Deprecate v1.0 MVP

---

## 📚 Related Documentation

- **Architecture Requirements**: `VeriAIDPO_Architecture_Requirements.md` (backend integration)
- **Colab Setup Guide**: `VeriAIDPO_Colab_Setup_Guide.md` (file upload instructions)
- **Implementation Overview**: `VeriAIDPO_Implementation_Overview.md` (big picture)
- **Created Notebook**: `VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`
- **Notebook Report**: `VeriAIDPO_Principles_VI_v2_Notebook_Creation_Report.md`

---

**Last Updated**: October 18, 2025  
**Status**: ✅ Vietnamese notebook ready for training  
**Next**: Upload to Colab Pro+ and execute 2-3 day training run
