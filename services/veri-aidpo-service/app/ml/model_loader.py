"""
VeriAIDPO Model Loader
Handles loading and inference for Vietnamese PDPL classification models

Version: 1.0.0
Status: PRODUCTION
"""

import os
from pathlib import Path
from typing import Dict, Optional, Tuple
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from loguru import logger
from functools import lru_cache


class VeriAIDPOModelLoader:
    """
    Singleton model loader for VeriAIDPO classification models
    
    Features:
    - Lazy loading (load model only when first needed)
    - Model caching (singleton pattern)
    - GPU support (auto-detect and use if available)
    - Vietnamese text optimization
    - Error handling with fallback
    """
    
    _instance = None
    _model = None
    _tokenizer = None
    _device = None
    _model_path = None
    _is_loaded = False
    
    def __new__(cls):
        """Singleton pattern - only one instance"""
        if cls._instance is None:
            cls._instance = super(VeriAIDPOModelLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize model loader (called once)"""
        if not self._is_loaded:
            self._setup_device()
            self._setup_model_path()
    
    def _setup_device(self):
        """Detect and setup compute device (GPU or CPU)"""
        if torch.cuda.is_available():
            self._device = torch.device("cuda")
            logger.info(f"[OK] VeriAIDPO using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self._device = torch.device("cpu")
            logger.info("[OK] VeriAIDPO using CPU")
    
    def _setup_model_path(self):
        """Setup model directory path - download from Hugging Face Hub if needed"""
        from huggingface_hub import snapshot_download
        import os
        
        # Get backend/app/ml/models directory
        current_dir = Path(__file__).parent
        models_dir = current_dir / "models"
        models_dir.mkdir(exist_ok=True)
        
        # Default to principles model
        self._model_path = models_dir / "VeriAIDPO_Principles_VI_v1"
        
        if not self._model_path.exists():
            logger.info(f"[OK] Model not found locally at {self._model_path}")
            logger.info("[OK] Downloading model from Hugging Face Hub...")
            
            try:
                # Get HF token from environment variable (required for private repos)
                hf_token = os.getenv("HF_TOKEN")
                if not hf_token:
                    logger.warning("[WARNING] HF_TOKEN not found - may fail for private repos")
                
                snapshot_download(
                    repo_id="TranHF/VeriAIDPO_Principles_VI_v1",
                    local_dir=str(self._model_path),
                    local_dir_use_symlinks=False,
                    token=hf_token  # Authentication for private repos
                )
                logger.info(f"[OK] Model downloaded successfully to {self._model_path}")
            except Exception as e:
                logger.error(f"[ERROR] Failed to download model: {e}")
                logger.warning("[WARNING] Model will need to be loaded manually")
        else:
            logger.info(f"[OK] Using local model at {self._model_path}")
    
    def load_model(self, model_type: str = "principles") -> bool:
        """
        Load VeriAIDPO model into memory
        
        Args:
            model_type: Model type to load (default: "principles")
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if self._is_loaded:
            logger.info("[OK] Model already loaded")
            return True
        
        try:
            logger.info(f"[OK] Loading VeriAIDPO {model_type} model...")
            
            # Verify model files exist
            required_files = [
                "model.safetensors",
                "config.json",
                "vocab.txt",
                "tokenizer_config.json"
            ]
            
            for file in required_files:
                file_path = self._model_path / file
                if not file_path.exists():
                    logger.error(f"[ERROR] Missing required file: {file}")
                    return False
                logger.debug(f"[OK] Found {file} ({file_path.stat().st_size / 1024 / 1024:.2f} MB)")
            
            # Load model
            logger.info(f"[OK] Loading model from {self._model_path}")
            self._model = AutoModelForSequenceClassification.from_pretrained(
                str(self._model_path),
                local_files_only=True
            )
            self._model.to(self._device)
            self._model.eval()
            
            # Load tokenizer
            logger.info("[OK] Loading tokenizer")
            self._tokenizer = AutoTokenizer.from_pretrained(
                str(self._model_path),
                local_files_only=True
            )
            
            self._is_loaded = True
            
            # Log model info
            num_labels = self._model.config.num_labels
            vocab_size = len(self._tokenizer)
            logger.info(f"[OK] Model loaded successfully")
            logger.info(f"    > Output labels: {num_labels}")
            logger.info(f"    > Vocabulary size: {vocab_size}")
            logger.info(f"    > Device: {self._device}")
            logger.info(f"    > Model type: {model_type}")
            
            return True
        
        except Exception as e:
            logger.error(f"[ERROR] Failed to load model: {e}")
            self._is_loaded = False
            return False
    
    def predict(self, text: str, max_length: int = 256) -> Optional[Dict]:
        """
        Run inference on Vietnamese text
        
        Args:
            text: Vietnamese text to classify
            max_length: Maximum token length (default: 256)
        
        Returns:
            Dict with prediction, confidence, and category_id
            None if prediction fails
        """
        # Ensure model is loaded
        if not self._is_loaded:
            success = self.load_model()
            if not success:
                logger.error("[ERROR] Cannot predict - model not loaded")
                return None
        
        try:
            # Tokenize input
            inputs = self._tokenizer(
                text,
                return_tensors='pt',
                max_length=max_length,
                truncation=True,
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self._device) for k, v in inputs.items()}
            
            # Run inference
            with torch.no_grad():
                outputs = self._model(**inputs)
            
            # Get predictions
            logits = outputs.logits[0]
            probs = torch.softmax(logits, dim=-1)
            
            predicted_category = probs.argmax().item()
            confidence = probs[predicted_category].item()
            
            # Get all probabilities for debugging
            all_probs = {
                f"cat_{i}": round(prob.item(), 4)
                for i, prob in enumerate(probs)
            }
            
            result = {
                'category_id': predicted_category,
                'confidence': round(confidence, 4),
                'all_probabilities': all_probs,
                'device': str(self._device)
            }
            
            logger.debug(f"Prediction: Cat {predicted_category} ({confidence:.2%})")
            
            return result
        
        except Exception as e:
            logger.error(f"[ERROR] Prediction failed: {e}")
            return None
    
    def get_model_info(self) -> Dict:
        """
        Get model information and status
        
        Returns:
            Dict with model metadata
        """
        if not self._is_loaded:
            return {
                'status': 'not_loaded',
                'model_path': str(self._model_path),
                'device': str(self._device),
                'message': 'Model will be loaded on first inference request'
            }
        
        return {
            'status': 'loaded',
            'model_path': str(self._model_path),
            'device': str(self._device),
            'num_labels': self._model.config.num_labels,
            'vocab_size': len(self._tokenizer),
            'max_length': 256,
            'model_type': 'VeriAIDPO_Principles_VI_v1'
        }
    
    def unload_model(self):
        """Unload model from memory (free resources)"""
        if self._is_loaded:
            self._model = None
            self._tokenizer = None
            self._is_loaded = False
            
            # Clear CUDA cache if using GPU
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            logger.info("[OK] Model unloaded from memory")
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._is_loaded


