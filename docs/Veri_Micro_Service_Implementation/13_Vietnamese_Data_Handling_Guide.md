# Vietnamese Data Handling Guide - VeriSyntra Microservices

**Document Version:** 1.0.0  
**Date:** November 1, 2025  
**Purpose:** Best practices for Vietnamese text encoding, data handling, and pattern recognition across VeriSyntra microservices

---

## Executive Summary

This guide provides comprehensive documentation for handling Vietnamese text and data patterns across VeriSyntra's microservices architecture. Vietnamese text requires special handling due to diacritics (á, ă, â, đ, ê, ô, ơ, ư), unique data formats (CMND/CCCD, phone numbers, addresses), and UTF-8 encoding requirements.

**Key Principles:**
- **UTF-8 encoding everywhere** - Database connections, file I/O, API communications
- **Service delegation pattern** - Generic services delegate Vietnamese pattern recognition to specialized services
- **Diacritics preservation** - Never strip or normalize Vietnamese diacritics
- **Regional awareness** - Recognize North/Central/South Vietnamese variations

---

## 1. Vietnamese Character Set and Encoding

### 1.1 Vietnamese Diacritics

**Complete Vietnamese Character Set:**

**Vowels with diacritics:**
```
a: á, à, ả, ã, ạ
ă: ắ, ằ, ẳ, ẵ, ặ
â: ấ, ầ, ẩ, ẫ, ậ
e: é, è, ẻ, ẽ, ẹ
ê: ế, ề, ể, ễ, ệ
i: í, ì, ỉ, ĩ, ị
o: ó, ò, ỏ, õ, ọ
ô: ố, ồ, ổ, ỗ, ộ
ơ: ớ, ờ, ở, ỡ, ợ
u: ú, ù, ủ, ũ, ụ
ư: ứ, ừ, ử, ữ, ự
y: ý, ỳ, ỷ, ỹ, ỵ
```

**Special consonant:**
```
đ (d with stroke) - CRITICAL: Not regular 'd'
```

**Total: 134 Vietnamese characters** (including uppercase variants)

### 1.2 UTF-8 Encoding Requirements

**Why UTF-8 is mandatory:**
- Vietnamese diacritics are multi-byte characters
- ASCII (7-bit) cannot represent Vietnamese characters
- Latin-1 (ISO-8859-1) missing Vietnamese-specific characters
- Windows-1252 has incomplete Vietnamese support

**UTF-8 Byte Sequences for Vietnamese:**
```python
# Examples of Vietnamese characters in UTF-8
'đ' -> b'\xc4\x91' (2 bytes)
'ă' -> b'\xc4\x83' (2 bytes)
'ơ' -> b'\xc6\xa1' (2 bytes)
'Nguyễn' -> b'Nguy\xe1\xbb\x85n' (8 bytes, 6 characters)
```

**Common Encoding Issues:**
```python
# [ERROR] Incorrect approaches
name = "Nguyễn Văn A"
name.encode('ascii')  # UnicodeEncodeError
name.encode('latin-1')  # UnicodeEncodeError

# [OK] Correct approach
name.encode('utf-8')  # b'Nguy\xe1\xbb\x85n V\xc4\x83n A'
```

---

## 2. Database Configuration for Vietnamese Text

### 2.1 PostgreSQL Configuration

**Connection String:**
```python
# [OK] Force UTF-8 encoding
DATABASE_URL = "postgresql://user:pass@host:5432/db?client_encoding=utf8"

# SQLAlchemy engine
from sqlalchemy import create_engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
    pool_pre_ping=True
)
```

