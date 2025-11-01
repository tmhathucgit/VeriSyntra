# VeriSyntra Code Generation Checklist

## BEFORE Generating Any Code - ALWAYS Check:

### 1. EMOJI CHARACTERS - NEVER USE
```
WRONG: ✓ ✅ ✗ ❌ ⚠️ • → 🔧
RIGHT: [OK] [ERROR] [WARNING] > -> [TOOL]
```

### 2. DYNAMIC CODE - ALWAYS PREFER
```python
# WRONG - Hard-coded
total = item1 + item2 + item3
print("18 markers loaded")

# RIGHT - Dynamic
total = sum(items)
print(f"{len(markers)} markers loaded")
```

### 3. DRY PRINCIPLE - SINGLE SOURCE OF TRUTH
```python
# WRONG - Redefining
PDPL_CATEGORIES = {...}  # Defined in Step 2
PDPL_CATEGORIES = {...}  # NO - Don't redefine

# RIGHT - Reuse existing
if 'PDPL_CATEGORIES' not in globals():
    raise RuntimeError("Run Step 2 first")
print(f"Using {len(PDPL_CATEGORIES)} categories")
```

### 4. DEPENDENCY VALIDATION
```python
# ALWAYS validate prerequisites
prerequisites = {
    'registry': 'registry' in globals(),
    'normalizer': 'normalizer' in globals()
}
if not all(prerequisites.values()):
    raise RuntimeError("Missing prerequisites!")
```

### 5. ASCII-ONLY IN ALL FILES
- Python (.py)
- TypeScript/JavaScript (.ts, .tsx, .js, .jsx)
- Jupyter Notebooks (.ipynb)
- Markdown (.md)
- JSON (.json)
- All comments and docstrings

## AFTER Generating Code - ALWAYS Validate:

1. Run: `python validate_code_standards.py <file>`
2. Check output for violations
3. Fix any issues BEFORE showing to user

## Common Mistakes to Avoid:

1. Using ✓ in success messages → Use [OK]
2. Using ❌ in error messages → Use [ERROR] or [NOT SAVED]
3. Hard-coding counts → Calculate dynamically
4. Redefining constants → Check if exists first
5. No prerequisite checks → Always validate dependencies

## Vietnamese Business Context Requirements:

- Always include `veriBusinessContext` parameter
- Use Vietnamese timezone: `Asia/Ho_Chi_Minh`
- Bilingual support: Vietnamese-first, English fallback
- Regional awareness: North, Central, South patterns
- PDPL 2025 compliance in all data handling

## Remember:

**The copilot-instructions.md is the source of truth.**
**This checklist is just a quick reference.**
**When in doubt, check the main instructions file.**
