# Document #2 - Section 4: Flow Discovery Service - COMPLETE

## Implementation Summary

**Status:** ✅ COMPLETE  
**Date:** 2025-11-04  
**File:** `services/flow_discovery_service.py`  
**Lines:** ~420 lines  
**Tests:** 14/14 passed  

## What Was Implemented

### 1. FlowDiscoveryService Class - Automated Flow Detection

**Purpose:** Discover data flows automatically from database metadata and API configurations for Vietnamese PDPL 2025 compliance

**Core Features:**
- Automated database flow discovery
- Automated API flow discovery
- Vietnamese region detection from locations
- IP geolocation to country codes
- Data category auto-classification from table names
- Cross-border flow auto-detection
- MPS threshold analysis
- Processing purpose tracking

### 2. Class Structure

```python
class FlowDiscoveryService:
    def __init__(self, graph: DataFlowGraph):
        self.graph = graph                    # DataFlowGraph from Section 3
        self.config = FlowMappingConfig()     # Section 1 config
        self.discovered_nodes = []            # Track discovered nodes
        self.discovered_edges = []            # Track discovered edges
```

**Integration Points:**
- **Section 1:** Uses `FlowMappingConfig` for thresholds and keywords
- **Section 2:** Creates `DataAssetNode` and `DataFlowEdge` models
- **Section 3:** Populates `DataFlowGraph` with discovered flows

### 3. Core Methods (7 total)

#### Discovery Methods (2)

**1. discover_database_flows(database_metadata: List[Dict]) -> Dict**

Discovers data flows from database connection metadata

**Input Format:**
```python
database_metadata = [
    {
        'database_id': 'db_customers_hanoi',
        'database_name': 'Cơ sở dữ liệu khách hàng Hà Nội',
        'location': 'Hanoi, Vietnam',
        'tables': ['customers', 'orders', 'addresses', 'cccd_info'],
        'estimated_records': 25000,
        'connections': [
            {
                'target_database_id': 'db_analytics_hcm',
                'purpose': 'Phân tích dữ liệu khách hàng'
            }
        ]
    }
]
```

**Processing Steps:**
1. **First Pass - Add Nodes:**
   - Extract database metadata
   - Detect Vietnamese region from location
   - Auto-classify data categories from table names
   - Determine sensitive data flag (Category 2 present)
   - Check MPS notification requirement
   - Create DataAssetNode with NodeType.DATABASE
   - Add node to graph

2. **Second Pass - Add Edges:**
   - For each connection in database metadata
   - Geolocate source and target countries
   - Detect cross-border transfers
   - Create DataFlowEdge with appropriate EdgeType
   - Store processing purpose in metadata
   - Add edge to graph

**Output:**
```python
{
    'nodes_added': 3,
    'edges_added': 2,
    'total_nodes': 3,
    'total_edges': 2
}
```

**Vietnamese Translation:** Phát hiện luồng dữ liệu từ metadata cơ sở dữ liệu

---

**2. discover_api_flows(api_metadata: List[Dict]) -> Dict**

Discovers data flows from API endpoint configurations

**Input Format:**
```python
api_metadata = [
    {
        'api_id': 'api_customer_service',
        'api_name': 'API Dịch vụ khách hàng',
        'endpoint_url': 'https://api.verisyntra.vn/customers',
        'location': 'Da Nang, Vietnam',
        'data_sources': ['db_customers_hanoi'],      # Input databases
        'data_targets': ['db_analytics_hcm'],        # Output databases
        'estimated_requests_per_day': 50000
    }
]
```

**Processing Steps:**
1. **Create API Node:**
   - Extract API metadata
   - Detect Vietnamese region
   - Create DataAssetNode with NodeType.API_ENDPOINT
   - Set data_categories to ['Category 1'] (APIs handle basic data)
   - Add node to graph

2. **Create Input Edges:**
   - For each data_source, create edge: source → API
   - EdgeType.API_CALL
   - Real-time frequency
   - Check cross-border status

3. **Create Output Edges:**
   - For each data_target, create edge: API → target
   - EdgeType.API_CALL
   - Real-time frequency
   - Check cross-border status

**Output:**
```python
{
    'nodes_added': 2,
    'edges_added': 4,  # 2 inputs + 2 outputs
    'total_nodes': 5,
    'total_edges': 6
}
```

**Vietnamese Translation:** Phát hiện luồng dữ liệu từ metadata API

---

#### Helper Methods (5)

**3. _detect_region(location: str) -> Optional[str]**

Detects Vietnamese region from location string

