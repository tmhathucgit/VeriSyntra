# VeriAIDPO - Dataset Size Strategy
## Optimal Sample Counts for Vietnamese & English Models

**Document Version**: 1.0  
**Created**: October 14, 2025  
**Purpose**: Define optimal dataset sizes for all 20 VeriAIDPO models (10 types × 2 languages)

---

## 🎯 Executive Summary

**Question**: Should all models use the same sample count as VeriAIDPO_Principles_VI?

**Answer**: **NO** - Different model types require different sample counts based on:
1. **Number of categories** (more categories = more samples needed)
2. **Task complexity** (harder tasks need more examples)
3. **Ambiguity level** (overlapping categories need more data)

---

## 📊 Current Inconsistency Identified

### **VeriAIDPO_Principles_VI (8 categories)**:
- **Hard Dataset Guide**: 5,000 samples per category = **40,000 total**
- **Implementation Plan**: 500 samples per category = **4,000 total** ❌

### **Other Models in Implementation Plan**:
- VeriAIDPO_LegalBasis (4 categories): 500 per category = **2,000 total**
- VeriAIDPO_BreachTriage (4 categories): 500 per category = **2,000 total**
- VeriAIDPO_CrossBorder (5 categories): 500 per category = **2,500 total**

**Problem**: These sample counts are too small for HARD datasets with ambiguity!

---

## 🧠 Dataset Size Calculation Formula

### **Base Formula**:
```python
SAMPLES_PER_CATEGORY = BASE_SAMPLES × COMPLEXITY_MULTIPLIER × AMBIGUITY_MULTIPLIER

Where:
- BASE_SAMPLES = 1,000 (minimum for production-grade models)
- COMPLEXITY_MULTIPLIER = 1.0 to 2.0 (based on task difficulty)
- AMBIGUITY_MULTIPLIER = 1.0 to 1.5 (for HARD datasets with overlap)
```

### **For Vietnamese Models (PRIMARY)**:
Vietnamese requires MORE samples due to:
- ✅ Regional variations (North, Central, South)
- ✅ Formality levels (legal, formal, business, casual)
- ✅ Less pre-trained data available than English
- ✅ More complex grammar and context-dependency

**Multiplier**: 1.5× base samples

### **For English Models (SECONDARY)**:
English can use FEWER samples due to:
- ✅ More pre-trained knowledge in BERT
- ✅ Simpler grammar structure
- ✅ No regional variations needed

**Multiplier**: 1.0× base samples

---

## 📋 Recommended Sample Counts by Model Type

### **1. VeriAIDPO_Principles (8 categories)**

**Complexity**: MEDIUM (well-defined PDPL principles)  
**Ambiguity**: HIGH (principles often overlap)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 3,000 | **24,000** | 8 categories × high ambiguity × regional variations |
| **English (SECONDARY)** | 1,500 | **12,000** | 8 categories × moderate ambiguity |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 900,   # 30% - Multi-principle overlap
    'HARD': 1,200,      # 40% - No keywords, semantic
    'MEDIUM': 600,      # 20% - Subtle keywords
    'EASY': 300,        # 10% - Clear examples
}
# Total per category: 3,000
# Total dataset: 24,000 samples
```

---

### **2. VeriAIDPO_LegalBasis (4 categories)**

**Complexity**: HIGH (legal nuances between contract/consent/obligation)  
**Ambiguity**: VERY HIGH (legal bases often overlap)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 2,500 | **10,000** | Legal complexity × cultural context × high overlap |
| **English (SECONDARY)** | 1,500 | **6,000** | Legal complexity × moderate overlap |

**Why MORE samples**:
- Legal basis determination is CRITICAL for PDPL compliance
- Categories heavily overlap (e.g., "contract" vs "consent" vs "legal obligation")
- Vietnamese legal language very different from business language
- Must handle government, banking, e-commerce, healthcare contexts

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 1,000,  # 40% - Overlapping legal bases
    'HARD': 1,000,       # 40% - No legal keywords
    'MEDIUM': 350,       # 14% - Subtle legal language
    'EASY': 150,         # 6% - Clear legal basis
}
# Total per category: 2,500
# Total dataset: 10,000 samples
```

---

### **3. VeriAIDPO_BreachTriage (4 categories)**

**Complexity**: VERY HIGH (severity assessment requires judgment)  
**Ambiguity**: VERY HIGH (borderline cases between severity levels)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 2,500 | **10,000** | Critical safety task × high ambiguity × MPS context |
| **English (SECONDARY)** | 1,500 | **6,000** | Critical safety task × moderate ambiguity |

