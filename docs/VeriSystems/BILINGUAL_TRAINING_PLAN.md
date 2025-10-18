# VeriAIDPO Bilingual Training Plan (Vietnamese + English)

**Date:** 2025-10-12  
**Objective:** Add English as secondary language to Vietnamese PDPL dataset  
**Primary Language:** Vietnamese (70%)  
**Secondary Language:** English (30%)  
**Target:** Bilingual PDPL 2025 compliance classification

---

## 📊 **Current State Analysis**

### **Existing Dataset (Vietnamese Only):**
```
Total Samples: 6,984 Vietnamese templates
├── Step 2.5 Enhanced Dataset
├── Model: PhoBERT-base (vinai/phobert-base)
├── Tokenizer: Vietnamese-specific (PhoBERT)
├── Categories: 8 PDPL 2025 categories
└── Performance: 100% test accuracy
```

### **Limitations:**
❌ **PhoBERT is Vietnamese-only** - Cannot handle English text effectively  
❌ **Current tokenizer:** Optimized for Vietnamese subwords  
❌ **No English templates** in current dataset  
❌ **No multilingual support** in current architecture

---

## 🎯 **Bilingual Training Strategy**

### **Option A: Separate Models (RECOMMENDED)**

**Architecture:** Train two specialized models

```
VeriAIDPO Bilingual System
├── VeriAIDPO-VI (Vietnamese)
│   ├── Model: PhoBERT-base
│   ├── Dataset: 6,984 Vietnamese samples
│   └── Accuracy: 100%
│
└── VeriAIDPO-EN (English)
    ├── Model: BERT-base-uncased
    ├── Dataset: 5,000 English samples (new)
    └── Target Accuracy: 88-92%
```

**Why Recommended:**
✅ PhoBERT optimized for Vietnamese (keep existing 100% performance)  
✅ BERT-base optimized for English with fast inference (40-80ms)  
✅ No accuracy degradation on Vietnamese  
✅ Language detection routes to correct model  
✅ Easier to maintain and update separately  
✅ Smaller model size (440MB) for efficient deployment

---

### **Option B: Single Multilingual Model**

**Architecture:** One model for both languages

```
VeriAIDPO Multilingual
├── Model: XLM-RoBERTa-base (multilingual)
├── Dataset: 10,984 samples
│   ├── Vietnamese: 6,984 samples (63.6%)
│   └── English: 4,000 samples (36.4%)
└── Target Accuracy: 90-95% (both languages)
```

**Trade-offs:**
⚠️ May reduce Vietnamese accuracy from 100% → 90-95%  
✅ Single model deployment (simpler infrastructure)  
⚠️ Requires complete retraining  
⚠️ Larger model size (~1.1GB vs 540MB)

---

## 🏗️ **Implementation Plan: Option A (Recommended)**

### **Phase 1: English Dataset Generation**

#### **Step 1: Create English Template Generator**

**File:** New Step 2.5 English variant

