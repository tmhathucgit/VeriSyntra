# VeriAIDPO - PhoBERT Training Guide for Vietnamese Cultural Context
## Training PhoBERT for Vietnamese PDPL 2025 Compliance with Regional Diversity

> **🇻🇳 Vietnamese-First Design**: This guide implements **Vietnamese as PRIMARY language** and **English as SECONDARY language** to align with VeriPortal's cultural approach. All code examples, variables, and outputs prioritize Vietnamese (Tiếng Việt) with support for regional diversity (Miền Bắc, Miền Trung, Miền Nam).

### **Executive Summary**

This document provides a complete guide to training **PhoBERT** (VinAI Research) on Vietnamese PDPL compliance datasets with full support for Vietnamese cultural and linguistic diversity.

**🎯 Vietnamese Cultural Alignment:**
- ✅ **Primary Language**: Vietnamese (Tiếng Việt)
- ✅ **Secondary Language**: English (for international developers)
- ✅ **Regional Support**: North (Bắc), Central (Trung), South (Nam) Vietnamese variations
- ✅ **Model**: PhoBERT-base/large (VinAI Research - Vietnamese-optimized)
- ✅ **Legal Context**: Vietnamese PDPL 2025 (Nghị định 13/2023/NĐ-CP)

**Why Vietnamese-First?**
1. 🇻🇳 VeriPortal serves Vietnamese market (95M+ Vietnamese speakers)
2. 🏛️ PDPL 2025 is Vietnamese law (primary legal language is Vietnamese)
3. 👥 End users are Vietnamese businesses and DPOs
4. 🌏 Respects Vietnamese cultural diversity (3 regional variations)
5. 📊 Training data is Vietnamese legal text

---

## **📋 Overview: What You'll Build**

**Goal**: Train PhoBERT to classify Vietnamese PDPL text into compliance categories

**Input**: Vietnamese text (e.g., "Công ty phải bảo vệ dữ liệu cá nhân")
**Output**: Compliance category (e.g., "Data minimization") + confidence score

**Training Process**:
```
Step 1: Prepare Dataset (PDPL legal text + labels)
   ↓
Step 2: Preprocess with VnCoreNLP (word segmentation)
   ↓
Step 3: Fine-tune PhoBERT (transfer learning)
   ↓
Step 4: Evaluate Model (test accuracy)
   ↓
Step 5: Save & Deploy Model
```

---

## **Step 1: Prepare Your PDPL Dataset**

### **1.1 Dataset Structure**

Create training data in JSONL format (one JSON object per line):

```jsonl
{"text": "Công ty phải thu thập dữ liệu một cách hợp pháp và minh bạch", "label": 0}
{"text": "Dữ liệu cá nhân chỉ được sử dụng cho mục đích đã thông báo", "label": 1}
{"text": "Chỉ thu thập dữ liệu cần thiết cho mục đích cụ thể", "label": 2}
{"text": "Dữ liệu phải chính xác và được cập nhật thường xuyên", "label": 3}
{"text": "Không lưu trữ dữ liệu lâu hơn thời gian cần thiết", "label": 4}
{"text": "Dữ liệu phải được mã hóa và bảo vệ an toàn", "label": 5}
{"text": "Doanh nghiệp chịu trách nhiệm về việc xử lý dữ liệu", "label": 6}
{"text": "Người dùng có quyền truy cập và xóa dữ liệu cá nhân", "label": 7}
```

### **1.2 Label Mapping (8 PDPL Principles) - Vietnamese-First Design**

**🇻🇳 Vietnamese Primary**: All labels default to Vietnamese. English is secondary for international use.

