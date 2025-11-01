# Strategy C Implementation Guide

## Overview

**Goal:** Regenerate dataset with stricter leak detection to achieve 90%+ uniqueness and <5% data leakage

**Timeline:** 30 minutes total
- Code modifications: 5 minutes
- Step 5 execution: 20-25 minutes  
- Step 6-7 execution: 5 minutes

**Expected Outcomes:**
- Base dataset uniqueness: 84% -> 90%+
- v1.1 dataset uniqueness: 59% -> 88%+
- Data leakage: 54% -> <5%
- Production accuracy: Reliable metrics (validation = production)

---

## Code Changes Required

### Change 1: Expand Distinctive Vocabulary (Step 4)

**Current State:**
```python
CAT2_DISTINCTIVE_PHRASES = {
    # 25 markers total
}

CAT6_DISTINCTIVE_PHRASES = {
    # 24 markers total
}
```

**Target State:**
```python
CAT2_DISTINCTIVE_PHRASES = {
    # 50 markers total (double current)
    # Add more QUANTITY/AMOUNT phrases
}

CAT6_DISTINCTIVE_PHRASES = {
    # 50 markers total (double current)
    # Add more PROOF/REPORTING phrases
}
```

**Implementation:**
- Expand each sub-category within Cat 2 and Cat 6
- Maintain Vietnamese cultural context
- Add regional variations (North/Central/South)

---

### Change 2: Expand Business Contexts (Step 2)

**Current State:**
```python
BUSINESS_CONTEXTS = {
    0: [list of ~6 phrases],
    1: [list of ~6 phrases],
    2: [list of ~6 phrases],
    # ... etc (~30 total phrases)
}
```

**Target State:**
```python
BUSINESS_CONTEXTS = {
    0: [list of ~12 phrases],
    1: [list of ~12 phrases],
    2: [list of ~12 phrases],
    # ... etc (~60 total phrases)
}
```

**Implementation:**
- Double context phrases per category
- Add industry-specific variations
- Include regional business terminology

---

### Change 3: Strict Leak Detection (Step 4)

**Current Code:**
```python
def _check_data_leak(self, sample_text: str, template_signature: str) -> bool:
    """Check if sample creates data leak
    
    Relaxed leak detection for v1.1:
    - Allows up to 3 occurrences of same normalized text (95%+ uniqueness)
    """
    normalized = self.normalizer.normalize_text(sample_text).normalized_text
    
    current_count = self._normalized_counts.get(normalized, 0)
    
    # Allow up to 3 occurrences of same normalized text
    if current_count >= 3:
        return True  # LEAK DETECTED
    
    self._normalized_counts[normalized] = current_count + 1
    self.generated_samples.add(normalized)
    
    return False
```

**Modified Code:**
```python
def _check_data_leak(self, sample_text: str, template_signature: str) -> bool:
    """Check if sample creates data leak
    
    STRICT leak detection for production (90%+ uniqueness):
    - Allows ONLY 1 occurrence of same normalized text
    - Prevents exact template duplication
    - Requires expanded template diversity
    """
    normalized = self.normalizer.normalize_text(sample_text).normalized_text
    
    # Track template signature
    self.generated_templates.add(template_signature)
    
    current_count = self._normalized_counts.get(normalized, 0)
    
    # STRICT: Allow only 1 occurrence (changed from 3)
    if current_count >= 1:
        return True  # LEAK DETECTED - duplicate not allowed
    
    self._normalized_counts[normalized] = current_count + 1
    self.generated_samples.add(normalized)
    
    return False
```

**Changes:**
- Threshold: `>= 3` -> `>= 1`
- Docstring updated to reflect strict mode
- Comment clarifies change from relaxed mode

---

### Change 4: Expand Template Structures (Step 4)

**Current Code:**
```python
def _generate_template(self, category_id: int, context: str, company: str) -> str:
    # 4 structure types: active, passive, conditional, inverted
    structures = ['active', 'passive', 'conditional', 'inverted']
    structure = random.choice(structures)
    
    # 4 templates per structure = 16 base templates per category
    if structure == 'active':
        templates = [
            f"{company} chi thu thap {context} thuc su can thiet.",
            f"{prefix} {company} tranh thu thap {context} du thua.",
            f"{company} khong {random.choice(actions)} {context} khong can thiet.",
            f"{company} han che viec thu thap {context} o muc toi thieu.",
        ]
```

