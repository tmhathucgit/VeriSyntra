"""
Phase 2 Validation Script
Tests VietnameseHardDatasetGenerator integration with Phase 1 components
"""

from app.ml.vietnamese_hard_dataset_generator import VietnameseHardDatasetGenerator
from app.core.company_registry import get_registry
from app.core.pdpl_normalizer import get_normalizer

def main():
    print("=" * 70)
    print("Phase 2 Validation: Vietnamese Hard Dataset Generator")
    print("=" * 70)
    print()
    
    # Step 1: Initialize generator
    print("[STEP 1] Initialize Generator...")
    gen = VietnameseHardDatasetGenerator()
    print("  SUCCESS: Generator initialized")
    print()
    
    # Step 2: Verify registry integration
    print("[STEP 2] Verify Company Registry Integration...")
    registry = get_registry()
    stats = registry.get_statistics()
    print(f"  Companies available: {stats['total_companies']}")
    print(f"  Industries: {len(stats['industries'])}")
    print(f"  Regions: {len(stats['regions'])}")
    print()
    
    # Step 3: Generate small dataset
    print("[STEP 3] Generate Test Dataset...")
    samples = gen.generate_dataset(
        samples_per_category=10,
        num_categories=4
    )
    print(f"  Generated: {len(samples)} samples")
    print(f"  Expected: ~{10 * 4} samples (may vary due to rounding)")
    assert 35 <= len(samples) <= 45, "Sample count out of acceptable range"
    print("  SUCCESS: Sample count within expected range")
    print()
    
    # Step 4: Verify normalization
    print("[STEP 4] Verify Text Normalization...")
    normalized_count = sum(1 for s in samples if "[COMPANY]" in s['text'])
    normalization_rate = (normalized_count / len(samples)) * 100
    print(f"  Normalized samples: {normalized_count}/{len(samples)}")
    print(f"  Normalization rate: {normalization_rate:.1f}%")
    assert normalization_rate > 80, "Normalization rate too low"
    print("  SUCCESS: Normalization working")
    print()
    
    # Step 5: Verify sample structure
    print("[STEP 5] Verify Sample Structure...")
    sample = samples[0]
    required_keys = ['text', 'label', 'raw_text', 'ambiguity', 'metadata']
    for key in required_keys:
        assert key in sample, f"Missing key: {key}"
    print(f"  All required keys present: {required_keys}")
    print()
    
    # Step 6: Show example samples
    print("[STEP 6] Example Samples...")
    for i in range(min(3, len(samples))):
        s = samples[i]
        print(f"\n  Sample {i+1}:")
        print(f"    Category: {s['label']} (Ambiguity: {s['ambiguity']})")
        print(f"    Company: {s['metadata']['company']}")
        print(f"    Industry: {s['metadata']['industry']}")
        print(f"    Region: {s['metadata']['region']}")
        print(f"    Raw: {s['raw_text'][:60]}...")
        print(f"    Normalized: {s['text'][:60]}...")
    print()
    
    # Step 7: Verify ambiguity distribution
    print("[STEP 7] Verify Ambiguity Distribution...")
    ambiguity_counts = {}
    for s in samples:
        amb = s['ambiguity']
        ambiguity_counts[amb] = ambiguity_counts.get(amb, 0) + 1
    
    for amb, count in sorted(ambiguity_counts.items()):
        percentage = (count / len(samples)) * 100
        print(f"  {amb}: {count} samples ({percentage:.1f}%)")
    print()
    
    # Step 8: Verify company diversity
    print("[STEP 8] Verify Company Diversity...")
    unique_companies = set(s['metadata']['company'] for s in samples)
    print(f"  Unique companies used: {len(unique_companies)}")
    print(f"  Examples: {list(unique_companies)[:5]}")
    print()
    
    # Step 9: Verify metadata completeness
    print("[STEP 9] Verify Metadata Completeness...")
    metadata_keys = ['company', 'industry', 'region', 'formality', 'context']
    complete_metadata = all(
        all(key in s['metadata'] for key in metadata_keys)
        for s in samples
    )
    assert complete_metadata, "Incomplete metadata found"
    print(f"  All samples have complete metadata: {metadata_keys}")
    print()
    
    # Step 10: Test get_statistics
    print("[STEP 10] Test Generator Statistics...")
    gen_stats = gen.get_statistics()
    print(f"  Model type: {gen_stats['model_type']}")
    print(f"  Categories: {gen_stats['num_categories']}")
    print(f"  Available model types: {len(gen_stats['available_model_types'])}")
    print(f"  Company registry total: {gen_stats['company_registry']['total_companies']}")
    print()
    
    print("=" * 70)
    print("Phase 2 Validation: ALL TESTS PASSED")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Dataset generation: WORKING")
    print(f"  - Company registry integration: WORKING")
    print(f"  - Text normalization: WORKING ({normalization_rate:.1f}%)")
    print(f"  - Company diversity: {len(unique_companies)} unique companies")
    print(f"  - Ambiguity levels: {len(ambiguity_counts)} levels")
    print(f"  - Metadata completeness: 100%")

if __name__ == '__main__':
    main()
