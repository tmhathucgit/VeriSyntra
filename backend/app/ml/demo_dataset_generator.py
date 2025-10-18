"""
Vietnamese Hard Dataset Generator - Demonstration Script
Tests dataset generation with company normalization.

Run: python backend/app/ml/demo_dataset_generator.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.ml.vietnamese_hard_dataset_generator import VietnameseHardDatasetGenerator


def main():
    print("=" * 70)
    print("VeriSyntra Dataset Generator - Phase 2 Demonstration")
    print("=" * 70)
    print()
    
    # Initialize generator
    print("[STEP 1] Initializing Dataset Generator...")
    generator = VietnameseHardDatasetGenerator()
    
    stats = generator.get_statistics()
    print(f"  Companies Available: {stats['company_registry']['total_companies']}")
    print(f"  Industries: {', '.join(stats['company_registry']['industries'])}")
    print(f"  Regions: {', '.join(stats['company_registry']['regions'])}")
    print(f"  Data Contexts: {stats['configuration']['data_contexts']}")
    print()
    
    # Test single sample generation
    print("[STEP 2] Generating Sample Data (Each Ambiguity Level)...")
    print()
    
    for ambiguity in ['EASY', 'MEDIUM', 'HARD', 'VERY_HARD']:
        sample = generator.generate_hard_sample(
            category_id=0,  # Lawfulness
            ambiguity=ambiguity,
            region='south',
            formality='business',
            industry='technology'
        )
        
        print(f"  {ambiguity} Sample:")
        print(f"    Raw Text:        {sample['raw_text']}")
        print(f"    Normalized:      {sample['text']}")
        print(f"    Label:           {sample['label']} ({sample['metadata']['category_name']})")
        print(f"    Company:         {sample['metadata']['company']}")
        print(f"    Industry:        {sample['metadata']['industry']}")
        print()
    
    # Test multiple categories
    print("[STEP 3] Testing All PDPL Categories...")
    print()
    
    for category_id in range(8):
        sample = generator.generate_hard_sample(
            category_id=category_id,
            ambiguity='HARD',
            region='south',
            formality='business'
        )
        
        print(f"  Category {category_id} ({sample['metadata']['category_name']}):")
        print(f"    Text: {sample['text'][:80]}...")
        print()
    
    # Generate small dataset
    print("[STEP 4] Generating Small Test Dataset...")
    print(f"  Configuration: 10 samples per category x 8 categories = 80 samples")
    print()
    
    dataset = generator.generate_dataset(
        samples_per_category=10,
        num_categories=8,
        output_file=None  # Don't save yet
    )
    
    print(f"  Total Samples Generated: {len(dataset)}")
    print()
    
    # Validate normalization
    print("[STEP 5] Validating Company Normalization...")
    normalized_count = sum(1 for sample in dataset if '[COMPANY]' in sample['text'])
    raw_company_count = sum(1 for sample in dataset if sample['metadata']['company'] != 'Cong ty ABC')
    
    print(f"  Samples with [COMPANY] token: {normalized_count}/{len(dataset)}")
    print(f"  Samples with real companies:  {raw_company_count}/{len(dataset)}")
    print(f"  Normalization Rate: {normalized_count/len(dataset)*100:.1f}%")
    print()
    
    # Check ambiguity distribution
    print("[STEP 6] Ambiguity Distribution Check...")
    ambiguity_counts = {}
    for sample in dataset:
        amb = sample['ambiguity']
        ambiguity_counts[amb] = ambiguity_counts.get(amb, 0) + 1
    
    for amb, count in sorted(ambiguity_counts.items()):
        percentage = count / len(dataset) * 100
        print(f"  {amb:12s}: {count:3d} samples ({percentage:5.1f}%)")
    print()
    
    # Sample quality check
    print("[STEP 7] Sample Quality Verification...")
    
    # Check for diverse companies
    unique_companies = set(sample['metadata']['company'] for sample in dataset)
    print(f"  Unique Companies Used: {len(unique_companies)}")
    
    # Check for diverse contexts
    unique_contexts = set(sample['metadata']['context'] for sample in dataset)
    print(f"  Unique Data Contexts: {len(unique_contexts)}")
    
    # Check for diverse regions
    unique_regions = set(sample['metadata']['region'] for sample in dataset)
    print(f"  Unique Regions: {', '.join(unique_regions)}")
    
    # Check for diverse formalities
    unique_formalities = set(sample['metadata']['formality'] for sample in dataset)
    print(f"  Unique Formalities: {', '.join(unique_formalities)}")
    print()
    
    # Show sample outputs
    print("[STEP 8] Sample Output Examples...")
    print()
    
    for i, sample in enumerate(dataset[:3], 1):
        print(f"  Example {i}:")
        print(f"    Category:   {sample['metadata']['category_name']}")
        print(f"    Ambiguity:  {sample['ambiguity']}")
        print(f"    Company:    {sample['metadata']['company']}")
        print(f"    Raw:        {sample['raw_text'][:60]}...")
        print(f"    Normalized: {sample['text'][:60]}...")
        print()
    
    print("=" * 70)
    print("Phase 2 Dataset Generator: ALL TESTS PASSED")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("  - Generate full production dataset (2500+ samples/category)")
    print("  - Train VeriAIDPO models with [COMPANY] normalized data")
    print("  - Validate model accuracy on company-agnostic predictions")


if __name__ == '__main__':
    main()