```python
# STEP 2.5 EN: English PDPL Template Generator
# Target: 5,000 English templates (625 per category)

PDPL_CATEGORIES = {
    0: {"vi": "Tính hợp pháp, công bằng và minh bạch", "en": "Lawfulness, fairness and transparency"},
    1: {"vi": "Hạn chế mục đích", "en": "Purpose limitation"},
    2: {"vi": "Tối thiểu hóa dữ liệu", "en": "Data minimisation"},
    3: {"vi": "Tính chính xác", "en": "Accuracy"},
    4: {"vi": "Hạn chế lưu trữ", "en": "Storage limitation"},
    5: {"vi": "Tính toàn vẹn và bảo mật", "en": "Integrity and confidentiality"},
    6: {"vi": "Trách nhiệm giải trình", "en": "Accountability"},
    7: {"vi": "Quyền của chủ thể dữ liệu", "en": "Data subject rights"}
}

# English business contexts
BUSINESS_CONTEXTS_EN = {
    'banking': ['account', 'transaction', 'credit card', 'loan', 'deposit', 'transfer'],
    'ecommerce': ['order', 'payment', 'delivery', 'product', 'promotion', 'review'],
    'healthcare': ['medical record', 'consultation', 'prescription', 'insurance', 'test', 'diagnosis'],
    'education': ['student', 'grade', 'tuition', 'certificate', 'course', 'degree'],
    'technology': ['application', 'account', 'data', 'security', 'service', 'software'],
    'insurance': ['policy', 'benefit', 'claim', 'premium', 'contract', 'request'],
    'telecommunications': ['call', 'message', 'data', 'roaming', 'charge', 'subscription'],
    'logistics': ['shipping', 'delivery', 'warehouse', 'tracking', 'fee', 'packaging']
}

# English companies (keep Vietnamese names + English templates)
COMPANIES_EN = {
    'north': ['VNG', 'FPT', 'VNPT', 'Viettel', 'Vingroup', 'VietinBank', 'Agribank', 'BIDV'],
    'central': ['Vinamilk', 'Hoa Phat', 'Petrolimex', 'PVN', 'EVN'],
    'south': ['Shopee VN', 'Lazada VN', 'Tiki', 'Grab VN', 'MoMo', 'ZaloPay', 'Techcombank']
}

# English template patterns
def get_english_templates(category_id):
    if category_id == 0:  # Lawfulness, fairness and transparency
        return {
            'simple': [
                '{company} must process {context} data lawfully and fairly.',
                'The company {company} ensures transparency in {context} processing.',
                '{company} provides clear information about {context} data usage.',
                'Lawful processing of {context} is required by {company}.',
                '{company} commits to fair data practices for {context}.'
            ],
            'compound': [
                '{company} processes {context} data lawfully and provides transparent information to users.',
                'The company {company} ensures fairness but also complies with legal requirements for {context}.',
                '{company} maintains transparency and lawful processing of {context} data.',
            ],
            'complex': [
                'To ensure lawfulness, {company} establishes clear legal basis for {context} processing.',
                'When processing {context} data, {company} must demonstrate compliance with legal requirements.',
                'Although complex, {company} commits to maintaining transparency in {context} processing.',
            ]
        }
    # ... (similar patterns for categories 1-7)
```

#### **Step 2: Generate English Dataset**

**Metrics:**
- **Target:** 625 templates per category × 8 = 5,000 samples
- **Quality:** Same rigor as Vietnamese (similarity detection, uniqueness)
- **Metadata:** Language tag added to each sample

```python
# Enhanced sample structure with language tag
{
    'text': 'VNG must process account data lawfully and fairly.',
    'label': 0,
    'template_id': 'abc123',
    'language': 'en',  # NEW: Language identifier
    'metadata': {
        'company': 'VNG',
        'context': 'banking',
        'region': 'north',
        'difficulty': 'easy',
        'formality': 'formal'
    }
}
```

---

### **Phase 2: English Model Training**

#### **Model Selection: BERT-base-uncased**

**Selected Model: BERT-base-uncased ✅**
```python
MODEL_NAME_EN = "bert-base-uncased"
# Size: ~440MB
# Parameters: 110M
# Performance: 88-92% expected (with 5,000 samples)
# Speed: Fast inference (40-80ms)
# Pre-training: 16GB text (BookCorpus + Wikipedia)
# Tokenizer: WordPiece (30K vocabulary)
# Best for: Production deployment with speed + accuracy balance
```

**Why BERT-base:**
✅ **Optimal accuracy:** 88-92% meets English PDPL requirements  
✅ **Fast inference:** 40-80ms critical for production  
✅ **Efficient deployment:** 440MB model size, lower resource needs  
✅ **Cost-effective:** 2-3 hours training time on T4 GPU  
✅ **Proven reliability:** Well-established, stable architecture  
✅ **Dataset fit:** 5,000 samples sufficient for target accuracy

#### **Training Configuration (BERT-base English Model):**

