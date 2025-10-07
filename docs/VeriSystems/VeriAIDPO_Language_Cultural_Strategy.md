# VeriAIDPO - Language & Cultural Strategy
## Chiến Lược Ngôn Ngữ & Văn Hóa Việt Nam

---

## **🇻🇳 Vietnamese-First Approach / Tiếp Cận Ưu Tiên Tiếng Việt**

### **Core Principle / Nguyên Tắc Cốt Lõi**

**VeriPortal is built FOR Vietnamese users, BY Vietnamese developers**
**VeriPortal được xây dựng CHO người dùng Việt Nam, BỞI nhà phát triển Việt Nam**

---

## **📚 Documentation Structure / Cấu Trúc Tài Liệu**

### **Primary (Vietnamese) / Tài Liệu Chính (Tiếng Việt)**

| Document | Purpose | Audience |
|----------|---------|----------|
| **VeriAIDPO_Huong_Dan_Huan_Luyen_PhoBERT.md** | Hướng dẫn huấn luyện PhoBERT | Nhà phát triển Việt Nam |
| **VeriPortal User Guide (TBD)** | Hướng dẫn sử dụng VeriPortal | Người dùng Việt Nam |
| **PDPL Compliance Wizards** | Trình hướng dẫn tuân thủ PDPL | Doanh nghiệp Việt Nam |

### **Secondary (English) / Tài Liệu Phụ (Tiếng Anh)**

| Document | Purpose | Audience |
|----------|---------|----------|
| **VeriAIDPO_PhoBERT_Training_Guide.md** | PhoBERT training guide | International developers |
| **VeriAIDPO_ML_AWS_Training_Plan.md** | AWS deployment strategy | DevOps/Cloud engineers |
| **VeriAIDPO_VnCoreNLP_Integration.md** | VnCoreNLP technical docs | ML engineers |
| **VeriAIDPO_Google_Colab_Training_Guide.md** | Colab quick-start | International researchers |

---

## **🎨 Language Design Principles / Nguyên Tắc Thiết Kế Ngôn Ngữ**

### **1. User Interface (VeriPortal) / Giao Diện Người Dùng**

```typescript
// PRIMARY: Vietnamese
const veriPortalLanguageConfig = {
  defaultLanguage: 'vi',        // Vietnamese first
  secondaryLanguage: 'en',      // English as fallback
  supportedRegions: [
    'Miền Bắc',   // Northern Vietnam
    'Miền Trung', // Central Vietnam
    'Miền Nam'    // Southern Vietnam
  ]
}
```

**Display Priority**:
1. 🇻🇳 Vietnamese (Tiếng Việt) - **Default**
2. 🇬🇧 English - **Toggle option**

### **2. PDPL Category Labels / Nhãn Danh Mục PDPL**

```python
# PRIMARY: Vietnamese labels (displayed to users)
PDPL_LABELS_VI = {
    0: "Tính hợp pháp, công bằng và minh bạch",
    1: "Hạn chế mục đích",
    2: "Tối thiểu hóa dữ liệu",
    3: "Tính chính xác",
    4: "Hạn chế lưu trữ",
    5: "Tính toàn vẹn và bảo mật",
    6: "Trách nhiệm giải trình",
    7: "Quyền của chủ thể dữ liệu"
}

# SECONDARY: English labels (for international reports)
PDPL_LABELS_EN = {
    0: "Lawfulness, fairness and transparency",
    1: "Purpose limitation",
    2: "Data minimization",
    3: "Accuracy",
    4: "Storage limitation",
    5: "Integrity and confidentiality",
    6: "Accountability",
    7: "Rights of data subjects"
}

# Default to Vietnamese
DEFAULT_LABELS = PDPL_LABELS_VI
```

### **3. AI Model Training / Huấn Luyện Mô Hình AI**

**Training Data Language**: **100% Vietnamese** 🇻🇳

```jsonl
{"text": "Công ty phải bảo vệ dữ liệu cá nhân một cách an toàn", "label": 5}
{"text": "Dữ liệu chỉ được sử dụng cho mục đích đã thông báo", "label": 1}
{"text": "Chỉ thu thập dữ liệu cần thiết cho mục đích cụ thể", "label": 2}
```

**Why Vietnamese training data?**
- ✅ PhoBERT is pre-trained on Vietnamese corpus
- ✅ PDPL 2025 is a Vietnamese law (Nghị định 13/2023)
- ✅ Target users are Vietnamese businesses
- ✅ Legal terminology must match Vietnamese legal language

---

