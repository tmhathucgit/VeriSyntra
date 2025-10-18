# Bilingual Training Configuration Summary

**Vietnamese (Primary 70%) + English (Secondary 30%)**

---

## 🎯 **RECOMMENDED APPROACH: Separate Models**

### **Architecture:**
```
VeriAIDPO Bilingual System
│
├── Model 1: VeriAIDPO-VI (Vietnamese) ✅ KEEP EXISTING
│   ├── Base: PhoBERT-base (vinai/phobert-base)
│   ├── Dataset: 6,984 Vietnamese samples
│   ├── Dropout: 0.25
│   ├── Learning Rate: 5e-5
│   ├── Label Smoothing: 0.15
│   ├── Epochs: 12
│   ├── Accuracy: 95-100% ✅
│   └── Size: 540 MB
│
└── Model 2: VeriAIDPO-EN (English) 🆕 NEW
    ├── Base: BERT-base-uncased
    ├── Dataset: 4,000-5,000 English samples (NEW)
    ├── Dropout: 0.20
    ├── Learning Rate: 3e-5
    ├── Label Smoothing: 0.10
    ├── Epochs: 8
    ├── Target Accuracy: 85-92%
    └── Size: 440 MB
```

---

## 📊 **Training Configuration Comparison**

| Parameter | Vietnamese (Current) | English (New) | Why Different? |
|-----------|---------------------|---------------|----------------|
| **Model** | PhoBERT-base | BERT-base | Language-optimized |
| **Samples** | 6,984 | 4,000-5,000 | 70/30 split |
| **Dropout** | 0.25 | 0.20 | English easier to learn |
| **Learning Rate** | 5e-5 | 3e-5 | Standard BERT LR |
| **Label Smoothing** | 0.15 | 0.10 | Less aggressive |
| **Epochs** | 12 | 8 | English needs fewer |
| **Target Accuracy** | 95-100% | 85-92% | Realistic for English |

---

## 🚀 **Implementation Steps**

### **Step 1: Generate English Dataset (Week 1)**
```python
# New file: Step 2.5 EN - English Template Generator

TARGET_SAMPLES = 4000  # 500 per category × 8

# English template structure
{
    'text': 'VNG must process account data lawfully and fairly.',
    'label': 0,
    'language': 'en',  # NEW: Language tag
    'metadata': {
        'company': 'VNG',
        'context': 'banking',
        'region': 'north',
        'difficulty': 'easy'
    }
}
```

### **Step 2: Train English Model (Week 2)**
```python
# Training config for English model

from transformers import AutoModelForSequenceClassification, TrainingArguments

MODEL_NAME = "bert-base-uncased"

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=8,
    hidden_dropout_prob=0.20,
    attention_probs_dropout_prob=0.20,
    classifier_dropout=0.20
)

training_args = TrainingArguments(
    output_dir="./veriaidpo_english",
    num_train_epochs=8,
    learning_rate=3e-5,
    per_device_train_batch_size=8,
    weight_decay=0.01,
    label_smoothing_factor=0.10,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1
)
```

### **Step 3: Create Bilingual Router (Week 3)**
```python
# Automatic language detection and routing

from langdetect import detect

class VeriAIDPOBilingualClassifier:
    def __init__(self):
        # Load both models
        self.model_vi = load_phobert_model()  # Existing
        self.model_en = load_bert_model()     # New
    
    def classify(self, text):
        # Auto-detect language
        language = detect(text)  # 'vi' or 'en'
        
        # Route to appropriate model
        if language == 'vi':
            return self.model_vi.predict(text)
        else:
            return self.model_en.predict(text)
```

---

## 🎯 **Expected Performance**

### **Vietnamese (No Change)**
```
Accuracy: 95-100% ✅ MAINTAINED
Confidence: 92-98%
Speed: 50-100ms
```

### **English (New)**
```
Accuracy: 85-92% 🎯 TARGET
Confidence: 85-95%
Speed: 40-80ms
```

