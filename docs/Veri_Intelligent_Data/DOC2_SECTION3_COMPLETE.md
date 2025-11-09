# Document #2 - Section 3: Flow Graph Database - COMPLETE

## Implementation Summary

**Status:** ✅ COMPLETE  
**Date:** 2025-11-04  
**File:** `graph/flow_graph.py`  
**Lines:** ~480 lines  
**Tests:** 14/14 passed  

## What Was Implemented

### 1. DataFlowGraph Class - NetworkX Wrapper

**Purpose:** Vietnamese PDPL 2025 data flow graph database with NetworkX directed graph backend

**Core Features:**
- Add/remove data asset nodes
- Add/remove data flow edges
- Query data lineage (upstream/downstream)
- Detect cross-border flows
- Find flows by processing purpose
- Detect circular flows
- Generate graph statistics
- Export to dictionary format
- Find shortest paths
- MPS reportable flows analysis

### 2. Class Structure

```python
class DataFlowGraph:
    def __init__(self, graph_id, business_id, business_name, primary_region):
        self.graph_id = graph_id
        self.business_id = business_id
        self.business_name = business_name
        self.primary_region = primary_region
        self.graph = nx.DiGraph()  # NetworkX directed graph
        self.config = FlowMappingConfig()  # Section 1 config
```

**Vietnamese Business Context:**
- `business_id` - Mã doanh nghiệp (Business registration number)
- `business_name` - Tên doanh nghiệp (Company name)
- `primary_region` - Vùng chính (North/Central/South)

### 3. Core Methods (20 total)

#### Node Management (4 methods)

**1. add_node(node: DataAssetNode) -> bool**
- Adds data asset node to graph
- Stores all 15 DataAssetNode fields as node attributes
- Returns False if node already exists
- Vietnamese: Thêm nút tài sản dữ liệu vào đồ thị

**2. remove_node(node_id: str) -> bool**
- Removes node and all connected edges
- Returns False if node doesn't exist
- Vietnamese: Xóa nút và tất cả các cạnh liên kết

**3. get_node(node_id: str) -> Optional[Dict]**
- Retrieves node attributes as dictionary
- Returns None if node not found
- Vietnamese: Lấy thông tin nút

**4. get_nodes_by_type(node_type: NodeType) -> List[str]**
- Filters nodes by type (database, api_endpoint, etc.)
- Returns list of node IDs
- Vietnamese: Lấy tất cả nút theo loại

#### Edge Management (5 methods)

**5. add_edge(edge: DataFlowEdge) -> bool**
- Adds data flow edge to graph
- Stores all 19 DataFlowEdge fields as edge attributes
- Returns False if edge already exists
- Vietnamese: Thêm cạnh luồng dữ liệu vào đồ thị

**6. remove_edge(source_node_id: str, target_node_id: str) -> bool**
- Removes edge between two nodes
- Returns False if edge doesn't exist
- Vietnamese: Xóa cạnh giữa hai nút

**7. get_edge(source_node_id: str, target_node_id: str) -> Optional[Dict]**
- Retrieves edge attributes as dictionary
- Returns None if edge not found
- Vietnamese: Lấy thông tin cạnh

**8. get_edges_by_type(edge_type: EdgeType) -> List[Tuple]**
- Filters edges by type (data_transfer, api_call, etc.)
- Returns list of (source, target) tuples
- Vietnamese: Lấy tất cả cạnh theo loại

**9. get_shortest_path(source_node_id: str, target_node_id: str) -> Optional[List[str]]**
- Finds shortest data flow path using NetworkX
- Returns list of node IDs in path, or None if no path exists
- Vietnamese: Tìm đường đi ngắn nhất giữa hai nút

#### Data Lineage (1 method)

**10. get_data_lineage(node_id: str, direction: str) -> Dict**
- Traces data lineage upstream and/or downstream
- direction: 'upstream', 'downstream', or 'both'
- Returns {'upstream': [...], 'downstream': [...]}
- Vietnamese: Lấy lịch sử dòng dữ liệu (nguồn gốc và điểm đến)

