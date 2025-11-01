# VeriAIDPO_Principles - PDPL Principles Classification (v2.0 Production)

**Phase**: 🚨 Phase 0 - CRITICAL PREREQUISITE  
**Priority**: 🚨 **MUST COMPLETE FIRST** - Required before all operational models  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2-3 days
- English (EN - SECONDARY): 2-3 days
- **Total**: 4-6 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_Principles_VI` v2.0 (PhoBERT, Vietnamese primary)
- `VeriAIDPO_Principles_EN` v2.0 (BERT, English secondary)

**Current Status**:
- ✅ Vietnamese v2.0 notebook created (`VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`)
- 📋 English v2.0 notebook pending
- 🔄 Ready for Google Colab Pro+ training

**Use Cases**: Core principle identification for all VeriPortal compliance modules

---

## 📊 Current State vs Production Requirements

### VeriAIDPO_Principles v1.0 MVP (Current)
- **Version**: v1.0_MVP (trained October 6, 2025)
- **Samples**: 4,488 (EASY synthetic data only)
- **Accuracy**: 90-93% on simple keyword-based examples
- **Dataset Difficulty**: 100% EASY (keyword detection)
- **Purpose**: ✅ Investor demo, proof of concept
- **Limitation**: ❌ Won't handle production Vietnamese compliance documents
- **Status**: Deployed for demos only

### VeriAIDPO_Principles v2.0 Production (Target)
- **Version**: v2.0_Production
- **Samples**: 24,000 Vietnamese + 12,000 English = **36,000 total**
- **Dataset Difficulty**: 40% VERY_HARD + 40% HARD (production-grade ambiguity)
- **Target Accuracy**: 78-88% VI, 82-90% EN (realistic for complex documents)
- **Purpose**: ✅ Enterprise customers (banks, telecom, government contractors)
- **Status**: Vietnamese notebook created, ready for training

---

## Categories (8 classes - Same as v1.0)

```python
PDPL_PRINCIPLES = {
    0: {
        "en": "Lawfulness",
        "vi": "Tính hợp pháp",
        "pdpl_article": "Article 7.1.a",
        "description_vi": "Xử lý dữ liệu phải có cơ sở pháp lý hợp lệ"
    },
    1: {
        "en": "Purpose Limitation",
        "vi": "Giới hạn mục đích",
        "pdpl_article": "Article 7.1.c",
        "description_vi": "Chỉ xử lý dữ liệu cho mục đích đã thông báo"
    },
    2: {
        "en": "Data Minimization",
        "vi": "Giảm thiểu dữ liệu",
        "pdpl_article": "Article 7.1.d",
        "description_vi": "Chỉ thu thập dữ liệu cần thiết cho mục đích"
    },
    3: {
        "en": "Accuracy",
        "vi": "Chính xác",
        "pdpl_article": "Article 7.1.e",
        "description_vi": "Dữ liệu phải chính xác và cập nhật"
    },
    4: {
        "en": "Storage Limitation",
        "vi": "Giới hạn lưu trữ",
        "pdpl_article": "Article 7.1.f",
        "description_vi": "Chỉ lưu trữ dữ liệu trong thời gian cần thiết"
    },
    5: {
        "en": "Security",
        "vi": "An toàn bảo mật",
        "pdpl_article": "Article 7.1.g",
        "description_vi": "Bảo vệ dữ liệu khỏi truy cập trái phép"
    },
    6: {
        "en": "Transparency",
        "vi": "Minh bạch",
        "pdpl_article": "Article 7.1.b",
        "description_vi": "Thông báo rõ ràng về xử lý dữ liệu"
    },
    7: {
        "en": "Consent",
        "vi": "Đồng ý",
        "pdpl_article": "Article 12",
        "description_vi": "Có đồng ý hợp lệ của chủ thể dữ liệu"
    }
}
```

---

## 🎯 Why Retraining is Critical

### Performance Comparison: v1.0 MVP vs v2.0 Production

| Scenario | v1.0 MVP (4,488 EASY samples) | v2.0 Production (24,000 HARD samples) |
|----------|------------------------------|--------------------------------------|
| **Simple example**<br>"Khách hàng đồng ý nhận email marketing" | ✅ **Correct** (Consent)<br>Easy keyword detection | ✅ **Correct** (Consent)<br>Deep semantic understanding |
| **Real bank policy**<br>"Căn cứ hợp đồng mở tài khoản, ngân hàng thu thập CMND để xác thực danh tính theo quy định Ngân hàng Nhà nước" | ❌ **Likely wrong**<br>Sees "thu thập" → guesses Data Minimization | ✅ **Correct** (Lawfulness)<br>Understands legal requirement context |
| **Startup privacy policy (casual)**<br>"Chúng mình chỉ lấy thông tin cần thiết để giao hàng thôi nha! 📦" | ❌ **Likely wrong**<br>Casual style not in training data | ✅ **Correct** (Purpose Limitation)<br>Handles all 4 formality levels |
| **Multi-principle overlap**<br>"Công ty chỉ sử dụng dữ liệu cho mục đích đã thông báo và đảm bảo bảo mật tuyệt đối" | ❌ **Confused**<br>Can't prioritize when 2+ principles present | ✅ **Correct** (Purpose Limitation)<br>Identifies PRIMARY principle correctly |

**Conclusion**: v1.0 works for investor demos with simple examples, but **enterprise customers need v2.0** to handle real-world Vietnamese compliance documents with ambiguity, regional variations, and multiple formality levels.

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_Principles_VI v2.0

- **Total Samples**: 24,000 (3,000 per category × 8)
- **Difficulty**: VERY HARD (enterprise-grade ambiguity)
- **Dataset Composition**:
  - **VERY_HARD**: 1,200/category (40%) - Multi-principle overlap, no keywords
  - **HARD**: 1,200/category (40%) - Subtle principle indicators, contextual only
  - **MEDIUM**: 450/category (15%) - Implicit principle references
  - **EASY**: 150/category (5%) - Clear principle examples (for baseline)
  
- **Regional Variations**: 
  - North (Hanoi): 33% - Formal governmental tone (synthetically applied from legal base)
  - Central (Da Nang/Hue): 33% - Traditional business formality (synthetically applied from legal base)
  - South (HCMC): 34% - Modern tech/startup phrasing (synthetically applied from legal base)
  - **Note**: Source legal text is national standard; regional flavor applied via post-processing
  
- **Formality Levels**:
  - Legal (formal contracts): 30% - Direct extraction from PDPL/Decree 13
  - Formal (corporate policies): 30% - Legal text rephrased with business vocabulary
  - Business (professional emails): 25% - Legal concepts simplified for corporate use
  - Casual (startup communications): 15% - Conversationalized legal concepts (GPT-4 assisted + human review)
  - **Transformation Pipeline**: Legal (100% source) → Formal (rephrase) → Business (simplify) → Casual (conversationalize)
  
- **Sources**:
  - **Primary Legal Corpus**: PDPL Law 91/2025/QH15 (352 lines), Decree 13/2023/NĐ-CP (461 lines)
  - **Template Libraries**: CompanyRegistry (46 Vietnamese companies), BUSINESS_CONTEXTS (108 industry-specific phrases)
  - **Distinctive Markers**: CAT2_DISTINCTIVE_PHRASES (54 quantity/comparative markers), CAT6_DISTINCTIVE_PHRASES (52 conditional/reasoning markers)
  - **Generation Method**: Pattern extraction from 813-line legal corpus → Template expansion → Synthetic formality/regional variations

### English (SECONDARY) - VeriAIDPO_Principles_EN v2.0

- **Total Samples**: 12,000 (1,500 per category × 8)
- **Difficulty**: MODERATE-HARD (controlled ambiguity)
- **Dataset Composition**:
  - **VERY_HARD**: 450/category (30%) - Multi-principle overlap
  - **HARD**: 600/category (40%) - Contextual principle identification
  - **MEDIUM**: 300/category (20%) - Subtle indicators
  - **EASY**: 150/category (10%) - Clear examples (for baseline)
  
- **Formality Levels**:
  - Formal (legal documents): 50%
  - Business (corporate policies): 50%
  
- **Sources**:
  - GDPR compliance documents
  - International privacy policies
  - Data protection best practices
  - Standard contractual clauses

---

## Template Examples

```python
# VERY_HARD (Multi-principle overlap, no keywords)
  - Standard contractual clauses

