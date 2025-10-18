# VeriAIDPO - English Dataset Strategy
## Do English Models Need Hard Datasets with Ambiguity?

**Document Version**: 1.0  
**Created**: October 14, 2025  
**Critical Question**: Should English models use the same HARD dataset strategy as Vietnamese models?

---

## 🎯 Quick Answer

**YES, but with MODERATE difficulty instead of VERY HARD.**

**Rationale**:
1. ✅ **English models ARE production-ready** (used by international partners)
2. ✅ **Same real-world ambiguity exists** (principles overlap in any language)
3. ✅ **BERT pre-training helps** but doesn't eliminate need for hard examples
4. ✅ **Investor confidence** requires realistic accuracy (not 100% overfitting)

**BUT**:
- ❌ English doesn't need regional variations (North/Central/South is Vietnamese-specific)
- ❌ English has more pre-trained knowledge in BERT
- ❌ English grammar is less context-dependent than Vietnamese

**Recommendation**: Use **MODERATE-HARD** datasets for English (not VERY HARD like Vietnamese)

---

## 📊 Comparison: Vietnamese vs English Dataset Needs

### **Vietnamese Models (PRIMARY)**

**Challenges Unique to Vietnamese**:
1. **Regional Linguistic Variations**:
   - North (Hanoi): Formal, government-influenced, "đơn vị chúng tôi"
   - Central (Da Nang): Traditional, balanced, "doanh nghiệp chúng tôi"
   - South (HCMC): Casual, business-focused, "công ty mình"

2. **Formality Spectrum**:
   - Legal: "Căn cứ vào quy định pháp luật..." (government documents)
   - Formal: "Doanh nghiệp tuân thủ quy định..." (corporate)
   - Business: "Công ty cam kết..." (SMEs)
   - Casual: "Chúng mình chỉ lấy thông tin cần thiết..." (startups)

3. **Vietnamese-Specific Context**:
   - MPS (Bộ Công an) reporting requirements
   - Vietnamese government terminology
   - ASEAN vs Western business language
   - Vietnamese legal system nuances

4. **Less Pre-trained Data**:
   - PhoBERT trained on Vietnamese Wikipedia + news (limited)
   - No extensive Vietnamese business/legal corpus
   - Fewer PDPL-specific Vietnamese documents

**Difficulty Level Needed**: **VERY HARD** (40% VERY_HARD samples)

---

### **English Models (SECONDARY)**

**Advantages for English**:
1. **No Regional Variations Needed**:
   - English for international partners is standardized
   - No North/Central/South distinction
   - Business English relatively uniform globally

2. **Rich Pre-trained Knowledge**:
   - BERT trained on massive English corpus (Wikipedia, books, web)
   - Extensive English legal/business documents
   - Better understanding of legal terminology out-of-the-box

3. **Simpler Grammar**:
   - Less context-dependent than Vietnamese
   - More explicit subject-verb-object structure
   - Easier to identify legal/compliance concepts

4. **International Standards**:
   - GDPR terminology well-established
   - English compliance language standardized
   - Less cultural context needed

**BUT English Still Needs Hard Datasets**:
1. ✅ **Principle overlap is language-independent**:
   - "We collect data legally for contract purposes" (Lawfulness + Purpose Limitation)
   - "We minimize data and delete after 6 months" (Minimization + Storage Limitation)

2. ✅ **Production-ready requirement**:
   - 100% accuracy on easy templates = overfitting
   - International partners need reliable models

3. ✅ **PDPL context is Vietnamese-specific**:
   - BERT doesn't know PDPL 2025 (new law)
   - MPS, DTIA, Vietnamese legal bases unknown to BERT
   - Need to learn Vietnamese compliance in English

**Difficulty Level Needed**: **MODERATE-HARD** (30% VERY_HARD, 40% HARD)

---

## 🎨 English Dataset Composition Strategy

### **Recommended Composition for English Models**

```python
ENGLISH_DATASET_COMPOSITION = {
    'VERY_HARD': 0.30,    # 30% - Multi-principle overlap (vs 40% for Vietnamese)
    'HARD': 0.40,         # 40% - No keywords, semantic understanding
    'MEDIUM': 0.20,       # 20% - Subtle keywords, some ambiguity
    'EASY': 0.10,         # 10% - Clear examples (baseline learning)
}
```

