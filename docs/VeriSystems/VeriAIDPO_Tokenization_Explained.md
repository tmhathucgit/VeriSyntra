# VeriAIDPO - Tokenization Explained
## What Happens When You "Tokenize Datasets"?

### **Executive Summary**

Tokenization converts Vietnamese text into numbers (tokens) that PhoBERT can process. This document explains the tokenization process step-by-step with visual examples.

---

## **🎯 Simple Definition**

**Tokenization** = Converting text into numbers that AI can understand

```
Vietnamese Text  →  [Tokenization]  →  Numbers  →  [PhoBERT]  →  Prediction
"Bảo vệ dữ liệu"                     [1,2,3,4,5]
```

---

## **📖 Real Example: Step-by-Step**

### **Input: Vietnamese PDPL Text**

```json
{
  "text": "Công ty phải bảo vệ dữ liệu cá nhân",
  "label": 5
}
```

### **Step 1: Load PhoBERT Tokenizer**

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
```

**What is a tokenizer?**
- A dictionary that maps Vietnamese words/syllables to numbers
- PhoBERT's tokenizer has ~64,000 Vietnamese words/tokens
- Example: "dữ_liệu" → Token ID 15432

### **Step 2: Tokenize Single Text**

```python
text = "Công ty phải bảo vệ dữ liệu cá nhân"

# Tokenize
result = tokenizer(text)