**Detection Logic:**
1. Check against `FlowMappingConfig.VIETNAMESE_REGIONS` (Section 1)
   - North: Hanoi, Hai Phong, etc.
   - Central: Da Nang, Hue, etc.
   - South: Ho Chi Minh, Can Tho, etc.

2. Fallback keyword matching:
   - North keywords: 'hanoi', 'hà nội', 'haiphong', 'north', 'bắc'
   - Central keywords: 'danang', 'đà nẵng', 'hue', 'huế', 'central', 'trung'
   - South keywords: 'saigon', 'hồ chí minh', 'hcmc', 'south', 'nam'

3. Return None if not in Vietnam

**Examples:**
```python
_detect_region("Hanoi, Vietnam")          # -> 'north'
_detect_region("Hồ Chí Minh City")        # -> 'south'
_detect_region("Đà Nẵng, Việt Nam")       # -> 'central'
_detect_region("Singapore")               # -> None
```

**Vietnamese Translation:** Phát hiện vùng Việt Nam từ chuỗi vị trí

---

**4. _geolocate_ip(location: str) -> str**

Geolocates IP address or location to country code

**Detection Logic:**
1. **Extract IP Address:**
   - Use regex pattern: `r'\b(?:\d{1,3}\.){3}\d{1,3}\b'`
   - Parse as IPv4Address

2. **Check Vietnamese IP Ranges:**
   - Check against `FlowMappingConfig.VIETNAMESE_IP_RANGES` (Section 1)
   - If IP in Vietnamese range → return 'VN'

3. **Check Common Foreign IP Ranges:**
   - 8.x.x.x → 'SG' (Singapore)
   - 3.x.x.x → 'US' (United States)
   - (Simplified for prototype)

4. **Keyword Matching:**
   - 'singapore', 'sg' → 'SG'
   - 'united states', 'usa', 'us' → 'US'
   - 'japan', 'jp', 'tokyo' → 'JP'

5. **Default:** Return 'VN' if unknown

**Examples:**
```python
_geolocate_ip("123.16.1.1")              # -> 'VN' (VNPT range)
_geolocate_ip("8.8.8.8")                 # -> 'SG'
_geolocate_ip("3.0.0.1")                 # -> 'US'
_geolocate_ip("Hanoi")                   # -> 'VN'
_geolocate_ip("Singapore")               # -> 'SG'
```

**Vietnamese Translation:** Xác định quốc gia từ địa chỉ IP

---

**5. _classify_data_categories(tables: List[str]) -> List[str]**

Auto-classifies data categories based on table names

**Classification Logic:**
1. **Check Category 2 Keywords** (sensitive data):
   - Uses `FlowMappingConfig.CATEGORY_2_KEYWORDS` (Section 1)
   - Keywords: 'cccd', 'cmnd', 'passport', 'sức khỏe', 'tôn giáo', etc.
   - If match found → add 'Category 2'

2. **Check Category 1 Keywords** (basic personal):
   - Uses `FlowMappingConfig.CATEGORY_1_KEYWORDS` (Section 1)
   - Keywords: 'họ tên', 'địa chỉ', 'số điện thoại', 'email', etc.
   - If match found → add 'Category 1'

3. **Default:** If no keywords match → default to 'Category 1'

**Examples:**
```python
_classify_data_categories(['customers', 'orders'])           
# -> ['Category 1']

_classify_data_categories(['customers', 'cccd_info'])        
# -> ['Category 1', 'Category 2']

_classify_data_categories(['health_records', 'medical_data'])
# -> ['Category 2']
```

**Vietnamese Translation:** Tự động phân loại dữ liệu dựa trên tên bảng

---

**6. _find_node_location(node_id: str) -> Optional[str]**

Finds location of a node in the graph

**Logic:**
1. Query graph using `graph.get_node(node_id)`
2. Extract 'location' field from node data
3. Return location string or None

**Purpose:** Used during edge creation to geolocate source and target nodes

**Vietnamese Translation:** Tìm vị trí của nút trong đồ thị

---

**7. get_discovery_summary() -> Dict**

Returns summary of all discovered flows

**Output:**
```python
{
    'total_nodes_discovered': 5,
    'total_edges_discovered': 6,
    'discovered_nodes': [
        'db_customers_hanoi',
        'db_analytics_hcm',
        'cloud_storage_sg',
        'api_customer_service',
        'api_payment_gateway'
    ],
    'discovered_edges': [
        'flow_db_customers_hanoi_to_db_analytics_hcm',
        'flow_db_analytics_hcm_to_cloud_storage_sg',
        'api_input_db_customers_hanoi_to_api_customer_service',
        ...
    ],
    'graph_statistics': {
        'total_nodes': 5,
        'total_edges': 6,
        'cross_border_flows': 2,
        'category_1_nodes': 5,
        'category_2_nodes': 1,
        'mps_notifications_required': 1,
        'overall_compliance': 'compliant'
    }
}
```

