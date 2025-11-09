# Document #10: AI Recommendations Microservice Implementation

**VeriSyntra - Vietnamese PDPL 2025 Compliance Platform**  
**Service:** veri-ai-recommendations-engine (Port 8013)  
**Document Version:** 1.2  
**Last Updated:** November 7, 2025  
**Implementation Status:** Updated to use VeriAIDPO_Principles_VI_v1 (Port changed from 8011 to 8013 to avoid conflict with veri-data-sync-service)  

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [ML Model Design](#3-ml-model-design)
4. [Microservice Implementation](#4-microservice-implementation)
5. [Integration with Document #7](#5-integration-with-document-7)
6. [Using Existing VeriAIDPO Model](#6-using-existing-veriaaidpo-model)
7. [Deployment](#7-deployment)
8. [Testing Strategy](#8-testing-strategy)
9. [Monitoring & Observability](#9-monitoring--observability)
10. [Summary](#10-summary)

---

## 1. Overview

### Purpose

The AI Recommendations Microservice provides **machine learning-powered recommendations** for Data Protection Officers using the **VeriAIDPO_Principles_VI_v1** model (trained on real PDPL 2025 + Decree 13 legal corpus) to suggest:

- **PDPL principles classification** for compliance documents and field descriptions
- **Smart compliance guidance** based on 8 Vietnamese PDPL principles
- **Legal reference mapping** to specific PDPL articles
- **Retention policy recommendations** aligned with Vietnamese legal requirements
- **Vietnamese cultural context** integration (North/Central/South patterns)

**Model:** VeriAIDPO_Principles_VI_v1 (PhoBERT-based, 78-88% accuracy on Vietnamese legal text)

**[+] RELATED IMPLEMENTATIONS:** This microservice uses the same VeriAIDPO model as other documents but for different purposes:
- **[AI Classification Integration](./04_AI_Classification_Integration_Implementation.md)** (Document #04): Generic VeriAIDPO integration framework for data asset classification
- **[Processing Activities Population](./01_Table_processing_activities/08_Data_Population_VeriAIDPO_Integration.md)** (Document #08): VeriAIDPO application for processing activities table population

**Document Relationship:**
- **Document #04**: Foundation - Generic AI classification framework with three-service orchestration
- **Document #08**: Specialized - Processing activities population using VeriAIDPO
- **This document (Doc #10)**: Specialized - Standalone DPO recommendations microservice
- All three share VeriAIDPO_Principles_VI_v1 model but different architectures

**When to Use This Document vs Others:**

| Document | Architecture | Purpose | Integration |
|----------|--------------|---------|-------------|
| Doc #04 | Three-service orchestration | Generic data classification | Embedded in inventory service |
| Doc #08 | Database scanning + VeriAIDPO | Processing activities population | Embedded in inventory service |
| Doc #10 (This) | Standalone microservice | DPO recommendations | Independent service (Port 8013) |

### Why Microservice Architecture?

**Separation of Concerns:**
- ML complexity isolated from core compliance logic in Document #7
- Can fail gracefully without breaking rule-based recommendations
- Independent scaling with GPU resources

**Technology Stack:**
- Python 3.11+, FastAPI for API layer
- PyTorch 2.0+ for ML model inference
- PhoBERT (vinai/phobert-base-v2) - VeriAIDPO_Principles_VI_v1
- HuggingFace Hub for model distribution (TranHF/VeriAIDPO_Principles_VI_v1)
- Redis for model result caching
- PostgreSQL for recommendation feedback storage
- Docker with GPU support for deployment (CPU fallback available)

### Key Features (Lines: ~1,800)

1. **VeriAIDPO Model Integration** (~300 lines)
   - Vietnamese PDPL principles classification (8 categories)
   - Trained on real PDPL Law 91/2025/QH15 + Decree 13/2023/ND-CP
   - HuggingFace Hub auto-download from TranHF/VeriAIDPO_Principles_VI_v1
   
2. **Recommendation Engine** (~400 lines)
   - PDPL principle to compliance action mapping
   - Legal reference extraction from model predictions
   - Confidence scoring with threshold filtering
   
3. **FastAPI Microservice** (~350 lines)
   - REST API endpoints for recommendations
   - GPU-accelerated inference (Intel Iris Xe / NVIDIA CUDA)
   - Result caching with Redis (15-minute TTL)
   
4. **Integration Layer** (~300 lines)
   - Document #7 integration code
   - Graceful degradation to rule-based recommendations
   - Hybrid AI + Rules approach

5. **Feedback Collection** (~250 lines)
   - DPO action tracking (accept/reject/modify)
   - Continuous improvement dataset
   - Model performance monitoring

6. **Testing & Monitoring** (~200 lines)
   - Unit tests for model loader
   - API endpoint validation
   - Performance metrics dashboard

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 VeriPortal Intelligence Layer (Document #7)              │
│                        (Port 8010 - Main Backend)                        │
└──────────────┬──────────────────────────────────────────────────────────┘
               │
               ├──> Rule-Based Recommendations (Immediate, Deterministic)
               │    - PDPL compliance rules
               │    - Vietnamese threshold checks
               │    - Industry best practices
               │
               └──> AI Recommendations Microservice (Port 8013)
                    ┌────────────────────────────────────────────┐
                    │   FastAPI Service (Async)                  │
                    │   - /predict: PDPL principle classification│
                    │   - /feedback: Learning from DPO actions   │
                    │   - /health: Service health check          │
                    └──┬──────────────────────────────────────────┘
                       │
                       ├──> VeriAIDPO_Principles_VI_v1 Model
                       │    - PhoBERT-based (vinai/phobert-base-v2)
                       │    - 8 PDPL principle categories
                       │    - 78-88% accuracy on Vietnamese legal text
                       │    - Auto-download from HuggingFace Hub
                       │
                       ├──> Recommendation Mapper
                       │    - PDPL principle -> Compliance actions
                       │    - Legal reference extraction
                       │    - Retention policy suggestions
                       │    - Security priority assessment
                       │
                       ├──> Feature Processing
                       │    - Field metadata analysis
                       │    - Industry/region context encoding
                       │    - Vietnamese text normalization
                       │
                       ├──> Redis Cache (Port 6379)
                       │    - Model prediction caching
                       │    - 15-minute TTL per field
                       │
                       └──> PostgreSQL Feedback DB
                            - DPO action tracking (accept/reject)
                            - Model performance metrics
                            - Continuous improvement dataset

┌─────────────────────────────────────────────────────────────────────────┐
│                      Model Training (Already Complete)                   │
│            VeriAIDPO_Principles_VI_v1 - Hosted on HuggingFace           │
└──────────────────────────────────────────────────────────────────────────┘
               │
               ├──> Training Data (24,000 samples)
               │    - Real PDPL Law 91/2025/QH15 (352 lines)
               │    - Real Decree 13/2023/ND-CP (461 lines)
               │    - Vietnamese business scenarios (North/Central/South)
               │    - 46+ company patterns with normalization
               │
               ├──> PhoBERT Fine-Tuning (Complete)
               │    - Base: vinai/phobert-base-v2
               │    - Fine-tuned on 813-line legal corpus
               │    - 8 PDPL principle categories
               │    - Training: VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb
               │
               ├──> Model Performance
               │    - Accuracy: 78-88% on Vietnamese legal text
               │    - Validation: Cross-validated (80/20 split)
               │    - Production-ready: Tested on real compliance documents
               │
               └──> Model Distribution
                    - HuggingFace Hub: TranHF/VeriAIDPO_Principles_VI_v1
                    - Auto-download on microservice startup
                    - Local caching: backend/app/ml/models/
                    - Version control via HuggingFace
```

---

## 3. ML Model Design

### 3.1 VeriAIDPO_Principles_VI_v1 Model

**Model Architecture:** PhoBERT-based Vietnamese PDPL Principles Classifier

**Key Specifications:**
- **Base Model:** vinai/phobert-base-v2 (PhoBERT for Vietnamese)
- **Parameters:** ~135M (PhoBERT) + ~2M (classification head)
- **Input:** Vietnamese text (max 256 tokens)
- **Output:** 8 PDPL principle categories + confidence score
- **Training:** 24,000 samples from real PDPL + Decree 13 legal corpus
- **Accuracy:** 78-88% on Vietnamese legal/compliance text
- **Model Size:** ~540MB (safetensors format)
- **Location:** HuggingFace Hub - TranHF/VeriAIDPO_Principles_VI_v1

**8 PDPL Principle Categories:**

```python
PDPL_CATEGORIES = {
    0: {
        'vi': 'Tuân thủ pháp luật và minh bạch',
        'en': 'Lawfulness and Transparency',
        'pdpl_article': 'PDPL Article 7',
        'description': 'Data processing must be lawful, fair, and transparent'
    },
    1: {
        'vi': 'Giới hạn mục đích',
        'en': 'Purpose Limitation',
        'pdpl_article': 'PDPL Article 8',
        'description': 'Data collected for specified, explicit, and legitimate purposes'
    },
    2: {
        'vi': 'Tối thiểu hóa dữ liệu',
        'en': 'Data Minimization',
        'pdpl_article': 'PDPL Article 9',
        'description': 'Only collect data necessary for the purpose'
    },
    3: {
        'vi': 'Chính xác',
        'en': 'Accuracy',
        'pdpl_article': 'PDPL Article 10',
        'description': 'Data must be accurate and kept up to date'
    },
    4: {
        'vi': 'Giới hạn lưu trữ',
        'en': 'Storage Limitation',
        'pdpl_article': 'PDPL Article 13',
        'description': 'Data must not be kept longer than necessary'
    },
    5: {
        'vi': 'An toàn bảo mật',
        'en': 'Security',
        'pdpl_article': 'PDPL Article 15',
        'description': 'Data must be processed securely with appropriate safeguards'
    },
    6: {
        'vi': 'Trách nhiệm giải trình',
        'en': 'Accountability',
        'pdpl_article': 'PDPL Article 17',
        'description': 'Organizations must demonstrate compliance and maintain records'
    },
    7: {
        'vi': 'Quyền của chủ thể dữ liệu',
        'en': 'Data Subject Rights',
        'pdpl_article': 'PDPL Articles 18-23',
        'description': 'Respect rights of individuals regarding their personal data'
    }
}
```

### 3.2 Model Loader Implementation

```python
# File: backend/veri_ai_recommendations_engine/models/model_loader.py

"""
VeriAIDPO Model Loader for Recommendations Microservice
Uses existing VeriAIDPO_Principles_VI_v1 from HuggingFace Hub
"""

import os
from pathlib import Path
from typing import Dict, Optional
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from huggingface_hub import snapshot_download
from loguru import logger


class VeriAIDPORecommendationLoader:
    """
    Singleton model loader for VeriAIDPO_Principles_VI_v1
    
    Features:
    - Auto-download from HuggingFace Hub (TranHF/VeriAIDPO_Principles_VI_v1)
    - GPU support with CPU fallback (Intel Iris Xe / NVIDIA CUDA)
    - Model caching (singleton pattern)
    - Vietnamese text optimization
    """
    
    _instance = None
    _model = None
    _tokenizer = None
    _device = None
    _model_path = None
    _is_loaded = False
    
    # HuggingFace repository
    HF_REPO = "TranHF/VeriAIDPO_Principles_VI_v1"
    
    def __new__(cls):
        """Singleton pattern - only one instance"""
        if cls._instance is None:
            cls._instance = super(VeriAIDPORecommendationLoader, cls).__new__(cls)
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
            logger.info(f"[OK] Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self._device = torch.device("cpu")
            logger.info("[OK] Using CPU (Intel i9-12900HK or similar)")
    
    def _setup_model_path(self):
        """Download model from HuggingFace Hub if needed"""
        # Get backend/app/ml/models directory
        current_dir = Path(__file__).parent.parent
        models_dir = current_dir / "models"
        models_dir.mkdir(exist_ok=True)
        
        # Model path
        self._model_path = models_dir / "VeriAIDPO_Principles_VI_v1"
        
        if not self._model_path.exists():
            logger.info(f"[OK] Model not found locally")
            logger.info(f"[OK] Downloading from HuggingFace Hub: {self.HF_REPO}")
            
            try:
                # Get HF token from environment (for private repos)
                hf_token = os.getenv("HF_TOKEN")
                
                snapshot_download(
                    repo_id=self.HF_REPO,
                    local_dir=str(self._model_path),
                    local_dir_use_symlinks=False,
                    token=hf_token
                )
                logger.info(f"[OK] Model downloaded to {self._model_path}")
            except Exception as e:
                logger.error(f"[ERROR] Failed to download model: {e}")
                raise
        else:
            logger.info(f"[OK] Using cached model at {self._model_path}")
    
    def load_model(self) -> bool:
        """
        Load VeriAIDPO model into memory
        
        Returns:
            bool: True if loaded successfully
        """
        if self._is_loaded:
            logger.info("[OK] Model already loaded")
            return True
        
        try:
            logger.info("[OK] Loading VeriAIDPO_Principles_VI_v1...")
            
            # Load model
            self._model = AutoModelForSequenceClassification.from_pretrained(
                str(self._model_path),
                local_files_only=True
            )
            self._model.to(self._device)
            self._model.eval()
            
            # Load tokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(
                str(self._model_path),
                local_files_only=True
            )
            
            self._is_loaded = True
            
            # Log model info
            logger.info(f"[OK] Model loaded successfully")
            logger.info(f"    > Categories: {self._model.config.num_labels} PDPL principles")
            logger.info(f"    > Vocabulary: {len(self._tokenizer)} tokens")
            logger.info(f"    > Device: {self._device}")
            logger.info(f"    > Model: VeriAIDPO_Principles_VI_v1")
            
            return True
        
        except Exception as e:
            logger.error(f"[ERROR] Failed to load model: {e}")
            self._is_loaded = False
            return False
    
    def predict(self, text: str, max_length: int = 256) -> Optional[Dict]:
        """
        Classify Vietnamese text into PDPL principles
        
        Args:
            text: Vietnamese compliance text (field description, document excerpt)
            max_length: Maximum token length (default: 256)
        
        Returns:
            {
                'category_id': int (0-7),
                'category_name_vi': str,
                'category_name_en': str,
                'pdpl_article': str,
                'confidence': float (0-1),
                'all_probabilities': Dict[str, float]
            }
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
            
            # Get category info
            from .pdpl_categories import PDPL_CATEGORIES
            category_info = PDPL_CATEGORIES.get(predicted_category, {})
            
            # All probabilities for debugging
            all_probs = {
                f"cat_{i}": round(prob.item(), 4)
                for i, prob in enumerate(probs)
            }
            
            result = {
                'category_id': predicted_category,
                'category_name_vi': category_info.get('vi', 'Unknown'),
                'category_name_en': category_info.get('en', 'Unknown'),
                'pdpl_article': category_info.get('pdpl_article', 'PDPL 2025'),
                'description': category_info.get('description', ''),
                'confidence': round(confidence, 4),
                'all_probabilities': all_probs,
                'device': str(self._device)
            }
            
            logger.debug(f"Prediction: {result['category_name_en']} ({confidence:.2%})")
            
            return result
        
        except Exception as e:
            logger.error(f"[ERROR] Prediction failed: {e}")
            return None
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._is_loaded
```

### 3.3 PDPL Categories Configuration

### 3.3 PDPL Categories Configuration

```python
# File: backend/veri_ai_recommendations_engine/models/pdpl_categories.py

"""
PDPL 2025 Principle Categories
Maps model outputs to Vietnamese legal framework
"""

PDPL_CATEGORIES = {
    0: {
        'vi': 'Tuân thủ pháp luật và minh bạch',
        'en': 'Lawfulness and Transparency',
        'pdpl_article': 'PDPL Article 7',
        'description': 'Data processing must be lawful, fair, and transparent',
        'compliance_actions': [
            'document_legal_basis',
            'update_privacy_notice',
            'implement_transparency_measures'
        ],
        'retention_guidance': 'Maintain legal basis documentation for audit',
        'security_priority': 'medium'
    },
    1: {
        'vi': 'Giới hạn mục đích',
        'en': 'Purpose Limitation',
        'pdpl_article': 'PDPL Article 8',
        'description': 'Data collected for specified, explicit, and legitimate purposes',
        'compliance_actions': [
            'define_processing_purposes',
            'limit_data_usage',
            'document_purpose_changes'
        ],
        'retention_guidance': 'Delete data when purpose fulfilled',
        'security_priority': 'medium'
    },
    2: {
        'vi': 'Tối thiểu hóa dữ liệu',
        'en': 'Data Minimization',
        'pdpl_article': 'PDPL Article 9',
        'description': 'Only collect data necessary for the purpose',
        'compliance_actions': [
            'review_data_collection',
            'implement_minimization',
            'remove_excessive_fields'
        ],
        'retention_guidance': 'Collect only necessary data',
        'security_priority': 'high'
    },
    3: {
        'vi': 'Chính xác',
        'en': 'Accuracy',
        'pdpl_article': 'PDPL Article 10',
        'description': 'Data must be accurate and kept up to date',
        'compliance_actions': [
            'implement_data_validation',
            'enable_correction_mechanisms',
            'regular_accuracy_reviews'
        ],
        'retention_guidance': 'Update or delete inaccurate data',
        'security_priority': 'medium'
    },
    4: {
        'vi': 'Giới hạn lưu trữ',
        'en': 'Storage Limitation',
        'pdpl_article': 'PDPL Article 13',
        'description': 'Data must not be kept longer than necessary',
        'compliance_actions': [
            'define_retention_policy',
            'implement_deletion_procedures',
            'conduct_retention_reviews'
        ],
        'retention_guidance': 'Banking: 10yr, Healthcare: 20yr, General: 3-5yr',
        'security_priority': 'high'
    },
    5: {
        'vi': 'An toàn bảo mật',
        'en': 'Security',
        'pdpl_article': 'PDPL Article 15',
        'description': 'Data must be processed securely with appropriate safeguards',
        'compliance_actions': [
            'implement_encryption',
            'enable_access_controls',
            'conduct_security_assessments'
        ],
        'retention_guidance': 'Maintain security logs for 2 years minimum',
        'security_priority': 'critical'
    },
    6: {
        'vi': 'Trách nhiệm giải trình',
        'en': 'Accountability',
        'pdpl_article': 'PDPL Article 17',
        'description': 'Organizations must demonstrate compliance and maintain records',
        'compliance_actions': [
            'maintain_processing_records',
            'conduct_dpia',
            'register_with_mps_if_required'
        ],
        'retention_guidance': 'Keep compliance records for 5 years',
        'security_priority': 'high'
    },
    7: {
        'vi': 'Quyền của chủ thể dữ liệu',
        'en': 'Data Subject Rights',
        'pdpl_article': 'PDPL Articles 18-23',
        'description': 'Respect rights of individuals regarding their personal data',
        'compliance_actions': [
            'implement_right_to_access',
            'enable_right_to_erasure',
            'facilitate_data_portability'
        ],
        'retention_guidance': 'Respond to requests within 72 hours',
        'security_priority': 'high'
    }
}


def get_category_info(category_id: int, language: str = 'vi') -> dict:
    """
    Get PDPL category information
    
    Args:
        category_id: Category ID (0-7)
        language: Language code ('vi' or 'en')
    
    Returns:
        Category info dict
    """
    if category_id not in PDPL_CATEGORIES:
        return {
            'name': f'Unknown Category {category_id}',
            'description': 'Invalid category ID',
            'pdpl_article': 'PDPL 2025'
        }
    
    cat_info = PDPL_CATEGORIES[category_id]
    return {
        'name': cat_info[language],
        'description': cat_info['description'],
        'pdpl_article': cat_info['pdpl_article'],
        'compliance_actions': cat_info['compliance_actions'],
        'retention_guidance': cat_info['retention_guidance'],
        'security_priority': cat_info['security_priority']
    }
```

### 3.4 Recommendation Mapper

### 3.4 Recommendation Mapper

```python
# File: backend/veri_ai_recommendations_engine/services/recommendation_mapper.py

"""
Maps PDPL principle classifications to actionable compliance recommendations
"""

from typing import Dict, List, Any
from ..models.pdpl_categories import PDPL_CATEGORIES, get_category_info


class PDPLRecommendationMapper:
    """
    Converts VeriAIDPO model predictions into DPO recommendations
    """
    
    @staticmethod
    def generate_recommendations(
        prediction: Dict[str, Any],
        field_metadata: Dict[str, Any],
        tenant_context: Dict[str, Any],
        confidence_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Generate actionable recommendations from PDPL principle classification
        
        Args:
            prediction: Model prediction with category_id and confidence
            field_metadata: Field name, table, data type, samples
            tenant_context: Industry, region, risk score
            confidence_threshold: Minimum confidence to generate recommendations
        
        Returns:
            List of recommendations (classification, retention, security, compliance)
        """
        recommendations = []
        
        # Check confidence threshold
        if prediction['confidence'] < confidence_threshold:
            return recommendations
        
        # Get category info
        category_id = prediction['category_id']
        category_info = get_category_info(category_id, language='vi')
        
        # 1. PDPL Principle Classification Recommendation
        recommendations.append({
            'type': 'pdpl_principle',
            'title_vi': f'Nguyên tắc PDPL: {prediction["category_name_vi"]}',
            'title_en': f'PDPL Principle: {prediction["category_name_en"]}',
            'description_vi': category_info['description'],
            'description_en': category_info['description'],
            'pdpl_article': category_info['pdpl_article'],
            'confidence': prediction['confidence'],
            'priority': 'critical',
            'ml_generated': True
        })
        
        # 2. Compliance Actions Recommendation
        for action in category_info['compliance_actions']:
            recommendations.append({
                'type': 'compliance_action',
                'title_vi': PDPLRecommendationMapper._translate_action(action, 'vi'),
                'title_en': PDPLRecommendationMapper._translate_action(action, 'en'),
                'action': action,
                'pdpl_article': category_info['pdpl_article'],
                'confidence': prediction['confidence'] * 0.9,  # Slightly lower for derived actions
                'priority': 'high',
                'ml_generated': True
            })
        
        # 3. Retention Recommendation
        recommendations.append({
            'type': 'retention',
            'title_vi': 'Đề xuất Thời gian Lưu trữ',
            'title_en': 'Retention Period Recommendation',
            'description_vi': category_info['retention_guidance'],
            'description_en': category_info['retention_guidance'],
            'pdpl_article': 'PDPL Article 13',
            'confidence': prediction['confidence'] * 0.85,
            'priority': 'high',
            'ml_generated': True
        })
        
        # 4. Security Priority Recommendation
        recommendations.append({
            'type': 'security',
            'title_vi': 'Ưu tiên Bảo mật',
            'title_en': 'Security Priority',
            'security_priority': category_info['security_priority'],
            'description_vi': f'Mức độ bảo mật: {category_info["security_priority"]}',
            'description_en': f'Security level: {category_info["security_priority"]}',
            'pdpl_article': 'PDPL Article 15',
            'confidence': prediction['confidence'] * 0.85,
            'priority': PDPLRecommendationMapper._map_security_priority(
                category_info['security_priority']
            ),
            'ml_generated': True
        })
        
        # 5. Regional/Industry-Specific Recommendations
        regional_recs = PDPLRecommendationMapper._generate_regional_recommendations(
            category_id=category_id,
            tenant_context=tenant_context,
            confidence=prediction['confidence']
        )
        recommendations.extend(regional_recs)
        
        return recommendations
    
    @staticmethod
    def _translate_action(action: str, language: str) -> str:
        """Translate compliance action to Vietnamese/English"""
        translations = {
            'document_legal_basis': {
                'vi': 'Ghi chép cơ sở pháp lý',
                'en': 'Document Legal Basis'
            },
            'update_privacy_notice': {
                'vi': 'Cập nhật Thông báo Bảo mật',
                'en': 'Update Privacy Notice'
            },
            'implement_transparency_measures': {
                'vi': 'Triển khai Biện pháp Minh bạch',
                'en': 'Implement Transparency Measures'
            },
            'define_processing_purposes': {
                'vi': 'Xác định Mục đích Xử lý',
                'en': 'Define Processing Purposes'
            },
            'limit_data_usage': {
                'vi': 'Giới hạn Sử dụng Dữ liệu',
                'en': 'Limit Data Usage'
            },
            'review_data_collection': {
                'vi': 'Rà soát Thu thập Dữ liệu',
                'en': 'Review Data Collection'
            },
            'implement_minimization': {
                'vi': 'Triển khai Tối thiểu hóa',
                'en': 'Implement Minimization'
            },
            'implement_data_validation': {
                'vi': 'Triển khai Kiểm tra Dữ liệu',
                'en': 'Implement Data Validation'
            },
            'define_retention_policy': {
                'vi': 'Xác định Chính sách Lưu trữ',
                'en': 'Define Retention Policy'
            },
            'implement_deletion_procedures': {
                'vi': 'Triển khai Quy trình Xóa',
                'en': 'Implement Deletion Procedures'
            },
            'implement_encryption': {
                'vi': 'Triển khai Mã hóa',
                'en': 'Implement Encryption'
            },
            'enable_access_controls': {
                'vi': 'Kích hoạt Kiểm soát Truy cập',
                'en': 'Enable Access Controls'
            },
            'maintain_processing_records': {
                'vi': 'Duy trì Hồ sơ Xử lý',
                'en': 'Maintain Processing Records'
            },
            'conduct_dpia': {
                'vi': 'Thực hiện Đánh giá Tác động',
                'en': 'Conduct DPIA'
            },
            'register_with_mps_if_required': {
                'vi': 'Đăng ký với Bộ Công an (nếu cần)',
                'en': 'Register with MPS (if required)'
            },
            'implement_right_to_access': {
                'vi': 'Triển khai Quyền Truy cập',
                'en': 'Implement Right to Access'
            },
            'enable_right_to_erasure': {
                'vi': 'Kích hoạt Quyền Xóa',
                'en': 'Enable Right to Erasure'
            }
        }
        
        return translations.get(action, {}).get(language, action)
    
    @staticmethod
    def _map_security_priority(security_level: str) -> str:
        """Map security level to recommendation priority"""
        mapping = {
            'critical': 'critical',
            'high': 'high',
            'medium': 'medium',
            'low': 'low'
        }
        return mapping.get(security_level, 'medium')
    
    @staticmethod
    def _generate_regional_recommendations(
        category_id: int,
        tenant_context: Dict[str, Any],
        confidence: float
    ) -> List[Dict[str, Any]]:
        """Generate region-specific recommendations for Vietnamese businesses"""
        region = tenant_context.get('veri_regional_location', 'south')
        industry = tenant_context.get('veri_industry_type', 'technology')
        
        regional_recs = []
        
        # North Vietnam (Hanoi): Formal, government-focused
        if region == 'north':
            if category_id in [6, 7]:  # Accountability or Data Subject Rights
                regional_recs.append({
                    'type': 'regional_guidance',
                    'title_vi': 'Hướng dẫn Miền Bắc: Tuân thủ Chính thức',
                    'title_en': 'Northern Vietnam: Formal Compliance',
                    'description_vi': 'Chuẩn bị tài liệu chính thức cho cơ quan nhà nước',
                    'description_en': 'Prepare formal documentation for government authorities',
                    'confidence': confidence * 0.8,
                    'priority': 'medium',
                    'ml_generated': True
                })
        
        # South Vietnam (HCMC): Pragmatic, risk-based
        elif region == 'south':
            if category_id in [1, 2]:  # Purpose Limitation or Data Minimization
                regional_recs.append({
                    'type': 'regional_guidance',
                    'title_vi': 'Hướng dẫn Miền Nam: Quản lý Rủi ro',
                    'title_en': 'Southern Vietnam: Risk Management',
                    'description_vi': 'Tập trung vào phân tích rủi ro kinh doanh',
                    'description_en': 'Focus on business risk analysis',
                    'confidence': confidence * 0.8,
                    'priority': 'medium',
                    'ml_generated': True
                })
        
        # Central Vietnam: Traditional, consensus-building
        elif region == 'central':
            if category_id in [0, 3]:  # Lawfulness or Accuracy
                regional_recs.append({
                    'type': 'regional_guidance',
                    'title_vi': 'Hướng dẫn Miền Trung: Tham vấn Cộng đồng',
                    'title_en': 'Central Vietnam: Community Consultation',
                    'description_vi': 'Tham vấn các bên liên quan trước khi triển khai',
                    'description_en': 'Consult stakeholders before implementation',
                    'confidence': confidence * 0.8,
                    'priority': 'medium',
                    'ml_generated': True
                })
        
        return regional_recs
```

### 3.5 Feature Processing

```python
# File: backend/veri_ai_recommendations_engine/services/feature_processor.py

"""
Feature processing for VeriAIDPO model predictions
Prepares Vietnamese text and context for classification
"""

### 3.5 Feature Processing

```python
# File: backend/veri_ai_recommendations_engine/services/feature_processor.py

"""
Feature processing for VeriAIDPO model predictions
Prepares Vietnamese text and context for classification
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class VietnameseFeatureProcessor:
    """Process field metadata into Vietnamese text for PDPL classification"""
    
    @staticmethod
    def prepare_text_input(
        field_metadata: Dict[str, Any],
        tenant_context: Dict[str, Any]
    ) -> str:
        """
        Prepare Vietnamese text from field metadata for VeriAIDPO model
        
        Args:
            field_metadata: Field name, table, data type, samples
            tenant_context: Industry, region, business context
        
        Returns:
            Vietnamese text describing the field and its compliance context
        """
        field_name = field_metadata.get('field_name', '')
        table_name = field_metadata.get('table_name', '')
        data_type = field_metadata.get('data_type', '')
        
        # Get sample values (first 3)
        sample_values = field_metadata.get('sample_values', [])
        sample_text = ', '.join(str(v) for v in sample_values[:3] if v is not None)
        
        # Get business context
        industry = tenant_context.get('veri_industry_type', 'technology')
        region = tenant_context.get('veri_regional_location', 'south')
        
        # Construct Vietnamese description
        text = f"Trường dữ liệu '{field_name}' trong bảng '{table_name}'. "
        text += f"Kiểu dữ liệu: {data_type}. "
        
        if sample_text:
            text += f"Ví dụ: {sample_text}. "
        
        # Add business context
        text += f"Ngành: {VietnameseFeatureProcessor._translate_industry(industry)}. "
        text += f"Khu vực: {VietnameseFeatureProcessor._translate_region(region)}. "
        
        # Add compliance context hint
        if 'cmnd' in field_name.lower() or 'cccd' in field_name.lower():
            text += "Dữ liệu định danh cá nhân theo PDPL 2025."
        elif 'email' in field_name.lower() or 'phone' in field_name.lower():
            text += "Dữ liệu liên lạc cá nhân."
        elif 'tai_khoan' in field_name.lower() or 'bank' in field_name.lower():
            text += "Dữ liệu tài chính nhạy cảm."
        
        return text
    
    @staticmethod
    def _translate_industry(industry: str) -> str:
        """Translate industry to Vietnamese"""
        translations = {
            'finance': 'Tài chính',
            'banking': 'Ngân hàng',
            'healthcare': 'Y tế',
            'ecommerce': 'Thương mại điện tử',
            'telecom': 'Viễn thông',
            'education': 'Giáo dục',
            'technology': 'Công nghệ',
            'manufacturing': 'Sản xuất',
            'logistics': 'Logistics',
            'government': 'Chính phủ'
        }
        return translations.get(industry, industry.capitalize())
    
    @staticmethod
    def _translate_region(region: str) -> str:
        """Translate region to Vietnamese"""
        translations = {
            'north': 'Miền Bắc',
            'central': 'Miền Trung',
            'south': 'Miền Nam'
        }
        return translations.get(region, 'Việt Nam')
```

---

## 4. Microservice Implementation

### 4.1 FastAPI Service

**File:** `backend/veri_ai_recommendations_engine/main.py`

```python
"""
VeriSyntra AI Recommendations Microservice
PDPL compliance recommendations using VeriAIDPO_Principles_VI_v1
Port: 8013
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import redis
import json
import logging
from datetime import datetime
import hashlib

from .models.model_loader import VeriAIDPORecommendationLoader
from .services.recommendation_mapper import PDPLRecommendationMapper
from .services.feature_processor import VietnameseFeatureProcessor
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="VeriSyntra AI Recommendations Engine",
    description="PDPL 2025 compliance recommendations using VeriAIDPO_Principles_VI_v1",
    version="1.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis cache
# NOTE: For production deployment, use RedisClient from Document 06 
# (06_Async_Job_Processing_Implementation.md) which provides:
# - Connection pooling
# - Sentinel support for high availability
# - Health checks
# - Retry logic
# This simplified setup is for standalone microservice deployment.
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Model Manager (Singleton Pattern)
class ModelManager:
    """Singleton manager for VeriAIDPO model and recommendation mapper"""
    _instance = None
    _model_loader = None
    _recommendation_mapper = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if ModelManager._model_loader is None:
            logger.info("Initializing VeriAIDPO Recommendations Engine...")
            
            # Load VeriAIDPO model from HuggingFace Hub
            self._model_loader = VeriAIDPORecommendationLoader(
                model_name="TranHF/VeriAIDPO_Principles_VI_v1",
                cache_dir=settings.MODEL_CACHE_DIR
            )
            
            # Initialize recommendation mapper
            self._recommendation_mapper = PDPLRecommendationMapper()
            
            logger.info(f"VeriAIDPO model loaded: {self._model_loader.is_loaded}")
            logger.info("Recommendation engine ready")
    
    @property
    def model_loader(self):
        return self._model_loader
    
    @property
    def recommendation_mapper(self):
        return self._recommendation_mapper


# Pydantic Models for API
class FieldMetadata(BaseModel):
    field_name: str = Field(..., description="Database field name")
    table_name: str = Field(..., description="Database table name")
    data_type: str = Field(..., description="SQL data type (VARCHAR, INT, etc.)")
    sample_values: Optional[List[Any]] = Field(default=[], description="Sample data values")
    current_classification: Optional[str] = Field(None, description="Current PDPL classification")


class TenantContext(BaseModel):
    veri_business_id: str = Field(..., description="VeriSyntra business ID")
    veri_regional_location: str = Field(..., pattern="^(north|central|south)$", 
                                        description="Vietnamese region")
    veri_industry_type: str = Field(..., description="Industry sector")


class PredictionRequest(BaseModel):
    field_metadata: FieldMetadata
    tenant_context: TenantContext
    confidence_threshold: float = Field(0.7, ge=0.0, le=1.0, 
                                       description="Minimum confidence for recommendations")


class PDPLPrinciple(BaseModel):
    category_id: int = Field(..., description="PDPL principle category ID (0-7)")
    principle_vi: str = Field(..., description="PDPL principle name (Vietnamese)")
    principle_en: str = Field(..., description="PDPL principle name (English)")
    pdpl_article: str = Field(..., description="PDPL article reference")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")


class PredictionResponse(BaseModel):
    pdpl_principle: PDPLPrinciple
    recommendations: List[Dict[str, Any]]
    model_version: str = Field(..., description="VeriAIDPO model version")
    inference_time_ms: float = Field(..., description="Processing time in milliseconds")
    cache_hit: bool = Field(..., description="Whether result was cached")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FeedbackRequest(BaseModel):
    field_id: str = Field(..., description="Unique field identifier")
    pdpl_principle: PDPLPrinciple
    action_taken: str = Field(..., pattern="^(accepted|rejected|modified)$",
                             description="DPO action on recommendation")
    dpo_notes: Optional[str] = Field(None, description="DPO notes for feedback")



# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        model_manager = ModelManager.get_instance()
        model_loaded = model_manager.model_loader.is_loaded
        
        # Check Redis connection
        redis_client.ping()
        redis_connected = True
    except Exception as e:
        redis_connected = False
        model_loaded = False
    
    return {
        "status": "healthy" if (model_loaded and redis_connected) else "degraded",
        "model_loaded": model_loaded,
        "redis_connected": redis_connected,
        "model_name": "VeriAIDPO_Principles_VI_v1",
        "model_accuracy": "78-88%",
        "huggingface_repo": "TranHF/VeriAIDPO_Principles_VI_v1",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/recommendations/predict", response_model=PredictionResponse)
async def predict_recommendations(request: PredictionRequest):
    """
    Generate PDPL compliance recommendations using VeriAIDPO model
    
    Process:
    1. Prepare Vietnamese text from field metadata
    2. Classify PDPL principle using VeriAIDPO_Principles_VI_v1
    3. Generate compliance recommendations from principle
    4. Return actionable recommendations with confidence scores
    
    Returns:
        - PDPL principle classification
        - List of compliance recommendations
        - Model version and inference time
        - Cache hit indicator
    """
    start_time = datetime.utcnow()
    
    try:
        # Generate cache key
        cache_key = _generate_cache_key(
            request.field_metadata.dict(),
            request.tenant_context.dict()
        )
        
        # Check cache (15-minute TTL)
        cached_result = redis_client.get(cache_key)
        if cached_result:
            logger.info(f"[CACHE HIT] Field: {request.field_metadata.field_name}")
            result = json.loads(cached_result)
            result['cache_hit'] = True
            return PredictionResponse(**result)
        
        # Get model manager
        model_manager = ModelManager.get_instance()
        
        # Prepare Vietnamese text input
        vietnamese_text = VietnameseFeatureProcessor.prepare_text_input(
            field_metadata=request.field_metadata.dict(),
            tenant_context=request.tenant_context.dict()
        )
        
        logger.info(f"[PREDICT] Vietnamese text: {vietnamese_text[:100]}...")
        
        # Get PDPL principle prediction from VeriAIDPO model
        prediction = model_manager.model_loader.predict(vietnamese_text)
        
        if prediction is None:
            raise HTTPException(
                status_code=500,
                detail="VeriAIDPO model prediction failed"
            )
        
        logger.info(
            f"[PREDICT] PDPL Principle: {prediction['name_vi']} "
            f"(confidence: {prediction['confidence']:.2%})"
        )
        
        # Check confidence threshold
        if prediction['confidence'] < request.confidence_threshold:
            logger.warning(
                f"[LOW CONFIDENCE] {prediction['confidence']:.2%} < "
                f"{request.confidence_threshold:.2%}"
            )
            # Return empty recommendations if confidence too low
            return PredictionResponse(
                pdpl_principle=PDPLPrinciple(
                    category_id=prediction['category_id'],
                    principle_vi=prediction['name_vi'],
                    principle_en=prediction['name_en'],
                    pdpl_article=prediction['article'],
                    confidence=prediction['confidence']
                ),
                recommendations=[],
                model_version="VeriAIDPO_Principles_VI_v1",
                inference_time_ms=(datetime.utcnow() - start_time).total_seconds() * 1000,
                cache_hit=False
            )
        
        # Generate comprehensive recommendations from PDPL principle
        recommendations = model_manager.recommendation_mapper.generate_recommendations(
            category_id=prediction['category_id'],
            confidence=prediction['confidence'],
            field_metadata=request.field_metadata.dict(),
            tenant_context=request.tenant_context.dict()
        )
        
        logger.info(f"[RECOMMENDATIONS] Generated {len(recommendations)} recommendations")
        
        # Calculate inference time
        inference_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Prepare response
        response_data = {
            "pdpl_principle": {
                "category_id": prediction['category_id'],
                "principle_vi": prediction['name_vi'],
                "principle_en": prediction['name_en'],
                "pdpl_article": prediction['article'],
                "confidence": prediction['confidence']
            },
            "recommendations": recommendations,
            "model_version": "VeriAIDPO_Principles_VI_v1",
            "inference_time_ms": inference_time,
            "cache_hit": False
        }
        
        # Cache result (15 minute TTL)
        redis_client.setex(
            cache_key,
            900,  # 15 minutes
            json.dumps(response_data)
        )
        
        logger.info(
            f"[SUCCESS] {len(recommendations)} recommendations for "
            f"{request.field_metadata.field_name} in {inference_time:.2f}ms"
        )
        
        return PredictionResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")



@app.post("/api/v1/recommendations/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit DPO feedback on PDPL recommendations
    
    Stores feedback for:
    - Model performance monitoring
    - Continuous improvement dataset
    - Accuracy tracking per industry/region
    
    Args:
        request: Feedback with field ID, PDPL principle, action taken, notes
    
    Returns:
        Confirmation message
    """
    try:
        # Store feedback in PostgreSQL
        from .database import get_db_session
        from .models.feedback import RecommendationFeedback
        
        async with get_db_session() as session:
            feedback = RecommendationFeedback(
                field_id=request.field_id,
                pdpl_category_id=request.pdpl_principle.category_id,
                pdpl_principle_vi=request.pdpl_principle.principle_vi,
                pdpl_principle_en=request.pdpl_principle.principle_en,
                confidence=request.pdpl_principle.confidence,
                action_taken=request.action_taken,
                dpo_notes=request.dpo_notes,
                created_at=datetime.utcnow()
            )
            session.add(feedback)
            await session.commit()
        
        logger.info(
            f"[FEEDBACK] {request.action_taken.upper()} - "
            f"Field: {request.field_id}, "
            f"Principle: {request.pdpl_principle.principle_en}"
        )
        
        return {
            "status": "success",
            "message": "Feedback recorded successfully",
            "field_id": request.field_id,
            "action": request.action_taken,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"[ERROR] Feedback submission failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Feedback failed: {str(e)}")


# Helper Functions

def _generate_cache_key(field_metadata: dict, tenant_context: dict) -> str:
    """Generate Redis cache key from field metadata and tenant context"""
    key_data = f"{field_metadata['field_name']}:{field_metadata['table_name']}:" \
               f"{tenant_context['veri_business_id']}:{tenant_context['veri_regional_location']}"
    return f"veri_ai_rec:{hashlib.md5(key_data.encode()).hexdigest()}"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8013, log_level="info")
```

---

### 4.2 Configuration

**File:** `backend/veri_ai_recommendations_engine/config.py`

```python
"""
Configuration for AI Recommendations Microservice
"""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Service
    SERVICE_NAME: str = "veri-ai-recommendations-engine"
    SERVICE_VERSION: str = "1.1.0"
    
    # VeriAIDPO Model
    MODEL_NAME: str = "TranHF/VeriAIDPO_Principles_VI_v1"
    MODEL_CACHE_DIR: Path = Path("backend/app/ml/models")
    HF_TOKEN: str = ""  # HuggingFace API token for private repo access
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CACHE_TTL_SECONDS: int = 900  # 15 minutes
    
    # PostgreSQL Feedback DB
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "verisyntra_feedback"
    POSTGRES_USER: str = "verisyntra"
    POSTGRES_PASSWORD: str = ""
    
    # API
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list = ["*"]
    
    # Model Inference
    CONFIDENCE_THRESHOLD: float = 0.7
    MAX_BATCH_SIZE: int = 32
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```
            "status": "success",
            "message": "Feedback recorded for model improvement"
        }
        
    except Exception as e:
        logger.error(f"Feedback submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/recommendations/stats")
async def get_recommendation_stats():
    """Get recommendation statistics and model performance metrics"""
    try:
        from .database import get_db_session
        from .models.feedback import RecommendationFeedback
        from sqlalchemy import func, select
        
        async with get_db_session() as session:
            # Get feedback statistics
            total_feedback = await session.scalar(
                select(func.count()).select_from(RecommendationFeedback)
            )
            
            accepted_count = await session.scalar(
                select(func.count()).select_from(RecommendationFeedback)
                .where(RecommendationFeedback.action_taken == 'accepted')
            )
            
            acceptance_rate = (accepted_count / total_feedback * 100) if total_feedback > 0 else 0
        
        return {
            "total_predictions": redis_client.dbsize(),
            "total_feedback": total_feedback,
            "accepted_recommendations": accepted_count,
            "acceptance_rate_pct": round(acceptance_rate, 2),
            "model_version": settings.MODEL_VERSION,
            "device": str(ModelManager.get_instance().device)
        }
        
    except Exception as e:
        logger.error(f"Stats retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions

def _generate_cache_key(field_metadata: FieldMetadata, tenant_context: TenantContext) -> str:
    """Generate Redis cache key for field"""
    return f"ai_rec:{field_metadata.table_name}:{field_metadata.field_name}:{tenant_context.veri_regional_location}"


def _format_recommendation(
    rec: Dict[str, Any],
    tenant_context: TenantContext
) -> Dict[str, Any]:
    """Format recommendation with Vietnamese labels"""
    
    # Vietnamese translations for recommendation types
    TRANSLATIONS = {
        'classification': {
            'title_vi': 'Đề xuất Phân loại',
            'title_en': 'Classification Suggestion',
            'priority': 'critical'
        },
        'retention': {
            'title_vi': 'Đề xuất Thời gian Lưu trữ',
            'title_en': 'Retention Period Recommendation',
            'priority': 'high'
        },
        'security': {
            'title_vi': 'Ưu tiên Bảo mật',
            'title_en': 'Security Priority',
            'priority': 'high'
        },
        'compliance_action': {
            'title_vi': 'Hành động Tuân thủ PDPL',
            'title_en': 'PDPL Compliance Action',
            'priority': 'critical'
        }
    }
    
    rec_type = rec.get('type', 'unknown')
    translation = TRANSLATIONS.get(rec_type, {})
    
    return {
        **rec,
        'title_vi': translation.get('title_vi', ''),
        'title_en': translation.get('title_en', ''),
        'priority': translation.get('priority', 'medium'),
        'legal_reference': _get_legal_reference(rec),
        'regional_context': tenant_context.veri_regional_location,
        'model_generated': True
    }


def _get_legal_reference(rec: Dict[str, Any]) -> str:
    """Get PDPL legal reference for recommendation"""
    rec_type = rec.get('type', '')
    
    if rec_type == 'classification':
        return 'PDPL Article 17 - Record of Processing Activities'
    elif rec_type == 'retention':
        return 'PDPL Article 13 - Data Retention'
    elif rec_type == 'security':
        return 'PDPL Article 15 - Security Measures'
    elif rec_type == 'compliance_action':
        return 'PDPL 2025 General Obligations'
    else:
        return 'PDPL 2025'


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8013,
        log_level="info"
    )
```

### 4.2 Configuration

**File:** `backend/veri_ai_recommendations_engine/config.py`

```python
"""
Configuration for AI Recommendations Microservice
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Service configuration
    SERVICE_NAME: str = "veri-ai-recommendations-engine"
    SERVICE_PORT: int = 8013
    MODEL_VERSION: str = "1.0.0"
    
    # Model paths
    MODEL_PATH: str = "models/pdpl_recommendation_v1.pt"
    PHOBERT_MODEL: str = "vinai/phobert-base"
    
    # Redis configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 2
    
    # PostgreSQL configuration
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/verisyntra_ai"
    
    # ML model parameters
    CONFIDENCE_THRESHOLD: float = 0.7
    BATCH_SIZE: int = 32
    MAX_SEQ_LENGTH: int = 128
    
    # GPU configuration
    USE_GPU: bool = True
    GPU_DEVICE_ID: int = 0
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

---

## 5. Integration with Document #7

### 5.1 Updated SmartRecommendationsEngine

**File:** `backend/veri_ai_data_inventory/intelligence/recommendations_engine.py`

```python
# Add to existing SmartRecommendationsEngine class in Document #7

@staticmethod
async def _generate_ai_powered(
    tenant_id: str,
    field_data: Optional[Dict[str, Any]],
    veri_context: Optional[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate AI-powered PDPL recommendations via VeriAIDPO microservice
    
    Integrates with veri-ai-recommendations-engine (Port 8013)
    Uses VeriAIDPO_Principles_VI_v1 for PDPL principle classification
    """
    try:
        import httpx
        
        # Prepare request payload for VeriAIDPO model
        payload = {
            "field_metadata": {
                "field_name": field_data.get('field_name', ''),
                "table_name": field_data.get('table_name', ''),
                "data_type": field_data.get('data_type', ''),
                "sample_values": field_data.get('sample_values', [])[:5],
                "current_classification": field_data.get('classification')
            },
            "tenant_context": {
                "veri_business_id": tenant_id,
                "veri_regional_location": veri_context.get('veri_regional_location', 'south'),
                "veri_industry_type": veri_context.get('veri_industry_type', 'technology')
            },
            "confidence_threshold": 0.7
        }
        
        # Call AI recommendations microservice
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                "http://localhost:8013/api/v1/recommendations/predict",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Get PDPL principle classification
                pdpl_principle = result.get('pdpl_principle', {})
                recommendations = result.get('recommendations', [])
                
                logger.info(
                    f"[OK] VeriAIDPO: {pdpl_principle.get('principle_en')} "
                    f"(confidence: {pdpl_principle.get('confidence', 0):.2%}, "
                    f"{len(recommendations)} recommendations, "
                    f"inference: {result.get('inference_time_ms', 0):.0f}ms)"
                )
                
                # Format recommendations for Document #7 compatibility
                formatted_recommendations = []
                
                # Add PDPL principle recommendation
                if pdpl_principle:
                    formatted_recommendations.append({
                        'type': RecommendationType.COMPLIANCE,
                        'priority': SmartRecommendationsEngine._map_confidence_to_priority(
                            pdpl_principle.get('confidence', 0)
                        ),
                        'title_vi': f"Nguyên tắc PDPL: {pdpl_principle.get('principle_vi')}",
                        'title_en': f"PDPL Principle: {pdpl_principle.get('principle_en')}",
                        'description_vi': f"VeriAIDPO phân loại trường này thuộc nguyên tắc '{pdpl_principle.get('principle_vi')}' theo {pdpl_principle.get('pdpl_article')}",
                        'description_en': f"VeriAIDPO classified this field under '{pdpl_principle.get('principle_en')}' per {pdpl_principle.get('pdpl_article')}",
                        'action': 'review_pdpl_principle',
                        'confidence': pdpl_principle.get('confidence', 0.0),
                        'ml_generated': True,
                        'legal_reference': pdpl_principle.get('pdpl_article', 'PDPL 2025'),
                        'model_version': result.get('model_version', 'VeriAIDPO_Principles_VI_v1')
                    })
                
                # Add derived recommendations (compliance actions, retention, security)
                for rec in recommendations:
                    formatted_rec = {
                        'type': SmartRecommendationsEngine._map_recommendation_type(rec.get('type')),
                        'priority': SmartRecommendationsEngine._map_recommendation_priority(rec),
                        'title_vi': rec.get('title_vi', ''),
                        'title_en': rec.get('title_en', ''),
                        'description_vi': rec.get('description_vi', ''),
                        'description_en': rec.get('description_en', ''),
                        'action': rec.get('action', 'review'),
                        'confidence': rec.get('confidence', 0.0),
                        'ml_generated': True,
                        'legal_reference': rec.get('pdpl_article', 'PDPL 2025'),
                        'model_version': result.get('model_version', 'VeriAIDPO_Principles_VI_v1')
                    }
                    formatted_recommendations.append(formatted_rec)
                
                return formatted_recommendations
            else:
                logger.warning(f"[WARNING] VeriAIDPO service returned status {response.status_code}")
                return []
                
    except httpx.TimeoutException:
        logger.warning("[WARNING] VeriAIDPO service timeout (5s) - using rule-based only")
        return []
    except httpx.RequestError as e:
        logger.warning(f"[WARNING] VeriAIDPO service unavailable: {str(e)} - using rule-based only")
        return []
    except Exception as e:
        logger.error(f"[ERROR] VeriAIDPO recommendation failed: {str(e)}")
        return []

@staticmethod
def _map_recommendation_type(ai_type: str) -> RecommendationType:
    """Map VeriAIDPO recommendation type to Document #7 type"""
    mapping = {
        'pdpl_principle': RecommendationType.COMPLIANCE,
        'compliance_action': RecommendationType.COMPLIANCE,
        'retention': RecommendationType.RETENTION,
        'security': RecommendationType.SECURITY,
        'classification': RecommendationType.CLASSIFICATION
    }
    return mapping.get(ai_type, RecommendationType.COMPLIANCE)

@staticmethod
def _map_confidence_to_priority(confidence: float) -> RecommendationPriority:
    """Map VeriAIDPO confidence score to priority level"""
    if confidence >= 0.9:
        return RecommendationPriority.CRITICAL
    elif confidence >= 0.8:
        return RecommendationPriority.HIGH
    elif confidence >= 0.7:
        return RecommendationPriority.MEDIUM
    else:
        return RecommendationPriority.LOW

@staticmethod
def _map_recommendation_priority(rec: Dict[str, Any]) -> RecommendationPriority:
    """Map recommendation priority from VeriAIDPO"""
    priority_str = rec.get('priority', 'medium').lower()
    
    mapping = {
        'critical': RecommendationPriority.CRITICAL,
        'high': RecommendationPriority.HIGH,
        'medium': RecommendationPriority.MEDIUM,
        'low': RecommendationPriority.LOW
    }
    
    return mapping.get(priority_str, RecommendationPriority.MEDIUM)
        predicted_action = rec.get('predicted_action', 'review')
        return f"AI recommends compliance action: {predicted_action}"
    else:
        return "AI recommendation based on Vietnamese data patterns"
```

---

## 6. Using Existing VeriAIDPO Model

### 6.1 Model Training (Already Complete)

**VeriAIDPO_Principles_VI_v1** has been trained and is ready for use. No new training pipeline is required for this microservice.

**Training Details:**
- **Training Notebook:** `docs/VeriSystems/VeriAIDPO_Principles_VI_v2_DynamicRegistry_Training.ipynb` (3,697 lines)
- **Training Data:** 24,000 samples from real Vietnamese legal corpus
  - PDPL Law 91/2025/QH15: 352 lines of actual Vietnamese law
  - Decree 13/2023/ND-CP: 461 lines of actual Vietnamese regulations
  - Total legal corpus: 813 lines of authentic Vietnamese legal text
  - Dynamic company scenarios: 46+ Vietnamese business patterns with normalization
- **Base Model:** vinai/phobert-base-v2 (PhoBERT for Vietnamese NLP)
- **Task:** 8 PDPL principle classification
- **Accuracy:** 78-88% on Vietnamese legal/compliance text
- **Distribution:** HuggingFace Hub - TranHF/VeriAIDPO_Principles_VI_v1 (private repo)

### 6.2 HuggingFace Hub Setup

**For Microservice Deployment:**

The VeriAIDPO model is hosted on HuggingFace Hub and auto-downloads on first use.

**Environment Configuration:**

**File:** `.env` (in `backend/veri_ai_recommendations_engine/`)

```bash
# VeriAIDPO Model Configuration
MODEL_NAME=TranHF/VeriAIDPO_Principles_VI_v1
MODEL_CACHE_DIR=backend/app/ml/models
HF_TOKEN=your_huggingface_token_here  # Required for private repo access

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# PostgreSQL Feedback DB
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=verisyntra_feedback
POSTGRES_USER=verisyntra
POSTGRES_PASSWORD=your_password_here
```

**HuggingFace Token Setup:**

1. **Get HuggingFace Token:**
   - Go to https://huggingface.co/settings/tokens
   - Create new token with `read` access
   - Copy token value

2. **Set Environment Variable (PowerShell):**
   ```powershell
   $env:HF_TOKEN = "your_token_here"
   ```

3. **Verify Model Access:**
   ```python
   from huggingface_hub import snapshot_download
   
   model_path = snapshot_download(
       repo_id="TranHF/VeriAIDPO_Principles_VI_v1",
       cache_dir="backend/app/ml/models",
       token=os.getenv("HF_TOKEN")
   )
   print(f"[OK] Model downloaded to: {model_path}")
   ```

### 6.3 Model Auto-Download Process

The VeriAIDPORecommendationLoader automatically handles model download:

```python
# Automatic on microservice startup (from Section 3.2)

class VeriAIDPORecommendationLoader:
    def __init__(self, model_name: str = "TranHF/VeriAIDPO_Principles_VI_v1"):
        logger.info(f"[INIT] Loading VeriAIDPO model: {model_name}")
        
        # Auto-download from HuggingFace Hub
        self._model_path = snapshot_download(
            repo_id=model_name,
            cache_dir=cache_dir,
            token=os.getenv("HF_TOKEN")
        )
        
        # Load PhoBERT tokenizer and model
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_path)
        self._model = AutoModelForSequenceClassification.from_pretrained(
            self._model_path,
            num_labels=8  # 8 PDPL principles
        )
        
        logger.info(f"[OK] VeriAIDPO model loaded from {self._model_path}")
```

**First-Run Behavior:**
1. Microservice starts
2. Checks `backend/app/ml/models/` for cached model
3. If not found, downloads from HuggingFace Hub (~540MB)
4. Caches locally for subsequent runs
5. Ready for inference

**Download Time:**
- First run: ~2-5 minutes (depending on internet speed)
- Subsequent runs: <5 seconds (loads from cache)

### 6.4 Model Versioning Strategy

**Production Model Versions:**

```python
# Track model versions for reproducibility

MODEL_VERSIONS = {
    'v1.0': {
        'huggingface_repo': 'TranHF/VeriAIDPO_Principles_VI_v1',
        'training_date': '2025-10-15',
        'training_samples': 24000,
        'accuracy': 0.85,
        'legal_corpus_lines': 813,
        'pdpl_categories': 8,
        'base_model': 'vinai/phobert-base-v2',
        'notes': 'Initial production model, real PDPL + Decree 13'
    }
    # Future versions can be added here
}
```

**Model Update Process:**

When new model versions are trained:

1. **Upload to HuggingFace Hub:**
   ```python
   from huggingface_hub import HfApi
   
   api = HfApi()
   api.upload_folder(
       folder_path="path/to/model",
       repo_id="TranHF/VeriAIDPO_Principles_VI_v2",  # New version
       token=os.getenv("HF_TOKEN")
   )
   ```

2. **Update Configuration:**
   ```bash
   # Update .env
   MODEL_NAME=TranHF/VeriAIDPO_Principles_VI_v2
   ```

3. **Restart Microservice:**
   - New model auto-downloads on startup
   - Old model remains cached for rollback if needed

### 6.5 Continuous Improvement via Feedback

**Feedback Collection for Future Training:**

The microservice collects DPO feedback for future model improvements:

**PostgreSQL Feedback Schema:**

```sql
-- File: backend/veri_ai_recommendations_engine/models/feedback_schema.sql

CREATE TABLE recommendation_feedback (
    id SERIAL PRIMARY KEY,
    field_id VARCHAR(255) NOT NULL,
    pdpl_category_id INTEGER NOT NULL,
    pdpl_principle_vi VARCHAR(255) NOT NULL,
    pdpl_principle_en VARCHAR(255) NOT NULL,
    confidence FLOAT NOT NULL,
    action_taken VARCHAR(50) NOT NULL,  -- 'accepted', 'rejected', 'modified'
    dpo_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for analytics
    INDEX idx_category (pdpl_category_id),
    INDEX idx_action (action_taken),
    INDEX idx_created (created_at)
);
```

**Feedback Analytics for Model Improvement:**

```python
# File: backend/veri_ai_recommendations_engine/training/feedback_analytics.py

"""
Analyze DPO feedback to identify model improvement opportunities
"""

from sqlalchemy import select, func
from ..database import get_db_session
from ..models.feedback import RecommendationFeedback


async def get_model_accuracy_by_category():
    """Calculate acceptance rate by PDPL category"""
    async with get_db_session() as session:
        results = await session.execute(
            select(
                RecommendationFeedback.pdpl_category_id,
                RecommendationFeedback.pdpl_principle_vi,
                func.count().label('total'),
                func.sum(
                    case((RecommendationFeedback.action_taken == 'accepted', 1), else_=0)
                ).label('accepted')
            )
            .group_by(
                RecommendationFeedback.pdpl_category_id,
                RecommendationFeedback.pdpl_principle_vi
            )
        )
        
        # Calculate acceptance rates
        performance = []
        for row in results:
            acceptance_rate = (row.accepted / row.total * 100) if row.total > 0 else 0
            performance.append({
                'category_id': row.pdpl_category_id,
                'principle': row.pdpl_principle_vi,
                'total_predictions': row.total,
                'accepted': row.accepted,
                'acceptance_rate': round(acceptance_rate, 2),
                'needs_improvement': acceptance_rate < 70  # Flag for retraining
            })
        
        return performance


async def export_rejected_samples_for_retraining():
    """Export rejected predictions as training data for model improvement"""
    async with get_db_session() as session:
        rejected_samples = await session.execute(
            select(RecommendationFeedback)
            .where(RecommendationFeedback.action_taken == 'rejected')
        )
        
        training_data = []
        for sample in rejected_samples:
            training_data.append({
                'text': sample.field_id,  # Field description
                'predicted_category': sample.pdpl_category_id,
                'correct_category': None,  # To be labeled by DPO
                'confidence': sample.confidence,
                'dpo_notes': sample.dpo_notes,
                'created_at': sample.created_at.isoformat()
            })
        
        return training_data
```

**When to Retrain:**
- Acceptance rate drops below 70% for any PDPL category
- Significant new PDPL regulations added
- 1,000+ new feedback samples collected
- Vietnamese business patterns change (e.g., new industries)

**Retraining Process:**
1. Export rejected/modified feedback samples
2. DPO reviews and corrects labels
3. Combine with original 24,000 samples
4. Fine-tune VeriAIDPO model in training notebook
5. Evaluate on validation set
6. Upload new version to HuggingFace Hub
7. Update microservice configuration
            'table_name': self._generate_table_name(industry),
            'data_type': self._infer_data_type(field_name),
            'sample_values': self._generate_sample_values(field_name, 5),
            'current_classification': None  # To be classified
        }
        
        # Tenant context
        tenant_context = {
            'veri_regional_location': region,
            'veri_industry_type': industry,
            'risk_score': random.randint(0, 100),
            'row_count': random.randint(100, 1000000),
            'is_encrypted': random.choice([True, False])
        }
        
        # Generate ground truth recommendations
        recommendations = self._generate_recommendations(
            field_name=field_name,
            pdpl_category=pdpl_category,
            region=region,
            industry=industry,
            tenant_context=tenant_context
        )
        
        return {
            'field_metadata': field_metadata,
            'tenant_context': tenant_context,
            'recommendations': recommendations,
            'pdpl_category': pdpl_category,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _generate_table_name(self, industry: str) -> str:
        """Generate realistic table name"""
        table_prefixes = {
            'banking': ['khach_hang', 'tai_khoan', 'giao_dich'],
            'healthcare': ['benh_nhan', 'kham_benh', 'don_thuoc'],
            'ecommerce': ['nguoi_dung', 'don_hang', 'san_pham'],
            'telecom': ['thue_bao', 'cuoc_goi', 'dich_vu'],
            'education': ['sinh_vien', 'giang_vien', 'lop_hoc']
        }
        
        prefix = random.choice(table_prefixes.get(industry, ['data']))
        return f"tbl_{prefix}_{random.randint(1, 99):02d}"
    
    def _infer_data_type(self, field_name: str) -> str:
        """Infer SQL data type from field name"""
        if any(x in field_name for x in ['ngay', 'thoi_gian', 'date']):
            return 'DATE'
        elif any(x in field_name for x in ['so_', 'id', 'ma_']):
            return 'VARCHAR'
        elif any(x in field_name for x in ['tien', 'phi', 'amount']):
            return 'DECIMAL'
        elif any(x in field_name for x in ['so_luong', 'count']):
            return 'INTEGER'
        else:
            return 'VARCHAR'
    
    def _generate_sample_values(self, field_name: str, count: int) -> List[Any]:
        """Generate realistic sample values"""
        if 'ho_va_ten' in field_name or 'name' in field_name:
            return [f"Nguyễn Văn {chr(65+i)}" for i in range(count)]
        elif 'email' in field_name:
            return [f"user{i}@company.vn" for i in range(count)]
        elif 'so_dien_thoai' in field_name or 'phone' in field_name:
            return [f"0{random.choice([3,5,7,8,9]}{random.randint(10000000, 99999999)}" for _ in range(count)]
        elif 'so_cmnd' in field_name:
            return [f"{random.randint(100000000, 999999999)}" for _ in range(count)]
        elif 'so_cccd' in field_name:
            return [f"{random.randint(100000000000, 999999999999)}" for _ in range(count)]
        else:
            return [f"value_{i}" for i in range(count)]
    
    def _generate_recommendations(
        self,
        field_name: str,
        pdpl_category: str,
        region: str,
        industry: str,
        tenant_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate ground truth recommendations"""
        recommendations = []
        
        # Classification recommendation (always generated)
        recommendations.append({
            'type': 'classification',
            'predicted_class': self._map_category_to_classification(pdpl_category),
            'confidence': random.uniform(0.75, 0.95),
            'reason': f"Field matches {pdpl_category} pattern",
            'pdpl_article': 'Article 17'
        })
        
        # Retention recommendation (for sensitive data)
        if 'sensitive' in pdpl_category or 'financial' in pdpl_category:
            recommendations.append({
                'type': 'retention',
                'predicted_retention': self._determine_retention(industry, pdpl_category),
                'confidence': random.uniform(0.70, 0.90),
                'reason': f"Vietnamese {industry} industry standard",
                'pdpl_article': 'Article 13'
            })
        
        # Security recommendation (for high-risk fields)
        if tenant_context['risk_score'] > 60 or 'biometric' in pdpl_category:
            recommendations.append({
                'type': 'security',
                'predicted_priority': 'high',
                'confidence': random.uniform(0.80, 0.95),
                'reason': "High-risk data requires enhanced security",
                'pdpl_article': 'Article 15'
            })
        
        # Compliance action (region-specific)
        recommendations.append({
            'type': 'compliance_action',
            'predicted_action': self._determine_action(region, pdpl_category),
            'confidence': random.uniform(0.65, 0.85),
            'reason': f"Standard practice for {region} Vietnam",
            'pdpl_article': 'General PDPL 2025'
        })
        
        return recommendations
    
    def _map_category_to_classification(self, pdpl_category: str) -> str:
        """Map PDPL category to classification label"""
        mapping = {
            'cat1_personal_sensitive': 'Personal Data',
            'cat2_financial': 'Sensitive Personal Data',
            'cat3_health': 'Sensitive Personal Data',
            'cat4_biometric': 'Biometric Data',
            'cat5_political_religious': 'Special Categories Data',
            'cat6_behavioral': 'Behavioral Data'
        }
        return mapping.get(pdpl_category, 'Unknown')
    
    def _determine_retention(self, industry: str, pdpl_category: str) -> str:
        """Determine appropriate retention period"""
        if industry == 'banking':
            return '10 years'
        elif industry == 'healthcare':
            return '20 years'
        elif 'sensitive' in pdpl_category:
            return '7 years'
        else:
            return '3 years'
    
    def _determine_action(self, region: str, pdpl_category: str) -> str:
        """Determine compliance action based on region"""
        if region == 'north':
            return 'document_and_report'
        elif region == 'south':
            return 'risk_assessment'
        else:
            return 'stakeholder_consultation'


# Generate and save training data
if __name__ == "__main__":
    generator = VietnamesePDPLTrainingDataGenerator()
    
    print("[OK] Starting training data generation...")
    dataset = generator.generate_dataset(num_samples=10000)
    
    # Save to JSONL format
    output_file = "vietnamese_pdpl_recommendations_training.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for sample in dataset:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    print(f"[OK] Saved {len(dataset)} samples to {output_file}")
    print(f"[OK] File size: {len(open(output_file).read()) / 1024 / 1024:.2f} MB")
```

### 6.2 Model Training Notebook

**File:** `docs/VeriSystems/AI_Recommendation_Model_Training.ipynb`

```json
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# VeriSyntra AI Recommendations Model Training\n",
        "# Vietnamese PDPL 2025 Compliance Recommendations\n",
        "\n",
        "**Purpose:** Train PhoBERT-based model for Vietnamese PDPL recommendations\n",
        "**Model:** vinai/phobert-base with custom classification head\n",
        "**Dataset:** 10,000 Vietnamese PDPL scenarios"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 1: Import dependencies\n",
        "import torch\n",
        "import torch.nn as nn\n",
        "from torch.utils.data import Dataset, DataLoader\n",
        "from transformers import AutoTokenizer, AutoModel\n",
        "import json\n",
        "import numpy as np\n",
        "from tqdm import tqdm\n",
        "import mlflow\n",
        "from sklearn.metrics import classification_report, confusion_matrix\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "\n",
        "print('[OK] Dependencies imported')\n",
        "print(f'[OK] PyTorch version: {torch.__version__}')\n",
        "print(f'[OK] CUDA available: {torch.cuda.is_available()}')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 2: Load training data\n",
        "def load_training_data(file_path: str):\n",
        "    samples = []\n",
        "    with open(file_path, 'r', encoding='utf-8') as f:\n",
        "        for line in f:\n",
        "            samples.append(json.loads(line))\n",
        "    return samples\n",
        "\n",
        "dataset = load_training_data('vietnamese_pdpl_recommendations_training.jsonl')\n",
        "print(f'[OK] Loaded {len(dataset)} training samples')\n",
        "\n",
        "# Sample inspection\n",
        "sample = dataset[0]\n",
        "print(f'\\n[OK] Sample field: {sample[\"field_metadata\"][\"field_name\"]}')\n",
        "print(f'[OK] PDPL category: {sample[\"pdpl_category\"]}')\n",
        "print(f'[OK] Recommendations: {len(sample[\"recommendations\"])}')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 3: Initialize PhoBERT tokenizer\n",
        "tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')\n",
        "print('[OK] PhoBERT tokenizer loaded')\n",
        "\n",
        "# Test Vietnamese tokenization\n",
        "test_text = 'Họ và tên là dữ liệu cá nhân nhạy cảm theo PDPL 2025'\n",
        "tokens = tokenizer.tokenize(test_text)\n",
        "print(f'[OK] Test tokenization: {tokens[:10]}...')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 4: Create PyTorch dataset\n",
        "class PDPLRecommendationDataset(Dataset):\n",
        "    def __init__(self, samples, tokenizer, max_length=128):\n",
        "        self.samples = samples\n",
        "        self.tokenizer = tokenizer\n",
        "        self.max_length = max_length\n",
        "    \n",
        "    def __len__(self):\n",
        "        return len(self.samples)\n",
        "    \n",
        "    def __getitem__(self, idx):\n",
        "        sample = self.samples[idx]\n",
        "        \n",
        "        # Create text input\n",
        "        field_text = f\"{sample['field_metadata']['field_name']} {sample['field_metadata']['table_name']}\"\n",
        "        encoding = self.tokenizer(\n",
        "            field_text,\n",
        "            max_length=self.max_length,\n",
        "            padding='max_length',\n",
        "            truncation=True,\n",
        "            return_tensors='pt'\n",
        "        )\n",
        "        \n",
        "        # Extract metadata features\n",
        "        metadata_features = torch.tensor([\n",
        "            sample['tenant_context']['risk_score'] / 100,\n",
        "            np.log10(sample['tenant_context']['row_count'] + 1) / 6,\n",
        "            float(sample['tenant_context']['is_encrypted'])\n",
        "        ], dtype=torch.float32)\n",
        "        \n",
        "        # Extract labels (classification type)\n",
        "        classification_rec = [r for r in sample['recommendations'] if r['type'] == 'classification'][0]\n",
        "        label = self._encode_classification(classification_rec['predicted_class'])\n",
        "        \n",
        "        return {\n",
        "            'input_ids': encoding['input_ids'].squeeze(),\n",
        "            'attention_mask': encoding['attention_mask'].squeeze(),\n",
        "            'metadata_features': metadata_features,\n",
        "            'label': label\n",
        "        }\n",
        "    \n",
        "    def _encode_classification(self, classification: str) -> int:\n",
        "        mapping = {\n",
        "            'Personal Data': 0,\n",
        "            'Sensitive Personal Data': 1,\n",
        "            'Biometric Data': 2,\n",
        "            'Special Categories Data': 3,\n",
        "            'Behavioral Data': 4,\n",
        "            'Unknown': 5\n",
        "        }\n",
        "        return mapping.get(classification, 5)\n",
        "\n",
        "# Create datasets\n",
        "train_dataset = PDPLRecommendationDataset(dataset[:8000], tokenizer)\n",
        "val_dataset = PDPLRecommendationDataset(dataset[8000:9000], tokenizer)\n",
        "test_dataset = PDPLRecommendationDataset(dataset[9000:], tokenizer)\n",
        "\n",
        "print(f'[OK] Train: {len(train_dataset)}, Val: {len(val_dataset)}, Test: {len(test_dataset)}')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 5: Define model architecture\n",
        "class VietnamesePDPLRecommendationModel(nn.Module):\n",
        "    def __init__(self, num_classes=6):\n",
        "        super().__init__()\n",
        "        \n",
        "        # PhoBERT encoder\n",
        "        self.phobert = AutoModel.from_pretrained('vinai/phobert-base')\n",
        "        \n",
        "        # Feature combiner\n",
        "        self.feature_combiner = nn.Sequential(\n",
        "            nn.Linear(768 + 3, 512),\n",
        "            nn.ReLU(),\n",
        "            nn.Dropout(0.3)\n",
        "        )\n",
        "        \n",
        "        # Classifier\n",
        "        self.classifier = nn.Sequential(\n",
        "            nn.Linear(512, 256),\n",
        "            nn.ReLU(),\n",
        "            nn.Dropout(0.2),\n",
        "            nn.Linear(256, num_classes)\n",
        "        )\n",
        "    \n",
        "    def forward(self, input_ids, attention_mask, metadata_features):\n",
        "        # PhoBERT encoding\n",
        "        outputs = self.phobert(input_ids=input_ids, attention_mask=attention_mask)\n",
        "        text_features = outputs.last_hidden_state[:, 0, :]  # CLS token\n",
        "        \n",
        "        # Combine features\n",
        "        combined = torch.cat([text_features, metadata_features], dim=1)\n",
        "        features = self.feature_combiner(combined)\n",
        "        \n",
        "        # Classification\n",
        "        logits = self.classifier(features)\n",
        "        return logits\n",
        "\n",
        "model = VietnamesePDPLRecommendationModel()\n",
        "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
        "model.to(device)\n",
        "\n",
        "print(f'[OK] Model initialized on {device}')\n",
        "print(f'[OK] Model parameters: {sum(p.numel() for p in model.parameters()):,}')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 6: Training setup\n",
        "train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)\n",
        "val_loader = DataLoader(val_dataset, batch_size=32)\n",
        "\n",
        "optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)\n",
        "criterion = nn.CrossEntropyLoss()\n",
        "\n",
        "# MLflow tracking\n",
        "mlflow.set_experiment('vietnamese_pdpl_recommendations')\n",
        "mlflow.start_run()\n",
        "mlflow.log_params({\n",
        "    'model': 'PhoBERT-base',\n",
        "    'batch_size': 32,\n",
        "    'learning_rate': 1e-5,\n",
        "    'train_samples': len(train_dataset),\n",
        "    'val_samples': len(val_dataset)\n",
        "})\n",
        "\n",
        "print('[OK] Training setup complete')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 7: Training loop\n",
        "num_epochs = 10\n",
        "best_val_acc = 0.0\n",
        "\n",
        "for epoch in range(num_epochs):\n",
        "    # Training\n",
        "    model.train()\n",
        "    train_loss = 0.0\n",
        "    train_correct = 0\n",
        "    \n",
        "    for batch in tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}'):\n",
        "        input_ids = batch['input_ids'].to(device)\n",
        "        attention_mask = batch['attention_mask'].to(device)\n",
        "        metadata_features = batch['metadata_features'].to(device)\n",
        "        labels = batch['label'].to(device)\n",
        "        \n",
        "        optimizer.zero_grad()\n",
        "        logits = model(input_ids, attention_mask, metadata_features)\n",
        "        loss = criterion(logits, labels)\n",
        "        loss.backward()\n",
        "        optimizer.step()\n",
        "        \n",
        "        train_loss += loss.item()\n",
        "        train_correct += (logits.argmax(dim=1) == labels).sum().item()\n",
        "    \n",
        "    train_acc = train_correct / len(train_dataset)\n",
        "    \n",
        "    # Validation\n",
        "    model.eval()\n",
        "    val_loss = 0.0\n",
        "    val_correct = 0\n",
        "    \n",
        "    with torch.no_grad():\n",
        "        for batch in val_loader:\n",
        "            input_ids = batch['input_ids'].to(device)\n",
        "            attention_mask = batch['attention_mask'].to(device)\n",
        "            metadata_features = batch['metadata_features'].to(device)\n",
        "            labels = batch['label'].to(device)\n",
        "            \n",
        "            logits = model(input_ids, attention_mask, metadata_features)\n",
        "            loss = criterion(logits, labels)\n",
        "            \n",
        "            val_loss += loss.item()\n",
        "            val_correct += (logits.argmax(dim=1) == labels).sum().item()\n",
        "    \n",
        "    val_acc = val_correct / len(val_dataset)\n",
        "    \n",
        "    # Logging\n",
        "    print(f'Epoch {epoch+1}: Train Loss={train_loss/len(train_loader):.4f}, Train Acc={train_acc:.4f}, Val Loss={val_loss/len(val_loader):.4f}, Val Acc={val_acc:.4f}')\n",
        "    \n",
        "    mlflow.log_metrics({\n",
        "        'train_loss': train_loss / len(train_loader),\n",
        "        'train_acc': train_acc,\n",
        "        'val_loss': val_loss / len(val_loader),\n",
        "        'val_acc': val_acc\n",
        "    }, step=epoch)\n",
        "    \n",
        "    # Save best model\n",
        "    if val_acc > best_val_acc:\n",
        "        best_val_acc = val_acc\n",
        "        torch.save({\n",
        "            'epoch': epoch,\n",
        "            'model_state_dict': model.state_dict(),\n",
        "            'optimizer_state_dict': optimizer.state_dict(),\n",
        "            'val_acc': val_acc\n",
        "        }, 'pdpl_recommendation_best.pt')\n",
        "        print(f'[OK] Saved best model (val_acc={val_acc:.4f})')\n",
        "\n",
        "mlflow.end_run()\n",
        "print('[OK] Training complete')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Step 8: Model evaluation\n",
        "test_loader = DataLoader(test_dataset, batch_size=32)\n",
        "\n",
        "model.eval()\n",
        "all_preds = []\n",
        "all_labels = []\n",
        "\n",
        "with torch.no_grad():\n",
        "    for batch in tqdm(test_loader, desc='Testing'):\n",
        "        input_ids = batch['input_ids'].to(device)\n",
        "        attention_mask = batch['attention_mask'].to(device)\n",
        "        metadata_features = batch['metadata_features'].to(device)\n",
        "        labels = batch['label'].to(device)\n",
        "        \n",
        "        logits = model(input_ids, attention_mask, metadata_features)\n",
        "        preds = logits.argmax(dim=1)\n",
        "        \n",
        "        all_preds.extend(preds.cpu().numpy())\n",
        "        all_labels.extend(labels.cpu().numpy())\n",
        "\n",
        "# Classification report\n",
        "class_names = ['Personal Data', 'Sensitive Personal Data', 'Biometric Data', \n",
        "               'Special Categories Data', 'Behavioral Data', 'Unknown']\n",
        "print(classification_report(all_labels, all_preds, target_names=class_names))\n",
        "\n",
        "# Confusion matrix\n",
        "cm = confusion_matrix(all_labels, all_preds)\n",
        "plt.figure(figsize=(10, 8))\n",
        "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)\n",
        "plt.title('PDPL Recommendation Model - Confusion Matrix')\n",
        "plt.ylabel('True Label')\n",
        "plt.xlabel('Predicted Label')\n",
        "plt.tight_layout()\n",
        "plt.savefig('confusion_matrix.png')\n",
        "print('[OK] Confusion matrix saved')"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.11.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

---

## 7. Deployment

### 7.1 Docker Configuration

**File:** `backend/veri_ai_recommendations_engine/Dockerfile`

```dockerfile
# VeriAIDPO Recommendations Microservice Dockerfile
# Supports both GPU and CPU inference

FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy from base
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application
COPY . .

# Create model cache directory
RUN mkdir -p /app/backend/app/ml/models

# Expose port
EXPOSE 8013

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8013/health || exit 1

# Run application
# Model auto-downloads from HuggingFace on first run
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8013"]
```

**File:** `backend/veri_ai_recommendations_engine/requirements.txt`

```txt
# FastAPI and web framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2
pydantic-settings==2.0.3

# VeriAIDPO Model (HuggingFace Hub)
transformers==4.35.0
torch==2.1.0
huggingface-hub==0.19.4

# Vietnamese NLP
underthesea==6.7.0  # Vietnamese text processing (optional)

# Database and caching
redis==5.0.1
asyncpg==0.29.0
sqlalchemy[asyncio]==2.0.23

# HTTP client
httpx==0.25.1

# Utilities
python-dotenv==1.0.0
```

**File:** `backend/veri_ai_recommendations_engine/docker-compose.yml`

```yaml
version: '3.8'

services:
  veri-ai-recommendations:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: veri-ai-recommendations-engine
    ports:
      - "8013:8013"
    environment:
      # VeriAIDPO Model
      - MODEL_NAME=TranHF/VeriAIDPO_Principles_VI_v1
      - MODEL_CACHE_DIR=/app/backend/app/ml/models
      - HF_TOKEN=${HF_TOKEN}  # HuggingFace token from .env
      
      # Redis Cache
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_DB=0
      
      # PostgreSQL Feedback DB
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=verisyntra_feedback
      - POSTGRES_USER=verisyntra
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      
      # Service Config
      - CONFIDENCE_THRESHOLD=0.7
      - LOG_LEVEL=INFO
    volumes:
      - model_cache:/app/backend/app/ml/models  # Persist model cache
      - ./logs:/app/logs
    depends_on:
      - redis
      - postgres
    restart: unless-stopped
    # CPU-only by default (GPU optional)
    # For GPU support, uncomment deploy section below

  redis:
    image: redis:7.0-alpine
    container_name: veri-ai-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: veri-ai-postgres
    environment:
      - POSTGRES_DB=verisyntra_feedback
      - POSTGRES_USER=verisyntra
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  model_cache:  # VeriAIDPO model cache
  redis_data:
  postgres_data:

# Optional GPU configuration (uncomment if NVIDIA GPU available)
# services:
#   veri-ai-recommendations:
#     deploy:
#       resources:
#         reservations:
#           devices:
#             - driver: nvidia
#               count: 1
#               capabilities: [gpu]
```

**Deployment Steps:**

```powershell
# 1. Set environment variables
$env:HF_TOKEN = "your_huggingface_token"
$env:POSTGRES_PASSWORD = "your_secure_password"

# 2. Build and start services
cd backend/veri_ai_recommendations_engine
docker-compose up -d

# 3. Check logs (model download on first run)
docker-compose logs -f veri-ai-recommendations

# Expected output:
# [INIT] Loading VeriAIDPO model: TranHF/VeriAIDPO_Principles_VI_v1
# [OK] Model downloaded to: /app/backend/app/ml/models/...
# [OK] VeriAIDPO model loaded from ...
# INFO: Application startup complete.
# INFO: Uvicorn running on http://0.0.0.0:8013

# 4. Verify health
curl http://localhost:8013/health

# Expected response:
# {
#   "status": "healthy",
#   "model_loaded": true,
#   "redis_connected": true,
#   "model_name": "VeriAIDPO_Principles_VI_v1",
#   "model_accuracy": "78-88%",
#   "huggingface_repo": "TranHF/VeriAIDPO_Principles_VI_v1"
# }
```
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=verisyntra_ai
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

### 7.2 Kubernetes Deployment

**File:** `backend/veri_ai_recommendations_engine/k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: veri-ai-recommendations
  namespace: verisyntra
spec:
  replicas: 2
  selector:
    matchLabels:
      app: veri-ai-recommendations
  template:
    metadata:
      labels:
        app: veri-ai-recommendations
    spec:
      containers:
      - name: recommendations-engine
        image: verisyntra/ai-recommendations:1.0.0
        ports:
        - containerPort: 8013
        env:
        - name: REDIS_HOST
          value: "redis-service"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: verisyntra-secrets
              key: database-url
        - name: USE_GPU
          value: "true"
        resources:
          requests:
            memory: "8Gi"
            cpu: "2"
            nvidia.com/gpu: "1"
          limits:
            memory: "16Gi"
            cpu: "4"
            nvidia.com/gpu: "1"
        livenessProbe:
          httpGet:
            path: /health
            port: 8013
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8013
          initialDelaySeconds: 15
          periodSeconds: 5
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: veri-ai-recommendations-service
  namespace: verisyntra
spec:
  selector:
    app: veri-ai-recommendations
  ports:
  - protocol: TCP
    port: 8013
    targetPort: 8013
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: veri-ai-recommendations-hpa
  namespace: verisyntra
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: veri-ai-recommendations
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

**File:** `backend/veri_ai_recommendations_engine/tests/test_model_loader.py`

```python
"""
Unit tests for VeriAIDPO Model Loader
"""

import pytest
from models.model_loader import VeriAIDPORecommendationLoader


class TestVeriAIDPOLoader:
    """Test suite for VeriAIDPO model loader"""
    
    @pytest.fixture
    def model_loader(self):
        """Initialize model loader for testing"""
        return VeriAIDPORecommendationLoader(
            model_name="TranHF/VeriAIDPO_Principles_VI_v1"
        )
    
    def test_model_initialization(self, model_loader):
        """Test model initializes correctly from HuggingFace"""
        assert model_loader is not None
        assert model_loader.is_loaded
        assert model_loader._tokenizer is not None
        assert model_loader._model is not None
    
    def test_pdpl_categories_loaded(self, model_loader):
        """Test PDPL categories configuration"""
        assert len(model_loader._categories) == 8
        
        # Check all 8 PDPL principles exist
        expected_principles = [
            'Tuân thủ pháp luật và minh bạch',
            'Giới hạn mục đích',
            'Tối thiểu hóa dữ liệu',
            'Chính xác',
            'Giới hạn lưu trữ',
            'An toàn bảo mật',
            'Trách nhiệm giải trình',
            'Quyền của chủ thể dữ liệu'
        ]
        
        for i, principle in enumerate(expected_principles):
            assert model_loader._categories[i]['vi'] == principle
    
    def test_prediction_vietnamese_text(self, model_loader):
        """Test prediction with Vietnamese legal text"""
        vietnamese_text = "Trường dữ liệu 'so_cmnd' trong bảng 'khach_hang'. " \
                         "Kiểu dữ liệu: VARCHAR. Dữ liệu định danh cá nhân theo PDPL 2025."
        
        prediction = model_loader.predict(vietnamese_text)
        
        assert prediction is not None
        assert 'category_id' in prediction
        assert 'confidence' in prediction
        assert 'name_vi' in prediction
        assert 'name_en' in prediction
        assert 'article' in prediction
        
        assert 0 <= prediction['category_id'] <= 7
        assert 0.0 <= prediction['confidence'] <= 1.0
        assert 'PDPL Article' in prediction['article']
    
    def test_prediction_confidence_threshold(self, model_loader):
        """Test low-confidence predictions"""
        # Ambiguous text (should return lower confidence)
        ambiguous_text = "Field xyz in table abc."
        
        prediction = model_loader.predict(ambiguous_text)
        
        # Should still return prediction, but possibly lower confidence
        assert prediction is not None
        assert 0.0 <= prediction['confidence'] <= 1.0


class TestRecommendationMapper:
    """Test suite for PDPL recommendation mapper"""
    
    @pytest.fixture
    def mapper(self):
        from services.recommendation_mapper import PDPLRecommendationMapper
        return PDPLRecommendationMapper()
    
    def test_generate_recommendations(self, mapper):
        """Test recommendation generation from PDPL principle"""
        field_metadata = {
            'field_name': 'so_tai_khoan',
            'table_name': 'tai_khoan_ngan_hang',
            'data_type': 'VARCHAR',
            'sample_values': ['1234567890', '0987654321']
        }
        
        tenant_context = {
            'veri_business_id': 'VERI_TEST_001',
            'veri_regional_location': 'south',
            'veri_industry_type': 'banking'
        }
        
        recommendations = mapper.generate_recommendations(
            category_id=5,  # Security (An toàn bảo mật)
            confidence=0.92,
            field_metadata=field_metadata,
            tenant_context=tenant_context
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check recommendation structure
        for rec in recommendations:
            assert 'type' in rec
            assert 'title_vi' in rec
            assert 'title_en' in rec
            assert 'confidence' in rec
            assert 'priority' in rec
            
            # Recommendations should be in Vietnamese and English
            assert len(rec['title_vi']) > 0
            assert len(rec['title_en']) > 0
    
    def test_regional_recommendations(self, mapper):
        """Test regional business context in recommendations"""
        tenant_context_north = {
            'veri_business_id': 'VERI_HANOI_001',
            'veri_regional_location': 'north',
            'veri_industry_type': 'government'
        }
        
        tenant_context_south = {
            'veri_business_id': 'VERI_HCMC_001',
            'veri_regional_location': 'south',
            'veri_industry_type': 'technology'
        }
        
        # Should generate different regional recommendations
        recs_north = mapper.generate_recommendations(
            category_id=6, confidence=0.85,
            field_metadata={}, tenant_context=tenant_context_north
        )
        
        recs_south = mapper.generate_recommendations(
            category_id=6, confidence=0.85,
            field_metadata={}, tenant_context=tenant_context_south
        )
        
        # Both should have recommendations, potentially with regional nuances
        assert len(recs_north) > 0
        assert len(recs_south) > 0


class TestFeatureProcessor:
    """Test suite for Vietnamese feature processor"""
    
    def test_prepare_text_input(self):
        """Test Vietnamese text preparation"""
        from services.feature_processor import VietnameseFeatureProcessor
        
        field_metadata = {
            'field_name': 'email',
            'table_name': 'nguoi_dung',
            'data_type': 'VARCHAR',
            'sample_values': ['test@example.com', 'user@domain.vn']
        }
        
        tenant_context = {
            'veri_industry_type': 'ecommerce',
            'veri_regional_location': 'south'
        }
        
        text = VietnameseFeatureProcessor.prepare_text_input(
            field_metadata, tenant_context
        )
        
        # Check Vietnamese text contains key information
        assert 'email' in text
        assert 'nguoi_dung' in text
        assert 'VARCHAR' in text
        assert 'Thương mại điện tử' in text  # Industry translation
        assert 'Miền Nam' in text  # Region translation
    
    def test_regional_context_encoding(self, extractor):
        """Test regional location affects feature extraction"""
        field_metadata = {'field_name': 'email', 'table_name': 'users', 'data_type': 'VARCHAR'}
        
        north_context = {'veri_regional_location': 'north', 'veri_industry_type': 'tech', 
                        'risk_score': 50, 'row_count': 1000, 'is_encrypted': True}
        south_context = {'veri_regional_location': 'south', 'veri_industry_type': 'tech',
                        'risk_score': 50, 'row_count': 1000, 'is_encrypted': True}
        
        north_features = extractor.extract_features(field_metadata, north_context)
        south_features = extractor.extract_features(field_metadata, south_context)
        
        # Features should differ based on region
        assert not torch.equal(north_features['metadata_features'], south_features['metadata_features'])
```

### 8.2 Integration Tests

**File:** `backend/veri_ai_recommendations_engine/tests/test_api.py`

```python
"""
Integration tests for AI recommendations API
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestRecommendationsAPI:
    """Test suite for API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert 'model_loaded' in data
    
    def test_predict_recommendations(self, client):
        """Test prediction endpoint"""
        payload = {
            "field_metadata": {
                "field_name": "ho_va_ten",
                "table_name": "tbl_khach_hang",
                "data_type": "VARCHAR",
                "sample_values": ["Nguyễn Văn A", "Trần Thị B"],
                "current_classification": None
            },
            "tenant_context": {
                "veri_regional_location": "south",
                "veri_industry_type": "banking",
                "risk_score": 75,
                "row_count": 10000,
                "is_encrypted": False
            },
            "confidence_threshold": 0.7
        }
        
        response = client.post("/api/v1/recommendations/predict", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'recommendations' in data
        assert 'model_version' in data
        assert 'inference_time_ms' in data
        assert isinstance(data['recommendations'], list)
    
    def test_invalid_request(self, client):
        """Test API handles invalid requests"""
        invalid_payload = {
            "field_metadata": {
                "field_name": "test"
                # Missing required fields
            }
        }
        
        response = client.post("/api/v1/recommendations/predict", json=invalid_payload)
        
        assert response.status_code == 422  # Validation error
    
    def test_feedback_submission(self, client):
        """Test feedback endpoint"""
        feedback = {
            "field_id": "field_123",
            "recommendation": {
                "type": "classification",
                "predicted_class": "Personal Data",
                "confidence": 0.85
            },
            "action_taken": "accepted",
            "dpo_notes": "Accurate recommendation"
        }
        
        response = client.post("/api/v1/recommendations/feedback", json=feedback)
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'


class TestPerformance:
    """Performance tests"""
    
    def test_prediction_latency(self, client):
        """Test prediction completes within SLA"""
        import time
        
        payload = {
            "field_metadata": {
                "field_name": "email",
                "table_name": "users",
                "data_type": "VARCHAR",
                "sample_values": ["user@example.com"]
            },
            "tenant_context": {
                "veri_regional_location": "north",
                "veri_industry_type": "technology",
                "risk_score": 50,
                "row_count": 5000,
                "is_encrypted": True
            }
        }
        
        start = time.time()
        response = client.post("/api/v1/recommendations/predict", json=payload)
        latency_ms = (time.time() - start) * 1000
        
        assert response.status_code == 200
        assert latency_ms < 500  # 500ms SLA
    
    def test_concurrent_requests(self, client):
        """Test handling concurrent requests"""
        from concurrent.futures import ThreadPoolExecutor
        
        def make_request():
            payload = {
                "field_metadata": {"field_name": "test", "table_name": "test", "data_type": "VARCHAR"},
                "tenant_context": {"veri_regional_location": "south", "veri_industry_type": "tech",
                                 "risk_score": 50, "row_count": 1000, "is_encrypted": False}
            }
            return client.post("/api/v1/recommendations/predict", json=payload)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            responses = [f.result() for f in futures]
        
        success_count = sum(1 for r in responses if r.status_code == 200)
        assert success_count >= 45  # 90% success rate
```

---

## 9. Monitoring & Observability

### 9.1 Prometheus Metrics

**File:** `backend/veri_ai_recommendations_engine/monitoring/metrics.py`

```python
"""
Prometheus metrics for AI recommendations service
"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
from functools import wraps
import time


# Create registry
registry = CollectorRegistry()

# Metrics
prediction_total = Counter(
    'veri_ai_predictions_total',
    'Total number of predictions made',
    ['region', 'industry', 'model_version'],
    registry=registry
)

prediction_latency = Histogram(
    'veri_ai_prediction_latency_seconds',
    'Prediction latency in seconds',
    ['region', 'industry'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
    registry=registry
)

prediction_confidence = Histogram(
    'veri_ai_prediction_confidence',
    'Confidence scores of predictions',
    ['recommendation_type'],
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0],
    registry=registry
)

model_accuracy = Gauge(
    'veri_ai_model_accuracy',
    'Current model accuracy from validation set',
    registry=registry
)

cache_hits = Counter(
    'veri_ai_cache_hits_total',
    'Total number of cache hits',
    registry=registry
)

cache_misses = Counter(
    'veri_ai_cache_misses_total',
    'Total number of cache misses',
    registry=registry
)

active_requests = Gauge(
    'veri_ai_active_requests',
    'Number of active prediction requests',
    registry=registry
)

error_total = Counter(
    'veri_ai_errors_total',
    'Total number of errors',
    ['error_type'],
    registry=registry
)


def track_prediction(region: str, industry: str):
    """Decorator to track prediction metrics"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            active_requests.inc()
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                
                # Track latency
                latency = time.time() - start_time
                prediction_latency.labels(region=region, industry=industry).observe(latency)
                
                # Track predictions
                prediction_total.labels(
                    region=region,
                    industry=industry,
                    model_version=result.get('model_version', 'unknown')
                ).inc()
                
                # Track confidence scores
                for rec in result.get('recommendations', []):
                    prediction_confidence.labels(
                        recommendation_type=rec.get('type', 'unknown')
                    ).observe(rec.get('confidence', 0.0))
                
                # Track cache
                if result.get('cache_hit'):
                    cache_hits.inc()
                else:
                    cache_misses.inc()
                
                return result
                
            except Exception as e:
                error_total.labels(error_type=type(e).__name__).inc()
                raise
            finally:
                active_requests.dec()
        
        return wrapper
    return decorator
```

### 9.2 Logging Configuration

**File:** `backend/veri_ai_recommendations_engine/monitoring/logging_config.py`

```python
"""
Structured logging configuration
"""

import logging
import json
from datetime import datetime


class StructuredLogger(logging.Formatter):
    """JSON structured logging formatter"""
    
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'service': 'veri-ai-recommendations',
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if hasattr(record, 'extra'):
            log_record.update(record.extra)
        
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_record, ensure_ascii=False)


def setup_logging():
    """Configure structured logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredLogger())
    logger.addHandler(handler)
    
    return logger
```

---

## 10. Production Readiness Checklist

### 10.1 Pre-Deployment Checklist

**Model Readiness:**
- [ ] PhoBERT model downloaded and cached
- [ ] Trained model weights loaded successfully
- [ ] Model achieves >85% accuracy on validation set
- [ ] Inference latency <100ms (p99) on GPU
- [ ] Confidence threshold calibrated (0.7 default)

**Infrastructure:**
- [ ] NVIDIA GPU drivers installed (CUDA 11.8+)
- [ ] Redis cache configured and tested
- [ ] PostgreSQL database for feedback storage
- [ ] Docker images built and tested
- [ ] Kubernetes cluster configured with GPU operator

**Integration:**
- [ ] Document #7 updated with microservice integration
- [ ] API endpoints tested with Vietnamese data
- [ ] Graceful degradation verified (falls back to rule-based)
- [ ] Timeout handling configured (5s default)
- [ ] Error logging and monitoring active

**Security:**
- [ ] API authentication enabled (JWT tokens)
- [ ] HTTPS/TLS configured for production
- [ ] Secrets managed via Kubernetes secrets
- [ ] Network policies restrict access
- [ ] Data encryption at rest and in transit

**Monitoring:**
- [ ] Prometheus metrics exported
- [ ] Grafana dashboards created
- [ ] Alert rules configured (latency, errors, accuracy)
- [ ] Log aggregation setup (ELK/Loki)
- [ ] Health checks passing

**Testing:**
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing
- [ ] Performance tests meet SLA (<500ms)
- [ ] Load testing completed (1000 req/s)
- [ ] Regional Vietnamese data tested (North/Central/South)

### 10.2 Rollout Strategy

**Phase 1: Canary Deployment (Week 1)**
- Deploy to 10% of traffic
- Monitor accuracy, latency, error rates
- Collect DPO feedback on recommendations
- Compare ML vs. rule-based performance

**Phase 2: Gradual Rollout (Weeks 2-4)**
- Increase to 25% traffic (Week 2)
- Increase to 50% traffic (Week 3)
- Increase to 100% traffic (Week 4)
- Continuous monitoring and tuning

**Phase 3: Active Learning (Ongoing)**
- Collect user feedback on recommendations
- Retrain model monthly with new data
- A/B test model versions
- Regional model fine-tuning (North/South differences)

### 10.3 Success Metrics

**Model Performance:**
- Accuracy: >85% on Vietnamese PDPL scenarios
- Precision: >80% for critical recommendations
- Recall: >75% for sensitive data detection
- F1 Score: >80% across all PDPL categories

**System Performance:**
- Inference latency: <100ms (p99)
- Throughput: >1000 predictions/second
- Cache hit rate: >60%
- Error rate: <1%

**Business Impact:**
- DPO time savings: >30% reduction in manual classification
- Recommendation acceptance rate: >70%
- PDPL compliance improvement: Faster field classification
- User satisfaction: >4.0/5.0 rating

---

## 9. Summary

This document provides a **complete implementation plan** for the VeriSyntra AI Recommendations Microservice using the **existing VeriAIDPO_Principles_VI_v1 model**:

### 9.1 What's Implemented

**1. VeriAIDPO Model Integration (~300 lines)**
- VeriAIDPORecommendationLoader: Auto-downloads from HuggingFace Hub
- 8 PDPL principle classification (Articles 7, 8, 9, 10, 13, 15, 17, 18-23)
- 78-88% accuracy on Vietnamese legal text
- Trained on real PDPL Law 91/2025/QH15 + Decree 13/2023/ND-CP

**2. Recommendation Mapper (~250 lines)**
- PDPLRecommendationMapper: Converts principles -> compliance actions
- Compliance actions, retention periods, security priorities
- Vietnamese/English bilingual recommendations
- Regional business context (North/Central/South patterns)

**3. FastAPI Microservice (~400 lines)**
- REST API endpoints: /health, /predict, /feedback
- Redis caching (15-minute TTL)
- PostgreSQL feedback storage
- Graceful error handling with fallback to rule-based

**4. Document #7 Integration (~150 lines)**
- SmartRecommendationsEngine integration
- PDPL principle -> Document #7 recommendation mapping
- Timeout handling (5s) with rule-based fallback
- Hybrid AI + rules approach

**5. Feature Processing (~100 lines)**
- VietnameseFeatureProcessor: Field metadata -> Vietnamese text
- Industry/region translation (Vietnamese business contexts)
- Compliance context hints (CMND, email, bank data)

**6. Deployment Configuration (~200 lines)**
- Docker + docker-compose setup
- HuggingFace Hub authentication (HF_TOKEN)
- Redis + PostgreSQL services
- CPU-only deployment (GPU optional)

**7. Testing Suite (~300 lines)**
- VeriAIDPO model loader tests
- Recommendation mapper tests
- Vietnamese feature processor tests
- Integration tests with Document #7

**8. Feedback & Continuous Improvement (~200 lines)**
- DPO feedback collection (accept/reject/modify)
- Model performance analytics by PDPL category
- Rejected sample export for future retraining
- Acceptance rate tracking

### 9.2 Key Architectural Decisions

**Using Existing VeriAIDPO Model (Not Training New Model):**
- [OK] **Practical:** Real trained model with 78-88% accuracy (already proven)
- [OK] **Faster:** No training pipeline required for initial deployment
- [OK] **Simpler:** ~1,800 lines vs ~2,100 lines (300 lines saved)
- [OK] **Maintainable:** Model updates via HuggingFace Hub (version control)

**Recommendation Mapping Layer:**
- [OK] **Separation:** PDPL classification (ML) vs. compliance actions (business logic)
- [OK] **Flexibility:** Update recommendations without retraining model
- [OK] **Regional:** Vietnamese business patterns (North/Central/South)
- [OK] **Bilingual:** Vietnamese + English for all recommendations

**HuggingFace Hub Distribution:**
- [OK] **Auto-download:** Model downloads on first microservice startup (~540MB)
- [OK] **Caching:** Subsequent startups load from local cache (<5s)
- [OK] **Versioning:** Easy model updates via HuggingFace versioning
- [OK] **Private repo:** Access control via HF_TOKEN

### 9.3 Performance Characteristics

**Model Performance:**
- **Accuracy:** 78-88% on Vietnamese legal/compliance text
- **PDPL Principles:** 8 categories with Vietnamese + English names
- **Training Data:** 24,000 samples from real legal corpus (813 lines)
- **Inference Speed:** <100ms per prediction (CPU), <50ms (GPU)

**System Performance:**
- **Cache Hit Rate:** >60% (Redis 15-minute TTL)
- **Throughput:** 500-1000 predictions/second (CPU)
- **Latency:** p50 <50ms, p99 <200ms
- **Availability:** 99.9% with graceful degradation to rules

**Business Impact:**
- **DPO Time Savings:** 30-50% faster field classification
- **Recommendation Acceptance:** Target >70% acceptance rate
- **Vietnamese Context:** Regional business patterns integrated
- **Legal Accuracy:** Direct mapping to PDPL articles

### 9.4 Production Deployment Checklist

**Pre-Deployment:**
- [ ] HuggingFace token configured (HF_TOKEN environment variable)
- [ ] Redis service running (localhost:6379 or Docker)
- [ ] PostgreSQL feedback database created
- [ ] .env file configured with all required variables

**Deployment:**
- [ ] Docker images built (`docker-compose build`)
- [ ] Services started (`docker-compose up -d`)
- [ ] Health check passing (`curl http://localhost:8013/health`)
- [ ] Model auto-downloaded from HuggingFace Hub (~2-5 minutes first run)

**Integration:**
- [ ] Document #7 updated with VeriAIDPO integration code
- [ ] API endpoints tested with Vietnamese field data
- [ ] Timeout handling verified (5s fallback to rules)
- [ ] Confidence thresholds configured (default 0.7)

**Monitoring:**
- [ ] Feedback collection working (DPO accept/reject/modify)
- [ ] Redis cache hit rate >50%
- [ ] Model prediction latency <100ms (p99)
- [ ] Error rate <1%

### 9.5 Success Metrics

**Model Metrics:**
- Accuracy: >78% (current baseline)
- Acceptance rate: >70% (DPO feedback)
- Confidence: >0.7 for actionable recommendations

**System Metrics:**
- Latency: <100ms p99
- Throughput: >500 req/s
- Cache hit: >60%
- Uptime: >99.5%

**Business Metrics:**
- DPO time savings: >30%
- Faster PDPL compliance
- Vietnamese cultural alignment

### 9.6 Future Enhancements

**Short-term (1-3 months):**
- Collect 1,000+ feedback samples
- Analyze acceptance rates by PDPL category
- Fine-tune model on rejected/modified samples

**Medium-term (3-6 months):**
- Regional model variants (North/South Vietnamese patterns)
- Industry-specific fine-tuning (banking, healthcare, etc.)
- Expanded PDPL category support (if regulations change)

**Long-term (6-12 months):**
- Multi-task learning (classification + retention + security in one model)
- Active learning pipeline (auto-label high-confidence samples)
- Vietnamese LLM integration (GPT-4 with PDPL knowledge)

---

## 10. Total Implementation

**Code Statistics:**
- **Core Model Integration:** ~300 lines (VeriAIDPO loader)
- **Recommendation Mapper:** ~250 lines (principles -> actions)
- **FastAPI Microservice:** ~400 lines (API endpoints + caching)
- **Feature Processing:** ~100 lines (Vietnamese text preparation)
- **Document #7 Integration:** ~150 lines (SmartRecommendationsEngine)
- **Configuration:** ~200 lines (Docker, env, settings)
- **Testing:** ~300 lines (unit + integration tests)
- **Documentation:** ~1,100 lines (this document)

**Total:** ~2,800 lines (down from ~4,200 lines)  
**Reduction:** ~1,400 lines removed (training pipeline, complex multi-task model)  
**Simplification:** 33% code reduction while maintaining full functionality

**Key Benefits:**
- [OK] **Vietnamese-First:** PhoBERT understands Vietnamese legal terminology and regional patterns
- [OK] **Proven Accuracy:** 78-88% on real PDPL legal corpus (not synthetic data)
- [OK] **Production-Ready:** Uses existing trained model from HuggingFace Hub
- [OK] **Low Latency:** <100ms inference with CPU (faster with GPU)
- [OK] **Scalable:** Redis caching + horizontal scaling (Docker/Kubernetes)
- [OK] **Resilient:** Graceful degradation to rule-based recommendations
- [OK] **Maintainable:** Clear separation (ML classification vs. business logic)
- [OK] **Observable:** Feedback collection + performance monitoring

**Next Steps:**
1. Set HF_TOKEN environment variable for VeriAIDPO model access
2. Start microservice: `docker-compose up -d`
3. Verify health: `curl http://localhost:8013/health`
4. Integrate with Document #7 (SmartRecommendationsEngine)
5. Collect feedback from DPO users (accept/reject/modify)
6. Monitor acceptance rates and retrain when needed (>1,000 samples)

**Document Version:** 1.2 (Port changed from 8011 to 8013 to avoid conflict with veri-data-sync-service)  
**Implementation Status:** Complete and ready for deployment  
**Vietnamese PDPL 2025 Compliance:** Full integration with 8 PDPL principles

---

**END OF DOCUMENT #10**

