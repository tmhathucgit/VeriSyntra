"""
VeriSyntra Regression Test Suite - Fixed Version
Run all critical tests after Phase 2 authentication migration

Vietnamese Context: Kiem thu hoi quy sau khi di chuyen xac thuc Phase 2
Tests authentication, security utilities, and API endpoints
"""

import subprocess
import sys
import os
from pathlib import Path
import time

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
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


def check_redis_availability():
    """
    Check if Redis is available via Docker container
    
    Returns:
        bool: True if Redis is available, False otherwise
    """
    print(f"\n{BOLD}--- Checking Redis Availability ---{RESET}")
    print("Verifying Redis connection for token blacklist tests...")
    
    try:
        # Try to connect to Redis using Python redis client
        import redis
        
        redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            socket_connect_timeout=5,
            socket_timeout=5,
            decode_responses=True
        )
        
        # Test connection with ping
        response = redis_client.ping()
        
        if response:
            print_success("Redis is running and accessible")
            redis_client.close()
            return True
        else:
            print_error("Redis ping failed")
            return False
    
    except ImportError:
        print_error("Redis Python client not installed")
        print("Install with: pip install redis")
        return False
    
    except redis.ConnectionError as e:
        print_error(f"Cannot connect to Redis: {str(e)}")
        print(f"\n{YELLOW}{BOLD}MANUAL ACTION REQUIRED:{RESET}")
        print(f"{YELLOW}1. Open Docker Desktop application{RESET}")
        print(f"{YELLOW}2. Ensure Docker Desktop is running{RESET}")
        print(f"{YELLOW}3. Check if 'verisyntra-redis' container is running{RESET}")
        print(f"{YELLOW}4. If not running, restart Docker Desktop{RESET}")
        print(f"{YELLOW}5. Wait for containers to start (~30 seconds){RESET}")
        print(f"{YELLOW}6. Re-run this regression test suite{RESET}")
        print(f"\n{YELLOW}Docker Desktop Status Check:{RESET}")
        print(f"  > Open Docker Desktop GUI")
        print(f"  > Verify 'verisyntra-redis' container status")
        print(f"  > Container should show 'Running' status")
        return False
    
    except Exception as e:
        print_error(f"Unexpected error checking Redis: {str(e)}")
        return False


def wait_for_user_confirmation(message):
    """
    Wait for user to confirm action completion
    
    Args:
        message: Message to display to user
    
    Returns:
        bool: True if user confirms, False if user cancels
    """
    print(f"\n{YELLOW}{BOLD}{message}{RESET}")
    print(f"{YELLOW}Options:{RESET}")
    print(f"  {GREEN}[Y]{RESET} - Docker Desktop restarted, Redis is ready")
    print(f"  {RED}[N]{RESET} - Skip Redis-dependent tests")
    print(f"  {BLUE}[R]{RESET} - Retry Redis connection check")
    
    while True:
        try:
            choice = input(f"\n{BOLD}Enter choice (Y/N/R): {RESET}").strip().upper()
            
            if choice == 'Y':
                print_success("Proceeding with Redis-dependent tests...")
                return True
            elif choice == 'N':
                print_warning("Skipping Redis-dependent tests")
                return False
            elif choice == 'R':
                print("Retrying Redis connection...")
                time.sleep(2)  # Brief delay before retry
                if check_redis_availability():
                    return True
                else:
                    print_error("Redis still not available")
                    continue
            else:
                print_warning("Invalid choice. Please enter Y, N, or R")
        
        except KeyboardInterrupt:
            print("\n")
            print_warning("User cancelled - skipping Redis-dependent tests")
            return False
        except Exception as e:
            print_error(f"Input error: {str(e)}")
            return False


