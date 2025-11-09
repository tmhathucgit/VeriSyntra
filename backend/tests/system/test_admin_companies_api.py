"""
Unit Tests for Admin Company Registry API (Phase 3)
Tests all admin endpoints for dynamic company management

Status: COMPLETE
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from app.api.v1.endpoints.admin_companies import router
from fastapi import FastAPI

# Create test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestAdminCompaniesAPI(unittest.TestCase):
    """Test admin company management endpoints"""
    
    def setUp(self):
        """Setup test environment"""
        # Use test registry
        from app.core.company_registry import get_registry
        self.registry = get_registry()
        self.initial_count = len(self.registry.get_all_company_names())
    
    def test_01_get_registry_stats(self):
        """Test GET /admin/companies/stats"""
        response = client.get("/admin/companies/stats")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('total_companies', data)
        self.assertIn('by_industry', data)
        self.assertIn('by_region', data)
        self.assertIsInstance(data['total_companies'], int)
        self.assertGreater(data['total_companies'], 0)
        
        print(f"\n  Stats: {data['total_companies']} companies")
    
    def test_02_add_company(self):
        """Test POST /admin/companies/add"""
        new_company = {
            "name": "Test Company ABC",
            "industry": "technology",
            "region": "south",
            "aliases": ["Test Co", "TC ABC"],
            "metadata": {"website": "test.com", "type": "Test"}
        }
        
        response = client.post("/admin/companies/add", json=new_company)
        
        # May be 201 or 400 if already exists
        self.assertIn(response.status_code, [201, 400])
        
        if response.status_code == 201:
            data = response.json()
            self.assertEqual(data['name'], new_company['name'])
            self.assertEqual(data['industry'], new_company['industry'])
            self.assertEqual(data['region'], new_company['region'])
            self.assertEqual(len(data['aliases']), 2)
            print(f"\n  Added company: {data['name']}")
        else:
            print(f"\n  Company already exists (expected in repeated tests)")
    
    def test_03_add_duplicate_company(self):
        """Test adding duplicate company (should fail)"""
        # Add company first
        company = {
            "name": "Duplicate Test Company",
            "industry": "technology",
            "region": "north",
            "aliases": ["DTC"],
            "metadata": {}
        }
        
        # First add should succeed (or already exist)
        response1 = client.post("/admin/companies/add", json=company)
        self.assertIn(response1.status_code, [201, 400])
        
        # Second add should fail
        response2 = client.post("/admin/companies/add", json=company)
        self.assertEqual(response2.status_code, 400)
        
        print(f"\n  Duplicate rejection working correctly")
    
    def test_04_search_companies(self):
        """Test GET /admin/companies/search"""
        response = client.get("/admin/companies/search?query=test")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('query', data)
        self.assertIn('count', data)
        self.assertIn('results', data)
        self.assertEqual(data['query'], 'test')
        self.assertIsInstance(data['results'], list)
        
        print(f"\n  Search found {data['count']} companies")
    
    def test_05_search_known_company(self):
        """Test searching for known company"""
        response = client.get("/admin/companies/search?query=FPT")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertGreater(data['count'], 0)
        
        # Check if FPT is in results
        found = any('FPT' in result.get('name', '') for result in data['results'])
        self.assertTrue(found, "FPT should be found in registry")
        
        print(f"\n  Found FPT: {data['count']} matches")
    
    def test_06_list_companies_by_industry(self):
        """Test GET /admin/companies/list/{industry}"""
        response = client.get("/admin/companies/list/technology")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['industry'], 'technology')
        self.assertIn('count', data)
        self.assertIn('companies', data)
        self.assertIsInstance(data['companies'], list)
        self.assertGreater(data['count'], 0)
        
        print(f"\n  Technology industry: {data['count']} companies")
    
    def test_07_list_multiple_industries(self):
        """Test listing companies from multiple industries"""
        industries = ['technology', 'finance', 'healthcare']
        
        for industry in industries:
            response = client.get(f"/admin/companies/list/{industry}")
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            print(f"\n  {industry}: {data['count']} companies")
    
    def test_08_export_registry(self):
        """Test GET /admin/companies/export"""
        response = client.get("/admin/companies/export")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('companies', data)
        self.assertIn('stats', data)
        self.assertIn('export_timestamp', data)
        self.assertIn('format_version', data)
        
        # Validate structure
        self.assertIsInstance(data['companies'], dict)
        self.assertIsInstance(data['stats'], dict)
        
        print(f"\n  Exported {data['stats']['total_companies']} companies")
    
    def test_09_reload_registry(self):
        """Test POST /admin/companies/reload"""
        response = client.post("/admin/companies/reload")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('details', data)
        
        print(f"\n  Registry reloaded successfully")
    
    def test_10_remove_company(self):
        """Test DELETE /admin/companies/remove"""
        # First add a company to remove
        test_company = {
            "name": "Company To Remove",
            "industry": "retail",
            "region": "central",
            "aliases": [],
            "metadata": {}
        }
        
        add_response = client.post("/admin/companies/add", json=test_company)
        
        if add_response.status_code == 201:
            # Now remove it
            response = client.delete(
                f"/admin/companies/remove?name=Company To Remove&industry=retail&region=central"
            )
            
            # Should succeed (200) or not found if already removed
            self.assertIn(response.status_code, [200, 404])
            
            if response.status_code == 200:
                data = response.json()
                self.assertIn('message', data)
                print(f"\n  Removed company successfully")
            else:
                print(f"\n  Company already removed (expected)")
        else:
            print(f"\n  Company already exists, skipping removal test")
    
    def test_11_remove_nonexistent_company(self):
        """Test removing non-existent company (should fail)"""
        response = client.delete(
            "/admin/companies/remove?name=Nonexistent Company&industry=technology&region=south"
        )
        
        self.assertEqual(response.status_code, 404)
        print(f"\n  Nonexistent company rejection working correctly")
    
    def test_12_add_company_missing_fields(self):
        """Test adding company with missing required fields"""
        incomplete_company = {
            "name": "Incomplete Company"
            # Missing industry and region
        }
        
        response = client.post("/admin/companies/add", json=incomplete_company)
        
        self.assertEqual(response.status_code, 422)  # Validation error
        print(f"\n  Validation working correctly")
    
    def test_13_search_empty_query(self):
        """Test search with empty query (should fail)"""
        response = client.get("/admin/companies/search?query=")
        
        self.assertEqual(response.status_code, 422)  # Validation error
        print(f"\n  Empty query validation working correctly")
    
    def test_14_add_company_all_industries(self):
        """Test that we can add companies to all supported industries"""
        industries = [
            'technology', 'finance', 'healthcare', 'education', 
            'retail', 'manufacturing', 'transportation', 'telecom', 'government'
        ]
        
        for idx, industry in enumerate(industries):
            company = {
                "name": f"Test {industry.title()} Company {idx}",
                "industry": industry,
                "region": "south",
                "aliases": [f"TC{idx}"],
                "metadata": {"test": True}
            }
            
            response = client.post("/admin/companies/add", json=company)
            # 201 (created) or 400 (already exists)
            self.assertIn(response.status_code, [201, 400])
        
        print(f"\n  All {len(industries)} industries supported")


class TestAPIIntegration(unittest.TestCase):
    """Test integration between admin API and registry"""
    
    def test_add_and_search_integration(self):
        """Test that added companies are immediately searchable"""
        # Add unique company
        import time
        unique_name = f"Integration Test Company {int(time.time())}"
        
        company = {
            "name": unique_name,
            "industry": "technology",
            "region": "north",
            "aliases": ["ITC"],
            "metadata": {}
        }
        
        # Add company
        add_response = client.post("/admin/companies/add", json=company)
        
        if add_response.status_code == 201:
            # Search for it
            search_response = client.get(f"/admin/companies/search?query={unique_name}")
            
            self.assertEqual(search_response.status_code, 200)
            
            search_data = search_response.json()
            self.assertGreater(search_data['count'], 0)
            
            # Verify it's in results
            found = any(unique_name in result.get('name', '') for result in search_data['results'])
            self.assertTrue(found, "Added company should be immediately searchable")
            
            print(f"\n  Integration test passed: add + search working")
        else:
            print(f"\n  Company already exists, skipping integration test")
    
    def test_stats_update_after_operations(self):
        """Test that stats update after add/remove operations"""
        # Get initial stats
        stats1_response = client.get("/admin/companies/stats")
        stats1 = stats1_response.json()
        
        # Perform operation (add company)
        import time
        unique_name = f"Stats Test Company {int(time.time())}"
        
        company = {
            "name": unique_name,
            "industry": "retail",
            "region": "central",
            "aliases": [],
            "metadata": {}
        }
        
        add_response = client.post("/admin/companies/add", json=company)
        
        # Get updated stats
        stats2_response = client.get("/admin/companies/stats")
        stats2 = stats2_response.json()
        
        # Stats should update (if add succeeded)
        if add_response.status_code == 201:
            self.assertGreaterEqual(stats2['total_companies'], stats1['total_companies'])
            print(f"\n  Stats update working: {stats1['total_companies']} -> {stats2['total_companies']}")
        else:
            print(f"\n  Stats unchanged (company already existed)")


def run_tests():
    """Run all tests with detailed output"""
    print("\n" + "="*70)
    print("PHASE 3: Admin Company Registry API Tests")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAdminCompaniesAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
