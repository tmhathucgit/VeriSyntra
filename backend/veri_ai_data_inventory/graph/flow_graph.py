"""
Data Flow Graph Database - Section 3

NetworkX-based graph database for Vietnamese PDPL 2025 data flow mapping
Supports data lineage tracking, cross-border flow detection, and compliance analysis
"""

from typing import Dict, List, Optional, Set, Tuple, Any
import networkx as nx
from datetime import datetime

# Import Section 1 and Section 2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.flow_constants import FlowMappingConfig
from models.flow_models import (
    DataAssetNode, 
    DataFlowEdge, 
    FlowGraphMetadata,
    NodeType,
    EdgeType
)


class DataFlowGraph:
    """
    NetworkX-based data flow graph for Vietnamese PDPL compliance
    
    Quan ly do thi luong du lieu cho tuan thu PDPL Viet Nam
    (Manages data flow graph for Vietnamese PDPL compliance)
    
    Features:
    - Add/remove nodes and edges
    - Query data lineage (upstream and downstream)
    - Detect cross-border flows
    - Find flows by processing purpose
    - Detect circular flows
    - Generate graph statistics
    """
    
    def __init__(self, graph_id: str, business_id: str, business_name: str, primary_region: str):
        """
        Initialize data flow graph
        
        Args:
            graph_id: Unique graph identifier
            business_id: Vietnamese business ID (Ma doanh nghiep)
            business_name: Vietnamese business name (Ten doanh nghiep)
            primary_region: Primary region (north/central/south)
        """
        self.graph_id = graph_id
        self.business_id = business_id
        self.business_name = business_name
        self.primary_region = primary_region
        
        # NetworkX directed graph
        self.graph = nx.DiGraph()
        
        # Metadata tracking
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Configuration from Section 1
        self.config = FlowMappingConfig()
    
    def add_node(self, node: DataAssetNode) -> bool:
        """
        Add data asset node to graph
        
        Them nut tai san du lieu vao do thi
        
        Args:
            node: DataAssetNode model from Section 2
        
        Returns:
            bool: True if added successfully, False if node already exists
        """
        if self.graph.has_node(node.node_id):
            return False
        
        # Add node with all attributes
        self.graph.add_node(
            node.node_id,
            node_type=node.node_type,
            name=node.name,
            location=node.location,
            vietnamese_region=node.vietnamese_region,
            data_categories=node.data_categories,
            estimated_record_count=node.estimated_record_count,
            sensitive_data=node.sensitive_data,
            column_filter_applied=node.column_filter_applied,
            filter_statistics=node.filter_statistics,
            pdpl_compliant=node.pdpl_compliant,
            mps_notification_required=node.mps_notification_required,
            metadata=node.metadata
        )
        
        self.updated_at = datetime.now()
        return True
    
    def add_edge(self, edge: DataFlowEdge) -> bool:
        """
        Add data flow edge to graph
        
        Them canh luong du lieu vao do thi
        
        Args:
            edge: DataFlowEdge model from Section 2
        
        Returns:
            bool: True if added successfully, False if edge already exists
        """
        if self.graph.has_edge(edge.source_node_id, edge.target_node_id):
            return False
        
        # Add edge with all attributes
        self.graph.add_edge(
            edge.source_node_id,
            edge.target_node_id,
            edge_id=edge.edge_id,
            edge_type=edge.edge_type,
            data_volume=edge.data_volume,
            frequency=edge.frequency,
            encryption_enabled=edge.encryption_enabled,
            transfer_mechanism=edge.transfer_mechanism,
            legal_basis=edge.legal_basis,
            is_cross_border=edge.is_cross_border,
            source_country=edge.source_country,
            target_country=edge.target_country,
            mps_notification_sent=edge.mps_notification_sent,
            dpa_in_place=edge.dpa_in_place,
            protocol=edge.protocol,
            metadata=edge.metadata
        )
        
        self.updated_at = datetime.now()
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """
        Remove node and all connected edges
        
        Xoa nut va tat ca cac canh lien ket
        
        Args:
            node_id: Node identifier to remove
        
        Returns:
            bool: True if removed, False if node doesn't exist
        """
        if not self.graph.has_node(node_id):
            return False
        
        self.graph.remove_node(node_id)
        self.updated_at = datetime.now()
        return True
    
    def remove_edge(self, source_node_id: str, target_node_id: str) -> bool:
        """
        Remove edge between two nodes
        
        Xoa canh giua hai nut
        
        Args:
            source_node_id: Source node ID
            target_node_id: Target node ID
        
        Returns:
            bool: True if removed, False if edge doesn't exist
        """
        if not self.graph.has_edge(source_node_id, target_node_id):
            return False
        
        self.graph.remove_edge(source_node_id, target_node_id)
        self.updated_at = datetime.now()
        return True
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get node attributes
        
        Lay thong tin nut
        
        Args:
            node_id: Node identifier
        
        Returns:
            Optional[Dict]: Node attributes or None if not found
        """
        if not self.graph.has_node(node_id):
            return None
        
        return dict(self.graph.nodes[node_id])
    
    def get_edge(self, source_node_id: str, target_node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get edge attributes
        
        Lay thong tin canh
        
        Args:
            source_node_id: Source node ID
            target_node_id: Target node ID
        
        Returns:
            Optional[Dict]: Edge attributes or None if not found
        """
        if not self.graph.has_edge(source_node_id, target_node_id):
            return None
        
        return dict(self.graph.edges[source_node_id, target_node_id])
    
    def get_data_lineage(self, node_id: str, direction: str = 'both') -> Dict[str, List[str]]:
        """
        Get data lineage for a node (upstream and/or downstream)
        
        Lay lich su dong du lieu (nguon goc va diem den)
        
        Args:
            node_id: Node to analyze
            direction: 'upstream', 'downstream', or 'both'
        
        Returns:
            Dict with 'upstream' and/or 'downstream' node lists
        """
        if not self.graph.has_node(node_id):
            return {'upstream': [], 'downstream': []}
        
        result = {}
        
        if direction in ['upstream', 'both']:
            # Get all predecessors (nodes that flow into this node)
            upstream = list(self.graph.predecessors(node_id))
            result['upstream'] = upstream
        
        if direction in ['downstream', 'both']:
            # Get all successors (nodes that this node flows to)
            downstream = list(self.graph.successors(node_id))
            result['downstream'] = downstream
        
        return result
    
    def find_cross_border_flows(self) -> List[Dict[str, Any]]:
        """
        Find all cross-border data flows for PDPL Article 20 compliance
        
        Tim tat ca luong du lieu xuyen bien gioi (Dieu 20 PDPL)
        
        Returns:
            List of cross-border edges with details
        """
        cross_border_flows = []
        
        for source, target, data in self.graph.edges(data=True):
            if data.get('is_cross_border', False):
                cross_border_flows.append({
                    'source_node_id': source,
                    'target_node_id': target,
                    'edge_id': data.get('edge_id'),
                    'edge_type': data.get('edge_type'),
                    'source_country': data.get('source_country', 'VN'),
                    'target_country': data.get('target_country', 'VN'),
                    'transfer_mechanism': data.get('transfer_mechanism'),
                    'legal_basis': data.get('legal_basis'),
                    'mps_notification_sent': data.get('mps_notification_sent', False),
                    'dpa_in_place': data.get('dpa_in_place', False),
                    'encryption_enabled': data.get('encryption_enabled', False)
                })
        
        return cross_border_flows
    
    def find_flows_by_purpose(self, purpose_keyword: str) -> List[Dict[str, Any]]:
        """
        Find flows by processing purpose (stored in metadata)
        
        Tim luong du lieu theo muc dich xu ly
        
        Args:
            purpose_keyword: Vietnamese or English keyword (e.g., "marketing", "tiep thi")
        
        Returns:
            List of edges matching the purpose
        """
        matching_flows = []
        
        for source, target, data in self.graph.edges(data=True):
            # Check if purpose is in metadata
            metadata = data.get('metadata', {})
            purpose = metadata.get('processing_purpose', '')
            if purpose and purpose_keyword.lower() in purpose.lower():
                matching_flows.append({
                    'source_node_id': source,
                    'target_node_id': target,
                    'edge_id': data.get('edge_id'),
                    'purpose': purpose,
                    'legal_basis': data.get('legal_basis'),
                    'is_cross_border': data.get('is_cross_border', False)
                })
        
        return matching_flows
    
    def detect_circular_flows(self) -> List[List[str]]:
        """
        Detect circular data flows (cycles in the graph)
        
        Phat hien luong du lieu vong tron
        
        Returns:
            List of cycles (each cycle is a list of node IDs)
        """
        try:
            # Find all simple cycles
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except Exception as e:
            # If graph has no cycles or error occurs
            return []
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[str]:
        """
        Get all nodes of a specific type
        
        Lay tat ca nut theo loai
        
        Args:
            node_type: NodeType enum value
        
        Returns:
            List of node IDs matching the type
        """
        matching_nodes = []
        
        for node_id, data in self.graph.nodes(data=True):
            if data.get('node_type') == node_type:
                matching_nodes.append(node_id)
        
        return matching_nodes
    
    def get_edges_by_type(self, edge_type: EdgeType) -> List[Tuple[str, str]]:
        """
        Get all edges of a specific type
        
        Lay tat ca canh theo loai
        
        Args:
            edge_type: EdgeType enum value
        
        Returns:
            List of (source, target) tuples matching the type
        """
        matching_edges = []
        
        for source, target, data in self.graph.edges(data=True):
            if data.get('edge_type') == edge_type:
                matching_edges.append((source, target))
        
        return matching_edges
    
    def get_graph_statistics(self) -> FlowGraphMetadata:
        """
        Generate comprehensive graph statistics
        
        Tao thong ke toan bo do thi
        
        Returns:
            FlowGraphMetadata model with statistics
        """
        # Count nodes by category
        category_1_nodes = 0
        category_2_nodes = 0
        
        for node_id, data in self.graph.nodes(data=True):
            categories = data.get('data_categories', [])
            if 'Category 1' in categories:
                category_1_nodes += 1
            if 'Category 2' in categories:
                category_2_nodes += 1
        
        # Count cross-border flows
        cross_border_flows = len(self.find_cross_border_flows())
        
        # Count MPS notifications required
        mps_notifications_required = 0
        for node_id, data in self.graph.nodes(data=True):
            if data.get('mps_notification_required', False):
                mps_notifications_required += 1
        
        # Check overall compliance
        non_compliant_nodes = []
        for node_id, data in self.graph.nodes(data=True):
            if data.get('pdpl_compliant') == False:
                non_compliant_nodes.append(node_id)
        
        overall_compliance = 'compliant' if len(non_compliant_nodes) == 0 else 'non_compliant'
        compliance_issues = [f"Node {node_id} not PDPL compliant" for node_id in non_compliant_nodes]
        
        # Create metadata
        metadata = FlowGraphMetadata(
            graph_id=self.graph_id,
            business_id=self.business_id,
            business_name=self.business_name,
            primary_region=self.primary_region,
            total_nodes=self.graph.number_of_nodes(),
            total_edges=self.graph.number_of_edges(),
            cross_border_flows=cross_border_flows,
            mps_notifications_required=mps_notifications_required,
            category_1_nodes=category_1_nodes,
            category_2_nodes=category_2_nodes,
            overall_compliance=overall_compliance,
            compliance_issues=compliance_issues
        )
        
        return metadata
    
    def export_to_dict(self) -> Dict[str, Any]:
        """
        Export graph to dictionary format
        
        Xuat do thi sang dinh dang dict
        
        Returns:
            Dict containing all graph data
        """
        nodes_data = []
        for node_id, data in self.graph.nodes(data=True):
            node_dict = {'node_id': node_id}
            node_dict.update(data)
            nodes_data.append(node_dict)
        
        edges_data = []
        for source, target, data in self.graph.edges(data=True):
            edge_dict = {
                'source_node_id': source,
                'target_node_id': target
            }
            edge_dict.update(data)
            edges_data.append(edge_dict)
        
        return {
            'graph_id': self.graph_id,
            'business_id': self.business_id,
            'business_name': self.business_name,
            'primary_region': self.primary_region,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'nodes': nodes_data,
            'edges': edges_data
        }
    
    def get_shortest_path(self, source_node_id: str, target_node_id: str) -> Optional[List[str]]:
        """
        Find shortest data flow path between two nodes
        
        Tim duong di ngan nhat giua hai nut
        
        Args:
            source_node_id: Starting node
            target_node_id: Ending node
        
        Returns:
            List of node IDs in the path, or None if no path exists
        """
        try:
            path = nx.shortest_path(self.graph, source_node_id, target_node_id)
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
    
    def find_mps_reportable_flows(self) -> Dict[str, Any]:
        """
        Find all flows requiring MPS notification under Vietnamese PDPL
        
        Tim luong du lieu can bao cao cho Bo Cong an (MPS)
        
        Returns:
            Dict with reportable flows and threshold analysis
        """
        # Count data subjects by category
        category_1_count = 0
        category_2_count = 0
        
        for node_id, data in self.graph.nodes(data=True):
            categories = data.get('data_categories', [])
            record_count = data.get('estimated_record_count', 0)
            
            if 'Category 1' in categories:
                category_1_count += record_count
            if 'Category 2' in categories:
                category_2_count += record_count
        
        # Check MPS thresholds from Section 1
        exceeds_cat1_threshold = category_1_count >= self.config.MPS_THRESHOLD_CATEGORY_1
        exceeds_cat2_threshold = category_2_count >= self.config.MPS_THRESHOLD_CATEGORY_2
        
        # Get cross-border flows requiring MPS notification
        cross_border_flows = self.find_cross_border_flows()
        unsent_notifications = [
            flow for flow in cross_border_flows 
            if not flow.get('mps_notification_sent', False)
        ]
        
        return {
            'category_1_data_subjects': category_1_count,
            'category_2_data_subjects': category_2_count,
            'mps_threshold_category_1': self.config.MPS_THRESHOLD_CATEGORY_1,
            'mps_threshold_category_2': self.config.MPS_THRESHOLD_CATEGORY_2,
            'exceeds_cat1_threshold': exceeds_cat1_threshold,
            'exceeds_cat2_threshold': exceeds_cat2_threshold,
            'requires_mps_registration': exceeds_cat1_threshold or exceeds_cat2_threshold,
            'total_cross_border_flows': len(cross_border_flows),
            'unsent_mps_notifications': len(unsent_notifications),
            'pending_notifications': unsent_notifications
        }


# Export
__all__ = ['DataFlowGraph']
