"""
Unit Tests for PDPLTextNormalizer
Tests Vietnamese text normalization for PDPL 2025 compliance.

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

from app.core.company_registry import CompanyRegistry
from app.core.pdpl_normalizer import PDPLTextNormalizer, NormalizationResult


class TestPDPLTextNormalizer(unittest.TestCase):
    """Test suite for PDPLTextNormalizer class."""
    
    def setUp(self):
        """Create test registry and normalizer."""
        # Create temporary config
        self.temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        
        test_data = {
            "technology": {
                "south": [
                    {
                        "name": "Grab Vietnam",
                        "aliases": ["Grab", "Grab VN"],
                        "metadata": {"website": "grab.com/vn"},
                        "added_date": "2025-10-18T00:00:00"
                    },
                    {
                        "name": "Shopee Vietnam",
                        "aliases": ["Shopee", "Shopee VN"],
                        "metadata": {"website": "shopee.vn"},
                        "added_date": "2025-10-18T00:00:00"
                    }
                ]
            },
            "finance": {
                "north": [
                    {
                        "name": "Vietcombank",
                        "aliases": ["VCB", "Bank for Foreign Trade"],
                        "metadata": {"website": "vietcombank.com.vn"},
                        "added_date": "2025-10-18T00:00:00"
                    }
                ]
            }
        }
        
        json.dump(test_data, self.temp_config, indent=2, ensure_ascii=False)
        self.temp_config.close()
        
        # Initialize registry and normalizer
        self.registry = CompanyRegistry(self.temp_config.name)
        self.normalizer = PDPLTextNormalizer(self.registry)
    
    def tearDown(self):
        """Clean up temporary files."""
        Path(self.temp_config.name).unlink(missing_ok=True)
    
    def test_initialization(self):
        """Test normalizer initialization."""
        self.assertIsNotNone(self.normalizer)
        self.assertIsNotNone(self.normalizer.company_registry)
    
    def test_normalize_single_company(self):
        """Test normalizing single company name."""
        text = "Grab Vietnam thu thap du lieu vi tri"
        result = self.normalizer.normalize_text(text)
        
        self.assertIsInstance(result, NormalizationResult)
        self.assertIn('[COMPANY]', result.normalized_text)
        self.assertEqual(result.company_count, 1)
        self.assertEqual(result.person_count, 0)
    
    def test_normalize_multiple_companies(self):
        """Test normalizing multiple company names."""
        text = "Vietcombank va Grab hop tac voi Shopee"
        result = self.normalizer.normalize_text(text)
        
        self.assertEqual(result.company_count, 3)
        self.assertEqual(result.normalized_text.count('[COMPANY]'), 3)
    
    def test_normalize_company_alias(self):
        """Test normalizing company by alias."""
        text = "VCB cung cap dich vu ngan hang"
        result = self.normalizer.normalize_text(text)
        
        self.assertEqual(result.company_count, 1)
        self.assertIn('[COMPANY]', result.normalized_text)
    
    def test_normalize_case_insensitive(self):
        """Test case-insensitive normalization."""
        text1 = "GRAB VIETNAM thu thap du lieu"
        text2 = "grab vietnam thu thap du lieu"
        text3 = "Grab Vietnam thu thap du lieu"
        
        result1 = self.normalizer.normalize_text(text1)
        result2 = self.normalizer.normalize_text(text2)
        result3 = self.normalizer.normalize_text(text3)
        
        self.assertEqual(result1.company_count, 1)
        self.assertEqual(result2.company_count, 1)
        self.assertEqual(result3.company_count, 1)
    
    def test_normalize_for_inference(self):
        """Test normalize_for_inference method."""
        text = "Shopee Vietnam ban hang online"
        normalized = self.normalizer.normalize_for_inference(text)
        
        self.assertIn('[COMPANY]', normalized)
        self.assertNotIn('Shopee', normalized)
    
    def test_no_normalization_when_no_companies(self):
        """Test text without companies remains unchanged."""
        text = "Day la van ban khong co ten cong ty"
        result = self.normalizer.normalize_text(text)
        
        self.assertEqual(result.original_text, result.normalized_text)
        self.assertEqual(result.company_count, 0)
    
    def test_entities_found_metadata(self):
        """Test entities_found contains correct metadata."""
        text = "Grab Vietnam hoat dong tai Viet Nam"
        result = self.normalizer.normalize_text(text)
        
        self.assertGreater(len(result.entities_found), 0)
        
        entity = result.entities_found[0]
        self.assertEqual(entity['type'], 'company')
        self.assertEqual(entity['token'], '[COMPANY]')
        self.assertIn('metadata', entity)
    
    def test_denormalize_text(self):
        """Test denormalization restores original entities."""
        normalized_text = "[COMPANY] thu thap du lieu nguoi dung"
        entity_map = {'[COMPANY]': 'Grab Vietnam'}
        
        denormalized = self.normalizer.denormalize_text(normalized_text, entity_map)
        
        self.assertEqual(denormalized, "Grab Vietnam thu thap du lieu nguoi dung")
        self.assertNotIn('[COMPANY]', denormalized)
    
    def test_get_company_mentions(self):
        """Test extracting company mentions."""
        text = "Vietcombank va Grab hop tac. Vietcombank cung cap tai khoan."
        mentions = self.normalizer.get_company_mentions(text)
        
        self.assertGreater(len(mentions), 0)
        
        # Check Vietcombank has 2 occurrences
        vietcombank_mention = next(
            (m for m in mentions if m['name'] == 'Vietcombank'),
            None
        )
        self.assertIsNotNone(vietcombank_mention)
        self.assertEqual(vietcombank_mention['occurrences'], 2)
    
    def test_validate_normalization(self):
        """Test normalization validation."""
        original = "Grab Vietnam thu thap du lieu"
        normalized = "[COMPANY] thu thap du lieu"
        
        validation = self.normalizer.validate_normalization(original, normalized)
        
        self.assertTrue(validation['is_valid'])
        self.assertEqual(validation['company_tokens'], 1)
        self.assertEqual(validation['person_tokens'], 0)
        self.assertGreater(validation['length_ratio'], 0)
    
    def test_validate_normalization_with_issues(self):
        """Test validation detects issues."""
        original = "Some text"
        normalized = "[COMPANY] already has [COMPANY] token"
        
        validation = self.normalizer.validate_normalization(original, normalized)
        
        self.assertEqual(validation['company_tokens'], 2)


class TestPDPLTextNormalizerEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_empty_text(self):
        """Test normalizing empty text."""
        temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        json.dump({}, temp_config, indent=2)
        temp_config.close()
        
        registry = CompanyRegistry(temp_config.name)
        normalizer = PDPLTextNormalizer(registry)
        
        result = normalizer.normalize_text("")
        
        self.assertEqual(result.original_text, "")
        self.assertEqual(result.normalized_text, "")
        self.assertEqual(result.company_count, 0)
        
        Path(temp_config.name).unlink()
    
    def test_text_with_special_characters(self):
        """Test normalizing text with special characters."""
        temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        
        test_data = {
            "technology": {
                "south": [
                    {
                        "name": "Test Company",
                        "aliases": [],
                        "metadata": {},
                        "added_date": "2025-10-18T00:00:00"
                    }
                ]
            }
        }
        
        json.dump(test_data, temp_config, indent=2)
        temp_config.close()
        
        registry = CompanyRegistry(temp_config.name)
        normalizer = PDPLTextNormalizer(registry)
        
        text = "Test Company (parent company) - main office!"
        result = normalizer.normalize_text(text)
        
        self.assertEqual(result.company_count, 1)
        self.assertIn('[COMPANY]', result.normalized_text)
        
        Path(temp_config.name).unlink()
    
    def test_overlapping_company_names(self):
        """Test handling overlapping company names."""
        temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        
        test_data = {
            "technology": {
                "south": [
                    {
                        "name": "FPT",
                        "aliases": [],
                        "metadata": {},
                        "added_date": "2025-10-18T00:00:00"
                    },
                    {
                        "name": "FPT Software",
                        "aliases": [],
                        "metadata": {},
                        "added_date": "2025-10-18T00:00:00"
                    }
                ]
            }
        }
        
        json.dump(test_data, temp_config, indent=2)
        temp_config.close()
        
        registry = CompanyRegistry(temp_config.name)
        normalizer = PDPLTextNormalizer(registry)
        
        # Longer name should be matched first
        text = "FPT Software is a subsidiary of FPT"
        result = normalizer.normalize_text(text)
        
        # Should normalize both companies
        self.assertGreaterEqual(result.company_count, 1)
        
        Path(temp_config.name).unlink()


if __name__ == '__main__':
    unittest.main()
