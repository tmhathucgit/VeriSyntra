#!/usr/bin/env python3
"""
Document Validation Script
Automatically checks VeriSyntra coding standards compliance

Usage:
    python validate_document.py 01_Data_Population_Manual_API.md
    python validate_document.py 02_Data_Population_Automated_Discovery.md
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Vietnamese diacritics pattern
VIETNAMESE_DIACRITICS = r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]'

# Non-diacritic Vietnamese words that should have diacritics
NON_DIACRITIC_VIOLATIONS = [
    'quan ly', 'khach hang', 'nhan vien', 'du lieu',
    'co so', 'muc dich', 'thong tin', 'nguoi dung',
    'dang nhap', 'tiep thi', 'ho tro', 'phan hoi',
    'khao sat', 'phan tich', 'kiem tra', 'dia chi',
    'so dien thoai', 'ngay sinh', 'mat khau',
    'ten dang nhap', 'dang ky', 'bat dau', 'ket thuc'
]

# Exception patterns (these are intentionally non-diacritic for validation purposes)
EXCEPTION_PATTERNS = [
    r'non_diacritic_keywords\s*=\s*\[',  # Validator arrays
    r'#.*non-diacritic',  # Comments about non-diacritic
    r'r"[^"]*"',  # Regex patterns in column names (e.g., r"ho_ten")
]


class DocumentValidator:
    """Validate VeriSyntra document coding standards"""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.content = filepath.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.stats: Dict = {}
    
    def validate_all(self) -> Tuple[bool, Dict]:
        """Run all validation checks"""
        print(f"\n[VALIDATING] {self.filepath.name}")
        print("=" * 60)
        
        # Run all checks
        self.check_hard_coding()
        self.check_vietnamese_diacritics()
        self.check_bilingual_support()
        self.check_no_emoji()
        self.generate_statistics()
        
        # Report results
        is_valid = len(self.errors) == 0
        self.print_report()
        
        return is_valid, {
            'errors': self.errors,
            'warnings': self.warnings,
            'stats': self.stats
        }
    
    def check_hard_coding(self):
        """Check for hard-coded values in functions"""
        print("\n[CHECK 1] Hard-Coding Violations...")
        
        violations = []
        in_function = False
        function_name = ""
        
        for i, line in enumerate(self.lines, 1):
            # Detect function definitions
            if re.match(r'\s*def\s+\w+', line):
                in_function = True
                match = re.search(r'def\s+(\w+)', line)
                function_name = match.group(1) if match else "unknown"
            
            # Check for dictionaries defined inside functions
            if in_function and re.search(r'{\s*$', line):
                # Look ahead for dictionary content
                if i + 1 < len(self.lines):
                    next_line = self.lines[i]
                    if re.search(r'["\'].*["\']:\s*["\']', next_line):
                        # Check if this is not a constant reference
                        if 'TRANSLATIONS' in line or '_VI' in line or '_EN' in line:
                            violations.append({
                                'line': i,
                                'function': function_name,
                                'type': 'hard_coded_dictionary',
                                'content': line.strip()
                            })
            
            # Reset on end of function
            if in_function and line.strip() == '':
                in_function = False
        
        if violations:
            self.errors.extend(violations)
            print(f"  [ERROR] Found {len(violations)} hard-coding violation(s)")
            for v in violations:
                print(f"    Line {v['line']}: {v['function']}() - {v['type']}")
        else:
            print("  [OK] No hard-coding violations found")
    
    def check_vietnamese_diacritics(self):
        """Check for missing Vietnamese diacritics"""
        print("\n[CHECK 2] Vietnamese Diacritics...")
        
        violations = []
        
        for i, line in enumerate(self.lines, 1):
            # Skip exception patterns
            is_exception = False
            for pattern in EXCEPTION_PATTERNS:
                if re.search(pattern, line):
                    is_exception = True
                    break
            
            if is_exception:
                continue
            
            # Check for non-diacritic Vietnamese words
            for word in NON_DIACRITIC_VIOLATIONS:
                if word in line.lower():
                    # Check if this line has any Vietnamese diacritics nearby
                    has_diacritics = bool(re.search(VIETNAMESE_DIACRITICS, line, re.IGNORECASE))
                    
                    # If no diacritics and not in a code identifier (e.g., variable name)
                    if not has_diacritics and not re.search(r'[a-z_]+\s*=\s*["\']', line):
                        violations.append({
                            'line': i,
                            'word': word,
                            'content': line.strip()[:80]
                        })
        
        if violations:
            self.errors.extend(violations)
            print(f"  [ERROR] Found {len(violations)} missing diacritic(s)")
            for v in violations[:5]:  # Show first 5
                print(f"    Line {v['line']}: '{v['word']}' should have diacritics")
        else:
            print("  [OK] All Vietnamese text has proper diacritics")
    
    def check_bilingual_support(self):
        """Check for Vietnamese-first bilingual pattern"""
        print("\n[CHECK 3] Bilingual Vietnamese-First Support...")
        
        # Count _vi and _en fields
        vi_fields = len(re.findall(r'\w+_vi[:\s]', self.content))
        en_fields = len(re.findall(r'\w+_en[:\s]', self.content))
        
        # Check for Optional[str] on _en fields
        optional_en = len(re.findall(r'\w+_en:\s*Optional\[str\]', self.content))
        required_vi = len(re.findall(r'\w+_vi:\s*str\s*=\s*Field\(\s*\.\.\.', self.content))
        
        self.stats['vietnamese_fields'] = vi_fields
        self.stats['english_fields'] = en_fields
        self.stats['optional_english_fields'] = optional_en
        self.stats['required_vietnamese_fields'] = required_vi
        
        if vi_fields > 0:
            print(f"  [OK] {vi_fields} Vietnamese-first fields found")
            print(f"  [OK] {en_fields} English secondary fields found")
            print(f"  [INFO] {required_vi} required Vietnamese fields")
            print(f"  [INFO] {optional_en} optional English fields")
        else:
            self.warnings.append({
                'type': 'no_bilingual_fields',
                'message': 'No _vi/_en bilingual fields detected'
            })
            print("  [WARNING] No bilingual fields detected")
    
    def check_no_emoji(self):
        """Check for emoji characters"""
        print("\n[CHECK 4] No Emoji Characters...")
        
        emoji_pattern = r'[✓✗⚠️•→🔧⏳]'
        violations = []
        
        for i, line in enumerate(self.lines, 1):
            if re.search(emoji_pattern, line):
                violations.append({
                    'line': i,
                    'content': line.strip()[:80]
                })
        
        if violations:
            self.errors.extend(violations)
            print(f"  [ERROR] Found {len(violations)} emoji character(s)")
            for v in violations[:5]:
                print(f"    Line {v['line']}: Contains emoji")
        else:
            print("  [OK] No emoji characters found")
    
    def generate_statistics(self):
        """Generate document statistics"""
        print("\n[CHECK 5] Document Statistics...")
        
        # Count constants
        enum_count = len(re.findall(r'class\s+\w+\(.*Enum\)', self.content))
        const_count = len(re.findall(r'^[A-Z_]+\s*[:=]', self.content, re.MULTILINE))
        
        # Count models
        model_count = len(re.findall(r'class\s+\w+\(BaseModel\)', self.content))
        
        # Count endpoints
        endpoint_count = len(re.findall(r'@router\.(get|post|put|delete)', self.content))
        
        self.stats.update({
            'total_lines': len(self.lines),
            'enums': enum_count,
            'constants': const_count,
            'pydantic_models': model_count,
            'api_endpoints': endpoint_count
        })
        
        print(f"  [INFO] Total lines: {self.stats['total_lines']}")
        print(f"  [INFO] Enums: {enum_count}")
        print(f"  [INFO] Constants: {const_count}")
        print(f"  [INFO] Pydantic models: {model_count}")
        print(f"  [INFO] API endpoints: {endpoint_count}")
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "=" * 60)
        print("VALIDATION REPORT")
        print("=" * 60)
        
        if len(self.errors) == 0:
            print("\n[OK] ALL CHECKS PASSED")
            print("\nDocument is compliant with VeriSyntra coding standards:")
            print("  [OK] Zero hard-coding")
            print("  [OK] Vietnamese diacritics enforced")
            print("  [OK] Vietnamese-first bilingual support")
            print("  [OK] No emoji characters")
        else:
            print(f"\n[ERROR] {len(self.errors)} ERROR(S) FOUND")
            print("\nFix required before approval:")
            for error in self.errors:
                print(f"  - Line {error.get('line', 'N/A')}: {error.get('type', 'error')}")
        
        if len(self.warnings) > 0:
            print(f"\n[WARNING] {len(self.warnings)} WARNING(S)")
            for warning in self.warnings:
                print(f"  - {warning.get('message', 'warning')}")
        
        print("\n" + "=" * 60)


def main():
    """Main validation function"""
    if len(sys.argv) < 2:
        print("Usage: python validate_document.py <document.md>")
        print("\nExample:")
        print("  python validate_document.py 01_Data_Population_Manual_API.md")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)
    
    validator = DocumentValidator(filepath)
    is_valid, results = validator.validate_all()
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