### **Overall System**
```
Combined Accuracy: 90-96% (weighted)
Language Detection: 98-99%
Total Size: 980 MB (both models)
Inference: 50-120ms
```

---

## ✅ **Why This Approach?**

### **Advantages:**
✅ **Keeps Vietnamese 100% accuracy** - No retraining needed  
✅ **Optimized per language** - PhoBERT for Vietnamese, BERT for English  
✅ **Easier maintenance** - Update models independently  
✅ **Better accuracy** - Language-specific optimization  
✅ **Flexible scaling** - Add more languages later

### **Trade-offs:**
⚠️ **Two models** - Slightly more complex deployment  
⚠️ **Larger total size** - 980 MB vs 540 MB  
✅ **Worth it** - Better performance justifies complexity

---

## 📋 **Next Actions**

### **Priority 1: Create English Dataset**
- [ ] Copy Step 2.5 → Create Step 2.5 EN
- [ ] Adapt templates for English grammar
- [ ] Generate 4,000-5,000 English samples
- [ ] Validate quality (uniqueness, balance)

### **Priority 2: Train English Model**
- [ ] Set up BERT-base model
- [ ] Configure training parameters (as above)
- [ ] Run training (expected 2-3 hours on T4)
- [ ] Evaluate on test set (target 85%+)

### **Priority 3: Deploy Bilingual System**
- [ ] Create bilingual classifier class
- [ ] Implement language detection (langdetect)
- [ ] Update API endpoints
- [ ] Test both languages

---

## 🔬 **Alternative NOT Recommended**

### **Single Multilingual Model (XLM-RoBERTa)**

**Configuration:**
```python
MODEL_NAME = "xlm-roberta-base"  # 1.1 GB

# Mixed dataset
Vietnamese: 6,984 (63.6%)
English: 4,000 (36.4%)
Total: 10,984

# Expected results
Vietnamese: 90-95% (⚠️ 5-10% DROP from 100%)
English: 85-90%
Overall: 88-93%
Size: 1.1 GB (larger than separate models)
Speed: 80-150ms (slower)
```

**Why Not:**
❌ Vietnamese accuracy drops 5-10%  
❌ Larger model size  
❌ Slower inference  
❌ Language interference  
❌ Must retrain everything

---

## 📊 **Timeline**

```
Week 1: English Dataset Generation
├── Create Step 2.5 EN template generator
├── Generate 4,000-5,000 English samples
├── Quality validation
└── Dataset ready ✅

Week 2: English Model Training
├── Configure BERT-base model
├── Train for 8 epochs (~2-3 hours)
├── Evaluate performance
└── Model ready (target 85%+) ✅

Week 3: Bilingual Integration
├── Create bilingual classifier
├── Implement language detection
├── Update API endpoints
└── Integration complete ✅

Week 4: Testing & Deployment
├── Test Vietnamese (maintain 100%)
├── Test English (85-92%)
├── Test auto-detection
└── Production deployment ✅
```

---

## 💾 **Deployment Structure**

```
VeriSyntra/backend/app/models/
├── veriaidpo_vi/              # Vietnamese model (existing)
│   ├── pytorch_model.bin      # 540 MB
│   ├── config.json
│   ├── vocab.txt
│   └── training_config.json
│
├── veriaidpo_en/              # English model (new)
│   ├── pytorch_model.bin      # 440 MB
│   ├── config.json
│   ├── vocab.txt
│   └── training_config.json
│
└── bilingual_router.py        # Language detection + routing
```

---

## 🎓 **Key Takeaways**

1. **Vietnamese = 100% accuracy** → Keep PhoBERT, don't retrain
2. **English = New BERT model** → Train separately for 85-92%
3. **Auto language detection** → Route to correct model
4. **Total system = 90-96%** → Weighted average
5. **Deployment = 980 MB** → Two models worth it for quality

---

**Ready to proceed?**  
Next step: Create English dataset generator (Step 2.5 EN)