**Example:**
```python
lineage = graph.get_data_lineage("api_crm_001", direction="both")
# Returns:
# {
#   'upstream': ['db_customer_001'],      # Data sources
#   'downstream': ['cloud_aws_sg']        # Data destinations
# }
```

#### PDPL Compliance Analysis (3 methods)

**11. find_cross_border_flows() -> List[Dict]**
- Finds all cross-border transfers for PDPL Article 20 compliance
- Returns list with transfer mechanisms, legal basis, MPS notification status
- Vietnamese: Tìm tất cả luồng dữ liệu xuyên biên giới (Điều 20 PDPL)

**Example Output:**
```python
[{
    'source_node_id': 'api_crm_001',
    'target_node_id': 'cloud_aws_sg',
    'edge_id': 'edge_002',
    'edge_type': 'cross_border_transfer',
    'source_country': 'VN',
    'target_country': 'SG',
    'transfer_mechanism': 'standard_contractual_clauses',
    'legal_basis': 'legitimate_interest',
    'mps_notification_sent': False,
    'dpa_in_place': True,
    'encryption_enabled': True
}]
```

**12. find_flows_by_purpose(purpose_keyword: str) -> List[Dict]**
- Searches flows by processing purpose (Vietnamese or English)
- Purpose stored in edge metadata['processing_purpose']
- Vietnamese: Tìm luồng dữ liệu theo mục đích xử lý

**Example:**
```python
flows = graph.find_flows_by_purpose("khách hàng")
# Finds flows with "khách hàng" (customer) in purpose
```

**13. find_mps_reportable_flows() -> Dict**
- Analyzes MPS (Ministry of Public Security) reporting requirements
- Checks Category 1 and Category 2 thresholds from Section 1
- Identifies unsent MPS notifications
- Vietnamese: Tìm luồng dữ liệu cần báo cáo cho Bộ Công an (MPS)

**Example Output:**
```python
{
    'category_1_data_subjects': 28000,
    'category_2_data_subjects': 15000,
    'mps_threshold_category_1': 10000,
    'mps_threshold_category_2': 1000,
    'exceeds_cat1_threshold': True,
    'exceeds_cat2_threshold': True,
    'requires_mps_registration': True,
    'total_cross_border_flows': 1,
    'unsent_mps_notifications': 1,
    'pending_notifications': [...]
}
```

#### Graph Analysis (3 methods)

**14. detect_circular_flows() -> List[List[str]]**
- Detects circular data flows (cycles) using NetworkX
- Returns list of cycles (each cycle is a list of node IDs)
- Vietnamese: Phát hiện luồng dữ liệu vòng tròn

**Example Output:**
```python
[
    ['test_circular_001', 'db_customer_001', 'api_crm_001']
    # Represents: test_circular_001 -> db_customer_001 -> api_crm_001 -> test_circular_001
]
```

**15. get_graph_statistics() -> FlowGraphMetadata**
- Generates comprehensive graph statistics
- Returns FlowGraphMetadata model (Section 2)
- Counts nodes by category, cross-border flows, compliance status
- Vietnamese: Tạo thống kê toàn bộ đồ thị

**Statistics Included:**
- total_nodes, total_edges
- cross_border_flows
- mps_notifications_required
- category_1_nodes, category_2_nodes
- overall_compliance (compliant/non_compliant/partial/under_review)
- compliance_issues (list of specific issues)

**16. export_to_dict() -> Dict**
- Exports entire graph to dictionary format
- Includes all nodes with attributes
- Includes all edges with attributes
- Includes metadata (graph_id, business info, timestamps)
- Vietnamese: Xuất đồ thị sang định dạng dict

**Example Output:**
```python
{
    'graph_id': 'graph_test_001',
    'business_id': '0123456789',
    'business_name': 'Công ty TNHH Test VeriSyntra',
    'primary_region': 'south',
    'created_at': '2025-11-04T21:35:45.519675',
    'updated_at': '2025-11-04T21:35:45.620123',
    'nodes': [
        {'node_id': 'db_customer_001', 'node_type': 'database', ...},
        {'node_id': 'api_crm_001', 'node_type': 'api_endpoint', ...}
    ],
    'edges': [
        {'source_node_id': 'db_customer_001', 'target_node_id': 'api_crm_001', ...}
    ]
}
```