```python
# label_mapping.py
"""
PDPL 2025 Compliance Category Labels (Bilingual)
Vietnamese-First Approach for VeriPortal

Cultural Context:
- Vietnamese (Tiếng Việt) is PRIMARY language
- English is SECONDARY language
- Supports regional variations (Bắc, Trung, Nam)
"""

# Vietnamese labels (PRIMARY - default for VeriPortal)
PDPL_NHAN_VI = {
    0: "Tính hợp pháp, công bằng và minh bạch",
    1: "Hạn chế mục đích",
    2: "Tối thiểu hóa dữ liệu",
    3: "Tính chính xác",
    4: "Hạn chế lưu trữ",
    5: "Tính toàn vẹn và bảo mật",
    6: "Trách nhiệm giải trình",
    7: "Quyền của chủ thể dữ liệu"
}

# English labels (SECONDARY - for international reports only)
PDPL_LABELS_EN = {
    0: "Lawfulness, fairness and transparency",
    1: "Purpose limitation",
    2: "Data minimization",
    3: "Accuracy",
    4: "Storage limitation",
    5: "Integrity and confidentiality",
    6: "Accountability",
    7: "Rights of data subjects"
}

# Regional variations (optional - for cultural diversity)
PDPL_NHAN_BAC = {  # Northern Vietnamese (Miền Bắc)
    0: "Tính hợp pháp, công bằng và minh bạch",
    5: "Tính toàn vẹn và bảo mật",
    # ... (uses standard Vietnamese with "đảm bảo", "cần phải")
}

PDPL_NHAN_TRUNG = {  # Central Vietnamese (Miền Trung)
    0: "Tính hợp pháp, công bằng và minh bạch",
    5: "Tính toàn vẹn và bảo đảm",  # Note: "bảo đảm" variation
    # ... (uses "cần", "bảo đảm")
}

PDPL_NHAN_NAM = {  # Southern Vietnamese (Miền Nam)
    0: "Tính hợp pháp, công bằng và minh bạch",
    5: "Tính toàn vẹn và bảo mật",
    # ... (uses "đảm bảo", "cần")
}

# DEFAULT: Use Vietnamese as primary (Vietnamese-first cultural alignment)
PDPL_LABELS = PDPL_NHAN_VI  # Vietnamese is DEFAULT

# Reverse mapping for label to ID conversion (Vietnamese primary)
NHAN_SANG_ID = {v: k for k, v in PDPL_NHAN_VI.items()}

# Helper function to get label in any language or region
def lay_nhan(nhan_id, ngon_ngu='vi', mien='standard'):
    """
    Get PDPL label in specified language and regional variation
    (Vietnamese function name: lay_nhan = get_label)
    
    Args:
        nhan_id (int): Label ID (0-7)
        ngon_ngu (str): 'vi' for Vietnamese (DEFAULT), 'en' for English
        mien (str): 'standard', 'bac' (North), 'trung' (Central), 'nam' (South)
    
    Returns:
        str: Label text in specified language and regional variation
    
    Examples:
        >>> lay_nhan(5)  # Vietnamese (default)
        'Tính toàn vẹn và bảo mật'
        
        >>> lay_nhan(5, ngon_ngu='en')  # English (secondary)
        'Integrity and confidentiality'
        
        >>> lay_nhan(5, mien='trung')  # Central Vietnamese
        'Tính toàn vẹn và bảo đảm'
    """
    if ngon_ngu == 'en':
        return PDPL_LABELS_EN[nhan_id]
    elif mien == 'bac':
        return PDPL_NHAN_BAC.get(nhan_id, PDPL_NHAN_VI[nhan_id])
    elif mien == 'trung':
        return PDPL_NHAN_TRUNG.get(nhan_id, PDPL_NHAN_VI[nhan_id])
    elif mien == 'nam':
        return PDPL_NHAN_NAM.get(nhan_id, PDPL_NHAN_VI[nhan_id])
    else:
        return PDPL_NHAN_VI[nhan_id]  # Default: Standard Vietnamese

# Alias for English-speaking developers (maps to Vietnamese-first function)
get_label = lay_nhan
```

**🇻🇳 Why Vietnamese-First Design?**

1. ✅ **Vietnamese is PRIMARY language** → VeriPortal serves Vietnamese market
2. ✅ **English is SECONDARY** → Only for international reports and developers
3. ✅ **Training data is Vietnamese** → PhoBERT learns Vietnamese legal language
4. ✅ **Regional diversity** → Supports Bắc, Trung, Nam linguistic variations
5. ✅ **Cultural alignment** → Respects Vietnamese language diversity (95M speakers across 3 regions)
6. ✅ **Legal context** → PDPL 2025 is Vietnamese law (Nghị định 13/2023/NĐ-CP)

### **1.3 Create Training Files - Vietnamese-First Structure**

**🇻🇳 Recommended**: Use Vietnamese folder and file names (primary language):

```
du_lieu_pdpl/                          (PDPL data folder)
├── huan_luyen.jsonl                  (training data - 70%)
├── kiem_tra.jsonl                    (validation data - 15%)
└── danh_gia.jsonl                    (test data - 15%)
```

**Alternative English naming** (for international developers):
```
data/
├── train.jsonl     (70% of data, e.g., 700 examples)
├── val.jsonl       (15% of data, e.g., 150 examples)
└── test.jsonl      (15% of data, e.g., 150 examples)
```