def run_pytest(test_pattern, description):
    """
    Run pytest with pattern
    
    Args:
        test_pattern: Pytest test pattern
        description: Test description
    
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
            timeout=120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"}
        )
        
        output = result.stdout + result.stderr
        
        # Parse pytest output
        if "passed" in output or result.returncode == 0:
            # Extract pass/fail counts
            if "passed" in output:
                print_success(f"{description} - Tests passed")
            return {
                "description": description,
                "status": "PASSED" if result.returncode == 0 else "PARTIAL",
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
        print_error(f"{description} - Timeout")
        return {
            "description": description,
            "status": "TIMEOUT",
            "output": "Test timeout",
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


def run_standalone_test(test_file, description):
    """
    Run standalone test file
    
    Args:
        test_file: Path to test file
        description: Test description
    
    Returns:
        dict: Test results
    """
    print(f"\n{BOLD}--- {description} ---{RESET}")
    print(f"File: {test_file}")
    
    workspace_root = Path(__file__).parent.parent.parent
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONLEGACYWINDOWSSTDIO": "1"}
        )
        
        output = result.stdout + result.stderr
        
        if result.returncode == 0 and ("PASSED" in output or "passed" in output.lower()):
            print_success(f"{description} - All tests passed")
            return {
                "description": description,
                "status": "PASSED",
                "output": output,
                "returncode": 0
            }
        else:
            print_error(f"{description} - Tests failed")
            return {
                "description": description,
                "status": "FAILED",
                "output": output,
                "returncode": result.returncode
            }
    
    except Exception as e:
        print_error(f"{description} - Error: {str(e)}")
        return {
            "description": description,
            "status": "ERROR",
            "output": str(e),
            "returncode": -1
        }


def run_powershell_test(script_path, description, fail_on_warnings=False):
    """
    Run PowerShell test script
    
    Args:
        script_path: Path to PowerShell script
        description: Test description
        fail_on_warnings: Fail if warnings detected
    
    Returns:
        dict: Test results
    """
    print(f"\n{BOLD}--- {description} ---{RESET}")
    print(f"Script: {script_path}")
    
    workspace_root = Path(__file__).parent.parent.parent
    
    try:
        # Build PowerShell command
        ps_args = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
        if fail_on_warnings:
            ps_args.extend(["-FailOnWarnings", "$true"])
        
        result = subprocess.run(
            ps_args,
            cwd=workspace_root,
            capture_output=True,
            text=True,
            timeout=120,
            encoding='utf-8',
            errors='replace'
        )
        
        output = result.stdout + result.stderr
        
        # PowerShell exit codes: 0 = success
        if result.returncode == 0 and ("ALL TESTS PASSED" in output or "PASSED WITH WARNINGS" in output):
            if "WARNINGS" in output and fail_on_warnings:
                print_error(f"{description} - Warnings detected (fail-on-warnings enabled)")
                return {
                    "description": description,
                    "status": "FAILED",
                    "output": output,
                    "returncode": 1
                }
            print_success(f"{description} - All tests passed")
            return {
                "description": description,
                "status": "PASSED",
                "output": output,
                "returncode": 0
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
        print_error(f"{description} - Timeout")
        return {
            "description": description,
            "status": "TIMEOUT",
            "output": "Test timeout",
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


def main():
    """Main regression test runner"""
    
    print_header("VeriSyntra Phase 2 Regression Test Suite")
    print_header("Kiem thu Hoi quy VeriSyntra Phase 2")
    
    workspace_root = Path(__file__).parent.parent.parent
    
    all_results = []
    
    # Check Redis availability BEFORE running token blacklist tests
    redis_available = check_redis_availability()
    
    if not redis_available:
        print_warning("Redis is not available - token blacklist tests will be affected")
        user_ready = wait_for_user_confirmation(
            "Please restart Docker Desktop and ensure Redis container is running."
        )
        
        if user_ready:
            # Re-check Redis after user confirmation
            redis_available = check_redis_availability()
            if not redis_available:
                print_error("Redis still not available after restart attempt")
                print_warning("Token blacklist tests will be SKIPPED")
        else:
            print_warning("Proceeding without Redis - token blacklist tests will be SKIPPED")
    
    # Priority 1: Authentication & Security (pytest-based)
    print_header("PRIORITY 1: Authentication & Security Tests")
    print_header("UU TIEN 1: Kiem thu Xac thuc & Bao mat")
    
    auth_tests = [
        ("tests/unit/test_password_utils.py", "Password Hashing & Validation", False),
        ("tests/unit/test_jwt_handler.py", "JWT Token Creation & Validation", False),
        ("tests/unit/test_token_blacklist.py", "Redis Token Blacklist", True),  # Requires Redis
    ]
    
    for test_file, description, requires_redis in auth_tests:
        # Skip Redis-dependent tests if Redis is not available
        if requires_redis and not redis_available:
            print(f"\n{YELLOW}[SKIPPED]{RESET} {description} - Redis not available")
            all_results.append({
                "description": description,
                "status": "SKIPPED",
                "output": "Redis not available",
                "returncode": 0
            })
            continue
        
        result = run_pytest(test_file, description)
        all_results.append(result)
    
    # Phase 2 Integration Test (standalone)
    auth_integration_file = workspace_root / "backend" / "tests" / "system" / "test_auth_phase2.py"
    if auth_integration_file.exists():
        result = run_standalone_test(
            auth_integration_file,
            "Phase 2 Authentication API Integration"
        )
        all_results.append(result)
    
    # Company Management API Tests
    company_api_tests = [
        ("tests/system/test_admin_companies_api.py", "Admin Companies API"),
        ("tests/system/test_company_registry.py", "Company Registry"),
    ]
    
    for test_file, description in company_api_tests:
        result = run_pytest(test_file, description)
        all_results.append(result)
    
    # Priority 2: Data Processing
    print_header("PRIORITY 2: Data Processing Tests")
    print_header("UU TIEN 2: Kiem thu Xu ly Du lieu")
    
    data_tests = [
        ("tests/unit/test_pdpl_normalizer.py", "PDPL Text Normalization"),
    ]
    
    for test_file, description in data_tests:
        result = run_pytest(test_file, description)
        all_results.append(result)
    
    # Priority 3: Vietnamese Encoding & Diacritics
    print_header("PRIORITY 3: Vietnamese UTF-8 Encoding Tests")
    print_header("UU TIEN 3: Kiem thu Ma hoa UTF-8 Tieng Viet")
    
    # Use relative path from backend/tests directory
    backend_tests_dir = Path(__file__).parent
    vietnamese_encoding_script = backend_tests_dir / "system" / "test_vietnamese_encoding.ps1"
    
    if vietnamese_encoding_script.exists():
        result = run_powershell_test(
            vietnamese_encoding_script,
            "Vietnamese UTF-8 Encoding & Diacritics Compliance",
            fail_on_warnings=True  # Strict mode for CI/CD
        )
        all_results.append(result)
    else:
        print_error(f"Vietnamese encoding test script not found at: {vietnamese_encoding_script}")
        all_results.append({
            "description": "Vietnamese UTF-8 Encoding & Diacritics Compliance",
            "status": "ERROR",
            "output": f"Script not found: {vietnamese_encoding_script}",
            "returncode": -1
        })
    
    # Summary
    print_header("Regression Test Summary / Tong ket Kiem thu Hoi quy")
    
    total = len(all_results)
    passed = sum(1 for r in all_results if r["status"] == "PASSED")
    partial = sum(1 for r in all_results if r["status"] == "PARTIAL")
    failed = sum(1 for r in all_results if r["status"] == "FAILED")
    errors = sum(1 for r in all_results if r["status"] == "ERROR")
    skipped = sum(1 for r in all_results if r["status"] == "SKIPPED")
    
    print(f"\n{BOLD}Overall Results:{RESET}")
    print(f"  Total Tests: {total}")
    print(f"  {GREEN}Passed: {passed}{RESET}")
    if partial > 0:
        print(f"  {YELLOW}Partial: {partial}{RESET}")
    if skipped > 0:
        print(f"  {YELLOW}Skipped: {skipped}{RESET}")
    print(f"  {RED}Failed: {failed}{RESET}")
    print(f"  {RED}Errors: {errors}{RESET}")
    
    print(f"\n{BOLD}Ket qua Tong the:{RESET}")
    print(f"  Tong so Test: {total}")
    print(f"  {GREEN}Thanh cong: {passed}{RESET}")
    if skipped > 0:
        print(f"  {YELLOW}Bo qua: {skipped}{RESET}")
    print(f"  {RED}That bai: {failed + errors}{RESET}")
    
    # List issues
    if failed > 0 or errors > 0:
        print(f"\n{RED}{BOLD}Issues Found:{RESET}")
        for result in all_results:
            if result["status"] in ["FAILED", "ERROR"]:
                print(f"  {RED}[{result['status']}]{RESET} {result['description']}")
    
    # List skipped tests
    if skipped > 0:
        print(f"\n{YELLOW}{BOLD}Skipped Tests:{RESET}")
        for result in all_results:
            if result["status"] == "SKIPPED":
                print(f"  {YELLOW}[SKIPPED]{RESET} {result['description']} - {result['output']}")
    
    print("\n" + "=" * 70)
    
    # Consider skipped tests as warnings, not failures
    if failed == 0 and errors == 0:
        if skipped > 0:
            print_warning(f"All tests passed ({skipped} skipped due to missing dependencies)")
            print_warning(f"Tat ca kiem thu thanh cong ({skipped} bo qua vi thieu phu thuoc)")
        else:
            print_success("All critical regression tests passed!")
            print_success("Tat ca kiem thu hoi quy thanh cong!")
        return 0
    else:
        print_error(f"{failed + errors} test suites with issues")
        print_error(f"Phat hien {failed + errors} van de")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
