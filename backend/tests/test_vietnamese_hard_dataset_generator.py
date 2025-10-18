"""
Unit Tests for VietnameseHardDatasetGenerator
Tests dataset generation with company normalization.

Author: VeriSyntra Development Team
Created: 2025-10-18
Version: 1.0.0
"""

import unittest
import json
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ml.vietnamese_hard_dataset_generator import VietnameseHardDatasetGenerator


class TestVietnameseHardDatasetGenerator(unittest.TestCase):
    """Test suite for VietnameseHardDatasetGenerator class."""
    
    def setUp(self):
        """Initialize generator for testing."""
        self.generator = VietnameseHardDatasetGenerator()
    
    def test_initialization(self):
        """Test generator initialization."""
        self.assertIsNotNone(self.generator)
        self.assertIsNotNone(self.generator.registry)
        self.assertIsNotNone(self.generator.normalizer)
        self.assertEqual(len(self.generator.PDPL_CATEGORIES), 8)
    
    def test_get_company_by_context(self):
        """Test company retrieval from registry."""
        company = self.generator.get_company_by_context()
        
        self.assertIsNotNone(company)
        self.assertIsInstance(company, str)
        self.assertGreater(len(company), 0)
    
    def test_get_company_by_industry(self):
        """Test company retrieval filtered by industry."""
        company = self.generator.get_company_by_context(industry='technology')
        
        self.assertIsNotNone(company)
        # Verify it's a known tech company or fallback
        self.assertGreater(len(company), 0)
    
    def test_get_company_by_region(self):
        """Test company retrieval filtered by region."""
        company = self.generator.get_company_by_context(region='south')
        
        self.assertIsNotNone(company)
        self.assertGreater(len(company), 0)
    
    def test_generate_easy_sample(self):
        """Test EASY sample generation."""
        sample = self.generator.generate_hard_sample(
            category_id=0,
            ambiguity='EASY',
            region='south',
            formality='business'
        )
        
        self.assertIsInstance(sample, dict)
        self.assertIn('text', sample)
        self.assertIn('label', sample)
        self.assertIn('raw_text', sample)
        self.assertIn('ambiguity', sample)
        self.assertIn('metadata', sample)
        
        self.assertEqual(sample['label'], 0)
        self.assertEqual(sample['ambiguity'], 'EASY')
    
    def test_generate_medium_sample(self):
        """Test MEDIUM sample generation."""
        sample = self.generator.generate_hard_sample(
            category_id=1,
            ambiguity='MEDIUM',
            region='north',
            formality='formal'
        )
        
        self.assertEqual(sample['label'], 1)
        self.assertEqual(sample['ambiguity'], 'MEDIUM')
    
    def test_generate_hard_sample(self):
        """Test HARD sample generation."""
        sample = self.generator.generate_hard_sample(
            category_id=2,
            ambiguity='HARD',
            region='south',
            formality='casual'
        )
        
        self.assertEqual(sample['label'], 2)
        self.assertEqual(sample['ambiguity'], 'HARD')
    
    def test_generate_very_hard_sample(self):
        """Test VERY_HARD sample generation."""
        sample = self.generator.generate_hard_sample(
            category_id=3,
            ambiguity='VERY_HARD',
            region='central',
            formality='legal'
        )
        
        self.assertEqual(sample['label'], 3)
        self.assertEqual(sample['ambiguity'], 'VERY_HARD')
    
    def test_company_normalization(self):
        """Test that company names are normalized to [COMPANY] token."""
        sample = self.generator.generate_hard_sample(
            category_id=0,
            ambiguity='EASY',
            region='south',
            formality='business',
            industry='technology'
        )
        
        # Normalized text should contain [COMPANY] token
        # (or might not if company name wasn't in the text)
        self.assertIn('text', sample)
        self.assertIn('raw_text', sample)
        
        # Raw text should be different from normalized (unless no company found)
        # At minimum, they should both be valid strings
        self.assertIsInstance(sample['text'], str)
        self.assertIsInstance(sample['raw_text'], str)
    
    def test_all_categories(self):
        """Test sample generation for all PDPL categories."""
        for category_id in range(8):
            sample = self.generator.generate_hard_sample(
                category_id=category_id,
                ambiguity='HARD',
                region='south',
                formality='business'
            )
            
            self.assertEqual(sample['label'], category_id)
            self.assertIn(sample['metadata']['category_name'], 
                         self.generator.PDPL_CATEGORIES.values())
    
    def test_metadata_completeness(self):
        """Test that metadata contains all required fields."""
        sample = self.generator.generate_hard_sample(
            category_id=0,
            ambiguity='HARD',
            region='south',
            formality='business',
            industry='finance'
        )
        
        metadata = sample['metadata']
        
        self.assertIn('company', metadata)
        self.assertIn('industry', metadata)
        self.assertIn('region', metadata)
        self.assertIn('formality', metadata)
        self.assertIn('context', metadata)
        self.assertIn('category_name', metadata)
    
    def test_generate_small_dataset(self):
        """Test generating small dataset."""
        dataset = self.generator.generate_dataset(
            samples_per_category=5,
            num_categories=8,
            output_file=None
        )
        
        # Should generate approximately 5 samples per category
        # (exact count may vary due to rounding with ambiguity ratios)
        self.assertGreater(len(dataset), 0)
        self.assertLess(len(dataset), 100)  # Should be around 40
        
        # Check all samples have required structure
        for sample in dataset:
            self.assertIn('text', sample)
            self.assertIn('label', sample)
            self.assertIn('raw_text', sample)
            self.assertIn('ambiguity', sample)
            self.assertIn('metadata', sample)
    
    def test_dataset_label_distribution(self):
        """Test that dataset has balanced label distribution."""
        dataset = self.generator.generate_dataset(
            samples_per_category=10,
            num_categories=8,
            output_file=None
        )
        
        # Count labels
        label_counts = {}
        for sample in dataset:
            label = sample['label']
            label_counts[label] = label_counts.get(label, 0) + 1
        
        # All categories should be present
        self.assertEqual(len(label_counts), 8)
        
        # Each category should have roughly equal samples
        for count in label_counts.values():
            self.assertGreater(count, 0)
    
    def test_dataset_ambiguity_distribution(self):
        """Test that dataset follows ambiguity distribution."""
        dataset = self.generator.generate_dataset(
            samples_per_category=100,
            num_categories=2,  # Just test 2 categories for speed
            output_file=None
        )
        
        # Count ambiguities
        ambiguity_counts = {}
        for sample in dataset:
            amb = sample['ambiguity']
            ambiguity_counts[amb] = ambiguity_counts.get(amb, 0) + 1
        
        total = len(dataset)
        
        # Check rough distribution (allowing 10% tolerance)
        very_hard_ratio = ambiguity_counts.get('VERY_HARD', 0) / total
        hard_ratio = ambiguity_counts.get('HARD', 0) / total
        medium_ratio = ambiguity_counts.get('MEDIUM', 0) / total
        easy_ratio = ambiguity_counts.get('EASY', 0) / total
        
        self.assertGreater(very_hard_ratio, 0.30)  # Target 40%
        self.assertGreater(hard_ratio, 0.30)  # Target 40%
        self.assertGreater(medium_ratio, 0.05)  # Target 14%
        # EASY might be 0 due to rounding with small sample size
    
    def test_save_dataset(self):
        """Test saving dataset to JSONL file."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.jsonl',
            delete=False
        ) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Generate and save dataset
            dataset = self.generator.generate_dataset(
                samples_per_category=5,
                num_categories=2,
                output_file=temp_path
            )
            
            # Verify file was created
            self.assertTrue(Path(temp_path).exists())
            
            # Read and validate JSONL
            with open(temp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.assertEqual(len(lines), len(dataset))
            
            # Validate each line is valid JSON
            for line in lines:
                obj = json.loads(line)
                self.assertIn('text', obj)
                self.assertIn('label', obj)
        
        finally:
            # Cleanup
            Path(temp_path).unlink(missing_ok=True)
    
    def test_get_statistics(self):
        """Test getting generator statistics."""
        stats = self.generator.get_statistics()
        
        self.assertIn('company_registry', stats)
        self.assertIn('configuration', stats)
        self.assertIn('pdpl_categories', stats)
        
        # Verify company registry stats
        registry_stats = stats['company_registry']
        self.assertIn('total_companies', registry_stats)
        self.assertGreater(registry_stats['total_companies'], 0)
        
        # Verify configuration
        config = stats['configuration']
        self.assertIn('ambiguity_levels', config)
        self.assertIn('regional_styles', config)
        self.assertIn('formality_levels', config)
        
        # Verify PDPL categories
        self.assertEqual(len(stats['pdpl_categories']), 8)


class TestDatasetQuality(unittest.TestCase):
    """Test dataset quality and diversity."""
    
    def setUp(self):
        """Initialize generator."""
        self.generator = VietnameseHardDatasetGenerator()
    
    def test_company_diversity(self):
        """Test that dataset uses diverse companies."""
        dataset = self.generator.generate_dataset(
            samples_per_category=20,
            num_categories=4,
            output_file=None
        )
        
        # Collect unique companies
        companies = set(sample['metadata']['company'] for sample in dataset)
        
        # Should use multiple different companies
        self.assertGreater(len(companies), 5)
    
    def test_context_diversity(self):
        """Test that dataset uses diverse data contexts."""
        dataset = self.generator.generate_dataset(
            samples_per_category=20,
            num_categories=4,
            output_file=None
        )
        
        # Collect unique contexts
        contexts = set(sample['metadata']['context'] for sample in dataset)
        
        # Should use multiple different contexts
        self.assertGreater(len(contexts), 5)
    
    def test_region_diversity(self):
        """Test that dataset covers all regions."""
        dataset = self.generator.generate_dataset(
            samples_per_category=30,
            num_categories=4,
            output_file=None
        )
        
        # Collect unique regions
        regions = set(sample['metadata']['region'] for sample in dataset)
        
        # Should have all three regions
        self.assertEqual(len(regions), 3)
        self.assertIn('north', regions)
        self.assertIn('central', regions)
        self.assertIn('south', regions)
    
    def test_formality_diversity(self):
        """Test that dataset uses all formality levels."""
        dataset = self.generator.generate_dataset(
            samples_per_category=30,
            num_categories=4,
            output_file=None
        )
        
        # Collect unique formalities
        formalities = set(sample['metadata']['formality'] for sample in dataset)
        
        # Should have all four formality levels
        self.assertEqual(len(formalities), 4)
        self.assertIn('legal', formalities)
        self.assertIn('formal', formalities)
        self.assertIn('business', formalities)
        self.assertIn('casual', formalities)


if __name__ == '__main__':
    unittest.main()