**📊 Dataset Size Requirements:**
- **Minimum**: 500-1000 examples (good accuracy for MVP)
- **Recommended**: 2000+ examples (production quality)
- **Optimal**: 5000+ examples with regional diversity (enterprise-grade)

**🌏 Regional Balance** (important for Vietnamese diversity):
- 33% from North Vietnam (Miền Bắc) - Hanoi, Hai Phong
- 33% from Central Vietnam (Miền Trung) - Da Nang, Hue
- 33% from South Vietnam (Miền Nam) - Ho Chi Minh City, Can Tho

### **1.4 Vietnamese Regional Diversity (Critical for Production)**

**🌏 Why Regional Diversity Matters:**
- Vietnam has 3 distinct linguistic regions (Bắc, Trung, Nam)
- Each region uses different vocabulary, pronunciation, and grammar
- PhoBERT must understand ALL regional variations for production quality
- VeriPortal serves users across all Vietnam regions

**📍 Regional Language Variations:**

```python
# du_lieu_mien.py (Regional Data Examples)
"""
Vietnamese Regional Diversity Examples for PDPL Training
Supports: Miền Bắc (North), Miền Trung (Central), Miền Nam (South)
"""

du_lieu_mien = {
    'Miền Bắc (North)': {
        'region_code': 'BAC',
        'cities': ['Hà Nội', 'Hải Phòng', 'Quảng Ninh'],
        'examples': [
            "Doanh nghiệp cần phải đảm bảo dữ liệu được bảo mật",
            "Công ty phải tuân thủ các quy định về bảo vệ dữ liệu cá nhân",
            "Dữ liệu khách hàng cần phải được mã hóa và lưu trữ an toàn",
            "Người dùng có quyền yêu cầu xóa dữ liệu cá nhân của mình"
        ],
        'characteristics': ['cần phải', 'đảm bảo', 'các quy định về', 'phải']
    },
    
    'Miền Trung (Central)': {
        'region_code': 'TRUNG',
        'cities': ['Đà Nẵng', 'Huế', 'Quảng Nam'],
        'examples': [
            "Doanh nghiệp cần bảo đảm dữ liệu được bảo mật",
            "Công ty phải tuân thủ quy định bảo vệ dữ liệu cá nhân",
            "Dữ liệu khách hàng cần được mã hóa và lưu trữ an toàn",
            "Người dùng có quyền yêu cầu xóa dữ liệu cá nhân"
        ],
        'characteristics': ['cần', 'bảo đảm', 'quy định', 'phải']
    },
    
    'Miền Nam (South)': {
        'region_code': 'NAM',
        'cities': ['Thành phố Hồ Chí Minh', 'Cần Thơ', 'Vũng Tàu'],
        'examples': [
            "Doanh nghiệp cần đảm bảo dữ liệu được bảo mật",
            "Công ty phải tuân thủ các quy định về bảo vệ dữ liệu cá nhân",
            "Dữ liệu khách hàng cần được mã hóa và lưu trữ an toàn",
            "Người dùng có quyền yêu cầu xóa dữ liệu cá nhân của họ"
        ],
        'characteristics': ['cần', 'đảm bảo', 'các quy định về', 'của họ']
    }
}
```

**🔍 Key Regional Differences:**

| Feature | Bắc (North) | Trung (Central) | Nam (South) |
|---------|-------------|-----------------|-------------|
| **Modal verb** | cần phải | cần | cần |
| **"Ensure"** | đảm bảo | bảo đảm | đảm bảo |
| **"Regulations"** | quy định về | quy định | quy định về |
| **"Their"** | của mình | của | của họ |
| **Formality** | Very formal | Moderate | Less formal |

**✅ Best Practice for Dataset Collection:**
1. Include 33% examples from each region (balanced)
2. Label examples with region metadata (optional)
3. Test model performance across all 3 regions
4. Ensure accuracy is >85% for ALL regions (not just average)

---

## **Step 2: Install Dependencies**

### **2.1 Create Virtual Environment**

```bash
# Create virtual environment
python -m venv veriaidpo-env

# Activate (Windows)
veriaidpo-env\Scripts\activate

# Activate (Linux/Mac)
source veriaidpo-env/bin/activate
```

### **2.2 Install Packages**

