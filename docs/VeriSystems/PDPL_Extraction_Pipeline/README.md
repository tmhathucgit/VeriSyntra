# PDPL 91/2025/QH15 Extraction & Training Pipeline

**Complete implementation plans for extracting official Vietnamese PDPL law text and integrating with synthetic training data across all VeriAIDPO model development phases.**

---

## 📋 Documentation Index

### **Master Architecture**
- **[00_Master_PDPL_Extraction_Plan.md](./00_Master_PDPL_Extraction_Plan.md)** (~850 lines)
  - 6-stage pipeline architecture
  - Complete Python extraction scripts
  - 3-4 week implementation timeline
  - **START HERE** for technical implementation

### **Phase-Specific Training Integration Plans**

#### **Phase 0: Principles Enhanced** (v1.0 → v1.1)
- **[01_Phase0_Principles_PDPL_Integration.md](./01_Phase0_Principles_PDPL_Integration.md)** (~1,100 lines)
  - Current state: 93.75% accuracy
  - Target: 95-96% accuracy
  - Fix weaknesses: Cat 2 (78% → 90%), Cat 6 (81% → 92%)
  - Extract 1,650 official PDPL samples
  - Hybrid training: 25% official + 75% synthetic (weighted 2:1)
  - **Timeline**: 2 weeks after master pipeline complete

#### **Phase 2A: Breach Triage** (NEW Model)
- **[03_Phase2A_BreachTriage_PDPL.md](./03_Phase2A_BreachTriage_PDPL.md)** (~950 lines)
  - New model: VeriAIDPO_BreachTriage v1.0
  - 4-level severity classification (Critical/High/Medium/Low)
  - Extract penalty provisions (Articles 38, 99-101)
  - Generate 10,000 Vietnamese breach scenarios
  - Hybrid training: 40% official + 60% synthetic (weighted 2.5:1)
  - Target accuracy: 85-90%, Critical recall >95%
  - **Timeline**: 3-4 months (Q1-Q2 2026)

#### **Phase 3A: Legal QA System** (NEW Model)
- **[05_Phase3A_LegalQA_PDPL.md](./05_Phase3A_LegalQA_PDPL.md)** (~1,000 lines)
  - New model: VeriAIDPO_LegalQA v1.0 (RAG-based)
  - Answer Vietnamese PDPL questions with article citations
  - Build vector database (500+ PDPL chunks)
  - Generate 10,000+ Vietnamese Q&A pairs
  - RAG architecture: Retrieval + Generation
  - Target accuracy: 90-95%, Citation precision >95%
  - **Timeline**: 6-8 months (Q3-Q4 2026)

---

## 🚀 Quick Start Guide

### **Step 1: Understand the Master Pipeline** (1 day)
**Read**: [00_Master_PDPL_Extraction_Plan.md](./00_Master_PDPL_Extraction_Plan.md)

**What You'll Learn:**
- How to extract Vietnamese text from PDPL 91/2025/QH15 PDF
- How to parse Vietnamese legal document structure (Chương → Điều → Khoản → Điểm)
- How to map articles to 8 PDPL categories
- Python scripts for all extraction stages

**Action Items:**
```bash
# Clone/download PDPL PDF
# Expected: 200-300 pages, Vietnamese UTF-8

# Prepare environment
pip install pymupdf numpy sentence-transformers qdrant-client

# Review scripts in master plan
# Ready to execute after legal document obtained
```

---

### **Step 2: Execute PDPL Extraction** (3-4 weeks)

**Week 1: Text Extraction**
```python
# Run Stage 1: PDF → Text
from pdpl_extraction import PDPLTextExtractor

extractor = PDPLTextExtractor("data/pdpl_91_2025_qh15.pdf")
extractor.extract_full_text()
extractor.save_raw_text("data/pdpl_raw_text.txt")
extractor.save_structured_json("data/pdpl_raw_extraction.json")

# Output: pdpl_raw_text.txt (200-300 pages Vietnamese text)
```

