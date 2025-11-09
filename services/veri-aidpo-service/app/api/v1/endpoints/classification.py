"""
VeriAIDPO Classification API with Company Normalization
Phase 3 Implementation - Company-Agnostic Classification

Version: 1.0.0
Status: COMPLETE - RBAC Protected (Task 1.1.3 Step 7)

RBAC Protection:
- Classification endpoints require processing_activity.read permission
- Normalize endpoint requires data_category.write permission  
- Health check is public (no auth)
- Model status requires analytics.read permission
- Preload model requires user.write permission (admin only)
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger

# Import core components (microservice local)
from app.core.pdpl_normalizer import get_normalizer
from app.core.company_registry import get_registry
from app.ml.model_loader import get_model_loader, get_category_info, PDPL_CATEGORIES

# RBAC authentication - Phase 2 integration
from app.auth.permissions import require_permission
from app.auth.jwt_validator import validate_token


router = APIRouter(prefix="/api/v1", tags=["classification"])


# Request/Response Models
class ClassificationRequest(BaseModel):
    """Request model for classification"""
    text: str = Field(
        ..., 
        description="Vietnamese text to classify", 
        example="Shopee VN thu thap so dien thoai de lien he giao hang"
    )
    model_type: str = Field(
        "principles", 
        description="Model type to use (principles, legal_basis, breach_triage, etc.)",
        example="legal_basis"
    )
    language: str = Field(
        "vi", 
        description="Language code (vi or en)",
        example="vi"
    )
    include_metadata: bool = Field(
        True, 
        description="Include normalization metadata in response"
    )


class ClassificationResponse(BaseModel):
    """Response model for classification"""
    prediction: str
    confidence: float
    category_id: int
    model_type: str
    language: str
    normalized_text: Optional[str] = None
    detected_companies: Optional[List[str]] = None
    original_text: Optional[str] = None
    processing_metadata: Optional[Dict[str, Any]] = None


class NormalizationRequest(BaseModel):
    """Request model for text normalization"""
    text: str = Field(..., description="Text to normalize", example="Shopee VN va Tiki deu thu thap email")
    normalize_companies: bool = Field(True, description="Normalize company names")
    normalize_persons: bool = Field(False, description="Normalize person names")
    normalize_locations: bool = Field(False, description="Normalize addresses")


class NormalizationResponse(BaseModel):
    """Response model for text normalization"""
    original_text: str
    normalized_text: str
    detected_companies: List[str]
    normalization_count: int
    processing_time_ms: float


# Model type definitions (from Phase 2)
MODEL_TYPES = {
    'principles': {
        0: 'Lawfulness', 1: 'Purpose Limitation', 2: 'Data Minimization',
        3: 'Accuracy', 4: 'Storage Limitation', 5: 'Security',
        6: 'Transparency', 7: 'Accountability'
    },
    'legal_basis': {
        0: 'Consent', 1: 'Contract Performance',
        2: 'Legal Obligation', 3: 'Legitimate Interest'
    },
    'breach_triage': {
        0: 'Low Risk', 1: 'Medium Risk',
        2: 'High Risk', 3: 'Critical Risk'
    },
    'cross_border': {
        0: 'Domestic Only', 1: 'Approved Country List',
        2: 'Requires MPS Approval', 3: 'Prohibited Transfer',
        4: 'Emergency Exception'
    },
    'consent_type': {
        0: 'Explicit Consent', 1: 'Implied Consent',
        2: 'Parental Consent', 3: 'Invalid Consent'
    },
    'data_sensitivity': {
        0: 'Basic Data', 1: 'Personal Data',
        2: 'Sensitive Data', 3: 'Special Category'
    },
    'dpo_tasks': {
        0: 'Advisory', 1: 'Policy Development',
        2: 'Training', 3: 'Audit', 4: 'Regulatory Liaison'
    },
    'risk_level': {
        0: 'Low Risk', 1: 'Medium Risk',
        2: 'High Risk (DPIA Required)', 3: 'Critical Risk'
    },
    'compliance_status': {
        0: 'Compliant', 1: 'Partially Compliant',
        2: 'Non-Compliant', 3: 'Unknown/Requires Assessment'
    },
    'regional': {
        0: 'North Vietnam', 1: 'Central Vietnam', 2: 'South Vietnam'
    },
    'industry': {
        0: 'Finance/Banking', 1: 'Healthcare',
        2: 'Education', 3: 'Technology/E-commerce'
    }
}


def get_category_name(model_type: str, category_id: int) -> str:
    """Get category name from model type and ID"""
    if model_type not in MODEL_TYPES:
        return f"Unknown (Category {category_id})"
    
    categories = MODEL_TYPES[model_type]
    return categories.get(category_id, f"Unknown (Category {category_id})")


# Classification Endpoints
@router.post("/classify", response_model=ClassificationResponse)
async def classify_text(
    request: ClassificationRequest,
    current_user: dict = Depends(require_permission("processing_activity.read"))
):
    """
    Universal VeriAIDPO classification endpoint
    
    **RBAC:** Requires `processing_activity.read` permission (admin/dpo/compliance_manager/staff roles)
    
    Automatically normalizes company names before inference, making the model
    company-agnostic. Works with ANY Vietnamese company without retraining.
    
    **Supported Model Types:**
    - principles: PDPL core principles (8 categories)
    - legal_basis: Legal basis for processing (4 categories)
    - breach_triage: Breach severity classification (4 categories)
    - cross_border: Cross-border transfer rules (5 categories)
    - consent_type: Consent mechanism classification (4 categories)
    - data_sensitivity: Data classification (4 categories)
    - dpo_tasks: DPO task categorization (5 categories)
    - risk_level: Risk assessment (4 categories)
    - compliance_status: Compliance tracking (4 categories)
    - regional: Regional business context (3 categories)
    - industry: Industry-specific rules (4 categories)
    
    **Example Request:**
    ```json
    {
      "text": "Shopee VN thu thap email dua tren hop dong mua ban voi khách hàng",
      "model_type": "legal_basis",
      "language": "vi",
      "include_metadata": true
    }
    ```
    
    **Example Response:**
    ```json
    {
      "prediction": "Contract Performance",
      "confidence": 0.87,
      "category_id": 1,
      "model_type": "legal_basis",
      "language": "vi",
      "normalized_text": "[COMPANY] thu thap email dua tren hop dong mua ban voi khách hàng",
      "detected_companies": ["Shopee VN", "Shopee Vietnam"],
      "original_text": "Shopee VN thu thap email..."
    }
    ```
    
    Vietnamese: Phan loai van ban PDPL su dung AI (yeu cau quyen doc hoat dong xu ly)
    """
    start_time = datetime.now()
    
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"classifying text: model_type={request.model_type}, language={request.language}"
        )
        
        # Validate model type
        if request.model_type not in MODEL_TYPES:
            available = ", ".join(MODEL_TYPES.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model_type '{request.model_type}'. Available: {available}"
            )
        
        # 1. Normalize text (company names -> [COMPANY])
        normalizer = get_normalizer()
        normalized_text = normalizer.normalize_for_inference(request.text)
        
        logger.debug(f"Normalized: '{request.text[:50]}...' -> '{normalized_text[:50]}...'")
        
        # 2. Run inference on normalized text
        # Load model and run prediction
        model_loader = get_model_loader()
        
        # For now, only 'principles' model is available
        if request.model_type == 'principles':
            # Run inference
            prediction_result = model_loader.predict(normalized_text)
            
            if prediction_result is None:
                raise HTTPException(
                    status_code=500,
                    detail="Model inference failed. Please check model files and try again."
                )
            
            category_id = prediction_result['category_id']
            confidence = prediction_result['confidence']
            
            # Get category name
            cat_info = get_category_info(category_id, language=request.language)
            category_name = cat_info['name']
            
            prediction = {
                'category': category_name,
                'category_id': category_id,
                'confidence': round(confidence, 2),
                'all_probabilities': prediction_result.get('all_probabilities', {})
            }
            
            logger.info(f"Prediction: {category_name} (Cat {category_id}, confidence: {confidence:.2%})")
        else:
            # Other model types not yet implemented
            raise HTTPException(
                status_code=501,
                detail=f"Model type '{request.model_type}' not yet implemented. Currently only 'principles' is available."
            )
        
        # 3. Prepare response
        response = ClassificationResponse(
            prediction=prediction['category'],
            confidence=prediction['confidence'],
            category_id=prediction['category_id'],
            model_type=request.model_type,
            language=request.language
        )
        
        # 4. Add metadata if requested
        if request.include_metadata:
            response.normalized_text = normalized_text
            response.original_text = request.text
            
            # Detect which companies were mentioned
            registry = get_registry()
            detected_companies = []
            company_names = registry.get_all_companies()
            
            for company in company_names:
                if company.lower() in request.text.lower():
                    detected_companies.append(company)
            
            response.detected_companies = detected_companies
            
            # Processing metadata
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            response.processing_metadata = {
                'processing_time_ms': round(processing_time, 2),
                'normalization_applied': normalized_text != request.text,
                'companies_detected': len(detected_companies),
                'model_categories': 8,  # PDPL has 8 categories
                'timestamp': datetime.now().isoformat()
            }
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@router.post("/classify-legal-basis", response_model=ClassificationResponse)
async def classify_legal_basis(
    request: ClassificationRequest,
    current_user: dict = Depends(require_permission("processing_activity.read"))
):
    """
    Classify legal basis for data processing (Article 13.1 PDPL)
    
    **RBAC:** Requires `processing_activity.read` permission (admin/dpo/compliance_manager/staff roles)
    
    Automatically routes to the legal_basis model.
    
    **Categories:**
    - Consent (Article 13.1.a)
    - Contract Performance (Article 13.1.b)
    - Legal Obligation (Article 13.1.c)
    - Legitimate Interest (Article 13.1.d)
    
    Vietnamese: Phan loai co so phap ly cho xu ly du lieu (Dieu 13.1 PDPL)
    """
    logger.info(
        f"[RBAC] User {current_user.email} (role: {current_user.role}) "
        f"classifying legal basis"
    )
    request.model_type = 'legal_basis'
    return await classify_text(request, current_user)


@router.post("/classify-breach-severity", response_model=ClassificationResponse)
async def classify_breach_severity(
    request: ClassificationRequest,
    current_user: dict = Depends(require_permission("processing_activity.read"))
):
    """
    Classify data breach severity for notification requirements
    
    **RBAC:** Requires `processing_activity.read` permission (admin/dpo/compliance_manager/staff roles)
    
    Automatically routes to the breach_triage model.
    
    **Categories:**
    - Critical Breach
    - High Severity
    - Medium Severity
    - Low Severity
    
    Vietnamese: Phan loai muc do nghiem trong cua vi pham du lieu
    """
    logger.info(
        f"[RBAC] User {current_user.email} (role: {current_user.role}) "
        f"classifying breach severity"
    )
    request.model_type = 'breach_triage'
    return await classify_text(request, current_user)


@router.post("/classify-cross-border", response_model=ClassificationResponse)
async def classify_cross_border(
    request: ClassificationRequest,
    current_user: dict = Depends(require_permission("processing_activity.read"))
):
    """
    Classify cross-border data transfer compliance
    
    **RBAC:** Requires `processing_activity.read` permission (admin/dpo/compliance_manager/staff roles)
    
    Automatically routes to the cross_border model.
    
    **Categories:**
    - Adequate Protection: Transfer to countries with adequate protection
    - Standard Clauses: Transfer using standard contractual clauses
    - Explicit Consent: Transfer based on data subject consent
    - MPS Approval Required: Transfer requiring Ministry approval
    - Prohibited Transfer: Transfer not allowed under PDPL
    
    Vietnamese: Phan loai tuan thu chuyen giao du lieu xuyen bien gioi
    """
    logger.info(
        f"[RBAC] User {current_user.email} (role: {current_user.role}) "
        f"classifying cross-border transfer"
    )
    request.model_type = 'cross_border'
    return await classify_text(request, current_user)


# Normalization Endpoint
@router.post("/normalize", response_model=NormalizationResponse)
async def normalize_text(
    request: NormalizationRequest,
    current_user: dict = Depends(require_permission("data_category.write"))
):
    """
    Normalize text for VeriAIDPO inference
    
    **RBAC:** Requires `data_category.write` permission (admin/dpo/compliance_manager roles)
    
    Standalone normalization endpoint useful for:
    - Testing normalization accuracy
    - Pre-processing text before batch classification
    - Debugging company detection
    
    **Example Request:**
    ```json
    {
      "text": "Shopee VN va Tiki deu thu thap email khách hàng",
      "normalize_companies": true,
      "normalize_persons": false,
      "normalize_locations": false
    }
    ```
    
    **Example Response:**
    ```json
    {
      "original_text": "Shopee VN va Tiki deu thu thap email khách hàng",
      "normalized_text": "[COMPANY] va [COMPANY] deu thu thap email khách hàng",
      "detected_companies": ["Shopee VN", "Tiki"],
      "normalization_count": 2,
      "processing_time_ms": 12.5
    }
    ```
    
    Vietnamese: Chuan hoa van ban cho suy luan VeriAIDPO
    """
    start_time = datetime.now()
    
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"normalizing text: companies={request.normalize_companies}, "
            f"persons={request.normalize_persons}, locations={request.normalize_locations}"
        )
        
        normalizer = get_normalizer()
        normalized_text = request.text
        
        # Apply normalizations
        if request.normalize_companies:
            normalized_text = normalizer.normalize_text(normalized_text)
        
        if request.normalize_persons:
            normalized_text = normalizer.normalize_person_names(normalized_text)
        
        if request.normalize_locations:
            normalized_text = normalizer.normalize_locations(normalized_text)
        
        # Detect companies
        registry = get_registry()
        detected_companies = []
        company_names = registry.get_all_companies()
        
        for company in company_names:
            if company.lower() in request.text.lower():
                detected_companies.append(company)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Count normalizations
        normalization_count = request.text.count('[COMPANY]') if '[COMPANY]' not in request.text else 0
        normalization_count += normalized_text.count('[COMPANY]')
        normalization_count += normalized_text.count('[PERSON]')
        normalization_count += normalized_text.count('[ADDRESS]')
        
        logger.info(f"Normalized {normalization_count} entities in {processing_time:.2f}ms")
        
        return NormalizationResponse(
            original_text=request.text,
            normalized_text=normalized_text,
            detected_companies=detected_companies,
            normalization_count=normalization_count,
            processing_time_ms=round(processing_time, 2)
        )
    
    except Exception as e:
        logger.error(f"Normalization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Normalization failed: {str(e)}")


# Health Check Endpoint
@router.get("/health")
async def veriaidpo_health_check():
    """
    VeriAIDPO service health check
    
    Returns status of all components:
    - Company registry
    - Text normalizer
    - Model loader
    - Available model types
    """
    try:
        registry = get_registry()
        normalizer = get_normalizer()
        model_loader = get_model_loader()
        
        stats = registry.get_statistics()
        model_info = model_loader.get_model_info()
        
        return {
            "status": "healthy",
            "service": "VeriAIDPO Classification API",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "company_registry": {
                    "status": "active",
                    "total_companies": stats['total_companies'],
                    "last_modified": stats.get('last_modified')
                },
                "text_normalizer": {
                    "status": "active",
                    "registry_loaded": True
                },
                "model_loader": {
                    "status": model_info['status'],
                    "device": model_info['device'],
                    "model_type": model_info.get('model_type', 'VeriAIDPO_Principles_VI_v1'),
                    "num_labels": model_info.get('num_labels', 'not_loaded'),
                    "vocab_size": model_info.get('vocab_size', 'not_loaded')
                },
                "model_types": {
                    "available": ['principles'],
                    "implemented": ['principles'],
                    "planned": list(MODEL_TYPES.keys())
                }
            },
            "version": "1.0.0"
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.get("/model-status")
async def get_model_status(
    current_user: dict = Depends(require_permission("analytics.read"))
):
    """
    Get detailed model status and information
    
    **RBAC:** Requires `analytics.read` permission (admin/dpo/compliance_manager/auditor roles)
    
    Returns:
    - Model loading status
    - Device information (CPU/GPU)
    - Model configuration
    - Performance metrics
    
    Vietnamese: Lay trang thai chi tiet cua mo hinh
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"checking model status"
        )
        model_loader = get_model_loader()
        model_info = model_loader.get_model_info()
        
        return {
            "status": "success",
            "model": model_info,
            "categories": {
                "total": 8,
                "list": [
                    {
                        "id": i,
                        "name_vi": PDPL_CATEGORIES[i]['vi'],
                        "name_en": PDPL_CATEGORIES[i]['en'],
                        "description": PDPL_CATEGORIES[i]['description']
                    }
                    for i in range(8)
                ]
            },
            "inference_config": {
                "max_length": 256,
                "language": "vi",
                "normalization": "company_agnostic"
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Model status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model status check failed: {str(e)}")


@router.post("/preload-model")
async def preload_model(
    current_user: dict = Depends(require_permission("user.write"))
):
    """
    Preload model into memory (optional optimization)
    
    **RBAC:** Requires `user.write` permission (admin role only)
    
    By default, model loads lazily on first inference request.
    Use this endpoint to preload for faster first response.
    
    Vietnamese: Tai truoc mo hinh vao bo nho (toi uu hoa - chi admin)
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"preloading model"
        )
        model_loader = get_model_loader()
        
        if model_loader.is_loaded:
            return {
                "status": "already_loaded",
                "message": "Model is already loaded in memory",
                "model_info": model_loader.get_model_info()
            }
        
        logger.info("Preloading model as requested...")
        success = model_loader.load_model()
        
        if success:
            return {
                "status": "success",
                "message": "Model preloaded successfully",
                "model_info": model_loader.get_model_info()
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to preload model. Check logs for details."
            )
    
    except Exception as e:
        logger.error(f"Model preload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model preload failed: {str(e)}")