```bash
# Install PyTorch (CPU version for local testing)
pip install torch torchvision torchaudio

# Install Hugging Face Transformers
pip install transformers==4.35.0

# Install training utilities
pip install datasets==2.14.0
pip install accelerate==0.24.0
pip install scikit-learn==1.3.0

# Install VnCoreNLP (optional, for preprocessing)
pip install vncorenlp==1.0.3

# Download VnCoreNLP JAR (one-time)
wget https://github.com/vncorenlp/VnCoreNLP/raw/master/VnCoreNLP-1.2.jar
```

### **2.3 Verify Installation**

```python
# test_installation.py
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification

print(f"PyTorch version: {torch.__version__}")
print(f"Transformers version: {transformers.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Test PhoBERT loading
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
print("✅ PhoBERT tokenizer loaded successfully")
```

---

## **Step 3: Preprocess Dataset with VnCoreNLP (Optional but Recommended)**

### **3.1 Why Preprocess?**

Vietnamese word segmentation improves PhoBERT accuracy:
- **Without**: "Công ty phải bảo vệ dữ liệu" → PhoBERT sees syllables
- **With VnCoreNLP**: "Công_ty phải bảo_vệ dữ_liệu" → PhoBERT sees words

**Accuracy improvement**: +5-10%

### **3.2 Preprocessing Script**

```python
# preprocess_dataset.py
"""
Preprocess Vietnamese PDPL dataset with VnCoreNLP
"""

from vncorenlp import VnCoreNLP
import json

# Initialize VnCoreNLP
annotator = VnCoreNLP("./VnCoreNLP-1.2.jar", annotators="wseg", max_heap_size='-Xmx2g')

def segment_vietnamese(text):
    """Segment Vietnamese text with VnCoreNLP"""
    segmented = annotator.tokenize(text)
    # Join words with underscores
    processed = ' '.join(['_'.join(sentence) for sentence in segmented])
    return processed

def preprocess_file(input_file, output_file):
    """Preprocess JSONL file"""
    with open(input_file, 'r', encoding='utf-8') as f_in:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for line in f_in:
                data = json.loads(line)
                # Segment Vietnamese text
                data['text'] = segment_vietnamese(data['text'])
                # Write to output
                f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
    print(f"✅ Preprocessed {input_file} → {output_file}")

# Preprocess all files
preprocess_file('data/train.jsonl', 'data/train_preprocessed.jsonl')
preprocess_file('data/val.jsonl', 'data/val_preprocessed.jsonl')
preprocess_file('data/test.jsonl', 'data/test_preprocessed.jsonl')

annotator.close()
print("✅ All files preprocessed successfully")
```

**Run preprocessing:**
```bash
python preprocess_dataset.py
```

---

## **Step 4: Load and Prepare Dataset**

### **4.1 Create Dataset Loader**

```python
# load_dataset.py
"""
Load PDPL dataset for PhoBERT training
"""

from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer

# Load PhoBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Load dataset from JSONL files
dataset = load_dataset('json', data_files={
    'train': 'data/train_preprocessed.jsonl',
    'validation': 'data/val_preprocessed.jsonl',
    'test': 'data/test_preprocessed.jsonl'
})

print(f"Dataset loaded:")
print(f"  Train: {len(dataset['train'])} examples")
print(f"  Validation: {len(dataset['validation'])} examples")
print(f"  Test: {len(dataset['test'])} examples")

# Tokenize function
def tokenize_function(examples):
    """Tokenize Vietnamese text for PhoBERT"""
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=256  # Maximum sequence length
    )

# Tokenize all datasets
print("Tokenizing datasets...")
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Remove original text column (keep tokenized input_ids, attention_mask)
tokenized_dataset = tokenized_dataset.remove_columns(['text'])

# Rename 'label' to 'labels' (required by Trainer)
tokenized_dataset = tokenized_dataset.rename_column('label', 'labels')

print("✅ Dataset tokenized and ready for training")
```

---

## **Step 5: Fine-tune PhoBERT**

### **5.1 Training Script**