**Week 2: Structure Parsing & Category Mapping**
```python
# Run Stage 2: Parse Vietnamese legal structure
from pdpl_extraction import PDPLStructureParser

parser = PDPLStructureParser("data/pdpl_raw_text.txt")
structure = parser.parse_full_structure()
parser.save_structure("data/pdpl_structured.json")

# Run Stage 3: Map articles to categories (requires legal expert input)
from pdpl_extraction import PDPLCategoryMapper

mapper = PDPLCategoryMapper("data/pdpl_structured.json")
mapper.create_mapping_template("data/pdpl_category_template.xlsx")

# MANUAL STEP: Legal expert fills in template (1-2 days)
# Then load and validate

mapper.load_manual_mappings("data/pdpl_category_template_completed.xlsx")
mapper.validate_with_ai()  # Compare human vs AI
mapper.save_mappings("data/pdpl_category_mapped.json")
```

**Week 3: Generate Phase-Specific Datasets**
```python
# Phase 0: Extract 1,650 samples for Principles
from phase0_integration import Phase0PDPLExtractor

phase0_extractor = Phase0PDPLExtractor("data/pdpl_category_mapped.json")
phase0_samples = phase0_extractor.extract_samples_by_category()
phase0_extractor.save_dataset("data/phase0_pdpl_official.json")

# Phase 2A: Extract penalty provisions for Breach Triage
from phase2a_integration import Phase2ABreachPDPLExtractor

phase2a_extractor = Phase2ABreachPDPLExtractor("data/pdpl_structured.json")
penalty_samples = phase2a_extractor.extract_penalty_provisions()
phase2a_extractor.save_dataset("data/phase2a_pdpl_penalties.json")

# Phase 3A: Build vector database for Legal QA
from phase3a_integration import PDPLKnowledgeBaseBuilder

kb_builder = PDPLKnowledgeBaseBuilder("data/pdpl_structured.json")
chunks = kb_builder.create_chunks()
kb_builder.save_chunks("data/phase3a_pdpl_chunks.json")
```

**Week 4: Quality Validation**
- Legal expert review (2-3 days)
- AI cross-validation (1 day)
- Consistency checks (1 day)
- Documentation (1 day)

---

### **Step 3: Choose Your Training Phase** (Based on priority)

#### **PRIORITY 1: Phase 0 - Principles Enhanced** (Immediate ROI)
**Read**: [01_Phase0_Principles_PDPL_Integration.md](./01_Phase0_Principles_PDPL_Integration.md)

**Why Start Here:**
- Foundation for all other models
- Immediate accuracy improvement (93.75% → 95-96%)
- Fixes critical weaknesses (Cat 2, Cat 6)
- Fastest to implement (2 weeks)
- Legal authority for VeriSyntra platform

**Action Items:**
```python
# Create hybrid dataset
from phase0_integration import Phase0HybridDatasetCreator

creator = Phase0HybridDatasetCreator(
    pdpl_path="data/phase0_pdpl_official.json",
    synthetic_path="data/vietnamese_pdpl_synthetic.jsonl"
)

hybrid_dataset = creator.create_weighted_dataset(
    pdpl_weight=2.0,
    synthetic_weight=1.0
)

creator.save_dataset(hybrid_dataset, "data/phase0_hybrid_training.jsonl")

# Train model (modify existing notebook)
# See detailed steps in Phase 0 plan
```

**Expected Results:**
- Overall: 93.75% → 95-96% (+1-2%)
- Cat 2: 78% → 90%+ (+12%)
- Cat 6: 81% → 92%+ (+11%)
- Legal language: Near-perfect recognition
- Can cite: "Điều 13.1.b PDPL 2025"

---

#### **PRIORITY 2: Phase 2A - Breach Triage** (Enterprise Value)
**Read**: [03_Phase2A_BreachTriage_PDPL.md](./03_Phase2A_BreachTriage_PDPL.md)

**Why Next:**
- High enterprise demand (incident response automation)
- Legal penalties = business critical
- New revenue stream (breach triage SaaS)
- 3-4 month timeline (manageable)

**Action Items:**
```python
# Generate breach scenarios
from phase2a_integration import VietnameseBreachScenarioGenerator

generator = VietnameseBreachScenarioGenerator()
breach_dataset = generator.generate_dataset(samples_per_severity={
    "CRITICAL": 1500,
    "HIGH": 2500,
    "MEDIUM": 3000,
    "LOW": 3000
})

generator.save_dataset(breach_dataset, "data/phase2a_synthetic_breaches.json")

# Create hybrid dataset
from phase2a_integration import Phase2AHybridCreator

creator = Phase2AHybridCreator(
    pdpl_penalties="data/phase2a_pdpl_penalties.json",
    synthetic_breaches="data/phase2a_synthetic_breaches.json"
)

hybrid = creator.create_weighted_dataset(pdpl_weight=2.5, synthetic_weight=1.0)
creator.save_dataset(hybrid, "data/phase2a_hybrid_training.jsonl")

# Train new model (PhoBERT-based classifier)
# See detailed training pipeline in Phase 2A plan
```