**Why MORE samples**:
- Breach severity is CRITICAL - wrong classification = legal consequences
- Borderline cases very common (Medium vs High risk)
- Must handle technical, legal, and business language
- Vietnamese MPS reporting context unique

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 1,000,  # 40% - Borderline severity cases
    'HARD': 1,000,       # 40% - No severity keywords
    'MEDIUM': 350,       # 14% - Subtle severity indicators
    'EASY': 150,         # 6% - Clear severity examples
}
# Total per category: 2,500
# Total dataset: 10,000 samples
```

---

### **4. VeriAIDPO_CrossBorder (5 categories)**

**Complexity**: HIGH (international regulations, MPS rules)  
**Ambiguity**: HIGH (country/region classifications change)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 2,000 | **10,000** | 5 categories × MPS context × country variations |
| **English (SECONDARY)** | 1,200 | **6,000** | 5 categories × international context |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 700,    # 35% - Unclear country adequacy
    'HARD': 800,         # 40% - No location keywords
    'MEDIUM': 350,       # 17.5% - Subtle location hints
    'EASY': 150,         # 7.5% - Clear location examples
}
# Total per category: 2,000
# Total dataset: 10,000 samples
```

---

### **5. VeriAIDPO_ConsentType (4 categories)**

**Complexity**: MEDIUM (consent types relatively clear)  
**Ambiguity**: MEDIUM (explicit vs implied can overlap)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 1,500 | **6,000** | 4 categories × moderate complexity |
| **English (SECONDARY)** | 1,000 | **4,000** | 4 categories × clear definitions |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 450,    # 30% - Implied vs explicit borderline
    'HARD': 600,         # 40% - No consent keywords
    'MEDIUM': 300,       # 20% - Subtle consent language
    'EASY': 150,         # 10% - Clear consent types
}
# Total per category: 1,500
# Total dataset: 6,000 samples
```

---

### **6. VeriAIDPO_DataSensitivity (4 categories)**

**Complexity**: MEDIUM (PDPL Article 11 defines categories)  
**Ambiguity**: MEDIUM (sensitive vs special category overlap)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 1,500 | **6,000** | 4 categories × cultural sensitivity context |
| **English (SECONDARY)** | 1,000 | **4,000** | 4 categories × standard definitions |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 450,    # 30% - Borderline sensitivity
    'HARD': 600,         # 40% - No sensitivity keywords
    'MEDIUM': 300,       # 20% - Subtle sensitivity hints
    'EASY': 150,         # 10% - Clear data types
}
# Total per category: 1,500
# Total dataset: 6,000 samples
```

---

### **7. VeriAIDPO_DPOTasks (5 categories)**

**Complexity**: LOW (DPO tasks well-defined by PDPL)  
**Ambiguity**: LOW (tasks relatively distinct)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 1,200 | **6,000** | 5 categories × clear task types |
| **English (SECONDARY)** | 800 | **4,000** | 5 categories × standard DPO tasks |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 240,    # 20% - Multi-task scenarios
    'HARD': 480,         # 40% - No task keywords
    'MEDIUM': 300,       # 25% - Subtle task indicators
    'EASY': 180,         # 15% - Clear task examples
}
# Total per category: 1,200
# Total dataset: 6,000 samples
```

---

### **8. VeriAIDPO_RiskLevel (4 categories)**

**Complexity**: HIGH (risk assessment requires judgment)  
**Ambiguity**: HIGH (borderline risk levels)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 2,000 | **8,000** | 4 categories × DPIA triggers × high stakes |
| **English (SECONDARY)** | 1,200 | **4,800** | 4 categories × risk assessment |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 700,    # 35% - Borderline risk levels
    'HARD': 800,         # 40% - No risk keywords
    'MEDIUM': 350,       # 17.5% - Subtle risk indicators
    'EASY': 150,         # 7.5% - Clear risk examples
}
# Total per category: 2,000
# Total dataset: 8,000 samples
```

---

### **9. VeriAIDPO_ComplianceStatus (4 categories)**

**Complexity**: MEDIUM (status based on gap analysis)  
**Ambiguity**: MEDIUM (partial vs non-compliant)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 1,200 | **4,800** | 4 categories × compliance assessment |
| **English (SECONDARY)** | 800 | **3,200** | 4 categories × status classification |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 360,    # 30% - Partial vs non-compliant
    'HARD': 480,         # 40% - No status keywords
    'MEDIUM': 240,       # 20% - Subtle status hints
    'EASY': 120,         # 10% - Clear status examples
}
# Total per category: 1,200
# Total dataset: 4,800 samples
```

---

### **10. VeriAIDPO_Regional (3 categories)**

**Complexity**: LOW (North/Central/South clear)  
**Ambiguity**: LOW (regional patterns distinct)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 1,500 | **4,500** | 3 categories × cultural/linguistic patterns |
| **English (SECONDARY)** | 1,000 | **3,000** | 3 categories × regional context |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 300,    # 20% - Mixed regional patterns
    'HARD': 600,         # 40% - No location keywords
    'MEDIUM': 375,       # 25% - Subtle regional hints
    'EASY': 225,         # 15% - Clear regional examples
}
# Total per category: 1,500
# Total dataset: 4,500 samples
```