---

## Data Augmentation Strategy (Limited Source Text)

### Challenge: 28x Expansion from Legal Corpus

**Source Data**: 813 lines of premium Vietnamese legal text (PDPL Law 352 lines + Decree 13 461 lines)  
**Target Dataset**: 24,000 Vietnamese samples (3,000 per category × 8 principles)  
**Expansion Factor**: 28x (813 → 24,000)

### Multi-Layer Augmentation Approach

#### 1. Pattern Extraction (from 813-line legal corpus)
```python
# Extract principle manifestations from legal articles
Source: "Điều 9. Bên kiểm soát dữ liệu cá nhân phải có sự đồng ý của chủ thể"
Pattern Identified: Consent principle (Principle #8)
Legal Terminology: "đồng ý", "chủ thể dữ liệu", "bên kiểm soát"

# Map legal concepts to each principle
Principle 1 (Lawfulness): Điều 3 (quy định pháp luật, hợp pháp, minh bạch)
Principle 2 (Purpose Limitation): Điều 3.2 (mục đích cụ thể, phạm vi)
Principle 3 (Data Minimization): Điều 3.2 (cần thiết, tối thiểu)
... (8 principles total)
```

#### 2. Template Generation (using backend modules)
```python
# Apply extracted patterns to Vietnamese business contexts

CompanyRegistry (46 companies):
- Technology: Viettel, FPT, VNG, Base.vn
- Banking: Techcombank, VPBank, VCB, ACB
- E-commerce: Shopee, Tiki, Lazada, Sendo
- Manufacturing: Vingroup, Hoa Phat, TH True Milk
... (46 total across 9 industries)

BUSINESS_CONTEXTS (108 industry-specific phrases):
- Technology: "ứng dụng di động", "dịch vụ đám mây", "API integration"
- Banking: "giao dịch ngân hàng", "thẻ tín dụng", "chuyển khoản"
- Healthcare: "hồ sơ bệnh án", "khám chữa bệnh", "dữ liệu sức khỏe"
... (108 total)

CAT2_DISTINCTIVE_PHRASES (54 quantity/comparative markers):
- Quantity: "chỉ", "chỉ cần", "tối thiểu", "không quá"
- Comparative: "nhiều hơn cần thiết", "vượt quá phạm vi"
... (54 total for Data Minimization principle)

CAT6_DISTINCTIVE_PHRASES (52 conditional/reasoning markers):
- Conditions: "chỉ khi", "trừ trường hợp", "nếu"
- Reasoning: "căn cứ", "theo quy định", "vì lý do"
... (52 total for Lawfulness principle)
```

#### 3. Synthetic Formality Transformation
```python
# Generate 4 formality levels from legal base

Legal (30% - direct from source):
"Điều 9. Bên kiểm soát dữ liệu cá nhân phải có sự đồng ý của chủ thể"

Formal (30% - legal rephrased with business vocab):
"Techcombank phải có sự đồng ý của khách hàng trước khi xử lý dữ liệu cá nhân"

Business (25% - legal concepts simplified):
"Chúng tôi cần sự đồng ý của bạn để sử dụng thông tin cá nhân"

Casual (15% - conversationalized with GPT-4 + human review):
"Bạn có đồng ý cho mình dùng thông tin của bạn không?"

# Transformation preserves legal accuracy while varying expression
```

#### 4. Regional Flavor Application
```python
# Synthetic regional variations (legal text is national standard)

North (Hanoi) 33% - Governmental formal tone:
"Theo quy định của Bộ Công an, doanh nghiệp phải có sự đồng ý"

Central (Da Nang/Hue) 33% - Traditional business formality:
"Chúng tôi cam kết tuân thủ các quy định về bảo vệ dữ liệu cá nhân"

South (HCMC) 34% - Modern tech/startup phrasing:
"Privacy của bạn rất quan trọng với chúng mình - bạn có đồng ý không?"

# Regional vocabulary and phrasing patterns added during generation
```

