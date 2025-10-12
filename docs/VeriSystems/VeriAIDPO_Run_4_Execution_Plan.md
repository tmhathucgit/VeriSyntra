# VeriAIDPO Run 4 - Execution Plan

**Date Created:** October 11, 2025  
**Status:** READY TO EXECUTE  
**Objective:** Validate Step 2.5 enhanced dataset achieves realistic 75-85% accuracy

---

## Executive Summary

### What Changed from Run 3:
- **ONLY** dataset source changed (Step 2 → Step 2.5)
- Model configuration **UNCHANGED** (0.15 dropout, 8e-5 LR, 0.005 WD)
- All other parameters **UNCHANGED**
- **Goal:** Isolate dataset difficulty as the variable

### Expected Outcomes:

| Metric | Run 3 (Step 2) | Run 4 Target (Step 2.5) | Improvement |
|--------|----------------|-------------------------|-------------|
| **Epoch 1 Accuracy** | 100% | 40-60% | ✅ Realistic difficulty |
| **Final Accuracy** | 100% (epoch 1) | 75-90% | ✅ Good without overfit |
| **Epochs Completed** | 1 (early stopped) | 5-8 | ✅ Gradual learning |
| **Test Behavior** | Instant memorization | Gradual improvement | ✅ True learning |
| **Generalization** | Poor (100% = overfit) | Good (train/val gap < 10%) | ✅ Better model |

---

## Run 4 Configuration

### Model Configuration (SAME as Run 3):
```python
model_name = "vinai/phobert-base"
hidden_dropout_prob = 0.15
attention_probs_dropout_prob = 0.15
classifier_dropout = 0.15
```

### Training Hyperparameters (SAME as Run 3):
```python
num_train_epochs = 12
learning_rate = 8e-5            # 0.00008
weight_decay = 0.005
warmup_steps = 50
lr_scheduler_type = "cosine"
warmup_ratio = 0.1
label_smoothing_factor = 0.0
per_device_train_batch_size = 8
per_device_eval_batch_size = 16
gradient_accumulation_steps = 2    # Effective batch = 16
max_grad_norm = 1.0
```

### Dataset Configuration (CHANGED from Run 3):

**Run 3 (Basic Step 2):**
- 30 base templates total
- Simple variations: Company × Region × Context
- Uniqueness: ~60%
- Result: 100% accuracy epoch 1 (instant memorization)

**Run 4 (Step 2.5 Enhanced):**
- 625 templates per category (5000 total)
- Component-based: ~150 building blocks → 200,000+ combinations
- Uniqueness: 95-98%
- Anti-leakage: Reserved companies + Similarity detection
- Difficulty stratification:
  - Easy: 25% (simple sentences, single category)
  - Medium: 40% (compound, cross-category keywords)
  - Hard: 25% (questions, negations, conditionals)
  - Very Hard: 10% (cultural conflicts, edge cases)

### Anti-Leakage Mechanisms:

**FIX 1: Complete Metadata**
- All templates have `structure`, `region`, `language` fields
- Ensures Step 3 stratification compatibility

**FIX 2: Reserved Company Sets**
- **30 train/val companies** (never in test set)
  - North: VNG, FPT, VNPT, Viettel, Vingroup, VietinBank, Agribank, BIDV, MB Bank, ACB, VPBank
  - Central: DXG, Saigon Co.op, Central Group, Vinamilk, Hoa Phat, Petrolimex, PVN, EVN, Vinatex
  - South: Shopee VN, Lazada VN, Tiki, Grab VN, MoMo, ZaloPay, Techcombank, VCB, CTG, MSB
- **13 test-only companies** (never in train/val)
  - North: TPBank, Sacombank, HDBank, OCB
  - Central: Vinashin, TNG, DHG Pharma, Hau Giang Pharma
  - South: LienVietPostBank, SeABank, SHB, NamABank, PGBank

