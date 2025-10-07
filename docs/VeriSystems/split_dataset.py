#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset Splitter for VeriAIDPO
Splits vietnamese_pdpl_mvp_complete.jsonl into train/val/test sets

Usage:
    python split_dataset.py

Output:
    - train.jsonl (70% of data)
    - val.jsonl (15% of data)
    - test.jsonl (15% of data)

Author: VeriSyntra AI Team
Date: October 6, 2025
"""

import json
import random
from pathlib import Path
from collections import defaultdict

def load_jsonl(file_path):
    """Load JSONL file"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def save_jsonl(data, file_path):
    """Save data to JSONL file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def stratified_split(data, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Split data with stratification by category (label)
    Ensures each category is proportionally represented in train/val/test
    
    Args:
        data: List of examples
        train_ratio: Proportion for training (default: 0.7)
        val_ratio: Proportion for validation (default: 0.15)
        test_ratio: Proportion for testing (default: 0.15)
    
    Returns:
        train_data, val_data, test_data
    """
    # Group by category
    by_category = defaultdict(list)
    for item in data:
        label = item.get('label', 0)
        by_category[label].append(item)
    
    train_data = []
    val_data = []
    test_data = []
    
    # Split each category proportionally
    for category, items in by_category.items():
        # Shuffle within category
        random.shuffle(items)
        
        n = len(items)
        train_end = int(n * train_ratio)
        val_end = train_end + int(n * val_ratio)
        
        train_data.extend(items[:train_end])
        val_data.extend(items[train_end:val_end])
        test_data.extend(items[val_end:])
    
    # Shuffle final datasets
    random.shuffle(train_data)
    random.shuffle(val_data)
    random.shuffle(test_data)
    
    return train_data, val_data, test_data

def print_statistics(train, val, test):
    """Print dataset statistics"""
    print("\n" + "="*70)
    print("📊 DATASET SPLIT STATISTICS")
    print("="*70)
    
    total = len(train) + len(val) + len(test)
    
    print(f"\nTotal examples: {total:,}")
    print(f"├─ Train: {len(train):,} ({len(train)/total*100:.1f}%)")
    print(f"├─ Val:   {len(val):,} ({len(val)/total*100:.1f}%)")
    print(f"└─ Test:  {len(test):,} ({len(test)/total*100:.1f}%)")
    
    # Category distribution
    def count_categories(data):
        counts = defaultdict(int)
        for item in data:
            counts[item.get('label', 0)] += 1
        return counts
    
    train_cats = count_categories(train)
    val_cats = count_categories(val)
    test_cats = count_categories(test)
    
    print("\n📊 Category Distribution (Balanced Check):")
    print("\nCategory | Train | Val | Test | Total")
    print("---------|-------|-----|------|------")
    
    for cat in sorted(train_cats.keys()):
        t = train_cats[cat]
        v = val_cats[cat]
        te = test_cats[cat]
        tot = t + v + te
        print(f"    {cat}    | {t:5d} | {v:3d} | {te:3d} | {tot:5d}")
    
    # Region distribution (if available)
    def count_regions(data):
        counts = defaultdict(int)
        for item in data:
            region = item.get('region', 'unknown')
            counts[region] += 1
        return counts
    
    train_regions = count_regions(train)
    val_regions = count_regions(val)
    test_regions = count_regions(test)
    
    print("\n🗺️  Regional Distribution:")
    print("\nRegion  | Train | Val | Test | Total")
    print("--------|-------|-----|------|------")
    
    all_regions = set(train_regions.keys()) | set(val_regions.keys()) | set(test_regions.keys())
    for region in sorted(all_regions):
        t = train_regions.get(region, 0)
        v = val_regions.get(region, 0)
        te = test_regions.get(region, 0)
        tot = t + v + te
        print(f"{region:7s} | {t:5d} | {v:3d} | {te:3d} | {tot:5d}")

def main():
    # Set random seed for reproducibility
    random.seed(42)
    
    print("\n" + "="*70)
    print("🇻🇳 VeriAIDPO DATASET SPLITTER")
    print("="*70)
    
    # Input/output paths
    input_file = Path('vietnamese_pdpl_mvp') / 'vietnamese_pdpl_mvp_complete.jsonl'
    output_dir = Path('vietnamese_pdpl_mvp')
    
    if not input_file.exists():
        print(f"\n❌ Error: Input file not found: {input_file}")
        print("   Make sure you're running this from the docs/VeriSystems directory")
        print("   Or update the input_file path in the script")
        return
    
    print(f"\n📁 Input file: {input_file}")
    print(f"📁 Output directory: {output_dir}")
    
    # Load data
    print("\n⏳ Loading dataset...")
    data = load_jsonl(input_file)
    print(f"✅ Loaded {len(data):,} examples")
    
    # Split data (70% train, 15% val, 15% test)
    print("\n⏳ Splitting dataset (stratified by category)...")
    train_data, val_data, test_data = stratified_split(data, 0.7, 0.15, 0.15)
    
    # Print statistics
    print_statistics(train_data, val_data, test_data)
    
    # Save splits
    print("\n" + "="*70)
    print("💾 SAVING SPLIT DATASETS")
    print("="*70)
    
    train_file = output_dir / 'train.jsonl'
    val_file = output_dir / 'val.jsonl'
    test_file = output_dir / 'test.jsonl'
    
    print(f"\n⏳ Saving train set...")
    save_jsonl(train_data, train_file)
    train_size_kb = train_file.stat().st_size / 1024
    print(f"✅ Saved {len(train_data):,} examples to {train_file.name} ({train_size_kb:.1f} KB)")
    
    print(f"\n⏳ Saving validation set...")
    save_jsonl(val_data, val_file)
    val_size_kb = val_file.stat().st_size / 1024
    print(f"✅ Saved {len(val_data):,} examples to {val_file.name} ({val_size_kb:.1f} KB)")
    
    print(f"\n⏳ Saving test set...")
    save_jsonl(test_data, test_file)
    test_size_kb = test_file.stat().st_size / 1024
    print(f"✅ Saved {len(test_data):,} examples to {test_file.name} ({test_size_kb:.1f} KB)")
    
    total_size_kb = train_size_kb + val_size_kb + test_size_kb
    
    print("\n" + "="*70)
    print("✅ DATASET SPLIT COMPLETE!")
    print("="*70)
    
    print(f"\n📁 Files created:")
    print(f"    - {train_file.name} ({train_size_kb:.1f} KB)")
    print(f"    - {val_file.name} ({val_size_kb:.1f} KB)")
    print(f"    - {test_file.name} ({test_size_kb:.1f} KB)")
    print(f"    Total: {total_size_kb:.1f} KB")
    
    print("\n🚀 Next Steps:")
    print("   1. Upload train.jsonl to Google Colab for PhoBERT training")
    print("   2. Use val.jsonl for validation during training")
    print("   3. Use test.jsonl for final accuracy evaluation")
    print("   4. See: VeriAIDPO_Google_Colab_Training_Guide.md")
    
    print("\n🇻🇳 Ready for PhoBERT Training! 🚀\n")

if __name__ == '__main__':
    main()