**Database and Table Creation:**
```sql
-- Create database with UTF-8 encoding
CREATE DATABASE verisyntra
    ENCODING = 'UTF8'
    LC_COLLATE = 'vi_VN.UTF-8'
    LC_CTYPE = 'vi_VN.UTF-8'
    TEMPLATE = template0;

-- Create table with Vietnamese column names
CREATE TABLE khach_hang (
    id SERIAL PRIMARY KEY,
    ho_ten VARCHAR(255) NOT NULL,           -- Vietnamese: Full name
    so_cmnd VARCHAR(12),                    -- Vietnamese: National ID
    dia_chi TEXT,                           -- Vietnamese: Address
    so_dien_thoai VARCHAR(15),              -- Vietnamese: Phone number
    email VARCHAR(255),
    ngay_sinh DATE,                         -- Vietnamese: Date of birth
    gioi_tinh VARCHAR(10),                  -- Vietnamese: Gender
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert Vietnamese data
INSERT INTO khach_hang (ho_ten, so_cmnd, dia_chi, so_dien_thoai)
VALUES 
    ('Nguyễn Văn A', '001234567890', 'Số 1 Đường Lê Lợi, Quận 1, TP.HCM', '0901234567'),
    ('Trần Thị B', '079123456789', 'Phường Hoàn Kiếm, Hà Nội', '0912345678');
```

**Query Vietnamese Data:**
```python
from sqlalchemy import text

# [OK] Query with Vietnamese column names
def get_vietnamese_customers():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT ho_ten, so_cmnd, dia_chi 
            FROM khach_hang 
            WHERE ho_ten LIKE :pattern
        """), {"pattern": "%Nguyễn%"})
        
        for row in result:
            # Ensure UTF-8 decoding
            ho_ten = row[0]  # Already Unicode string
            print(f"Customer: {ho_ten}")
```

### 2.2 MongoDB Configuration

**Connection with UTF-8:**
```python
from pymongo import MongoClient

# [OK] MongoDB with UTF-8 validation
client = MongoClient(
    "mongodb://localhost:27017/",
    unicode_decode_error_handler='strict'  # Fail on invalid UTF-8
)

db = client['verisyntra']

# Insert Vietnamese document
db.customers.insert_one({
    "ho_ten": "Nguyễn Văn A",
    "so_cmnd": "001234567890",
    "dia_chi": {
        "tinh_thanh": "TP. Hồ Chí Minh",  # Vietnamese: City/Province
        "quan_huyen": "Quận 1",            # Vietnamese: District
        "phuong_xa": "Phường Bến Nghé",    # Vietnamese: Ward
        "dia_chi_chi_tiet": "Số 1 Đường Lê Lợi"
    }
})

# Query with Vietnamese field names
customers = db.customers.find({"ho_ten": {"$regex": "Nguyễn"}})
for customer in customers:
    print(customer["ho_ten"])  # UTF-8 preserved
```

### 2.3 MySQL Configuration

**Connection String:**
```python
# [OK] MySQL with UTF-8mb4 (full Unicode support)
DATABASE_URL = "mysql+pymysql://user:pass@host:3306/db?charset=utf8mb4"

# Create table with utf8mb4 collation
CREATE TABLE khach_hang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ho_ten VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    so_cmnd VARCHAR(12),
    dia_chi TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 3. Vietnamese Data Patterns and Formats

### 3.1 Vietnamese Names

**Name Structure:**
```
[Family Name] [Middle Name(s)] [Given Name]
Example: Nguyễn Văn A
- Family: Nguyễn (most common: Nguyễn, Trần, Lê, Phạm, Hoàng)
- Middle: Văn (common: Văn, Thị, Đức, Hữu, etc.)
- Given: A
```

**Common Vietnamese Family Names:**
```python
VIETNAMESE_FAMILY_NAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
    "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh", "Đào", "Mai", "Lâm"
]

def is_vietnamese_name(name: str) -> bool:
    """Check if name is likely Vietnamese"""
    # Check for Vietnamese diacritics
    vietnamese_chars = 'áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ'
    
    if any(char in name.lower() for char in vietnamese_chars):
        return True
    
    # Check family name
    parts = name.split()
    if parts and parts[0] in VIETNAMESE_FAMILY_NAMES:
        return True
    
    return False