**Vietnamese Translation:** Lấy tóm tắt luồng dữ liệu đã phát hiện

---

## Verification Results

**All 14 tests passed:**

### Test 1: Service Initialization ✅
- FlowDiscoveryService created successfully
- DataFlowGraph integration working
- FlowMappingConfig loaded

### Test 2: Database Flow Discovery ✅
- Discovered 3 database nodes
- Created 2 connection edges
- Two-pass algorithm working (nodes first, then edges)

### Test 3: Vietnamese Region Detection ✅
- Hanoi → 'north'
- Ho Chi Minh City → 'south'
- Singapore → None (not Vietnamese)

### Test 4: Data Category Auto-Classification ✅
- Detected 'Category 2' from 'cccd_info' table
- Correctly marked as sensitive_data=True
- Combined Category 1 and Category 2 in data_categories

### Test 5: Cross-Border Flow Detection ✅
- Detected 1 cross-border flow: db_analytics_hcm → cloud_storage_sg
- Correctly identified VN → SG transfer
- EdgeType.CROSS_BORDER_TRANSFER assigned

### Test 6: MPS Notification Requirement Detection ✅
- Category 1: 70,000 data subjects (exceeds 10,000 threshold)
- Category 2: 25,000 data subjects (exceeds 1,000 threshold)
- MPS registration required: TRUE
- Threshold logic working correctly

### Test 7: API Flow Discovery ✅
- Added 2 API nodes
- Created 4 edges (2 inputs + 2 outputs)
- API endpoint metadata processed correctly

### Test 8: API Node Region Detection ✅
- Da Nang API → 'central'
- Hanoi API → 'north'
- Region detection working for API locations

### Test 9: Graph Statistics After Discovery ✅
- Total nodes: 5 (3 databases + 2 APIs)
- Total edges: 6 (2 DB connections + 4 API flows)
- Cross-border flows: 2
- Category counts accurate

### Test 10: Discovery Summary ✅
- 5 nodes discovered
- 6 edges discovered
- All node IDs tracked
- All edge IDs tracked
- Graph statistics included

### Test 11: IP Geolocation Testing ✅
- 123.16.1.1 → 'VN' (Vietnamese IP range)
- 8.8.8.8 → 'SG' (Singapore)
- 3.0.0.1 → 'US' (United States)
- 'Hanoi' → 'VN' (keyword matching)
- 'Singapore' → 'SG' (keyword matching)

### Test 12: Data Lineage Tracking ✅
- API upstream: db_customers_hanoi (data source)
- API downstream: db_analytics_hcm (data target)
- Lineage tracking accurate after discovery

### Test 13: Processing Purpose Storage ✅
- Vietnamese purpose stored in edge metadata: "Phân tích dữ liệu khách hàng"
- Metadata field working correctly
- Vietnamese diacritics preserved

### Test 14: Edge Type Auto-Classification ✅
- 4 API_CALL edges (API flows)
- 1 DATA_TRANSFER edge (domestic DB connection)
- 1 CROSS_BORDER_TRANSFER edge (VN → SG)
- EdgeType correctly assigned based on transfer type

## Key Features Demonstrated

### 1. Automated Discovery
**No manual graph construction needed:**
```python
service = FlowDiscoveryService(graph)

# Provide metadata
database_metadata = [...]
api_metadata = [...]

# Auto-discover and populate graph
service.discover_database_flows(database_metadata)
service.discover_api_flows(api_metadata)

# Graph is now populated with 5 nodes and 6 edges
```

### 2. Intelligent Region Detection
**Vietnamese geography awareness:**
- Hanoi, Hải Phòng → North
- Đà Nẵng, Huế → Central  
- Hồ Chí Minh, Cần Thơ → South
- Handles both Vietnamese and English city names
- Supports diacritics (Hà Nội, Đà Nẵng)

### 3. PDPL Category Classification
**Automated PDPL compliance analysis:**
- Table name 'cccd_info' → Category 2 (CCCD = Căn cước công dân)
- Table name 'customers' → Category 1
- Table name 'health_records' → Category 2
- Combines multiple categories if both present

### 4. Cross-Border Auto-Detection
**International transfer identification:**
- VN → VN = DATA_TRANSFER (domestic)
- VN → SG = CROSS_BORDER_TRANSFER (international)
- VN → US = CROSS_BORDER_TRANSFER (international)
- Automatically sets is_cross_border flag

