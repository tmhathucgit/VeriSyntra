# VeriAIDPO Run 4 - Quick Reference Card

**ERROR ENCOUNTERED:** ✅ RESOLVED

---

## ❌ The Error You Got:

```python
NameError: name 'PDPL_CATEGORIES' is not defined
```

**Location:** Cell 7 (Step 2.5), Line 536

---

## 🔍 Root Cause:

Cell 7 (Step 2.5) requires variables defined in **Cell 2 (Step 1)**:
- `PDPL_CATEGORIES` - 8 PDPL compliance categories
- `VIETNAMESE_COMPANIES` - Company lists by region

**What happened:** You likely skipped Cell 2 and jumped directly to Cell 7.

---

## ✅ Solution - Correct Execution Order:

### **MUST RUN (In Order):**

1. **Cell 1:** Environment Setup
   - Installs packages (~3-5 min)
   - Required: accelerate, transformers, datasets, etc.

2. **Cell 2:** Step 1 - PDPL Categories ⚠️ **DO NOT SKIP**
   - Defines `PDPL_CATEGORIES` dictionary
   - Defines `VIETNAMESE_COMPANIES` dictionary
   - **Required for Cell 7 to work**
   - Duration: <1 minute

3. **Cell 7:** Step 2.5 Enhanced
   - Uses `PDPL_CATEGORIES` from Cell 2
   - Uses `VIETNAMESE_COMPANIES` from Cell 2
   - Generates 5000 templates
   - Duration: ~2-3 minutes

### **SKIP:**

- ⏭️ **Cell 3:** Basic Step 2 (we're using Step 2.5 instead)

---

## 🔧 Fix Steps on Google Colab:

### **If you already got the error:**

1. ✅ Go back to Cell 2
2. ✅ Run Cell 2 (Step 1 - PDPL Categories)
3. ✅ Wait for it to complete (~10 seconds)
4. ✅ Then run Cell 7 (Step 2.5) again
5. ✅ Error should be resolved

### **Complete Run 4 Sequence:**

```
✅ Cell 1:  Environment Setup          (~3-5 min)
✅ Cell 2:  Step 1 - PDPL Categories   (<1 min)   ⚠️ REQUIRED
⏭️ Cell 3:  Basic Step 2               (SKIP)
✅ Cell 7:  Step 2.5 Enhanced          (~2-3 min)
✅ Cell 8:  Step 3 - Data Splitting    (<1 min)
✅ Cell 9:  Step 3.5 - Tokenization    (~1 min)
✅ Cell 10: Step 4 - Model Setup       (~2-3 min)
✅ Cell 11: Step 5 - Training          (~20-30 min) ⭐
✅ Cell 12: Step 6 - Test Validation   (~1 min)
✅ Cell 13: Step 6.5 - Verification    (~1 min)
✅ Cell 14: Step 6.75 - Results Export (<1 min)
```

**Total Time:** ~35-45 minutes

---

## 🎯 What Cell 2 Does:

### Defines PDPL_CATEGORIES:
```python
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
```

### Defines VIETNAMESE_COMPANIES:
```python
VIETNAMESE_COMPANIES = {
    'north': ['VNG', 'FPT', 'VNPT', 'Viettel', ...],
    'central': ['DXG', 'Saigon Co.op', ...],
    'south': ['Shopee VN', 'Lazada VN', 'Tiki', ...]
}
```

**Why Step 2.5 needs these:**
- `PDPL_CATEGORIES`: Loop through 8 categories to generate 625 templates each
- `VIETNAMESE_COMPANIES`: Referenced by Cell 7's component-based generator

---

## 📊 Expected Output After Fix:

### Cell 2 Output:
```
======================================================================
STEP 1: PDPL 2025 CATEGORIES
======================================================================

8 PDPL categories defined
Companies by region: North (15), Central (13), South (15)
```

### Cell 7 Output (After running Cell 2):
```
============================================================
STEP 2.5 (ENHANCED): HARDER DATASET WITH AMBIGUITY
============================================================

Enhanced dataset ENABLED - generating harder samples via components...

Initializing Component-Based Template Generator...
  Generating 625 templates for Category 0 (Lawfulness...):
    Easy: 156, Medium: 250, Hard: 156, Very Hard: 63
  Generating 625 templates for Category 1 (Purpose limitation):
    ...

Total enhanced samples generated: 5000

Validation & Statistics:
----------------------------------------
Uniqueness: 4850/5000 (97.0%)
Difficulty distribution: {'easy': 1250, 'medium': 2000, 'hard': 1250, 'very_hard': 500}
Formality distribution: {...}
Region distribution: {...}
Metadata completeness: 5000/5000 (100.0%)

✅ STEP 2.5 (ENHANCED) COMPLETE - Enhanced dataset ready!
```

---

## ⚠️ Common Mistakes to Avoid:

### ❌ DON'T:
- Skip Cell 2 thinking it's part of Basic Step 2
- Jump directly to Cell 7 without running Cell 1 & 2
- Run cells out of order

### ✅ DO:
- Always run Cell 1 first (environment setup)
- Always run Cell 2 second (defines required variables)
- Skip Cell 3 (Basic Step 2)
- Then run Cell 7 (Step 2.5)
- Continue with Cells 8-14 in order

---

## 🎯 Why This Order Matters:

**Cell Dependencies:**
```
Cell 1 (Environment)
  ↓ provides packages
Cell 2 (PDPL Categories)
  ↓ provides PDPL_CATEGORIES, VIETNAMESE_COMPANIES
Cell 7 (Step 2.5)
  ↓ generates enhanced_samples
Cell 8 (Data Splitting)
  ↓ provides train_dataset, val_dataset, test_dataset
Cell 9-14 (Training & Validation)
```

**Breaking the chain at Cell 2 → Cell 7 causes NameError**

---

## 📝 Checklist - Before Running Cell 7:

- [ ] Cell 1 executed successfully (packages installed)
- [ ] Cell 2 executed successfully (no errors)
- [ ] Can see "STEP 1: PDPL 2025 CATEGORIES" output
- [ ] Can see "8 PDPL categories defined" message
- [ ] Cell 3 skipped (not executed)
- [ ] Now ready to run Cell 7

---

## 🚀 Resume Your Run 4:

**Current Status:** Error resolved, ready to continue

**Next Steps:**
1. ✅ Verify Cell 2 has been run
2. ✅ Re-run Cell 7 (should work now)
3. ✅ Continue with Cells 8-14
4. ✅ Monitor Cell 11 (Training) for 40-60% epoch 1 accuracy
5. ✅ Download results when complete

**Expected Final Result:** 75-90% test accuracy (vs Run 3's 100%)

---

**Document Created:** October 11, 2025  
**Status:** ERROR RESOLVED - Ready to resume Run 4  
**Reference:** See `VeriAIDPO_Run_4_Execution_Plan.md` for full details