```

### 3.2 Vietnamese National ID (CMND/CCCD)

**CMND (Chứng Minh Nhân Dân) - Old format:**
```
9 digits or 12 digits
Format: [Province Code (3 digits)][Year Code (2 digits)][Serial (4-7 digits)]
Example: 001234567 (9 digits) or 001234567890 (12 digits)
```

**CCCD (Căn Cước Công Dân) - New format:**
```
12 digits
Format: [0][Province Code (2 digits)][YY (2 digits)][Gender (1 digit)][Serial (6 digits)]
Example: 079123456789
- 0: Country code (Vietnam)
- 79: Province code (HCMC)
- 12: Year 2012
- 3: Gender (odd=male, even=female)
- 456789: Serial number
```

**Pattern Recognition:**
```python
import re

def classify_vietnamese_national_id(value: str) -> dict:
    """Classify Vietnamese national ID format"""
    # Remove spaces and hyphens
    clean_value = re.sub(r'[\s-]', '', value)
    
    # CMND: 9 or 12 digits
    if re.match(r'^\d{9}$', clean_value):
        return {
            "type": "CMND",
            "format": "9_digit",
            "pdpl_category": "sensitive_data",
            "vietnamese_format": True
        }
    
    # CMND: 12 digits (old style)
    if re.match(r'^\d{12}$', clean_value) and not clean_value.startswith('0'):
        return {
            "type": "CMND",
            "format": "12_digit",
            "pdpl_category": "sensitive_data",
            "vietnamese_format": True
        }
    
    # CCCD: 12 digits starting with 0
    if re.match(r'^0\d{11}$', clean_value):
        province_code = clean_value[1:3]
        year = clean_value[3:5]
        gender = int(clean_value[5])
        
        return {
            "type": "CCCD",
            "format": "12_digit_new",
            "province_code": province_code,
            "year": f"20{year}",
            "gender": "male" if gender % 2 == 1 else "female",
            "pdpl_category": "sensitive_data",
            "vietnamese_format": True
        }
    
    return {"type": "unknown", "vietnamese_format": False}
```

### 3.3 Vietnamese Phone Numbers

**Format:**
```
Mobile: 10 digits starting with 0
Format: [0][Network Code (2-3 digits)][Subscriber Number (6-7 digits)]
Examples:
- 0901234567 (Viettel)
- 0912345678 (Vinaphone)
- 0981234567 (Mobifone)

Landline: 
- Hanoi: 024 + 7-8 digits
- HCMC: 028 + 7-8 digits
- Da Nang: 0236 + 6-7 digits
```

**Pattern Recognition:**
```python
VIETNAMESE_MOBILE_PREFIXES = {
    "Viettel": ["086", "096", "097", "098", "032", "033", "034", "035", "036", "037", "038", "039"],
    "Vinaphone": ["088", "091", "094", "083", "084", "085", "081", "082"],
    "Mobifone": ["089", "090", "093", "070", "079", "077", "076", "078"],
    "Vietnamobile": ["092", "056", "058"],
    "Gmobile": ["099", "059"]
}

def classify_vietnamese_phone(value: str) -> dict:
    """Classify Vietnamese phone number"""
    clean_value = re.sub(r'[\s\-\(\)]', '', value)
    
    # Mobile: 10 digits starting with 0
    if re.match(r'^0\d{9}$', clean_value):
        prefix = clean_value[1:4]
        
        for carrier, prefixes in VIETNAMESE_MOBILE_PREFIXES.items():
            if prefix in prefixes:
                return {
                    "type": "mobile",
                    "carrier": carrier,
                    "format": "vietnamese_mobile",
                    "pdpl_category": "regular_data"
                }
    
    # Landline: Hanoi (024)
    if re.match(r'^024\d{7,8}$', clean_value):
        return {"type": "landline", "region": "hanoi", "format": "vietnamese_landline"}
    
    # Landline: HCMC (028)
    if re.match(r'^028\d{7,8}$', clean_value):
        return {"type": "landline", "region": "hcmc", "format": "vietnamese_landline"}
    
    return {"type": "unknown", "vietnamese_format": False}
