# VeriAIDPO_ComplianceStatus - Overall Compliance Classification

**Phase**: 🔵 Phase 3 - LOW PRIORITY (Enhanced UX)  
**Priority**: 🔵 LOW  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 1 day
- English (EN - SECONDARY): 1 day
- **Total**: 2 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_ComplianceStatus_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_ComplianceStatus_EN` (BERT, English secondary)

**Classes**: 4 (Compliant, Partial, Non-Compliant, Unknown)

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_ComplianceStatus_VI

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

### English (SECONDARY) - VeriAIDPO_ComplianceStatus_EN

- **Total Samples**: 3,200 (800 per category)
- **Difficulty**: MODERATE
- **Dataset Composition**:
  - **VERY_HARD**: 200/category (25%) - Borderline status
  - **HARD**: 320/category (40%) - No status keywords
  - **MEDIUM**: 200/category (25%) - Subtle indicators
  - **EASY**: 80/category (10%) - Clear examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR compliance reports, international audit frameworks

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_ComplianceStatus_VI)

- Target Accuracy: 82-88% (production-grade for UX)
- Confidence: 80-87% average
- Inference Speed: <50ms
- Dataset: 4,800 samples with 25% VERY_HARD ambiguity

### English Model (VeriAIDPO_ComplianceStatus_EN)

- Target Accuracy: 85-92% (production-grade)
- Confidence: 83-90% average
- Inference Speed: <50ms
- Dataset: 3,200 samples with 25% VERY_HARD ambiguity

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_ComplianceStatus_VI)

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

### English Model (VeriAIDPO_ComplianceStatus_EN)

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

---

## 📋 Architecture Requirements

**CRITICAL - Production Backend Integration**:

✅ **MUST use production backend modules** - See [Architecture Requirements](../VeriAIDPO_Architecture_Requirements.md)

**Required Files for Colab**:
1. `backend/app/core/company_registry.py` (513 lines)
2. `backend/app/core/pdpl_normalizer.py` (~300 lines)
3. `backend/config/company_registry.json` (46+ companies)

**Key Benefits**:
- ✅ Training code = Production code (zero drift)
- ✅ Hot-reload capability (add companies without retraining)
- ✅ Single source of truth
- ✅ Easier maintenance

**Setup Guide**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md`

---

## Related Documentation

- [Implementation Overview](../VeriAIDPO_Implementation_Overview.md)
- [Architecture Requirements](../VeriAIDPO_Architecture_Requirements.md)
- [Phase 0: Principles Retraining](../VeriAIDPO_Phase0_Principles_Retraining.md)
- [Colab Setup Guide](../VeriAIDPO_Colab_Setup_Guide.md)
