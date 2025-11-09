# Document #2 - Section 2: Flow Data Models - COMPLETE

## Implementation Summary

**Status:** ✅ COMPLETE  
**Date:** 2025-11-05  
**File:** `models/flow_models.py`  
**Lines:** ~300 lines  
**Tests:** 7/7 passed  

## What Was Implemented

### 1. Pydantic v2 Data Models (5 models)

**Enums (2):**
- `NodeType` - 8 node types for data assets
- `EdgeType` - 7 edge types for data flows

**Pydantic Models (3):**
- `DataAssetNode` - Data asset nodes with Document #1 integration
- `DataFlowEdge` - Data flow edges with PDPL Article 20 compliance
- `FlowGraphMetadata` - Graph-level metadata and compliance summary

### 2. NodeType Enum (8 types)

```python
class NodeType(str, Enum):
    DATABASE = "database"
    API_ENDPOINT = "api_endpoint"
    FILE_SYSTEM = "file_system"
    CLOUD_STORAGE = "cloud_storage"
    THIRD_PARTY_SERVICE = "third_party_service"
    MPS_SYSTEM = "mps_system"
    DATA_SUBJECT = "data_subject"
    PROCESSING_ACTIVITY = "processing_activity"
```

**Purpose:** Categorize data storage and processing locations in Vietnamese PDPL context

### 3. EdgeType Enum (7 types)

```python
class EdgeType(str, Enum):
    DATA_TRANSFER = "data_transfer"
    API_CALL = "api_call"
    FILE_COPY = "file_copy"
    CROSS_BORDER_TRANSFER = "cross_border_transfer"
    THIRD_PARTY_SHARING = "third_party_sharing"
    MPS_NOTIFICATION = "mps_notification"
    USER_ACCESS = "user_access"
```

**Purpose:** Categorize data movement types for PDPL compliance tracking

### 4. DataAssetNode Model (15 fields)

**Core Fields:**
- `node_id: str` - Unique identifier
- `node_type: NodeType` - Type of data asset
- `name: str` - Vietnamese business name
- `location: str` - Physical/logical location
- `vietnamese_region: Optional[str]` - North/Central/South

**PDPL Compliance Fields:**
- `data_categories: List[str]` - Category 1, Category 2, Non-Personal
- `estimated_record_count: Optional[int]` - For MPS threshold calculation
- `sensitive_data: Optional[bool]` - Category 2 flag
- `pdpl_compliant: Optional[bool]` - Compliance status
- `mps_notification_required: Optional[bool]` - MPS reporting flag

**Document #1 Integration Fields:**
- `column_filter_applied: Optional[bool]` - Step 8 integration
- `filter_statistics: Optional[Dict[str, Any]]` - Filtering results

**Validators (2):**
1. `validate_vietnamese_region` - Ensures north/central/south
2. `validate_data_categories` - Ensures Category 1/Category 2/Non-Personal

### 5. DataFlowEdge Model (19 fields)

**Core Fields:**
- `edge_id: str` - Unique identifier
- `source_node_id: str` - Source data asset
- `target_node_id: str` - Target data asset
- `edge_type: EdgeType` - Type of flow

**Flow Characteristics:**
- `data_volume: Optional[str]` - Transfer volume
- `frequency: Optional[str]` - Transfer frequency
- `encryption_enabled: Optional[bool]` - Security flag
- `protocol: Optional[str]` - Transfer protocol

**PDPL Article 20 Cross-Border Fields:**
- `is_cross_border: Optional[bool]` - Auto-detected
- `source_country: Optional[str]` - ISO 2-letter code
- `target_country: Optional[str]` - ISO 2-letter code
- `transfer_mechanism: Optional[str]` - SCC, BCR, consent, MPS approval, adequacy
- `legal_basis: Optional[str]` - consent, contract, legal_obligation, vital_interest, public_task, legitimate_interest

**Compliance Tracking:**
- `mps_notification_sent: Optional[bool]` - MPS reporting status
- `dpa_in_place: Optional[bool]` - Data Processing Agreement
- `data_processing_purpose: Optional[str]` - Business purpose

**Validators (2):**
1. `validate_country_codes` - Ensures 2-letter ISO codes (VN, SG, US)
2. `validate_cross_border_status` - Auto-detects cross-border transfers

**Cross-Border Auto-Detection Logic:**
```python
@model_validator(mode='after')
def validate_cross_border_status(self):
    source = self.source_country if self.source_country else 'VN'
    target = self.target_country if self.target_country else 'VN'
    
    # Cross-border if either source or target is outside Vietnam
    if source != 'VN' or target != 'VN':
        self.is_cross_border = True
    
    return self
```

**Example:** VN → SG transfer automatically sets `is_cross_border = True`

### 6. FlowGraphMetadata Model (12 fields)

**Graph Identification:**
- `graph_id: str` - Unique identifier
- `business_id: str` - Vietnamese business ID
- `business_name: str` - Vietnamese company name
- `primary_region: str` - North/Central/South

**Graph Statistics:**
- `total_nodes: int` - Total data assets
- `total_edges: int` - Total data flows
- `cross_border_flows: int` - International transfers
- `mps_notifications_required: int` - MPS reporting count

**PDPL Category Counts:**
- `category_1_nodes: int` - Basic personal data nodes
- `category_2_nodes: int` - Sensitive data nodes

**Compliance Summary:**
- `overall_compliance: str` - compliant, non_compliant, partial, under_review
- `compliance_issues: List[str]` - List of issues

**Validators (2):**
1. `validate_primary_region` - Ensures north/central/south
2. `validate_compliance_status` - Ensures valid status values

