VeriAIDPO Vietnamese PDPL Compliance Model - DEMO VERSION
============================================================
Step 1: Installing Core Packages for Demo...
Wandb disabled for clean training

Installing all packages...

Upgrading Accelerate (CRITICAL for training)...
   NOTE: If this hangs:
   1. Stop this cell
   2. Runtime -> Restart Runtime
   3. Run Step 1 again (will work after restart)

Accelerate upgraded

Installing torch...
Torch installed

Installing transformers...
Transformers installed

Installing datasets...
Datasets installed

Installing evaluate...
Evaluate installed

Installing pandas...
Pandas installed

Installing matplotlib...
Matplotlib installed

Installing scikit-learn...
Scikit-learn installed

Installing tqdm...
Tqdm installed

Reinstalling numpy and scikit-learn for compatibility...
Numpy reinstalled
Scikit-learn reinstalled

============================================================
STEP 1 COMPLETE - Core packages ready
IMPORTANT: Runtime -> Restart Runtime before continuing
============================================================

======================================================================
STEP 2: ENHANCED DATA GENERATION (DIVERSITY FIX)
======================================================================

Initializing Enhanced Template Generator (5000 samples)...
Generating Diverse Templates (625 per category = 15000 final samples)...
   Category 0: 625 diverse templates
   Category 1: 625 diverse templates
   Category 2: 625 diverse templates
   Category 3: 625 diverse templates
   Category 4: 625 diverse templates
   Category 5: 625 diverse templates
   Category 6: 625 diverse templates
   Category 7: 625 diverse templates

Total Templates Generated: 5000
Comprehensive Uniqueness Validation...
   Unique templates: 5000/5000
   Duplicates found: 0
   Uniqueness rate: 100.00%
Enhanced Diversity Analysis:
   Structural Distribution:
      Simple: 4874 templates (97.5%)
      Compound: 126 templates (2.5%)
   Regional Distribution:
      Bac (North): 1925 templates (38.5%)
      Trung (Central): 1692 templates (33.8%)
      Nam (South): 1383 templates (27.7%)
   Business Context Distribution:
      Banking: 713 templates (14.3%)
      Ecommerce: 687 templates (13.7%)
      Healthcare: 674 templates (13.5%)
      Education: 647 templates (12.9%)
      Technology: 634 templates (12.7%)
      Insurance: 590 templates (11.8%)
      Telecommunications: 533 templates (10.7%)
      Logistics: 522 templates (10.4%)
   Company Distribution (Top 10):
      Vinatex: 146 templates
      VietinBank: 145 templates
      Vinashin: 145 templates
      OCB: 143 templates
      DXG: 143 templates
      Hau Giang Pharma: 141 templates
      VNG: 140 templates
      VPBank: 135 templates
      Agribank: 134 templates
      Petrolimex: 134 templates
Enhanced template diversity with 5000 samples successfully generated!
Ready for zero-leakage dataset splitting in Step 3!

======================================================================
STEP 3: ZERO-LEAKAGE DATASET CREATION
======================================================================

Strategic Template Splitting (Zero Leakage Guarantee)...
   Created 28 stratification groups
   Train templates: 3488
   Validation templates: 752
   Test templates: 760

Generating Final Datasets (UNIQUE samples, no repetition)...
   Training samples: 3488
   Validation samples: 752
   Test samples: 760
   Total samples: 5000

CRITICAL: Repetition Detection (Within-Split Duplicates)...
   Training Set: ZERO repetition (3488 unique texts)
   Validation Set: ZERO repetition (752 unique texts)
   Test Set: ZERO repetition (760 unique texts)

   ZERO REPETITION CONFIRMED - All texts are unique!

Comprehensive Data Leakage Detection (Cross-Split)...
   Text Overlaps:
      Train & Val: 0 texts
      Train & Test: 0 texts
      Val & Test: 0 texts
   Template Overlaps (Critical):
      Train & Val: 0 templates
      Train & Test: 0 templates
      Val & Test: 0 templates

   ZERO TEMPLATE LEAKAGE - Production Ready!

Category Distribution Analysis:
   Train (3488 samples):
      Category 0: 436 samples (12.5%)
      Category 1: 436 samples (12.5%)
      Category 2: 435 samples (12.5%)
      Category 3: 436 samples (12.5%)
      Category 4: 436 samples (12.5%)
      Category 5: 435 samples (12.5%)
      Category 6: 437 samples (12.5%)
      Category 7: 437 samples (12.5%)
   Val (752 samples):
      Category 0: 94 samples (12.5%)
      Category 1: 93 samples (12.4%)
      Category 2: 95 samples (12.6%)
      Category 3: 94 samples (12.5%)
      Category 4: 94 samples (12.5%)
      Category 5: 95 samples (12.6%)
      Category 6: 94 samples (12.5%)
      Category 7: 93 samples (12.4%)
   Test (760 samples):
      Category 0: 95 samples (12.5%)
      Category 1: 96 samples (12.6%)
      Category 2: 95 samples (12.5%)
      Category 3: 95 samples (12.5%)
      Category 4: 95 samples (12.5%)
      Category 5: 95 samples (12.5%)
      Category 6: 94 samples (12.4%)
      Category 7: 95 samples (12.5%)