**Compared to Vietnamese**:
```python
VIETNAMESE_DATASET_COMPOSITION = {
    'VERY_HARD': 0.40,    # 40% - Multi-principle + regional variations
    'HARD': 0.40,         # 40% - No keywords + cultural context
    'MEDIUM': 0.15,       # 15% - Subtle keywords + formality
    'EASY': 0.05,         # 5% - Clear examples (minimal)
}
```

**Key Differences**:
- English: 30% VERY_HARD (vs 40% Vietnamese) - less ambiguity needed
- English: 10% EASY (vs 5% Vietnamese) - more clear examples to anchor learning
- English: 20% MEDIUM (vs 15% Vietnamese) - more intermediate examples

---

## 💡 English Hard Dataset Examples

### **Example 1: Multi-Principle Overlap (VERY_HARD)**

**English** (30% of dataset):
```python
ENGLISH_VERY_HARD = [
    # Lawfulness + Purpose Limitation overlap
    "Based on the service agreement, {company} collects {context} to fulfill delivery obligations, "
    "ensuring this information is used solely for shipping and payment purposes.",
    # PRIMARY: Lawfulness (service agreement = legal basis: contract)
    # SECONDARY: Purpose Limitation (solely for shipping)
    
    # Data Minimization + Storage Limitation overlap
    "{company} requests only {context} necessary for order processing and deletes this data "
    "6 months after transaction completion.",
    # PRIMARY: Storage Limitation (deletes after 6 months)
    # SECONDARY: Data Minimization (only necessary data)
    
    # Accuracy + Transparency overlap
    "{company} discloses the verification process for {context} and allows customers to review "
    "and correct their information at any time.",
    # PRIMARY: Accuracy (review and correct)
    # SECONDARY: Transparency (discloses process)
]
```

**Vietnamese** (40% of dataset):
```python
VIETNAMESE_VERY_HARD = [
    # Same concept but WITH regional variations
    # North (Formal):
    "Căn cứ hợp đồng dịch vụ, đơn vị chúng tôi thu thập {context} để thực hiện nghĩa vụ giao hàng, "
    "đảm bảo thông tin này chỉ sử dụng cho mục đích vận chuyển và thanh toán.",
    
    # South (Casual):
    "Dựa trên thỏa thuận dịch vụ, công ty mình thu thập {context} để ship hàng, "
    "cam kết chỉ dùng cho việc giao hàng và thanh toán thôi nhé.",
    
    # Same principle overlap + regional variation = HARDER
]
```

---

### **Example 2: No-Keyword Samples (HARD)**

**English** (40% of dataset):
```python
ENGLISH_HARD_NO_KEYWORDS = {
    "lawfulness": [
        # No "legal", "lawful", "compliance" keywords
        "{company} collects {context} based on the purchase agreement between parties.",
        "Under the signed terms, {company} may process {context} for service delivery.",
        "The subscription agreement permits {company} to use {context}.",
    ],
    
    "purpose_limitation": [
        # No "purpose", "limitation", "restrict" keywords
        "{company} uses {context} for order fulfillment only, not for other activities.",
        "Information is applied solely to shipping, not shared with third parties.",
        "{company} does not expand the scope of {context} usage beyond stated terms.",
    ],
    
    "data_minimization": [
        # No "minimize", "minimum", "necessary" keywords
        "{company} requests only {context} sufficient for the transaction.",
        "We collect just enough {context} to complete the service, nothing more.",
        "{company} avoids requesting {context} unrelated to the purchase.",
    ],
    
    "accuracy": [
        # No "accurate", "correct", "verify" keywords
        "{company} allows customers to review and update {context} anytime.",
        "If {context} contains errors, customers can request changes.",
        "{company} provides tools to check and modify {context}.",
    ],
}
```

**Key Difference from Vietnamese**:
- English: Standard business language variations
- Vietnamese: Business language + regional dialects + formality levels

---

### **Example 3: Business Context Complexity (HARD)**

**English** (realistic scenarios):
```python
ENGLISH_BUSINESS_CONTEXT = {
    "ecommerce_lawfulness": [
        """When you place an order on {company}.com, we need your phone and address 
        to coordinate delivery. This is required to complete the purchase contract.""",
        # PRIMARY: Lawfulness (contract performance)
    ],
    
    "fintech_purpose_limitation": [
        """E-wallet {company} collects your ID document for identity verification as 
        required by banking regulations. This information is used for KYC only, 
        not shared for marketing purposes.""",
        # PRIMARY: Purpose Limitation (KYC only)
    ],
    
    "healthtech_accuracy": [
        """Health information in {company}'s electronic medical records must be kept 
        current. Doctors can update records after each visit, and patients can request 
        corrections if they find errors.""",
        # PRIMARY: Accuracy
    ],
}
```