#### 5. Quality Control Pipeline
```python
# Multi-stage validation for 24,000 generated samples

Stage 1: VnCoreNLP Validation
- Vietnamese word segmentation check
- Grammar and syntax validation
- Proper Vietnamese linguistic structure

Stage 2: Legal Accuracy Verification
- All samples must align with PDPL Law 91/2025 and Decree 13/2023
- Principle classification must be legally defensible
- No contradictions with Vietnamese data protection framework

Stage 3: Uniqueness Target (90%+)
- Strict data leak detection (threshold >= 1 occurrence)
- Template diversity validation across 46 companies
- max_attempts = 200 for unique sample generation

Stage 4: Human Review
- 100 samples per category (800 total QA samples)
- Vietnamese legal expert validation
- Regional authenticity verification (North/Central/South contexts)

Stage 5: Difficulty Distribution Verification
- VERY_HARD: 40% (multi-principle overlap, no keywords)
- HARD: 40% (contextual understanding required)
- MEDIUM: 15% (implicit references)
- EASY: 5% (clear examples for baseline)
```

#### 6. Example Augmentation Pipeline
```python
# Complete transformation from legal source to training sample

Source (PDPL Điều 9):
"Bên kiểm soát dữ liệu cá nhân phải có sự đồng ý của chủ thể"

↓ Pattern Extraction
Principle: Consent (#8)
Terminology: "đồng ý", "chủ thể", "bên kiểm soát"

↓ Template Application (CompanyRegistry: Techcombank, Banking)
Context: "giao dịch ngân hàng", "khách hàng", "dịch vụ tài chính"

↓ Formality Transformation (Business level)
"Techcombank cần sự đồng ý của bạn trước khi xử lý thông tin giao dịch"

↓ Regional Flavor (South - Modern banking)
"Techcombank cần sự đồng ý của bạn để xử lý thông tin giao dịch nhé"

↓ Difficulty Assignment (HARD - contextual only)
Final Sample: "Techcombank cần xác nhận từ bạn để tiếp tục dịch vụ tài chính"
Label: Consent (Principle #8)
Difficulty: HARD (no explicit "đồng ý" keyword)
Region: South
Formality: Business
```

### Success Metrics for Augmentation

| Metric | Target | Method |
|--------|--------|--------|
| **Total Samples** | 24,000 Vietnamese | Multi-layer generation pipeline |
| **Uniqueness** | 90%+ | Strict leak detection (threshold >= 1) |
| **Legal Accuracy** | 100% | All samples align with PDPL/Decree 13 |
| **Regional Balance** | 33/33/34% N/C/S | Post-processing regional vocabulary |
| **Formality Balance** | 30/30/25/15% | Legal→Formal→Business→Casual pipeline |
| **Difficulty Balance** | 40/40/15/5% VH/H/M/E | Template complexity variation |
| **Template Diversity** | 46 companies × 108 contexts | CompanyRegistry × BUSINESS_CONTEXTS |
| **Quality Validation** | 100 samples/category | Vietnamese legal expert review |

### Why This Approach Works

**Advantages**:
- ✅ **Legal Accuracy**: 100% derived from official PDPL/Decree 13 (813 lines of premium source)
- ✅ **Production Diversity**: 4 formality levels × 3 regions = 12 variation dimensions
- ✅ **Template Richness**: 46 companies × 108 contexts = 4,968 unique combinations
- ✅ **Quality Control**: VnCoreNLP + human review ensures Vietnamese linguistic quality
- ✅ **Scalable**: Same approach works for all 11 VeriAIDPO models (Phases 0-3)