```python
# STEP 4 EN: English Model Configuration

MODEL_NAME_EN = "bert-base-uncased"

# Model Configuration
model_config = {
    'hidden_dropout_prob': 0.20,        # Lower than Vietnamese (English easier)
    'attention_probs_dropout_prob': 0.20,
    'classifier_dropout': 0.20,
    'num_labels': 8
}

# Training Arguments
training_args = {
    'num_train_epochs': 8,              # More epochs (English needs more training)
    'learning_rate': 3e-5,              # Standard BERT learning rate
    'per_device_train_batch_size': 8,
    'per_device_eval_batch_size': 16,
    'weight_decay': 0.01,
    'warmup_ratio': 0.1,
    'label_smoothing_factor': 0.1,      # Moderate smoothing
    'lr_scheduler_type': 'cosine',
    'save_strategy': 'epoch',
    'evaluation_strategy': 'epoch',
    'load_best_model_at_end': True,
    'metric_for_best_model': 'eval_accuracy'
}

# SmartTrainingCallback thresholds (English)
callback_config = {
    'early_high_accuracy_threshold': 0.90,   # 90% (vs 92% for Vietnamese)
    'extreme_overfitting_threshold': 0.95,   # Allow slightly higher
    'patience': 3
}
```

**Expected Training Results (5,000 samples):**
```
Epoch 1: 50-65% accuracy (healthy start)
Epoch 3-4: 78-88% accuracy
Final (Epoch 6-8): 88-92% accuracy
```

---

### **Phase 3: Bilingual Inference System**

#### **Language Detection + Model Routing**

**File:** `backend/app/core/veriaidpo_bilingual_classifier.py`

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from langdetect import detect
from typing import Dict, Optional

