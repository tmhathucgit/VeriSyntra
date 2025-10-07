# 🔧 Google Colab Troubleshooting Guide

**VeriAIDPO Bilingual Training Pipeline**

---

## 🚨 Common Errors & Solutions

### 1. **VnCoreNLP Connection Error**

#### Error Message:
```
ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=39215): Max retries exceeded with url: /annotators 
(Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x79b447057500>: 
Failed to establish a new connection: [Errno 111] Connection refused'))
```

#### Cause:
VnCoreNLP requires a Java server to be running, but it's failing to start in Google Colab's environment.

#### Solution (Already Fixed in Updated Notebook):
The updated Step 3 now includes:
1. **Automatic retry** with alternative port (9000)
2. **Fallback mode** - Uses simple preprocessing if VnCoreNLP fails
3. **Better error messages** - Shows what's happening

#### Manual Fix (If Using Old Notebook):
Replace Step 3 cell with this code:

```python
print("="*70)
print("STEP 3: BILINGUAL TEXT PREPROCESSING (+7-10% Accuracy for Vietnamese)")
print("="*70 + "\n")

from vncorenlp import VnCoreNLP
import json
import re
from tqdm.auto import tqdm
import os
import time

print("🔧 Initializing VnCoreNLP for Vietnamese...")

# Check if JAR file exists
if not os.path.exists('./VnCoreNLP-1.2.jar'):
    print("❌ VnCoreNLP-1.2.jar not found!")
    raise FileNotFoundError("Please ensure VnCoreNLP JAR was downloaded in Step 1")

# Initialize VnCoreNLP with proper error handling for Colab
try:
    print("   Starting VnCoreNLP server (this may take 10-15 seconds)...")
    annotator = VnCoreNLP("./VnCoreNLP-1.2.jar", annotators="wseg", max_heap_size='-Xmx2g')
    
    # Test the connection
    time.sleep(2)  # Give server time to fully start
    test_result = annotator.tokenize("Thử nghiệm")
    print("✅ VnCoreNLP ready and tested successfully!\n")
    
except Exception as e:
    print(f"⚠️  VnCoreNLP initialization error: {e}")
    print("   Attempting alternative initialization...")
    
    try:
        # Try with different port
        annotator = VnCoreNLP("./VnCoreNLP-1.2.jar", annotators="wseg", max_heap_size='-Xmx2g', port=9000)
        time.sleep(3)
        test_result = annotator.tokenize("Thử nghiệm")
        print("✅ VnCoreNLP ready (using alternative port)!\n")
    except Exception as e2:
        print(f"❌ Failed to initialize VnCoreNLP: {e2}")
        print("   Falling back to simple preprocessing for Vietnamese...")
        annotator = None

def segment_vietnamese(text):
    """Vietnamese word segmentation with VnCoreNLP"""
    if annotator is None:
        # Fallback: simple preprocessing if VnCoreNLP failed
        return text.lower().strip()
    
    try:
        segmented = annotator.tokenize(text)
        return ' '.join(['_'.join(sentence) for sentence in segmented])
    except Exception as e:
        return text

def preprocess_english(text):
    """English text preprocessing (simple cleaning)"""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ... (rest of preprocessing code)
```

#### Impact if VnCoreNLP Fails:
- ✅ **Training will still work** (fallback mode)
- ⚠️  **Vietnamese accuracy may drop 5-7%**
  - Expected: 88-92% with VnCoreNLP
  - Expected: 81-85% without VnCoreNLP
- ✅ **English accuracy unaffected** (85-88%)

#### Alternative Workaround:
If you keep getting this error, you can **skip Vietnamese word segmentation**:
1. Comment out VnCoreNLP initialization
2. Use simple preprocessing for both languages
3. Accept 5-7% lower Vietnamese accuracy for the demo

---

### 2. **GPU Not Available**

#### Error Message:
```
RuntimeError: GPU not available
```

#### Solution:
1. Click **Runtime** → **Change runtime type**
2. Set **Hardware accelerator** to **GPU** (T4)
3. Click **Save**
4. Re-run all cells

#### Verification:
Step 1 should show:
```
✅ GPU Detected:
   GPU: Tesla T4
```

---

### 3. **Out of Memory (VRAM)**

#### Error Message:
```
CUDA out of memory. Tried to allocate X.XX GiB
```

#### Solution:
Reduce batch size in Step 5:

```python
training_args = TrainingArguments(
    # ... other params ...
    per_device_train_batch_size=16,   # Reduce from 32 to 16
    per_device_eval_batch_size=32,    # Reduce from 64 to 32
)
```