**Vietnamese** (same scenarios BUT with cultural context):
```python
VIETNAMESE_BUSINESS_CONTEXT = {
    "ecommerce_lawfulness_north": [
        """Khi quý khách đặt hàng trên {company}.vn, đơn vị chúng tôi cần số điện thoại 
        và địa chỉ để phối hợp giao hàng. Việc này là bắt buộc để hoàn tất hợp đồng mua bán.""",
        # North: "đơn vị chúng tôi", "quý khách", formal
    ],
    
    "ecommerce_lawfulness_south": [
        """Khi bạn đặt hàng trên {company}.vn, chúng mình cần SĐT và địa chỉ để shipper 
        liên hệ giao hàng. Đây là điều kiện để hoàn tất đơn hàng nhé.""",
        # South: "chúng mình", "shipper", "nhé", casual
    ],
}
```

---

## 📋 English Dataset Generation Simplifications

### **What English Datasets DON'T Need**:

**❌ Regional Variations**:
```python
# VIETNAMESE NEEDS (3 regional styles):
VIETNAMESE_REGIONAL = {
    'north': "Đơn vị chúng tôi tuân thủ quy định...",
    'central': "Doanh nghiệp tuân thủ quy định...",
    'south': "Công ty mình tuân thủ quy định...",
}

# ENGLISH DOESN'T NEED:
ENGLISH_STANDARD = "The company complies with regulations..."
# One standard business English version sufficient
```

**❌ Formality Spectrum (Reduced)**:
```python
# VIETNAMESE NEEDS (4 formality levels):
VIETNAMESE_FORMALITY = {
    'legal': "Căn cứ Nghị định 13/2023/NĐ-CP...",
    'formal': "Theo quy định pháp luật hiện hành...",
    'business': "Công ty cam kết tuân thủ luật...",
    'casual': "Mình làm đúng theo luật nhé...",
}

# ENGLISH NEEDS (2 formality levels):
ENGLISH_FORMALITY = {
    'formal': "In accordance with Decree 13/2023...",
    'business': "The company commits to legal compliance...",
}
# No extreme casual needed for international partners
```

**❌ Cultural Business Context**:
```python
# VIETNAMESE NEEDS:
VIETNAMESE_CULTURAL = [
    "Theo văn hóa kinh doanh miền Bắc...",  # Northern business culture
    "Phù hợp với doanh nghiệp miền Nam...",  # Southern business style
    "Tuân thủ quy tắc miền Trung...",        # Central traditional values
]

# ENGLISH DOESN'T NEED:
ENGLISH_INTERNATIONAL = "Following international business standards..."
# Standard international business context
```

---

### **What English Datasets STILL NEED**:

**✅ Multi-Principle Overlap** (30% VERY_HARD):
```python
ENGLISH_OVERLAP = [
    "Based on contract, {company} processes {context} for delivery only and deletes after 2 years.",
    # Lawfulness + Purpose Limitation + Storage Limitation
]
```

**✅ No-Keyword Samples** (40% HARD):
```python
ENGLISH_NO_KEYWORDS = [
    "{company} collects {context} under the signed agreement.",  # Lawfulness (no "legal")
    "Data is used for shipping only, not other purposes.",       # Purpose (no "limitation")
    "{company} requests just enough {context} for the service.", # Minimization (no "minimize")
]
```

**✅ PDPL-Specific Context**:
```python
ENGLISH_PDPL_CONTEXT = [
    "Transfer to Singapore data center requires MPS notification under PDPL 2025.",
    "Cross-border data flow to AWS must comply with Decree 13/2023 Article 10.",
    "DTIA submission required for transfers outside ASEAN adequacy countries.",
]
# BERT doesn't know PDPL 2025, MPS, DTIA - must learn from dataset
```

**✅ Realistic Business Scenarios**:
```python
ENGLISH_REALISTIC = [
    "E-commerce platform {company} collects shipping address to fulfill customer orders.",
    "Fintech app requires ID verification for banking compliance, used for KYC only.",
    "Healthcare system allows patients to review and correct medical records.",
]
```

---

## 🎯 Recommended English Dataset Composition by Model

### **High-Stakes Models** (LegalBasis, BreachTriage, CrossBorder, RiskLevel)