print(result)
```

**Output:**
```python
{
  'input_ids': [2, 8901, 1234, 5432, 9876, 3210, 15432, 7654, 3456, 3],
  'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}
```

**Explanation:**
- `input_ids`: Vietnamese words converted to numbers
  - `2` = `<s>` (sentence start token)
  - `8901` = "Công"
  - `1234` = "ty"
  - `5432` = "phải"
  - ... (and so on)
  - `3` = `</s>` (sentence end token)

- `attention_mask`: Tells PhoBERT which tokens are real (1) vs padding (0)
  - All `1` means all tokens are real (no padding yet)

---

## **🔢 Visual Breakdown: Token IDs**

### **Before Tokenization:**
```
┌────────────────────────────────────────────────┐
│ Text: "Công ty phải bảo vệ dữ liệu cá nhân"   │
│                                                │
│ PhoBERT cannot read this! ❌                   │
└────────────────────────────────────────────────┘
```

### **After Tokenization:**
```
┌────────────────────────────────────────────────┐
│ Token IDs: [2, 8901, 1234, 5432, 9876, 3210,  │
│             15432, 7654, 3456, 3]             │
│                                                │
│ PhoBERT can read this! ✅                      │
└────────────────────────────────────────────────┘
```

### **Token Mapping Table:**

| Position | Token ID | Vietnamese Word | English Meaning |
|----------|----------|-----------------|-----------------|
| 0 | 2 | `<s>` | Sentence start |
| 1 | 8901 | Công | Company |
| 2 | 1234 | ty | (part of company) |
| 3 | 5432 | phải | must |
| 4 | 9876 | bảo | protect |
| 5 | 3210 | vệ | (part of protect) |
| 6 | 15432 | dữ_liệu | data |
| 7 | 7654 | cá | personal |
| 8 | 3456 | nhân | (part of personal) |
| 9 | 3 | `</s>` | Sentence end |

---

## **📦 Batch Tokenization (Multiple Texts)**

### **Input: Multiple Training Examples**

```python
texts = [
    "Công ty phải bảo vệ dữ liệu",
    "Dữ liệu phải chính xác",
    "Không lưu trữ dữ liệu quá lâu"
]

# Tokenize all at once
result = tokenizer(
    texts,
    padding=True,        # Make all same length
    truncation=True,     # Cut if too long
    max_length=20        # Maximum 20 tokens
)

print(result['input_ids'])
```

**Output:**
```python
[
  [2, 8901, 1234, 5432, 9876, 3210, 15432, 3, 1, 1, 1, 1],  # Text 1 (padded)
  [2, 15432, 5432, 6789, 4321, 3, 1, 1, 1, 1, 1, 1],        # Text 2 (padded)
  [2, 9999, 8888, 7777, 15432, 6666, 5555, 3, 1, 1, 1, 1]   # Text 3 (padded)
]
```

**Notice:**
- All sequences are now **12 tokens long** (same length)
- Short sequences have `1` (padding token) at the end
- All start with `2` (`<s>`) and end with `3` (`</s>`)

---

## **🎨 Padding & Truncation**

### **Problem: Different Length Sequences**

```python
Text 1: "Công ty phải bảo vệ dữ liệu"                    → 8 tokens
Text 2: "Dữ liệu phải chính xác"                         → 6 tokens
Text 3: "Công ty phải tuân thủ Nghị định 13/2023..."    → 25 tokens
```

PhoBERT requires **all inputs same length** (like a table with equal rows).

### **Solution 1: Padding (Add Fake Tokens)**

```python
tokenizer(texts, padding='max_length', max_length=12)
```

**Result:**
```python
Text 1: [2, 8901, 1234, 5432, 9876, 3210, 15432, 3, 1, 1, 1, 1]  ← Added 4 padding
Text 2: [2, 15432, 5432, 6789, 4321, 3, 1, 1, 1, 1, 1, 1]        ← Added 6 padding
Text 3: [2, 8901, 1234, 5432, 9999, 8888, 7777, 6666, 5555, 4444, 3333, 3]  ← Truncated!
                                                                     ↑ Cut here
```

### **Solution 2: Attention Mask (Tell PhoBERT Which Tokens Are Real)**

```python
{
  'input_ids':      [2, 8901, 1234, 3, 1, 1, 1],
  'attention_mask': [1, 1,    1,    1, 0, 0, 0]
                                    ↑ Real  ↑ Padding (ignore)
}
```

- `1` = Real token (PhoBERT pays attention)
- `0` = Padding token (PhoBERT ignores)

---

## **🔧 Tokenization in Training Code**

### **From the Training Guide (Step 4)**

```python
# load_dataset.py
from datasets import load_dataset
from transformers import AutoTokenizer

# Load PhoBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Load your PDPL dataset
dataset = load_dataset('json', data_files={
    'train': 'data/train_preprocessed.jsonl',
    'validation': 'data/val_preprocessed.jsonl',
    'test': 'data/test_preprocessed.jsonl'
})

# Define tokenization function
def tokenize_function(examples):
    """Tokenize Vietnamese text for PhoBERT"""
    return tokenizer(
        examples['text'],        # Vietnamese text
        padding='max_length',    # Pad to max_length
        truncation=True,         # Truncate if too long
        max_length=256           # Maximum 256 tokens
    )

# Apply tokenization to entire dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)
```

### **What Happens:**

**Before tokenization:**
```python
dataset['train'][0]
# Output:
{
  'text': 'Công_ty phải bảo_vệ dữ_liệu cá_nhân',
  'label': 5
}
```

**After tokenization:**
```python
tokenized_dataset['train'][0]
# Output:
{
  'input_ids': [2, 8901, 1234, 5432, 9876, 3210, 15432, 7654, 3456, 3, 1, 1, ...],
  'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, ...],
  'labels': 5  # (renamed from 'label')
}
```

**Key changes:**
- ✅ `text` is now `input_ids` (numbers)
- ✅ Added `attention_mask` (which tokens are real)
- ✅ `label` renamed to `labels` (required by Trainer)

---

## **🧠 Why Tokenization Matters**

### **Without Tokenization:**
```python
# ❌ PhoBERT cannot process raw text
model(text="Công ty phải bảo vệ dữ liệu")  # Error!
```

### **With Tokenization:**
```python
# ✅ PhoBERT processes token IDs
inputs = tokenizer("Công ty phải bảo vệ dữ liệu", return_tensors="pt")
model(**inputs)  # Works! Returns predictions
```

---

## **📊 Tokenization Parameters Explained**

### **Common Parameters:**

| Parameter | What It Does | Example Value |
|-----------|--------------|---------------|
| `padding` | Add fake tokens to make all sequences same length | `'max_length'` |
| `truncation` | Cut sequences if they're too long | `True` |
| `max_length` | Maximum number of tokens | `256` |
| `return_tensors` | Return PyTorch tensors (for model input) | `'pt'` |

### **Example with All Parameters:**

```python
result = tokenizer(
    "Công ty phải bảo vệ dữ liệu cá nhân",
    padding='max_length',     # Pad to 256 tokens
    truncation=True,          # Cut if > 256 tokens
    max_length=256,           # Max 256 tokens
    return_tensors='pt'       # Return PyTorch tensor
)

print(result.keys())
# Output: dict_keys(['input_ids', 'attention_mask'])

print(result['input_ids'].shape)
# Output: torch.Size([1, 256])  ← 1 sequence, 256 tokens
```

---

## **🎯 Real Training Example**

### **Complete Tokenization Workflow:**

```python
# Step 1: Load data
dataset = load_dataset('json', data_files='data/train.jsonl')

# Example data:
# {"text": "Công ty phải bảo vệ dữ liệu", "label": 5}
# {"text": "Dữ liệu phải chính xác", "label": 3}

# Step 2: Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Step 3: Define tokenization function
def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=256
    )

