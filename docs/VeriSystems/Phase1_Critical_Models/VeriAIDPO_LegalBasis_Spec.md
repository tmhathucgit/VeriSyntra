# VeriAIDPO_LegalBasis - Legal Basis Classification

**Phase**: 🚨 Phase 1 - CRITICAL  
**Priority**: 🚨 CRITICAL  
**PDPL Reference**: Article 13.1 (a-f)  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2-3 days
- English (EN - SECONDARY): 2-3 days
- **Total**: 4-6 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_LegalBasis_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_LegalBasis_EN` (BERT, English secondary)

**Use Cases**: Legal Basis Setup wizard, compliance validation, processing activity records

---

## Categories (4 classes)

```python
LEGAL_BASIS_CATEGORIES = {
    0: {
        "en": "Consent",
        "vi": "Đồng ý của chủ thể dữ liệu",
        "pdpl_article": "Article 13.1.a",
        "description_en": "Data subject has given explicit consent for processing",
        "description_vi": "Chủ thể dữ liệu đã đồng ý rõ ràng cho việc xử lý",
        "examples_en": [
            "User subscribes to marketing newsletter",
            "Customer opts in to promotional emails",
            "Visitor accepts cookies on website"
        ],
        "examples_vi": [
            "Người dùng đăng ký nhận bản tin marketing",
            "Khách hàng chọn nhận email khuyến mãi",
            "Khách truy cập chấp nhận cookies trên website"
        ]
    },
    1: {
        "en": "Contract Performance",
        "vi": "Thực hiện hợp đồng",
        "pdpl_article": "Article 13.1.b",
        "description_en": "Processing necessary for contract execution",
        "description_vi": "Xử lý cần thiết để thực hiện hợp đồng",
        "examples_en": [
            "Processing payment for online order",
            "Shipping customer address for delivery",
            "Account management for service provision"
        ],
        "examples_vi": [
            "Xử lý thanh toán cho đơn hàng trực tuyến",
            "Giao hàng theo địa chỉ khách hàng",
            "Quản lý tài khoản để cung cấp dịch vụ"
        ]
    },
    2: {
        "en": "Legal Obligation",
        "vi": "Nghĩa vụ pháp lý",
        "pdpl_article": "Article 13.1.c",
        "description_en": "Processing required by Vietnamese law",
        "description_vi": "Xử lý theo yêu cầu của luật pháp Việt Nam",
        "examples_en": [
            "Tax reporting to Vietnamese authorities",
            "Employee salary reporting to social insurance",
            "MPS compliance reporting"
        ],
        "examples_vi": [
            "Báo cáo thuế cho cơ quan thuế Việt Nam",
            "Báo cáo lương nhân viên cho bảo hiểm xã hội",
            "Báo cáo tuân thủ cho Bộ Công an"
        ]
    },
    3: {
        "en": "Legitimate Interest",
        "vi": "Lợi ích chính đáng",
        "pdpl_article": "Article 13.1.f",
        "description_en": "Processing for legitimate business interests (with balancing test)",
        "description_vi": "Xử lý cho lợi ích kinh doanh chính đáng (cần cân nhắc)",
        "examples_en": [
            "Fraud prevention and security monitoring",
            "Network security threat detection",
            "Internal audit and compliance monitoring"
        ],
        "examples_vi": [
            "Phòng chống gian lận và giám sát bảo mật",
            "Phát hiện mối đe dọa an ninh mạng",
            "Kiểm toán nội bộ và giám sát tuân thủ"
        ]
    }
}
```

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_LegalBasis_VI

- **Total Samples**: 10,000 (2,500 per category)
- **Difficulty**: VERY HARD with high ambiguity
- **Dataset Composition**:
  - VERY_HARD: 1,000 samples/category (40%) - Overlapping legal bases
  - HARD: 1,000 samples/category (40%) - No legal keywords
  - MEDIUM: 350 samples/category (14%) - Subtle legal language
  - EASY: 150 samples/category (6%) - Clear legal basis
- **Regional Variations**: North (formal), Central (balanced), South (casual)
- **Formality Levels**: Legal, Formal, Business, Casual
- **Sources**:
  - Vietnamese e-commerce consent forms (Shopee, Tiki, Lazada)
  - Banking contract terms (VCB, Techcombank, VPBank)
  - Tax reporting documentation (GSO, MPS)
  - Security policy documents (Viettel, FPT)

### English (SECONDARY) - VeriAIDPO_LegalBasis_EN

- **Total Samples**: 6,000 (1,500 per category)
- **Difficulty**: MODERATE-HARD with controlled ambiguity
- **Dataset Composition**:
  - VERY_HARD: 525 samples/category (35%) - Overlapping legal bases
  - HARD: 600 samples/category (40%) - No legal keywords
  - MEDIUM: 270 samples/category (18%) - Subtle legal language
  - EASY: 105 samples/category (7%) - Clear legal basis
- **Formality Levels**: Formal, Business
- **Sources**: International compliance documents, GDPR comparisons, standard business agreements

---

## Template Examples

```python
# Consent (Category 0)
"Khách hàng đồng ý cho {company} gửi email khuyến mãi về sản phẩm mới."
"User gives permission to {company} to send promotional notifications."