**FIX 3: Similarity Detection**
- SequenceMatcher with 85% threshold
- Rejects templates >85% similar to existing ones
- Tracks rejections for monitoring

---

## Execution Steps

### Phase 1: Pre-Execution Setup

**1.1 Verify Notebook Configuration**
- [ ] Open `VeriAIDPO_Colab_Training_CLEAN.ipynb` locally
- [ ] Check Cell 7 (Step 2.5): `USE_ENHANCED_DATASET = True` ✅
- [ ] Check Cell 3 (Basic Step 2): Should be skipped in execution
- [ ] Verify all cells are intact (23 cells total)

**1.2 Google Colab Setup**
- [ ] Go to https://colab.research.google.com
- [ ] Upload `VeriAIDPO_Colab_Training_CLEAN.ipynb`
- [ ] Runtime → Change runtime type → T4 GPU
- [ ] Verify GPU: Run `!nvidia-smi` (should show Tesla T4)

**1.3 Pre-Run Checklist**
- [ ] Colab notebook uploaded
- [ ] T4 GPU connected
- [ ] Cell 7 shows `USE_ENHANCED_DATASET = True`
- [ ] Ready to execute

---

### Phase 2: Execution Sequence

**2.1 Environment Setup (Cell 1)**
```
Expected output:
- All packages installed successfully
- Accelerate upgraded to >=0.25.0
- No errors
Duration: ~3-5 minutes
```

**2.2 PDPL Categories (Cell 2) - REQUIRED FOR STEP 2.5**
```
⚠️ CRITICAL: MUST run this cell before Cell 7 (Step 2.5)
Cell 7 depends on: PDPL_CATEGORIES, VIETNAMESE_COMPANIES

Expected output:
- 8 PDPL categories listed
- Vietnamese companies by region
- No errors
Duration: <1 minute

⚠️ DO NOT SKIP THIS CELL - Cell 7 will fail with NameError if skipped
```

**2.3 Basic Step 2 (Cell 3) - SKIP THIS**
```
Action: Do NOT run Cell 3
Reason: Using Step 2.5 instead
Note: Cell 2 provides variables needed by Cell 7
```

**2.4 Step 2.5 Enhanced (Cell 7) - CRITICAL**
```
Expected output:
- "Enhanced dataset ENABLED" message
- Generation progress for each category
- Statistics:
  * Uniqueness: 95-98%
  * Difficulty distribution: ~25% easy, ~40% medium, ~25% hard, ~10% very hard
  * Formality distribution: formal, business, casual
  * Region distribution: balanced north/central/south
  * Metadata completeness: 100%
- Total: 5000 templates generated
- Some similarity rejections (proves detection working)

Duration: ~2-3 minutes

⚠️ WATCH FOR:
- Uniqueness < 90%: Possible issue with generator
- No similarity rejections: Detection may not be working
- Generation errors: Check component library syntax
```

**2.5 Data Splitting (Cell 8)**
```
Expected output:
- Stratified 70/15/15 split
- Train: ~3500 samples
- Validation: ~750 samples  
- Test: ~750 samples
- All categories balanced

Duration: <1 minute
```

**2.6 Tokenization Diagnostic (Cell 9)**
```
Expected output:
- Test 1-5: ALL PASSED
- UNK rate: 0.00%
- Balance ratio: 1.00
- "Overall Diagnostic: ALL TESTS PASSED"

Duration: ~1 minute

⚠️ IF FAILS: Stop execution, investigate dataset issues
```

**2.7 Model Setup (Cell 10)**
```
Expected output:
- Model loaded: vinai/phobert-base
- Dropout: 0.15, 0.15, 0.15
- LR: 8e-05
- Weight decay: 0.005
- Trainer setup: PASS
- SmartTrainingCallback configured

Duration: ~2-3 minutes
```