# Step 4: Tokenize entire dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Step 5: Prepare for training
tokenized_dataset = tokenized_dataset.remove_columns(['text'])  # Remove original text
tokenized_dataset = tokenized_dataset.rename_column('label', 'labels')  # Rename label

# Step 6: Now ready for PhoBERT training!
# PhoBERT receives: input_ids + attention_mask → Predicts: label
```

---

## **❓ Common Questions**

### **Q1: Why convert text to numbers?**
**A:** Neural networks (like PhoBERT) can only process numbers, not text. Tokenization is the bridge.

### **Q2: What are Token IDs?**
**A:** Unique numbers assigned to each Vietnamese word/syllable in PhoBERT's vocabulary (64,000 tokens total).

### **Q3: What is padding?**
**A:** Adding fake tokens (ID=1) to make all sequences the same length (required for batch processing).

### **Q4: What is attention_mask?**
**A:** A list of 1s and 0s telling PhoBERT which tokens are real (1) and which are padding (0).

### **Q5: Why max_length=256?**
**A:** PhoBERT can process up to 512 tokens, but 256 is enough for most PDPL compliance text and trains faster.

### **Q6: Can I see the original words from Token IDs?**
**A:** Yes! Use `tokenizer.decode()`:

```python
token_ids = [2, 8901, 1234, 5432, 3]
text = tokenizer.decode(token_ids)
print(text)
# Output: "Công ty phải"
```

---

## **🔍 Visual Summary**

```
┌─────────────────────────────────────────────────────────────┐
│                    TOKENIZATION PROCESS                     │
└─────────────────────────────────────────────────────────────┘

Raw Data (JSONL file):
┌─────────────────────────────────────────────────────────────┐
│ {"text": "Công ty phải bảo vệ dữ liệu", "label": 5}        │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    [TOKENIZATION]
                            ↓
Tokenized Data (Numbers):
┌─────────────────────────────────────────────────────────────┐
│ {                                                           │
│   "input_ids": [2, 8901, 1234, 5432, 9876, 3210, ...],    │
│   "attention_mask": [1, 1, 1, 1, 1, 1, ...],              │
│   "labels": 5                                              │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
                      [PHOBERT MODEL]
                            ↓
Prediction:
┌─────────────────────────────────────────────────────────────┐
│ Category: "Integrity and confidentiality"                  │
│ Confidence: 94.32%                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## **✅ Key Takeaways**

1. ✅ **Tokenization = Text → Numbers** (so AI can read it)
2. ✅ **Token IDs** = Unique numbers for Vietnamese words
3. ✅ **Padding** = Make all sequences same length
4. ✅ **Attention Mask** = Tell AI which tokens are real
5. ✅ **Max Length 256** = Good for PDPL text (not too long)
6. ✅ **Happens automatically** = Just call `tokenizer(text)`

---

## **🚀 Next Steps**

After understanding tokenization:
1. ✅ Read `VeriAIDPO_PhoBERT_Training_Guide.md` (Step 4-5)
2. ✅ Run tokenization on your PDPL dataset
3. ✅ Train PhoBERT with tokenized data
4. ✅ PhoBERT learns to predict compliance categories!

---

**Tokenization is the foundation of PhoBERT training!** 🎯

Without it, PhoBERT cannot read Vietnamese text.
With it, PhoBERT becomes a Vietnamese PDPL compliance expert! 🇻🇳

---

*Document Version: 1.0*
*Last Updated: October 5, 2025*
*Owner: VeriSyntra AI/ML Team*
