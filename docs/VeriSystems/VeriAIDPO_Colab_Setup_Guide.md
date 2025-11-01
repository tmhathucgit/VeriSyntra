# VeriAIDPO Training - Google Colab Setup Guide

**Date**: October 18, 2025  
**Notebook**: `VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb`  
**Purpose**: Setup guide for using VeriSyntra backend modules in Google Colab

---

## Overview

This notebook uses **production backend modules** from VeriSyntra instead of duplicating code inline. This ensures training uses the exact same logic as the production API.

---

## Required Files

You need to upload **3 files** from VeriSyntra backend to Google Colab:

### 1. Company Registry Module
**File**: `backend/app/core/company_registry.py`  
**Purpose**: Production CompanyRegistry class  
**Size**: ~20KB  
**Contains**: 
- `CompanyRegistry` class
- `get_registry()` singleton function
- Hot-reload logic
- Search and statistics methods

### 2. PDPL Normalizer Module
**File**: `backend/app/core/pdpl_normalizer.py`  
**Purpose**: Production PDPLTextNormalizer class  
**Size**: ~15KB  
**Contains**:
- `PDPLTextNormalizer` class
- `get_normalizer()` singleton function
- Company name to [COMPANY] token normalization
- Regex pattern building from registry

### 3. Company Registry Data
**File**: `backend/config/company_registry.json`  
**Purpose**: Production company database  
**Size**: ~25KB  
**Contains**: 
- 46+ Vietnamese companies
- 9 industries (banking, tech, retail, telecom, etc.)
- 3 regions (North, Central, South)
- Company aliases for each entry

---

## Setup Method 1: Google Drive (Recommended)

### Step 1: Upload Backend to Google Drive

1. Open Google Drive in browser
2. Create folder structure: `VeriSyntra/backend/`
3. Upload entire `backend` folder from your local VeriSyntra project
4. Verify these files exist in Drive:
   ```
   VeriSyntra/
   └── backend/
       ├── app/
       │   └── core/
       │       ├── company_registry.py
       │       └── pdpl_normalizer.py
       └── config/
           └── company_registry.json
   ```

### Step 2: Update Notebook Path

In Colab notebook, find Step 2 cell and update this line:

```python
# Change this to your Google Drive path
BACKEND_PATH = '/content/drive/MyDrive/VeriSyntra/backend'
```

### Step 3: Mount Drive in Colab

When you run the notebook, it will:
1. Ask permission to mount Google Drive
2. Click "Connect to Google Drive"
3. Select your Google account
4. Grant permissions

**Advantages**:
- ✅ Files persist across Colab sessions
- ✅ Easy to update files in Drive
- ✅ Entire backend folder available
- ✅ Can run multiple notebooks sharing same files

---

## Setup Method 2: Direct Upload to Colab

### Step 1: Open Colab File Browser

1. Open notebook in Google Colab
2. Click the **folder icon** (📁) in left sidebar
3. You'll see `/content/` directory

### Step 2: Create Directory Structure

Click "New folder" and create:
```
/content/
├── app/
│   └── core/
└── config/
```

### Step 3: Upload Files

1. Navigate to `/content/app/core/`
2. Click upload icon
3. Upload `company_registry.py` and `pdpl_normalizer.py`

4. Navigate to `/content/config/`
5. Click upload icon
6. Upload `company_registry.json`

### Step 4: Update Notebook Path

In Step 2 cell, change:

```python
# For direct upload
BACKEND_PATH = '/content'
```

**Advantages**:
- ✅ Faster initial setup
- ✅ No Google Drive required

**Disadvantages**:
- ❌ Files deleted when runtime disconnects
- ❌ Must re-upload each new session

---

## Setup Method 3: GitHub Clone (Advanced)

### Step 1: Clone VeriSyntra Repo in Colab

Add this cell at the beginning:

```python
# Clone VeriSyntra repository
!git clone https://github.com/tmhathucgit/VeriSyntra.git
!ls -la VeriSyntra/backend/
```

### Step 2: Update Notebook Path

```python
BACKEND_PATH = '/content/VeriSyntra/backend'
```

**Advantages**:
- ✅ Always up-to-date with repo
- ✅ Easy to pull latest changes

**Disadvantages**:
- ❌ Requires public repo or GitHub auth
- ❌ Downloads entire repo (may be large)

---

## Verification Checklist

After setup, verify the imports work:

### Check 1: Files Exist

```python
import os

files_to_check = [
    'app/core/company_registry.py',
    'app/core/pdpl_normalizer.py',
    'config/company_registry.json'
]

for file in files_to_check:
    path = os.path.join(BACKEND_PATH, file)
    exists = os.path.exists(path)
    print(f"{'✅' if exists else '❌'} {file}: {'Found' if exists else 'NOT FOUND'}")
```

### Check 2: Imports Work

```python
try:
    from app.core.company_registry import get_registry, CompanyRegistry
    from app.core.pdpl_normalizer import get_normalizer, PDPLTextNormalizer
    print("✅ SUCCESS: All imports working")
except ImportError as e:
    print(f"❌ ERROR: {e}")
```

### Check 3: Registry Loaded