## Verification Results

**All 7 tests passed:**

### Test 1: NodeType Enum ✅
- Verified 8 node types defined correctly
- All enum values accessible

### Test 2: EdgeType Enum ✅
- Verified 7 edge types defined correctly
- All enum values accessible

### Test 3: DataAssetNode Model ✅
- Successfully created node with all fields
- Vietnamese region validation working (north/central/south)
- Data category validation working (Category 1/Category 2/Non-Personal)
- Document #1 integration fields working (column_filter_applied, filter_statistics)

### Test 4: DataFlowEdge Model ✅
- Successfully created domestic edge (VN → VN)
- Successfully created cross-border edge (VN → SG)
- **Cross-border auto-detection working correctly** (VN → SG = True)
- Country code validation working (2-letter ISO)
- Transfer mechanism and legal basis fields working

### Test 5: FlowGraphMetadata Model ✅
- Successfully created metadata with all fields
- Vietnamese region validation working
- Compliance status validation working (compliant/non_compliant/partial/under_review)
- Statistics fields working correctly

### Test 6: Model Serialization ✅
- `model_dump()` working (Pydantic v2)
- `model_dump_json()` working (Pydantic v2)
- All 15 DataAssetNode fields serialized
- All 19 DataFlowEdge fields serialized

### Test 7: Document #1 Integration ✅
- Column filtering integration working
- `column_filter_applied` field working
- `filter_statistics` field with nested dict working
- Timestamp integration working

## Technical Details

### Pydantic v2 Migration

**All validators updated to Pydantic v2 syntax:**

1. **Field Validators (v1 → v2):**
```python
# OLD (Pydantic v1)
@validator('field_name')
def validate_field(cls, v):
    return v

# NEW (Pydantic v2)
@field_validator('field_name')
@classmethod
def validate_field(cls, v):
    return v
```

2. **Model Validators for Cross-Field Logic (v1 → v2):**
```python
# OLD (Pydantic v1)
@validator('is_cross_border')
def validate_cross_border(cls, v, values):
    source = values.get('source_country')
    return v

# NEW (Pydantic v2)
@model_validator(mode='after')
def validate_cross_border(self):
    source = self.source_country
    return self
```

### Vietnamese Diacritics Compliance

**All Vietnamese text uses proper diacritics:**
- Model descriptions in Vietnamese
- Field descriptions with diacritics
- Comments with proper tone marks
- Example values use correct Vietnamese

**Database identifiers remain ASCII-safe:**
- Field names: `vietnamese_region` (not `vùng_việt_nam`)
- Enum values: `cross_border_transfer` (not `chuyển_giao_xuyên_biên_giới`)
- Model names: `DataAssetNode` (English)

## Integration Points

### Document #1 Integration
- `column_filter_applied` - Boolean flag from Step 8
- `filter_statistics` - Dict with total_columns, scanned_columns, filtered_out

### Section 1 Integration (flow_constants.py)
- Uses VIETNAMESE_REGIONS for validation
- Uses COUNTRY_CODES for country validation
- Uses TRANSFER_MECHANISMS for compliance
- Uses LEGAL_BASIS_DESCRIPTIONS for legal basis

### Section 3 Preview (flow_graph.py)
- `DataAssetNode` will be nodes in NetworkX graph
- `DataFlowEdge` will be edges in NetworkX graph
- `FlowGraphMetadata` will track graph-level statistics

## File Structure

```
backend/veri_ai_data_inventory/
├── config/
│   └── flow_constants.py          # Section 1 (COMPLETE)
├── models/
│   └── flow_models.py             # Section 2 (COMPLETE) ← THIS FILE
└── graph/
    └── flow_graph.py              # Section 3 (NEXT)
```

## Next Steps

**Section 3: Flow Graph Database (flow_graph.py)**
- Implement NetworkX DiGraph wrapper
- Add/remove nodes and edges
- Query data lineage
- Detect cross-border flows
- Find circular flows
- Generate graph statistics

**Estimated:** ~300 lines, 3-4 hours

## Critical Success Factors

✅ **Pydantic v2 compatibility** - All validators updated correctly  
✅ **Cross-border auto-detection** - VN ↔ other countries detected automatically  
✅ **Vietnamese region validation** - North/Central/South standardized  
✅ **PDPL category validation** - Category 1/Category 2/Non-Personal enforced  
✅ **Document #1 integration** - Column filtering fields working  
✅ **Model serialization** - JSON export working for API integration  
✅ **Vietnamese diacritics** - Proper usage in user-facing text  
✅ **Database-safe identifiers** - ASCII field names maintained  

## Completion Checklist

- [x] NodeType enum defined (8 types)
- [x] EdgeType enum defined (7 types)
- [x] DataAssetNode model created (15 fields)
- [x] DataFlowEdge model created (19 fields)
- [x] FlowGraphMetadata model created (12 fields)
- [x] Region validators implemented (north/central/south)
- [x] Category validators implemented (Cat1/Cat2/Non-Personal)
- [x] Country code validators implemented (2-letter ISO)
- [x] Cross-border auto-detection implemented (VN ↔ other)
- [x] Pydantic v2 syntax updated (field_validator, model_validator)
- [x] Document #1 integration fields added
- [x] Model serialization tested (model_dump, model_dump_json)
- [x] All 7 verification tests passed
- [x] Vietnamese diacritics used in comments/docs
- [x] ASCII-safe field names used
- [x] Documentation created (this file)

---

**Section 2 Status:** ✅ COMPLETE - Ready for Section 3 implementation