class VeriAIDPOBilingualClassifier:
    """
    Bilingual PDPL Classifier with automatic language detection
    Routes to Vietnamese (PhoBERT) or English (BERT) model
    """
    
    def __init__(
        self,
        model_path_vi: str = "./app/models/veriaidpo_vi",
        model_path_en: str = "./app/models/veriaidpo_en"
    ):
        # Load Vietnamese model (PhoBERT)
        self.tokenizer_vi = AutoTokenizer.from_pretrained(model_path_vi)
        self.model_vi = AutoModelForSequenceClassification.from_pretrained(model_path_vi)
        self.model_vi.eval()
        
        # Load English model (BERT)
        self.tokenizer_en = AutoTokenizer.from_pretrained(model_path_en)
        self.model_en = AutoModelForSequenceClassification.from_pretrained(model_path_en)
        self.model_en.eval()
        
        # Move to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_vi.to(self.device)
        self.model_en.to(self.device)
        
        # PDPL Categories (bilingual)
        self.categories = {
            0: {"vi": "Tính hợp pháp, công bằng và minh bạch", "en": "Lawfulness, fairness and transparency"},
            1: {"vi": "Hạn chế mục đích", "en": "Purpose limitation"},
            2: {"vi": "Tối thiểu hóa dữ liệu", "en": "Data minimisation"},
            3: {"vi": "Tính chính xác", "en": "Accuracy"},
            4: {"vi": "Hạn chế lưu trữ", "en": "Storage limitation"},
            5: {"vi": "Tính toàn vẹn và bảo mật", "en": "Integrity and confidentiality"},
            6: {"vi": "Trách nhiệm giải trình", "en": "Accountability"},
            7: {"vi": "Quyền của chủ thể dữ liệu", "en": "Data subject rights"}
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect text language
        Returns: 'vi' (Vietnamese) or 'en' (English)
        """
        try:
            detected = detect(text)
            return 'vi' if detected == 'vi' else 'en'
        except:
            # Fallback: Check for Vietnamese characters
            vietnamese_chars = set('àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ')
            has_vietnamese = any(c.lower() in vietnamese_chars for c in text)
            return 'vi' if has_vietnamese else 'en'
    
    def classify_request(
        self,
        text: str,
        language: Optional[str] = None,
        veri_business_context: Optional[Dict] = None
    ) -> Dict:
        """
        Classify PDPL request in Vietnamese or English
        
        Args:
            text: PDPL request text
            language: Force language ('vi' or 'en'), or None for auto-detect
            veri_business_context: Cultural context from frontend
        
        Returns:
            {
                "category_id": int,
                "category_name_vi": str,
                "category_name_en": str,
                "confidence": float,
                "detected_language": str,
                "model_used": str
            }
        """
        # Detect language
        detected_lang = language if language else self.detect_language(text)
        
        # Route to appropriate model
        if detected_lang == 'vi':
            tokenizer = self.tokenizer_vi
            model = self.model_vi
            model_name = "PhoBERT (Vietnamese)"
        else:
            tokenizer = self.tokenizer_en
            model = self.model_en
            model_name = "BERT (English)"
        
        # Tokenize
        inputs = tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=256
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Predict
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Return bilingual result
        return {
            "category_id": predicted_class,
            "category_name_vi": self.categories[predicted_class]["vi"],
            "category_name_en": self.categories[predicted_class]["en"],
            "confidence": float(confidence),
            "detected_language": detected_lang,
            "model_used": model_name,
            "bilingual": True
        }
```

#### **API Endpoint (Bilingual)**

```python
# backend/app/api/v1/endpoints/veriaidpo.py

@router.post("/classify-bilingual", response_model=VeriPDPLBilingualResponse)
async def classify_bilingual_pdpl_request(request: VeriPDPLBilingualRequest):
    """
    Classify PDPL request in Vietnamese or English
    Automatic language detection and model routing
    """
    try:
        classifier = get_bilingual_classifier()
        result = classifier.classify_request(
            text=request.text,
            language=request.language,  # Optional: force language
            veri_business_context=request.veriBusinessContext
        )
        return VeriPDPLBilingualResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bilingual classification error: {str(e)}"
        )
```

---

## 📊 **Training Configuration Comparison**

### **Vietnamese Model (Current)**
```python
{
    'model': 'vinai/phobert-base',
    'dataset_size': 6984,
    'dropout': 0.25,
    'learning_rate': 5e-5,
    'label_smoothing': 0.15,
    'epochs': 12,
    'expected_accuracy': '95-100%',
    'model_size': '540 MB'
}
```

### **English Model (Proposed)**
```python
{
    'model': 'bert-base-uncased',
    'dataset_size': 5000,
    'dropout': 0.20,
    'learning_rate': 3e-5,
    'label_smoothing': 0.10,
    'epochs': 8,
    'expected_accuracy': '88-92%',
    'model_size': '440 MB'
}
```

### **Combined System**
```python
{
    'total_models': 2,
    'total_parameters': '~270M',
    'total_size': '~980 MB',
    'languages': ['vi', 'en'],
    'language_detection': 'automatic',
    'deployment': 'separate models with router'
}
```

---

## 🎯 **Implementation Roadmap**

### **Week 1: English Dataset Creation**
- [ ] Create Step 2.5 EN (English template generator)
- [ ] Generate 5,000 English PDPL templates (625 per category)
- [ ] Validate uniqueness and quality
- [ ] Create English Step 3 (data splitting)
- [ ] Expected output: English dataset ready

### **Week 2: English Model Training**
- [ ] Set up BERT-base-uncased model (bert-base-uncased)
- [ ] Configure training parameters (dropout 0.20, LR 3e-5, 8 epochs)
- [ ] Train English model (Run 1) - Expected 2-3 hours on T4 GPU
- [ ] Evaluate performance on test set
- [ ] Target: 88-92% test accuracy, 88-95% confidence

### **Week 3: Bilingual System Integration**
- [ ] Create bilingual classifier class
- [ ] Implement language detection
- [ ] Create model routing logic
- [ ] Update API endpoints
- [ ] Test bilingual inference

### **Week 4: Testing & Deployment**
- [ ] Test Vietnamese classification (maintain 100%)
- [ ] Test English classification (88-92%)
- [ ] Test language detection accuracy
- [ ] Integration testing
- [ ] Deploy to production

---

## 📈 **Expected Performance Metrics**

### **Vietnamese Performance (Maintained)**
```
Test Accuracy: 95-100%
Confidence: 92-98%
Inference Speed: 50-100ms
Language: Vietnamese only
```

### **English Performance (Target)**
```
Test Accuracy: 88-92%
Confidence: 88-95%
Inference Speed: 40-80ms
Language: English only
```

### **Bilingual System (Combined)**
```
Overall Accuracy: 92-96% (weighted average)
Language Detection: 98-99%
Total Inference: 50-120ms (including detection)
Languages: Vietnamese (primary), English (secondary)
```

---

## 💡 **Alternative: Mixed Dataset Training (Not Recommended)**

If you still want to train **one model** on **mixed Vietnamese + English data**:

### **Model: XLM-RoBERTa-base**
```python
MODEL_NAME = "xlm-roberta-base"  # Multilingual transformer

# Dataset composition
mixed_dataset = {
    'vietnamese': 6984,  # 58.3%
    'english': 5000,     # 41.7%
    'total': 11984
}

# Training config (adjusted for multilingual)
config = {
    'dropout': 0.25,              # Higher dropout for mixed data
    'learning_rate': 2e-5,        # Lower LR for stability
    'label_smoothing': 0.15,      # Prevent language-specific overfitting
    'epochs': 10-12,              # More epochs needed
    'batch_size': 8,              # Smaller batches
    'model_size': '1.1 GB'        # Larger model
}

# Expected results
results = {
    'vietnamese_accuracy': '90-95%',  # ⚠️ 5-10% drop from 100%
    'english_accuracy': '85-90%',
    'overall_accuracy': '88-93%',
    'inference_speed': '80-150ms'    # Slower due to larger model
}
```

**Why Not Recommended:**
❌ Reduces Vietnamese accuracy from 100% to 90-95%  
❌ Larger model size (1.1GB vs 980MB for separate models)  
❌ Slower inference  
❌ More complex training  
❌ Language interference possible

---

## ✅ **Recommended Next Steps**

### **Immediate Actions:**

1. **Decide on Architecture:**
   - ✅ **Option A (Recommended):** Separate models (Vietnamese PhoBERT + English BERT)
   - ⚠️ **Option B:** Single multilingual model (XLM-RoBERTa)

2. **If choosing Option A (Separate Models - RECOMMENDED):**
   - Create English template generator (Step 2.5 EN)
   - Generate 5,000 English samples (625 per category)
   - Train BERT-base-uncased on English data
   - Implement bilingual routing system with language detection

3. **If choosing Option B (Single Multilingual):**
   - Merge Vietnamese + English datasets
   - Retrain from scratch with XLM-RoBERTa
   - Accept 5-10% Vietnamese accuracy drop
   - Test multilingual performance

### **Priority Order:**
1. 🥇 **Create English dataset** (Week 1)
2. 🥈 **Train English model** (Week 2)
3. 🥉 **Build bilingual router** (Week 3)
4. 📦 **Deploy and test** (Week 4)

---

## 📝 **Summary**

**Recommended Approach:** **Separate Models (Option A)**

| Metric | Vietnamese Model | English Model | Combined System |
|--------|-----------------|---------------|-----------------|
| **Model** | PhoBERT-base | BERT-base | Bilingual Router |
| **Dataset** | 6,984 samples | 5,000 samples | 11,984 total |
| **Accuracy** | 95-100% | 88-92% | 92-96% avg |
| **Size** | 540 MB | 440 MB | 980 MB |
| **Speed** | 50-100ms | 40-80ms | 50-120ms |
| **Deployment** | Existing | New training | Router logic |

**Key Benefits:**
✅ Maintains Vietnamese 100% accuracy (PhoBERT unchanged)  
✅ Optimized models for each language (PhoBERT-VI + BERT-EN)  
✅ Fast inference: BERT-base 40-80ms per classification  
✅ Efficient deployment: 980MB total (440MB EN + 540MB VI)  
✅ Easier maintenance and updates per language  
✅ Language-specific fine-tuning possible  
✅ No retraining of existing Vietnamese model  
✅ Cost-effective: BERT-base trains in 2-3 hours

**Trade-off:**
⚠️ Slightly more deployment complexity (2 models + router)  
✅ Worth it for better per-language performance and speed

---

**Would you like me to create the English dataset generator (Step 2.5 EN) next?**