```python
# train_phobert.py
"""
Fine-tune PhoBERT on Vietnamese PDPL compliance dataset
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Set random seed for reproducibility
torch.manual_seed(42)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Load dataset
dataset = load_dataset('json', data_files={
    'train': 'data/train_preprocessed.jsonl',
    'validation': 'data/val_preprocessed.jsonl',
    'test': 'data/test_preprocessed.jsonl'
})

# Tokenize function
def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=256
    )

# Tokenize datasets
tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset = tokenized_dataset.remove_columns(['text'])
tokenized_dataset = tokenized_dataset.rename_column('label', 'labels')

# Load PhoBERT model (8 output classes for PDPL categories)
model = AutoModelForSequenceClassification.from_pretrained(
    "vinai/phobert-base",
    num_labels=8  # 8 PDPL compliance categories
)

# Data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Define metrics
def compute_metrics(eval_pred):
    """Calculate accuracy, precision, recall, F1"""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    
    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average='weighted'
    )
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# Training arguments
training_args = TrainingArguments(
    output_dir='./phobert-pdpl-finetuned',
    
    # Training hyperparameters
    num_train_epochs=5,              # Number of training epochs
    per_device_train_batch_size=16,  # Batch size for training
    per_device_eval_batch_size=32,   # Batch size for evaluation
    learning_rate=2e-5,              # Learning rate
    weight_decay=0.01,               # Weight decay (L2 regularization)
    warmup_steps=500,                # Warmup steps for learning rate
    
    # Evaluation & saving
    evaluation_strategy='epoch',     # Evaluate every epoch
    save_strategy='epoch',           # Save checkpoint every epoch
    load_best_model_at_end=True,    # Load best model after training
    metric_for_best_model='accuracy',# Use accuracy to select best model
    
    # Logging
    logging_dir='./logs',
    logging_steps=100,
    
    # Performance
    fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
    dataloader_num_workers=0,        # Number of data loading workers
    
    # Early stopping (optional)
    # early_stopping_patience=3,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['validation'],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# Train model
print("🚀 Starting PhoBERT training...")
trainer.train()

# Evaluate on test set
print("\n📊 Evaluating on test set...")
test_results = trainer.evaluate(tokenized_dataset['test'])
print(f"Test Results: {test_results}")

# Save final model
print("\n💾 Saving model...")
trainer.save_model('./phobert-pdpl-final')
tokenizer.save_pretrained('./phobert-pdpl-final')

print("✅ Training complete! Model saved to ./phobert-pdpl-final")
```

### **5.2 Run Training**

```bash
# Start training (CPU - slower)
python train_phobert.py

# OR with GPU (faster)
CUDA_VISIBLE_DEVICES=0 python train_phobert.py
```

**Expected training time**:
- **CPU**: 2-4 hours (1000 examples, 5 epochs)
- **GPU (T4/V100)**: 15-30 minutes

---

## **Step 6: Evaluate Model**

### **6.1 Evaluation Script**

```python
# evaluate_model.py
"""
Evaluate fine-tuned PhoBERT on test set
"""

from transformers import pipeline
from datasets import load_dataset
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Load fine-tuned model
classifier = pipeline(
    'text-classification',
    model='./phobert-pdpl-final',
    tokenizer='./phobert-pdpl-final',
    device=0 if torch.cuda.is_available() else -1
)

# Load test dataset
test_dataset = load_dataset('json', data_files='data/test_preprocessed.jsonl')['train']

# PDPL labels
labels = [
    "Lawfulness", "Purpose limitation", "Data minimization",
    "Accuracy", "Storage limitation", "Integrity",
    "Accountability", "Data subject rights"
]

# Predict on test set
print("Making predictions on test set...")
predictions = []
true_labels = []

for example in test_dataset:
    result = classifier(example['text'])[0]
    predicted_label = int(result['label'].split('_')[1])  # Extract label number
    predictions.append(predicted_label)
    true_labels.append(example['label'])

# Calculate metrics
print("\n📊 Classification Report:")
print(classification_report(true_labels, predictions, target_names=labels))

# Confusion matrix
print("\n📈 Confusion Matrix:")
cm = confusion_matrix(true_labels, predictions)
print(cm)

# Overall accuracy
accuracy = np.mean(np.array(predictions) == np.array(true_labels))
print(f"\n✅ Overall Accuracy: {accuracy:.2%}")
```

**Run evaluation:**
```bash
python evaluate_model.py
```

**Expected accuracy**: 85-95% (depends on dataset quality and size)

---

## **Step 7: Test Your Trained Model**

### **7.1 Interactive Testing**

