# VeriAIDPO Run 3 - Balanced - Complete Results

**Date:** 2025-10-12 00:38:53  
**Status:** COMPLETED  
**Configuration:** Run 4  
**Notebook:** VeriAIDPO_Colab_Training_CLEAN.ipynb

---

## Executive Summary

### Configuration:
- **Model:** PhoBERT-base (vinai/phobert-base, 135M parameters)
- **Dropout:** 0.15
- **Learning Rate:** 8e-05
- **Weight Decay:** 0.005
- **Dataset:** 3486 train / 751 val / 763 test

### Quick Results:
- **Test Accuracy:** 0.00%
- **Status:** NEEDS WORK - Significant improvements required

---

## Step 3.5: Vietnamese Tokenization Diagnostic

### Test Results Summary:

**Test 1: Basic Vietnamese Tokenization**
- PASS: Sample 1: 13/13 known tokens (0% UNK)
- PASS: Sample 2: 12/12 known tokens (0% UNK)
- PASS: Sample 3: 11/11 known tokens (0% UNK)
- **Result:** Vietnamese text properly tokenized into meaningful subwords

**Test 2: Training Data Inspection**
- PASS: First 3 samples tokenized successfully
- PASS: Token counts reasonable (22-35 non-padding tokens)
- PASS: Special tokens correctly added
- PASS: Zero unknown tokens detected

**Test 3: Vocabulary Coverage**
- **Total tokens analyzed:** ~2,942 (from 100 random samples)
- **Unknown tokens:** 0
- **UNK rate:** 0.00%
- **PASS:** PhoBERT tokenizer fully understands Vietnamese text

**Test 4: Label Distribution**
- **Balance ratio:** 1.00 (perfect balance)
- **Distribution:** All 8 categories have 12.5% of samples
- **PASS:** Classes perfectly balanced

**Test 5: Text-Label Consistency**
- PASS: All 8 categories verified
- PASS: Sample texts match category semantics
- PASS: Token lengths diverse (22-35 tokens)

**Overall Diagnostic:** ALL TESTS PASSED
- Tokenization is working perfectly
- Dataset is high quality
- Ready for training

---

## Step 4: Model Configuration & Setup

### Model Loading:
```
Model: vinai/phobert-base
Status: Successfully loaded
Device: cuda
Parameters: 135M
```

### Dropout Configuration:
```python
hidden_dropout_prob = 0.15
attention_probs_dropout_prob = 0.15
classifier_dropout = 0.15
```

**Rationale:** Run 4: overfitting (100% epoch 1)

### Training Hyperparameters:
```python
num_train_epochs = 12
learning_rate = 8e-05  # 80.0e-5
weight_decay = 0.005
warmup_steps = 50
lr_scheduler_type = "SchedulerType.COSINE"
warmup_ratio = 0.1
label_smoothing_factor = 0.0
```

### Batch & Optimization:
```python
per_device_train_batch_size = 8
per_device_eval_batch_size = 16
gradient_accumulation_steps = 2
effective_batch_size = 16
max_grad_norm = 1.0
```

### Dataset Verification:
- **Training samples:** 3486
- **Validation samples:** 751
- **Test samples:** 763
- **Total samples:** 5000

### Trainer Setup:
- PASS: Tokenizer loaded successfully
- PASS: Model moved to GPU (cuda)
- PASS: Datasets tokenized and ready
- PASS: Trainer instance created
- PASS: SmartTrainingCallback configured

**Configuration Status:** All components ready for training

---

## Step 5: Training Results

### Training Progress:

| Epoch | Training Loss | Validation Loss | Accuracy | Precision | Recall | F1 |
|-------|---------------|-----------------|----------|-----------|--------|----|
| 0 | 0.0235 | N/A | N/A | N/A | N/A | N/A |
| 1 | N/A | 0.0038 | 100.00% | 1.000 | 1.000 | 1.000 |

### Training Summary:
- **Total epochs completed:** 1.0
- **Total training steps:** 218
- **Epoch 1 accuracy:** N/A
- **Final accuracy:** 100.00%
- **Early stopping:** Yes (stopped at epoch 1.0/12)

---

## Step 6: Test Set Validation

