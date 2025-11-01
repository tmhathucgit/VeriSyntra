# VeriAIDPO_Regional - Vietnamese Regional Context Classification

**Phase**: 🔵 Phase 3 - LOW PRIORITY (Enhanced UX)  
**Priority**: 🔵 LOW  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 1 day
- English (EN - SECONDARY): 1 day
- **Total**: 2 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_Regional_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_Regional_EN` (BERT, English secondary)

**Classes**: 3 (North, Central, South)

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_Regional_VI

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

### English (SECONDARY) - VeriAIDPO_Regional_EN

- **Total Samples**: 3,000 (1,000 per category)
- **Difficulty**: MODERATE (for international context understanding)
- **Dataset Composition**:
  - **VERY_HARD**: 250/category (25%) - Borderline regional context
  - **HARD**: 400/category (40%) - No location keywords
  - **MEDIUM**: 250/category (25%) - Subtle indicators
  - **EASY**: 100/category (10%) - Clear examples
- **Formality Levels**: Formal, Business
- **Sources**: Vietnamese regional business descriptions in English, international documentation

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_Regional_VI)

- Target Accuracy: 85-92% (production-grade for cultural context)
- Confidence: 83-90% average
- Inference Speed: <50ms
- Dataset: 4,500 samples with 25% VERY_HARD ambiguity

### English Model (VeriAIDPO_Regional_EN)

- Target Accuracy: 88-93% (production-grade)
- Confidence: 85-91% average
- Inference Speed: <50ms
- Dataset: 3,000 samples with 25% VERY_HARD ambiguity

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_Regional_VI)

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

### English Model (VeriAIDPO_Regional_EN)

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