```python
ENGLISH_HIGH_STAKES_COMPOSITION = {
    'VERY_HARD': 0.35,    # 35% - More overlap for critical decisions
    'HARD': 0.40,         # 40% - No keywords
    'MEDIUM': 0.18,       # 18% - Subtle keywords
    'EASY': 0.07,         # 7% - Clear examples
}

# Example for VeriAIDPO_LegalBasis_EN (6,000 samples):
# VERY_HARD: 2,100 samples (overlapping legal bases)
# HARD: 2,400 samples (no legal keywords)
# MEDIUM: 1,080 samples (subtle legal language)
# EASY: 420 samples (clear legal basis examples)
```

**Why More VERY_HARD**:
- Legal basis determination is critical
- Contract vs Consent vs Legal Obligation often overlap
- Wrong classification = compliance violation

---

### **Medium-Stakes Models** (ConsentType, DataSensitivity, DPOTasks)

```python
ENGLISH_MEDIUM_STAKES_COMPOSITION = {
    'VERY_HARD': 0.30,    # 30% - Standard overlap
    'HARD': 0.40,         # 40% - No keywords
    'MEDIUM': 0.20,       # 20% - Subtle keywords
    'EASY': 0.10,         # 10% - Clear examples
}

# Example for VeriAIDPO_ConsentType_EN (4,000 samples):
# VERY_HARD: 1,200 samples (explicit vs implied borderline)
# HARD: 1,600 samples (no consent keywords)
# MEDIUM: 800 samples (subtle consent language)
# EASY: 400 samples (clear consent types)
```

---

### **Low-Stakes Models** (ComplianceStatus, Regional, Industry)

```python
ENGLISH_LOW_STAKES_COMPOSITION = {
    'VERY_HARD': 0.25,    # 25% - Less overlap
    'HARD': 0.40,         # 40% - No keywords
    'MEDIUM': 0.22,       # 22% - Subtle keywords
    'EASY': 0.13,         # 13% - More clear examples
}

# Example for VeriAIDPO_Industry_EN (3,200 samples):
# VERY_HARD: 800 samples (multi-industry scenarios)
# HARD: 1,280 samples (no industry keywords)
# MEDIUM: 704 samples (subtle industry hints)
# EASY: 416 samples (clear industry examples)
```

---

## 📊 English vs Vietnamese Dataset Comparison

| Aspect | Vietnamese | English | Difference |
|--------|-----------|---------|------------|
| **Sample Count** | 94,100 | 56,200 | 67% more for Vietnamese |
| **VERY_HARD %** | 35-40% | 25-35% | 5-10% more for Vietnamese |
| **Regional Variations** | 3 (North/Central/South) | 0 | Vietnamese only |
| **Formality Levels** | 4 (Legal/Formal/Business/Casual) | 2 (Formal/Business) | 2× more for Vietnamese |
| **Cultural Context** | High (Vietnamese business) | Low (International standard) | Vietnamese-specific |
| **Pre-trained Knowledge** | Limited (PhoBERT) | Extensive (BERT) | Advantage: English |
| **Expected Accuracy** | 78-88% | 82-90% | 4-5% higher for English |

---

## ✅ Final Recommendation: English Dataset Strategy

### **YES, Use Hard Datasets for English Models**

**Reasons**:
1. ✅ Production-ready requirement (not just demo models)
2. ✅ Real-world ambiguity exists regardless of language
3. ✅ PDPL 2025 context unknown to BERT (must learn from dataset)
4. ✅ Investor confidence needs realistic accuracy metrics

---

### **BUT Use MODERATE-HARD (Not VERY HARD)**

**Simplifications for English**:
1. ❌ No regional variations needed
2. ❌ Fewer formality levels (2 vs 4)
3. ❌ No Vietnamese cultural context
4. ✅ More clear examples to leverage BERT's pre-training

**Composition**:
- High-stakes: 35% VERY_HARD, 40% HARD, 18% MEDIUM, 7% EASY
- Medium-stakes: 30% VERY_HARD, 40% HARD, 20% MEDIUM, 10% EASY
- Low-stakes: 25% VERY_HARD, 40% HARD, 22% MEDIUM, 13% EASY

---

### **Expected Performance**

| Model Type | Vietnamese Target | English Target | Difference |
|------------|------------------|----------------|------------|
| **Training Accuracy** | 82-88% | 85-90% | +3-5% English |
| **Validation Accuracy** | 78-85% | 82-88% | +4-5% English |
| **Test Accuracy** | 75-82% | 80-87% | +5% English |
| **Production Accuracy** | 75-82% | 80-87% | +5% English |

