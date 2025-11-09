"""
Flow Data Models
Document #2 - Section 2: Flow Data Models

Pydantic models for data flow graph nodes and edges
Vietnamese PDPL 2025 compliance focused
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator


class NodeType(str, Enum):
    """
    Types of nodes in the data flow graph
    
    Represents different data asset types in Vietnamese enterprise systems
    """
    DATABASE = "database"                    # Cơ sở dữ liệu
    API_ENDPOINT = "api_endpoint"            # Điểm cuối API
    FILE_SYSTEM = "file_system"              # Hệ thống tệp
    CLOUD_STORAGE = "cloud_storage"          # Lưu trữ đám mây
    THIRD_PARTY_SERVICE = "third_party_service"  # Dịch vụ bên thứ ba
    MPS_SYSTEM = "mps_system"                # Hệ thống Bộ Công an
    DATA_SUBJECT = "data_subject"            # Chủ thể dữ liệu
    PROCESSING_ACTIVITY = "processing_activity"  # Hoạt động xử lý


class EdgeType(str, Enum):
    """
    Types of edges (connections) in the data flow graph
    
    Represents different types of data flows between assets
    """
    DATA_TRANSFER = "data_transfer"          # Chuyển dữ liệu nội bộ
    API_CALL = "api_call"                    # Gọi API
    FILE_COPY = "file_copy"                  # Sao chép tệp
    CROSS_BORDER_TRANSFER = "cross_border_transfer"  # Chuyển xuyên biên giới
    THIRD_PARTY_SHARING = "third_party_sharing"      # Chia sẻ bên thứ ba
    MPS_NOTIFICATION = "mps_notification"    # Thông báo Bộ Công an
    USER_ACCESS = "user_access"              # Truy cập người dùng


class DataAssetNode(BaseModel):
    """
    Represents a data asset node in the flow graph
    
    Integration with Document #1 column filtering
    """
    
    node_id: str = Field(..., description="Unique identifier for the node")
    node_type: NodeType = Field(..., description="Type of data asset")
    name: str = Field(..., description="Human-readable name of the asset")
    
    # Location and ownership
    location: str = Field(..., description="Physical or logical location (e.g., 'Hanoi', 'Singapore')")
    vietnamese_region: Optional[str] = Field(None, description="Vietnamese region: north, central, south")
    owner: Optional[str] = Field(None, description="Business owner or department")
    
    # Data characteristics
    data_categories: List[str] = Field(default_factory=list, description="PDPL data categories (Category 1, Category 2)")
    estimated_record_count: Optional[int] = Field(None, description="Estimated number of records")
    sensitive_data: bool = Field(False, description="Contains PDPL Category 2 data")
    
    # Document #1 integration: Column filtering status
    column_filter_applied: bool = Field(False, description="Whether Document #1 column filtering was applied")
    filter_statistics: Optional[Dict[str, Any]] = Field(None, description="Statistics from column filtering")
    scanned_at: Optional[datetime] = Field(None, description="Last scan timestamp")
    
    # Compliance metadata
    pdpl_compliant: bool = Field(True, description="Meets PDPL 2025 requirements")
    mps_notification_required: bool = Field(False, description="Requires MPS notification under Decree 13/2023")
    
    # Technical metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional node metadata")
    
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "node_id": "db_customers_hanoi",
                "node_type": "database",
                "name": "Customer Database - Hanoi",
                "location": "Hanoi",
                "vietnamese_region": "north",
                "owner": "Marketing Department",
                "data_categories": ["Category 1", "Category 2"],
                "estimated_record_count": 15000,
                "sensitive_data": True,
                "column_filter_applied": True,
                "filter_statistics": {
                    "total_columns": 25,
                    "scanned_columns": 18,
                    "filtered_out": 7
                },
                "pdpl_compliant": True,
                "mps_notification_required": True
            }
        }
    
    @field_validator('vietnamese_region')
    @classmethod
    def validate_vietnamese_region(cls, v):
        """Validate Vietnamese region values"""
        if v is not None and v not in ['north', 'central', 'south']:
            raise ValueError('vietnamese_region must be: north, central, or south')
        return v
    
    @field_validator('data_categories')
    @classmethod
    def validate_data_categories(cls, v):
        """Validate PDPL data categories"""
        valid_categories = ['Category 1', 'Category 2', 'Non-Personal']
        for category in v:
            if category not in valid_categories:
                raise ValueError(f'Invalid data category: {category}. Must be one of {valid_categories}')
        return v


class DataFlowEdge(BaseModel):
    """
    Represents a data flow edge (connection) between nodes
    
    Vietnamese PDPL Article 20 compliance for cross-border transfers
    """
    
    edge_id: str = Field(..., description="Unique identifier for the edge")
    source_node_id: str = Field(..., description="Source node ID")
    target_node_id: str = Field(..., description="Target node ID")
    edge_type: EdgeType = Field(..., description="Type of data flow")
    
    # Flow characteristics
    data_volume: Optional[int] = Field(None, description="Estimated number of records transferred")
    frequency: Optional[str] = Field(None, description="Transfer frequency (e.g., 'hourly', 'daily', 'real-time')")
    
    # Security and compliance
    encryption_enabled: bool = Field(True, description="Data encrypted in transit")
    transfer_mechanism: Optional[str] = Field(None, description="PDPL Article 20 mechanism (SCC, BCR, etc.)")
    legal_basis: Optional[str] = Field(None, description="Legal basis for processing (consent, contract, etc.)")
    
    # Cross-border transfer metadata
    is_cross_border: bool = Field(False, description="Crosses Vietnamese border (PDPL Article 20)")
    source_country: Optional[str] = Field("VN", description="Source country ISO code")
    target_country: Optional[str] = Field("VN", description="Target country ISO code")
    
    # MPS compliance
    mps_notification_sent: bool = Field(False, description="MPS notification sent (if required)")
    mps_notification_date: Optional[datetime] = Field(None, description="Date of MPS notification")
    
    # Data Processing Agreement
    dpa_in_place: bool = Field(False, description="Data Processing Agreement signed")
    dpa_reference: Optional[str] = Field(None, description="DPA reference number")
    
    # Technical metadata
    protocol: Optional[str] = Field(None, description="Transfer protocol (HTTPS, SFTP, etc.)")
    last_transfer: Optional[datetime] = Field(None, description="Last successful transfer timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional edge metadata")
    
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "edge_id": "flow_db_to_s3",
                "source_node_id": "db_customers_hanoi",
                "target_node_id": "s3_backup_singapore",
                "edge_type": "cross_border_transfer",
                "data_volume": 15000,
                "frequency": "daily",
                "encryption_enabled": True,
                "transfer_mechanism": "standard_contractual_clauses",
                "legal_basis": "legitimate_interest",
                "is_cross_border": True,
                "source_country": "VN",
                "target_country": "SG",
                "mps_notification_sent": True,
                "dpa_in_place": True,
                "protocol": "HTTPS"
            }
        }
    
    @field_validator('source_country', 'target_country')
    @classmethod
    def validate_country_codes(cls, v):
        """Validate ISO country codes"""
        if v is not None and len(v) != 2:
            raise ValueError('Country code must be 2-letter ISO code (e.g., VN, SG, US)')
        return v.upper() if v else v
    
    @model_validator(mode='after')
    def validate_cross_border_status(self):
        """Auto-detect cross-border transfers"""
        source = self.source_country if self.source_country else 'VN'
        target = self.target_country if self.target_country else 'VN'
        
        # Cross-border if either source or target is outside Vietnam
        if source != 'VN' or target != 'VN':
            self.is_cross_border = True
        
        return self


class FlowGraphMetadata(BaseModel):
    """
    Metadata for the entire data flow graph
    
    Vietnamese business context and compliance summary
    """
    
    graph_id: str = Field(..., description="Unique identifier for the graph")
    business_id: str = Field(..., description="Vietnamese business identifier")
    business_name: str = Field(..., description="Vietnamese business name")
    
    # Vietnamese regional context
    primary_region: str = Field(..., description="Primary operating region: north, central, south")
    regional_locations: List[str] = Field(default_factory=list, description="All Vietnamese locations")
    
    # Graph statistics
    total_nodes: int = Field(0, description="Total number of nodes")
    total_edges: int = Field(0, description="Total number of edges")
    
    # Compliance summary
    cross_border_flows: int = Field(0, description="Number of cross-border transfers")
    mps_notifications_required: int = Field(0, description="Number of flows requiring MPS notification")
    mps_notifications_sent: int = Field(0, description="Number of MPS notifications sent")
    
    # Data categories summary
    category_1_nodes: int = Field(0, description="Nodes with Category 1 data")
    category_2_nodes: int = Field(0, description="Nodes with Category 2 data (sensitive)")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Graph creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    # PDPL compliance status
    overall_compliance: str = Field("compliant", description="Overall PDPL compliance status")
    compliance_issues: List[str] = Field(default_factory=list, description="List of compliance issues")
    
    class Config:
        json_schema_extra = {
            "example": {
                "graph_id": "graph_company_001",
                "business_id": "VN-123456789",
                "business_name": "Công ty TNHH ABC",
                "primary_region": "south",
                "regional_locations": ["Ho Chi Minh", "Binh Duong"],
                "total_nodes": 15,
                "total_edges": 28,
                "cross_border_flows": 3,
                "mps_notifications_required": 2,
                "mps_notifications_sent": 2,
                "category_1_nodes": 10,
                "category_2_nodes": 5,
                "overall_compliance": "compliant",
                "compliance_issues": []
            }
        }
    
    @field_validator('primary_region')
    @classmethod
    def validate_primary_region(cls, v):
        """Validate Vietnamese region"""
        if v not in ['north', 'central', 'south']:
            raise ValueError('primary_region must be: north, central, or south')
        return v
    
    @field_validator('overall_compliance')
    @classmethod
    def validate_compliance_status(cls, v):
        """Validate compliance status values"""
        valid_statuses = ['compliant', 'non_compliant', 'partial', 'under_review']
        if v not in valid_statuses:
            raise ValueError(f'overall_compliance must be one of {valid_statuses}')
        return v


# Export all models
__all__ = [
    'NodeType',
    'EdgeType',
    'DataAssetNode',
    'DataFlowEdge',
    'FlowGraphMetadata'
]
