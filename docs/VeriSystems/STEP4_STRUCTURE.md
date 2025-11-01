# Step 4 Structure - Quick Reference

## Overview
Step 4 builds the dataset generator in 3 logical parts. **All 3 parts must be executed in order.**

---

## Step 4.1: Define VietnameseDatasetGenerator Class

**Cell Type:** Code  
**Execution Time:** Instant (~1 second)  
**What it does:**
- Defines the `VietnameseDatasetGenerator` class structure
- Loads distinctive vocabulary:
  - CAT2_DISTINCTIVE_PHRASES: 18 markers for Data Minimization (quantity/amount focus)
  - CAT6_DISTINCTIVE_PHRASES: 24 markers for Accountability (proof/reporting focus)
- Adds helper methods:
  - `_get_company_by_region_industry()`: Smart company selection
  - `_generate_template()`: Template generation with 60% distinctive vocabulary injection
  - `_check_data_leak()`: Multi-layer leak detection (template + normalized text tracking)

**Output:** Class definition created (no object yet)

---

## Step 4.2: Add Generation Methods

**Cell Type:** Code  
**Execution Time:** Instant (~1 second)  
**What it does:**
- Adds `generate_sample()` method:
  - Creates individual PDPL compliance samples
  - Uses distinctive vocabulary for Cat 2 and Cat 6
  - Implements relaxed leak detection (3x duplicates allowed, 95%+ uniqueness)
  - Increased max_attempts from 50 to 100 for v1.1 larger dataset
  - Raises RuntimeError if all attempts fail (prevents infinite loop)
- Adds `generate_contrastive_pairs()` method:
  - Creates minimal pairs for Cat 1/2 confusion (Purpose vs Data Minimization)
  - Creates minimal pairs for Cat 0/6 confusion (Transparency vs Accountability)
  - 8 template pairs per confusion set
  - All marked as VERY_HARD ambiguity

**Output:** Methods bound to class (still no object)

---

## Step 4.3: Create Generator Instance (REQUIRED)

**Cell Type:** Code  
**Execution Time:** Instant (~1 second)  
**What it does:**
- **CRITICAL:** Creates the actual `generator` object
- Validates all prerequisites:
  - PDPL_CATEGORIES (from Step 2)
  - BUSINESS_CONTEXTS (from Step 2)
  - registry (from Step 2)
  - normalizer (from Step 3)
  - VietnameseDatasetGenerator class (from Steps 4.1-4.2)
- Instantiates generator with all dependencies
- Verifies generator is ready with stats:
  - Number of companies available
  - Number of PDPL categories
  - Number of business contexts
  - Tracking status (templates, normalized texts, company usage)

**Output:** Working `generator` object ready for Step 5

**WARNING:** If you skip this cell, Step 5 will fail with:
```
NameError: name 'generator' is not defined
```

---

## Execution Checklist

Before running Step 5, verify you've run:

- [ ] Cell 3 (Step 1): Environment setup
- [ ] Cell 5 (Step 2): Registry + categories
- [ ] Cell 7 (Step 3): Normalizer
- [ ] Cell 9 (Step 4.1): Define generator class
- [ ] Cell 11 (Step 4.2): Add methods
- [ ] Cell 13 (Step 4.3): **Create generator instance** [CRITICAL]

Then run the prerequisites check cell to verify all 5 objects are loaded.

---

## Why 3 Parts?

**Educational Value:**
- Part 1: Shows class architecture
- Part 2: Shows generation logic
- Part 3: Shows instantiation

**Debugging Flexibility:**
- If instance gets corrupted, just re-run Part 3
- If methods need modification, re-run Part 2 + Part 3
- If class structure changes, re-run all 3 parts

**Cell Size Management:**
- Total: ~820 lines of code
- Split into manageable chunks (488 + 273 + 59 lines)
- Easier to navigate in Colab

**Error Recovery:**
- Clear separation between definition and instantiation
- Can re-run just the failing part
- Reduces re-execution time during debugging

---

## Common Issues

**Issue:** Step 5 fails with "generator not defined"  
**Solution:** Run Step 4.3 (the cell was likely skipped)

**Issue:** Step 4.3 fails with "PDPL_CATEGORIES not defined"  
**Solution:** Run Step 2 first

**Issue:** Step 4.3 fails with "registry not defined"  
**Solution:** Run Step 2 first

**Issue:** Step 4.3 fails with "normalizer not defined"  
**Solution:** Run Step 3 first

---

## Quick Summary

```
Step 4.1: Define class        [Class exists]
Step 4.2: Add methods          [Methods exist]
Step 4.3: Create instance      [Generator object exists] <- REQUIRED for Step 5
```

All 3 parts take ~3 seconds total to execute.