### 5. MPS Threshold Analysis
**Vietnamese MPS reporting compliance:**
- Cat1 threshold: 10,000 data subjects
- Cat2 threshold: 1,000 data subjects
- Automatic mps_notification_required flag
- Integrated with Section 1 constants

## Integration Success

### Section 1 Integration (flow_constants.py)
✅ Uses `FlowMappingConfig` for:
- `VIETNAMESE_REGIONS` - 33 cities across 3 regions
- `VIETNAMESE_IP_RANGES` - 9 ISP CIDR ranges
- `CATEGORY_1_KEYWORDS` - 5 basic personal data keywords
- `CATEGORY_2_KEYWORDS` - 9 sensitive data keywords
- `MPS_THRESHOLD_CATEGORY_1` - 10,000
- `MPS_THRESHOLD_CATEGORY_2` - 1,000

### Section 2 Integration (flow_models.py)
✅ Creates models:
- `DataAssetNode` - For databases and APIs
- `DataFlowEdge` - For connections and API calls
- `NodeType` enum - DATABASE, API_ENDPOINT
- `EdgeType` enum - DATA_TRANSFER, API_CALL, CROSS_BORDER_TRANSFER

### Section 3 Integration (flow_graph.py)
✅ Populates `DataFlowGraph`:
- `graph.add_node()` - Add discovered nodes
- `graph.add_edge()` - Add discovered edges
- `graph.get_node()` - Query node locations
- `graph.find_cross_border_flows()` - Verify discoveries
- `graph.get_graph_statistics()` - Summary after discovery

## File Structure

```
backend/veri_ai_data_inventory/
├── config/
│   └── flow_constants.py          # Section 1 (COMPLETE)
├── models/
│   └── flow_models.py             # Section 2 (COMPLETE)
├── graph/
│   └── flow_graph.py              # Section 3 (COMPLETE)
├── services/
│   ├── __init__.py                # Updated with FlowDiscoveryService
│   └── flow_discovery_service.py  # Section 4 (COMPLETE) ← THIS FILE
└── compliance/
    └── cross_border_validator.py  # Section 5 (NEXT)
```

## Next Steps

**Section 5: Cross-Border Validator (cross_border_validator.py)**
- Validate PDPL Article 20 compliance for cross-border transfers
- Check transfer mechanisms (SCC, BCR, consent, etc.)
- Verify adequate countries
- Generate Transfer Impact Assessment (TIA)
- Validate DPA (Data Processing Agreement) requirements

**Estimated:** ~200 lines, 2-3 hours

## Critical Success Factors

✅ **Database flow discovery** - 3 nodes, 2 edges discovered  
✅ **API flow discovery** - 2 nodes, 4 edges discovered  
✅ **Region detection** - North/Central/South identification working  
✅ **IP geolocation** - VN/SG/US country detection working  
✅ **Data category classification** - Category 1/2 auto-detection  
✅ **Cross-border detection** - VN ↔ international transfers identified  
✅ **MPS threshold analysis** - 70K Cat1, 25K Cat2 detected  
✅ **Processing purpose tracking** - Vietnamese purposes in metadata  
✅ **Two-pass algorithm** - Nodes first, edges second (prevents errors)  
✅ **Vietnamese diacritics** - Proper usage in comments/purposes  
✅ **Database-safe identifiers** - ASCII method/field names  

## Completion Checklist

- [x] FlowDiscoveryService class created
- [x] discover_database_flows() implemented
- [x] discover_api_flows() implemented
- [x] _detect_region() helper implemented
- [x] _geolocate_ip() helper implemented
- [x] _classify_data_categories() helper implemented
- [x] _find_node_location() helper implemented
- [x] get_discovery_summary() implemented
- [x] Section 1 integration (FlowMappingConfig)
- [x] Section 2 integration (DataAssetNode, DataFlowEdge)
- [x] Section 3 integration (DataFlowGraph)
- [x] Vietnamese region detection (33 cities)
- [x] IP geolocation (Vietnamese ranges + foreign IPs)
- [x] Data category auto-classification (Cat1/Cat2)
- [x] Cross-border auto-detection (VN ↔ others)
- [x] MPS threshold checking (10K/1K)
- [x] Processing purpose storage (Vietnamese)
- [x] Two-pass discovery algorithm (nodes → edges)
- [x] All 14 verification tests passed
- [x] Vietnamese diacritics in comments
- [x] Documentation created (this file)

---

**Section 4 Status:** ✅ COMPLETE - Ready for Section 5 implementation
