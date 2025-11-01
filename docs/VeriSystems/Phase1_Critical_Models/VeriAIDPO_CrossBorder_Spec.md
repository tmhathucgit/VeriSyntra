# VeriAIDPO_CrossBorder - Cross-Border Transfer Classification

**Phase**: 🚨 Phase 1 - CRITICAL  
**Priority**: 🚨 CRITICAL  
**PDPL Reference**: Articles 32-36, Decree 13/2023 Articles 10-11  
**Training Time**: 
- Vietnamese (VI - PRIMARY): 3-4 days
- English (EN - SECONDARY): 3-4 days
- **Total**: 6-8 days (can train in parallel)

**Models to Train**:
- `VeriAIDPO_CrossBorder_VI` (PhoBERT, Vietnamese primary)
- `VeriAIDPO_CrossBorder_EN` (BERT, English secondary)

**Use Cases**: Cross-border transfer wizard, data flow monitoring, MPS approval automation

---

## Categories (5 classes)

```python
CROSS_BORDER_CATEGORIES = {
    0: {
        "en": "Domestic Only",
        "vi": "Chỉ trong nước",
        "mps_approval": "Not required",
        "risk_level": "Low",
        "examples_en": [
            "Data stored on Viettel IDC servers in Hanoi",
            "Processing within Vietnam using VNG Cloud",
            "Local backup to FPT Data Center in HCMC"
        ],
        "examples_vi": [
            "Dữ liệu lưu trữ trên máy chủ Viettel IDC tại Hà Nội",
            "Xử lý trong nước sử dụng VNG Cloud",
            "Sao lưu cục bộ tại FPT Data Center TP.HCM"
        ]
    },
    1: {
        "en": "Approved Country Transfer",
        "vi": "Chuyển sang Quốc gia Được phê duyệt",
        "mps_approval": "General approval (notification only)",
        "risk_level": "Low",
        "examples_en": [
            "Transfer to Singapore data center (ASEAN adequacy)",
            "Backup to approved ASEAN cloud provider",
            "Processing by approved international partner"
        ],
        "examples_vi": [
            "Chuyển sang trung tâm dữ liệu Singapore (ASEAN được phê duyệt)",
            "Sao lưu sang nhà cung cấp cloud ASEAN được phê duyệt",
            "Xử lý bởi đối tác quốc tế được phê duyệt"
        ]
    },
    2: {
        "en": "Requires MPS Approval",
        "vi": "Yêu cầu Phê duyệt Bộ Công an",
        "mps_approval": "Required - DTIA submission",
        "risk_level": "Medium",
        "examples_en": [
            "Transfer to US cloud provider (AWS, Google, Azure)",
            "European data processing center",
            "International vendor without adequacy decision"
        ],
        "examples_vi": [
            "Chuyển sang nhà cung cấp cloud Mỹ (AWS, Google, Azure)",
            "Trung tâm xử lý dữ liệu châu Âu",
            "Nhà cung cấp quốc tế chưa có quyết định tương đương"
        ]
    },
    3: {
        "en": "Prohibited Transfer",
        "vi": "Chuyển bị Cấm",
        "mps_approval": "Not allowed",
        "risk_level": "Critical",
        "examples_en": [
            "Transfer to embargoed country",
            "Sensitive national security data export",
            "Transfer without legal basis or safeguards"
        ],
        "examples_vi": [
            "Chuyển sang quốc gia bị cấm vận",
            "Xuất khẩu dữ liệu nhạy cảm an ninh quốc gia",
            "Chuyển không có cơ sở pháp lý hoặc biện pháp bảo vệ"
        ]
    },
    4: {
        "en": "Unknown/Needs Assessment",
        "vi": "Chưa rõ/Cần Đánh giá",
        "mps_approval": "Assessment required",
        "risk_level": "Medium",
        "examples_en": [
            "New vendor with unclear data location",
            "Third-party service with unknown sub-processors",
            "Cloud service without data residency commitment"
        ],
        "examples_vi": [
            "Nhà cung cấp mới với vị trí dữ liệu không rõ",
            "Dịch vụ bên thứ ba với sub-processor không rõ",
            "Dịch vụ cloud không cam kết data residency"
        ]
    }
}
```

---

## Training Dataset Requirements

### Vietnamese (PRIMARY) - VeriAIDPO_CrossBorder_VI

- **Total Samples**: 10,000 (2,000 per category)
- **Difficulty**: HARD (MPS context, country variations)
- **Dataset Composition**:
  - VERY_HARD: 700 samples/category (35%) - Unclear country adequacy
  - HARD: 800 samples/category (40%) - No location keywords
  - MEDIUM: 350 samples/category (17.5%) - Subtle location hints
  - EASY: 150 samples/category (7.5%) - Clear location examples
- **Regional Variations**: North (formal), Central (balanced), South (casual)
- **Sources**:
  - Vietnamese cloud provider documentation (Viettel, FPT, VNG)
  - International transfer agreements
  - MPS adequacy decisions
  - Data processing agreements (DPAs)

### English (SECONDARY) - VeriAIDPO_CrossBorder_EN

- **Total Samples**: 6,000 (1,200 per category)
- **Difficulty**: MODERATE-HARD (international context)
- **Dataset Composition**:
  - VERY_HARD: 420 samples/category (35%) - Unclear country adequacy
  - HARD: 480 samples/category (40%) - No location keywords
  - MEDIUM: 216 samples/category (18%) - Subtle location hints
  - EASY: 84 samples/category (7%) - Clear location examples
- **Sources**: International data transfer agreements, GDPR adequacy decisions, cloud provider documentation

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