**Key Insight**: 813 lines of premium legal text provide **legal accuracy**, while 24,000 synthetic samples provide **training diversity** — together they create an enterprise-grade Vietnamese PDPL classifier that works across real-world business contexts, not just formal legal documents.

---

## Template Examples

```python
# VERY_HARD (Multi-principle overlap, no keywords)
"Căn cứ hợp đồng, {company} chỉ xử lý dữ liệu cần thiết trong phạm vi đã thông báo."
# → PRIMARY: Purpose Limitation (despite mentioning minimization + lawfulness)
# Generated from: PDPL Điều 3.2 + CompanyRegistry + BUSINESS_CONTEXTS
# Note: Template extracted from legal text, NOT from pre-existing casual examples

````
# → PRIMARY: Purpose Limitation (despite mentioning minimization + lawfulness)

# HARD (Contextual only, subtle indicators)
"{company} cập nhật thông tin khách hàng định kỳ để đảm bảo dịch vụ tốt nhất."
# → Accuracy (no explicit keywords)
# Generated from: PDPL Điều 3.3 (accuracy principle) + CompanyRegistry + Business formality

# MEDIUM (Implicit reference)
"Thông tin của bạn được mã hóa và chỉ nhân viên có quyền mới truy cập được."
# → Security (implicit protection measures)
# Generated from: PDPL Điều 3.4 (security principle) + Formal corporate policy style

# EASY (Clear keyword)
"Chúng tôi cam kết bảo mật thông tin khách hàng theo tiêu chuẩn ISO 27001."
# → Security (explicit security mention)
# Generated from: PDPL Điều 3.4 + Legal formality (direct extraction)

# Note: All examples represent target outputs generated from 813-line legal corpus.
# NOT from pre-existing casual sources - all derived from PDPL/Decree 13 legal framework.
```

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_Principles_VI v2.0)

