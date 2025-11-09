"""
VeriSyntra Result Aggregator

Aggregates and normalizes results from multiple scanner sources.
Provides deduplication and统一 result format.
"""

import logging
from typing import Dict, Any, List, Optional, Set
from collections import defaultdict

logger = logging.getLogger(__name__)


class ResultAggregator:
    """
    Aggregate results from multiple scanners into unified format.
    
    Provides deduplication, categorization, and statistics for
    multi-source scan results.
    """
    
    def __init__(self):
        """Initialize result aggregator"""
        self.aggregated_results: Dict[str, Any] = {
            'sources': [],
            'total_items': 0,
            'items_by_category': defaultdict(int),
            'items_by_scanner_type': defaultdict(int),
            'errors': [],
            'metadata': {}
        }
        self.seen_items: Set[str] = set()
    
    def add_scanner_results(
        self,
        scanner_type: str,
        scanner_category: str,
        results: Dict[str, Any],
        source_identifier: str = ''
    ) -> None:
        """
        Add results from a scanner.
        
        Args:
            scanner_type: Type of scanner (postgresql, s3, etc.)
            scanner_category: Category (database, cloud, filesystem)
            results: Scanner results dictionary
            source_identifier: Optional identifier for the source
        """
        if results.get('status') == 'error':
            self.aggregated_results['errors'].append({
                'scanner_type': scanner_type,
                'source': source_identifier,
                'error': results.get('message', 'Unknown error')
            })
            logger.warning(
                f"[WARNING] Scanner {scanner_type} returned error: "
                f"{results.get('message')}"
            )
            return
        
        # Extract item count
        item_count = results.get('count', 0)
        if item_count == 0:
            # Try alternative count fields
            data = results.get('data', {})
            if isinstance(data, dict):
                item_count = (
                    len(data.get('tables', [])) +
                    len(data.get('objects', [])) +
                    len(data.get('files', []))
                )
        
        # Add to source list
        source_entry = {
            'scanner_type': scanner_type,
            'scanner_category': scanner_category,
            'source_identifier': source_identifier,
            'item_count': item_count,
            'status': results.get('status', 'success')
        }
        self.aggregated_results['sources'].append(source_entry)
        
        # Update counters
        self.aggregated_results['total_items'] += item_count
        self.aggregated_results['items_by_category'][scanner_category] += item_count
        self.aggregated_results['items_by_scanner_type'][scanner_type] += item_count
        
        logger.info(
            f"[OK] Added {item_count} items from {scanner_type} "
            f"({scanner_category})"
        )
    
    def deduplicate_items(
        self,
        items: List[Dict[str, Any]],
        key_field: str = 'path'
    ) -> List[Dict[str, Any]]:
        """
        Deduplicate items based on a key field.
        
        Args:
            items: List of item dictionaries
            key_field: Field to use for deduplication
            
        Returns:
            Deduplicated list of items
        """
        unique_items = []
        
        for item in items:
            item_key = item.get(key_field, '')
            
            if not item_key:
                # No key field, include anyway
                unique_items.append(item)
                continue
            
            if item_key not in self.seen_items:
                self.seen_items.add(item_key)
                unique_items.append(item)
            else:
                logger.debug(f"[INFO] Skipping duplicate item: {item_key}")
        
        if len(items) > len(unique_items):
            logger.info(
                f"[OK] Deduplicated {len(items)} items to {len(unique_items)} "
                f"({len(items) - len(unique_items)} duplicates removed)"
            )
        
        return unique_items
    
    def get_aggregated_results(self) -> Dict[str, Any]:
        """
        Get the final aggregated results.
        
        Returns:
            Aggregated results dictionary
        """
        return {
            'sources': self.aggregated_results['sources'],
            'total_items': self.aggregated_results['total_items'],
            'items_by_category': dict(self.aggregated_results['items_by_category']),
            'items_by_scanner_type': dict(self.aggregated_results['items_by_scanner_type']),
            'total_sources': len(self.aggregated_results['sources']),
            'total_errors': len(self.aggregated_results['errors']),
            'errors': self.aggregated_results['errors'],
            'metadata': self.aggregated_results['metadata']
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get summary statistics.
        
        Returns:
            Statistics dictionary
        """
        total_sources = len(self.aggregated_results['sources'])
        successful_sources = sum(
            1 for s in self.aggregated_results['sources']
            if s['status'] == 'success'
        )
        
        return {
            'total_sources': total_sources,
            'successful_sources': successful_sources,
            'failed_sources': len(self.aggregated_results['errors']),
            'success_rate': (successful_sources / total_sources * 100) if total_sources > 0 else 0.0,
            'total_items_discovered': self.aggregated_results['total_items'],
            'unique_items': len(self.seen_items),
            'categories': list(self.aggregated_results['items_by_category'].keys()),
            'scanner_types': list(self.aggregated_results['items_by_scanner_type'].keys())
        }
    
    def merge_metadata(
        self,
        scanner_type: str,
        metadata: Dict[str, Any]
    ) -> None:
        """
        Merge scanner-specific metadata into aggregated results.
        
        Args:
            scanner_type: Scanner type identifier
            metadata: Metadata dictionary to merge
        """
        if scanner_type not in self.aggregated_results['metadata']:
            self.aggregated_results['metadata'][scanner_type] = []
        
        self.aggregated_results['metadata'][scanner_type].append(metadata)
    
    def clear(self) -> None:
        """Clear all aggregated results"""
        self.aggregated_results = {
            'sources': [],
            'total_items': 0,
            'items_by_category': defaultdict(int),
            'items_by_scanner_type': defaultdict(int),
            'errors': [],
            'metadata': {}
        }
        self.seen_items.clear()
        logger.info("[OK] Result aggregator cleared")
    
    @staticmethod
    def normalize_database_results(results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize database scanner results to standard format.
        
        Args:
            results: Database scanner results
            
        Returns:
            Normalized results dictionary
        """
        normalized = {
            'type': 'database',
            'items': [],
            'count': 0
        }
        
        tables = results.get('data', {}).get('tables', [])
        
        for table in tables:
            normalized['items'].append({
                'resource_type': 'table',
                'name': table.get('table_name', ''),
                'columns': len(table.get('columns', [])),
                'row_count': table.get('row_count', 0)
            })
        
        normalized['count'] = len(normalized['items'])
        return normalized
    
    @staticmethod
    def normalize_cloud_results(results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize cloud storage scanner results to standard format.
        
        Args:
            results: Cloud scanner results
            
        Returns:
            Normalized results dictionary
        """
        normalized = {
            'type': 'cloud',
            'items': [],
            'count': 0
        }
        
        # Handle S3 objects
        objects = results.get('data', {}).get('objects', [])
        
        for obj in objects:
            normalized['items'].append({
                'resource_type': 'object',
                'key': obj.get('key', ''),
                'size': obj.get('size', 0),
                'storage_class': obj.get('storage_class', 'STANDARD')
            })
        
        normalized['count'] = len(normalized['items'])
        return normalized
    
    @staticmethod
    def normalize_filesystem_results(results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize filesystem scanner results to standard format.
        
        Args:
            results: Filesystem scanner results
            
        Returns:
            Normalized results dictionary
        """
        normalized = {
            'type': 'filesystem',
            'items': [],
            'count': 0
        }
        
        files = results.get('data', {}).get('files', [])
        
        for file_info in files:
            normalized['items'].append({
                'resource_type': 'file',
                'path': file_info.get('path', ''),
                'size': file_info.get('size', 0),
                'extension': file_info.get('extension', '')
            })
        
        normalized['count'] = len(normalized['items'])
        return normalized