# Global singleton instance
_model_loader = None


def get_model_loader() -> VeriAIDPOModelLoader:
    """
    Get singleton model loader instance
    
    Returns:
        VeriAIDPOModelLoader: Shared model loader
    """
    global _model_loader
    if _model_loader is None:
        _model_loader = VeriAIDPOModelLoader()
    return _model_loader


def predict_pdpl_category(text: str) -> Optional[Dict]:
    """
    Convenience function for PDPL principles classification
    
    Args:
        text: Vietnamese text to classify
    
    Returns:
        Dict with prediction results or None if failed
    """
    loader = get_model_loader()
    return loader.predict(text)


# PDPL Category Names (Vietnamese + English)
PDPL_CATEGORIES = {
    0: {
        'vi': 'Tuân thủ pháp luật và minh bạch',
        'en': 'Lawfulness and Transparency',
        'description': 'Data processing must be lawful, fair, and transparent'
    },
    1: {
        'vi': 'Giới hạn mục đích',
        'en': 'Purpose Limitation',
        'description': 'Data must be collected for specified, explicit, and legitimate purposes'
    },
    2: {
        'vi': 'Tối thiểu hóa dữ liệu',
        'en': 'Data Minimization',
        'description': 'Only collect data that is necessary for the purpose'
    },
    3: {
        'vi': 'Chính xác',
        'en': 'Accuracy',
        'description': 'Data must be accurate and kept up to date'
    },
    4: {
        'vi': 'Giới hạn lưu trữ',
        'en': 'Storage Limitation',
        'description': 'Data must not be kept longer than necessary'
    },
    5: {
        'vi': 'An toàn bảo mật',
        'en': 'Security',
        'description': 'Data must be processed securely with appropriate safeguards'
    },
    6: {
        'vi': 'Trách nhiệm giải trình',
        'en': 'Accountability',
        'description': 'Organizations must demonstrate compliance and maintain records'
    },
    7: {
        'vi': 'Quyền của chủ thể dữ liệu',
        'en': 'Data Subject Rights',
        'description': 'Respect rights of individuals regarding their personal data'
    }
}


def get_category_info(category_id: int, language: str = 'vi') -> Dict:
    """
    Get category information by ID
    
    Args:
        category_id: Category ID (0-7)
        language: Language code ('vi' or 'en')
    
    Returns:
        Dict with category name and description
    """
    if category_id not in PDPL_CATEGORIES:
        return {
            'name': f'Unknown Category {category_id}',
            'description': 'Invalid category ID'
        }
    
    cat_info = PDPL_CATEGORIES[category_id]
    return {
        'name': cat_info[language],
        'description': cat_info['description']
    }