```python
MODEL_NAME = "vinai/phobert-base-v2"  # Vietnamese PhoBERT
NUM_CATEGORIES = 8
TOTAL_SAMPLES = 24000  # 3,000 per category
DATASET_DIFFICULTY = "VERY_HARD"  # 40% VERY_HARD, 40% HARD, 15% MEDIUM, 5% EASY
EPOCHS = 8-10  # More epochs for very hard dataset
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256  # Longer for complex Vietnamese sentences
WARMUP_STEPS = 500
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

### English Model (VeriAIDPO_Principles_EN v2.0)

```python
MODEL_NAME = "bert-base-uncased"  # English BERT
NUM_CATEGORIES = 8
TOTAL_SAMPLES = 12000  # 1,500 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
EPOCHS = 6-8  # Fewer epochs (BERT has more pre-training)
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128  # Standard for English
WARMUP_STEPS = 300
FORMALITY_LEVELS = ['formal', 'business']
```

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_Principles_VI v2.0)

- **Target Accuracy**: 78-88% (realistic for production with 40% VERY_HARD)
- **Confidence**: 75-85% average
- **Inference Speed**: <50ms per request
- **F1-Score**: 0.75-0.85 (balanced across all 8 categories)
- **Dataset**: 24,000 samples with 40% VERY_HARD + 40% HARD ambiguity

**Quality Principles**:
- ✅ **Quality over quantity**: 24,000 legally accurate samples > 100,000 mediocre samples
- ✅ **Uniqueness target**: 90%+ despite 28x expansion from 813-line legal corpus
- ✅ **Legal accuracy**: 100% alignment with PDPL Law 91/2025 and Decree 13/2023 framework
- ✅ **Regional authenticity**: Synthetic North/Central/South variations reflect real Vietnamese business contexts
- ✅ **Production readiness**: 80% VERY_HARD/HARD samples train enterprise-grade classifier

**Comparison to v1.0**:
- v1.0 MVP: 90-93% accuracy (but only on EASY synthetic data)
- v2.0 Production: 78-88% accuracy (on HARD real-world documents)
- **Trade-off**: Lower accuracy on paper, but handles real enterprise scenarios

**Source Data Foundation**:
- Premium legal corpus: 813 lines of official PDPL/Decree 13 (100% accurate Vietnamese legal text)
- Template expansion: 46 companies × 108 business contexts = 4,968 unique combinations
- Quality control: VnCoreNLP validation + 800 human-reviewed samples (100 per category)

### English Model (VeriAIDPO_Principles_EN v2.0)

- **Target Accuracy**: 82-90% (production-grade)
- **Confidence**: 80-88% average
- **Inference Speed**: <50ms per request
- **F1-Score**: 0.80-0.88 (balanced across all 8 categories)
- **Dataset**: 12,000 samples with 30% VERY_HARD + 40% HARD ambiguity

---

## Vietnamese v2.0 Notebook (Already Created ✅)

**File**: `VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`  
**Status**: ✅ **READY FOR GOOGLE COLAB PRO+ UPLOAD**  
**Created**: October 18, 2025  
**Cells**: 22 cells, 1,402 lines of code

**Key Features**:
- ✅ Uses production backend modules (CompanyRegistry, PDPLTextNormalizer)
- ✅ Dynamic company registry (46+ Vietnamese companies)
- ✅ 24,000 sample generation scripts
- ✅ PhoBERT-base-v2 fine-tuning pipeline
- ✅ Evaluation metrics and confusion matrix
- ✅ Model export for production deployment

**Next Step**: Upload to Google Colab Pro+ and execute training (2-3 days)

---

## Dataset Generation Scripts

### Vietnamese Dataset (24,000 samples from 813-line legal corpus)

**Generation Workflow**:
```
Step 1: Extract patterns from PDPL/Decree 13 (813 lines)
Step 2: Generate templates using CompanyRegistry (46 companies) + BUSINESS_CONTEXTS (108 phrases)
Step 3: Apply formality transformations (Legal → Formal → Business → Casual)
Step 4: Apply regional variations (North/Central/South post-processing)
Step 5: VnCoreNLP validation + human QA review
```

**Script Execution**:
```bash
# Generate Vietnamese v2.0 production dataset (28x expansion from legal corpus)
python backend/scripts/generate_principles_vi_v2.py \
  --source data/pdpl_extraction/pdpl_ocr_text_compact.txt \
  --source data/decree_13_2023/decree_13_2023_text_final.txt \
  --output-file vietnamese_principles_v2.jsonl \
  --samples-per-category 3000 \
  --difficulty VERY_HARD \
  --regional-distribution north:0.33,central:0.33,south:0.34 \
  --formality-distribution legal:0.30,formal:0.30,business:0.25,casual:0.15 \
  --augmentation-strategy template_expansion \
  --quality-control vncorenp+human \
  --uniqueness-target 0.90 \
  --hard-dataset-strategy \
  --verify-quality

# Verify dataset quality (uniqueness, legal accuracy, balance)
python backend/scripts/verify_dataset.py \
  --input-file vietnamese_principles_v2.jsonl \
  --expected-samples 24000 \
  --expected-categories 8 \
  --check-uniqueness 0.90 \
  --check-legal-accuracy
```

### English Dataset (12,000 samples)

```bash
# Generate English v2.0 production dataset
python backend/scripts/generate_principles_en_v2.py \
  --output-file english_principles_v2.jsonl \
  --samples-per-category 1500 \
  --difficulty MODERATE-HARD \
  --formality-distribution formal:0.50,business:0.50 \
  --hard-dataset-strategy \
  --verify-quality

# Verify dataset quality
python backend/scripts/verify_dataset.py \
  --input-file english_principles_v2.jsonl \
  --expected-samples 12000 \
  --expected-categories 8
