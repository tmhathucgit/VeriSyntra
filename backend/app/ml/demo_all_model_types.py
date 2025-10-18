"""
Demo Script: All 11 VeriAIDPO Model Types
Demonstrates Vietnamese Hard Dataset Generator supporting all model types
from VeriAIDPO_Missing_Principles_Implementation_Plan.md

Author: VeriSyntra Development Team
Created: 2025-10-18
Version: 2.0.0
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.ml.vietnamese_hard_dataset_generator import VietnameseHardDatasetGenerator


def demo_all_model_types():
    """Demonstrate all 11 model types with sample generation."""
    
    print("=" * 80)
    print("VeriAIDPO Dataset Generator - All 11 Model Types Demo")
    print("=" * 80)
    print()
    
    # Get all available model types
    model_types = [
        'principles',
        'legal_basis',
        'breach_triage',
        'cross_border',
        'consent_type',
        'data_sensitivity',
        'dpo_tasks',
        'risk_level',
        'compliance_status',
        'regional',
        'industry'
    ]
    
    results = {}
    
    for model_type in model_types:
        print(f"\n{'='*80}")
        print(f"MODEL TYPE: {model_type.upper().replace('_', ' ')}")
        print(f"{'='*80}\n")
        
        try:
            # Initialize generator for this model type
            generator = VietnameseHardDatasetGenerator(model_type=model_type)
            
            # Get statistics
            stats = generator.get_statistics()
            
            print(f"✅ Model Type: {stats['model_type']}")
            print(f"✅ Number of Categories: {stats['num_categories']}")
            print(f"✅ Categories: {stats['categories']}")
            print()
            
            # Generate one sample for each category
            print(f"Generating samples for all {stats['num_categories']} categories:")
            print("-" * 80)
            
            samples = []
            for category_id in range(stats['num_categories']):
                category_name = stats['categories'][category_id]
                
                # Generate HARD sample for demonstration
                sample = generator.generate_hard_sample(
                    category_id=category_id,
                    ambiguity='HARD',
                    region='south',
                    formality='business',
                    industry='technology'
                )
                
                samples.append(sample)
                
                print(f"\n📋 Category {category_id}: {category_name}")
                print(f"   Raw: {sample['raw_text'][:100]}...")
                print(f"   Normalized: {sample['text'][:100]}...")
                print(f"   Company: {sample['metadata']['company']}")
                print(f"   Ambiguity: {sample['ambiguity']}")
            
            results[model_type] = {
                'status': 'SUCCESS',
                'num_categories': stats['num_categories'],
                'samples_generated': len(samples)
            }
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results[model_type] = {
                'status': 'FAILED',
                'error': str(e)
            }
    
    # Summary Report
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    print()
    
    total_categories = 0
    successful = 0
    failed = 0
    
    for model_type, result in results.items():
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
        print(f"{status_icon} {model_type:20s} - {result['status']}")
        
        if result['status'] == 'SUCCESS':
            successful += 1
            total_categories += result['num_categories']
            print(f"   Categories: {result['num_categories']}, Samples: {result['samples_generated']}")
        else:
            failed += 1
            print(f"   Error: {result['error']}")
    
    print()
    print(f"Total Model Types: {len(model_types)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total Categories Across All Models: {total_categories}")
    print()
    
    # Dataset Size Calculation
    print("=" * 80)
    print("PRODUCTION DATASET SIZE ESTIMATES")
    print("=" * 80)
    print()
    
    dataset_sizes = {
        'principles': 3000,      # 8 categories × 3000 = 24,000 samples
        'legal_basis': 2500,     # 4 categories × 2500 = 10,000 samples
        'breach_triage': 2000,   # 4 categories × 2000 = 8,000 samples
        'cross_border': 2000,    # 5 categories × 2000 = 10,000 samples
        'consent_type': 1500,    # 4 categories × 1500 = 6,000 samples
        'data_sensitivity': 1500,# 4 categories × 1500 = 6,000 samples
        'dpo_tasks': 1200,       # 5 categories × 1200 = 6,000 samples
        'risk_level': 2000,      # 4 categories × 2000 = 8,000 samples
        'compliance_status': 1200,# 4 categories × 1200 = 4,800 samples
        'regional': 1500,        # 3 categories × 1500 = 4,500 samples
        'industry': 1200         # 4 categories × 1200 = 4,800 samples
    }
    
    total_vi_samples = 0
    
    for model_type, samples_per_cat in dataset_sizes.items():
        if model_type in results and results[model_type]['status'] == 'SUCCESS':
            num_cats = results[model_type]['num_categories']
            total_samples = samples_per_cat * num_cats
            total_vi_samples += total_samples
            
            print(f"{model_type:20s}: {samples_per_cat:,} × {num_cats} = {total_samples:,} samples")
    
    print()
    print(f"{'TOTAL VIETNAMESE':20s}: {total_vi_samples:,} samples")
    print(f"{'TOTAL ENGLISH':20s}: {int(total_vi_samples * 0.5):,} samples (50% of VI)")
    print(f"{'GRAND TOTAL':20s}: {int(total_vi_samples * 1.5):,} samples")
    print()
    
    if failed == 0:
        print("🎉 ALL MODEL TYPES SUCCESSFULLY VALIDATED! 🎉")
    else:
        print(f"⚠️  {failed} model type(s) failed validation")
    
    print()


if __name__ == "__main__":
    demo_all_model_types()