#### Trade-off:
- ✅ Fits in memory
- ⚠️  Training time increases ~25% (25-40 minutes instead of 20-35)

---

### 4. **Training Takes Too Long (>45 minutes)**

#### Possible Causes:
1. Colab GPU is slow/shared
2. Batch size too small
3. Too many epochs

#### Solutions:

**Option 1: Restart Runtime**
```
Runtime → Restart runtime → Run all cells again
```

**Option 2: Reduce Epochs**
```python
training_args = TrainingArguments(
    num_train_epochs=3,  # Reduce from 5 to 3
)
```
Trade-off: 2-3% lower accuracy

**Option 3: Use Colab Pro**
- Faster GPUs (V100/A100)
- Training time: 10-15 minutes

---

### 5. **Dataset Upload Fails**

#### Error Message:
```
FileNotFoundError: data/train.jsonl not found
```

#### Solution:
Verify files uploaded correctly:
```python
!ls -lh data/
```

Should show:
```
train.jsonl
val.jsonl
test.jsonl
```

If missing, re-upload:
1. Choose option 2 in Step 2
2. Upload each file separately
3. Verify with `!ls -lh data/`

---

### 6. **"Language Field Not Found" in Step 6**

#### Message:
```
ℹ️  Vietnamese-only dataset detected (no 'language' field)
```

#### Cause:
You uploaded a Vietnamese-only dataset without `language` field.

#### Solution:

**Option 1: Regenerate with Bilingual Flag**
```bash
# On your local machine
python VeriAIDPO_MVP_QuickStart.py --synthetic_only --synthetic_samples 6000 --bilingual --output_dir vietnamese_pdpl_bilingual
```
Then upload the new files.

**Option 2: Accept Vietnamese-Only Mode**
- Step 6 will show regional validation only
- No English metrics
- Still works fine for Vietnamese-only demo

---

### 7. **Model Download Fails**

#### Error Message:
```
Failed to download phobert-pdpl-final.zip
```

#### Solution:

**Option 1: Save to Google Drive**
```python
# In Step 7, before download
from google.colab import drive
drive.mount('/content/drive')

!cp phobert-pdpl-final.zip /content/drive/MyDrive/
print("✅ Model saved to Google Drive!")
```

**Option 2: Download Manually**
1. Click **Files** tab (left sidebar)
2. Find `phobert-pdpl-final.zip`
3. Right-click → Download

---

### 8. **"Killed" Message During Training**

#### Error Message:
```
Killed
```

#### Cause:
Colab ran out of RAM (not VRAM).

#### Solution:

**Option 1: Reduce Dataset Size**
In Step 2, change:
```python
num_samples = 3000  # Reduce from 5000
```

**Option 2: Reduce Batch Size & Workers**
```python
training_args = TrainingArguments(
    per_device_train_batch_size=16,
    dataloader_num_workers=0,  # Reduce from 2
)
```

**Option 3: Restart Runtime**
```
Runtime → Factory reset runtime → Run all cells again
```

---

### 9. **JSON Decode Error in Step 2**

#### Error Message:
```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

#### Cause:
Uploaded JSONL file is corrupted or not in JSONL format.

#### Solution:
Verify file format locally:
```bash
# Each line should be valid JSON
head -n 1 train.jsonl | python -m json.tool
```

Should show structured JSON with fields:
- `text`
- `label`
- `language`
- `category_name_vi`
- `category_name_en`

---

### 10. **VnCoreNLP JAR Not Found**

#### Error Message:
```
FileNotFoundError: VnCoreNLP-1.2.jar not found
```

#### Solution:
Re-run Step 1 to download VnCoreNLP:
```python
!wget -q https://github.com/vncorenlp/VnCoreNLP/raw/master/VnCoreNLP-1.2.jar
!ls -lh VnCoreNLP-1.2.jar  # Verify download
```

Should show ~48MB file.

---

## 🎯 Performance Troubleshooting

### Expected Accuracy Too Low

| Issue | Vietnamese < 85% | English < 80% |
|-------|------------------|---------------|
| **Likely Cause** | VnCoreNLP failed, insufficient training epochs | PhoBERT not ideal for English, small dataset |
| **Quick Fix** | Use fallback mode, increase epochs to 7 | Expected for demo, acceptable 85-88% |
| **Long-term Fix** | Train locally with VnCoreNLP | Post-funding: train separate BERT-EN model |

### Training Time Issues

| Time Range | Status | Action |
|------------|--------|--------|
| **15-25 min** | ✅ Excellent | Normal for Colab GPU |
| **25-35 min** | ✅ Good | Acceptable |
| **35-45 min** | ⚠️ Slow | Reduce batch size or epochs |
| **>45 min** | ❌ Problem | Restart runtime, check GPU allocation |

---

## 📊 Validation Checklist

### Before Training:
- [ ] GPU enabled (Runtime → Change runtime type → GPU)
- [ ] VnCoreNLP JAR downloaded (48MB file)
- [ ] Dataset generated with `language` field
- [ ] All 3 files uploaded (train.jsonl, val.jsonl, test.jsonl)

### During Training:
- [ ] VnCoreNLP initialized successfully (or fallback mode activated)
- [ ] Language distribution shown in Step 3 (VI count, EN count)
- [ ] Training started with GPU (not CPU)
- [ ] Progress bars updating every 50 steps

### After Training:
- [ ] Step 6 shows separate Vietnamese and English metrics
- [ ] Vietnamese accuracy ≥ 85% (target: 88-92%)
- [ ] English accuracy ≥ 80% (target: 85-88%)
- [ ] Model saved to `phobert-pdpl-final/`
- [ ] ZIP file created (~500 MB)

---

## 🆘 Emergency Fixes

### Nuclear Option: Full Reset
```python
# 1. Factory reset runtime
# Runtime → Factory reset runtime

