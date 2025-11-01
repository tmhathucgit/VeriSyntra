# VeriAIDPO_DPOTasks - DPO Task Type Classification

**Phase**: ⚠️ Phase 2 - MEDIUM PRIORITY  
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

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_DPOTasks_VI

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

### English (SECONDARY) - VeriAIDPO_DPOTasks_EN

- **Total Samples**: 4,000 (800 per category)
- **Difficulty**: MODERATE
- **Dataset Composition**:
  - **VERY_HARD**: 240/category (30%) - Overlapping task types
  - **HARD**: 320/category (40%) - No task keywords
  - **MEDIUM**: 160/category (20%) - Subtle task indicators
  - **EASY**: 80/category (10%) - Clear task examples
- **Formality Levels**: Formal, Business
- **Sources**: GDPR DPO tasks, international data protection officer guides

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_DPOTasks_VI)

- Target Accuracy: 80-87% (production-grade with task overlap)
- Confidence: 78-85% average
- Inference Speed: <50ms
- Dataset: 6,000 samples with 30% VERY_HARD ambiguity

### English Model (VeriAIDPO_DPOTasks_EN)

- Target Accuracy: 83-90% (production-grade)
- Confidence: 82-88% average
- Inference Speed: <50ms
- Dataset: 4,000 samples with 30% VERY_HARD ambiguity

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_DPOTasks_VI)

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

### English Model (VeriAIDPO_DPOTasks_EN)

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
