# VeriAIDPO_DataSensitivity - Data Category Classification

**Phase**: ⚠️ Phase 2 - MEDIUM PRIORITY  
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

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_DataSensitivity_VI

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

### English (SECONDARY) - VeriAIDPO_DataSensitivity_EN

- **Total Samples**: 4,000 (1,000 per category)
- **Difficulty**: MODERATE-HARD
- **Dataset Composition**:
  - **VERY_HARD**: 300/category (30%) - Borderline data categories
  - **HARD**: 400/category (40%) - No explicit data type keywords
  - **MEDIUM**: 200/category (20%) - Subtle sensitivity indicators
  - **EASY**: 100/category (10%) - Clear category examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR data categories, international data classification standards

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_DataSensitivity_VI)

- Target Accuracy: 78-85% (production-grade with classification ambiguity)
- Confidence: 75-82% average
- Inference Speed: <50ms
- Dataset: 6,000 samples with 30% VERY_HARD ambiguity

### English Model (VeriAIDPO_DataSensitivity_EN)

- Target Accuracy: 82-88% (production-grade)
- Confidence: 80-85% average
- Inference Speed: <50ms
- Dataset: 4,000 samples with 30% VERY_HARD ambiguity

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_DataSensitivity_VI)

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

### English Model (VeriAIDPO_DataSensitivity_EN)

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