```python
# test_model_interactive.py
"""
Test fine-tuned PhoBERT on Vietnamese PDPL text
"""

from transformers import pipeline

# Load your trained model
classifier = pipeline(
    'text-classification',
    model='./phobert-pdpl-final',
    tokenizer='./phobert-pdpl-final'
)

# PDPL labels
labels = [
    "Lawfulness",
    "Purpose limitation",
    "Data minimization",
    "Accuracy",
    "Storage limitation",
    "Integrity",
    "Accountability",
    "Data subject rights"
]

# Test examples
test_cases = [
    "Công ty phải thu thập dữ liệu một cách hợp pháp và minh bạch",
    "Dữ liệu chỉ được sử dụng cho mục đích đã thông báo",
    "Chỉ thu thập dữ liệu cần thiết nhất",
    "Dữ liệu phải chính xác và được cập nhật",
    "Không lưu trữ dữ liệu quá lâu",
    "Dữ liệu phải được mã hóa và bảo vệ",
    "Doanh nghiệp chịu trách nhiệm về dữ liệu",
    "Người dùng có quyền xóa dữ liệu cá nhân"
]

print("🧪 Testing PhoBERT on Vietnamese PDPL text:\n")

for text in test_cases:
    result = classifier(text)[0]
    label_id = int(result['label'].split('_')[1])
    confidence = result['score']
    
    print(f"📝 Text: {text}")
    print(f"✅ Category: {labels[label_id]}")
    print(f"📊 Confidence: {confidence:.2%}\n")
```

**Run interactive test:**
```bash
python test_model_interactive.py
```

---

## **Step 8: Use Your Model in VeriAIDPO**

### **8.1 Create Prediction API (Vietnamese-First Bilingual Support)**

```python
# veriaidpo_api.py
"""
VeriAIDPO Compliance Prediction API
Vietnamese-First Design with English Secondary Support

Cultural Context:
- Primary language: Vietnamese (Tiếng Việt)
- Secondary language: English (for international reports)
- Model: PhoBERT (VinAI Research - Vietnamese-optimized)
- Legal framework: PDPL 2025 (Nghị định 13/2023/NĐ-CP)
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class VeriAIDPO:
    def __init__(self, model_path='./phobert-pdpl-final'):
        """Initialize VeriAIDPO compliance classifier"""
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        
        # Vietnamese labels (PRIMARY - default display)
        self.nhan_vi = [
            "Tính hợp pháp, công bằng và minh bạch",
            "Hạn chế mục đích",
            "Tối thiểu hóa dữ liệu",
            "Tính chính xác",
            "Hạn chế lưu trữ",
            "Tính toàn vẹn và bảo mật",
            "Trách nhiệm giải trình",
            "Quyền của chủ thể dữ liệu"
        ]
        
        # English labels (SECONDARY - for international reports)
        self.labels_en = [
            "Lawfulness, fairness and transparency",
            "Purpose limitation",
            "Data minimization",
            "Accuracy",
            "Storage limitation",
            "Integrity and confidentiality",
            "Accountability",
            "Rights of data subjects"
        ]
    
    def du_doan(self, van_ban, ngon_ngu='vi', mien='standard'):
        """
        Dự đoán danh mục tuân thủ PDPL 2025
        (Predict PDPL 2025 compliance category)
        
        Args:
            van_ban (str): Vietnamese text to classify
            ngon_ngu (str): 'vi' for Vietnamese (DEFAULT), 'en' for English labels
            mien (str): Regional variation - 'standard', 'bac', 'trung', 'nam'
        
        Returns:
            dict: Prediction results with Vietnamese-first output
        """
        # Tokenize Vietnamese text
        inputs = self.tokenizer(
            van_ban,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        )
        
        # Predict using PhoBERT
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            xac_suat = torch.softmax(logits, dim=-1)[0]  # probabilities
        
        # Get prediction
        nhan_du_doan = torch.argmax(xac_suat).item()  # predicted label ID
        do_tin_cay = xac_suat[nhan_du_doan].item()  # confidence score
        
        # Select label language (Vietnamese PRIMARY)
        nhan_hien_thi = self.nhan_vi if ngon_ngu == 'vi' else self.labels_en
        
        return {
            'van_ban': van_ban,  # Input text
            'danh_muc': nhan_hien_thi[nhan_du_doan],  # Category (Vietnamese default)
            'danh_muc_tieng_viet': self.nhan_vi[nhan_du_doan],  # Always include Vietnamese
            'category_english': self.labels_en[nhan_du_doan],  # Always include English (secondary)
            'do_tin_cay': do_tin_cay,  # Confidence score
            'mien': mien,  # Regional variation
            'tat_ca_diem': {  # All category scores
                nhan: float(xac_suat_item)
                for nhan, xac_suat_item in zip(nhan_hien_thi, xac_suat)
            }
        }
    
    # English alias for international developers (maps to Vietnamese-first function)
    def predict(self, text, language='vi', region='standard'):
        """English alias for du_doan() - Vietnamese-first prediction"""
        result = self.du_doan(text, ngon_ngu=language, mien=region)
        # Map Vietnamese keys to English for convenience
        return {
            'text': result['van_ban'],
            'category': result['danh_muc'],
            'category_vietnamese': result['danh_muc_tieng_viet'],
            'category_english': result['category_english'],
            'confidence': result['do_tin_cay'],
            'region': result['mien'],
            'all_scores': result['tat_ca_diem']
        }

# Example usage - Vietnamese-First
if __name__ == '__main__':
    veriaidpo = VeriAIDPO()
    
    van_ban_test = "Công ty phải bảo vệ dữ liệu cá nhân một cách an toàn"
    
    # 🇻🇳 Vietnamese output (PRIMARY - default)
    ket_qua_vi = veriaidpo.du_doan(van_ban_test, ngon_ngu='vi')
    print("=== Kết quả tiếng Việt (Mặc định) ===")
    print(f"Văn bản: {ket_qua_vi['van_ban']}")
    print(f"Danh mục: {ket_qua_vi['danh_muc']}")
    print(f"Độ tin cậy: {ket_qua_vi['do_tin_cay']:.2%}\n")
    
    # 🇬🇧 English output (SECONDARY - for international use)
    ket_qua_en = veriaidpo.predict(van_ban_test, language='en')
    print("=== English Output (Secondary) ===")
    print(f"Text: {ket_qua_en['text']}")
    print(f"Category: {ket_qua_en['category']}")
    print(f"Confidence: {ket_qua_en['confidence']:.2%}\n")
    
    # 🌏 Regional variation example (Central Vietnam)
    ket_qua_trung = veriaidpo.du_doan(
        "Doanh nghiệp cần bảo đảm dữ liệu được bảo mật",
        ngon_ngu='vi',
        mien='trung'
    )
    print("=== Miền Trung (Central Vietnam) ===")
    print(f"Văn bản: {ket_qua_trung['van_ban']}")
    print(f"Danh mục: {ket_qua_trung['danh_muc']}")
    print(f"Miền: {ket_qua_trung['mien']}")
    print(f"Độ tin cậy: {ket_qua_trung['do_tin_cay']:.2%}")
```