## **🗺️ Regional Diversity / Đa Dạng Vùng Miền**

### **Vietnamese Regional Variations / Biến Thể Vùng Miền Việt Nam**

VeriPortal supports and understands Vietnamese language variations across three regions:

| Region | Example Phrase | PhoBERT Training |
|--------|----------------|------------------|
| **Miền Bắc** (North) | "Công ty cần phải tuân thủ quy định về bảo vệ dữ liệu" | ✅ Included |
| **Miền Trung** (Central) | "Công ty cần tuân thủ quy định bảo vệ dữ liệu" | ✅ Included |
| **Miền Nam** (South) | "Công ty cần tuân thủ quy định về bảo vệ dữ liệu" | ✅ Included |

**Key Differences**:
- **Formality**: Miền Bắc tends to use "cần phải" (need to must), others use "cần" (need)
- **Prepositions**: "về" (about) usage varies by region
- **Vocabulary**: "bảo đảm" (Central) vs "đảm bảo" (North/South) = both mean "ensure"

**VeriPortal Approach**:
- ✅ Train PhoBERT on examples from **all three regions**
- ✅ Ensure model understands regional variations
- ✅ Maintain accuracy across regional dialects
- ✅ Use **standard Vietnamese** for official documents

---

## **💬 User-Facing Text Strategy / Chiến Lược Văn Bản Người Dùng**

### **VeriPortal UI Text Hierarchy**

```typescript
// Example: Compliance Score Display
const complianceScoreDisplay = {
  // PRIMARY (always show)
  vi: {
    title: "Điểm Tuân Thủ",
    description: "Đánh giá mức độ tuân thủ PDPL 2025",
    scoreLabel: "Điểm số"
  },
  
  // SECONDARY (toggle to show)
  en: {
    title: "Compliance Score",
    description: "PDPL 2025 compliance assessment",
    scoreLabel: "Score"
  }
}
```

### **Document Generation Text**

```typescript
// Vietnamese-first document generation
const generatedDocument = {
  language: 'vi',               // Primary: Vietnamese
  legalFramework: 'PDPL 2025',  // Vietnamese law
  complianceStandard: 'Nghị định 13/2023', // Vietnamese decree
  
  // English version (optional, for international partners)
  secondaryLanguage: 'en',
  secondaryLegalReference: 'Decree 13/2023/ND-CP'
}
```

---

## **🎯 Implementation Guidelines / Hướng Dẫn Thực Hiện**

### **For Developers / Dành cho Nhà Phát Triển**

#### **1. Code Comments / Chú Thích Code**

```python
# ✅ GOOD: Vietnamese variable names for Vietnamese domain
danh_muc_tuan_thu = "Tính toàn vẹn và bảo mật"
do_tin_cay = 0.9432

# ⚠️ ACCEPTABLE: English technical terms
def train_phobert(dataset, epochs=5):
    """Huấn luyện PhoBERT trên dữ liệu PDPL Việt Nam"""
    # Technical implementation in English is OK
    model = AutoModelForSequenceClassification.from_pretrained("vinai/phobert-base")
    return model
```

#### **2. User Messages / Thông Báo Người Dùng**

```typescript
// ✅ CORRECT: Vietnamese first, English optional
const messages = {
  success: {
    vi: "Đã lưu thành công!",
    en: "Saved successfully!"
  },
  error: {
    vi: "Đã xảy ra lỗi. Vui lòng thử lại.",
    en: "An error occurred. Please try again."
  }
}

// ❌ INCORRECT: English only
const messages = {
  success: "Saved successfully!",
  error: "An error occurred."
}
```

#### **3. API Responses / Phản Hồi API**

```python
# ✅ GOOD: Bilingual response, Vietnamese primary
def predict_compliance(text):
    result = model.predict(text)
    return {
        "danh_muc_vi": "Tính toàn vẹn và bảo mật",  # PRIMARY
        "category_en": "Integrity and confidentiality",  # SECONDARY
        "do_tin_cay": 0.9432,
        "confidence": 0.9432
    }
```

### **For Content Writers / Dành cho Người Viết Nội Dung**

#### **Documentation Order**

1. **Write Vietnamese version FIRST** (primary audience)
2. **Translate to English** (for international reference)
3. **Never translate technical terms** (PhoBERT, VnCoreNLP, etc.)
4. **Preserve Vietnamese legal terminology** (Nghị định, tuân thủ, etc.)

#### **Tone & Style**

- **Vietnamese**: Formal but friendly (phù hợp văn hóa Việt Nam)
- **English**: Professional and clear (for international developers)