---

### **11. VeriAIDPO_Industry (4 categories)**

**Complexity**: LOW (industry types clear)  
**Ambiguity**: LOW (industry patterns distinct)

| Language | Samples/Category | Total Samples | Rationale |
|----------|------------------|---------------|-----------|
| **Vietnamese (PRIMARY)** | 1,200 | **4,800** | 4 categories × industry-specific language |
| **English (SECONDARY)** | 800 | **3,200** | 4 categories × industry context |

**Dataset Composition (Vietnamese)**:
```python
COMPOSITION = {
    'VERY_HARD': 240,    # 20% - Multi-industry scenarios
    'HARD': 480,         # 40% - No industry keywords
    'MEDIUM': 300,       # 25% - Subtle industry hints
    'EASY': 180,         # 15% - Clear industry examples
}
# Total per category: 1,200
# Total dataset: 4,800 samples
```

---

## 📊 Complete Dataset Summary

### **Vietnamese Models (PRIMARY) - Total Samples**

| Model Type | Categories | Samples/Category | Total Samples | Priority |
|------------|-----------|------------------|---------------|----------|
| VeriAIDPO_Principles_VI | 8 | 3,000 | **24,000** | 🚨 CRITICAL |
| VeriAIDPO_LegalBasis_VI | 4 | 2,500 | **10,000** | 🚨 CRITICAL |
| VeriAIDPO_BreachTriage_VI | 4 | 2,500 | **10,000** | 🚨 CRITICAL |
| VeriAIDPO_CrossBorder_VI | 5 | 2,000 | **10,000** | 🚨 CRITICAL |
| VeriAIDPO_ConsentType_VI | 4 | 1,500 | **6,000** | ⚠️ MEDIUM |
| VeriAIDPO_DataSensitivity_VI | 4 | 1,500 | **6,000** | ⚠️ MEDIUM |
| VeriAIDPO_DPOTasks_VI | 5 | 1,200 | **6,000** | ⚠️ MEDIUM |
| VeriAIDPO_RiskLevel_VI | 4 | 2,000 | **8,000** | ⚠️ MEDIUM |
| VeriAIDPO_ComplianceStatus_VI | 4 | 1,200 | **4,800** | 🔵 LOW |
| VeriAIDPO_Regional_VI | 3 | 1,500 | **4,500** | 🔵 LOW |
| VeriAIDPO_Industry_VI | 4 | 1,200 | **4,800** | 🔵 LOW |
| **TOTAL** | **49 categories** | **Avg: 1,827** | **94,100** | - |

---

### **English Models (SECONDARY) - Total Samples**

| Model Type | Categories | Samples/Category | Total Samples | Priority |
|------------|-----------|------------------|---------------|----------|
| VeriAIDPO_Principles_EN | 8 | 1,500 | **12,000** | 🚨 CRITICAL |
| VeriAIDPO_LegalBasis_EN | 4 | 1,500 | **6,000** | 🚨 CRITICAL |
| VeriAIDPO_BreachTriage_EN | 4 | 1,500 | **6,000** | 🚨 CRITICAL |
| VeriAIDPO_CrossBorder_EN | 5 | 1,200 | **6,000** | 🚨 CRITICAL |
| VeriAIDPO_ConsentType_EN | 4 | 1,000 | **4,000** | ⚠️ MEDIUM |
| VeriAIDPO_DataSensitivity_EN | 4 | 1,000 | **4,000** | ⚠️ MEDIUM |
| VeriAIDPO_DPOTasks_EN | 5 | 800 | **4,000** | ⚠️ MEDIUM |
| VeriAIDPO_RiskLevel_EN | 4 | 1,200 | **4,800** | ⚠️ MEDIUM |
| VeriAIDPO_ComplianceStatus_EN | 4 | 800 | **3,200** | 🔵 LOW |
| VeriAIDPO_Regional_EN | 3 | 1,000 | **3,000** | 🔵 LOW |
| VeriAIDPO_Industry_EN | 4 | 800 | **3,200** | 🔵 LOW |
| **TOTAL** | **49 categories** | **Avg: 1,118** | **56,200** | - |

---

## 💡 Key Insights

### **1. Vietnamese Requires 67% MORE Samples**
- Vietnamese total: **94,100 samples**
- English total: **56,200 samples**
- Ratio: **1.67:1**

**Reason**: Vietnamese language complexity + regional variations + less pre-trained data

---