```

---

## 📋 Architecture Requirements

**CRITICAL - Production Backend Integration**:

✅ **MUST use production backend modules** - See [Architecture Requirements](../VeriAIDPO_Architecture_Requirements.md)

**Required Files for Colab**:
1. `backend/app/core/company_registry.py` (513 lines)
2. `backend/app/core/pdpl_normalizer.py` (~300 lines)
3. `backend/config/company_registry.json` (46+ companies)

**Why This Matters for Phase 0**:
- Training code = Production code (zero drift)
- Hot-reload: Add new companies without retraining
- Vietnamese company names normalized consistently
- Single source of truth

**Setup Guide**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md`

---

## Deployment Strategy

### Zero-Downtime Dual-Model Routing

**v1.0 MVP (Keep for demos)**:
- Continue serving investor demos
- API endpoint: `/api/v1/veriaidpo/principles/classify`
- Use case: Simple examples, proof of concept

**v2.0 Production (Enterprise customers)**:
- Deploy after training complete
- API endpoint: `/api/v2/veriaidpo/principles/classify`
- Use case: Real enterprise compliance documents
- Automatic routing based on user subscription tier

**Gradual Migration**:
1. Week 1-2: v2.0 in beta testing with selected customers
2. Week 3-4: v2.0 becomes default for all enterprise subscriptions
3. Month 2+: v1.0 remains for free tier and demos only

---

## Next Steps

### Immediate (Next 24 hours):
1. ✅ **Review Vietnamese v2.0 notebook**
   - Check dataset generation logic
   - Verify architecture compliance
   - Confirm all 22 cells ready

2. 📤 **Upload to Google Colab Pro+**
   - Create new Colab notebook instance
   - Upload 3 backend files (company_registry.py, pdpl_normalizer.py, company_registry.json)
   - Upload Vietnamese v2.0 notebook
   - Select T4/A100 GPU

3. ▶️ **Execute Vietnamese v2.0 Training**
   - Run all 22 cells sequentially
   - Monitor training progress (8-10 epochs × 2-3 hours)
   - Download trained model

### Short-term (Next 1-2 weeks):
4. 🧪 **Test Vietnamese v2.0 Model**
   - Load model in production environment
   - Test on 100 real Vietnamese compliance documents
   - Compare accuracy vs v1.0 MVP
   - Verify performance meets 78-88% target

5. 📓 **Create English v2.0 Notebook**
   - Copy structure from Vietnamese notebook
   - Adjust for BERT instead of PhoBERT
   - Generate 12,000 English samples
   - Upload and train (2-3 days)

6. 🚀 **Deploy Both Models to Production**
   - v2.0 Vietnamese + English
   - Zero-downtime dual routing
   - Monitor performance metrics

### Medium-term (Weeks 3-4):
7. 📊 **Monitor Production Performance**
   - Track accuracy on real customer documents
   - Collect edge cases for dataset improvement
   - Fine-tune if needed (additional epochs)

8. ➡️ **Begin Phase 1 Models**
   - Start with LegalBasis (most critical)
   - Use v2.0 Principles as template
   - Continue with BreachTriage and CrossBorder

---

## Related Documentation

- [Implementation Overview](../VeriAIDPO_Implementation_Overview.md) - Start here for full context
- [Architecture Requirements](../VeriAIDPO_Architecture_Requirements.md) - MANDATORY for all models
- [Phase 0 Detailed Plan](../VeriAIDPO_Phase0_Principles_Retraining.md) - Comprehensive retraining guide
- [Colab Setup Guide](../VeriAIDPO_Colab_Setup_Guide.md) - Step-by-step training environment setup
- Phase 1 Models: [LegalBasis](../Phase1_Critical_Models/VeriAIDPO_LegalBasis_Spec.md), [BreachTriage](../Phase1_Critical_Models/VeriAIDPO_BreachTriage_Spec.md), [CrossBorder](../Phase1_Critical_Models/VeriAIDPO_CrossBorder_Spec.md)

---

**Phase 0 Priority**: 🚨 **CRITICAL - Must complete before Phase 1-3**  
**Current Status**: ✅ Vietnamese notebook ready → 📤 Upload to Colab → ▶️ Train (2-3 days)  
**Next Action**: Upload Vietnamese v2.0 notebook to Google Colab Pro+ and begin training