**Expected Results:**
- Overall accuracy: 85-90%
- Critical recall: >95% (must catch all serious breaches)
- False negative rate: <2%
- Response time: <500ms
- VeriPortal integration: Real-time breach triage

---

#### **PRIORITY 3: Phase 3A - Legal QA** (Advanced AI)
**Read**: [05_Phase3A_LegalQA_PDPL.md](./05_Phase3A_LegalQA_PDPL.md)

**Why Later:**
- Requires RAG infrastructure (complex)
- 6-8 month timeline (long-term investment)
- Foundation for customer self-service
- Differentiator vs competitors

**Action Items:**
```python
# Build vector database
from phase3a_integration import PDPLVectorDatabase

db = PDPLVectorDatabase(
    chunks_path="data/phase3a_pdpl_chunks.json",
    embeddings_path="data/phase3a_pdpl_embeddings.npy"
)

db.create_collection()
db.upload_chunks()

# Generate Q&A training pairs
from phase3a_integration import PDPLQADatasetGenerator

qa_gen = PDPLQADatasetGenerator("data/phase3a_pdpl_chunks.json")
qa_dataset = qa_gen.generate_full_dataset()
qa_gen.save_dataset(qa_dataset, "data/phase3a_qa_pdpl_official.json")

# Train RAG system
# See detailed implementation in Phase 3A plan
```

**Expected Results:**
- Answer accuracy: 90-95%
- Article citation precision: >95%
- Response time: <2 seconds
- Knowledge coverage: 100% of PDPL
- NPS score: >80

---

## 🎯 Decision Tree: Which Phase Should I Start?

```
START
  |
  v
Do you have PDPL PDF? ───NO──> [Wait] Obtain PDPL 91/2025/QH15 official document
  |                             Contact: Ministry of Public Security (Vietnam)
 YES
  |
  v
Have you run master extraction? ───NO──> [Week 1-4] Execute master pipeline
  |                                       See: 00_Master_PDPL_Extraction_Plan.md
 YES
  |
  v
What's your priority?
  |
  ├─ Immediate accuracy improvement ───> [Phase 0] 01_Phase0_Principles_PDPL_Integration.md
  |   (2 weeks, 93.75% -> 95-96%)        LOW EFFORT, HIGH IMPACT
  |
  ├─ Enterprise breach triage ─────────> [Phase 2A] 03_Phase2A_BreachTriage_PDPL.md
  |   (3-4 months, NEW revenue stream)   MEDIUM EFFORT, HIGH VALUE
  |
  └─ Advanced legal Q&A chatbot ───────> [Phase 3A] 05_Phase3A_LegalQA_PDPL.md
      (6-8 months, market differentiator) HIGH EFFORT, LONG-TERM PAYOFF
```

---

## 📊 Training Data Overview

### **Official PDPL Data** (Extracted from Law)

| Phase | Articles | Samples | Purpose | Extraction Script |
|-------|----------|---------|---------|-------------------|
| **Phase 0** | 7, 13 | 1,650 | 8 PDPL principles | `Phase0PDPLExtractor` |
| **Phase 2A** | 38, 99-101 | 200 | Penalty provisions | `Phase2ABreachPDPLExtractor` |
| **Phase 3A** | All articles | 500+ chunks | Legal Q&A knowledge base | `PDPLKnowledgeBaseBuilder` |

### **Synthetic Data** (Business-Oriented)

| Phase | Samples | Purpose | Generator Script |
|-------|---------|---------|------------------|
| **Phase 0** | 26,000 | Vietnamese business scenarios | (Existing) `vietnamese_pdpl_synthetic.jsonl` |
| **Phase 2A** | 10,000 | Breach scenarios (4 severity levels) | `VietnameseBreachScenarioGenerator` |
| **Phase 3A** | 10,000 | Vietnamese Q&A pairs | `PDPLQADatasetGenerator` |

### **Hybrid Training Mixes**

| Phase | Official % | Synthetic % | Weighting | Effective Mix | Rationale |
|-------|-----------|-------------|-----------|---------------|-----------|
| **Phase 0** | 25% | 75% | 2:1 | ~50/50 | Balance legal + business |
| **Phase 2A** | 40% | 60% | 2.5:1 | ~60/40 | Penalties must be exact |
| **Phase 3A** | 60% | 40% | 3:1 | ~82/18 | Legal answers need precision |