**Modified Code:**
```python
def _generate_template(self, category_id: int, context: str, company: str) -> str:
    # 8 structure types (doubled from 4)
    structures = [
        'active', 'passive', 'conditional', 'inverted',
        'declarative', 'imperative', 'interrogative', 'comparative'
    ]
    structure = random.choice(structures)
    
    # 8 templates per structure = 64 base templates per category
    if structure == 'active':
        templates = [
            # Original 4 templates
            f"{company} chi thu thap {context} thuc su can thiet.",
            f"{prefix} {company} tranh thu thap {context} du thua.",
            f"{company} khong {random.choice(actions)} {context} khong can thiet.",
            f"{company} han che viec thu thap {context} o muc toi thieu.",
            # New 4 templates
            f"{company} dam bao {context} duoc xu ly hop ly.",
            f"{company} thuc hien {context} mot cach minh bach.",
            f"{company} quan ly {context} theo quy dinh PDPL.",
            f"{company} giai thich {context} cho chu the du lieu.",
        ]
    elif structure == 'declarative':
        # NEW structure type
        templates = [
            f"Chinh sach cua {company} ve {context} rat ro rang.",
            f"{company} da cong khai {context} tren website.",
            f"Quy trinh {context} tai {company} duoc giam sat chat che.",
            f"{company} bao ve {context} bang cac bien phap ky thuat.",
            f"Nhan vien {company} duoc dao tao ve {context}.",
            f"{company} cap nhat {context} dinh ky hang nam.",
            f"Quy dinh ve {context} cua {company} tuan thu PDPL 2025.",
            f"{company} thong bao {context} cho khach hang khi can.",
        ]
    # ... similar expansion for other structures
```

**Changes:**
- Structures: 4 -> 8 types
- Templates per structure: 4 -> 8
- Total base templates: 16 -> 64 per category
- Template space: 480 -> 7,680 unique patterns per category

**Math:**
```
OLD: 16 templates × 30 contexts = 480 unique patterns
NEW: 64 templates × 60 contexts = 3,840 unique patterns

For Cat 2 (3,750 samples):
  OLD: 3,750 / 480 = 7.8x duplication
  NEW: 3,750 / 3,840 = 0.98x (97% uniqueness)
```

---

### Change 5: Increase Max Attempts (Step 5)

**Current Code:**
```python
# Step 5 - Generate base dataset
target_per_category = 3000
max_attempts = 100  # Increased from 50 to handle relaxed leak detection
```

**Modified Code:**
```python
# Step 5 - Generate base dataset  
target_per_category = 3000
max_attempts = 200  # Increased from 100 to handle STRICT leak detection
```

**Rationale:**
- Stricter leak detection requires more attempts to find unique samples
- With 3,840 patterns per category, 200 attempts is safe
- Prevents false "infinite loop" detection

---

## Implementation Sequence

### Phase 1: Expand Data Definitions (5 minutes)

**Step 1.1: Expand BUSINESS_CONTEXTS (Step 2)**
- Read current cell content
- Double each category's context phrases (6 -> 12)
- Validate syntax
- Update cell

**Step 1.2: Expand CAT2_DISTINCTIVE_PHRASES (Step 4)**
- Read current dictionary
- Add 25 more QUANTITY/AMOUNT markers
- Validate syntax
- Update cell

**Step 1.3: Expand CAT6_DISTINCTIVE_PHRASES (Step 4)**
- Read current dictionary
- Add 26 more PROOF/REPORTING markers
- Validate syntax  
- Update cell

### Phase 2: Modify Generation Logic (5 minutes)

**Step 2.1: Update _check_data_leak method**
- Change threshold: `>= 3` -> `>= 1`
- Update docstring
- Validate syntax

**Step 2.2: Expand _generate_template method**
- Add 4 new structure types
- Double templates per structure (4 -> 8)
- Validate syntax

**Step 2.3: Update max_attempts**
- Change from 100 -> 200
- Add comment explaining strict mode

### Phase 3: Execute and Validate (25 minutes)

**Step 3.1: Re-run Step 5 (20-25 minutes)**
- Generate 24,000 base samples
- Monitor for infinite loop (should not occur)
- Expected uniqueness: 90%+ (vs 84% before)

**Step 3.2: Re-run Step 6 (instant)**
- Validate base dataset quality
- Check template diversity, uniqueness

**Step 3.3: Re-run Step 7 (5 minutes)**
- Generate v1.1 augmentation
- Split dataset 80/10/10
- Check data leakage: Target <5% (vs 54% before)

