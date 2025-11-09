"""
VeriSyntra Machine Learning Test Suite
Run ML model and dataset tests independently from backend regression tests

Vietnamese Context: Kiem thu Mo hinh Hoc may VeriAiDPO
Tests model inference, dataset generation, and ML API endpoints

Usage:
    python backend/tests/run_ml_tests.py              # Run all ML tests
    python backend/tests/run_ml_tests.py --quick      # Skip slow dataset tests
    python backend/tests/run_ml_tests.py --models-only # Only model inference tests
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{BOLD}{'=' * 70}{RESET}")
    print(f"{BLUE}{BOLD}{text}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 70}{RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}[OK]{RESET} {text}")


def print_error(text):
    """Print error message"""
    print(f"{RED}[ERROR]{RESET} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}[WARNING]{RESET} {text}")


def print_info(text):
    """Print info message"""
    print(f"{CYAN}[INFO]{RESET} {text}")


def run_pytest(test_pattern, description, timeout=300):
    """
    Run pytest with pattern
    
    Args:
        test_pattern: Pytest test pattern
        description: Test description
        timeout: Test timeout in seconds (default 300 = 5 minutes)
    
    Returns:
        dict: Test results
    """
    print(f"\n{BOLD}--- {description} ---{RESET}")
    print(f"Pattern: {test_pattern}")
    
    backend_dir = Path(__file__).parent.parent
    
    try:
        # Run pytest from backend directory
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                test_pattern,
                "-v",
                "--tb=short",
                "--color=yes"
            ],
            cwd=backend_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"}
        )
        
        output = result.stdout + result.stderr
        
        # Parse pytest output
        if "passed" in output or result.returncode == 0:
            print_success(f"{description} - Tests passed")
            return {
                "description": description,
                "status": "PASSED",
                "output": output,
                "returncode": result.returncode
            }
        else:
            print_error(f"{description} - Tests failed")
            return {
                "description": description,
                "status": "FAILED",
                "output": output,
                "returncode": result.returncode
            }
    
    except subprocess.TimeoutExpired:
        print_error(f"{description} - Timeout after {timeout}s")
        return {
            "description": description,
            "status": "TIMEOUT",
            "output": f"Test timeout after {timeout} seconds",
            "returncode": -1
        }
    
    except Exception as e:
        print_error(f"{description} - Error: {str(e)}")
        return {
            "description": description,
            "status": "ERROR",
            "output": str(e),
            "returncode": -1
        }


def check_ml_dependencies():
    """Check if ML dependencies are installed"""
    print_info("Checking ML dependencies...")
    
    required_packages = [
        'transformers',
        'torch',
        'datasets',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} installed")
        except ImportError:
            missing_packages.append(package)
            print_warning(f"{package} not installed")
    
    if missing_packages:
        print_warning(f"Missing packages: {', '.join(missing_packages)}")
        print_info("Install with: pip install transformers torch datasets")
        return False
    
    print_success("All ML dependencies installed")
    return True


def main():
    """Main ML test runner"""
    
    parser = argparse.ArgumentParser(
        description="VeriSyntra ML Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backend/tests/run_ml_tests.py                # Run all ML tests
  python backend/tests/run_ml_tests.py --quick        # Skip slow tests
  python backend/tests/run_ml_tests.py --models-only  # Only model tests
        """
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Skip slow dataset generation tests'
    )
    
    parser.add_argument(
        '--models-only',
        action='store_true',
        help='Run only model inference tests'
    )
    
    parser.add_argument(
        '--skip-deps-check',
        action='store_true',
        help='Skip ML dependencies check'
    )
    
    args = parser.parse_args()
    
    print_header("VeriSyntra Machine Learning Test Suite")
    print_header("Kiem thu Mo hinh Hoc may VeriAiDPO")
    
    # Check dependencies
    if not args.skip_deps_check:
        if not check_ml_dependencies():
            print_error("ML dependencies missing. Use --skip-deps-check to bypass.")
            return 1
    
    all_results = []
    
    # Priority 1: Model Inference & Integration
    print_header("PRIORITY 1: Model Inference & Integration Tests")
    print_header("UU TIEN 1: Kiem thu Suy dien Mo hinh")
    
    model_tests = [
        ("tests/ml/test_model_integration.py", "Model Integration & Loading", 180),
        ("tests/ml/test_all_model_types.py", "All Model Types & Variants", 300),
    ]
    
    for test_file, description, timeout in model_tests:
        if not args.models_only or 'model' in test_file:
            result = run_pytest(test_file, description, timeout=timeout)
            all_results.append(result)
    
    # Priority 2: API Endpoints (if not models-only)
    if not args.models_only:
        print_header("PRIORITY 2: VeriAiDPO Classification API Tests")
        print_header("UU TIEN 2: Kiem thu API Phan loai VeriAiDPO")
        
        api_tests = [
            ("tests/ml/test_veriaidpo_classification_api.py", "VeriAiDPO Classification API", 180),
        ]
        
        for test_file, description, timeout in api_tests:
            result = run_pytest(test_file, description, timeout=timeout)
            all_results.append(result)
    
    # Priority 3: Dataset Generation (if not quick mode and not models-only)
    if not args.quick and not args.models_only:
        print_header("PRIORITY 3: Vietnamese Dataset Generation Tests")
        print_header("UU TIEN 3: Kiem thu Tao Du lieu Tieng Viet")
        
        print_warning("Dataset generation tests can be slow (5-10 minutes)")
        
        dataset_tests = [
            ("tests/ml/test_vietnamese_hard_dataset_generator.py", "Vietnamese Hard Dataset Generator", 600),
        ]
        
        for test_file, description, timeout in dataset_tests:
            result = run_pytest(test_file, description, timeout=timeout)
            all_results.append(result)
    else:
        if args.quick:
            print_info("Skipping dataset generation tests (--quick mode)")
        if args.models_only:
            print_info("Skipping dataset tests (--models-only mode)")
    
    # Summary
    print_header("ML Test Summary / Tong ket Kiem thu ML")
    
    total = len(all_results)
    passed = sum(1 for r in all_results if r["status"] == "PASSED")
    failed = sum(1 for r in all_results if r["status"] == "FAILED")
    errors = sum(1 for r in all_results if r["status"] == "ERROR")
    timeouts = sum(1 for r in all_results if r["status"] == "TIMEOUT")
    
    print(f"\n{BOLD}Overall Results:{RESET}")
    print(f"  Total Tests: {total}")
    print(f"  {GREEN}Passed: {passed}{RESET}")
    print(f"  {RED}Failed: {failed}{RESET}")
    print(f"  {RED}Errors: {errors}{RESET}")
    if timeouts > 0:
        print(f"  {YELLOW}Timeouts: {timeouts}{RESET}")
    
    print(f"\n{BOLD}Ket qua Tong the:{RESET}")
    print(f"  Tong so Test: {total}")
    print(f"  {GREEN}Thanh cong: {passed}{RESET}")
    print(f"  {RED}That bai: {failed + errors + timeouts}{RESET}")
    
    # List issues
    if failed > 0 or errors > 0 or timeouts > 0:
        print(f"\n{RED}{BOLD}Issues Found:{RESET}")
        for result in all_results:
            if result["status"] in ["FAILED", "ERROR", "TIMEOUT"]:
                print(f"  {RED}[{result['status']}]{RESET} {result['description']}")
    
    # Performance summary
    print(f"\n{BOLD}Test Performance Notes:{RESET}")
    print(f"  {CYAN}Model loading:{RESET} First run slower (model download)")
    print(f"  {CYAN}Dataset generation:{RESET} Slower tests (use --quick to skip)")
    print(f"  {CYAN}API tests:{RESET} Require running backend server")
    
    print("\n" + "=" * 70)
    
    if failed == 0 and errors == 0 and timeouts == 0:
        print_success("All ML tests passed!")
        print_success("Tat ca kiem thu ML thanh cong!")
        return 0
    else:
        print_error(f"{failed + errors + timeouts} test suites with issues")
        print_error(f"Phat hien {failed + errors + timeouts} van de")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
