# Data Population Method #08: VeriAIDPO AI Integration
## Automated Processing Activities from Database Discovery Scans

**Population Method:** VeriAIDPO + Data Discovery Scanning  
**Architecture:** PhoBERT Vietnamese NLP + Database Schema Analysis  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides a **detailed implementation plan** to integrate the **VeriAIDPO model** (PhoBERT-based Vietnamese PDPL classification) with the existing **Data Discovery & Scanning** implementation to automatically populate the `processing_activities` table.

[!] PREREQUISITE:** This document builds upon the foundation established in [Document #02: Automated Database Discovery](./02_Data_Population_Automated_Discovery.md). Review Document #02 first for the core database scanning infrastructure.

**[+] RELATED IMPLEMENTATIONS:**
- **[AI Classification Integration](../04_AI_Classification_Integration_Implementation.md)** (Document #04): Generic AI classification framework - provides the foundational VeriAIDPO integration patterns used here
- **[DPO Recommendations Microservice](../10_AI_Recommendations_Microservice_Implementation.md)** (Document #10): Alternative VeriAIDPO application for DPO compliance recommendations

**Document Relationship Chain:**
- **Document #02**: Base layer - Pattern-based database discovery (quick setup)
- **Document #04**: Framework layer - Generic AI classification integration (reusable patterns)
- **Document #08** (this document): Application layer - Processing activities population (specialized implementation)
- **Document #10**: Service layer - DPO recommendations microservice (different use case)

**Relationship to Document #02:**
- **Document #02** provides the **base layer**: Generic pattern-based database discovery
- **Document #08** (this document) provides the **advanced layer**: ML-powered PDPL principle classification using PhoBERT
- Implementation: Start with Document #02's scanning engine, then add VeriAIDPO for intelligent classification

**Relationship to Document #04:**
- **Document #04** provides the **generic framework**: VeriAIDPO integration patterns for any data classification
- **This document** applies that framework specifically to processing activities population
- Reuses three-service orchestration pattern (Port 8010 -> 8007 -> 8006) from Doc #04

**Integration Goal:**  
Transform raw database scans into PDPL-compliant processing activity records using AI-powered Vietnamese legal analysis.

**Key Components:**
1. **Data Discovery Scanning** (Port 8010) - Scans databases and extracts schema metadata
2. **VeriAIDPO Classification** (PhoBERT model) - Analyzes Vietnamese text for PDPL principles
3. **Activity Generator** (NEW) - Bridges scanning output to processing_activities table
4. **Vietnamese NLP Pipeline** - Generates Vietnamese-first activity names and purposes

**Expected Outcome:**  
70% reduction in DPO manual work for ROPA creation with 85%+ accuracy for Vietnamese enterprises.

**Why VeriAIDPO Instead of Basic Discovery (Doc #02)?**

| Capability | Doc #02 (Pattern-Based) | Doc #08 (VeriAIDPO) |
|-----------|------------------------|---------------------|
| **Classification** | Keyword matching | PhoBERT ML model |
| **PDPL Principles** | Inferred | 8 explicit categories |
| **Vietnamese Legal Text** | Basic translation | Advanced NLP analysis |
| **Confidence Scoring** | No | Yes (with DPO review) |
| **Legal Basis Accuracy** | Pattern-based | Context-aware |
| **Training Data** | None | 36,000 Vietnamese samples |
| **Production Ready** | Quick prototype | Enterprise-grade |

**Migration Path:** If you've implemented Document #02, this document shows how to upgrade with minimal changes to existing infrastructure.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Integration Components](#integration-components)
3. [Data Flow Pipeline](#data-flow-pipeline)
4. [Implementation Phases](#implementation-phases)
5. [Code Implementation](#code-implementation)
6. [Database Schema Updates](#database-schema-updates)
7. [API Endpoints](#api-endpoints)
8. [Vietnamese NLP Processing](#vietnamese-nlp-processing)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Guide](#deployment-guide)

---

## System Architecture

### High-Level Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VeriAIDPO Integration Architecture                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [Step 1: Data Discovery Scan]                                         │
│  ┌──────────────────────────────────────────────────┐                  │
│  │  veri-ai-data-inventory (Port 8010)              │                  │
│  │  - Database connector (MySQL, PostgreSQL, etc.)  │                  │
│  │  - Schema analyzer (tables, columns, types)      │                  │
│  │  - Sample extractor (100 rows per column)        │                  │
│  │  - Vietnamese UTF-8 validator                    │                  │
│  └──────────────────────────────────────────────────┘                  │
│                           │                                             │
│                           v                                             │
│  [Scan Output: JSON Schema Metadata]                                   │
│  {                                                                      │
│    "table_name": "khach_hang",                                         │
│    "columns": ["ho_ten", "so_dien_thoai", "email", "dia_chi"],        │
│    "sample_data": [...],                                               │
│    "row_count": 15000                                                  │
│  }                                                                      │
│                           │                                             │
│                           v                                             │
│  [Step 2: Vietnamese Context Builder]                                  │
│  ┌──────────────────────────────────────────────────┐                  │
│  │  VietnameseContextBuilder (NEW SERVICE)          │                  │
│  │  - Table name translator (khach_hang -> Customer) │                  │
│  │  - Column name analyzer (ho_ten -> Full Name)     │                  │
│  │  - Purpose inference (CRM, HR, Finance, etc.)    │                  │
│  │  - Industry context mapper (Fintech, Healthcare) │                  │
│  └──────────────────────────────────────────────────┘                  │
│                           │                                             │
│                           v                                             │
│  [Vietnamese Text Context]                                             │
│  "Bảng dữ liệu 'khach_hang' chứa các trường ho_ten, so_dien_thoai,   │
│   email, dia_chi. Mục đích xử lý là quản lý thông tin khách hàng      │
│   để cung cấp dịch vụ."                                               │
│                           │                                             │
│                           v                                             │
│  [Step 3: VeriAIDPO Classification]                                   │
│  ┌──────────────────────────────────────────────────┐                  │
│  │  VeriAIDPOModelLoader (PhoBERT)                  │                  │
│  │  - Load model: vinai/phobert-base-v2             │                  │
│  │  - Tokenize Vietnamese text (max 256 tokens)     │                  │
│  │  - Run inference (GPU/CPU auto-detect)           │                  │
│  │  - Output: PDPL principle + confidence score     │                  │
│  └──────────────────────────────────────────────────┘                  │
│                           │                                             │
│                           v                                             │
│  [Classification Result]                                               │
│  {                                                                      │
│    "category_id": 1,                                                   │
│    "category_name_vi": "Giới hạn mục đích",                           │
│    "category_name_en": "Purpose Limitation",                          │
│    "confidence": 0.87,                                                 │
│    "pdpl_article": "Art. 7.1.c"                                       │
│  }                                                                      │
│                           │                                             │
│                           v                                             │
│  [Step 4: Activity Generator]                                         │
│  ┌──────────────────────────────────────────────────┐                  │
│  │  ProcessingActivityGenerator (NEW SERVICE)       │                  │
│  │  - Map PDPL principle -> Legal basis              │                  │
│  │  - Generate activity_name_vi (Vietnamese-first)  │                  │
│  │  - Generate processing_purpose_vi                │                  │
│  │  - Detect sensitive data (PDPL Art. 4.13)        │                  │
│  │  - Calculate retention period (industry rules)   │                  │
│  │  - Assess DPIA requirement                       │                  │
│  └──────────────────────────────────────────────────┘                  │
│                           │                                             │
│                           v                                             │
│  [Step 5: Insert to processing_activities Table]                      │
│  ┌──────────────────────────────────────────────────┐                  │
│  │  PostgreSQL: processing_activities Table         │                  │
│  │  - activity_id: UUID                             │                  │
│  │  - activity_name_vi: "Quản lý khách hàng CRM"   │                  │
│  │  - processing_purpose_vi: "Lưu trữ và..."       │                  │
│  │  - legal_basis: "contract"                       │                  │
│  │  - pdpl_principle_vi: "Giới hạn mục đích"       │                  │
│  │  - confidence_score: 0.87                        │                  │
│  │  - status: "pending_review" (DPO approval)       │                  │
│  │  - created_by: "system-ai-discovery"             │                  │
│  └──────────────────────────────────────────────────┘                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Components

### Component 1: Data Discovery Scanning (EXISTING)

**Location:** `backend/veri_ai_data_inventory/`  
**Documentation:** `docs/Veri_Intelligent_Data/01_Data_Discovery_Scanning_Implementation.md`

**Current Capabilities:**
- Multi-database scanning (PostgreSQL, MySQL, SQL Server, MongoDB)
- Schema analysis (tables, columns, data types)
- Sample data extraction (100 rows per column)
- Vietnamese UTF-8 encoding support
- Column filtering (include/exclude modes)

**Output Format:**
```json
{
  "scan_job_id": "uuid",
  "database_name": "production_db",
  "tables_discovered": [
    {
      "table_name": "khach_hang",
      "schema": "public",
      "row_count": 15000,
      "columns": [
        {
          "column_name": "ho_ten",
          "data_type": "VARCHAR(255)",
          "is_nullable": false,
          "sample_values": ["Nguyễn Văn A", "Trần Thị B", ...]
        },
        {
          "column_name": "so_dien_thoai",
          "data_type": "VARCHAR(20)",
          "is_nullable": true,
          "sample_values": ["0901234567", "0912345678", ...]
        }
      ],
      "created_at": "2025-11-06T10:00:00+07:00"
    }
  ]
}
```

---

### Component 2: VeriAIDPO Model (EXISTING)

**Location:** `backend/app/ml/model_loader.py`  
**Model:** `vinai/phobert-base-v2` (PhoBERT)  
**Hugging Face:** `TranHF/VeriAIDPO_Principles_VI_v1`

**Current Capabilities:**
- 8-category PDPL principle classification
- Vietnamese text tokenization (max 256 tokens)
- Confidence scoring (0.0-1.0)
- GPU/CPU auto-detection
- Singleton pattern (lazy loading)

**Input:** Vietnamese text describing data processing  
**Output:**
```json
{
  "category_id": 1,
  "category_name_vi": "Giới hạn mục đích",
  "category_name_en": "Purpose Limitation",
  "confidence": 0.87,
  "all_probabilities": {
    "cat_0": 0.05,
    "cat_1": 0.87,
    "cat_2": 0.03,
    ...
  }
}
```

---

### Component 3: Vietnamese Context Builder (NEW - TO IMPLEMENT)

**Location:** `backend/veri_ai_data_inventory/services/vietnamese_context_builder.py`

**Purpose:** Transform database scan metadata into Vietnamese text suitable for VeriAIDPO analysis

**Responsibilities:**
1. Translate table names to Vietnamese business terms
2. Analyze column names for data category hints
3. Infer processing purpose from table/column patterns
4. Build Vietnamese sentence context for VeriAIDPO
5. Add industry-specific context (Fintech, Healthcare, etc.)

**Implementation:**
```python
# backend/veri_ai_data_inventory/services/vietnamese_context_builder.py

"""
Vietnamese Context Builder
Transform Database Scans to Vietnamese Legal Context
"""

from typing import Dict, List, Optional
import re

class VietnameseContextBuilder:
    """
    Xây dựng ngữ cảnh tiếng Việt từ kết quả quét database
    Build Vietnamese context from database scan results
    """
    
    # Table name to Vietnamese business term mapping
    TABLE_NAME_MAPPINGS: Dict[str, str] = {
        # Customer management
        "customer": "khách hàng",
        "khach_hang": "khách hàng",
        "client": "khách hàng",
        
        # Employee management
        "employee": "nhân viên",
        "nhan_vien": "nhân viên",
        "staff": "nhân viên",
        "hr": "nhân sự",
        
        # Financial
        "transaction": "giao dịch",
        "giao_dich": "giao dịch",
        "payment": "thanh toán",
        "invoice": "hóa đơn",
        
        # Healthcare
        "patient": "bệnh nhân",
        "benh_nhan": "bệnh nhân",
        "medical_record": "hồ sơ bệnh án",
        
        # General
        "user": "người dùng",
        "account": "tài khoản",
        "order": "đơn hàng"
    }
    
    # Processing purpose templates
    PURPOSE_TEMPLATES: Dict[str, str] = {
        "khách hàng": "Quản lý thông tin khách hàng để cung cấp dịch vụ và hỗ trợ",
        "nhân viên": "Quản lý nhân sự để thực hiện nghĩa vụ lao động và tính lương",
        "giao dịch": "Xử lý giao dịch để thực hiện hợp đồng và tuân thủ pháp luật",
        "bệnh nhân": "Lưu trữ hồ sơ bệnh án để cung cấp dịch vụ y tế",
        "người dùng": "Quản lý tài khoản để cung cấp dịch vụ và bảo mật",
        "đơn hàng": "Xử lý đơn hàng để thực hiện hợp đồng mua bán"
    }
    
    def build_context(
        self,
        table_name: str,
        columns: List[Dict[str, any]],
        industry: Optional[str] = None
    ) -> str:
        """
        Xây dựng ngữ cảnh tiếng Việt từ metadata bảng
        Build Vietnamese context from table metadata
        
        Args:
            table_name: Database table name
            columns: List of column metadata
            industry: Optional industry context (fintech, healthcare, etc.)
        
        Returns:
            Vietnamese text context for VeriAIDPO
        """
        # Step 1: Translate table name to Vietnamese business term
        vietnamese_term = self._translate_table_name(table_name)
        
        # Step 2: Extract column names
        column_names = [col['column_name'] for col in columns]
        
        # Step 3: Infer processing purpose
        purpose = self._infer_purpose(vietnamese_term, column_names, industry)
        
        # Step 4: Build Vietnamese sentence
        context = f"Bảng dữ liệu '{table_name}' chứa các trường "
        context += ", ".join(column_names[:5])  # First 5 columns
        if len(column_names) > 5:
            context += f" và {len(column_names) - 5} trường khác"
        context += f". Mục đích xử lý là {purpose}."
        
        # Step 5: Add industry context if provided
        if industry:
            context += f" Ngành nghề: {industry}."
        
        return context
    
    def _translate_table_name(self, table_name: str) -> str:
        """Dịch tên bảng sang tiếng Việt"""
        table_lower = table_name.lower()
        
        for en_term, vi_term in self.TABLE_NAME_MAPPINGS.items():
            if en_term in table_lower:
                return vi_term
        
        # Default: use table name as-is
        return table_name
    
    def _infer_purpose(
        self,
        vietnamese_term: str,
        column_names: List[str],
        industry: Optional[str]
    ) -> str:
        """Suy luận mục đích xử lý từ ngữ cảnh"""
        # Check for purpose template
        if vietnamese_term in self.PURPOSE_TEMPLATES:
            return self.PURPOSE_TEMPLATES[vietnamese_term]
        
        # Infer from column patterns
        if any(re.search(r'health|benh|medical', col.lower()) for col in column_names):
            return "Lưu trữ thông tin sức khỏe để cung cấp dịch vụ y tế"
        
        if any(re.search(r'payment|thanh_toan|transaction', col.lower()) for col in column_names):
            return "Xử lý giao dịch tài chính để thực hiện hợp đồng"
        
        # Default generic purpose
        return "Lưu trữ và quản lý dữ liệu để cung cấp dịch vụ"
```

---

### Component 4: Processing Activity Generator (NEW - TO IMPLEMENT)

**Location:** `backend/veri_ai_data_inventory/services/activity_generator.py`

**Purpose:** Transform VeriAIDPO classification into processing_activities table records

**Implementation:**
```python
# backend/veri_ai_data_inventory/services/activity_generator.py

"""
Processing Activity Generator
VeriAIDPO Classification -> processing_activities Table
"""

from typing import Dict, List, Optional
from datetime import datetime
import uuid

from app.ml.model_loader import get_model_loader, PDPL_CATEGORIES
from .vietnamese_context_builder import VietnameseContextBuilder


class ProcessingActivityGenerator:
    """
    Tạo processing activity từ kết quả phân loại VeriAIDPO
    Generate processing activities from VeriAIDPO classification
    """
    
    # PDPL Principle to Legal Basis mapping
    PRINCIPLE_TO_LEGAL_BASIS: Dict[int, str] = {
        0: "legal_obligation",   # Lawfulness
        1: "contract",            # Purpose Limitation
        2: "contract",            # Data Minimization
        3: "contract",            # Accuracy
        4: "contract",            # Storage Limitation
        5: "legal_obligation",    # Security
        6: "consent",             # Transparency
        7: "consent"              # Consent
    }
    
    # Sensitive data keywords (PDPL Art. 4.13)
    SENSITIVE_DATA_KEYWORDS: List[str] = [
        "health", "suc_khoe", "benh_an", "medical",
        "biometric", "sinh_trac", "fingerprint", "face",
        "genetic", "di_truyen", "dna",
        "political", "chinh_tri", "party",
        "religious", "ton_giao", "religion",
        "sexual", "tinh_duc", "orientation",
        "criminal", "tu_phap", "conviction",
        "union", "cong_doan", "trade_union",
        "child", "tre_em", "under_16"
    ]
    
    def __init__(self):
        self.veriaidpo_model = get_model_loader()
        self.context_builder = VietnameseContextBuilder()
    
    async def generate_from_scan(
        self,
        scan_result: Dict[str, any],
        tenant_id: str
    ) -> List[Dict[str, any]]:
        """
        Tạo processing activities từ kết quả quét database
        Generate processing activities from database scan results
        
        Args:
            scan_result: Output from data discovery scan
            tenant_id: Tenant identifier for multi-tenant isolation
        
        Returns:
            List of processing activity records ready for insertion
        """
        activities = []
        
        for table in scan_result.get('tables_discovered', []):
            # Build Vietnamese context
            context = self.context_builder.build_context(
                table_name=table['table_name'],
                columns=table['columns'],
                industry=scan_result.get('industry')
            )
            
            # Classify using VeriAIDPO
            classification = self.veriaidpo_model.predict(context)
            
            # Generate activity record
            activity = self._build_activity_record(
                table=table,
                classification=classification,
                context=context,
                tenant_id=tenant_id
            )
            
            activities.append(activity)
        
        return activities
    
    def _build_activity_record(
        self,
        table: Dict[str, any],
        classification: Dict[str, any],
        context: str,
        tenant_id: str
    ) -> Dict[str, any]:
        """Xây dựng bản ghi processing activity"""
        category_id = classification['category_id']
        confidence = classification['confidence']
        
        # Get PDPL category info
        pdpl_info = PDPL_CATEGORIES.get(category_id, {})
        
        # Infer legal basis from PDPL principle
        legal_basis = self.PRINCIPLE_TO_LEGAL_BASIS.get(category_id, "contract")
        
        # Generate activity name (Vietnamese-first)
        activity_name_vi = self._generate_activity_name(table['table_name'])
        activity_name_en = self._generate_activity_name_en(table['table_name'])
        
        # Extract processing purpose from context
        purpose_vi = self._extract_purpose(context)
        
        # Detect sensitive data
        has_sensitive = self._detect_sensitive_data(table['columns'])
        
        # Build activity record
        activity = {
            "activity_id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "activity_name_vi": activity_name_vi,
            "activity_name_en": activity_name_en,
            "processing_purpose_vi": purpose_vi,
            "processing_purpose_en": None,  # Optional translation
            
            # Legal basis
            "legal_basis": legal_basis,
            "legal_basis_vi": self._translate_legal_basis(legal_basis),
            "legal_basis_en": legal_basis.replace('_', ' ').title(),
            
            # PDPL principle
            "pdpl_principle_vi": pdpl_info.get('vi'),
            "pdpl_principle_en": pdpl_info.get('en'),
            "pdpl_article": pdpl_info.get('description'),
            
            # Data characteristics
            "has_sensitive_data": has_sensitive,
            "data_retention_months": self._calculate_retention(table['table_name']),
            "requires_dpia": has_sensitive,  # Simplified logic
            
            # AI metadata
            "confidence_score": confidence,
            "source_table_name": table['table_name'],
            "discovered_columns": [col['column_name'] for col in table['columns']],
            
            # Status
            "status": "pending_review" if confidence < 0.80 else "ai_suggested",
            "created_by": "system-ai-discovery",
            "created_at": datetime.now().isoformat(),
            
            # Review notes
            "review_notes_vi": self._generate_review_notes(confidence),
            "review_notes_en": None
        }
        
        return activity
    
    def _generate_activity_name(self, table_name: str) -> str:
        """Tạo tên activity bằng tiếng Việt"""
        # Map common table patterns to Vietnamese activity names
        name_map = {
            "customer": "Quản lý thông tin khách hàng",
            "khach_hang": "Quản lý thông tin khách hàng",
            "employee": "Quản lý nhân viên",
            "nhan_vien": "Quản lý nhân viên",
            "transaction": "Xử lý giao dịch",
            "giao_dich": "Xử lý giao dịch",
            "user": "Quản lý người dùng",
            "order": "Xử lý đơn hàng"
        }
        
        table_lower = table_name.lower()
        for pattern, name_vi in name_map.items():
            if pattern in table_lower:
                return name_vi
        
        # Default: capitalize table name
        return f"Quản lý {table_name}"
    
    def _generate_activity_name_en(self, table_name: str) -> str:
        """Generate activity name in English"""
        return f"{table_name.replace('_', ' ').title()} Management"
    
    def _extract_purpose(self, context: str) -> str:
        """Trích xuất mục đích xử lý từ ngữ cảnh"""
        # Look for "Mục đích xử lý là ..." pattern
        import re
        match = re.search(r'Mục đích xử lý là (.+?)\.', context)
        if match:
            return match.group(1)
        
        return "Lưu trữ và quản lý dữ liệu để cung cấp dịch vụ"
    
    def _detect_sensitive_data(self, columns: List[Dict]) -> bool:
        """Phát hiện dữ liệu nhạy cảm theo PDPL Điều 4.13"""
        for column in columns:
            column_name = column['column_name'].lower()
            for keyword in self.SENSITIVE_DATA_KEYWORDS:
                if keyword in column_name:
                    return True
        return False
    
    def _calculate_retention(self, table_name: str) -> int:
        """Tính thời gian lưu trữ dựa trên loại dữ liệu"""
        retention_map = {
            "customer": 24,      # 2 years
            "employee": 84,      # 7 years (labor law)
            "transaction": 60,   # 5 years (tax law)
            "medical": 120,      # 10 years (healthcare)
            "audit": 84          # 7 years (compliance)
        }
        
        table_lower = table_name.lower()
        for pattern, months in retention_map.items():
            if pattern in table_lower:
                return months
        
        return 24  # Default: 2 years
    
    def _translate_legal_basis(self, legal_basis: str) -> str:
        """Dịch cơ sở pháp lý sang tiếng Việt"""
        translations = {
            "consent": "Sự đồng ý",
            "contract": "Thực hiện hợp đồng",
            "legal_obligation": "Tuân thủ nghĩa vụ pháp lý",
            "vital_interest": "Bảo vệ lợi ích sống còn",
            "public_task": "Thực hiện nhiệm vụ công",
            "legitimate_interest": "Lợi ích hợp pháp"
        }
        return translations.get(legal_basis, legal_basis)
    
    def _generate_review_notes(self, confidence: float) -> str:
        """Tạo ghi chú xem xét cho DPO"""
        if confidence >= 0.90:
            return "Độ tin cậy cao - Khuyến nghị phê duyệt"
        elif confidence >= 0.80:
            return "Độ tin cậy tốt - Xem xét phê duyệt"
        elif confidence >= 0.70:
            return "Độ tin cậy trung bình - Cần xác nhận cơ sở pháp lý"
        else:
            return "Độ tin cậy thấp - Cần xem xét kỹ và điều chỉnh thủ công"
```

---

## Data Flow Pipeline

### End-to-End Workflow

```
[Trigger: User Initiates Database Scan]
         │
         v
[1. Data Discovery Scan Job Created]
   POST /api/v1/scan/database
   Body: {
     "database_type": "postgresql",
     "connection_string": "...",
     "include_tables": ["khach_hang", "nhan_vien"]
   }
         │
         v
[2. Scanner Analyzes Database Schema]
   - Connect to database (UTF-8 encoding)
   - List tables and columns
   - Extract sample data (100 rows)
   - Validate Vietnamese diacritics
         │
         v
[3. Scan Results Stored]
   Save to: scan_jobs table
   Status: completed
         │
         v
[4. TRIGGER: Auto-Process with VeriAIDPO]
   IF scan_job.auto_generate_activities = true
         │
         v
[5. Vietnamese Context Builder]
   For each table:
     - Build Vietnamese context text
     - "Bảng 'khach_hang' chứa ho_ten, email..."
         │
         v
[6. VeriAIDPO Classification]
   - Load PhoBERT model
   - Tokenize Vietnamese text
   - Run inference
   - Output: PDPL principle + confidence
         │
         v
[7. Activity Generator]
   - Map principle -> legal basis
   - Generate activity_name_vi
   - Extract processing_purpose_vi
   - Detect sensitive data
   - Calculate retention period
         │
         v
[8. Insert to processing_activities Table]
   INSERT INTO processing_activities (
     activity_id, tenant_id,
     activity_name_vi, processing_purpose_vi,
     legal_basis, pdpl_principle_vi,
     confidence_score, status,
     created_by, created_at
   ) VALUES (...)
         │
         v
[9. DPO Review Queue]
   Status: pending_review
   - DPO reviews AI-generated activities
   - Approves or edits
   - Status -> active
         │
         v
[10. ROPA Complete]
   Processing activities ready for PDPL compliance reporting
```

---

## Implementation Phases

### Phase 1: Foundation Setup (Week 1)

**Goal:** Establish core infrastructure for VeriAIDPO integration

**Tasks:**
1. **Verify VeriAIDPO Model Deployment**
   - Confirm model available at `backend/app/ml/models/VeriAIDPO_Principles_VI_v1`
   - Test inference with Vietnamese text samples
   - Verify GPU/CPU detection working

2. **Create Vietnamese Context Builder Service**
   - Implement `VietnameseContextBuilder` class
   - Add table name translations
   - Add processing purpose templates
   - Unit tests with Vietnamese examples

3. **Create Processing Activity Generator Service**
   - Implement `ProcessingActivityGenerator` class
   - Add PDPL principle -> legal basis mapping
   - Add sensitive data detection logic
   - Unit tests with mock classification results

**Deliverables:**
- `backend/veri_ai_data_inventory/services/vietnamese_context_builder.py`
- `backend/veri_ai_data_inventory/services/activity_generator.py`
- Unit test suite (80%+ coverage)

---

### Phase 2: Database Schema Integration (Week 2)

**Goal:** Update database schema to support AI-generated activities

**Database Schema Updates:**

```sql
-- Add new columns to processing_activities table
ALTER TABLE processing_activities ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3,2);
ALTER TABLE processing_activities ADD COLUMN IF NOT EXISTS source_table_name VARCHAR(255);
ALTER TABLE processing_activities ADD COLUMN IF NOT EXISTS discovered_columns JSONB;
ALTER TABLE processing_activities ADD COLUMN IF NOT EXISTS ai_classification_metadata JSONB;

-- Add index for AI-generated activities
CREATE INDEX IF NOT EXISTS idx_processing_activities_ai_generated 
ON processing_activities(created_by, confidence_score) 
WHERE created_by = 'system-ai-discovery';

-- Add new scan_jobs configuration column
ALTER TABLE scan_jobs ADD COLUMN IF NOT EXISTS auto_generate_activities BOOLEAN DEFAULT false;

-- Create activity review workflow table
CREATE TABLE IF NOT EXISTS activity_review_queue (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_id UUID NOT NULL REFERENCES processing_activities(activity_id),
    tenant_id UUID NOT NULL,
    review_status VARCHAR(50) NOT NULL, -- pending, approved, rejected, modified
    reviewed_by VARCHAR(255),
    review_notes_vi TEXT,
    review_notes_en TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);

CREATE INDEX idx_activity_review_tenant ON activity_review_queue(tenant_id, review_status);
```

**Migration Script:**
```bash
# Create Alembic migration
cd backend/veri_ai_data_inventory
alembic revision -m "add_veriaidpo_integration_columns"

# Apply migration
alembic upgrade head
```

---

### Phase 3: API Endpoint Development (Week 3)

**Goal:** Create API endpoints for scan -> activity generation workflow

**New API Endpoints:**

```python
# backend/veri_ai_data_inventory/api/endpoints/veriaidpo_integration.py

"""
VeriAIDPO Integration API Endpoints
Scan Database -> Generate Processing Activities
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/veriaidpo-integration", tags=["veriaidpo-integration"])


class GenerateActivitiesRequest(BaseModel):
    """Yêu cầu tạo processing activities từ scan"""
    scan_job_id: str = Field(..., description="ID của scan job đã hoàn thành")
    auto_approve_threshold: Optional[float] = Field(0.90, description="Ngưỡng tự động phê duyệt")
    tenant_id: str = Field(..., description="Tenant identifier")


class GenerateActivitiesResponse(BaseModel):
    """Kết quả tạo processing activities"""
    total_activities: int
    ai_suggested: int
    pending_review: int
    activities: List[Dict[str, any]]


@router.post("/generate-from-scan", response_model=GenerateActivitiesResponse)
async def generate_activities_from_scan(
    request: GenerateActivitiesRequest,
    current_user = Depends(get_current_user)
):
    """
    Tạo processing activities từ kết quả quét database
    Generate processing activities from database scan results
    
    Workflow:
    1. Retrieve scan_job results
    2. For each table: Build Vietnamese context
    3. Classify with VeriAIDPO
    4. Generate activity records
    5. Insert to processing_activities table
    6. Return statistics
    """
    # Step 1: Retrieve scan job
    scan_job = await get_scan_job(request.scan_job_id, request.tenant_id)
    if not scan_job:
        raise HTTPException(status_code=404, detail="Scan job not found")
    
    if scan_job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Scan job not completed")
    
    # Step 2: Generate activities
    generator = ProcessingActivityGenerator()
    activities = await generator.generate_from_scan(
        scan_result=scan_job['results'],
        tenant_id=request.tenant_id
    )
    
    # Step 3: Insert to database
    ai_suggested = 0
    pending_review = 0
    
    for activity in activities:
        # Auto-approve high confidence
        if activity['confidence_score'] >= request.auto_approve_threshold:
            activity['status'] = 'active'
            ai_suggested += 1
        else:
            activity['status'] = 'pending_review'
            pending_review += 1
        
        await insert_processing_activity(activity)
    
    return {
        "total_activities": len(activities),
        "ai_suggested": ai_suggested,
        "pending_review": pending_review,
        "activities": activities
    }


@router.get("/review-queue/{tenant_id}")
async def get_review_queue(
    tenant_id: str,
    current_user = Depends(get_current_user)
):
    """
    Lấy danh sách activities cần DPO xem xét
    Get activities pending DPO review
    """
    activities = await get_pending_review_activities(tenant_id)
    return {
        "total": len(activities),
        "activities": activities
    }


@router.post("/approve-activity/{activity_id}")
async def approve_activity(
    activity_id: str,
    review_notes: Optional[str] = None,
    current_user = Depends(get_current_dpo_user)  # Requires DPO role
):
    """
    Phê duyệt activity do AI tạo
    Approve AI-generated activity
    """
    await update_activity_status(
        activity_id=activity_id,
        status='active',
        reviewed_by=current_user.user_id,
        review_notes=review_notes
    )
    return {"message": "Activity approved", "activity_id": activity_id}
```

---

### Phase 4: Testing & Validation (Week 4)

**Goal:** Comprehensive testing with real Vietnamese enterprise data

**Test Strategy:**

1. **Unit Tests** - Individual component testing
2. **Integration Tests** - End-to-end pipeline testing
3. **Vietnamese NLP Tests** - Diacritics and legal terminology validation
4. **Industry-Specific Tests** - Fintech, Healthcare, E-commerce scenarios
5. **Performance Tests** - Large database scanning (100+ tables)

**Test Cases:**

```python
# tests/test_veriaidpo_integration.py

"""
VeriAIDPO Integration Test Suite
"""

import pytest
from backend.veri_ai_data_inventory.services.vietnamese_context_builder import VietnameseContextBuilder
from backend.veri_ai_data_inventory.services.activity_generator import ProcessingActivityGenerator


class TestVietnameseContextBuilder:
    """Test Vietnamese context generation"""
    
    def test_customer_table_context(self):
        """Test: Customer table generates correct Vietnamese context"""
        builder = VietnameseContextBuilder()
        
        context = builder.build_context(
            table_name="khach_hang",
            columns=[
                {"column_name": "ho_ten"},
                {"column_name": "email"},
                {"column_name": "so_dien_thoai"}
            ]
        )
        
        assert "khách hàng" in context.lower()
        assert "ho_ten" in context
        assert "Mục đích xử lý" in context
        assert "cung cấp dịch vụ" in context
    
    def test_vietnamese_diacritics_preserved(self):
        """Test: Vietnamese diacritics preserved in context"""
        builder = VietnameseContextBuilder()
        
        context = builder.build_context(
            table_name="nhân_viên",
            columns=[{"column_name": "họ_tên"}]
        )
        
        # Verify diacritics not lost
        assert "nhân viên" in context or "nhân_viên" in context
        assert "họ_tên" in context or "họ tên" in context


class TestProcessingActivityGenerator:
    """Test activity generation from classification"""
    
    @pytest.mark.asyncio
    async def test_generate_customer_activity(self):
        """Test: Customer table generates valid activity"""
        generator = ProcessingActivityGenerator()
        
        scan_result = {
            "tables_discovered": [
                {
                    "table_name": "khach_hang",
                    "columns": [
                        {"column_name": "ho_ten", "data_type": "VARCHAR(255)"},
                        {"column_name": "email", "data_type": "VARCHAR(255)"}
                    ]
                }
            ]
        }
        
        activities = await generator.generate_from_scan(
            scan_result=scan_result,
            tenant_id="test-tenant-123"
        )
        
        assert len(activities) == 1
        activity = activities[0]
        
        # Validate Vietnamese fields
        assert "activity_name_vi" in activity
        assert "Quản lý" in activity["activity_name_vi"]
        assert "processing_purpose_vi" in activity
        assert activity["legal_basis"] in ["consent", "contract", "legal_obligation"]
        assert 0.0 <= activity["confidence_score"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_sensitive_data_detection(self):
        """Test: Sensitive data columns detected correctly"""
        generator = ProcessingActivityGenerator()
        
        scan_result = {
            "tables_discovered": [
                {
                    "table_name": "benh_nhan",
                    "columns": [
                        {"column_name": "ho_ten"},
                        {"column_name": "benh_an"},  # Health data - sensitive!
                        {"column_name": "ket_qua_xet_nghiem"}
                    ]
                }
            ]
        }
        
        activities = await generator.generate_from_scan(
            scan_result=scan_result,
            tenant_id="test-tenant-123"
        )
        
        activity = activities[0]
        assert activity["has_sensitive_data"] is True
        assert activity["requires_dpia"] is True
```

---

### Phase 5: Production Deployment (Week 5)

**Goal:** Deploy to production with monitoring and rollback plan

**Deployment Checklist:**

- [ ] VeriAIDPO model deployed to production
- [ ] Database migrations applied
- [ ] API endpoints tested in staging
- [ ] Vietnamese NLP validation passed
- [ ] Performance benchmarks met (< 5 sec per table)
- [ ] DPO review workflow functional
- [ ] Monitoring dashboards configured
- [ ] Documentation updated
- [ ] Training materials for DPOs ready

**Production Configuration:**

```python
# config/production.py

VERIAIDPO_CONFIG = {
    "model_path": "/app/ml/models/VeriAIDPO_Principles_VI_v1",
    "auto_load": False,  # Lazy loading
    "gpu_enabled": True,
    "confidence_threshold": 0.75,
    "auto_approve_threshold": 0.90,
    "max_context_length": 256,  # tokens
    "batch_size": 10  # tables per batch
}

ACTIVITY_GENERATION_CONFIG = {
    "enabled": True,
    "require_dpo_review": True,
    "auto_approve_high_confidence": False,  # Production: always review
    "retention_calculation_mode": "industry_standard",
    "vietnamese_diacritics_required": True
}
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] VeriAIDPO model successfully classifies Vietnamese database contexts
- [TARGET] Vietnamese Context Builder generates accurate legal terminology
- [TARGET] Processing Activity Generator creates valid PDPL-compliant records
- [TARGET] 85%+ accuracy on test dataset (100 Vietnamese enterprise tables)
- [TARGET] < 5 seconds average processing time per table
- [TARGET] Zero hard-coding violations (all values in constants)
- [TARGET] DPO review workflow functional with Vietnamese UI
- [TARGET] Bilingual error handling (Vietnamese-first)
- [TARGET] Integration tests pass (end-to-end pipeline)
- [TARGET] Production deployment successful
- [TARGET] 70%+ reduction in manual ROPA creation time
- [TARGET] Documentation complete with Vietnamese examples

---

**Status:** Implementation Ready  
**Next Steps:** Begin Phase 1 - Foundation Setup  
**Owner:** VeriSyntra AI Team  
**Review Date:** November 13, 2025