**2.8 Training (Cell 11) - MOST CRITICAL**
```
Expected output - Epoch 1:
- Training loss: Should start ~2.0-2.5 (NOT 0.0089 like Run 3)
- Validation accuracy: Target 40-60% (NOT 100%)
- Validation loss: Should be ~0.5-1.5 (NOT 0.0032 like Run 3)

Expected progression:
- Epoch 1: 40-60%
- Epoch 2: 55-70%
- Epoch 3: 65-80%
- Final: 75-90%

Duration: ~20-30 minutes total

⚠️ CRITICAL MONITORING:
- If epoch 1 = 100%: STOP - same issue as Run 3, dataset not working
- If epoch 1 < 30%: Dataset may be too hard
- If early stop epoch 1: Same overfitting issue as Run 3
- Watch for gradual improvement (not sudden jumps to 100%)

✅ SUCCESS INDICATORS:
- Epoch 1: 40-60%
- Gradual improvement each epoch
- Completes 5+ epochs without early stopping
- Final accuracy 75-90%
```

**2.9 Test Validation (Cell 12)**
```
Expected output:
- Test accuracy: Should match validation ±5%
- If validation final = 85%, test should be 80-90%
- Precision/Recall/F1: Should be balanced across categories

Duration: ~1 minute

⚠️ WATCH FOR:
- Test >> Validation: Possible leakage still present
- Test << Validation: Model not generalizing well
```

**2.10 Manual Verification (Cell 13)**
```
Expected output:
- **Dataset Source Detection:** Step 2 (Basic) or Step 2.5 (Enhanced)
- Manual calculation confirms Step 6 results
- Per-category accuracy breakdown
- Confidence analysis (should be varied, not all >99%)

**Step 2.5 Enhanced - Success Indicators:**
- Dataset source: "Step 2.5 (Enhanced)" detected ✅
- Uniqueness: 95-98% ✅
- Difficulty stratification present ✅
- Reserved company sets active ✅
- If accuracy 75-90%: "EXCELLENT - Ready for demo" ✅

**Step 2 Basic - Known Issue:**
- Dataset source: "Step 2 (Basic)" detected ⚠️
- Uniqueness: ~60% (low)
- If accuracy >95%: Confirms overfitting issue
- Recommendation: Switch to Step 2.5 Enhanced

Duration: ~1 minute
```

**2.11 Results Export (Cell 14)**
```
Expected output:
- VeriAIDPO_Run_4_Results.md generated
- Download link appears
- Click to download

Duration: <1 minute
```

---

### Phase 3: Post-Execution Analysis