```python
registry = get_registry()
stats = registry.get_statistics()

print(f"\nCompany Registry Statistics:")
print(f"  Total Companies: {stats['total_companies']}")
print(f"  Industries: {len(stats['industries'])}")
print(f"  Regions: {len(stats['regions'])}")

if stats['total_companies'] >= 40:
    print("\n✅ SUCCESS: Production registry loaded")
else:
    print(f"\n❌ WARNING: Only {stats['total_companies']} companies loaded")
```

### Check 4: Normalizer Works

```python
normalizer = get_normalizer()
test = "Vietcombank can thu thap du lieu hop phap."
result = normalizer.normalize_text(test)

print(f"\nOriginal: {result.original_text}")
print(f"Normalized: {result.normalized_text}")

if '[COMPANY]' in result.normalized_text:
    print("✅ SUCCESS: Normalizer working correctly")
else:
    print("❌ ERROR: Normalization failed")
```

---

## Troubleshooting

### Issue 1: "No module named 'app'"

**Cause**: `BACKEND_PATH` not in Python path  
**Solution**: 
```python
import sys
sys.path.insert(0, BACKEND_PATH)
```

### Issue 2: "FileNotFoundError: company_registry.json"

**Cause**: JSON file not in correct location  
**Solution**: 
- Check file is in `backend/config/company_registry.json`
- Verify `BACKEND_PATH` points to `backend` directory (not `backend/app`)

### Issue 3: "ModuleNotFoundError: No module named 'google.colab'"

**Cause**: Notebook not running in Colab (running locally)  
**Solution**: 
- Comment out the `drive.mount()` line
- Use direct file paths instead

### Issue 4: "Only X companies loaded" (less than 40)

**Cause**: Wrong JSON file or corrupted upload  
**Solution**:
- Re-upload `company_registry.json`
- Verify JSON is valid (check for syntax errors)
- Make sure uploading the correct file from `backend/config/`

---

## File Locations Reference

### Local VeriSyntra Project Structure
```
VeriSyntra/
└── backend/
    ├── app/
    │   ├── __init__.py
    │   └── core/
    │       ├── __init__.py
    │       ├── company_registry.py    ← Upload this
    │       └── pdpl_normalizer.py     ← Upload this
    └── config/
        └── company_registry.json      ← Upload this
```

### Google Colab Structure (Method 1 - Drive)
```
/content/drive/MyDrive/VeriSyntra/
└── backend/
    ├── app/
    │   └── core/
    │       ├── company_registry.py
    │       └── pdpl_normalizer.py
    └── config/
        └── company_registry.json
```

### Google Colab Structure (Method 2 - Direct)
```
/content/
├── app/
│   └── core/
│       ├── company_registry.py
│       └── pdpl_normalizer.py
└── config/
    └── company_registry.json
```

---

## Why This Matters

### Production Parity

**Training Code = Production Code**

When you use the backend modules directly:
- ✅ Model trains with **exact same** company registry as API
- ✅ Normalization logic is **identical** in training and inference
- ✅ No "it worked in training but fails in production" issues
- ✅ Hot-reload works: add company to registry → API uses it immediately (no retrain)

### Example: Adding a New Company

**Traditional Approach** (hardcoded):
```python
# ❌ Must update code and retrain model
companies = ['Vietcombank', 'FPT', 'Shopee']  # Add new company here
# → Train new model → Deploy new model
```

**VeriSyntra Approach** (dynamic):
```python
# ✅ Just update registry JSON
# 1. Add to backend/config/company_registry.json
# 2. API hot-reloads automatically
# 3. Model works with new company (already normalized to [COMPANY])
# → No retraining needed!
```

---

## Best Practices

### 1. Use Google Drive for Long Training Sessions

Google Colab disconnects after 12 hours of inactivity. If using direct upload:
- Files are lost on disconnect
- Must re-upload to resume

With Google Drive:
- Files persist across sessions
- Just reconnect and continue

### 2. Version Control Your Registry

Keep `company_registry.json` in version control:
- Track when companies are added
- Maintain history of changes
- Easy to roll back if needed

### 3. Test Imports Before Training

Always run verification checks before starting 2-3 day training:
- Verify all 3 files uploaded
- Check imports work
- Test registry has 46+ companies
- Confirm normalizer produces [COMPANY] tokens

### 4. Backup Training Checkpoints

Enable checkpoint saving in training args:
```python
TrainingArguments(
    save_steps=500,
    save_total_limit=3
)
```

This way if Colab disconnects, you don't lose all progress.

---

## Quick Start Summary

### 5-Minute Setup (Google Drive Method)

1. **Upload to Drive** (2 min)
   - Upload `backend/` folder to Google Drive

2. **Open Notebook** (1 min)
   - Open in Google Colab Pro+

3. **Update Path** (30 sec)
   - Change `BACKEND_PATH` to your Drive location

4. **Run Verification** (1 min)
   - Run Step 2 cell
   - Check all imports work
   - Verify 46+ companies loaded

5. **Start Training** (30 sec)
   - Run all cells in order
   - Monitor GPU usage

**Total**: 5 minutes to production-ready training setup!

---

## Support

If you encounter issues:

1. Check this guide's **Troubleshooting** section
2. Verify **File Locations Reference** matches your setup
3. Run **Verification Checklist** to diagnose
4. Check Colab logs for specific error messages

---

**Guide Version**: 1.0  
**Last Updated**: October 18, 2025  
**Notebook**: VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb
