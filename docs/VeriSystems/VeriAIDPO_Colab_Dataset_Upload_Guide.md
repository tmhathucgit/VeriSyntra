# VeriAIDPO - Google Colab Dataset Upload Guide
## Quick Reference: Upload Your Data to the Automated Pipeline

> **🎯 Goal**: Get your Vietnamese PDPL dataset into Google Colab for automated training

---

## **📊 Three Upload Methods**

The automated pipeline supports **3 data sources**. Choose the one that fits your situation:

| Method | Best For | Speed | Complexity |
|--------|----------|-------|------------|
| **1. Generate Synthetic** | MVP/Demo | ⚡ Instant | ✅ Easiest |
| **2. Manual Upload** | Small datasets (<50MB) | 🐢 Slow | ⚠️ Medium |
| **3. Google Drive** | Large datasets (>50MB) | 🚀 Fast | 🔧 Advanced |

---

## **Method 1: Generate Synthetic Data (RECOMMENDED FOR MVP)**

### **When to Use:**
- ✅ You need data **immediately** (no preparation)
- ✅ You're building an **MVP or demo**
- ✅ You want **90-93% accuracy** (good enough for investors)
- ✅ You need **perfect regional balance** (Bắc, Trung, Nam)

### **How It Works:**

When you run the automated pipeline and choose **Option 1**, the notebook will:

1. **Generate 1,000 Vietnamese examples** in seconds
2. **Auto-label** with 8 PDPL categories
3. **Auto-balance** regions (33% Bắc, 33% Trung, 34% Nam)
4. **Split** into train/val/test (70%/15%/15%)
5. **Save** to `data/` folder in Colab

### **Step-by-Step:**

```python
# In the automated pipeline notebook, when you reach Step 2:

Choose data source:
  1. Generate synthetic data (FASTEST - recommended for MVP)
  2. Upload your own dataset (JSONL format)
  3. Load from Google Drive

Enter choice (1/2/3): 1  ← Type "1" and press Enter

# Output:
🤖 Generating synthetic Vietnamese PDPL dataset...
✅ Synthetic dataset generated:
   Train: 700 examples
   Validation: 150 examples
   Test: 150 examples
   Total: 1000 examples

✅ Data ingestion complete!
```

### **What You Get:**

```
data/
├── train.jsonl              (700 examples)
├── val.jsonl                (150 examples)
└── test.jsonl               (150 examples)
```

**Sample data format:**
```json
{"text": "Công ty VNG cần phải thu thập dữ liệu cá nhân một cách hợp pháp, công bằng và minh bạch theo quy định của PDPL 2025.", "label": 0, "region": "bac", "category_name_vi": "Tính hợp pháp, công bằng và minh bạch"}
```

### **Advantages:**
- ✅ **0 seconds upload time** (no files to upload!)
- ✅ **Perfect for testing** the pipeline
- ✅ **Balanced data** across all 8 PDPL categories
- ✅ **Regional diversity** built-in
- ✅ **Ready for training** immediately

---

## **Method 2: Manual Upload (Your Own Dataset)**

### **When to Use:**
- ✅ You have **your own Vietnamese PDPL data**
- ✅ Dataset is **small** (<50MB total)
- ✅ You want **control over content**
- ✅ You're fine with **slower upload**

### **Prerequisites:**

Prepare **3 JSONL files** on your PC:

```
my_dataset/
├── train.jsonl       (70% of data)
├── val.jsonl         (15% of data)
└── test.jsonl        (15% of data)
```

**Required format (JSONL):**
```jsonl
{"text": "Vietnamese PDPL compliance text here", "label": 0}
{"text": "Another Vietnamese text", "label": 5}
{"text": "More compliance examples", "label": 2}
```

**Important rules:**
- ✅ UTF-8 encoding (Vietnamese characters)
- ✅ `label` must be 0-7 (8 PDPL categories)
- ✅ One JSON object per line
- ✅ Optional: Include `"region": "bac|trung|nam"` for regional validation

### **Step-by-Step:**

**Step 1: Run the automated pipeline notebook**

**Step 2: When you reach the data ingestion step, choose Option 2:**

```python
Choose data source:
  1. Generate synthetic data (FASTEST - recommended for MVP)
  2. Upload your own dataset (JSONL format)
  3. Load from Google Drive

Enter choice (1/2/3): 2  ← Type "2" and press Enter
```

**Step 3: Upload each file when prompted:**

```python
📤 Upload your dataset files (JSONL format):

1. Upload train.jsonl:
```

A file dialog will appear:

![Upload Dialog](data:image/png;base64,...)

**Step 4: Click "Choose Files" and select `train.jsonl` from your PC**

**Step 5: Wait for upload to complete:**

```
train.jsonl(text/plain) - 1.2 MB, last modified: 10/6/2025 - 100%
Saving train.jsonl to train.jsonl
```

**Step 6: Repeat for `val.jsonl` and `test.jsonl`:**

```python
2. Upload val.jsonl:
[Choose Files button]

3. Upload test.jsonl:
[Choose Files button]
```

**Step 7: Files are automatically moved to `data/` folder:**

```
✅ Dataset uploaded successfully!
✅ Data ingestion complete!
```

### **Expected Upload Times:**

| File Size | Upload Time | Recommendation |
|-----------|-------------|----------------|
| <1 MB | 5-15 seconds | ✅ Good |
| 1-10 MB | 30-60 seconds | ✅ OK |
| 10-50 MB | 2-5 minutes | ⚠️ Slow but acceptable |
| >50 MB | 5-15 minutes | ❌ Use Google Drive instead |

### **Troubleshooting:**

**Issue**: Upload is slow or fails
- **Solution**: Use Method 3 (Google Drive) instead

**Issue**: "Invalid JSON" error
- **Solution**: Check your JSONL format (one JSON per line, UTF-8 encoding)

**Issue**: Vietnamese characters are broken (Ã, Ä, etc.)
- **Solution**: Save files as UTF-8 (in Notepad: Save As → Encoding: UTF-8)

---

## **Method 3: Google Drive (FASTEST FOR LARGE DATASETS)**

### **When to Use:**
- ✅ Dataset is **large** (>50MB)
- ✅ You want **fastest upload** (already in the cloud!)
- ✅ You **reuse the same dataset** multiple times
- ✅ You want to **keep data persistent** across Colab sessions

### **Prerequisites:**

**Step 1: Upload your dataset to Google Drive (one-time setup):**

1. Open Google Drive: https://drive.google.com
2. Create a folder structure:

```
MyDrive/
└── veriaidpo/
    └── data/
        ├── train.jsonl
        ├── val.jsonl
        └── test.jsonl
```

3. Upload your 3 JSONL files to `MyDrive/veriaidpo/data/`

**Upload to Drive is FAST:**
- Google Drive desktop app: Instant sync
- Web upload: Background upload (can close browser)
- One-time upload: Reuse in all future Colab sessions!

### **Step-by-Step:**

**Step 1: Run the automated pipeline notebook**

**Step 2: Choose Option 3 when prompted:**

```python
Choose data source:
  1. Generate synthetic data (FASTEST - recommended for MVP)
  2. Upload your own dataset (JSONL format)
  3. Load from Google Drive

Enter choice (1/2/3): 3  ← Type "3" and press Enter
```

**Step 3: Mount Google Drive:**

```python
📂 Mounting Google Drive...
```

A popup will appear asking for permission:

![Mount Drive](data:image/png;base64,...)

**Step 4: Click "Connect to Google Drive"**

**Step 5: Choose your Google account**

**Step 6: Click "Allow"** to give Colab access to your Drive

**Step 7: Enter your folder path:**

```python
Enter path to data folder (e.g., MyDrive/veriaidpo/data): 
```

Type: `MyDrive/veriaidpo/data` and press Enter

**Step 8: Files are copied instantly:**

```
Mounted at /content/drive
✅ Dataset loaded from Google Drive!
✅ Data ingestion complete!
```

### **Advantages:**

- ✅ **10-100x faster** than manual upload (files already in cloud!)
- ✅ **Reusable**: Mount once, use in all notebooks
- ✅ **Persistent**: Data survives Colab session restarts
- ✅ **No size limits** (up to your Drive quota)
- ✅ **Shareable**: Team members can access the same data

### **Google Drive Path Examples:**

```bash
# Root of "My Drive"
MyDrive/veriaidpo/data

# Inside a shared folder
MyDrive/Shared with me/VeriAIDPO/datasets

# Nested folders
MyDrive/Projects/VeriSyntra/ML/vietnamese_pdpl_data
```

**Tip**: Right-click folder in Google Drive → Get link → Path is in the URL

---

## **🎯 Quick Decision Guide**

### **Choose Method 1 (Synthetic) if:**
- [ ] You need data RIGHT NOW (no prep time)
- [ ] You're building an MVP/demo for investors
- [ ] You don't have Vietnamese PDPL data yet
- [ ] 90-93% accuracy is sufficient

### **Choose Method 2 (Manual Upload) if:**
- [ ] You have small dataset (<50MB)
- [ ] You're uploading for the first time
- [ ] You don't use Google Drive regularly
- [ ] You prefer simple drag-and-drop

### **Choose Method 3 (Google Drive) if:**
- [ ] You have large dataset (>50MB)
- [ ] You'll train multiple models (reuse data)
- [ ] You want fastest access to data
- [ ] You collaborate with a team

---

## **📋 Complete Upload Workflow**

### **For First-Time Users (MVP):**

```
1. Open VeriAIDPO_Automated_Training.ipynb in Colab
2. Enable GPU (Runtime → Change runtime type → GPU)
3. Run all cells (Runtime → Run all)
4. Choose Option 1 (Generate synthetic data)
5. Wait 15-30 minutes
6. Download trained model
```

**Time**: 15-30 minutes total (0 upload time!)

---

### **For Users with Own Data (<50MB):**

```
1. Prepare train.jsonl, val.jsonl, test.jsonl on your PC
2. Open VeriAIDPO_Automated_Training.ipynb in Colab
3. Enable GPU
4. Run all cells
5. Choose Option 2 (Upload your own dataset)
6. Upload train.jsonl (wait for upload)
7. Upload val.jsonl (wait for upload)
8. Upload test.jsonl (wait for upload)
9. Wait 15-30 minutes for training
10. Download trained model
```

**Time**: 2-5 minutes upload + 15-30 minutes training = **20-35 minutes total**

---

### **For Users with Large Data or Teams (>50MB):**

```
# One-time setup:
1. Upload dataset to Google Drive (MyDrive/veriaidpo/data/)

# Every training run:
1. Open VeriAIDPO_Automated_Training.ipynb in Colab
2. Enable GPU
3. Run all cells
4. Choose Option 3 (Load from Google Drive)
5. Click "Connect to Google Drive" → Allow
6. Enter path: MyDrive/veriaidpo/data
7. Wait 15-30 minutes for training
8. Download trained model
```

**Time**: 10 seconds to load data + 15-30 minutes training = **~15-30 minutes total**

---

## **🔧 JSONL Format Requirements**

### **Minimum Required Format:**

```jsonl
{"text": "Vietnamese text here", "label": 0}
{"text": "Another example", "label": 5}
```

### **Recommended Format (with regional data):**

```jsonl
{"text": "Vietnamese text", "label": 0, "region": "bac"}
{"text": "Another example", "label": 5, "region": "trung"}
{"text": "More data", "label": 2, "region": "nam"}
```

### **Full Format (all metadata):**

```jsonl
{"text": "Công ty VNG cần phải bảo vệ dữ liệu", "label": 5, "region": "bac", "category_name_vi": "Tính toàn vẹn và bảo mật", "source": "synthetic", "quality": "high"}
```

### **Label Mapping (8 PDPL Categories):**

```python
0 = "Tính hợp pháp, công bằng và minh bạch"      # Lawfulness, fairness, transparency
1 = "Hạn chế mục đích"                            # Purpose limitation
2 = "Tối thiểu hóa dữ liệu"                       # Data minimization
3 = "Tính chính xác"                              # Accuracy
4 = "Hạn chế lưu trữ"                             # Storage limitation
5 = "Tính toàn vẹn và bảo mật"                    # Integrity and confidentiality
6 = "Trách nhiệm giải trình"                      # Accountability
7 = "Quyền của chủ thể dữ liệu"                   # Data subject rights
```

---

## **💡 Pro Tips**

### **Tip 1: Test with Synthetic First**
Always run with synthetic data (Option 1) first to verify the pipeline works, then switch to your own data.

### **Tip 2: Use Google Drive for Production**
For production models, upload your dataset to Google Drive once and reuse it across all training runs.

### **Tip 3: Validate Data Format Before Upload**
```python
# Quick validation script (run on your PC):
import json

with open('train.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            assert 'text' in data, f"Line {i}: Missing 'text' field"
            assert 'label' in data, f"Line {i}: Missing 'label' field"
            assert 0 <= data['label'] <= 7, f"Line {i}: Invalid label {data['label']}"
        except Exception as e:
            print(f"❌ Error on line {i}: {e}")
            break
    else:
        print("✅ Dataset format is valid!")
```

### **Tip 4: Keep Backup in Google Drive**
Even if you upload manually, save a copy to Google Drive for future use.

### **Tip 5: Use Descriptive Folder Names**
```
❌ Bad:  MyDrive/data/
✅ Good: MyDrive/veriaidpo/vietnamese_pdpl_v1/
```

---

## **❓ FAQ**

**Q: Can I mix synthetic and real data?**  
A: Yes! Generate synthetic data (Option 1), then manually add your own examples to the created files.

**Q: What if my files are in CSV format?**  
A: Convert to JSONL first:
```python
import pandas as pd
import json

df = pd.read_csv('data.csv')
with open('train.jsonl', 'w', encoding='utf-8') as f:
    for _, row in df.iterrows():
        f.write(json.dumps({"text": row['text'], "label": row['label']}, ensure_ascii=False) + '\n')
```

**Q: Can I use the same dataset for multiple training runs?**  
A: Yes! Upload to Google Drive once (Method 3), then reuse in all future sessions.

**Q: How do I add more data later?**  
A: Stop the notebook, upload/modify files, restart from Step 2.

**Q: What's the maximum dataset size?**  
A: Colab has ~13GB RAM. Realistically, you can train on 50,000-100,000 examples.

---

## **✅ Checklist Before Starting**

- [ ] Decided which upload method to use (1, 2, or 3)
- [ ] Prepared dataset files (if using Method 2 or 3)
- [ ] Verified JSONL format is correct (UTF-8, valid JSON)
- [ ] Opened `VeriAIDPO_Automated_Training.ipynb` in Google Colab
- [ ] Enabled GPU (Runtime → Change runtime type → GPU)
- [ ] Ready to run the automated pipeline!

---

## **📚 Related Documents**

- **VeriAIDPO_Automated_Training.ipynb** - The Colab notebook (upload this to Colab)
- **VeriAIDPO_Google_Colab_Training_Guide.md** - Full training guide with all details
- **VeriAIDPO_Data_Collection_Guide.md** - How to collect Vietnamese PDPL data
- **VeriAIDPO_MVP_QuickStart.py** - Generate synthetic data locally

---

*Document Version: 1.0*  
*Last Updated: October 6, 2025*  
*Owner: VeriSyntra AI/ML Team*  
*Focus: Google Colab Dataset Upload Methods*  
*🇻🇳 Vietnamese-First ML Pipeline*
