"""
VeriSyntra Scanner Manager

Central orchestrator for all scanner operations with Vietnamese UTF-8 support.
Manages scanner lifecycle, error handling, and multi-source coordination.
"""

import logging
import uuid
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Flexible import pattern
try:
    from ..config import ScanManagerConfig
    from ..utils import UTF8Validator
except ImportError:
    from config.constants import ScanManagerConfig
    from utils.utf8_validator import UTF8Validator

from .scanner_registry import ScannerRegistry
from .scanner_interface import BaseScannerAdapter
from .error_handler import ScanErrorHandler
from .progress_tracker import ScanProgressTracker, ScanStatus
from .result_aggregator import ResultAggregator

logger = logging.getLogger(__name__)


class ScannerManager:
    """
    Unified scanner lifecycle manager with Vietnamese UTF-8 support.
    
    Orchestrates all scanner types (database, cloud, filesystem) with:
    - Dynamic configuration (zero hard-coding)
    - Error handling and retry logic
    - Progress tracking
    - Multi-source parallel scanning
    - Result aggregation
    """
    
    def __init__(
        self,
        utf8_validator: Optional[UTF8Validator] = None,
        max_concurrent_scans: int = ScanManagerConfig.MAX_CONCURRENT_SCANS,
        scan_timeout: int = ScanManagerConfig.SCANNER_TIMEOUT_SECONDS,
        enable_parallel: bool = ScanManagerConfig.ENABLE_PARALLEL_SCANNING
    ):
        """
        Initialize Scanner Manager with dynamic configuration.
        
        Args:
            utf8_validator: Vietnamese UTF-8 validator (default: creates new instance)
            max_concurrent_scans: Maximum concurrent scans (default from ScanManagerConfig)
            scan_timeout: Scan timeout in seconds (default from ScanManagerConfig)
            enable_parallel: Enable parallel scanning (default from ScanManagerConfig)
        """
        self.validator = utf8_validator or UTF8Validator()
        self.max_concurrent = max_concurrent_scans
        self.timeout = scan_timeout
        self.enable_parallel = enable_parallel
        
        self.registry = ScannerRegistry()
        self.error_handler = ScanErrorHandler()
        self.progress_tracker = ScanProgressTracker()
        self.result_aggregator = ResultAggregator()
        
        self.active_scanners: Dict[str, Any] = {}
        
        logger.info(
            f"[OK] ScannerManager initialized (max_concurrent: {self.max_concurrent}, "
            f"timeout: {self.timeout}s, parallel: {self.enable_parallel})"
        )
    
    def create_scanner(
        self,
        scanner_type: str,
        connection_config: Dict[str, Any]
    ) -> Optional[Any]:
        """
        Create a scanner instance from registry.
        
        Args:
            scanner_type: Scanner type identifier (postgresql, s3, etc.)
            connection_config: Connection configuration dictionary
            
        Returns:
            Scanner instance or None if creation failed
        """
        # Validate scanner type
        if not self.registry.validate_scanner_type(scanner_type):
            logger.error(f"[ERROR] Invalid scanner type: {scanner_type}")
            return None
        
        # Get scanner class
        scanner_class = self.registry.get_scanner_class(scanner_type)
        if not scanner_class:
            logger.error(f"[ERROR] Failed to load scanner class: {scanner_type}")
            return None
        
        try:
            # Create scanner instance
            # Pass UTF8Validator to scanners that support it
            if scanner_type in ['local_filesystem', 'network_share']:
                scanner = scanner_class(self.validator, connection_config)
            else:
                scanner = scanner_class(connection_config)
            
            logger.info(f"[OK] Created scanner instance: {scanner_type}")
            return scanner
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to create scanner {scanner_type}: {str(e)}")
            return None
    
    def execute_scan(
        self,
        scanner_type: str,
        connection_config: Dict[str, Any],
        scan_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute complete scan lifecycle: connect -> discover -> close.
        
        Args:
            scanner_type: Scanner type identifier
            connection_config: Connection configuration
            scan_options: Optional scanning parameters
            
        Returns:
            Scan results dictionary
        """
        scan_id = str(uuid.uuid4())
        scan_options = scan_options or {}
        
        # Start progress tracking
        scanner_category = self.registry.get_scanner_category(scanner_type)
        self.progress_tracker.start_scan(
            scan_id,
            scanner_type,
            description=f"Scanning {scanner_category} source"
        )
        
        try:
            # Create scanner
            self.progress_tracker.update_progress(
                scan_id,
                status=ScanStatus.CONNECTING,
                current_operation='Creating scanner instance'
            )
            
            scanner = self.create_scanner(scanner_type, connection_config)
            if not scanner:
                raise RuntimeError(f"Failed to create scanner: {scanner_type}")
            
            self.active_scanners[scan_id] = scanner
            
            # Connect with retry
            self.progress_tracker.update_progress(
                scan_id,
                status=ScanStatus.CONNECTING,
                progress_percent=20.0,
                current_operation='Connecting to source'
            )
            
            connect_result = self.error_handler.retry_on_failure(scanner.connect)
            
            if isinstance(connect_result, dict) and connect_result.get('status') == 'error':
                raise RuntimeError(f"Connection failed: {connect_result.get('message')}")
            
            # Discover data
            self.progress_tracker.update_progress(
                scan_id,
                status=ScanStatus.DISCOVERING,
                progress_percent=50.0,
                current_operation='Discovering data assets'
            )
            
            discover_result = scanner.discover_files(**scan_options) \
                if scanner_type in ['local_filesystem', 'network_share'] \
                else scanner.discover(**scan_options)
            
            # Count discovered items
            item_count = len(discover_result) if isinstance(discover_result, list) else \
                        discover_result.get('count', 0) if isinstance(discover_result, dict) else 0
            
            self.progress_tracker.update_progress(
                scan_id,
                progress_percent=100.0,
                items_discovered=item_count,
                current_operation='Scan completed'
            )
            
            # Close scanner
            scanner.close()
            
            # Mark as completed
            self.progress_tracker.complete_scan(scan_id, success=True)
            
            # Create standardized response
            result = BaseScannerAdapter.create_success_response(
                message=f'Scan completed successfully',
                data=discover_result,
                count=item_count,
                scan_id=scan_id,
                scanner_type=scanner_type,
                scanner_category=scanner_category
            )
            
            logger.info(
                f"[OK] Scan {scan_id} completed: {item_count} items discovered "
                f"from {scanner_type}"
            )
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[ERROR] Scan {scan_id} failed: {error_msg}")
            
            # Mark as failed
            self.progress_tracker.complete_scan(scan_id, success=False, error_message=error_msg)
            
            return self.error_handler.create_error_response(
                message='Scan failed',
                error=e,
                scan_id=scan_id,
                scanner_type=scanner_type
            )
            
        finally:
            # Cleanup
            if scan_id in self.active_scanners:
                try:
                    self.active_scanners[scan_id].close()
                except Exception:
                    pass
                del self.active_scanners[scan_id]
    
    def execute_multi_source_scan(
        self,
        scan_requests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Execute scans across multiple sources (database + cloud + filesystem).
        
        Args:
            scan_requests: List of scan request dictionaries:
                [
                    {
                        'scanner_type': str,
                        'connection_config': dict,
                        'scan_options': dict (optional),
                        'source_identifier': str (optional)
                    }
                ]
        
        Returns:
            Aggregated results from all scanners
        """
        logger.info(f"[INFO] Starting multi-source scan: {len(scan_requests)} sources")
        
        # Clear previous results
        self.result_aggregator.clear()
        
        if self.enable_parallel and len(scan_requests) > 1:
            # Parallel scanning
            results = self._execute_parallel_scans(scan_requests)
        else:
            # Sequential scanning
            results = self._execute_sequential_scans(scan_requests)
        
        # Aggregate all results
        for request, result in zip(scan_requests, results):
            scanner_type = request['scanner_type']
            scanner_category = self.registry.get_scanner_category(scanner_type)
            source_id = request.get('source_identifier', '')
            
            self.result_aggregator.add_scanner_results(
                scanner_type,
                scanner_category,
                result,
                source_id
            )
        
        # Get aggregated results
        aggregated = self.result_aggregator.get_aggregated_results()
        statistics = self.result_aggregator.get_statistics()
        
        logger.info(
            f"[OK] Multi-source scan completed: {statistics['total_items_discovered']} "
            f"items from {statistics['successful_sources']}/{statistics['total_sources']} sources"
        )
        
        return {
            'status': 'success',
            'message': 'Multi-source scan completed',
            'results': aggregated,
            'statistics': statistics
        }
    
    def _execute_parallel_scans(
        self,
        scan_requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute scans in parallel using thread pool"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            # Submit all scan jobs
            future_to_request = {
                executor.submit(
                    self.execute_scan,
                    req['scanner_type'],
                    req['connection_config'],
                    req.get('scan_options', {})
                ): req
                for req in scan_requests
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_request):
                try:
                    result = future.result(timeout=self.timeout)
                    results.append(result)
                except Exception as e:
                    logger.error(f"[ERROR] Parallel scan failed: {str(e)}")
                    results.append(self.error_handler.create_error_response(
                        message='Parallel scan failed',
                        error=e
                    ))
        
        return results
    
    def _execute_sequential_scans(
        self,
        scan_requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute scans sequentially"""
        results = []
        
        for request in scan_requests:
            result = self.execute_scan(
                request['scanner_type'],
                request['connection_config'],
                request.get('scan_options', {})
            )
            results.append(result)
        
        return results
    
    def get_scan_status(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific scan"""
        return self.progress_tracker.get_scan_status(scan_id)
    
    def get_all_scan_statuses(self) -> List[Dict[str, Any]]:
        """Get status of all tracked scans"""
        return self.progress_tracker.get_all_scans()
    
    def get_active_scans(self) -> List[Dict[str, Any]]:
        """Get all currently active scans"""
        return self.progress_tracker.get_active_scans()
    
    def cancel_scan(self, scan_id: str) -> bool:
        """Cancel an active scan"""
        return self.progress_tracker.cancel_scan(scan_id)
    
    def list_available_scanners(self) -> Dict[str, str]:
        """List all available scanner types"""
        return self.registry.list_available_scanners()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        return {
            'progress': self.progress_tracker.get_summary(),
            'results': self.result_aggregator.get_statistics(),
            'errors': self.error_handler.get_error_summary()
        }
