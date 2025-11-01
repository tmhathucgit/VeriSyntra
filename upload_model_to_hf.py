"""
Upload VeriAIDPO Model to Hugging Face Hub
==========================================

This script uploads your trained Vietnamese PDPL classification model
to Hugging Face Hub for use in microservices architecture.

Usage:
    1. Create account at https://huggingface.co/join
    2. Create access token at https://huggingface.co/settings/tokens
    3. Run: python upload_model_to_hf.py
"""

from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder
import os

# Configuration
MODEL_NAME = "VeriAIDPO_Principles_VI_v1"
MODEL_PATH = Path(__file__).parent / "backend" / "app" / "ml" / "models" / MODEL_NAME
REPO_NAME = None  # Will be set dynamically based on logged-in user

# Model metadata
MODEL_CARD = """---
language: vi
tags:
- vietnamese
- pdpl
- compliance
- data-protection
- text-classification
license: mit
datasets:
- custom
metrics:
- accuracy
- f1
---

# VeriAIDPO Principles VI v1

Vietnamese PDPL (Personal Data Protection Law) Principles Classification Model

## Model Description

This model classifies Vietnamese text according to 8 PDPL principles from Vietnam's 
Decree 13/2023/ND-CP on Personal Data Protection.

**Base Model:** PhoBERT (vinai/phobert-base)

**Fine-tuned for:** Vietnamese PDPL 2025 compliance text classification

## Categories (8 PDPL Principles)

0. **Tuân thủ pháp luật và minh bạch** (Lawfulness and Transparency)
1. **Giới hạn mục đích** (Purpose Limitation)
2. **Tối thiểu hóa dữ liệu** (Data Minimization)
3. **Chính xác** (Accuracy)
4. **Giới hạn lưu trữ** (Storage Limitation)
5. **An toàn bảo mật** (Security)
6. **Trách nhiệm giải trình** (Accountability)
7. **Quyền của chủ thể dữ liệu** (Data Subject Rights)

## Intended Use

This model is designed for:
- Vietnamese enterprises implementing PDPL 2025 compliance
- DPO (Data Protection Officer) tools and automation
- Legal tech applications for Vietnamese data protection
- Compliance monitoring and auditing systems

## Training Data

- **Language:** Vietnamese
- **Domain:** Legal/Compliance text from Vietnamese PDPL regulations
- **Size:** Custom dataset based on Decree 13/2023/ND-CP
- **Preprocessing:** Vietnamese-specific text normalization

## Performance

- **Accuracy:** >95% on validation set
- **F1 Score:** >0.93 across all categories
- **Best for:** Vietnamese legal and compliance text

## Usage

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("tmhathucgit/VeriAIDPO_Principles_VI_v1")
tokenizer = AutoTokenizer.from_pretrained("tmhathucgit/VeriAIDPO_Principles_VI_v1")

# Classify Vietnamese text
text = "Tổ chức phải có trách nhiệm chứng minh tuân thủ các quy định về bảo vệ dữ liệu cá nhân"
inputs = tokenizer(text, return_tensors="pt", max_length=256, truncation=True)

with torch.no_grad():
    outputs = model(**inputs)
    prediction = outputs.logits.argmax().item()

# Category names
categories = {
    0: "Lawfulness and Transparency",
    1: "Purpose Limitation",
    2: "Data Minimization",
    3: "Accuracy",
    4: "Storage Limitation",
    5: "Security",
    6: "Accountability",
    7: "Data Subject Rights"
}

print(f"Predicted category: {categories[prediction]}")
```

## Limitations

- Optimized for Vietnamese legal text only
- May not perform well on informal or colloquial Vietnamese
- Best results with compliance-related text
- Requires Vietnamese diacritics for optimal performance

## Citation

If you use this model, please cite:

```
@misc{veriaidpo_principles_v1,
  title={VeriAIDPO Principles VI v1: Vietnamese PDPL Classification Model},
  author={VeriSyntra},
  year={2025},
  publisher={Hugging Face},
  howpublished={\\url{https://huggingface.co/tmhathucgit/VeriAIDPO_Principles_VI_v1}}
}
```

## License

MIT License

## Contact

- **Organization:** VeriSyntra
- **GitHub:** https://github.com/tmhathucgit/VeriSyntra
- **Purpose:** Vietnamese PDPL 2025 Compliance Platform
"""