```

### 3.4 Vietnamese Addresses

**Address Structure:**
```
[Number] [Street], [Ward], [District], [Province/City]

Example: Số 1 Đường Lê Lợi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh

Components:
- Số: Number (e.g., "Số 1")
- Đường: Street (e.g., "Đường Lê Lợi")
- Phường/Xã: Ward (e.g., "Phường Bến Nghé")
- Quận/Huyện: District (e.g., "Quận 1")
- Tỉnh/Thành phố: Province/City (e.g., "TP. Hồ Chí Minh")
```

**Address Keywords:**
```python
VIETNAMESE_ADDRESS_KEYWORDS = {
    "number": ["Số", "số"],
    "street": ["Đường", "đường", "Phố", "phố"],
    "ward": ["Phường", "phường", "Xã", "xã"],
    "district": ["Quận", "quận", "Huyện", "huyện", "Thị xã", "thị xã"],
    "province": ["Tỉnh", "tỉnh", "Thành phố", "thành phố", "TP.", "TP"]
}

def is_vietnamese_address(text: str) -> bool:
    """Check if text is likely a Vietnamese address"""
    # Check for Vietnamese address keywords
    keywords_found = 0
    for category, keywords in VIETNAMESE_ADDRESS_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            keywords_found += 1
    
    # Likely an address if 2+ categories found
    return keywords_found >= 2
```

---

## 4. Service-Specific Vietnamese Handling

### 4.1 veri-ai-data-inventory (Generic with UTF-8 Support)

**Role:** Generic data discovery with Vietnamese text preservation

**UTF-8 Configuration:**
```python
# File: services/veri-ai-data-inventory/config.py
import os

class Config:
    # Force UTF-8 encoding
    PYTHONIOENCODING = 'utf-8'
    LANG = 'C.UTF-8'
    LC_ALL = 'C.UTF-8'
    
    # Database connections with UTF-8
    DATABASE_URL = os.getenv('DATABASE_URL', '') + '?client_encoding=utf8'
    MONGODB_URL = os.getenv('MONGODB_URL', '')
    
    # Service integration
    CLASSIFICATION_SERVICE = 'http://veri-vi-ai-classification:8006'
    NLP_SERVICE = 'http://veri-vi-nlp-processor:8007'
```

**Vietnamese Text Validation:**
```python
# File: services/veri-ai-data-inventory/utils/vietnamese_validator.py
import logging

logger = logging.getLogger(__name__)

class VietnameseTextValidator:
    """Validator for Vietnamese text encoding"""
    
    VIETNAMESE_DIACRITICS = 'áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ'
    
    @staticmethod
    def validate_utf8(text: str) -> bool:
        """Validate UTF-8 encoding"""
        try:
            text.encode('utf-8').decode('utf-8')
            return True
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            logger.error(f"UTF-8 validation failed: {e}")
            return False
    
    @staticmethod
    def has_vietnamese_diacritics(text: str) -> bool:
        """Check if text contains Vietnamese diacritics"""
        return any(char in text.lower() for char in VietnameseTextValidator.VIETNAMESE_DIACRITICS)
    
    @staticmethod
    def clean_and_validate(text: str) -> tuple[str, bool]:
        """Clean and validate Vietnamese text"""
        # Strip whitespace
        clean_text = text.strip()
        
        # Validate UTF-8
        is_valid = VietnameseTextValidator.validate_utf8(clean_text)
        
        if not is_valid:
            logger.warning(f"Invalid Vietnamese text: {text[:50]}...")
        
        return clean_text, is_valid
```

**Database Scanning with Vietnamese Support:**
```python
# File: services/veri-ai-data-inventory/scanners/database_scanner.py
from sqlalchemy import create_engine, text
from utils.vietnamese_validator import VietnameseTextValidator

