"""
Unit Tests for VeriAIDPO Classification API (Phase 3)
Tests classification endpoints with company normalization

Status: COMPLETE
"""

import unittest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from app.api.v1.endpoints.veriaidpo_classification import router
from fastapi import FastAPI

# Create test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestVeriAIDPOClassificationAPI(unittest.TestCase):
    """Test VeriAIDPO classification endpoints"""
    
    def test_01_health_check(self):
        """Test GET /veriaidpo/health"""
        response = client.get("/veriaidpo/health")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('components', data)
        self.assertIn('company_registry', data['components'])
        self.assertIn('text_normalizer', data['components'])
        self.assertIn('model_types', data['components'])
        
        print(f"\n  VeriAIDPO service healthy")
        print(f"  Model types available: {len(data['components']['model_types']['available'])}")
    
    def test_02_classify_with_company_normalization(self):
        """Test POST /veriaidpo/classify with company name"""
        request = {
            "text": "Shopee VN thu thap so dien thoai de lien he giao hang",
            "model_type": "principles",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)
        self.assertIn('category_id', data)
        self.assertIn('normalized_text', data)
        self.assertIn('detected_companies', data)
        
        # Verify normalization happened
        self.assertIn('[COMPANY]', data['normalized_text'])
        self.assertNotIn('Shopee', data['normalized_text'])
        
        # Verify company was detected
        self.assertGreater(len(data['detected_companies']), 0)
        
        print(f"\n  Classification successful")
        print(f"  Prediction: {data['prediction']} (confidence: {data['confidence']})")
        print(f"  Normalized: '{data['normalized_text'][:60]}...'")
        print(f"  Companies detected: {len(data['detected_companies'])}")
    
    def test_03_classify_without_metadata(self):
        """Test classification without metadata"""
        request = {
            "text": "Tiki thu thap email khach hang",
            "model_type": "legal_basis",
            "language": "vi",
            "include_metadata": False
        }
        
        response = client.post("/veriaidpo/classify", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('prediction', data)
        self.assertIn('confidence', data)
        self.assertIsNone(data.get('normalized_text'))
        self.assertIsNone(data.get('detected_companies'))
        
        print(f"\n  Classification without metadata working")
    
    def test_04_classify_all_model_types(self):
        """Test classification with all model types"""
        model_types = [
            'principles', 'legal_basis', 'breach_triage', 'cross_border',
            'consent_type', 'data_sensitivity', 'dpo_tasks', 'risk_level',
            'compliance_status', 'regional', 'industry'
        ]
        
        for model_type in model_types:
            request = {
                "text": "FPT Corporation thu thap du lieu ca nhan",
                "model_type": model_type,
                "language": "vi",
                "include_metadata": False
            }
            
            response = client.post("/veriaidpo/classify", json=request)
            
            self.assertEqual(response.status_code, 200, 
                           f"Model type '{model_type}' should work")
            
            data = response.json()
            self.assertEqual(data['model_type'], model_type)
        
        print(f"\n  All {len(model_types)} model types working")
    
    def test_05_classify_invalid_model_type(self):
        """Test classification with invalid model type"""
        request = {
            "text": "Test text",
            "model_type": "invalid_model",
            "language": "vi",
            "include_metadata": False
        }
        
        response = client.post("/veriaidpo/classify", json=request)
        
        self.assertEqual(response.status_code, 400)
        
        print(f"\n  Invalid model type rejection working")
    
    def test_06_classify_legal_basis_endpoint(self):
        """Test POST /veriaidpo/classify-legal-basis"""
        request = {
            "text": "Vietcombank thu thap CMND dua tren hop dong mo tai khoan",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify-legal-basis", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['model_type'], 'legal_basis')
        self.assertIn('prediction', data)
        
        print(f"\n  Legal basis classification: {data['prediction']}")
    
    def test_07_classify_breach_severity_endpoint(self):
        """Test POST /veriaidpo/classify-breach-severity"""
        request = {
            "text": "MoMo bi ro ri 10000 so dien thoai khach hang",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify-breach-severity", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['model_type'], 'breach_triage')
        self.assertIn('prediction', data)
        
        print(f"\n  Breach severity: {data['prediction']}")
    
    def test_08_classify_cross_border_endpoint(self):
        """Test POST /veriaidpo/classify-cross-border"""
        request = {
            "text": "Grab VN chuyen du lieu sang Singapore de xu ly",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify-cross-border", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['model_type'], 'cross_border')
        self.assertIn('prediction', data)
        
        print(f"\n  Cross-border: {data['prediction']}")
    
    def test_09_normalize_text_endpoint(self):
        """Test POST /veriaidpo/normalize"""
        request = {
            "text": "Shopee VN va Tiki deu thu thap email khach hang",
            "normalize_companies": True,
            "normalize_persons": False,
            "normalize_locations": False
        }
        
        response = client.post("/veriaidpo/normalize", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('original_text', data)
        self.assertIn('normalized_text', data)
        self.assertIn('detected_companies', data)
        self.assertIn('normalization_count', data)
        
        # Verify normalization
        self.assertIn('[COMPANY]', data['normalized_text'])
        self.assertGreater(len(data['detected_companies']), 0)
        
        print(f"\n  Normalization: {data['normalization_count']} entities normalized")
        print(f"  Companies detected: {data['detected_companies']}")
    
    def test_10_normalize_multiple_companies(self):
        """Test normalization with multiple companies"""
        request = {
            "text": "FPT, Viettel va VNPT deu la cong ty cong nghe Viet Nam",
            "normalize_companies": True,
            "normalize_persons": False,
            "normalize_locations": False
        }
        
        response = client.post("/veriaidpo/normalize", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Should detect multiple companies
        self.assertGreater(len(data['detected_companies']), 1)
        
        # Should have multiple [COMPANY] tokens
        company_count = data['normalized_text'].count('[COMPANY]')
        self.assertGreater(company_count, 1)
        
        print(f"\n  Multiple companies normalized: {len(data['detected_companies'])} detected")
        print(f"  Normalized text: '{data['normalized_text']}'")
    
    def test_11_classify_with_multiple_companies(self):
        """Test classification with multiple companies in text"""
        request = {
            "text": "Shopee VN va Tiki deu thu thap du lieu ca nhan de goi y san pham",
            "model_type": "principles",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Should detect multiple companies
        self.assertGreater(len(data['detected_companies']), 1)
        
        # Normalized text should have multiple [COMPANY] tokens
        company_count = data['normalized_text'].count('[COMPANY]')
        self.assertGreater(company_count, 1)
        
        print(f"\n  Multiple companies in classification: {len(data['detected_companies'])} detected")
    
    def test_12_classify_with_alias(self):
        """Test classification with company alias"""
        request = {
            "text": "VCB thu thap thong tin khach hang de mo tai khoan",
            "model_type": "legal_basis",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # VCB is alias for Vietcombank
        # Should be normalized
        self.assertIn('[COMPANY]', data['normalized_text'])
        
        print(f"\n  Alias recognition working")
        print(f"  Detected: {data['detected_companies']}")
    
    def test_13_classify_without_company(self):
        """Test classification with text containing no company names"""
        request = {
            "text": "Doanh nghiep can bao ve du lieu ca nhan theo PDPL 2025",
            "model_type": "principles",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Should work even without company names
        self.assertIn('prediction', data)
        
        # No companies detected
        self.assertEqual(len(data['detected_companies']), 0)
        
        # Text should be unchanged
        self.assertEqual(data['normalized_text'], request['text'])
        
        print(f"\n  Classification without company names working")
    
    def test_14_processing_metadata(self):
        """Test that processing metadata is included"""
        request = {
            "text": "Test classification with metadata",
            "model_type": "principles",
            "language": "vi",
            "include_metadata": True
        }
        
        response = client.post("/veriaidpo/classify", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Check processing metadata
        self.assertIn('processing_metadata', data)
        metadata = data['processing_metadata']
        
        self.assertIn('processing_time_ms', metadata)
        self.assertIn('normalization_applied', metadata)
        self.assertIn('companies_detected', metadata)
        self.assertIn('model_categories', metadata)
        self.assertIn('timestamp', metadata)
        
        print(f"\n  Processing metadata: {metadata['processing_time_ms']}ms")


class TestNormalizationAccuracy(unittest.TestCase):
    """Test normalization accuracy and edge cases"""
    
    def test_normalization_case_insensitive(self):
        """Test that normalization is case-insensitive"""
        request = {
            "text": "SHOPEE VN va shopee vn va Shopee VN",
            "normalize_companies": True,
            "normalize_persons": False,
            "normalize_locations": False
        }
        
        response = client.post("/veriaidpo/normalize", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # All variations should be normalized
        self.assertNotIn('SHOPEE', data['normalized_text'])
        self.assertNotIn('shopee', data['normalized_text'])
        self.assertNotIn('Shopee', data['normalized_text'])
        
        print(f"\n  Case-insensitive normalization working")
    
    def test_normalization_preserves_context(self):
        """Test that normalization preserves surrounding context"""
        request = {
            "text": "Truoc khi Tiki thu thap email, khach hang phai dong y",
            "normalize_companies": True,
            "normalize_persons": False,
            "normalize_locations": False
        }
        
        response = client.post("/veriaidpo/normalize", json=request)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Context should be preserved
        self.assertIn('Truoc khi', data['normalized_text'])
        self.assertIn('thu thap email', data['normalized_text'])
        self.assertIn('khach hang phai dong y', data['normalized_text'])
        
        # Only company should be replaced
        self.assertIn('[COMPANY]', data['normalized_text'])
        self.assertNotIn('Tiki', data['normalized_text'])
        
        print(f"\n  Context preservation working")


def run_tests():
    """Run all tests with detailed output"""
    print("\n" + "="*70)
    print("PHASE 3: VeriAIDPO Classification API Tests")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestVeriAIDPOClassificationAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestNormalizationAccuracy))
    
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
