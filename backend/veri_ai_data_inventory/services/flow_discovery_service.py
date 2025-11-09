"""
Flow Discovery Service - Section 4

Automated data flow discovery for Vietnamese PDPL 2025 compliance
Discovers flows from databases, APIs, file systems, and cloud storage
"""

from typing import Dict, List, Optional, Any, Tuple
import re
import ipaddress
from datetime import datetime

# Import previous sections
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config.flow_constants import FlowMappingConfig
from models.flow_models import (
    DataAssetNode,
    DataFlowEdge,
    NodeType,
    EdgeType
)
from graph.flow_graph import DataFlowGraph


class FlowDiscoveryService:
    """
    Automated data flow discovery service
    
    Dich vu phat hien tu dong luong du lieu
    (Automated data flow discovery service)
    
    Features:
    - Discover database-to-database flows
    - Discover API endpoint flows
    - Detect Vietnamese regions from location
    - Geolocate IP addresses to countries
    - Auto-classify data categories
    - Generate DataFlowGraph automatically
    """
    
    def __init__(self, graph: DataFlowGraph):
        """
        Initialize flow discovery service
        
        Args:
            graph: DataFlowGraph instance to populate
        """
        self.graph = graph
        self.config = FlowMappingConfig()
        
        # Track discovered flows
        self.discovered_nodes: List[str] = []
        self.discovered_edges: List[str] = []
    
    def discover_database_flows(
        self,
        database_metadata: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Discover data flows from database metadata
        
        Phat hien luong du lieu tu metadata co so du lieu
        
        Args:
            database_metadata: List of database info dicts with:
                - database_id: str
                - database_name: str
                - location: str (city or IP)
                - tables: List[str]
                - estimated_records: int
                - connections: List[Dict] with target_database_id, purpose
        
        Returns:
            Dict with discovered nodes and edges count
        """
        nodes_added = 0
        edges_added = 0
        
        # First pass: Add all nodes
        for db_info in database_metadata:
            # Extract database info
            db_id = db_info.get('database_id')
            db_name = db_info.get('database_name')
            location = db_info.get('location', '')
            tables = db_info.get('tables', [])
            estimated_records = db_info.get('estimated_records', 0)
            
            # Detect Vietnamese region from location
            vietnamese_region = self._detect_region(location)
            
            # Auto-classify data categories based on table names
            data_categories = self._classify_data_categories(tables)
            
            # Determine if sensitive data
            sensitive_data = 'Category 2' in data_categories
            
            # Check MPS notification requirement (Category 2 with high volume)
            mps_required = (
                'Category 2' in data_categories and 
                estimated_records >= self.config.MPS_THRESHOLD_CATEGORY_2
            ) or (
                'Category 1' in data_categories and 
                estimated_records >= self.config.MPS_THRESHOLD_CATEGORY_1
            )
            
            # Create node
            node = DataAssetNode(
                node_id=db_id,
                node_type=NodeType.DATABASE,
                name=db_name,
                location=location,
                vietnamese_region=vietnamese_region,
                data_categories=data_categories,
                estimated_record_count=estimated_records,
                sensitive_data=sensitive_data,
                pdpl_compliant=True,  # Assume compliant initially
                mps_notification_required=mps_required,
                metadata={
                    'tables': tables,
                    'discovered_at': datetime.now().isoformat()
                }
            )
            
            # Add node to graph
            if self.graph.add_node(node):
                nodes_added += 1
                self.discovered_nodes.append(db_id)
        
        # Second pass: Add all edges (now that all nodes exist)
        for db_info in database_metadata:
            db_id = db_info.get('database_id')
            location = db_info.get('location', '')
            estimated_records = db_info.get('estimated_records', 0)
            connections = db_info.get('connections', [])
            
            # Create edges for connections
            for connection in connections:
                target_db_id = connection.get('target_database_id')
                purpose = connection.get('purpose', '')
                
                # Detect if cross-border based on source and target locations
                source_country = self._geolocate_ip(location)
                target_location = self._find_node_location(target_db_id)
                target_country = self._geolocate_ip(target_location) if target_location else 'VN'
                
                is_cross_border = source_country != 'VN' or target_country != 'VN'
                
                # Create edge
                edge = DataFlowEdge(
                    edge_id=f"flow_{db_id}_to_{target_db_id}",
                    source_node_id=db_id,
                    target_node_id=target_db_id,
                    edge_type=EdgeType.CROSS_BORDER_TRANSFER if is_cross_border else EdgeType.DATA_TRANSFER,
                    data_volume=estimated_records,
                    frequency='daily',  # Default frequency
                    encryption_enabled=True,  # Assume encrypted
                    is_cross_border=is_cross_border,
                    source_country=source_country,
                    target_country=target_country,
                    metadata={
                        'processing_purpose': purpose,
                        'discovered_at': datetime.now().isoformat()
                    }
                )
                
                # Add edge to graph
                if self.graph.add_edge(edge):
                    edges_added += 1
                    self.discovered_edges.append(edge.edge_id)
        
        return {
            'nodes_added': nodes_added,
            'edges_added': edges_added,
            'total_nodes': len(self.discovered_nodes),
            'total_edges': len(self.discovered_edges)
        }
    
    def discover_api_flows(
        self,
        api_metadata: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Discover data flows from API endpoint metadata
        
        Phat hien luong du lieu tu metadata API
        
        Args:
            api_metadata: List of API info dicts with:
                - api_id: str
                - api_name: str
                - endpoint_url: str
                - location: str (server location or IP)
                - data_sources: List[str] (source node IDs)
                - data_targets: List[str] (target node IDs)
                - estimated_requests_per_day: int
        
        Returns:
            Dict with discovered nodes and edges count
        """
        nodes_added = 0
        edges_added = 0
        
        for api_info in api_metadata:
            # Extract API info
            api_id = api_info.get('api_id')
            api_name = api_info.get('api_name')
            endpoint_url = api_info.get('endpoint_url', '')
            location = api_info.get('location', '')
            data_sources = api_info.get('data_sources', [])
            data_targets = api_info.get('data_targets', [])
            requests_per_day = api_info.get('estimated_requests_per_day', 0)
            
            # Detect Vietnamese region
            vietnamese_region = self._detect_region(location)
            
            # Create API node
            node = DataAssetNode(
                node_id=api_id,
                node_type=NodeType.API_ENDPOINT,
                name=api_name,
                location=location,
                vietnamese_region=vietnamese_region,
                data_categories=['Category 1'],  # APIs typically handle basic data
                estimated_record_count=requests_per_day,
                sensitive_data=False,
                pdpl_compliant=True,
                mps_notification_required=False,
                metadata={
                    'endpoint_url': endpoint_url,
                    'discovered_at': datetime.now().isoformat()
                }
            )
            
            # Add node to graph
            if self.graph.add_node(node):
                nodes_added += 1
                self.discovered_nodes.append(api_id)
            
            # Create edges from data sources to API
            for source_id in data_sources:
                source_location = self._find_node_location(source_id)
                source_country = self._geolocate_ip(source_location) if source_location else 'VN'
                target_country = self._geolocate_ip(location)
                
                is_cross_border = source_country != 'VN' or target_country != 'VN'
                
                edge = DataFlowEdge(
                    edge_id=f"api_input_{source_id}_to_{api_id}",
                    source_node_id=source_id,
                    target_node_id=api_id,
                    edge_type=EdgeType.API_CALL,
                    data_volume=requests_per_day,
                    frequency='real-time',
                    encryption_enabled=True,
                    is_cross_border=is_cross_border,
                    source_country=source_country,
                    target_country=target_country,
                    metadata={
                        'processing_purpose': 'API data retrieval',
                        'discovered_at': datetime.now().isoformat()
                    }
                )
                
                if self.graph.add_edge(edge):
                    edges_added += 1
                    self.discovered_edges.append(edge.edge_id)
            
            # Create edges from API to data targets
            for target_id in data_targets:
                source_country = self._geolocate_ip(location)
                target_location = self._find_node_location(target_id)
                target_country = self._geolocate_ip(target_location) if target_location else 'VN'
                
                is_cross_border = source_country != 'VN' or target_country != 'VN'
                
                edge = DataFlowEdge(
                    edge_id=f"api_output_{api_id}_to_{target_id}",
                    source_node_id=api_id,
                    target_node_id=target_id,
                    edge_type=EdgeType.API_CALL,
                    data_volume=requests_per_day,
                    frequency='real-time',
                    encryption_enabled=True,
                    is_cross_border=is_cross_border,
                    source_country=source_country,
                    target_country=target_country,
                    metadata={
                        'processing_purpose': 'API data transfer',
                        'discovered_at': datetime.now().isoformat()
                    }
                )
                
                if self.graph.add_edge(edge):
                    edges_added += 1
                    self.discovered_edges.append(edge.edge_id)
        
        return {
            'nodes_added': nodes_added,
            'edges_added': edges_added,
            'total_nodes': len(self.discovered_nodes),
            'total_edges': len(self.discovered_edges)
        }
    
    def _detect_region(self, location: str) -> Optional[str]:
        """
        Detect Vietnamese region from location string
        
        Phat hien vung Viet Nam tu chuoi vi tri
        
        Args:
            location: Location string (city name, address, or IP)
        
        Returns:
            'north', 'central', 'south', or None
        """
        if not location:
            return None
        
        location_lower = location.lower()
        
        # Check against Vietnamese regions from Section 1
        for region, cities in self.config.VIETNAMESE_REGIONS.items():
            for city in cities:
                if city.lower() in location_lower:
                    return region
        
        # Fallback: common city name matching
        north_keywords = ['hanoi', 'hà nội', 'haiphong', 'hải phòng', 'north', 'bắc']
        central_keywords = ['danang', 'đà nẵng', 'hue', 'huế', 'central', 'trung']
        south_keywords = ['saigon', 'sài gòn', 'ho chi minh', 'hồ chí minh', 'hcmc', 'south', 'nam']
        
        for keyword in north_keywords:
            if keyword in location_lower:
                return 'north'
        
        for keyword in central_keywords:
            if keyword in location_lower:
                return 'central'
        
        for keyword in south_keywords:
            if keyword in location_lower:
                return 'south'
        
        return None
    
    def _geolocate_ip(self, location: str) -> str:
        """
        Geolocate IP address to country code
        
        Xac dinh quoc gia tu dia chi IP
        
        Args:
            location: Location string (may contain IP address)
        
        Returns:
            2-letter country code (defaults to 'VN')
        """
        if not location:
            return 'VN'
        
        # Extract IP address from location string
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip_match = re.search(ip_pattern, location)
        
        if ip_match:
            ip_str = ip_match.group(0)
            
            try:
                ip_obj = ipaddress.IPv4Address(ip_str)
                
                # Check against Vietnamese IP ranges from Section 1
                for ip_range in self.config.VIETNAMESE_IP_RANGES:
                    network = ipaddress.IPv4Network(ip_range)
                    if ip_obj in network:
                        return 'VN'
                
                # If not in Vietnamese ranges, check common foreign ranges
                # Singapore: 8.0.0.0/8 (simplified example)
                if ip_str.startswith('8.'):
                    return 'SG'
                
                # US: 3.0.0.0/8 (simplified example)
                if ip_str.startswith('3.'):
                    return 'US'
                
                # Default to VN if unknown
                return 'VN'
                
            except ValueError:
                # Invalid IP, return VN
                return 'VN'
        
        # No IP found, check for country keywords
        location_lower = location.lower()
        
        if any(keyword in location_lower for keyword in ['singapore', 'sg']):
            return 'SG'
        if any(keyword in location_lower for keyword in ['united states', 'usa', 'us']):
            return 'US'
        if any(keyword in location_lower for keyword in ['japan', 'jp', 'tokyo']):
            return 'JP'
        
        # Default to Vietnam
        return 'VN'
    
    def _classify_data_categories(self, tables: List[str]) -> List[str]:
        """
        Auto-classify data categories based on table names
        
        Tu dong phan loai du lieu dua tren ten bang
        
        Args:
            tables: List of table names
        
        Returns:
            List of data categories (Category 1, Category 2, Non-Personal)
        """
        categories = set()
        
        for table in tables:
            table_lower = table.lower()
            
            # Check Category 2 keywords (sensitive data)
            for keyword in self.config.CATEGORY_2_KEYWORDS:
                if keyword.lower() in table_lower:
                    categories.add('Category 2')
                    break
            
            # Check Category 1 keywords (basic personal data)
            for keyword in self.config.CATEGORY_1_KEYWORDS:
                if keyword.lower() in table_lower:
                    categories.add('Category 1')
                    break
        
        # If no categories found, default to Category 1
        if not categories:
            categories.add('Category 1')
        
        return list(categories)
    
    def _find_node_location(self, node_id: str) -> Optional[str]:
        """
        Find location of a node in the graph
        
        Tim vi tri cua nut trong do thi
        
        Args:
            node_id: Node identifier
        
        Returns:
            Location string or None
        """
        node_data = self.graph.get_node(node_id)
        if node_data:
            return node_data.get('location')
        return None
    
    def get_discovery_summary(self) -> Dict[str, Any]:
        """
        Get summary of discovered flows
        
        Lay tom tat luong du lieu da phat hien
        
        Returns:
            Dict with discovery statistics
        """
        return {
            'total_nodes_discovered': len(self.discovered_nodes),
            'total_edges_discovered': len(self.discovered_edges),
            'discovered_nodes': self.discovered_nodes,
            'discovered_edges': self.discovered_edges,
            'graph_statistics': self.graph.get_graph_statistics().model_dump()
        }


# Export
__all__ = ['FlowDiscoveryService']
