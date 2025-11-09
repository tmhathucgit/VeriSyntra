# VeriSyntra ML Test Suite

**Machine learning model tests** for VeriAiDPO PDPL classification and Vietnamese dataset generation.

---

## 📁 Test Organization

### ML Test Files

**Model Inference & Integration:**
- `test_model_integration.py` - Model loading, inference, basic validation
- `test_all_model_types.py` - All model variants and types testing

**API Endpoints:**
- `test_veriaidpo_classification_api.py` - VeriAiDPO classification API endpoints

**Dataset Generation:**
- `test_vietnamese_hard_dataset_generator.py` - Vietnamese PDPL dataset generation with cultural context

---

## 🚀 Running ML Tests

### Full ML Test Suite

```bash
# Run all ML tests (slow - may take 10-15 minutes)
python backend/tests/run_ml_tests.py
```

### Quick Mode (Skip Slow Tests)

```bash
# Skip dataset generation tests (faster - 3-5 minutes)
python backend/tests/run_ml_tests.py --quick
```

### Models Only

```bash
# Only model inference tests (fastest - 1-2 minutes)
python backend/tests/run_ml_tests.py --models-only
```

### Individual Test Files

```bash
# Run specific test file
pytest backend/tests/ml/test_model_integration.py -v

# Run with timeout (for slow tests)
pytest backend/tests/ml/test_vietnamese_hard_dataset_generator.py -v --timeout=600
```

---

## ⚙️ Prerequisites

### ML Dependencies

```bash
# Install ML dependencies
pip install transformers torch datasets

# Or install all backend requirements
pip install -r backend/requirements.txt
```

### Model Files

**VeriAiDPO model** must be available:
- **Hugging Face:** `tmhathucgit/VeriAIDPO_Principles_VI_v1`
- **Local:** `backend/app/ml/models/VeriAIDPO_*/`

First run downloads model from Hugging Face (~500MB).

### Running Backend (for API tests)

```bash
# Start backend server
cd backend
python main_prototype.py

# API available at http://localhost:8000
```

---

## 📊 Expected Test Duration

| Test Suite | Duration | Notes |
|------------|----------|-------|
| Model Integration | 1-2 min | First run: model download |
| All Model Types | 2-5 min | Tests multiple variants |
| VeriAiDPO API | 1-2 min | Requires running backend |
| Dataset Generator | 5-10 min | Slow - generates samples |

**Total (Full Suite):** 10-15 minutes  
**Quick Mode:** 3-5 minutes  
**Models Only:** 1-2 minutes

---

## 🎯 When to Run ML Tests

### Run ML Tests When:

✅ **Changing ML code:**
- Model loading/inference logic
- Dataset generation algorithms
- VeriAiDPO classification API

✅ **Updating models:**
- New model versions
- Model fine-tuning
- Architecture changes

✅ **Before deployments:**
- Pre-production validation
- Model quality assurance

✅ **Scheduled (CI/CD):**
- Nightly builds
- Weekly quality checks

### DO NOT Run ML Tests:

❌ **On every code change** - Too slow for rapid development
❌ **With backend regression tests** - Different test cadence
❌ **For non-ML changes** - Authentication, database, UI changes

---

## 🔧 Test Configuration

### Environment Variables

```bash
# Model configuration
VERIAIDPO_MODEL_PATH=backend/app/ml/models/VeriAIDPO_Principles_VI_v1
HUGGINGFACE_MODEL_NAME=tmhathucgit/VeriAIDPO_Principles_VI_v1

# Backend API (for API tests)
BACKEND_URL=http://localhost:8000
```

### Test Timeouts

Configured in `run_ml_tests.py`:
- Model tests: 180s (3 min)
- API tests: 180s (3 min)
- Dataset tests: 600s (10 min)

---

## 🎨 Test Output Examples

### Successful Run

```
======================================================================
VeriSyntra Machine Learning Test Suite
Kiem thu Mo hinh Hoc may VeriAiDPO
======================================================================

[INFO] Checking ML dependencies...
[OK] transformers installed
[OK] torch installed
[OK] datasets installed
[OK] All ML dependencies installed

======================================================================
PRIORITY 1: Model Inference & Integration Tests
UU TIEN 1: Kiem thu Suy dien Mo hinh
======================================================================

--- Model Integration & Loading ---
Pattern: tests/ml/test_model_integration.py
[OK] Model Integration & Loading - Tests passed

--- All Model Types & Variants ---
Pattern: tests/ml/test_all_model_types.py
[OK] All Model Types & Variants - Tests passed

======================================================================
ML Test Summary / Tong ket Kiem thu ML
======================================================================

Overall Results:
  Total Tests: 4
  Passed: 4
  Failed: 0
  Errors: 0

[OK] All ML tests passed!
[OK] Tat ca kiem thu ML thanh cong!
```

---

## 🐛 Troubleshooting

### Model Download Issues

```bash
# If model download fails, manually download
python -c "from transformers import AutoModel; AutoModel.from_pretrained('tmhathucgit/VeriAIDPO_Principles_VI_v1')"
```

### Memory Issues

```bash
# Reduce batch size for dataset tests
export TEST_BATCH_SIZE=8

# Use quick mode to skip memory-intensive tests
python backend/tests/run_ml_tests.py --quick
```

### GPU/CUDA Issues

```bash
# Force CPU mode (slower but more compatible)
export CUDA_VISIBLE_DEVICES=""
pytest backend/tests/ml/ -v
```

---

## 📚 Related Documentation

- **ML Models:** `backend/app/ml/README.md`
- **Dataset Generation:** `docs/VeriSystems/VeriAIDPO_MVP_QuickStart.py`
- **Model Training:** `docs/VeriSystems/VeriAIDPO_Google_Colab_Training_Guide.md`
- **Backend Tests:** `backend/tests/README.md`

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/ml-tests.yml
name: ML Test Suite

on:
  schedule:
    - cron: '0 2 * * *'  # Run nightly at 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  ml-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install transformers torch datasets pytest
      
      - name: Run ML tests (quick mode)
        run: python backend/tests/run_ml_tests.py --quick
        env:
          CUDA_VISIBLE_DEVICES: ""
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: ml-test-results
          path: backend/tests/ml/
```

---

**Last Updated:** November 8, 2025  
**Maintainer:** VeriSyntra ML Team  
**Test Coverage:** 4 ML test suites, 50+ individual tests