**📤 Output Example:**
```
=== Kết quả tiếng Việt (Mặc định) ===
Văn bản: Công ty phải bảo vệ dữ liệu cá nhân một cách an toàn
Danh mục: Tính toàn vẹn và bảo mật
Độ tin cậy: 94.32%

=== English Output (Secondary) ===
Text: Công ty phải bảo vệ dữ liệu cá nhân một cách an toàn
Category: Integrity and confidentiality
Confidence: 94.32%

=== Miền Trung (Central Vietnam) ===
Văn bản: Doanh nghiệp cần bảo đảm dữ liệu được bảo mật
Danh mục: Tính toàn vẹn và bảo mật
Miền: trung
Độ tin cậy: 92.15%
```

---

## **🎯 Complete Training Workflow (Quick Reference)**

```bash
# 1. Prepare dataset
# Create data/train.jsonl, data/val.jsonl, data/test.jsonl

# 2. Preprocess (optional but recommended)
python preprocess_dataset.py

# 3. Train PhoBERT
python train_phobert.py

# 4. Evaluate model
python evaluate_model.py

# 5. Test interactively
python test_model_interactive.py

# 6. Use in VeriAIDPO
python veriaidpo_api.py
```

---

## **💡 Tips for Better Results**

### **Dataset Quality (🇻🇳 Vietnamese-First)**
- ✅ **More Vietnamese data = better accuracy** (aim for 2000+ examples)
- ✅ **Balanced classes** (equal examples per 8 PDPL categories)
- ✅ **Real-world Vietnamese legal text** (actual PDPL compliance examples)
- ✅ **Regional diversity** (33% Bắc, 33% Trung, 33% Nam)
- ✅ **Quality over quantity** (500 high-quality > 2000 low-quality)
- ✅ **Vietnamese legal terminology** (use official PDPL 2025 terms)

### **Training Optimization (PhoBERT-Specific)**
- ✅ **Use GPU** (10-20x faster than CPU for training)
- ✅ **Increase epochs** (5-10 epochs for better convergence)
- ✅ **Tune learning rate** (try 1e-5, 2e-5, 3e-5, 5e-5)
- ✅ **Use VnCoreNLP preprocessing** (+7-10% accuracy for Vietnamese)
- ✅ **Batch size optimization** (16-32 for GPU, 4-8 for CPU)
- ✅ **Early stopping** (prevent overfitting on small datasets)