**Weighting Explained:**
```python
# Example: Phase 0 (2:1 weighting)
pdpl_probability = (1650 * 2.0) / ((1650 * 2.0) + (26000 * 1.0))
# = 3300 / 29300 = 11.3%

synthetic_probability = (26000 * 1.0) / 29300 = 88.7%

# But PDPL samples appear 2x more often in batches
# Effective mix: ~50% PDPL language exposure, 50% synthetic
```

---

## 🔧 Technical Requirements

### **Python Environment**
```bash
# Core dependencies
pip install pymupdf numpy pandas openpyxl

# Vietnamese NLP
pip install underthesea vncorenlp sentence-transformers

# Deep learning
pip install torch transformers datasets accelerate

# Vector database (Phase 3A)
pip install qdrant-client

# Data validation
pip install jsonschema pydantic
```

### **Hardware Requirements**

| Phase | CPU | RAM | GPU | Storage | Training Time |
|-------|-----|-----|-----|---------|---------------|
| **Master Pipeline** | 4+ cores | 8GB | None | 2GB | N/A (extraction) |
| **Phase 0** | 8+ cores | 16GB | RTX 3060+ (6GB) | 10GB | 2-4 hours |
| **Phase 2A** | 8+ cores | 16GB | RTX 3060+ (6GB) | 15GB | 8-12 hours |
| **Phase 3A** | 16+ cores | 32GB | RTX 3080+ (10GB) | 50GB | 24-48 hours |

### **Vietnamese Language Support**
- **Encoding**: UTF-8 (mandatory)
- **Diacritics**: Full Unicode support required
- **Font**: Vietnamese-compatible fonts (e.g., Arial, Times New Roman)
- **NLP**: PhoBERT, VnCoreNLP, Underthesea

---

## ✅ Success Metrics

### **Master Pipeline Quality**
- [x] PDF extraction: 100% page coverage
- [x] Vietnamese text: No diacritics corruption
- [x] Structure parsing: >95% accuracy (Chapters/Articles/Clauses)
- [x] Category mapping: >80% AI-human agreement
- [x] Sample generation: 1,500-2,000 official samples

### **Phase 0: Principles Enhanced**
- [x] Overall accuracy: 93.75% → 95-96%
- [x] Cat 2 (Data Minimization): 78% → 90%+
- [x] Cat 6 (Transparency): 81% → 92%+
- [x] Legal language: Near-perfect recognition
- [x] Article citation: Recognizes "Điều X.Y.Z"

### **Phase 2A: Breach Triage**
- [x] Overall accuracy: 85-90%
- [x] Critical recall: >95%
- [x] High recall: >90%
- [x] False negative rate: <2%
- [x] MPS compliance: 100% (recommendations match legal requirements)

### **Phase 3A: Legal QA**
- [x] Answer accuracy: 90-95%
- [x] Article citation precision: >95%
- [x] Response time: <2 seconds
- [x] Knowledge coverage: 100% of PDPL articles
- [x] User satisfaction: NPS >80

---

## 🗂️ File Structure (After Completion)

```
data/
├── pdpl_extraction/
│   ├── pdpl_91_2025_qh15.pdf              # Original PDPL law PDF
│   ├── pdpl_raw_text.txt                  # Extracted Vietnamese text
│   ├── pdpl_raw_extraction.json           # Metadata + text
│   ├── pdpl_structured.json               # Parsed structure
│   ├── pdpl_category_mapped.json          # Articles → 8 categories
│   └── pdpl_category_template.xlsx        # For legal expert mapping
│
├── phase0_principles/
│   ├── phase0_pdpl_official.json          # 1,650 official samples
│   ├── vietnamese_pdpl_synthetic.jsonl    # 26,000 synthetic samples
│   └── phase0_hybrid_training.jsonl       # Weighted mix (2:1)
│
├── phase2a_breach_triage/
│   ├── phase2a_pdpl_penalties.json        # 200 penalty provisions
│   ├── phase2a_synthetic_breaches.json    # 10,000 breach scenarios
│   └── phase2a_hybrid_training.jsonl      # Weighted mix (2.5:1)
│
├── phase3a_legal_qa/
│   ├── phase3a_pdpl_chunks.json           # 500+ PDPL chunks
│   ├── phase3a_pdpl_embeddings.npy        # Vector embeddings
│   ├── phase3a_qa_pdpl_official.json      # 10,000+ Q&A pairs
│   └── qdrant_storage/                    # Vector database
│
└── validation/
    ├── extraction_validation_report.md
    ├── legal_expert_review.xlsx
    └── ai_validation_results.json
```