**3.1 Download Results**
- [ ] Download `VeriAIDPO_Run_4_Results.md` from Colab
- [ ] Move to `C:\Users\Administrator\Downloads\`
- [ ] Run PowerShell: `.\Move-VeriAIDPO-Results.ps1`
- [ ] Verify file moved to `docs\VeriSystems\`

**3.2 Open and Review Results**
- [ ] Open `VeriAIDPO_Run_4_Results.md` in VS Code
- [ ] Check Executive Summary section
- [ ] Review training progression table
- [ ] Analyze confusion matrix
- [ ] Check confidence distribution

**3.3 Run 3 vs Run 4 Comparison**

Create comparison table:

| Metric | Run 3 (Step 2) | Run 4 (Step 2.5) | Change |
|--------|----------------|------------------|--------|
| Epoch 1 Accuracy | 100% | [ACTUAL] | [DELTA] |
| Final Accuracy | 100% | [ACTUAL] | [DELTA] |
| Epochs Completed | 1 | [ACTUAL] | [DELTA] |
| Training Loss (E1) | 0.0089 | [ACTUAL] | [DELTA] |
| Validation Loss (E1) | 0.0032 | [ACTUAL] | [DELTA] |
| Test Accuracy | 100% | [ACTUAL] | [DELTA] |
| Mean Confidence | 99.68% | [ACTUAL] | [DELTA] |
| Early Stop Reason | Overfitting (>92%) | [ACTUAL] | [STATUS] |

**3.4 Decision Matrix**

Based on Run 4 final test accuracy:

**Scenario A: 88-95% (Still Too High)**
- **Diagnosis:** Some leakage remains, but much better than Run 3
- **Action:** Implement optional Fix 4 (reserved contexts)
- **Action:** Implement optional Fix 5 (cross-split similarity check)
- **Expected improvement:** Down to 75-82%
- **Timeline:** Run 5 needed

**Scenario B: 80-88% (SUCCESS - Sweet Spot)**
- **Diagnosis:** ✅ Perfect performance for demonstration
- **Action:** Proceed to demo preparation
- **Action:** Document findings in tracking doc
- **Action:** Prepare investor presentation materials
- **Timeline:** No Run 5 needed, ready for demo

**Scenario C: 70-80% (Good, Slightly Low)**
- **Diagnosis:** Dataset might be slightly too hard
- **Action:** Optional - adjust difficulty distribution (30% easy, 45% medium, 20% hard, 5% very hard)
- **Action:** Acceptable for demo if stable
- **Timeline:** Run 5 optional

**Scenario D: < 70% (Too Hard)**
- **Diagnosis:** Dataset is too difficult
- **Action:** Adjust difficulty distribution:
  - Increase easy: 35%
  - Increase medium: 45%
  - Decrease hard: 15%
  - Decrease very hard: 5%
- **Action:** Review component combinations for overly complex patterns
- **Timeline:** Run 5 required

**Scenario E: Still 100% (Failed)**
- **Diagnosis:** Critical - Step 2.5 not working as intended
- **Action:** Emergency investigation:
  - Check if Step 2.5 actually ran (verify generation logs)
  - Check uniqueness stats (should be 95-98%)
  - Check similarity rejection counts (should be > 0)
  - Investigate reserved company implementation
- **Timeline:** Debug and re-run

---

## Success Criteria Summary

### Must-Have (Blocking Issues if Not Met):
- ✅ Epoch 1 accuracy < 95% (proves dataset is harder)
- ✅ Final accuracy 70-90% (proves realistic difficulty)
- ✅ Completes > 1 epoch (proves not instant overfitting)
- ✅ Test accuracy ≈ Validation accuracy ±10% (proves generalization)

### Should-Have (Optimal Results):
- ✅ Epoch 1 accuracy: 40-60%
- ✅ Final accuracy: 75-88%
- ✅ Completes 5+ epochs
- ✅ Train/Val gap < 10%
- ✅ Confusion matrix shows realistic category confusion
- ✅ Confidence distribution varied (not all >99%)

### Nice-to-Have (Bonus):
- Epoch-by-epoch accuracy follows sigmoid curve
- No early stopping (completes all 12 epochs)
- Per-category accuracy balanced (70-90% for all)
- Regional performance balanced

---

## Troubleshooting Guide

### Issue 0: NameError - 'PDPL_CATEGORIES' is not defined ⚠️ COMMON
**Symptoms:** Cell 7 (Step 2.5) fails with `NameError: name 'PDPL_CATEGORIES' is not defined`
**Diagnosis:** Cell 2 (Step 1) was not executed before Cell 7
**Actions:**
1. **CRITICAL:** You MUST run Cell 2 before Cell 7
2. Cell 2 defines required variables:
   - `PDPL_CATEGORIES` (8 compliance categories)
   - `VIETNAMESE_COMPANIES` (company lists)
3. Correct execution order:
   - Cell 1: Environment Setup ✅
   - **Cell 2: Step 1 (PDPL Categories) ✅ REQUIRED**
   - Skip Cell 3 ⏭️
   - **Cell 7: Step 2.5 ✅ (depends on Cell 2)**
4. Solution: Go back and run Cell 2, then re-run Cell 7
5. **Do NOT skip Cell 2** - it's required for Step 2.5

### Issue 1: Epoch 1 Still 100%
**Symptoms:** Same as Run 3, instant perfect accuracy
**Diagnosis:** Step 2.5 didn't execute properly
**Actions:**
1. Check Colab cell execution order - did you skip Cell 3 and run Cell 7?
2. Check Cell 7 output - did it show "Enhanced dataset ENABLED"?
3. Check uniqueness stats - should be 95-98%, not ~60%
4. Re-run Cell 7, verify output carefully
5. If still failing, download notebook, check `USE_ENHANCED_DATASET` value

### Issue 2: Epoch 1 < 30%
**Symptoms:** Model struggling to learn, very slow progress
**Diagnosis:** Dataset might be too hard
**Actions:**
1. Check difficulty distribution in Cell 7 output
2. Verify very_hard is only ~10%
3. Consider adjusting ratios in next run
4. Check for data quality issues in generated templates

### Issue 3: Test >> Validation (Leakage)
**Symptoms:** Test accuracy significantly higher than validation
**Diagnosis:** Test set leakage still present
**Actions:**
1. Check reserved companies - verify test-only companies
2. Implement optional Fix 4 (reserved contexts)
3. Implement optional Fix 5 (cross-split similarity check)
4. Run 5 needed

### Issue 4: Early Stop Epoch 1 (Overfitting)
**Symptoms:** SmartTrainingCallback stops at epoch 1, >92% accuracy
**Diagnosis:** Dataset still too easy despite Step 2.5
**Actions:**
1. Emergency check: Verify Cell 7 actually generated new templates
2. Check similarity rejection count - should be > 0
3. Investigate component library diversity
4. May need to increase similarity threshold to 90%
5. May need to implement reserved contexts (Fix 4)

### Issue 5: Cell 7 Generation Errors
**Symptoms:** Python errors during template generation
**Diagnosis:** Code issue in component-based generator
**Actions:**
1. Check error message carefully
2. Common issues:
   - Missing imports (SequenceMatcher, random, copy)
   - Reserved company sets malformed
   - Component library syntax errors
3. Use `mcp_pylance_mcp_s_pylanceSyntaxErrors` to validate
4. Fix and re-upload notebook

---

## Timeline Estimate

**Total Execution Time: ~35-45 minutes**

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Upload & Setup | 5 min | 5 min |
| Cell 1 (Environment) | 3-5 min | 8-10 min |
| Cell 2 (Categories) | <1 min | 9-11 min |
| Cell 7 (Step 2.5) | 2-3 min | 11-14 min |
| Cell 8 (Splitting) | <1 min | 12-15 min |
| Cell 9 (Tokenization) | 1 min | 13-16 min |
| Cell 10 (Model Setup) | 2-3 min | 15-19 min |
| **Cell 11 (Training)** | **20-30 min** | **35-49 min** |
| Cell 12 (Test) | 1 min | 36-50 min |
| Cell 13 (Verification) | 1 min | 37-51 min |
| Cell 14 (Export) | <1 min | 38-52 min |
| Download & Analysis | 5-10 min | 43-62 min |

**Total with analysis: ~45-60 minutes**

---

## Next Steps After Run 4

### If Successful (75-88% accuracy):
1. ✅ Update `VeriAIDPO_Training_Config_Tracking.md` with Run 4 results
2. ✅ Mark Run 4 as final configuration for demo
3. ✅ Prepare investor demo materials:
   - Learning curve visualization (Run 3 vs Run 4)
   - Confusion matrix comparison
   - Real-world Vietnamese business examples
   - PDPL compliance categorization showcase
4. ✅ Export final model for VeriSyntra integration
5. ✅ Document deployment instructions

### If Needs Improvement (< 75% or > 88%):
1. Implement optional fixes (Fix 4 & 5)
2. Adjust difficulty distribution
3. Plan Run 5 execution
4. Update tracking document
5. Re-evaluate timeline

---

**Document Status:** READY FOR EXECUTION  
**Last Updated:** October 11, 2025  
**Next Action:** Upload notebook to Google Colab and execute Run 4
