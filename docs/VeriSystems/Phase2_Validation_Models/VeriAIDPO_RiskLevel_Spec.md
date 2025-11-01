# VeriAIDPO_RiskLevel - Risk Assessment Classification

**Phase**: ⚠️ Phase 2 - MEDIUM PRIORITY  
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

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_RiskLevel_VI

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

### English (SECONDARY) - VeriAIDPO_RiskLevel_EN

- **Total Samples**: 4,800 (1,200 per category)
- **Difficulty**: MODERATE-HARD (critical judgment required)
- **Dataset Composition**:
  - **VERY_HARD**: 420/category (35%) - Borderline risk assessments
  - **HARD**: 480/category (40%) - No risk keywords
  - **MEDIUM**: 216/category (18%) - Subtle risk signals
  - **EASY**: 84/category (7%) - Clear risk examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR risk assessment guides, international DPIA frameworks

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_RiskLevel_VI)

- Target Accuracy: 75-83% (production-grade with high judgment complexity)
- Confidence: 72-80% average
- Inference Speed: <50ms
- Dataset: 8,000 samples with 35% VERY_HARD ambiguity

### English Model (VeriAIDPO_RiskLevel_EN)

- Target Accuracy: 80-88% (production-grade)
- Confidence: 78-85% average
- Inference Speed: <50ms
- Dataset: 4,800 samples with 35% VERY_HARD ambiguity

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_RiskLevel_VI)

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

### English Model (VeriAIDPO_RiskLevel_EN)

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