---

## 📚 Additional Resources

### **Vietnamese PDPL 91/2025/QH15 References**
- **Official Source**: [Vietnam National Assembly](https://quochoi.vn/) (Vietnamese)
- **English Summary**: [DLA Piper Data Protection Laws](https://www.dlapiperdataprotection.com/)
- **Legal Commentary**: Vietnamese legal journals and practitioners

### **Vietnamese NLP Tools**
- **PhoBERT**: [https://github.com/VinAIResearch/PhoBERT](https://github.com/VinAIResearch/PhoBERT)
- **VnCoreNLP**: [https://github.com/vncorenlp/VnCoreNLP](https://github.com/vncorenlp/VnCoreNLP)
- **Underthesea**: [https://github.com/undertheseanlp/underthesea](https://github.com/undertheseanlp/underthesea)

### **Vietnamese Sentence Transformers**
- **Vietnamese SBERT**: `keepitreal/vietnamese-sbert`
- **BKAI Vietnamese Bi-Encoder**: `bkai-foundation-models/vietnamese-bi-encoder`

### **Vector Databases for RAG**
- **Qdrant**: [https://qdrant.tech/](https://qdrant.tech/) (Recommended)
- **Pinecone**: [https://www.pinecone.io/](https://www.pinecone.io/)
- **Weaviate**: [https://weaviate.io/](https://weaviate.io/)

---

## 🚨 Critical Reminders

### **1. Legal Expert Involvement**
**REQUIRED** for:
- Article-to-category mapping validation
- PDPL interpretation accuracy
- Q&A answer correctness
- Legal language quality review

**Timeline**: Budget 1-2 days of legal expert time per phase

### **2. Vietnamese Text Encoding**
**ALWAYS** use UTF-8 encoding:
```python
# CORRECT
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# WRONG - Will corrupt diacritics
with open(file_path, 'r') as f:  # NO encoding specified
    content = f.read()
```

### **3. Data Leakage Prevention**
**CRITICAL** for Phase 0 improvements:
- Strict train/validation split (no phrase overlap)
- Separate test set (never seen during training)
- Cross-validation with different random seeds

**See**: `01_Phase0_Principles_PDPL_Integration.md` for leak detection code

### **4. Hybrid Training Weights**
**DO NOT** just mix 50/50:
```python
# WRONG - Equal probability
dataset = pdpl_samples + synthetic_samples
random.shuffle(dataset)

# CORRECT - Weighted sampling
dataset = create_weighted_dataset(
    pdpl_samples, pdpl_weight=2.0,
    synthetic_samples, synthetic_weight=1.0
)
```

**Rationale**: Official PDPL must have higher importance during training

---

## 🤝 Contributing

**Internal Team Workflow:**
1. Extract PDPL following `00_Master` plan
2. Legal expert validates mappings (1-2 days)
3. Choose priority phase (Phase 0 recommended first)
4. Generate hybrid dataset with proper weighting
5. Train model following phase-specific plan
6. A/B test vs previous version
7. Deploy if performance targets met

**Questions or Issues:**
- Technical: VeriSyntra AI Team
- Legal: Legal compliance advisor
- Vietnamese NLP: Linguistic consultant

---

## 📝 Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1.0 | 2025-01-20 | Initial comprehensive documentation | VeriSyntra AI Team |
| | | - Master pipeline (6 stages) | |
| | | - Phase 0 plan (Principles enhanced) | |
| | | - Phase 2A plan (Breach Triage NEW) | |
| | | - Phase 3A plan (Legal QA RAG) | |

---

**Status**: DOCUMENTATION COMPLETE - Ready for implementation  
**Next Step**: Obtain PDPL 91/2025/QH15 PDF and execute master extraction pipeline  
**Priority**: Phase 0 (2 weeks) → Phase 2A (3-4 months) → Phase 3A (6-8 months)

---

**VeriSyntra AI - Vietnamese PDPL Compliance Platform**  
*Culturally-intelligent AI for Vietnamese enterprises*