# Contract (Category 1)
"{company} xử lý thông tin thanh toán để hoàn tất giao dịch mua hàng của khách."
"{company} processes payment information to complete customer purchase transaction."

# Legal Obligation (Category 2)
"{company} báo cáo dữ liệu lương nhân viên cho cơ quan bảo hiểm xã hội theo luật."
"{company} reports employee salary data to social insurance as required by law."

# Legitimate Interest (Category 3)
"{company} giám sát truy cập hệ thống để phát hiện hoạt động đáng ngờ và bảo vệ khách hàng."
"{company} monitors system access to detect suspicious activity and protect customers."
```

---

## Training Configuration

### Vietnamese Model (VeriAIDPO_LegalBasis_VI)

```python
MODEL_NAME = "vinai/phobert-base-v2"  # Vietnamese PhoBERT
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 10000  # 2,500 per category
DATASET_DIFFICULTY = "VERY_HARD"  # 40% VERY_HARD, 40% HARD, 14% MEDIUM, 6% EASY
EPOCHS = 8-10  # More epochs for hard dataset
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256  # Longer for complex Vietnamese sentences
REGIONAL_VARIATIONS = ['north', 'central', 'south']
FORMALITY_LEVELS = ['legal', 'formal', 'business', 'casual']
```

### English Model (VeriAIDPO_LegalBasis_EN)

```python
MODEL_NAME = "bert-base-uncased"  # English BERT
NUM_CATEGORIES = 4
TOTAL_SAMPLES = 6000  # 1,500 per category
DATASET_DIFFICULTY = "MODERATE-HARD"  # 35% VERY_HARD, 40% HARD, 18% MEDIUM, 7% EASY
EPOCHS = 6-8  # Fewer epochs (BERT has more pre-training)
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 128  # Standard for English
FORMALITY_LEVELS = ['formal', 'business']
```

---

## Success Metrics

### Vietnamese Model (VeriAIDPO_LegalBasis_VI)

- **Target Accuracy**: 82-88% (production-grade with hard dataset)
- **Confidence**: 78-85% average
- **Inference Speed**: <50ms per request
- **Dataset**: 10,000 samples with 40% VERY_HARD ambiguity

### English Model (VeriAIDPO_LegalBasis_EN)

- **Target Accuracy**: 85-90% (production-grade with moderate-hard dataset)
- **Confidence**: 82-88% average
- **Inference Speed**: <50ms per request
- **Dataset**: 6,000 samples with 35% VERY_HARD ambiguity

---

## 📋 Architecture Requirements

**CRITICAL - Production Backend Integration**:

✅ **MUST use production backend modules** - See [Architecture Requirements](../VeriAIDPO_Architecture_Requirements.md)

**Required Files for Colab**:
1. `backend/app/core/company_registry.py` (513 lines)
2. `backend/app/core/pdpl_normalizer.py` (~300 lines)
3. `backend/config/company_registry.json` (46+ companies)

**Key Benefits**:
- ✅ Training code = Production code (zero drift)
- ✅ Hot-reload capability (add companies without retraining)
- ✅ Single source of truth
- ✅ Easier maintenance

**Setup Guide**: See `docs/VeriSystems/VeriAIDPO_Colab_Setup_Guide.md`

---

## Related Documentation

- [Implementation Overview](../VeriAIDPO_Implementation_Overview.md)
- [Architecture Requirements](../VeriAIDPO_Architecture_Requirements.md)
- [Phase 0: Principles Retraining](../VeriAIDPO_Phase0_Principles_Retraining.md)
- [Colab Setup Guide](../VeriAIDPO_Colab_Setup_Guide.md)