class DatabaseScanner:
    """Database scanner with Vietnamese text support"""
    
    def __init__(self, connection_string: str):
        # Force UTF-8 encoding
        if 'postgresql' in connection_string and 'client_encoding' not in connection_string:
            connection_string += '?client_encoding=utf8'
        
        self.engine = create_engine(
            connection_string,
            connect_args={"options": "-c client_encoding=utf8"}
        )
        self.validator = VietnameseTextValidator()
    
    def scan_table(self, table_name: str) -> dict:
        """Scan table with Vietnamese column name support"""
        with self.engine.connect() as conn:
            # Get columns
            columns = conn.execute(text(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = :table
            """), {"table": table_name})
            
            results = []
            for column_name, data_type in columns:
                # Validate Vietnamese column name
                _, is_valid = self.validator.clean_and_validate(column_name)
                
                if not is_valid:
                    logger.warning(f"Invalid UTF-8 in column: {table_name}.{column_name}")
                    continue
                
                # Extract sample data
                samples = self.extract_samples(conn, table_name, column_name)
                
                # Delegate to Vietnamese classification service
                classification = self.classify_field(column_name, data_type, samples)
                
                results.append({
                    "column_name": column_name,
                    "data_type": data_type,
                    "samples": samples,
                    "classification": classification,
                    "has_vietnamese_text": self.validator.has_vietnamese_diacritics(column_name)
                })
            
            return {
                "table_name": table_name,
                "columns": results,
                "vietnamese_text_detected": any(r["has_vietnamese_text"] for r in results)
            }
    
    def extract_samples(self, conn, table_name: str, column_name: str, limit: int = 100) -> list:
        """Extract sample data with Vietnamese text preservation"""
        query = text(f'SELECT "{column_name}" FROM "{table_name}" WHERE "{column_name}" IS NOT NULL LIMIT :limit')
        result = conn.execute(query, {"limit": limit})
        
        samples = []
        for row in result:
            value = row[0]
            if value:
                # Validate Vietnamese text
                _, is_valid = self.validator.clean_and_validate(str(value))
                if is_valid:
                    samples.append(str(value))
        
        return samples[:100]  # Limit to 100 samples
```

### 4.2 veri-vi-ai-classification (Vietnamese Specialist)

**Role:** Vietnamese-specific pattern recognition and classification

**Vietnamese Pattern Library:**
```python
# File: services/veri-vi-ai-classification/patterns/vietnamese_patterns.py

VIETNAMESE_PATTERNS = {
    "national_id": {
        "cmnd_9": r'^\d{9}$',
        "cmnd_12": r'^[1-9]\d{11}$',
        "cccd": r'^0\d{11}$'
    },
    "phone": {
        "mobile": r'^0\d{9}$',
        "landline_hanoi": r'^024\d{7,8}$',
        "landline_hcmc": r'^028\d{7,8}$'
    },
    "name_fields": [
        "ho_ten", "họ_tên", "ten", "tên", "full_name",
        "ho", "họ", "ten_dem", "tên_đệm", "ten_lot",
        "customer_name", "employee_name"
    ],
    "address_fields": [
        "dia_chi", "địa_chỉ", "address", "so_nha", "số_nhà",
        "duong", "đường", "pho", "phố", "phuong", "phường",
        "quan", "quận", "huyen", "huyện", "tinh", "tỉnh"
    ],
    "id_fields": [
        "cmnd", "cccd", "so_cmnd", "số_cmnd", "so_cccd", "số_cccd",
        "national_id", "identity_card"
    ]
}
```

### 4.3 veri-vi-nlp-processor (Vietnamese NLP)

**Role:** Vietnamese text preprocessing and tokenization

**VnCoreNLP Integration:**
```java
// File: services/veri-vi-nlp-processor/src/main/java/VnCoreNLPService.java
import vn.pipeline.*;

public class VnCoreNLPService {
    private VnCoreNLP pipeline;
    
    public VnCoreNLPService() throws IOException {
        // Initialize VnCoreNLP with Vietnamese models
        String[] annotators = {"wseg", "pos", "ner"};
        this.pipeline = new VnCoreNLP(annotators);
    }
    
    public VietnameseTokens tokenize(String vietnameseText) {
        // Tokenize Vietnamese text
        // Example: "Nguyễn Văn A" -> ["Nguyễn", "Văn", "A"]
        Annotation annotation = new Annotation(vietnameseText);
        pipeline.annotate(annotation);
        
        return new VietnameseTokens(annotation);
    }
}
```

---

## 5. Docker Configuration for Vietnamese Support

### 5.1 Dockerfile with UTF-8 Locale

**Standard Vietnamese-Ready Dockerfile:**
```dockerfile
FROM python:3.11-slim

# CRITICAL: Set UTF-8 locale for Vietnamese text
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=utf-8

WORKDIR /app

# Install system dependencies with locale support
RUN apt-get update && apt-get install -y \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Generate UTF-8 locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "vi_VN.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Service-specific port (example: 8010 for veri-ai-data-inventory)
EXPOSE 8010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
```

### 5.2 Docker Compose Configuration

**docker-compose.yml with Vietnamese encoding:**
```yaml
version: '3.8'

services:
  veri-ai-data-inventory:
    build: ./services/veri-ai-data-inventory
    environment:
      # Vietnamese text encoding
      - LANG=C.UTF-8
      - LC_ALL=C.UTF-8
      - PYTHONIOENCODING=utf-8
      
      # Database with UTF-8
      - DATABASE_URL=postgresql://user:pass@postgres:5432/verisyntra?client_encoding=utf8
      - MONGODB_URL=mongodb://mongo:27017/verisyntra
      
      # Service integration
      - CLASSIFICATION_SERVICE_URL=http://veri-vi-ai-classification:8006
      - NLP_SERVICE_URL=http://veri-vi-nlp-processor:8007
    depends_on:
      - postgres
      - mongo
      - veri-vi-ai-classification
      - veri-vi-nlp-processor
  
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=verisyntra
      - POSTGRES_USER=veriuser
      - POSTGRES_PASSWORD=secure_password
      # CRITICAL: UTF-8 encoding
      - POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=C.UTF-8
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

---

## 6. Testing Vietnamese Text Handling

### 6.1 Unit Tests

**Test UTF-8 Encoding:**
```python
# File: tests/test_vietnamese_encoding.py
import pytest

def test_vietnamese_diacritics():
    """Test Vietnamese diacritics preservation"""
    test_names = [
        "Nguyễn Văn A",
        "Trần Thị Hương",
        "Lê Đức Anh",
        "Phạm Thị Phượng"
    ]
    
    for name in test_names:
        # Encode and decode
        encoded = name.encode('utf-8')
        decoded = encoded.decode('utf-8')
        
        assert name == decoded, f"Diacritics lost: {name} != {decoded}"

def test_vietnamese_column_names():
    """Test Vietnamese database column names"""
    columns = ["ho_ten", "so_cmnd", "dia_chi", "so_dien_thoai"]
    
    for column in columns:
        # Should be valid UTF-8
        assert column.encode('utf-8').decode('utf-8') == column

def test_vietnamese_address():
    """Test Vietnamese address preservation"""
    address = "Số 1 Đường Lê Lợi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh"
    
    # Should preserve all diacritics
    encoded = address.encode('utf-8')
    decoded = encoded.decode('utf-8')
    
    assert address == decoded
    assert 'Đường' in decoded
    assert 'Hồ Chí Minh' in decoded
```

### 6.2 Integration Tests

**Test Database Scanning:**
```python
# File: tests/integration/test_vietnamese_database_scan.py
import pytest
from services.veri_data_inventory.scanners import DatabaseScanner

@pytest.fixture
def vietnamese_test_db():
    """Create test database with Vietnamese data"""
    # Setup test database
    conn = create_test_database()
    
    # Create table with Vietnamese column names
    conn.execute("""
        CREATE TABLE test_khach_hang (
            id SERIAL PRIMARY KEY,
            ho_ten VARCHAR(255),
            so_cmnd VARCHAR(12),
            dia_chi TEXT,
            so_dien_thoai VARCHAR(15)
        )
    """)
    
    # Insert Vietnamese test data
    conn.execute("""
        INSERT INTO test_khach_hang (ho_ten, so_cmnd, dia_chi, so_dien_thoai)
        VALUES 
            ('Nguyễn Văn A', '001234567890', 'Số 1 Đường Lê Lợi, Quận 1, TP.HCM', '0901234567'),
            ('Trần Thị B', '079123456789', 'Phường Hoàn Kiếm, Hà Nội', '0912345678')
    """)
    
    yield conn
    conn.close()

def test_scan_vietnamese_table(vietnamese_test_db):
    """Test scanning table with Vietnamese data"""
    scanner = DatabaseScanner(vietnamese_test_db.url)
    
    # Scan table
    result = scanner.scan_table("test_khach_hang")
    
    # Verify Vietnamese column names preserved
    column_names = [col["column_name"] for col in result["columns"]]
    assert "ho_ten" in column_names
    assert "so_cmnd" in column_names
    assert "dia_chi" in column_names
    
    # Verify Vietnamese data preserved
    ho_ten_column = next(col for col in result["columns"] if col["column_name"] == "ho_ten")
    samples = ho_ten_column["samples"]
    
    assert any("Nguyễn" in sample for sample in samples)
    assert any("Trần" in sample for sample in samples)
```

---

## 7. Common Issues and Solutions

### 7.1 Encoding Issues

**Issue: "UnicodeEncodeError: 'ascii' codec can't encode character"**

```python
# [ERROR] Causes
print("Nguyễn Văn A".encode('ascii'))  # UnicodeEncodeError

# [OK] Solution
print("Nguyễn Văn A".encode('utf-8'))  # Works
```

**Issue: Database returns garbled Vietnamese text**

```sql
-- [ERROR] Wrong encoding
\encoding LATIN1
SELECT ho_ten FROM khach_hang;  -- Returns garbage

-- [OK] Correct encoding
\encoding UTF8
SELECT ho_ten FROM khach_hang;  -- Returns "Nguyễn Văn A"
```

### 7.2 Docker Locale Issues

**Issue: Vietnamese text not displaying in container**

```dockerfile
# [ERROR] Missing locale configuration
FROM python:3.11-slim
# Vietnamese text will be garbled

# [OK] Add locale support
FROM python:3.11-slim
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
RUN apt-get update && apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
```

---

## 8. Summary and Best Practices

### 8.1 Checklist for Vietnamese Text Support

- [ ] **Database connections:** Force UTF-8 encoding (`?client_encoding=utf8`)
- [ ] **Docker containers:** Set `LANG=C.UTF-8`, `LC_ALL=C.UTF-8`, `PYTHONIOENCODING=utf-8`
- [ ] **Database tables:** Use UTF-8 collation (`utf8mb4_unicode_ci` for MySQL)
- [ ] **Python code:** Never use `.encode('ascii')` or `.encode('latin-1')`
- [ ] **Service delegation:** Generic services delegate Vietnamese pattern recognition
- [ ] **Testing:** Include Vietnamese diacritics in all test cases
- [ ] **API responses:** Ensure JSON responses preserve UTF-8

### 8.2 Service Delegation Pattern

**Architecture:**
```
veri-ai-data-inventory (Generic Scanner)
  |
  |-- UTF-8 encoding for Vietnamese text
  |-- Validates Vietnamese column names
  |-- Extracts Vietnamese data samples
  |
  +-> Delegates to veri-vi-nlp-processor
  |     |-- Vietnamese tokenization
  |     |-- VnCoreNLP preprocessing
  |
  +-> Delegates to veri-vi-ai-classification
        |-- Vietnamese pattern recognition
        |-- CMND/CCCD detection
        |-- Vietnamese name/address classification
```

---

**Document End**
