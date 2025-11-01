# Google Colab Reload Guide - VeriAIDPO Training Notebook

## Overview

The `VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb` notebook has been updated with reload-friendly features to help you continue work after Colab session disconnects.

## What Was Added

### 1. Reload Warning in Title Cell

The first cell now includes a prominent warning about Colab session behavior:

```
IMPORTANT: After Reloading Notebook on Colab

If you're reopening this notebook after a session disconnect:

1. Run the "Quick Reload Status Check" cell below to see what's still in memory
2. Most likely: All variables are lost - you'll need to re-run cells sequentially
3. Alternative: Load saved checkpoints if you have them

Colab does NOT save Python variables between sessions! You must re-run cells to restore state.
```

### 2. Quick Reload Status Check (Cells 2-3)

**Purpose:** Instantly see what's still in memory after reload

**What it checks:**
- PDPL_CATEGORIES (Step 2)
- BUSINESS_CONTEXTS (Step 2)
- registry (Step 2)
- normalizer (Step 3)
- generator (Step 4)
- dataset (Step 5 - 24,000 samples)
- dataset_v11 (Step 7.5 - 26,000 samples)
- train_dataset, val_dataset, test_dataset (Step 7)
- trainer, model (Step 8)

**What it tells you:**
- Which variables are loaded vs missing
- What step to continue from
- Session state recommendation

**Example output:**
```
NOTEBOOK RELOAD STATUS CHECK
======================================================================

MEMORY STATE:
----------------------------------------------------------------------
[OK] PDPL_CATEGORIES      (8 items)           - Step 2: PDPL categories definition
[OK] BUSINESS_CONTEXTS    (135 items)         - Step 2: Business contexts definition
[OK] registry                                 - Step 2: Company registry instance
[OK] normalizer                              - Step 3: Text normalizer instance
[OK] generator                               - Step 4: Dataset generator instance
[--] dataset                                 - Step 5: Base dataset (24,000 samples)
[--] dataset_v11                             - Step 7.5: v1.1 augmented dataset (26,000 samples)

======================================================================
SUMMARY:
  Loaded:  5 variables
  Missing: 7 variables

STATUS: READY FOR DATASET GENERATION
  > Continue from Step 5 (Generate Base Dataset)

======================================================================
```

### 3. Session Persistence Helpers (Cells 4-5)

**Purpose:** Save/load your progress to avoid re-running everything

**Three helper functions:**

#### `save_session_state(checkpoint_name='auto_checkpoint')`

Saves current session state to disk (in `./session_checkpoints/` folder)

