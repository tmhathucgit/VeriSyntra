"""
VeriAIDPO Model Integration Test
Tests the integrated model with backend API

Run this after starting the backend server:
    cd backend
    python main_prototype.py

Then in another terminal:
    python backend/test_model_integration.py
"""

import requests
import json
from typing import Dict, List


# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"
VERIAIDPO_ENDPOINT = f"{API_V1}/veriaidpo"

# Test samples (same as inference_test.py for comparison)
TEST_SAMPLES = [
    # Category 0: Lawfulness and Transparency
    {
        "text": "Cong ty phai thu thap du lieu ca nhan hop phap va minh bach theo quy dinh phap luat",
        "expected_category": 0,
        "expected_name": "Tuân thủ pháp luật và minh bạch"
    },
    {
        "text": "To chuc can dam bao tinh hop phap khi xu ly du lieu va phai thong bao ro rang cho chu the du lieu",
        "expected_category": 0,
        "expected_name": "Tuân thủ pháp luật và minh bạch"
    },
    
    # Category 1: Purpose Limitation
    {
        "text": "Thu thap du lieu khach hang chi duoc su dung dung voi muc dich kinh doanh da thong bao",
        "expected_category": 1,
        "expected_name": "Giới hạn mục đích"
    },
    {
        "text": "Cong ty chi duoc su dung du lieu ca nhan cho muc dich cu the da duoc chu the dong y",
        "expected_category": 1,
        "expected_name": "Giới hạn mục đích"
    },
    
    # Category 2: Data Minimization
    {
        "text": "Doanh nghiep chi nen thu thap luong du lieu toi thieu can thiet thay vi yeu cau qua nhieu thong tin",
        "expected_category": 2,
        "expected_name": "Tối thiểu hóa dữ liệu"
    },
    {
        "text": "Can han che so luong du lieu ca nhan thu thap chi lay nhung gi thuc su can thiet",
        "expected_category": 2,
        "expected_name": "Tối thiểu hóa dữ liệu"
    },
    
    # Category 3: Accuracy
    {
        "text": "To chuc phai dam bao du lieu ca nhan luon chinh xac va cap nhat day du",
        "expected_category": 3,
        "expected_name": "Chính xác"
    },
    {
        "text": "Doanh nghiep co trach nhiem kiem tra va sua chua du lieu sai lech hoac khong chinh xac",
        "expected_category": 3,
        "expected_name": "Chính xác"
    },
    
    # Category 4: Storage Limitation
    {
        "text": "Du lieu chi duoc luu tru trong khoang thoi gian can thiet sau do phai xoa bo",
        "expected_category": 4,
        "expected_name": "Giới hạn lưu trữ"
    },
    {
        "text": "Cong ty phai xoa du lieu khach hang sau khi het han hop dong va khong con muc dich luu giu",
        "expected_category": 4,
        "expected_name": "Giới hạn lưu trữ"
    },
    
    # Category 5: Security
    {
        "text": "To chuc phai ap dung cac bien phap bao mat manh de bao ve du lieu khoi truy cap trai phep",
        "expected_category": 5,
        "expected_name": "An toàn bảo mật"
    },
    {
        "text": "Doanh nghiep can ma hoa du lieu nhay cam va su dung xac thuc da yeu to de tang cuong an ninh",
        "expected_category": 5,
        "expected_name": "An toàn bảo mật"
    },
    
    # Category 6: Accountability
    {
        "text": "Cong ty phai chung minh tuan thu PDPL bang cach ghi chep day du cac hoat dong xu ly du lieu",
        "expected_category": 6,
        "expected_name": "Trách nhiệm giải trình"
    },
    {
        "text": "To chuc can luu tru ho so kiem toan de bao cao cho co quan quan ly ve viec tuan thu quy dinh",
        "expected_category": 6,
        "expected_name": "Trách nhiệm giải trình"
    },
    
    # Category 7: Data Subject Rights
    {
        "text": "Chu the du lieu co quyen yeu cau truy cap, sua doi hoac xoa bo du lieu ca nhan cua minh",
        "expected_category": 7,
        "expected_name": "Quyền của chủ thể dữ liệu"
    },
    {
        "text": "Nguoi dung co the rut lai su dong y va yeu cau chuyen du lieu sang nha cung cap khac",
        "expected_category": 7,
        "expected_name": "Quyền của chủ thể dữ liệu"
    }
]


def test_health_check():
    """Test 1: Health check endpoint"""
    print("\n[TEST 1] Health Check")
    print("=" * 60)
    
    try:
        response = requests.get(f"{VERIAIDPO_ENDPOINT}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Status: {data['status']}")
            print(f"[OK] Service: {data['service']}")
            
            # Model loader status
            model_status = data['components']['model_loader']['status']
            device = data['components']['model_loader']['device']
            print(f"[OK] Model Status: {model_status}")
            print(f"[OK] Device: {device}")
            
            return True
        else:
            print(f"[ERROR] Health check failed: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[ERROR] Health check exception: {e}")
        return False


