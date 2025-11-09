"""
Unit Tests for CompanyRegistry
Tests dynamic company management and hot-reload functionality.

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


class TestCompanyRegistry(unittest.TestCase):
    """Test suite for CompanyRegistry class."""
    
    def setUp(self):
        """Create temporary config file for testing."""
        self.temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        
        # Create test data
        test_data = {
            "technology": {
                "south": [
                    {
                        "name": "Test Company A",
                        "aliases": ["TCA", "Test A"],
                        "metadata": {"website": "testa.vn", "type": "Startup"},
                        "added_date": "2025-10-18T00:00:00"
                    },
                    {
                        "name": "Test Company B",
                        "aliases": ["TCB", "Test B"],
                        "metadata": {"website": "testb.vn", "type": "Private"},
                        "added_date": "2025-10-18T00:00:00"
                    }
                ]
            },
            "finance": {
                "north": [
                    {
                        "name": "Test Bank",
                        "aliases": ["TB", "Test Banking"],
                        "metadata": {"website": "testbank.vn", "type": "SOE"},
                        "added_date": "2025-10-18T00:00:00"
                    }
                ]
            }
        }
        
        json.dump(test_data, self.temp_config, indent=2, ensure_ascii=False)
        self.temp_config.close()
        
        # Initialize registry with test config
        self.registry = CompanyRegistry(self.temp_config.name)
    
    def tearDown(self):
        """Clean up temporary files."""
        Path(self.temp_config.name).unlink(missing_ok=True)
    
    def test_initialization(self):
        """Test registry initialization."""
        self.assertIsNotNone(self.registry)
        self.assertEqual(len(self.registry._company_index), 3)
    
    def test_reload(self):
        """Test hot-reload functionality."""
        result = self.registry.reload()
        
        self.assertTrue(result['success'])
        self.assertEqual(result['companies_loaded'], 3)
        self.assertEqual(result['industries'], 2)
        self.assertIn('north', result['regions'])
        self.assertIn('south', result['regions'])
    
    def test_add_company(self):
        """Test adding new company."""
        result = self.registry.add_company(
            name="New Startup",
            industry="technology",
            region="south",
            aliases=["NS", "NewStart"],
            metadata={"founded": 2025},
            persist=False
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['company_name'], "New Startup")
        
        # Verify company was added
        company_info = self.registry.get_company_info("New Startup")
        self.assertIsNotNone(company_info)
        self.assertEqual(company_info['industry'], 'technology')
    
    def test_add_duplicate_company(self):
        """Test adding duplicate company fails."""
        result = self.registry.add_company(
            name="Test Company A",
            industry="technology",
            region="south",
            persist=False
        )
        
        self.assertFalse(result['success'])
        self.assertIn('already exists', result['message'])
    
    def test_remove_company(self):
        """Test removing company."""
        result = self.registry.remove_company("Test Company A", persist=False)
        
        self.assertTrue(result['success'])
        
        # Verify company was removed
        company_info = self.registry.get_company_info("Test Company A")
        self.assertIsNone(company_info)
    
    def test_remove_nonexistent_company(self):
        """Test removing non-existent company fails."""
        result = self.registry.remove_company("Nonexistent Company", persist=False)
        
        self.assertFalse(result['success'])
        self.assertIn('not found', result['message'])
    
    def test_search_by_query(self):
        """Test searching companies by query."""
        results = self.registry.search_companies(query="test")
        
        self.assertGreaterEqual(len(results), 2)
        
        # Check results contain search term
        for result in results:
            self.assertIn('test', result['name'].lower())
    
    def test_search_by_industry(self):
        """Test searching companies by industry."""
        results = self.registry.search_companies(industry="finance")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Test Bank')
    
    def test_search_by_region(self):
        """Test searching companies by region."""
        results = self.registry.search_companies(region="south")
        
        self.assertEqual(len(results), 2)
    
    def test_search_combined_filters(self):
        """Test searching with multiple filters."""
        results = self.registry.search_companies(
            query="company",
            industry="technology",
            region="south"
        )
        
        self.assertEqual(len(results), 2)
    
    def test_resolve_alias(self):
        """Test alias resolution."""
        canonical = self.registry.resolve_alias("TCA")
        self.assertEqual(canonical, "Test Company A")
        
        canonical = self.registry.resolve_alias("Test A")
        self.assertEqual(canonical, "Test Company A")
        
        # Test canonical name returns itself
        canonical = self.registry.resolve_alias("Test Company A")
        self.assertEqual(canonical, "Test Company A")
    
    def test_resolve_invalid_alias(self):
        """Test resolving invalid alias returns None."""
        canonical = self.registry.resolve_alias("Invalid Alias")
        self.assertIsNone(canonical)
    
    def test_get_company_info(self):
        """Test getting company information."""
        info = self.registry.get_company_info("Test Company A")
        
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'Test Company A')
        self.assertEqual(info['industry'], 'technology')
        self.assertEqual(info['region'], 'south')
        self.assertIn('website', info['metadata'])
    
    def test_get_company_info_by_alias(self):
        """Test getting company info using alias."""
        info = self.registry.get_company_info("TCA")
        
        self.assertIsNotNone(info)
        self.assertEqual(info['name'], 'Test Company A')
    
    def test_get_all_companies(self):
        """Test getting all companies."""
        companies = self.registry.get_all_companies()
        
        self.assertEqual(len(companies), 3)
        self.assertIn('Test Company A', companies)
        self.assertIn('Test Bank', companies)
    
    def test_get_statistics(self):
        """Test getting registry statistics."""
        stats = self.registry.get_statistics()
        
        self.assertEqual(stats['total_companies'], 3)
        self.assertEqual(stats['total_aliases'], 6)
        self.assertEqual(stats['industries']['technology'], 2)
        self.assertEqual(stats['industries']['finance'], 1)
        self.assertIn('technology', stats['industry_list'])
        self.assertIn('north', stats['region_list'])


class TestCompanyRegistryEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_invalid_config_path(self):
        """Test initialization with invalid config path."""
        # Registry should handle invalid path gracefully
        registry = CompanyRegistry("/nonexistent/path/config.json")
        
        # The registry should exist but reload should fail
        self.assertIsNotNone(registry)
        
        # Reload should report failure
        result = registry.reload()
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_add_company_missing_fields(self):
        """Test adding company with missing required fields."""
        temp_config = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        json.dump({}, temp_config, indent=2)
        temp_config.close()
        
        registry = CompanyRegistry(temp_config.name)
        
        result = registry.add_company(
            name="",
            industry="technology",
            region="south",
            persist=False
        )
        
        self.assertFalse(result['success'])
        
        Path(temp_config.name).unlink()
    
    def test_case_insensitive_search(self):
        """Test case-insensitive company search."""
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
                        "name": "TestCompany",
                        "aliases": ["TC"],
                        "metadata": {},
                        "added_date": "2025-10-18T00:00:00"
                    }
                ]
            }
        }
        
        json.dump(test_data, temp_config, indent=2)
        temp_config.close()
        
        registry = CompanyRegistry(temp_config.name)
        
        # Test case variations
        self.assertIsNotNone(registry.resolve_alias("testcompany"))
        self.assertIsNotNone(registry.resolve_alias("TESTCOMPANY"))
        self.assertIsNotNone(registry.resolve_alias("tc"))
        self.assertIsNotNone(registry.resolve_alias("TC"))
        
        Path(temp_config.name).unlink()


if __name__ == '__main__':
    unittest.main()