**What it saves:**
- All Step 2-7 variables (categories, contexts, registry, normalizer, generator, datasets)
- Does NOT save model/trainer (too large - use Step 8's model checkpoints instead)

**Example usage:**
```python
# After completing Step 5 (takes 15-20 minutes)
save_session_state('after_step5')

# After completing Step 7.5 (v1.1 augmentation)
save_session_state('after_step7_5_complete')
```

**Output:**
```
Saving session state to: ./session_checkpoints/after_step5.pkl
----------------------------------------------------------------------
[OK] Saved: PDPL_CATEGORIES      (8 items)
[OK] Saved: BUSINESS_CONTEXTS    (135 items)
[OK] Saved: registry             
[OK] Saved: normalizer           
[OK] Saved: generator            
[OK] Saved: dataset              (24000 items)
----------------------------------------------------------------------
[OK] Session state saved successfully!
     Checkpoint: ./session_checkpoints/after_step5.pkl
     Variables saved: 6
     File size: 12.45 MB
```

#### `load_session_state(checkpoint_name='auto_checkpoint')`

Restores session state from disk after Colab reload

**Example usage:**
```python
# After Colab reload, restore your progress
load_session_state('after_step5')
```

**Output:**
```
Loading session state from: ./session_checkpoints/after_step5.pkl
----------------------------------------------------------------------
[OK] Restored: PDPL_CATEGORIES      (8 items)
[OK] Restored: BUSINESS_CONTEXTS    (135 items)
[OK] Restored: registry             
[OK] Restored: normalizer           
[OK] Restored: generator            
[OK] Restored: dataset              (24000 items)
----------------------------------------------------------------------
[OK] Session state loaded successfully!
     Variables restored: 6

TIP: Run the 'Quick Reload Status Check' cell above
     to verify what's now in memory
```

#### `list_checkpoints()`

Shows all available checkpoints

**Example usage:**
```python
list_checkpoints()
```

**Output:**
```
Available Session Checkpoints:
======================================================================
Name: after_step5
  Size: 12.45 MB
  Modified: 2025-10-19 14:32:15

Name: after_step7_5_complete
  Size: 13.21 MB
  Modified: 2025-10-19 15:45:30
```

## Recommended Workflow

### First Time Running (Fresh Session)

1. **Run Cell 2** (Quick Reload Status Check)
   - Should show: "STATUS: FRESH SESSION"
   
2. **Run Steps 1-4 sequentially** (15-20 minutes)
   - Step 1: Environment setup
   - Step 2: PDPL categories + company registry
   - Step 3: Text normalizer
   - Step 4: Dataset generator class

3. **Save checkpoint after Step 4**
   ```python
   save_session_state('after_step4_ready')
   ```

4. **Run Step 5** (Generate 24,000 samples - 15-20 minutes)

5. **Save checkpoint after Step 5**
   ```python
   save_session_state('after_step5_dataset_ready')
   ```

6. **Continue with remaining steps...**

### After Colab Disconnect (Reload)

1. **Run Cell 2** (Quick Reload Status Check)
   - Will show what's missing

2. **Option A: Re-run cells sequentially**
   - Start from Step 1 if everything is lost
   - Faster if you only need to re-run a few steps

3. **Option B: Load saved checkpoint**
   ```python
   # See available checkpoints
   list_checkpoints()
   
   # Load the one you need
   load_session_state('after_step5_dataset_ready')
   ```

4. **Verify loaded state**
   - Re-run Cell 2 (Quick Reload Status Check)
   - Should show variables are loaded

5. **Continue from where you left off**

## Best Practices

### Save Checkpoints at These Milestones:

1. **After Step 4** (generator ready)
   - Quick checkpoint, small file (~1 MB)
   - Name: `after_step4_ready`

2. **After Step 5** (base dataset generated)
   - Important checkpoint, 15-20 minutes saved
   - Name: `after_step5_dataset_ready`
   - File size: ~12 MB

3. **After Step 7.5** (v1.1 augmentation complete)
   - Critical checkpoint, saves all dataset work
   - Name: `after_step7_5_v11_ready`
   - File size: ~13 MB

4. **After Step 7** (datasets split)
   - Ready for training checkpoint
   - Name: `after_step7_splits_ready`
   - File size: ~13 MB

### DO NOT Save Checkpoints:

- **After Step 8** (training) - Model is too large (540MB)
  - Use Step 8's built-in model checkpoints instead
  - Model saves to `./VeriAIDPO_Principles_VI_v1/`

### Checkpoint Management:

```python
# Delete old checkpoints to save space
import os
os.remove('./session_checkpoints/old_checkpoint.pkl')

# Or delete all
import shutil
shutil.rmtree('./session_checkpoints')
```

## Important Notes

### What Colab Does NOT Save:

- **Python variables** (dataset, model, etc.)
- **Instance objects** (registry, normalizer, generator)
- **Large dataframes/lists**

### What Colab DOES Save:

- **Files on disk** (JSONL files, model checkpoints, session_checkpoints/)
- **Notebook cell outputs** (visible until cleared)
- **Uploaded files** (in `/content/` for ~12 hours)

### Session Persistence Limitations:

1. **Checkpoint files are stored in Colab's temporary filesystem**
   - Lost if runtime is fully recycled (not just disconnected)
   - Download important checkpoints to your local machine

2. **Large datasets take time to save/load**
   - 24,000 samples (~12 MB) = ~5-10 seconds to save/load
   - 26,000 samples (~13 MB) = ~5-10 seconds to save/load

3. **Model/Trainer not included in checkpoints**
   - Too large (540MB)
   - Use Step 8's automatic model saving instead

## Troubleshooting

### "Checkpoint not found" error

**Cause:** Colab runtime was fully recycled (not just disconnected)

**Solution:**
```python
# Check if checkpoint directory exists
import os
print(os.path.exists('./session_checkpoints'))

# If False, your runtime was recycled - re-run from Step 1
```

### "Cannot pickle object" error

**Cause:** Some objects cannot be serialized (rare)

**Solution:**
- This shouldn't happen with the current notebook
- If it does, skip that variable manually

### Variables still missing after load

**Cause:** Checkpoint was saved before those variables were created

**Solution:**
- Check when checkpoint was created: `list_checkpoints()`
- Load a later checkpoint or re-run missing steps

## Example: Full Workflow with Checkpoints

```python
# === Fresh Session ===

# 1. Check status
# Run Cell 2 (Quick Reload Status Check)

# 2. Run Steps 1-4 (setup)
# Run Cells 6, 9, 11, 13-15

# 3. Save checkpoint
save_session_state('after_step4')

# 4. Generate dataset (Step 5 - 15-20 minutes)
# Run Cell 16

# 5. Save checkpoint
save_session_state('after_step5')

# === Colab Disconnect (Oh no!) ===

# 6. After reload - check status
# Run Cell 2 - shows everything missing

# 7. Load checkpoint
load_session_state('after_step5')

# 8. Verify
# Run Cell 2 - should show dataset loaded

# 9. Continue from Step 6
# Run remaining cells...
```

## Summary

The notebook now has **three layers of reload protection**:

1. **Visual warning** in title cell
2. **Status check** to see what's in memory
3. **Checkpoint system** to save/restore progress

**Time saved:** Up to 30+ minutes if you checkpoint after Step 5 and Step 7.5!

---

**Questions?** Check the cell outputs - they include helpful tips and instructions.
