"""
Unit Tests for All 11 VeriAIDPO Model Types
Tests the expanded VietnameseHardDatasetGenerator supporting all model types

Author: VeriSyntra Development Team
Created: 2025-10-18
Version: 2.0.0
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.ml.vietnamese_hard_dataset_generator import VietnameseHardDatasetGenerator


class TestAllModelTypes(unittest.TestCase):
    """Test all 11 model types initialization and basic functionality."""
    
    def test_all_model_types_initialization(self):
        """Test that all 11 model types can be initialized."""
        model_types = [
            'principles', 'legal_basis', 'breach_triage', 'cross_border',
            'consent_type', 'data_sensitivity', 'dpo_tasks', 'risk_level',
            'compliance_status', 'regional', 'industry'
        ]
        
        for model_type in model_types:
            with self.subTest(model_type=model_type):
                generator = VietnameseHardDatasetGenerator(model_type=model_type)
                self.assertEqual(generator.model_type, model_type)
                self.assertIsNotNone(generator.categories)
                self.assertGreater(len(generator.categories), 0)
    
    def test_invalid_model_type(self):
        """Test that invalid model type raises ValueError."""
        with self.assertRaises(ValueError) as context:
            VietnameseHardDatasetGenerator(model_type='invalid_model')
        
        self.assertIn("Invalid model_type", str(context.exception))
    
    def test_category_counts(self):
        """Test that each model type has correct number of categories."""
        expected_counts = {
            'principles': 8,
            'legal_basis': 4,
            'breach_triage': 4,
            'cross_border': 5,
            'consent_type': 4,
            'data_sensitivity': 4,
            'dpo_tasks': 5,
            'risk_level': 4,
            'compliance_status': 4,
            'regional': 3,
            'industry': 4
        }
        
        for model_type, expected_count in expected_counts.items():
            with self.subTest(model_type=model_type):
                generator = VietnameseHardDatasetGenerator(model_type=model_type)
                self.assertEqual(len(generator.categories), expected_count)
    
    def test_generate_sample_all_models(self):
        """Test sample generation for all model types."""
        model_types = [
            'principles', 'legal_basis', 'breach_triage', 'cross_border',
            'consent_type', 'data_sensitivity', 'dpo_tasks', 'risk_level',
            'compliance_status', 'regional', 'industry'
        ]
        
        for model_type in model_types:
            with self.subTest(model_type=model_type):
                generator = VietnameseHardDatasetGenerator(model_type=model_type)
                
                # Generate sample for first category
                sample = generator.generate_hard_sample(
                    category_id=0,
                    ambiguity='HARD',
                    region='south',
                    formality='business'
                )
                
                self.assertIn('text', sample)
                self.assertIn('label', sample)
                self.assertIn('raw_text', sample)
                self.assertIn('ambiguity', sample)
                self.assertIn('metadata', sample)
                self.assertEqual(sample['metadata']['model_type'], model_type)
    
    def test_invalid_category_id(self):
        """Test that invalid category_id raises ValueError."""
        generator = VietnameseHardDatasetGenerator(model_type='principles')
        
        with self.assertRaises(ValueError) as context:
            generator.generate_hard_sample(category_id=999)
        
        self.assertIn("Invalid category_id", str(context.exception))
    
    def test_statistics_includes_model_type(self):
        """Test that get_statistics includes model type information."""
        generator = VietnameseHardDatasetGenerator(model_type='legal_basis')
        stats = generator.get_statistics()
        
        self.assertIn('model_type', stats)
        self.assertEqual(stats['model_type'], 'legal_basis')
        self.assertIn('categories', stats)
        self.assertIn('num_categories', stats)
        self.assertIn('available_model_types', stats)
        self.assertEqual(len(stats['available_model_types']), 11)


class TestPrinciplesModel(unittest.TestCase):
    """Test VeriAIDPO_Principles model (8 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='principles')
    
    def test_all_categories(self):
        """Test all 8 PDPL principle categories."""
        expected_categories = [
            "Lawfulness", "Purpose Limitation", "Data Minimization",
            "Accuracy", "Storage Limitation", "Security",
            "Transparency", "Accountability"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestLegalBasisModel(unittest.TestCase):
    """Test VeriAIDPO_LegalBasis model (4 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='legal_basis')
    
    def test_all_categories(self):
        """Test all 4 legal basis categories."""
        expected_categories = [
            "Consent", "Contract Performance",
            "Legal Obligation", "Legitimate Interest"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestBreachTriageModel(unittest.TestCase):
    """Test VeriAIDPO_BreachTriage model (4 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='breach_triage')
    
    def test_all_categories(self):
        """Test all 4 breach severity categories."""
        expected_categories = [
            "Low Risk", "Medium Risk", "High Risk", "Critical Risk"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestCrossBorderModel(unittest.TestCase):
    """Test VeriAIDPO_CrossBorder model (5 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='cross_border')
    
    def test_all_categories(self):
        """Test all 5 cross-border transfer categories."""
        expected_categories = [
            "Domestic Only", "Approved Country Transfer",
            "Requires MPS Approval", "Prohibited Transfer",
            "Emergency Exception"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestConsentTypeModel(unittest.TestCase):
    """Test VeriAIDPO_ConsentType model (4 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='consent_type')
    
    def test_all_categories(self):
        """Test all 4 consent type categories."""
        expected_categories = [
            "Explicit Consent", "Implied Consent",
            "Parental Consent", "Invalid Consent"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestDataSensitivityModel(unittest.TestCase):
    """Test VeriAIDPO_DataSensitivity model (4 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='data_sensitivity')
    
    def test_all_categories(self):
        """Test all 4 data sensitivity categories."""
        expected_categories = [
            "Basic Data", "Personal Data",
            "Sensitive Data", "Special Category Data"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestDPOTasksModel(unittest.TestCase):
    """Test VeriAIDPO_DPOTasks model (5 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='dpo_tasks')
    
    def test_all_categories(self):
        """Test all 5 DPO task categories."""
        expected_categories = [
            "Advisory", "Policy Development", "Training",
            "Audit", "Regulatory Reporting"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestRiskLevelModel(unittest.TestCase):
    """Test VeriAIDPO_RiskLevel model (4 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='risk_level')
    
    def test_all_categories(self):
        """Test all 4 risk level categories."""
        expected_categories = [
            "Low Risk", "Medium Risk",
            "High Risk (DPIA Required)", "Critical Risk"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestComplianceStatusModel(unittest.TestCase):
    """Test VeriAIDPO_ComplianceStatus model (4 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='compliance_status')
    
    def test_all_categories(self):
        """Test all 4 compliance status categories."""
        expected_categories = [
            "Compliant", "Partially Compliant",
            "Non-Compliant", "Unknown Status"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestRegionalModel(unittest.TestCase):
    """Test VeriAIDPO_Regional model (3 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='regional')
    
    def test_all_categories(self):
        """Test all 3 regional categories."""
        expected_categories = ["North", "Central", "South"]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestIndustryModel(unittest.TestCase):
    """Test VeriAIDPO_Industry model (4 categories)."""
    
    def setUp(self):
        self.generator = VietnameseHardDatasetGenerator(model_type='industry')
    
    def test_all_categories(self):
        """Test all 4 industry categories."""
        expected_categories = [
            "Finance", "Healthcare", "Education", "Technology"
        ]
        
        for i, expected_name in enumerate(expected_categories):
            self.assertEqual(self.generator.categories[i], expected_name)


class TestDatasetGeneration(unittest.TestCase):
    """Test dataset generation for multiple model types."""
    
    def test_generate_small_dataset_principles(self):
        """Test generating small dataset for principles model."""
        generator = VietnameseHardDatasetGenerator(model_type='principles')
        dataset = generator.generate_dataset(samples_per_category=5)
        
        # Note: Due to rounding in ambiguity distribution (40% + 40% + 14% + 6%),
        # actual count may be less than samples_per_category × num_categories
        # Expected: ~32 samples (4 per category after rounding: 2+2+0+0=4, 4×8=32)
        self.assertGreaterEqual(len(dataset), 30)
        self.assertLessEqual(len(dataset), 42)
        
        # Check all samples have required fields
        for sample in dataset:
            self.assertIn('text', sample)
            self.assertIn('label', sample)
            self.assertIn('metadata', sample)
            self.assertEqual(sample['metadata']['model_type'], 'principles')
    
    def test_generate_small_dataset_legal_basis(self):
        """Test generating small dataset for legal_basis model."""
        generator = VietnameseHardDatasetGenerator(model_type='legal_basis')
        dataset = generator.generate_dataset(samples_per_category=10)
        
        # Note: Due to rounding (4+4+1+0=9, 9×4=36)
        self.assertGreaterEqual(len(dataset), 34)
        self.assertLessEqual(len(dataset), 42)
        
        # Check label distribution
        labels = [sample['label'] for sample in dataset]
        self.assertEqual(set(labels), {0, 1, 2, 3})
    
    def test_generate_dataset_with_num_categories(self):
        """Test generating dataset with limited categories."""
        generator = VietnameseHardDatasetGenerator(model_type='principles')
        dataset = generator.generate_dataset(samples_per_category=5, num_categories=3)
        
        # Note: Due to rounding (2+2+0+0=4, 4×3=12)
        self.assertGreaterEqual(len(dataset), 10)
        self.assertLessEqual(len(dataset), 17)
        
        # Check only first 3 labels used
        labels = [sample['label'] for sample in dataset]
        self.assertTrue(set(labels).issubset({0, 1, 2}))
    
    def test_invalid_num_categories(self):
        """Test that exceeding available categories raises ValueError."""
        generator = VietnameseHardDatasetGenerator(model_type='regional')  # 3 categories
        
        with self.assertRaises(ValueError) as context:
            generator.generate_dataset(samples_per_category=5, num_categories=10)
        
        self.assertIn("exceeds available categories", str(context.exception))


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