### **2. Critical Models Need 2-3× More Samples**
- **LegalBasis/BreachTriage/CrossBorder**: 10,000 samples each
- **ConsentType/DataSensitivity**: 6,000 samples each
- **ComplianceStatus/Regional/Industry**: 4,500-4,800 samples each

**Reason**: High-stakes decisions require robust training

---

### **3. Total Dataset Generation Effort**

| Metric | Vietnamese | English | Combined |
|--------|-----------|---------|----------|
| **Total Samples** | 94,100 | 56,200 | **150,300** |
| **Generation Time** | 15-20 hours | 10-12 hours | **25-32 hours** |
| **Validation Time** | 8-10 hours | 5-6 hours | **13-16 hours** |
| **Total Effort** | 23-30 hours | 15-18 hours | **38-48 hours** |

---

## 🚀 Implementation Recommendation

### **Phased Dataset Generation**

**Phase 1: Critical Models (Week 1)**
```python
# Generate Vietnamese datasets first (PRIMARY)
VeriAIDPO_LegalBasis_VI:      10,000 samples (4-5 hours)
VeriAIDPO_BreachTriage_VI:    10,000 samples (4-5 hours)
VeriAIDPO_CrossBorder_VI:     10,000 samples (4-5 hours)

# Then English (SECONDARY)
VeriAIDPO_LegalBasis_EN:       6,000 samples (2-3 hours)
VeriAIDPO_BreachTriage_EN:     6,000 samples (2-3 hours)
VeriAIDPO_CrossBorder_EN:      6,000 samples (2-3 hours)

Total: 48,000 samples, 18-24 hours generation
```

**Phase 2: Validation Models (Week 2)**
```python
# Vietnamese
VeriAIDPO_ConsentType_VI:       6,000 samples (3 hours)
VeriAIDPO_DataSensitivity_VI:   6,000 samples (3 hours)
VeriAIDPO_DPOTasks_VI:          6,000 samples (3 hours)
VeriAIDPO_RiskLevel_VI:         8,000 samples (4 hours)

# English
VeriAIDPO_ConsentType_EN:       4,000 samples (2 hours)
VeriAIDPO_DataSensitivity_EN:   4,000 samples (2 hours)
VeriAIDPO_DPOTasks_EN:          4,000 samples (2 hours)
VeriAIDPO_RiskLevel_EN:         4,800 samples (2.5 hours)

Total: 42,800 samples, 21.5 hours generation
```

**Phase 3: Polish Models (Week 3)**
```python
# Vietnamese
VeriAIDPO_ComplianceStatus_VI:  4,800 samples (2.5 hours)
VeriAIDPO_Regional_VI:          4,500 samples (2.5 hours)
VeriAIDPO_Industry_VI:          4,800 samples (2.5 hours)

# English
VeriAIDPO_ComplianceStatus_EN:  3,200 samples (1.5 hours)
VeriAIDPO_Regional_EN:          3,000 samples (1.5 hours)
VeriAIDPO_Industry_EN:          3,200 samples (1.5 hours)

Total: 23,500 samples, 12 hours generation
```

**Phase 0: Principles Model (BEFORE Phase 1)**
```python
# Must complete first to establish baseline
VeriAIDPO_Principles_VI:       24,000 samples (8-10 hours)
VeriAIDPO_Principles_EN:       12,000 samples (4-5 hours) [already exists]

Total: 24,000 new samples, 8-10 hours generation
```

---

## ✅ Final Recommendation

### **Answer to Your Question**:

**NO, models should NOT all use the same sample count as VeriAIDPO_Principles_VI.**

**Recommended Approach**:
1. **VeriAIDPO_Principles_VI**: **24,000 samples** (3,000/category × 8 categories)
   - Baseline model, most categories, high ambiguity
   
2. **Critical Models** (LegalBasis, BreachTriage, CrossBorder): **10,000 samples each**
   - High complexity, high stakes, legal/safety critical
   
3. **Medium Models** (ConsentType, DataSensitivity, DPOTasks, RiskLevel): **6,000-8,000 samples**
   - Moderate complexity, important but not critical
   
4. **Polish Models** (ComplianceStatus, Regional, Industry): **4,500-4,800 samples**
   - Lower complexity, clear distinctions

### **Total Dataset Generation**:
- Vietnamese: **94,100 samples** (PRIMARY)
- English: **56,200 samples** (SECONDARY)
- **Grand Total**: **150,300 samples**
- **Effort**: 38-48 hours dataset generation + validation

This strategy ensures each model has sufficient data for its complexity level while optimizing generation effort.

---

**Document Owner**: VeriSyntra ML Team  
**Last Updated**: October 14, 2025  
**Version**: 1.0  
**Status**: ✅ Ready for Implementation
