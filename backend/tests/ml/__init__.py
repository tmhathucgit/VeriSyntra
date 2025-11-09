"""
VeriSyntra Machine Learning Test Suite

Vietnamese Context: Bo kiem thu Mo hinh Hoc may VeriAiDPO
Tests for VeriAiDPO model inference, dataset generation, and ML APIs

Test Organization:
- test_model_integration.py - Model loading and inference
- test_all_model_types.py - All model variants
- test_veriaidpo_classification_api.py - Classification API
- test_vietnamese_hard_dataset_generator.py - Dataset generation

Usage:
    python backend/tests/run_ml_tests.py              # Full suite
    python backend/tests/run_ml_tests.py --quick      # Skip slow tests
    python backend/tests/run_ml_tests.py --models-only # Models only
"""

__version__ = "1.0.0"
__author__ = "VeriSyntra ML Team"

# ML test suite metadata
ML_TEST_SUITE = {
    "name": "VeriSyntra ML Test Suite",
    "version": __version__,
    "test_count": 4,
    "categories": [
        "Model Inference",
        "API Endpoints",
        "Dataset Generation"
    ],
    "duration_estimates": {
        "full": "10-15 minutes",
        "quick": "3-5 minutes",
        "models_only": "1-2 minutes"
    }
}