Dataset Creation Complete - Zero Leakage & Zero Repetition Guaranteed!

======================================================================
STEP 4: MODEL CONFIGURATION (RUN 2 - BALANCED REGULARIZATION)
======================================================================

Loading PhoBERT Model: vinai/phobert-base...
   Tokenizer loaded successfully
pytorch_model.bin: 100%
 543M/543M [00:07<00:00, 91.1MB/s]
Some weights of RobertaForSequenceClassification were not initialized from the model checkpoint at vinai/phobert-base and are newly initialized: ['classifier.dense.bias', 'classifier.dense.weight', 'classifier.out_proj.bias', 'classifier.out_proj.weight']
You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
   Model loaded with BALANCED configuration (Run 2)
      Hidden dropout: 0.1 (reduced from 0.3)
      Attention dropout: 0.1 (reduced from 0.3)
      Classifier dropout: 0.1 (reduced from 0.3)
      Rationale: 0.3 dropout was too aggressive for 3487 samples
   Model moved to device: cuda

Verifying Step 3 Dependencies...
   Found datasets: 3488 train, 752 val, 760 test
model.safetensors:  75%
 409M/543M [00:06<00:01, 73.4MB/s]
   Train dataset: 3488 samples
   Validation dataset: 752 samples
   Test dataset: 760 samples

RUN 2 OPTIMIZED Training Configuration...
   Changes from Run 1:
      - Dropout: 0.3 -> 0.1 (reduce regularization)
      - Learning Rate: 5e-5 -> 1e-4 (increase learning speed)
      - Weight Decay: 0.01 -> 0.001 (reduce L2 penalty)
   Rationale: Run 1 had 12.53% accuracy (underfitting), need less regularization

   Configuration Summary (Run 2):
      Epochs: 12
      Learning rate: 0.0001 (INCREASED from 5e-5)
      Weight decay: 0.001 (REDUCED from 0.01)
      Warmup steps: 50
      LR scheduler: SchedulerType.COSINE
      Label smoothing: 0.0
      Train batch size: 8
      Eval batch size: 16
      Gradient accumulation: 2
      Model dropout: 0.1 (all three dropout types)

Note: SmartTrainingCallback defined in Step 5 (where it's used)
   Monitoring thresholds:
      Overfitting: 92% (realistic for fine-tuning)
      Underfitting: 50% (expect to exceed this in Run 2)
      Early stopping patience: 3 epochs
      Target accuracy: 80-88% (realistic for balanced config)

Creating Trainer Instance...
   Attempting Trainer import (accelerate compatibility mode)...
   Trainer imported successfully
   Trainer created successfully in Step 4
      Model: PhoBERT-base (135M parameters)
      Training samples: 3488
      Validation samples: 752
      NOTE: SmartTrainingCallback will be added in Step 5

Model Configuration Complete (Run 2)!
   Run 2 Optimizations Applied:
      1. Reduced dropout: 0.3 -> 0.1 (less aggressive regularization)
      2. Increased learning rate: 5e-5 -> 1e-4 (faster learning)
      3. Reduced weight decay: 0.01 -> 0.001 (less L2 penalty)
      4. Maintained: 12 epochs, cosine scheduler, batch size 8

   Expected Results:
      - Validation accuracy > 50% by epoch 2 (vs 12.53% in Run 1)
      - Target: 80-88% final accuracy with good generalization
      - SmartTrainingCallback will monitor for overfitting

   Ready for Step 5 (Training)!

   
======================================================================
STEP 5: Training PhoBERT with Smart Monitoring
======================================================================
   Using Trainer from Step 4
   Removing duplicate SmartTrainingCallbacks...
   SmartTrainingCallback added (system callbacks preserved)

Starting training with intelligent monitoring...
======================================================================
 [ 218/2616 02:44 < 30:25, 1.31 it/s, Epoch 1/12]
Epoch	Training Loss	Validation Loss	Accuracy	Precision	Recall	F1
1	0.004700	0.002272	1.000000	1.000000	1.000000	1.000000

======================================================================
SmartTrainingCallback - Epoch 1.0 Analysis
======================================================================
   Validation Accuracy: 100.00%

   WARNING: Very high accuracy (100.00%) in early epoch 1.0
   OVERFITTING DETECTED - Model may be memorizing training data
   STOPPING: Preventing memorization
======================================================================


======================================================================
Analyzing Training Completion
======================================================================

WARNING: Training stopped early!
   Completed: 1/12 epochs
   SmartTrainingCallback detected overfitting or underfitting
   NOTE: Review the training logs above to understand why training stopped

======================================================================