# 2. Clear all outputs
# Edit → Clear all outputs

# 3. Re-run all cells from top
# Runtime → Run all
```

### Skip VnCoreNLP Entirely
If VnCoreNLP keeps failing, modify Step 3:
```python
# Skip VnCoreNLP initialization
annotator = None

# Use simple preprocessing for Vietnamese
def segment_vietnamese(text):
    return text.lower().strip()
```
**Impact**: 5-7% lower Vietnamese accuracy (acceptable for demo)

### Use Vietnamese-Only Dataset
If bilingual generation fails:
1. In Step 2, choose option 1
2. Wait for Vietnamese-only generation
3. Accept regional validation only (no English metrics)
4. Still demonstrates Vietnamese PDPL capability

---

## 📞 Getting Help

### Check These First:
1. **Colab Status**: https://status.cloud.google.com/
2. **GPU Quota**: Runtime → View resources (ensure GPU allocated)
3. **Session Time**: Colab free tier has 12-hour limit

### Debug Information to Collect:
```python
# System info
!nvidia-smi
!free -h
!df -h

# Python packages
!pip list | grep -E "transformers|vncorenlp|datasets"

# Files
!ls -lh
!ls -lh data/
```

### Common Resolution Steps:
1. ✅ Restart runtime (Runtime → Restart runtime)
2. ✅ Clear outputs (Edit → Clear all outputs)
3. ✅ Re-run from Step 1
4. ✅ Check VnCoreNLP fallback activated
5. ✅ Verify GPU still allocated

---

## ✅ Success Indicators

You know everything is working when you see:

**Step 1:**
```
✅ GPU Detected: Tesla T4
✅ VnCoreNLP JAR downloaded
```

**Step 2:**
```
🌏 Generating BILINGUAL synthetic PDPL dataset (70% Vietnamese + 30% English)...
✅ Bilingual synthetic dataset generated: 5000 examples
   Vietnamese (PRIMARY): 3500 (70.0%)
   English (SECONDARY):  1500 (30.0%)
```

**Step 3:**
```
✅ VnCoreNLP ready and tested successfully!
✅ Bilingual preprocessing complete!
   Train: 3500 total (2450 Vietnamese, 1050 English)
💡 Vietnamese texts preprocessed with VnCoreNLP (+7-10% accuracy)
```

**Step 6:**
```
🇻🇳 Vietnamese (PRIMARY):
   Overall Accuracy: 90.5%
   ✅ Vietnamese meets 88%+ target!

🇬🇧 English (SECONDARY):
   Overall Accuracy: 86.3%
   ✅ English meets 85%+ target!

🎉 Both languages meet accuracy targets!
```

---

## 📚 Related Documentation

- **Main Guide**: `VeriAIDPO_Bilingual_QuickStart_Guide.md`
- **Update Summary**: `COLAB_BILINGUAL_UPDATE_COMPLETE.md`
- **Local Script**: `VeriAIDPO_MVP_QuickStart.py`
- **Notebook**: `VeriAIDPO_Google_Colab_Automated_Training.ipynb`

---

**Last Updated**: October 6, 2025  
**Notebook Version**: Bilingual v2.0 with VnCoreNLP Fallback