**Step 3.4: Document Results**
- Compare before/after metrics
- Verify leakage reduction
- Prepare for Step 8 training

---

## Validation Checkpoints

### Checkpoint 1: After Code Modifications
```
[OK] All Python syntax validated
[OK] No undefined variables
[OK] Docstrings updated
[OK] Comments explain changes
```

### Checkpoint 2: After Step 5 Execution
```
[OK] 24,000 samples generated
[OK] No infinite loop occurred
[OK] Uniqueness >= 90%
[OK] Template diversity improved
[OK] Generation time: 20-25 minutes
```

### Checkpoint 3: After Step 7 Execution
```
[OK] 26,000 samples in v1.1 dataset
[OK] Uniqueness >= 88%
[OK] Train/Val overlap < 5%
[OK] Train/Test overlap < 5%
[OK] Files saved: train.jsonl, validation.jsonl, test.jsonl
```

---

## Expected Results Comparison

| Metric | Before (Relaxed) | After (Strict) | Improvement |
|--------|-----------------|----------------|-------------|
| **Base dataset uniqueness** | 84.87% | 90%+ | +5%+ |
| **v1.1 dataset uniqueness** | 59.73% | 88%+ | +28%+ |
| **Template patterns (Cat 2)** | 480 | 3,840 | 8x |
| **Leak detection threshold** | 3 duplicates | 1 duplicate | Stricter |
| **Train/Val overlap** | 54.2% | <5% | -49%+ |
| **Train/Test overlap** | 54.2% | <5% | -49%+ |
| **Validation accuracy** | 87% (inflated) | 85% (true) | Reliable |
| **Production accuracy** | 75% (true) | 85% (true) | +10% |
| **Val-Prod gap** | 12% | <2% | Trustworthy |

---

## Risk Mitigation

### Risk 1: Infinite Loop Despite Expansion
**Likelihood:** Low (template space 8x larger)
**Mitigation:** 
- max_attempts increased to 200
- Emergency break after 10 consecutive failures
- Can further relax to allow 2 duplicates if needed

### Risk 2: Generation Time Too Long
**Likelihood:** Medium (stricter detection = more rejections)
**Mitigation:**
- Expected 20-25 minutes is acceptable
- Can monitor progress and abort if >30 minutes
- Template space is sufficient for 24k samples

### Risk 3: Quality Degradation
**Likelihood:** Low (more templates = more variety)
**Mitigation:**
- Step 6 validation catches quality issues
- New templates maintain Vietnamese cultural context
- Distinctive vocabulary still injected at 60%

---

## Success Criteria

### Must Have:
- [REQUIRED] Base dataset uniqueness >= 90%
- [REQUIRED] v1.1 dataset uniqueness >= 88%
- [REQUIRED] Train/Val overlap < 5%
- [REQUIRED] No infinite loop errors

### Should Have:
- [DESIRED] Step 5 execution time < 25 minutes
- [DESIRED] Template diversity validation passes
- [DESIRED] Category balance maintained

### Nice to Have:
- [OPTIONAL] Uniqueness > 92%
- [OPTIONAL] Train/Val overlap < 3%
- [OPTIONAL] All Step 6 validations pass

---

## Rollback Plan

If Strategy C fails or takes too long:

**Option 1: Partial Rollback**
- Keep expanded templates/contexts
- Relax leak detection to allow 2 duplicates (instead of 1)
- Target: 80%+ uniqueness, <10% leakage

**Option 2: Full Rollback**
- Revert all changes
- Apply Strategy B instead (deduplicate before split)
- Faster but smaller training set

**Option 3: Hybrid Approach**
- Use strict mode for Cat 2/6 only (confused categories)
- Use relaxed mode for other categories
- Reduces generation time while fixing key issues

---

## Next Steps After Completion

1. Execute Step 8 training (6-8 minutes)
2. Monitor validation accuracy (expect 82-85%, not 87%+)
3. Execute Step 9 production testing
4. Verify production accuracy matches validation (+/- 2%)
5. If production >= 85%: SUCCESS - deploy model
6. If production < 85%: Investigate further improvements

---

## Notes

- All code changes use ASCII characters only (no emoji)
- Dynamic coding preferred (reuse definitions, calculate counts)
- Python syntax validation before each cell update
- Follow VeriSyntra coding standards from copilot-instructions.md