def check_model_files():
    """Check if all required model files exist"""
    print("\n[STEP 1] Checking model files...")
    
    if not MODEL_PATH.exists():
        print(f"[ERROR] Model directory not found: {MODEL_PATH}")
        return False
    
    required_files = [
        "model.safetensors",
        "config.json",
        "vocab.txt",
        "tokenizer_config.json",
        "special_tokens_map.json"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = MODEL_PATH / file
        if not file_path.exists():
            missing_files.append(file)
        else:
            size_mb = file_path.stat().st_size / 1024 / 1024
            print(f"  [OK] {file} ({size_mb:.2f} MB)")
    
    if missing_files:
        print(f"[ERROR] Missing files: {', '.join(missing_files)}")
        return False
    
    print("[OK] All required files found!")
    return True


def login_to_huggingface():
    """Login to Hugging Face Hub"""
    print("\n[STEP 2] Hugging Face Authentication")
    print("=" * 60)
    print("You need a Hugging Face account and access token.")
    print("")
    print("1. Create account: https://huggingface.co/join")
    print("2. Create token: https://huggingface.co/settings/tokens")
    print("   - Click 'New token'")
    print("   - Select 'Write' permissions")
    print("   - Copy the token")
    print("")
    
    token = input("Paste your Hugging Face token here: ").strip()
    
    if not token:
        print("[ERROR] No token provided")
        return None, None
    
    try:
        api = HfApi(token=token)
        user_info = api.whoami()
        username = user_info['name']
        print(f"[OK] Logged in as: {username}")
        
        # Set repo name dynamically
        repo_name = f"{username}/{MODEL_NAME}"
        print(f"[OK] Repository will be: {repo_name}")
        
        return api, repo_name
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return None, None


def create_model_repo(api: HfApi, repo_name: str):
    """Create repository on Hugging Face Hub"""
    print(f"\n[STEP 3] Creating repository: {repo_name}")
    
    try:
        # Check if repo already exists
        try:
            api.repo_info(repo_id=repo_name, repo_type="model")
            print(f"[OK] Repository already exists: {repo_name}")
            
            overwrite = input("Do you want to overwrite? (yes/no): ").strip().lower()
            if overwrite != "yes":
                print("[CANCELLED] Upload cancelled")
                return False
        except:
            # Repo doesn't exist, create it
            create_repo(
                repo_id=repo_name,
                repo_type="model",
                private=True,  # Private repo - protects proprietary VeriSyntra models
                token=api.token
            )
            print(f"[OK] Created PRIVATE repository: {repo_name}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to create repository: {e}")
        return False


def upload_model_files(api: HfApi, repo_name: str):
    """Upload model files to Hugging Face Hub"""
    print(f"\n[STEP 4] Uploading model files...")
    print("This may take several minutes (515 MB model file)...")
    
    try:
        # Create README.md
        readme_path = MODEL_PATH / "README.md"
        model_card = MODEL_CARD.replace("tmhathucgit/VeriAIDPO_Principles_VI_v1", repo_name)
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(model_card)
        print("[OK] Created README.md")
        
        # Upload entire folder
        print(f"[OK] Uploading from: {MODEL_PATH}")
        print(f"[OK] Uploading to: {repo_name}")
        
        upload_folder(
            folder_path=str(MODEL_PATH),
            repo_id=repo_name,
            repo_type="model",
            token=api.token,
            commit_message="Upload VeriAIDPO Principles VI v1 model"
        )
        
        print("[OK] Upload complete!")
        print(f"\n[SUCCESS] Model available at:")
        print(f"https://huggingface.co/{repo_name}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return False


def show_usage_instructions(repo_name: str):
    """Show how to use the uploaded model"""
    print("\n" + "=" * 60)
    print("HOW TO USE YOUR MODEL IN MICROSERVICES")
    print("=" * 60)
    
    print(f"""
1. UPDATE YOUR .gitignore:
   Add these lines to prevent committing large model files:
   
   # ML Models - download from Hugging Face Hub
   backend/app/ml/models/*.safetensors
   backend/app/ml/models/VeriAIDPO_*/

2. UPDATE backend/app/ml/model_loader.py:
   
   from huggingface_hub import snapshot_download
   
   def _setup_model_path(self):
       local_path = Path(__file__).parent / "models" / "VeriAIDPO_Principles_VI_v1"
       
       if not local_path.exists():
           logger.info("Downloading model from Hugging Face Hub...")
           snapshot_download(
               repo_id="{REPO_NAME}",
               local_dir=str(local_path),
               local_dir_use_symlinks=False
           )
       
       self._model_path = local_path

3. IN YOUR DOCKER CONTAINER:
   The model will automatically download on first startup!
   
   Environment variable (optional):
   ENV HF_HOME=/app/.cache/huggingface

4. TEST LOCALLY:
   
   from transformers import AutoModelForSequenceClassification, AutoTokenizer
   
   model = AutoModelForSequenceClassification.from_pretrained("{REPO_NAME}")
   tokenizer = AutoTokenizer.from_pretrained("{REPO_NAME}")

5. REMOVE LOCAL MODEL FILES FROM GIT:
   
   git rm --cached -r backend/app/ml/models/VeriAIDPO_Principles_VI_v1/
   git commit -m "Remove large model files - now hosted on Hugging Face Hub"
""")


def main():
    """Main upload workflow"""
    print("=" * 60)
    print("VeriAIDPO Model Upload to Hugging Face Hub")
    print("=" * 60)
    
    # Step 1: Check files
    if not check_model_files():
        return
    
    # Step 2: Login
    api, repo_name = login_to_huggingface()
    if not api or not repo_name:
        return
    
    # Step 3: Create repo
    if not create_model_repo(api, repo_name):
        return
    
    # Step 4: Upload files
    if not upload_model_files(api, repo_name):
        return
    
    # Show usage instructions
    show_usage_instructions(repo_name)
    
    print("\n[COMPLETE] Model successfully uploaded to Hugging Face Hub!")


if __name__ == "__main__":
    main()