## Verification Results

**All 14 tests passed:**

### Test 1: Graph Initialization ✅
- Created DataFlowGraph instance
- NetworkX DiGraph initialized
- Business context stored correctly

### Test 2: Add Data Asset Nodes ✅
- Added 3 nodes: database, api_endpoint, cloud_storage
- Duplicate node detection working
- All node attributes stored correctly

### Test 3: Add Data Flow Edges ✅
- Added domestic edge (VN → VN)
- Added cross-border edge (VN → SG)
- Edge attributes stored correctly

### Test 4: Retrieve Node and Edge Data ✅
- Retrieved node by ID
- Retrieved edge by source/target IDs
- All attributes accessible

### Test 5: Data Lineage Tracking ✅
- Upstream lineage working (sources)
- Downstream lineage working (targets)
- Bidirectional lineage working

### Test 6: Cross-Border Flow Detection ✅
- Detected 1 cross-border flow (VN → SG)
- Transfer mechanism retrieved (SCC)
- MPS notification status tracked

### Test 7: Find Flows by Processing Purpose ✅
- Searched by Vietnamese keyword "khách hàng"
- Found matching flows in metadata
- Purpose-based filtering working

### Test 8: Graph Statistics ✅
- Total nodes: 3
- Total edges: 2
- Cross-border flows: 1
- Category counts correct
- MPS notifications tracked
- Overall compliance calculated

### Test 9: Filter by Node/Edge Type ✅
- Filtered 1 database node
- Filtered 1 API node
- Filtered 1 cloud storage node
- Filtered 1 cross-border edge
- Filtered 1 API call edge

### Test 10: MPS Reportable Flows ✅
- Category 1: 28,000 data subjects (exceeds 10,000 threshold)
- Category 2: 15,000 data subjects (exceeds 1,000 threshold)
- MPS registration required: True
- Unsent notifications: 1
- Pending notifications tracked

### Test 11: Shortest Path Finding ✅
- Found path: db_customer_001 → api_crm_001 → cloud_aws_sg
- NetworkX shortest_path integration working

### Test 12: Remove Node and Edge ✅
- Removed edge successfully
- Removed node successfully
- Graph updated correctly

### Test 13: Export Graph to Dictionary ✅
- Exported 2 nodes (after removal)
- Exported 1 edge (after removal)
- Timestamps included
- Business metadata included

### Test 14: Circular Flow Detection ✅
- Detected 1 circular flow
- Cycle path: test_circular_001 → db_customer_001 → api_crm_001 → test_circular_001
- NetworkX simple_cycles integration working

## Integration Points

### Section 1 Integration (flow_constants.py)
- Uses `FlowMappingConfig()` for MPS thresholds
- MPS_THRESHOLD_CATEGORY_1 = 10,000
- MPS_THRESHOLD_CATEGORY_2 = 1,000
- Validates against configuration constants

### Section 2 Integration (flow_models.py)
- Accepts `DataAssetNode` model for nodes
- Accepts `DataFlowEdge` model for edges
- Returns `FlowGraphMetadata` model for statistics
- Uses `NodeType` and `EdgeType` enums

### Section 4 Preview (flow_discovery_service.py)
- Will use `add_node()` and `add_edge()` to build graph
- Will use `find_cross_border_flows()` for discovery
- Will use `get_graph_statistics()` for reporting

## Technical Details

### NetworkX Integration

**Graph Type:** `nx.DiGraph()` - Directed graph for data flow directionality

**Node Storage:**
```python
self.graph.add_node(
    node_id,                        # Node identifier
    node_type=...,                  # NodeType enum
    name=...,                       # Vietnamese name
    vietnamese_region=...,          # north/central/south
    data_categories=[...],          # Category 1/2/Non-Personal
    # ... 15 total fields
)
```