### Overall Test Performance:
- **Test Accuracy:** 0.00%
- **Precision:** 0.000
- **Recall:** 0.000
- **F1 Score:** 0.000

### Vietnamese Regional Performance:

| Region | Accuracy | Description |
|--------|----------|-------------|
| north | 100.00% | Unknown region |
| central | 100.00% | Unknown region |
| south | 100.00% | Unknown region |

### Production Readiness Assessment:

CRITICAL - SIGNIFICANT IMPROVEMENTS REQUIRED

**Critical Issues:**
- Accuracy too low for any production use
- Model not learning effectively
- Major configuration or data issues

**Immediate Actions:**
- Review training configuration
- Verify data quality and labels
- Consider different model architecture
- See Run 4 recommendations below

**Decision:** Do not proceed to demo

---

## Step 6.5: Test Dataset Diagnostic

### Diagnostic Purpose:
Investigate the 0% test accuracy issue by analyzing test dataset integrity, prediction behavior, and potential root causes.

### Manual Accuracy Verification:
- **Manually calculated accuracy:** 1.0000 (100.00%)
- **Original reported accuracy:** 0.00% (from Step 6)
- **WARNING:** Discrepancy detected between manual and reported accuracy!

### Prediction Analysis:
- **Unique predicted labels:** [tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7)]
- **Unique true labels:** [tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(0), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(1), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(2), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(3), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(4), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(5), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(6), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7), tensor(7)]
- **Prediction diversity:** 763 out of 8 categories predicted

### Per-Category Diagnostic Accuracy:

| Label | Category | Correct/Total | Accuracy |
|-------|----------|---------------|----------|
| 0 | Tính hợp pháp, công bằng và mi... | 95/95 | 100.00% |
| 1 | Hạn chế mục đích... | 96/96 | 100.00% |
| 2 | Tối thiểu hóa dữ liệu... | 96/96 | 100.00% |
| 3 | Tính chính xác... | 95/95 | 100.00% |
| 4 | Hạn chế lưu trữ... | 96/96 | 100.00% |
| 5 | Tính toàn vẹn và bảo mật... | 95/95 | 100.00% |
| 6 | Trách nhiệm giải trình... | 95/95 | 100.00% |
| 7 | Quyền của chủ thể dữ liệu... | 95/95 | 100.00% |

### Model Confidence Analysis:
- **Mean confidence:** 0.9962
- **Median confidence:** 0.9963
- **Min confidence:** 0.9793
- **Max confidence:** 0.9967

### Root Cause Analysis:

**Moderate Performance:** 100.00% accuracy

**Note:** If Step 6 reported 0% but diagnostic shows >100.00%, there may be a calculation error in Step 6.


### Recommended Actions for Run 4:

*Configuration recommendations depend on diagnostic results from Step 6.5*

---

## Analysis & Recommendations

### Training Behavior Analysis:
- **Initial learning:** Epoch 1 accuracy = 0%
- **Final performance:** Epoch 1 accuracy = 100.00%
- **Improvement:** +100.00% across 1 epoch(s)

WARNING: Slow start - Initial accuracy very low - model struggling to learn
WARNING: Rapid learning - May indicate overfitting


### Comparison with Previous Runs:

| Metric | Run 1 | Run 2 | Run 3 | Run 4 (Current) |
|--------|-------|-------|-------|---------------------------|
| **Dropout** | 0.3 | 0.1 | 0.15 | 0.15 |
| **Learning Rate** | 5e-5 | 1e-4 | 8e-05 | 8e-05 |
| **Epoch 1 Acc** | 12.53% | 100% | 100.00% | 100.00% |
| **Final Acc** | 12.53% | N/A | 100.00% | 100.00% |
| **Issue** | Underfitting | Overfitting | Overfitting | TBD |

### Next Steps Checklist:

- [ ] Upload this results file to VeriSyntra repo
- [ ] Update VeriAIDPO_Training_Config_Tracking.md with results
- [ ] Compare training curves across all runs
- [ ] Decide if Run 4 is needed
- [ ] If successful (>75%), prepare for investor demo
- [ ] If unsuccessful (<75%), analyze for Run 4 configuration

---

**Report Generated:** 2025-10-12 00:38:53  
**Configuration:** Run 4 
**Auto-Export:** Enabled  
**Next Action:** Review results and update tracking document
