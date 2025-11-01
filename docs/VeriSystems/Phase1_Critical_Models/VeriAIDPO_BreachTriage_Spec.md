# VeriAIDPO_BreachTriage - Breach Notification Classification

**Phase**: 🚨 Phase 1 - CRITICAL  
**Priority**: 🚨 CRITICAL  
**PDPL Reference**: Articles 37-38, Decree 13/2023 Article 18  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 2-3 days
- English (EN - SECONDARY): 2-3 days
- **Total**: 4-6 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_BreachTriage_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_BreachTriage_EN` (BERT, English secondary)

**Use Cases**: Incident response automation, breach triage, MPS notification triggers

---

## Categories (4 classes)

```python
BREACH_SEVERITY_CATEGORIES = {
    0: {
        "en": "Low Risk",
        "vi": "Rủi ro Thấp",
        "notification": "Internal only - Document and monitor",
        "notification_vi": "Nội bộ - Ghi chép và theo dõi",
        "timeline": "None required",
        "examples_en": [
            "Minor configuration error affecting non-sensitive data",
            "Brief system downtime with no data exposure",
            "Isolated access log anomaly"
        ],
        "examples_vi": [
            "Lỗi cấu hình nhỏ ảnh hưởng dữ liệu không nhạy cảm",
            "Hệ thống gián đoạn ngắn không lộ dữ liệu",
            "Log truy cập bất thường đơn lẻ"
        ]
    },
    1: {
        "en": "Medium Risk",
        "vi": "Rủi ro Trung bình",
        "notification": "Internal notification + DPO review",
        "notification_vi": "Thông báo nội bộ + DPO xem xét",
        "timeline": "Within 7 days",
        "examples_en": [
            "Unauthorized access to limited personal data",
            "Email sent to wrong recipient list (small scale)",
            "Temporary exposure of non-sensitive customer data"
        ],
        "examples_vi": [
            "Truy cập trái phép vào dữ liệu cá nhân hạn chế",
            "Email gửi nhầm danh sách người nhận (quy mô nhỏ)",
            "Lộ tạm thời dữ liệu khách hàng không nhạy cảm"
        ]
    },
    2: {
        "en": "High Risk",
        "vi": "Rủi ro Cao",
        "notification": "MPS notification required within 72 hours + Data subject notification",
        "notification_vi": "Báo cáo Bộ Công an trong 72 giờ + Thông báo chủ thể dữ liệu",
        "timeline": "Within 72 hours",
        "examples_en": [
            "Exposure of sensitive personal data (health, financial)",
            "Large-scale data breach affecting 1000+ individuals",
            "Ransomware attack encrypting customer database"
        ],
        "examples_vi": [
            "Lộ dữ liệu cá nhân nhạy cảm (sức khỏe, tài chính)",
            "Vi phạm dữ liệu quy mô lớn ảnh hưởng 1000+ người",
            "Tấn công ransomware mã hóa cơ sở dữ liệu khách hàng"
        ]
    },
    3: {
        "en": "Critical Risk",
        "vi": "Rủi ro Nghiêm trọng",
        "notification": "Immediate MPS notification + Public disclosure + Data subject notification",
        "notification_vi": "Báo cáo Bộ Công an ngay lập tức + Công bố công khai + Thông báo chủ thể",
        "timeline": "Immediate (within 24 hours)",
        "examples_en": [
            "National security implications",
            "Banking/financial system breach",
            "Children's data exposure at scale",
            "Systematic data exfiltration by foreign entities"
        ],
        "examples_vi": [
            "Liên quan đến an ninh quốc gia",
            "Vi phạm hệ thống ngân hàng/tài chính",
            "Lộ dữ liệu trẻ em quy mô lớn",
            "Đánh cắp dữ liệu có hệ thống bởi tổ chức nước ngoài"
        ]
    }
}
```

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_BreachTriage_VI

- **Total Samples**: 10,000 (2,500 per severity level)
- **Difficulty**: VERY HARD (critical safety task)
- **Dataset Composition**:
  - VERY_HARD: 1,000 samples/category (40%) - Borderline severity cases
  - HARD: 1,000 samples/category (40%) - No severity keywords
  - MEDIUM: 350 samples/category (14%) - Subtle severity indicators
  - EASY: 150 samples/category (6%) - Clear severity examples
- **Regional Variations**: North (formal), Central (balanced), South (casual)
- **Sources**:
  - Vietnamese breach reports (anonymized)
  - Security incident scenarios
  - MPS guidelines and case studies
  - International breach databases (translated to Vietnamese)

### English (SECONDARY) - VeriAIDPO_BreachTriage_EN

- **Total Samples**: 6,000 (1,500 per severity level)
- **Difficulty**: MODERATE-HARD (critical safety task)
- **Dataset Composition**:
  - VERY_HARD: 525 samples/category (35%) - Borderline severity cases
  - HARD: 600 samples/category (40%) - No severity keywords
  - MEDIUM: 270 samples/category (18%) - Subtle severity indicators
  - EASY: 105 samples/category (7%) - Clear severity examples
- **Sources**: International breach reports, security incident databases, GDPR breach examples

---

## Template Examples

```python
# Low Risk (Category 0)
"Hệ thống {company} bị lỗi trong 10 phút nhưng không có dữ liệu nào bị truy cập trái phép."
"{company} system error for 10 minutes but no unauthorized data access occurred."

# Medium Risk (Category 1)
"Nhân viên {company} vô tình gửi email chứa 50 địa chỉ khách hàng cho người không liên quan."
"{company} employee accidentally sent email with 50 customer addresses to unrelated person."

# High Risk (Category 2)
"Tin tặc xâm nhập hệ thống {company} và truy cập thông tin thẻ tín dụng của 5,000 khách hàng."
"Hackers breached {company} system and accessed credit card info of 5,000 customers."

# Critical Risk (Category 3)
"Dữ liệu nhạy cảm về an ninh quốc gia bị rò rỉ từ hệ thống của {company}."
"Sensitive national security data leaked from {company} system."
```

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
