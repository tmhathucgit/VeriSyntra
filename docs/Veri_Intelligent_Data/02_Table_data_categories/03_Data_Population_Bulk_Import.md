# Data Population Method 3: Bulk Import CSV/Excel
## Vietnamese PDPL 2025 Compliance - Data Categories Table

**Project:** veri-ai-data-inventory Data Population  
**Target:** data_categories Table  
**Method:** File-Based Bulk Import with PDPL Validation  
**Architecture:** Pandas + Vietnamese Column Mapping + PDPL Article 4.13 Detection  
**Status:** Implementation Ready  
**Date:** November 6, 2025

---

## Executive Summary

This document provides detailed implementation for **bulk import of data categories** from CSV and Excel files. The system supports Vietnamese-first column mapping, automatic PDPL Article 4.13 sensitive data detection, and validation of category data before database insertion.

**Key Features:**
- CSV and Excel file import (XLS, XLSX)
- Vietnamese column name mapping with 5+ aliases per field
- Automatic PDPL Article 4.13 sensitive category detection
- File validation and preview before import
- Batch processing with transaction support
- Import status tracking (pending, processing, completed, failed)
- Zero hard-coding with configuration-based mapping

**Use Cases:**
- Bulk create data categories from spreadsheets
- Import Vietnamese category templates
- Migrate categories from existing systems
- Mass update category definitions
- PDPL compliance baseline setup

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [File Format Configuration](#file-format-configuration)
3. [Vietnamese Column Mapping](#vietnamese-column-mapping)
4. [Import Processing Pipeline](#import-processing-pipeline)
5. [PDPL Validation Rules](#pdpl-validation-rules)
6. [Error Handling](#error-handling)
7. [Success Criteria](#success-criteria)

---

## Architecture Overview

### Bulk Import System

```
┌─────────────────────────────────────────────────────────────┐
│         Bulk Import Architecture (CSV/Excel)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  File        │  │  Column      │  │  PDPL        │     │
│  │  Upload      │─>│  Mapper      │─>│  Validator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         v                  v                  v            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Pandas      │  │  Preview     │  │  Batch       │     │
│  │  Parser      │  │  Generator   │  │  Processor   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │            │
│         └──────────────────┴──────────────────┘            │
│                           │                                │
│                           v                                │
│              ┌────────────────────────┐                    │
│              │  data_categories       │                    │
│              │  (Bulk Imported)       │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Import Workflow:**
1. Upload CSV/Excel file
2. Detect file type and encoding
3. Map Vietnamese column names to fields
4. Validate PDPL compliance (Article 4.13)
5. Generate preview with validation results
6. User confirms import
7. Batch process with transaction
8. Track import status and errors

---

## File Format Configuration

### Supported File Types and Limits

```python
# services/import/file_config.py

"""
File Import Configuration
Vietnamese-first Bulk Import Settings
"""

from enum import Enum
from typing import Dict


class FileType(str, Enum):
    """
    Loại file import
    File type for import
    """
    CSV = "csv"
    XLSX = "xlsx"
    XLS = "xls"


class ImportStatus(str, Enum):
    """
    Trạng thái import
    Import status
    """
    PENDING = "pending"              # Chờ xử lý
    VALIDATING = "validating"        # Đang kiểm tra
    VALID = "valid"                  # Hợp lệ
    INVALID = "invalid"              # Không hợp lệ
    PROCESSING = "processing"        # Đang xử lý
    COMPLETED = "completed"          # Hoàn thành
    FAILED = "failed"                # Thất bại
    PARTIAL = "partial"              # Hoàn thành một phần


# File size limits
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Row limits
MAX_ROWS_PER_IMPORT = 10000
MIN_ROWS_PER_IMPORT = 1

# Batch processing
BATCH_SIZE = 500
TRANSACTION_BATCH_SIZE = 100

# Supported encodings
SUPPORTED_ENCODINGS = [
    "utf-8",
    "utf-8-sig",
    "latin1",
    "iso-8859-1",
    "cp1252",
    "windows-1252"
]

# Default encoding
DEFAULT_ENCODING = "utf-8"

# CSV delimiters
CSV_DELIMITERS = [",", ";", "\t", "|"]
DEFAULT_CSV_DELIMITER = ","
```

---

## Vietnamese Column Mapping

### Multi-Alias Column Name Mapping

```python
# services/import/column_mapper.py

"""
Vietnamese Column Name Mapper
PDPL-Aware Field Mapping
"""

from typing import Dict, List, Optional
import pandas as pd


# Vietnamese column name aliases (5+ variations per field)
# Bao gồm cả phiên bản KHÔNG dấu để hỗ trợ người dùng nhập liệu (database identifiers)
CATEGORY_COLUMN_MAPPINGS: Dict[str, List[str]] = {
    "category_name_vi": [
        "tên danh mục",
        "ten danh muc",  # Phiên bản không dấu - Database identifier
        "tên loại dữ liệu",
        "ten loai du lieu",  # Phiên bản không dấu - Database identifier
        "danh mục",
        "danh muc",  # Phiên bản không dấu - Database identifier
        "category name vi",
        "category_name_vi",
        "ten_danh_muc"
    ],
    "category_name_en": [
        "tên tiếng anh",
        "ten tieng anh",
        "category name en",
        "category_name_en",
        "english name",
        "name_en"
    ],
    "category_description_vi": [
        "mô tả",
        "mo ta",
        "mô tả danh mục",
        "mo ta danh muc",
        "description vi",
        "description_vi",
        "mo_ta"
    ],
    "category_description_en": [
        "mô tả tiếng anh",
        "mo ta tieng anh",
        "description en",
        "description_en",
        "english description"
    ],
    "category_type": [
        "loại danh mục",
        "loai danh muc",
        "loại",
        "loai",
        "type",
        "category type",
        "category_type",
        "loai_danh_muc"
    ],
    "is_sensitive": [
        "dữ liệu nhạy cảm",
        "du lieu nhay cam",  # Phiên bản không dấu - Database identifier
        "nhạy cảm",
        "nhay cam",  # Phiên bản không dấu - Database identifier
        "sensitive",
        "is sensitive",
        "is_sensitive",
        "nhay_cam"
    ],
    "pdpl_article_reference": [
        "điều luật PDPL",
        "dieu luat PDPL",
        "điều PDPL",
        "dieu PDPL",
        "PDPL article",
        "article",
        "pdpl_article",
        "dieu_luat"
    ],
    "examples_vi": [
        "ví dụ",
        "vi du",
        "ví dụ tiếng Việt",
        "vi du tieng viet",
        "examples vi",
        "examples_vi",
        "vi_du"
    ],
    "examples_en": [
        "ví dụ tiếng anh",
        "vi du tieng anh",
        "examples en",
        "examples_en",
        "english examples"
    ]
}


# Category type mapping (Vietnamese/English variations)
CATEGORY_TYPE_MAPPINGS: Dict[str, str] = {
    # Basic category variations
    "cơ bản": "basic",
    "co ban": "basic",
    "basic": "basic",
    "thông thường": "basic",
    "thong thuong": "basic",
    "bình thường": "basic",
    "binh thuong": "basic",
    
    # Sensitive category variations
    "nhạy cảm": "sensitive",
    "nhay cam": "sensitive",
    "sensitive": "sensitive",
    "đặc biệt": "sensitive",
    "dac biet": "sensitive",
    "bảo mật": "sensitive",
    "bao mat": "sensitive"
}


# Boolean mapping for is_sensitive field
BOOLEAN_MAPPINGS: Dict[str, bool] = {
    # Vietnamese Yes
    "có": True,
    "co": True,
    "yes": True,
    "y": True,
    "true": True,
    "1": True,
    "đúng": True,
    "dung": True,
    
    # Vietnamese No
    "không": False,
    "khong": False,
    "no": False,
    "n": False,
    "false": False,
    "0": False,
    "sai": False
}


class ColumnMapper:
    """
    Bộ ánh xạ cột CSV/Excel
    Column mapper for Vietnamese imports
    
    Maps Vietnamese column names to database fields
    """
    
    def __init__(self):
        self.mappings = CATEGORY_COLUMN_MAPPINGS
        self.type_mappings = CATEGORY_TYPE_MAPPINGS
        self.boolean_mappings = BOOLEAN_MAPPINGS
    
    def map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ánh xạ tên cột CSV/Excel sang field database
        Map CSV/Excel columns to database fields
        
        Returns DataFrame with standardized columns
        """
        # Create reverse mapping (alias -> field)
        reverse_mapping = {}
        for field, aliases in self.mappings.items():
            for alias in aliases:
                reverse_mapping[alias.lower()] = field
        
        # Rename columns
        column_rename = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in reverse_mapping:
                column_rename[col] = reverse_mapping[col_lower]
        
        df = df.rename(columns=column_rename)
        
        return df
    
    def normalize_category_type(self, value: str) -> str:
        """
        Chuẩn hóa loại danh mục
        Normalize category type value
        """
        if pd.isna(value):
            return "basic"  # Default
        
        value_lower = str(value).lower().strip()
        return self.type_mappings.get(value_lower, "basic")
    
    def normalize_boolean(self, value: any) -> bool:
        """
        Chuẩn hóa giá trị boolean
        Normalize boolean value
        """
        if pd.isna(value):
            return False
        
        value_lower = str(value).lower().strip()
        return self.boolean_mappings.get(value_lower, False)
```

---

## Import Processing Pipeline

### Pandas-Based File Processor

```python
# services/import/file_processor.py

"""
File Import Processor
Pandas DataFrame Processing
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
from pathlib import Path
import chardet


class FileProcessor:
    """
    Xử lý file import
    File import processor
    
    Pandas-based CSV/Excel processing
    """
    
    def __init__(self):
        self.mapper = ColumnMapper()
        self.validator = PDPLCategoryValidator()
    
    async def process_file(
        self,
        file_path: Path,
        file_type: FileType
    ) -> Tuple[pd.DataFrame, Dict[str, any]]:
        """
        Xử lý file CSV/Excel
        Process CSV/Excel file
        
        Returns DataFrame and metadata
        """
        # Step 1: Load file
        df = await self._load_file(file_path, file_type)
        
        # Step 2: Map columns
        df = self.mapper.map_columns(df)
        
        # Step 3: Normalize values
        df = self._normalize_values(df)
        
        # Step 4: Validate rows
        validation_results = self._validate_rows(df)
        
        metadata = {
            "total_rows": len(df),
            "valid_rows": validation_results["valid_count"],
            "invalid_rows": validation_results["invalid_count"],
            "columns_mapped": list(df.columns),
            "validation_errors": validation_results["errors"]
        }
        
        return df, metadata
    
    async def _load_file(
        self,
        file_path: Path,
        file_type: FileType
    ) -> pd.DataFrame:
        """Tải file CSV/Excel"""
        if file_type == FileType.CSV:
            # Detect encoding
            encoding = self._detect_encoding(file_path)
            
            # Try different delimiters
            for delimiter in CSV_DELIMITERS:
                try:
                    df = pd.read_csv(
                        file_path,
                        encoding=encoding,
                        delimiter=delimiter,
                        skip_blank_lines=True
                    )
                    
                    if len(df.columns) > 1:
                        return df
                except Exception:
                    continue
            
            # Fallback to default delimiter
            df = pd.read_csv(file_path, encoding=encoding)
            
        elif file_type in [FileType.XLSX, FileType.XLS]:
            df = pd.read_excel(file_path)
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return df
    
    def _detect_encoding(self, file_path: Path) -> str:
        """Phát hiện encoding của file"""
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            if encoding not in SUPPORTED_ENCODINGS:
                encoding = DEFAULT_ENCODING
            
            return encoding
    
    def _normalize_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Chuẩn hóa giá trị trong DataFrame"""
        # Normalize category_type
        if 'category_type' in df.columns:
            df['category_type'] = df['category_type'].apply(
                self.mapper.normalize_category_type
            )
        
        # Normalize is_sensitive
        if 'is_sensitive' in df.columns:
            df['is_sensitive'] = df['is_sensitive'].apply(
                self.mapper.normalize_boolean
            )
        else:
            # Auto-set based on category_type
            df['is_sensitive'] = df['category_type'].apply(
                lambda x: x == 'sensitive'
            )
        
        return df
    
    def _validate_rows(self, df: pd.DataFrame) -> Dict[str, any]:
        """Kiểm tra validation từng hàng"""
        valid_count = 0
        invalid_count = 0
        errors = []
        
        for idx, row in df.iterrows():
            is_valid, error_msg = self.validator.validate_row(row)
            
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                errors.append({
                    "row": idx + 2,  # +2 for Excel row number (1-indexed + header)
                    "error": error_msg
                })
        
        return {
            "valid_count": valid_count,
            "invalid_count": invalid_count,
            "errors": errors
        }
```

---

## PDPL Validation Rules

### Category Import Validator

```python
# services/import/pdpl_validator.py

"""
PDPL Category Validator
Article 4.13 Compliance Checking
"""

from typing import Tuple
import pandas as pd
import re


class PDPLCategoryValidator:
    """
    Kiểm tra PDPL cho import
    PDPL validator for imports
    
    Validates category data compliance
    """
    
    # Vietnamese diacritics pattern
    VIETNAMESE_DIACRITICS_PATTERN = re.compile(
        r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]',
        re.IGNORECASE
    )
    
    # Category name length
    CATEGORY_NAME_MIN_LENGTH = 3
    CATEGORY_NAME_MAX_LENGTH = 200
    
    # Description length
    DESCRIPTION_MIN_LENGTH = 10
    DESCRIPTION_MAX_LENGTH = 2000
    
    def validate_row(self, row: pd.Series) -> Tuple[bool, Optional[str]]:
        """
        Kiểm tra một hàng dữ liệu
        Validate single row
        
        Returns (is_valid, error_message)
        """
        # Required field: category_name_vi
        if 'category_name_vi' not in row or pd.isna(row['category_name_vi']):
            return False, "Thiếu tên danh mục tiếng Việt (category_name_vi)"
        
        category_name_vi = str(row['category_name_vi']).strip()
        
        # Check length
        if len(category_name_vi) < self.CATEGORY_NAME_MIN_LENGTH:
            return False, f"Tên danh mục quá ngắn (tối thiểu {self.CATEGORY_NAME_MIN_LENGTH} ký tự)"
        
        if len(category_name_vi) > self.CATEGORY_NAME_MAX_LENGTH:
            return False, f"Tên danh mục quá dài (tối đa {self.CATEGORY_NAME_MAX_LENGTH} ký tự)"
        
        # Check Vietnamese diacritics
        if not self.VIETNAMESE_DIACRITICS_PATTERN.search(category_name_vi):
            return False, "Tên danh mục tiếng Việt phải có dấu (diacritics)"
        
        # Required field: category_description_vi
        if 'category_description_vi' not in row or pd.isna(row['category_description_vi']):
            return False, "Thiếu mô tả danh mục tiếng Việt (category_description_vi)"
        
        description_vi = str(row['category_description_vi']).strip()
        
        if len(description_vi) < self.DESCRIPTION_MIN_LENGTH:
            return False, f"Mô tả quá ngắn (tối thiểu {self.DESCRIPTION_MIN_LENGTH} ký tự)"
        
        if len(description_vi) > self.DESCRIPTION_MAX_LENGTH:
            return False, f"Mô tả quá dài (tối đa {self.DESCRIPTION_MAX_LENGTH} ký tự)"
        
        # Validate category_type and is_sensitive consistency
        if 'category_type' in row and 'is_sensitive' in row:
            category_type = row['category_type']
            is_sensitive = row['is_sensitive']
            
            if category_type == 'sensitive' and not is_sensitive:
                return False, "Danh mục nhạy cảm (sensitive) phải có is_sensitive = True"
            
            if category_type == 'basic' and is_sensitive:
                return False, "Danh mục cơ bản (basic) không thể có is_sensitive = True"
        
        return True, None
```

---

## Error Handling

### Import Error Management

```python
# api/models/import_models.py

"""
Import Models
Vietnamese-first Bulk Import
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime


class ImportPreviewResponse(BaseModel):
    """
    Xem trước import
    Import preview response
    
    Shows validation results before import
    """
    
    import_session_id: UUID
    file_name: str
    file_type: FileType
    file_size_bytes: int
    
    total_rows: int
    valid_rows: int
    invalid_rows: int
    
    columns_detected: List[str]
    columns_mapped: List[str]
    
    validation_errors: List[Dict[str, any]] = Field(
        default_factory=list,
        description="Danh sách lỗi validation | Validation errors list"
    )
    
    can_proceed: bool
    requires_review: bool
    
    preview_data: List[Dict[str, any]] = Field(
        default_factory=list,
        description="10 hàng đầu để xem trước | First 10 rows preview"
    )
    
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "import_session_id": "ff0e8400-e29b-41d4-a716-446655440020",
                "file_name": "data_categories_template.csv",
                "file_type": "csv",
                "file_size_bytes": 2048,
                "total_rows": 15,
                "valid_rows": 13,
                "invalid_rows": 2,
                "columns_detected": ["Tên danh mục", "Mô tả", "Loại"],
                "columns_mapped": ["category_name_vi", "category_description_vi", "category_type"],
                "validation_errors": [
                    {
                        "row": 5,
                        "error": "Tên danh mục tiếng Việt phải có dấu (diacritics)"
                    },
                    {
                        "row": 12,
                        "error": "Mô tả quá ngắn (tối thiểu 10 ký tự)"
                    }
                ],
                "can_proceed": True,
                "requires_review": True,
                "preview_data": [],
                "created_at": "2025-11-06T21:00:00+07:00"
            }
        }


class ImportExecutionRequest(BaseModel):
    """
    Yêu cầu thực hiện import
    Import execution request
    
    Confirms import after preview
    """
    
    import_session_id: UUID
    skip_invalid_rows: bool = Field(
        default=True,
        description="Bỏ qua hàng lỗi | Skip invalid rows"
    )
    
    create_mode: str = Field(
        default="create_new",
        description="create_new hoặc update_existing | create_new or update_existing"
    )


class ImportResultResponse(BaseModel):
    """
    Kết quả import
    Import result response
    
    Final import outcome
    """
    
    import_session_id: UUID
    status: ImportStatus
    
    total_rows: int
    processed_rows: int
    created_count: int
    updated_count: int
    failed_count: int
    
    errors: List[Dict[str, any]] = Field(
        default_factory=list,
        description="Danh sách lỗi | Error list"
    )
    
    processing_time_seconds: float
    completed_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "import_session_id": "ff0e8400-e29b-41d4-a716-446655440020",
                "status": "completed",
                "total_rows": 15,
                "processed_rows": 13,
                "created_count": 13,
                "updated_count": 0,
                "failed_count": 2,
                "errors": [],
                "processing_time_seconds": 2.5,
                "completed_at": "2025-11-06T21:05:00+07:00"
            }
        }
```

---

## Success Criteria

**Implementation Complete When:**

- [TARGET] CSV and Excel file support (CSV, XLSX, XLS)
- [TARGET] Vietnamese column mapping (5+ aliases per field)
- [TARGET] Automatic category type detection (basic/sensitive)
- [TARGET] PDPL Article 4.13 validation
- [TARGET] File encoding detection (UTF-8, Latin1, CP1252, etc.)
- [TARGET] CSV delimiter detection (comma, semicolon, tab, pipe)
- [TARGET] Import preview with validation errors
- [TARGET] Batch processing with transaction support
- [TARGET] Import status tracking (7 statuses)
- [TARGET] Error handling with Vietnamese messages
- [TARGET] Zero hard-coding (all mappings in configuration)
- [TARGET] Vietnamese diacritics enforcement
- [TARGET] Bilingual error messages

**Next Document:** #04 - VeriPortal Wizards