**Edge Storage:**
```python
self.graph.add_edge(
    source_node_id,                 # Source node
    target_node_id,                 # Target node
    edge_id=...,                    # Edge identifier
    edge_type=...,                  # EdgeType enum
    is_cross_border=...,            # Boolean
    transfer_mechanism=...,         # SCC, BCR, etc.
    # ... 19 total fields
)
```

### Vietnamese Diacritics Compliance

**All Vietnamese text uses proper diacritics:**
- Method docstrings in Vietnamese
- Comments with tone marks
- Vietnamese field values (in metadata)

**Database-safe identifiers:**
- Field names: `vietnamese_region` (not `vùng_việt_nam`)
- Method names: `find_mps_reportable_flows` (English)
- Variable names: `cross_border_flows` (English)

### Metadata Storage Pattern

**Processing purpose stored in edge metadata:**
```python
edge = DataFlowEdge(
    edge_id="edge_001",
    # ... other fields
    metadata={"processing_purpose": "Quản lý quan hệ khách hàng"}
)
```

**Why metadata?** DataFlowEdge model doesn't have `processing_purpose` field, so we store it in the flexible `metadata` dict.

## File Structure

```
backend/veri_ai_data_inventory/
├── config/
│   └── flow_constants.py          # Section 1 (COMPLETE)
├── models/
│   └── flow_models.py             # Section 2 (COMPLETE)
├── graph/
│   ├── __init__.py                # Graph module init
│   └── flow_graph.py              # Section 3 (COMPLETE) ← THIS FILE
└── services/
    └── flow_discovery_service.py  # Section 4 (NEXT)
```

## Next Steps

**Section 4: Flow Discovery Service (flow_discovery_service.py)**
- Implement automated flow detection from databases
- Implement API flow discovery
- IP geolocation for region detection
- Automatic graph population
- Integration with Section 3 DataFlowGraph

**Estimated:** ~250 lines, 2-3 hours

## Critical Success Factors

✅ **NetworkX integration** - Directed graph working correctly  
✅ **Node management** - Add/remove/get nodes functioning  
✅ **Edge management** - Add/remove/get edges functioning  
✅ **Data lineage** - Upstream/downstream tracking working  
✅ **Cross-border detection** - PDPL Article 20 compliance  
✅ **Processing purpose search** - Vietnamese keyword search  
✅ **MPS reporting** - Threshold analysis and notification tracking  
✅ **Circular flow detection** - Graph cycle detection  
✅ **Graph statistics** - Comprehensive metadata generation  
✅ **Type filtering** - Node/edge type queries working  
✅ **Shortest path** - NetworkX pathfinding integration  
✅ **Export functionality** - Dictionary serialization  
✅ **Vietnamese diacritics** - Proper usage in comments/docs  
✅ **Database-safe identifiers** - ASCII field names  

## Completion Checklist

- [x] DataFlowGraph class created
- [x] NetworkX DiGraph initialized
- [x] add_node() method implemented
- [x] remove_node() method implemented
- [x] get_node() method implemented
- [x] get_nodes_by_type() method implemented
- [x] add_edge() method implemented
- [x] remove_edge() method implemented
- [x] get_edge() method implemented
- [x] get_edges_by_type() method implemented
- [x] get_data_lineage() method implemented
- [x] find_cross_border_flows() method implemented
- [x] find_flows_by_purpose() method implemented
- [x] detect_circular_flows() method implemented
- [x] get_graph_statistics() method implemented
- [x] export_to_dict() method implemented
- [x] get_shortest_path() method implemented
- [x] find_mps_reportable_flows() method implemented
- [x] Section 1 integration (FlowMappingConfig)
- [x] Section 2 integration (DataAssetNode, DataFlowEdge, FlowGraphMetadata)
- [x] All 14 verification tests passed
- [x] Vietnamese diacritics in comments
- [x] Documentation created (this file)

---

**Section 3 Status:** ✅ COMPLETE - Ready for Section 4 implementation