---

## **📊 Language Usage Statistics / Thống Kê Sử Dụng Ngôn Ngữ**

### **Current Documentation Coverage**

| Category | Vietnamese | English | Status |
|----------|-----------|---------|--------|
| **Training Guides** | ✅ VeriAIDPO_Huong_Dan_Huan_Luyen_PhoBERT.md | ✅ VeriAIDPO_PhoBERT_Training_Guide.md | Complete |
| **Technical Docs** | 🔄 In Progress | ✅ VeriAIDPO_ML_AWS_Training_Plan.md | Partial |
| **User Guides** | 🔄 To Be Created | 🔄 To Be Created | Planned |
| **API Docs** | 🔄 To Be Created | ✅ Inline comments | Partial |

### **VeriPortal UI Coverage**

| Module | Vietnamese % | English % |
|--------|-------------|-----------|
| **Onboarding** | 100% | 100% (toggle) |
| **Compliance Wizards** | 100% | 100% (toggle) |
| **Document Generation** | 100% | 100% (toggle) |
| **Business Intelligence** | 100% | 100% (toggle) |
| **System Integration** | 100% | 100% (toggle) |

✅ **All modules support bilingual toggle** (Vietnamese default, English optional)

---

## **🚀 Roadmap / Lộ Trình**

### **Phase 1: Foundation (Complete) ✅**
- ✅ VeriPortal UI with Vietnamese-first design
- ✅ react-i18next integration
- ✅ PhoBERT training guide (Vietnamese + English)
- ✅ Bilingual label system

### **Phase 2: Content Expansion (In Progress) 🔄**
- 🔄 Vietnamese user documentation
- 🔄 Vietnamese API documentation
- 🔄 Regional variation testing (North, Central, South)
- 🔄 Vietnamese cultural compliance examples

### **Phase 3: AI Enhancement (Planned) 📅**
- 📅 PhoBERT fine-tuning on regional variations
- 📅 Vietnamese legal term extraction
- 📅 Automated Vietnamese document generation
- 📅 Vietnamese chatbot (VeriChat)

---

## **✅ Best Practices Checklist / Danh Sách Kiểm Tra**

### **For Vietnamese Users / Người Dùng Việt Nam**

- [ ] Default language is Vietnamese
- [ ] All UI text has Vietnamese translation
- [ ] Legal terms use Vietnamese (Nghị định, tuân thủ, etc.)
- [ ] Regional variations are supported
- [ ] Vietnamese cultural context is respected

### **For International Users / Người Dùng Quốc Tế**

- [ ] English toggle is available
- [ ] Technical documentation has English version
- [ ] API responses include English fields
- [ ] Error messages are bilingual
- [ ] Code comments are in English (for collaboration)

### **For AI Training / Huấn Luyện AI**

- [ ] Training data is 100% Vietnamese
- [ ] Examples cover all three regions (North, Central, South)
- [ ] Legal terminology matches Vietnamese PDPL 2025
- [ ] VnCoreNLP preprocessing for Vietnamese word segmentation
- [ ] Model outputs Vietnamese labels by default

---

## **📖 Summary / Tóm Tắt**

### **English Summary**

VeriPortal follows a **Vietnamese-first, English-secondary** approach:
- **Primary audience**: Vietnamese businesses and users
- **Primary language**: Vietnamese (tiếng Việt)
- **Secondary language**: English (for international reference)
- **Regional support**: North, Central, South Vietnam
- **Cultural alignment**: Respects Vietnamese legal and business culture

### **Tóm Tắt Tiếng Việt**

VeriPortal tuân theo phương pháp **Tiếng Việt là chính, Tiếng Anh là phụ**:
- **Đối tượng chính**: Doanh nghiệp và người dùng Việt Nam
- **Ngôn ngữ chính**: Tiếng Việt
- **Ngôn ngữ phụ**: Tiếng Anh (cho tham khảo quốc tế)
- **Hỗ trợ vùng miền**: Bắc, Trung, Nam Việt Nam
- **Phù hợp văn hóa**: Tôn trọng văn hóa pháp lý và kinh doanh Việt Nam

---

**VeriPortal is built for Vietnam, by Vietnamese developers, for Vietnamese users.** 🇻🇳

**VeriPortal được xây dựng cho Việt Nam, bởi nhà phát triển Việt Nam, cho người dùng Việt Nam.** 🇻🇳

---

*Document Version: 1.0*
*Last Updated: October 5, 2025*
*Owner: VeriSyntra Cultural Alignment Team*
