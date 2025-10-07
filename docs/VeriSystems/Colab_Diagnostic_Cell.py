# 🔍 VeriAIDPO Colab Diagnostic Test
# Copy-paste this into a NEW cell in Google Colab and run it

print("=" * 60)
print("🔍 COLAB DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Python version
print("\n✅ Test 1: Python Version")
import sys
print(f"   Python: {sys.version}")

# Test 2: GPU availability
print("\n✅ Test 2: GPU Check")
import torch
if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)} ✅")
    print(f"   CUDA Version: {torch.version.cuda}")
    print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("   ⚠️ WARNING: No GPU detected!")
    print("   Fix: Runtime → Change runtime type → GPU")

# Test 3: Check for dataset files
print("\n✅ Test 3: Dataset Files")
import os
files = ['train.jsonl', 'val.jsonl', 'test.jsonl']
for file in files:
    if os.path.exists(file):
        size = os.path.getsize(file) / 1024  # KB
        print(f"   ✅ {file}: {size:.2f} KB")
    else:
        print(f"   ❌ {file}: NOT FOUND")
        print(f"      → Upload from: docs/VeriSystems/vietnamese_pdpl_mvp/")

# Test 4: Test simple output
print("\n✅ Test 4: Output Test")
print("   If you can see this, Colab is working! 🎉")

# Test 5: Progress bar test
print("\n✅ Test 5: Progress Bar Test")
from tqdm import tqdm
import time
for i in tqdm(range(10), desc="Testing progress bar"):
    time.sleep(0.1)
print("   Progress bar working! ✅")

print("\n" + "=" * 60)
print("🎯 DIAGNOSTIC COMPLETE")
print("=" * 60)
print("\nIf you see this entire output, Colab is working correctly!")
print("You can now run the training notebook cells.")