**Why English Higher**:
- BERT's pre-trained knowledge helps
- Simpler grammar structure
- No regional variation complexity

**But Still Realistic**:
- Not 100% (avoids overfitting)
- Handles real ambiguity
- Production-ready for international partners

---

## 🏢 Company Name Strategy for English Datasets

### **Overview**

English datasets also use the **Dynamic Company Registry** approach, but with a **dual-company strategy** reflecting Vietnam's business reality:

1. **Vietnamese Companies** (60%): International branches of Vietnamese brands
   - Shopee Vietnam, Grab Vietnam, Viettel Telecom
   - VCB Bank, Techcombank, MoMo Wallet
   - Used in English documents for Vietnamese operations

2. **International Companies** (40%): Global brands operating in Vietnam
   - Google, Facebook, Amazon, Microsoft
   - Uber, Netflix, Spotify
   - Used when referencing international compliance standards

### **Why This Dual Approach?**

**Vietnamese Business Context**:
- Many Vietnamese companies create English-language privacy policies
- International partners need compliance docs in English
- B2B contracts often in English (Shopee.com, Grab International)

**Examples**:
```
Vietnamese context (60%):
"Shopee Vietnam collects personal data in accordance with PDPL 2025..."
"Vietcombank provides cross-border payment services compliant with..."

International context (40%):
"Google Analytics processes data as outlined in our privacy policy..."
"Amazon Web Services stores customer data in compliance with..."
```

### **Company Selection by Industry**

Similar to Vietnamese datasets, English samples use context-aware company selection:

| Industry | Vietnamese Companies (60%) | International Companies (40%) |
|----------|---------------------------|------------------------------|
| **Technology** | Shopee, Grab, VNG, FPT, Viettel | Google, Facebook, Amazon, Microsoft |
| **Finance** | Vietcombank, Techcombank, MoMo, ZaloPay | PayPal, Stripe, Visa, Mastercard |
| **E-commerce** | Tiki, Sendo, Shopee Vietnam | Amazon, eBay, Alibaba |
| **Transportation** | Grab Vietnam, Gojek Vietnam | Uber, Lyft (legacy references) |
| **Healthcare** | Vinmec International, FV Hospital | Johnson & Johnson, Pfizer |
| **Education** | ELSA Speak, Topica Edtech | Coursera, Udemy, Khan Academy |

### **Normalization Pipeline**

Just like Vietnamese datasets, English samples are normalized to `[COMPANY]` token:

```python
# Step 1: GENERATION - Use real companies
sample = {
    'text': "Shopee Vietnam collects customer ID for KYC verification...",
    'company': 'Shopee Vietnam',
    'industry': 'e-commerce'
}

# Step 2: NORMALIZATION - Replace with token
normalized_text = "[COMPANY] collects customer ID for KYC verification..."

# Step 3: TRAINING - Model learns company-agnostic patterns
# Model works with ANY company (Vietnamese or international)
```

### **Formality Levels in English (2 Levels)**

Unlike Vietnamese (4 levels), English maintains **professional consistency**:

#### **Formal** (50% of samples):
```
"The Company collects personal data in accordance with applicable regulations."
"Our organization implements appropriate security measures as required by law."
"We process customer information pursuant to contractual obligations."
```

#### **Business** (50% of samples):
```
"We collect your personal data to provide our services."
"The company commits to protecting your information."
"Your data is processed only for specified purposes."
```

**Note**: No "Legal" level (no government decree style) or "Casual" level (professional standard maintained)

### **Sample Distribution**

```python
ENGLISH_COMPANIES_VIETNAMESE = [
    'Shopee Vietnam', 'Grab Vietnam', 'Viettel', 'VNG Corporation',
    'FPT Software', 'Tiki.vn', 'Sendo', 'Lazada Vietnam',
    'Vietcombank', 'Techcombank', 'BIDV', 'ACB Bank',
    'MoMo Wallet', 'ZaloPay', 'VNPay', 'ShopeePay',
    'Vinmec International Hospital', 'FV Hospital',
    'ELSA Speak', 'Topica Edtech', 'CoderSchool'
]

ENGLISH_COMPANIES_INTERNATIONAL = [
    'Google', 'Facebook', 'Amazon', 'Microsoft',
    'Apple', 'Netflix', 'Spotify', 'Zoom',
    'PayPal', 'Stripe', 'Visa', 'Mastercard',
    'Uber', 'Airbnb', 'Booking.com',
    'Coursera', 'Udemy', 'Khan Academy',
    'Johnson & Johnson', 'Pfizer'
]

def select_english_company(template_text, context='vietnamese'):
    """
    Select company based on context
    Default: Vietnamese companies (60% of samples)
    """
    if context == 'international' or random.random() < 0.4:
        return random.choice(ENGLISH_COMPANIES_INTERNATIONAL)
    else:
        return random.choice(ENGLISH_COMPANIES_VIETNAMESE)
```