def test_model_status():
    """Test 2: Model status endpoint"""
    print("\n[TEST 2] Model Status")
    print("=" * 60)
    
    try:
        response = requests.get(f"{VERIAIDPO_ENDPOINT}/model-status")
        
        if response.status_code == 200:
            data = response.json()
            model_info = data['model']
            
            print(f"[OK] Model Status: {model_info['status']}")
            print(f"[OK] Device: {model_info['device']}")
            print(f"[OK] Model Path: {model_info['model_path']}")
            
            if model_info['status'] == 'loaded':
                print(f"[OK] Labels: {model_info['num_labels']}")
                print(f"[OK] Vocabulary: {model_info['vocab_size']}")
            
            print(f"[OK] Categories: {data['categories']['total']}")
            
            return True
        else:
            print(f"[ERROR] Model status failed: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[ERROR] Model status exception: {e}")
        return False


def test_preload_model():
    """Test 3: Preload model"""
    print("\n[TEST 3] Preload Model")
    print("=" * 60)
    
    try:
        response = requests.post(f"{VERIAIDPO_ENDPOINT}/preload-model")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Status: {data['status']}")
            print(f"[OK] Message: {data['message']}")
            
            if 'model_info' in data:
                info = data['model_info']
                if 'num_labels' in info:
                    print(f"[OK] Model loaded: {info['num_labels']} labels, {info['vocab_size']} vocab")
            
            return True
        else:
            print(f"[ERROR] Preload failed: {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print(f"[ERROR] Preload exception: {e}")
        return False


def test_classification():
    """Test 4: Run classification on test samples"""
    print("\n[TEST 4] Classification Tests")
    print("=" * 60)
    
    correct = 0
    total = len(TEST_SAMPLES)
    results = []
    
    for i, sample in enumerate(TEST_SAMPLES, 1):
        try:
            # Send classification request
            payload = {
                "text": sample['text'],
                "model_type": "principles",
                "language": "vi",
                "include_metadata": True
            }
            
            response = requests.post(f"{VERIAIDPO_ENDPOINT}/classify", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                predicted_cat = data['category_id']
                expected_cat = sample['expected_category']
                confidence = data['confidence']
                
                is_correct = predicted_cat == expected_cat
                if is_correct:
                    correct += 1
                
                # Store result
                results.append({
                    'sample_id': i,
                    'expected': expected_cat,
                    'predicted': predicted_cat,
                    'confidence': confidence,
                    'correct': is_correct,
                    'text_preview': sample['text'][:50] + "..."
                })
                
                # Print result
                status = "[OK]" if is_correct else "[ERROR]"
                print(f"Test {i}/{total}: {status} Cat {expected_cat} -> Cat {predicted_cat} ({confidence:.2%})")
            
            else:
                print(f"Test {i}/{total}: [ERROR] Request failed: {response.status_code}")
                results.append({
                    'sample_id': i,
                    'error': f"HTTP {response.status_code}"
                })
        
        except Exception as e:
            print(f"Test {i}/{total}: [ERROR] Exception: {e}")
            results.append({
                'sample_id': i,
                'error': str(e)
            })
    
    # Print summary
    print("\n" + "=" * 60)
    print("CLASSIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {total - correct}")
    print(f"Accuracy: {correct / total * 100:.2f}%")
    
    # Average confidence
    valid_results = [r for r in results if 'confidence' in r]
    if valid_results:
        avg_conf = sum(r['confidence'] for r in valid_results) / len(valid_results)
        print(f"Average Confidence: {avg_conf:.2%}")
    
    # Per-category breakdown
    print("\nPer-Category Results:")
    for cat in range(8):
        cat_results = [r for r in valid_results if r['expected'] == cat]
        if cat_results:
            cat_correct = sum(1 for r in cat_results if r['correct'])
            cat_total = len(cat_results)
            cat_acc = cat_correct / cat_total * 100
            print(f"  Cat {cat}: {cat_acc:.1f}% ({cat_correct}/{cat_total})")
    
    return correct / total >= 0.5  # Pass if >50% accuracy


def test_normalization():
    """Test 5: Text normalization with company names"""
    print("\n[TEST 5] Text Normalization")
    print("=" * 60)
    
    test_texts = [
        "Shopee VN thu thap email khach hang",
        "Tiki va Lazada Vietnam deu yeu cau so dien thoai",
        "VNG Corporation xu ly du lieu nguoi dung"
    ]
    
    for i, text in enumerate(test_texts, 1):
        try:
            payload = {
                "text": text,
                "normalize_companies": True
            }
            
            response = requests.post(f"{VERIAIDPO_ENDPOINT}/normalize", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\nTest {i}/{len(test_texts)}:")
                print(f"  Original: {data['original_text']}")
                print(f"  Normalized: {data['normalized_text']}")
                print(f"  Companies: {', '.join(data['detected_companies']) if data['detected_companies'] else 'None'}")
                print(f"  Count: {data['normalization_count']}")
            else:
                print(f"Test {i}: [ERROR] Request failed: {response.status_code}")
        
        except Exception as e:
            print(f"Test {i}: [ERROR] Exception: {e}")
    
    return True


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "=" * 60)
    print("VERIAIDPO MODEL INTEGRATION TEST")
    print("=" * 60)
    print("Testing VeriAIDPO_Principles_VI_v1 model integration")
    print("Backend URL:", BASE_URL)
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Model Status", test_model_status),
        ("Preload Model", test_preload_model),
        ("Classification", test_classification),
        ("Normalization", test_normalization)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' crashed: {e}")
            failed += 1
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {passed / len(tests) * 100:.1f}%")
    
    if failed == 0:
        print("\n[OK] ALL TESTS PASSED - Integration successful!")
    else:
        print(f"\n[WARNING] {failed} test(s) failed - Review errors above")
    
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
