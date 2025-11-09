#!/usr/bin/env python3
"""
Quick Document Validation
Runs automated checks and prints summary

Usage: python quick_validate.py 02_Data_Population_Automated_Discovery.md
"""

import sys
from pathlib import Path

def quick_validate(filepath: Path):
    """Quick validation with checklist"""
    
    if not filepath.exists():
        print(f"[ERROR] File not found: {filepath}")
        return False
    
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    print(f"\n========== VALIDATION: {filepath.name} ==========\n")
    
    # Check 1: Hard-coding
    has_hard_coding = False
    if 'def _get_status_translation' in content and 'STATUS_TRANSLATIONS' in content:
        # Check if STATUS_TRANSLATIONS is defined inside function
        for i, line in enumerate(lines):
            if 'def _get_status_translation' in line:
                # Check next 5 lines
                for j in range(i, min(i+10, len(lines))):
                    if 'STATUS_TRANSLATIONS_VI = {' in lines[j] or 'STATUS_TRANSLATIONS_EN = {' in lines[j]:
                        has_hard_coding = True
                        break
    
    if has_hard_coding:
        print("[ERROR] Hard-coding found in functions")
    else:
        print("[OK] No hard-coding violations")
    
    # Check 2: Vietnamese diacritics (context-aware)
    violations = [
        'quan ly', 'khach hang', 'nhan vien', 'du lieu',
        'dia chi', 'mat khau', 'dang nhap', 'co so', 'muc dich',
        'thong tin', 'nguoi dung', 'nhay cam', 'loai', 'danh muc'
    ]
    
    # Context patterns that indicate acceptable non-diacritic usage
    acceptable_contexts = [
        'non_diacritic_keywords',    # Validation patterns
        'non_diacritic_words',        # Validation lists
        'COLUMN_MAPPINGS',            # Database column aliases
        'column_mappings',            # Column alias dictionaries
        'r"',                         # Regex patterns
        'Database identifier',        # Explicit comment marker
        'Phien ban khong dau',        # Vietnamese comment marker
        'validation pattern',         # English comment marker
        '"""',                        # Python docstrings (correct usage)
        "'''",                        # Python docstrings (correct usage)
        '--',                         # SQL comments (correct usage)
        'COMMENT ON',                 # SQL COMMENT statements (correct usage)
        '# ',                         # Python comments (correct usage)
    ]
    
    missing_diacritics = []
    for word in violations:
        if word in content.lower():
            # Check each occurrence
            for i, line in enumerate(lines):
                if word in line.lower():
                    # Skip if in acceptable context
                    is_acceptable = False
                    
                    # Check if line is a docstring or comment (SHOULD have diacritics)
                    is_user_facing = (
                        '"""' in line or "'''" in line or  # Docstrings
                        line.strip().startswith('#') or     # Comments
                        '--' in line or                      # SQL comments
                        'COMMENT ON' in line                 # SQL COMMENT statements
                    )
                    
                    # If it's user-facing text and has diacritics elsewhere in line, it's OK
                    if is_user_facing:
                        # Line already has Vietnamese diacritics = proper usage
                        if any(c in line for c in 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'):
                            is_acceptable = True
                    
                    # Check current line for acceptable contexts (validation lists, etc.)
                    if not is_acceptable:
                        for context in acceptable_contexts:
                            if context in line:
                                is_acceptable = True
                                break
                    
                    # Check surrounding lines (±2) for context
                    if not is_acceptable:
                        for j in range(max(0, i-2), min(len(lines), i+3)):
                            for context in acceptable_contexts:
                                if context in lines[j]:
                                    is_acceptable = True
                                    break
                            if is_acceptable:
                                break
                    
                    # Only report if it's a real violation (no diacritics in non-acceptable context)
                    if not is_acceptable:
                        if not any(c in line for c in 'àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'):
                            missing_diacritics.append(word)
                            break
    
    if missing_diacritics:
        unique_violations = set(missing_diacritics)
        print(f"[ERROR] Missing diacritics in user-facing text: {', '.join(unique_violations)}")
    else:
        print("[OK] All Vietnamese text has proper diacritics")
    
    # Check 3: Bilingual support
    vi_fields = content.count('_vi:')
    en_fields = content.count('_en:')
    
    if vi_fields > 0:
        print(f"[OK] Bilingual support: {vi_fields} Vietnamese, {en_fields} English fields")
    else:
        print("[WARNING] No bilingual fields detected")
    
    # Check 4: No emoji
    emojis = ['✓', '✗', '⚠️', '•', '→', '🔧']
    has_emoji = any(emoji in content for emoji in emojis)
    
    if has_emoji:
        print("[ERROR] Emoji characters found")
    else:
        print("[OK] No emoji characters")
    
    # Statistics
    total_lines = len(lines)
    enums = content.count('class ') - content.count('class Config')
    constants = len([l for l in lines if l.strip() and l[0].isupper() and '=' in l])
    
    print(f"\n[STATS] Lines: {total_lines} | Enums: {enums} | Constants: {constants}")
    
    # Final verdict
    is_valid = not has_hard_coding and not missing_diacritics and not has_emoji
    
    print("\n" + "=" * 60)
    if is_valid:
        print("[PASSED] Document is compliant with VeriSyntra standards")
    else:
        print("[FAILED] Document has violations - review required")
    print("=" * 60 + "\n")
    
    return is_valid


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <document.md>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    is_valid = quick_validate(filepath)
    sys.exit(0 if is_valid else 1)