### **Benefits of Dual-Company Strategy**

✅ **Realistic Training Data**: Reflects actual English compliance docs in Vietnam  
✅ **International Compatibility**: Works with global partners  
✅ **Zero Retraining**: Add any company (Vietnamese or international) via registry  
✅ **Production Ready**: Handles B2B, B2C, domestic, and cross-border scenarios  

### **Implementation Reference**

For complete code and architecture:
- **`VeriAIDPO_Dynamic_Company_Registry_Implementation.md`** - Full implementation plan
- **`VeriAIDPO_Google_Colab_Training_Guide.md`** - Training with normalization
- **`config/company_registry.json`** - Database includes English company names

### **Dataset Generation Example**

```python
# Financial context → Select bank
if 'payment' in template or 'transaction' in template:
    company = select_english_company(template, context='vietnamese')
    # 60% chance: "Vietcombank"
    # 40% chance: "PayPal"

# E-commerce context → Select platform
elif 'order' in template or 'purchase' in template:
    company = select_english_company(template, context='vietnamese')
    # 60% chance: "Shopee Vietnam"
    # 40% chance: "Amazon"

# Tech context → Select tech company
else:
    company = select_english_company(template, context='international')
    # Mix of Vietnamese tech (VNG, FPT) and international (Google, Microsoft)
```

---

## 🚀 Implementation Summary

### **English Dataset Generation Effort**

| Model Type | Samples | VERY_HARD | HARD | MEDIUM | EASY | Time |
|------------|---------|-----------|------|--------|------|------|
| Principles_EN | 12,000 | 3,600 | 4,800 | 2,400 | 1,200 | 4-5h |
| LegalBasis_EN | 6,000 | 2,100 | 2,400 | 1,080 | 420 | 2-3h |
| BreachTriage_EN | 6,000 | 2,100 | 2,400 | 1,080 | 420 | 2-3h |
| CrossBorder_EN | 6,000 | 2,100 | 2,400 | 1,080 | 420 | 2-3h |
| ConsentType_EN | 4,000 | 1,200 | 1,600 | 800 | 400 | 2h |
| DataSensitivity_EN | 4,000 | 1,200 | 1,600 | 800 | 400 | 2h |
| DPOTasks_EN | 4,000 | 1,200 | 1,600 | 800 | 400 | 2h |
| RiskLevel_EN | 4,800 | 1,680 | 1,920 | 864 | 336 | 2.5h |
| ComplianceStatus_EN | 3,200 | 800 | 1,280 | 704 | 416 | 1.5h |
| Regional_EN | 3,000 | 750 | 1,200 | 660 | 390 | 1.5h |
| Industry_EN | 3,200 | 800 | 1,280 | 704 | 416 | 1.5h |
| **TOTAL** | **56,200** | **17,530** | **22,480** | **11,172** | **5,018** | **23-28h** |

---

## 🎯 Conclusion

### **Direct Answer**:

**YES, English models need hard datasets with ambiguity.**

**BUT**:
- Use **MODERATE-HARD** difficulty (not VERY HARD like Vietnamese)
- **30-35% VERY_HARD** samples (vs 40% for Vietnamese)
- **No regional variations** (vs 3 regions for Vietnamese)
- **2 formality levels** (vs 4 for Vietnamese)
- **Higher expected accuracy** (82-90% vs 78-88% Vietnamese)

**Total Effort**:
- Vietnamese: 94,100 samples, 23-30 hours
- English: 56,200 samples, 23-28 hours
- **Same effort, different approaches**

This ensures both Vietnamese (PRIMARY) and English (SECONDARY) models are **production-ready** for real-world use while optimizing for each language's unique characteristics.

---

**Document Owner**: VeriSyntra ML Team  
**Last Updated**: October 14, 2025  
**Version**: 2.0 (Dynamic Company Registry Integration)  
**Status**: ✅ Ready for Implementation  
**Changes**: Added dual-company strategy (Vietnamese 60% + International 40%) with normalization pipeline