### **Model Improvement (PhoBERT Focus)**
- ✅ **Try PhoBERT-large** (better accuracy, 2x slower, requires more memory)
- ✅ **PhoBERT + VnCoreNLP** (word segmentation improves Vietnamese understanding)
- ✅ **Data augmentation** (Vietnamese paraphrasing, regional variations)
- ✅ **Active learning** (retrain with corrected predictions)
- ✅ **Cross-validation** (test performance across different data splits)
- ✅ **Regional testing** (ensure >85% accuracy for ALL 3 regions)

### **Vietnamese Cultural Best Practices**
- ✅ **Test with all regional variations** (Bắc, Trung, Nam)
- ✅ **Use Vietnamese variable names** (danh_muc, do_tin_cay, van_ban)
- ✅ **Display Vietnamese first** (English secondary in UI)
- ✅ **Vietnamese legal context** (PDPL 2025 Nghị định 13/2023/NĐ-CP)
- ✅ **Native speaker validation** (test with Vietnamese DPO experts)

---

## **📊 Expected Performance**

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| **Training Data** | 500 examples | 1000 examples | 2000+ examples |
| **Accuracy** | 75-80% | 85-90% | 90-95% |
| **Training Time (GPU)** | 10-15 min | 20-30 min | 40-60 min |
| **Inference Speed** | <2 sec | <1 sec | <0.5 sec |

---

## **🚨 Troubleshooting**

### **Issue 1: Out of Memory**
```python
# Solution: Reduce batch size
per_device_train_batch_size=8  # Instead of 16
```

### **Issue 2: Low Accuracy (<70%)**
```python
# Solutions:
1. Add more training data (minimum 1000 examples)
2. Check label quality (are labels correct?)
3. Use VnCoreNLP preprocessing
4. Train for more epochs (10 instead of 5)
```

### **Issue 3: Training Too Slow**
```bash
# Solution: Use GPU or reduce dataset size for testing
# For CPU testing, use smaller dataset (100-200 examples)
```

---

## **✅ Next Steps**

After training your PhoBERT model:

1. ✅ **Test regional variations** (Validate accuracy across Bắc, Trung, Nam)
2. ✅ **Deploy to AWS** (see `VeriAIDPO_ML_AWS_Training_Plan.md` for PhoBERT deployment)
3. ✅ **Integrate with VeriPortal** (Add to Vietnamese-first compliance wizards)
4. ✅ **Continuous learning** (Retrain monthly with regional Vietnamese data)
5. ✅ **A/B testing** (Compare PhoBERT vs baseline accuracy)
6. ✅ **Vietnamese validation** (Test with native DPO speakers from all regions)
7. ✅ **ISO 42001 certification** (Document PhoBERT training process)

---

## **🇻🇳 Vietnamese Cultural Summary**

**This guide implements Vietnamese-first AI for VeriPortal:**

| Aspect | Vietnamese-First Approach |
|--------|---------------------------|
| **Primary Language** | Vietnamese (Tiếng Việt) |
| **Secondary Language** | English (for international developers) |
| **Model** | PhoBERT (VinAI Research - Vietnamese-optimized) |
| **Regional Support** | Bắc (North), Trung (Central), Nam (South) |
| **Legal Framework** | PDPL 2025 (Nghị định 13/2023/NĐ-CP) |
| **Variable Names** | Vietnamese (danh_muc, do_tin_cay, van_ban) |
| **UI Display** | Vietnamese PRIMARY, English SECONDARY |
| **Training Data** | 100% Vietnamese legal text |

**🎯 Key Success Factors:**
- ✅ PhoBERT pre-trained on 20GB Vietnamese text (best accuracy)
- ✅ VnCoreNLP word segmentation (+7-10% accuracy)
- ✅ Regional diversity ensures nationwide coverage
- ✅ Vietnamese-first design aligns with VeriPortal UX
- ✅ Bilingual output supports international compliance reports

---

**Bạn đã sẵn sàng huấn luyện PhoBERT trên dữ liệu PDPL của Việt Nam!** 🚀🇻🇳

**You're now ready to train PhoBERT on your Vietnamese PDPL dataset!** 🚀

---

*Document Version: 2.0 (Vietnamese-First Cultural Update)*
*Last Updated: October 6, 2025*
*Owner: VeriSyntra AI/ML Team*
*Model Focus: PhoBERT (VinAI Research) only*
*Cultural Alignment: Vietnamese PRIMARY, English SECONDARY*
