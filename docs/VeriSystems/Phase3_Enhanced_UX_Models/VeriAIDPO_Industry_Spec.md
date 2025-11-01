# VeriAIDPO_Industry - Industry-Specific Requirements Classification

**Phase**: 🔵 Phase 3 - LOW PRIORITY (Enhanced UX)  
**Priority**: 🔵 LOW  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2 days
- English (EN - SECONDARY): 2 days
- **Total**: 4 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_Industry_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_Industry_EN` (BERT, English secondary)

**Classes**: 4 (Finance, Healthcare, Education, Technology)

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_Industry_VI

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

### English (SECONDARY) - VeriAIDPO_Industry_EN

- **Total Samples**: 3,200 (800 per category)
- **Difficulty**: MODERATE
- **Dataset Composition**:
  - **VERY_HARD**: 200/category (25%) - Cross-industry scenarios
  - **HARD**: 320/category (40%) - No industry keywords
  - **MEDIUM**: 200/category (25%) - Subtle indicators
  - **EASY**: 80/category (10%) - Clear examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR industry-specific guidelines, international sector requirements

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_Industry_VI)

- Target Accuracy: 83-90% (production-grade for industry context)
- Confidence: 80-88% average
- Inference Speed: <50ms
- Dataset: 4,800 samples with 25% VERY_HARD ambiguity

### English Model (VeriAIDPO_Industry_EN)

- Target Accuracy: 85-92% (production-grade)
- Confidence: 83-90% average
- Inference Speed: <50ms
- Dataset: 3,200 samples with 25% VERY_HARD ambiguity

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_Industry_VI)

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

### English Model (VeriAIDPO_Industry_EN)

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
