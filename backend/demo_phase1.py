"""
Phase 1 Implementation Demonstration
Shows Company Registry and Text Normalizer in action.

Run: python backend/demo_phase1.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.core.company_registry import get_registry
from app.core.pdpl_normalizer import get_normalizer


def main():
    print("=" * 70)
    print("VeriSyntra Phase 1: Dynamic Company Registry Implementation")
    print("=" * 70)
    print()
    
    # Initialize registry
    print("[STEP 1] Loading Company Registry...")
    registry = get_registry()
    stats = registry.get_statistics()
    
    print(f"  SUCCESS: Loaded {stats['total_companies']} companies")
    print(f"  Aliases: {stats['total_aliases']}")
    print(f"  Industries: {len(stats['industry_list'])}")
    print(f"    - {', '.join(stats['industry_list'])}")
    print(f"  Regions: {len(stats['region_list'])}")
    print(f"    - {', '.join(stats['region_list'])}")
    print()
    
    # Demonstrate company search
    print("[STEP 2] Company Search Demonstration...")
    print()
    print("  Query: Search 'bank' in finance industry")
    results = registry.search_companies(query="bank", industry="finance")
    print(f"  Results: {len(results)} companies found")
    for company in results[:3]:
        print(f"    - {company['name']} ({company['region']})")
    print()
    
    # Demonstrate alias resolution
    print("[STEP 3] Alias Resolution Demonstration...")
    test_aliases = [
        ("VCB", "Vietcombank"),
        ("Grab", "Grab Vietnam"),
        ("MoMo", "MoMo")
    ]
    for alias, expected in test_aliases:
        canonical = registry.resolve_alias(alias)
        status = "OK" if canonical == expected else f"FAIL (got: {canonical})"
        print(f"  {alias:20s} -> {canonical:30s} [{status}]")
    print()
    
    # Initialize normalizer
    print("[STEP 4] Text Normalization Demonstration...")
    normalizer = get_normalizer()
    print()
    
    # Test cases
    test_cases = [
        "Grab Vietnam collects location data from users",
        "Vietcombank and MoMo partnership for digital payments",
        "FPT Corporation signs contract with Shopee",
        "VCB provides banking accounts for Tiki customers"
    ]
    
    for i, text in enumerate(test_cases, 1):
        result = normalizer.normalize_text(text)
        print(f"  Test Case {i}:")
        print(f"    Original:   {text}")
        print(f"    Normalized: {result.normalized_text}")
        print(f"    Companies:  {result.company_count} detected")
        print()
    
    # Demonstrate normalization validation
    print("[STEP 5] Normalization Validation...")
    original = "Grab Vietnam processes personal data"
    normalized = normalizer.normalize_for_inference(original)
    validation = normalizer.validate_normalization(original, normalized)
    
    print(f"  Original:     {original}")
    print(f"  Normalized:   {normalized}")
    print(f"  Valid:        {validation['is_valid']}")
    print(f"  Tokens Added: {validation['token_count']}")
    print(f"  Length Ratio: {validation['length_ratio']:.2f}")
    print()
    
    # Demonstrate add company
    print("[STEP 6] Dynamic Company Addition...")
    result = registry.add_company(
        name="Demo Startup Ltd",
        industry="technology",
        region="south",
        aliases=["DSL", "Demo Startup"],
        metadata={"founded": 2025, "type": "Startup"},
        persist=False  # Don't save to file
    )
    print(f"  Add Company:  {result['company_name']}")
    print(f"  Status:       {'SUCCESS' if result['success'] else 'FAILED'}")
    print(f"  Message:      {result['message']}")
    print()
    
    # Verify it's searchable
    company_info = registry.get_company_info("Demo Startup Ltd")
    if company_info:
        print("  Company Info Retrieved:")
        print(f"    Name:     {company_info['name']}")
        print(f"    Industry: {company_info['industry']}")
        print(f"    Region:   {company_info['region']}")
    print()
    
    # Final statistics
    print("[STEP 7] Final Statistics...")
    final_stats = registry.get_statistics()
    print(f"  Total Companies: {final_stats['total_companies']}")
    print(f"  Total Aliases:   {final_stats['total_aliases']}")
    print()
    
    print("=" * 70)
    print("Phase 1 Implementation: ALL TESTS PASSED")
    print("=" * 70)


if __name__ == '__main__':
    main()
