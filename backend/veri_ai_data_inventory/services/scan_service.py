"""
VeriSyntra Scan Service

Main orchestration service that integrates ScannerManager (Step 6) with API layer.
Handles background execution and Vietnamese business context-aware scanning.

Key Features:
- Integrates with ScannerManager for multi-source scanning
- Vietnamese business context support
- Column filtering integration
- Progress tracking and error handling
- Dynamic configuration (zero hard-coding)
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

# Import dynamic configuration
try:
    from ..config.constants import APIConfig, ScanConfig
    from ..scanner_manager.scanner_manager import ScannerManager
    from ..services.job_state_manager import get_job_state_manager, JobState
except ImportError:
    from config.constants import APIConfig, ScanConfig
    from scanner_manager.scanner_manager import ScannerManager
    from services.job_state_manager import get_job_state_manager, JobState

logger = logging.getLogger(__name__)


class ScanService:
    """
    Main scan orchestration service
    
    Coordinates between API endpoints, ScannerManager, and job state management.
    Uses dynamic configuration throughout - zero hard-coded values.
    """
    
    def __init__(self):
        """Initialize scan service"""
        self.scanner_manager = ScannerManager()
        self.job_state_manager = get_job_state_manager()
        logger.info("[OK] ScanService initialized")
    
    async def create_scan_job(
        self,
        scan_job_id: UUID,
        tenant_id: UUID,
        source_type: str,
        connection_config: Dict[str, Any],
        column_filter: Optional[Dict[str, Any]] = None,
        veri_business_context: Optional[Dict[str, Any]] = None
    ) -> JobState:
        """
        Create new scan job
        
        Args:
            scan_job_id: Unique job identifier
            tenant_id: Tenant identifier
            source_type: Data source type
            connection_config: Connection configuration
            column_filter: Column filtering config (optional)
            veri_business_context: Vietnamese business context (optional)
        
        Returns:
            Created job state
        """
        try:
            job_state = self.job_state_manager.create_job(
                scan_job_id=scan_job_id,
                tenant_id=tenant_id,
                source_type=source_type,
                connection_config=connection_config,
                column_filter=column_filter,
                veri_business_context=veri_business_context
            )
            
            logger.info(
                f"[OK] Scan job {scan_job_id} created for tenant {tenant_id}"
            )
            
            return job_state
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to create scan job: {str(e)}")
            raise
    
    async def execute_scan(
        self,
        scan_job_id: UUID,
        tenant_id: UUID,
        source_type: str,
        connection_config: Dict[str, Any],
        column_filter: Optional[Dict[str, Any]] = None,
        veri_business_context: Optional[Dict[str, Any]] = None
    ):
        """
        Execute scan in background
        
        This method orchestrates the entire scanning process:
        1. Start the job
        2. Create appropriate scanner from ScannerManager
        3. Execute scan with progress tracking
        4. Process results
        5. Update job state
        """
        job = self.job_state_manager.get_job(scan_job_id)
        if not job:
            logger.error(f"[ERROR] Job {scan_job_id} not found")
            return
        
        try:
            # Mark job as started - uses APIConfig.STATUS_RUNNING
            job.start()
            
            logger.info(
                f"[OK] Executing scan job {scan_job_id} "
                f"(source: {source_type}, tenant: {tenant_id})"
            )
            
            # Determine scanner type from connection_config
            scanner_type = self._determine_scanner_type(source_type, connection_config)
            
            # Create scanner using ScannerManager (Step 6)
            scanner = self.scanner_manager.create_scanner(
                scanner_type=scanner_type,
                connection_config=connection_config
            )
            
            # Connect to data source
            if not scanner.connect():
                raise RuntimeError(f"Failed to connect to {scanner_type}")
            
            # Update progress
            job.update_progress(20)
            
            # Execute discovery based on source type
            if source_type == "database":
                results = await self._scan_database(
                    scanner=scanner,
                    connection_config=connection_config,
                    column_filter=column_filter,
                    job=job
                )
            elif source_type == "cloud":
                results = await self._scan_cloud_storage(
                    scanner=scanner,
                    connection_config=connection_config,
                    job=job
                )
            elif source_type == "filesystem":
                results = await self._scan_filesystem(
                    scanner=scanner,
                    connection_config=connection_config,
                    job=job
                )
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
            
            # Process and normalize results
            discovered_assets = self._process_results(results, veri_business_context)
            filter_statistics = results.get('filter_statistics')
            
            # Mark job as completed - uses APIConfig.STATUS_COMPLETED
            job.complete(
                discovered_assets=discovered_assets,
                filter_statistics=filter_statistics
            )
            
            logger.info(
                f"[OK] Scan job {scan_job_id} completed successfully: "
                f"{len(discovered_assets)} assets discovered"
            )
            
        except Exception as e:
            error_msg = str(e)[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]  # Use config limit
            job.fail(error_msg)
            logger.error(f"[ERROR] Scan job {scan_job_id} failed: {error_msg}")
        
        finally:
            # Ensure scanner is closed
            try:
                if 'scanner' in locals():
                    scanner.close()
            except Exception as e:
                logger.warning(f"[WARNING] Error closing scanner: {str(e)}")
    
    async def get_scan_status(self, scan_job_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get scan job status
        
        Args:
            scan_job_id: Job identifier
        
        Returns:
            Job state dictionary or None if not found
        """
        job = self.job_state_manager.get_job(scan_job_id)
        if not job:
            return None
        
        return job.to_dict()
    
    async def cancel_scan(self, scan_job_id: UUID) -> bool:
        """
        Cancel running scan job
        
        Args:
            scan_job_id: Job identifier
        
        Returns:
            True if cancelled, False if not found
        """
        job = self.job_state_manager.get_job(scan_job_id)
        if not job:
            return False
        
        # Can only cancel non-terminal jobs
        if job.is_terminal():
            logger.warning(
                f"[WARNING] Cannot cancel job {scan_job_id} "
                f"in terminal state: {job.status}"
            )
            return False
        
        job.cancel()
        return True
    
    def _determine_scanner_type(
        self,
        source_type: str,
        connection_config: Dict[str, Any]
    ) -> str:
        """Determine specific scanner type from source_type and config"""
        if source_type == "database":
            # Get scanner_type from config (e.g., 'postgresql', 'mysql', 'mongodb')
            return connection_config.get('scanner_type', 'postgresql')
        elif source_type == "cloud":
            # Get cloud provider (e.g., 's3', 'azure_blob', 'gcs')
            return connection_config.get('provider', 's3')
        elif source_type == "filesystem":
            # Get filesystem type (e.g., 'local_filesystem', 'network_share')
            return connection_config.get('filesystem_type', 'local_filesystem')
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    
    async def _scan_database(
        self,
        scanner: Any,
        connection_config: Dict[str, Any],
        column_filter: Optional[Dict[str, Any]],
        job: JobState
    ) -> Dict[str, Any]:
        """Scan database source with column filtering"""
        # Get schema/database name
        schema = connection_config.get('schema', 'public')
        database = connection_config.get('database', '')
        
        # Discover schema
        job.update_progress(40)
        schema_info = scanner.discover()
        
        job.update_progress(60)
        
        # Apply column filtering if provided
        if column_filter:
            try:
                # Import column filtering services
                from ..services.column_filter_service import ColumnFilterService
                from ..models.column_filter import ColumnFilterConfig
                
                # Parse filter configuration
                filter_config = ColumnFilterConfig(**column_filter)
                
                # Apply filtering to each table
                filter_stats = {
                    'total_tables': 0,
                    'total_columns_discovered': 0,
                    'total_columns_scanned': 0,
                    'columns_filtered_out': 0
                }
                
                for table in schema_info.get('tables', []):
                    all_columns = [col['column_name'] for col in table.get('columns', [])]
                    
                    # Filter columns
                    filtered_columns = ColumnFilterService.filter_columns(
                        all_columns,
                        filter_config
                    )
                    
                    # Update statistics
                    filter_stats['total_tables'] += 1
                    filter_stats['total_columns_discovered'] += len(all_columns)
                    filter_stats['total_columns_scanned'] += len(filtered_columns)
                    filter_stats['columns_filtered_out'] += len(all_columns) - len(filtered_columns)
                    
                    # Keep only filtered columns in results
                    table['columns'] = [
                        col for col in table.get('columns', [])
                        if col['column_name'] in filtered_columns
                    ]
                    table['all_columns_count'] = len(all_columns)
                    table['scanned_columns_count'] = len(filtered_columns)
                
                # Calculate reduction percentage
                if filter_stats['total_columns_discovered'] > 0:
                    reduction = (
                        filter_stats['columns_filtered_out'] /
                        filter_stats['total_columns_discovered']
                    ) * 100
                    filter_stats['reduction_percentage'] = round(reduction, 2)
                else:
                    filter_stats['reduction_percentage'] = 0.0
                
                # Add filter statistics to results
                schema_info['filter_statistics'] = filter_stats
                
                logger.info(
                    f"[OK] Column filtering applied: {filter_stats['total_columns_scanned']}/"
                    f"{filter_stats['total_columns_discovered']} columns selected "
                    f"({filter_stats['reduction_percentage']}% reduction)"
                )
                
            except Exception as e:
                logger.error(f"[ERROR] Column filtering failed: {str(e)}")
                # Continue with unfiltered results on error
                pass
        
        job.update_progress(80)
        
        return schema_info
    
    async def _scan_cloud_storage(
        self,
        scanner: Any,
        connection_config: Dict[str, Any],
        job: JobState
    ) -> Dict[str, Any]:
        """Scan cloud storage source"""
        job.update_progress(40)
        
        # Discover cloud objects
        objects_info = scanner.discover()
        
        job.update_progress(80)
        
        return objects_info
    
    async def _scan_filesystem(
        self,
        scanner: Any,
        connection_config: Dict[str, Any],
        job: JobState
    ) -> Dict[str, Any]:
        """Scan filesystem source"""
        job.update_progress(40)
        
        # Discover files
        files_info = scanner.discover()
        
        job.update_progress(80)
        
        return files_info
    
    def _process_results(
        self,
        results: Dict[str, Any],
        veri_business_context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process and normalize scan results
        
        Converts scanner-specific results into standardized discovered assets.
        """
        discovered_assets = []
        
        # Handle different result structures
        if 'tables' in results:
            # Database results
            for table in results.get('tables', []):
                asset = {
                    'asset_type': 'table',
                    'asset_name': table.get('table_name', ''),
                    'asset_path': table.get('full_name', ''),
                    'column_count': table.get('column_count', 0),
                    'row_count': table.get('row_count', 0),
                    'size_bytes': table.get('size_bytes'),
                    'has_vietnamese_data': table.get('has_vietnamese_data', False),
                    'pdpl_sensitive': self._is_pdpl_sensitive(table)
                }
                discovered_assets.append(asset)
        
        elif 'objects' in results:
            # Cloud storage results
            for obj in results.get('objects', []):
                asset = {
                    'asset_type': 'object',
                    'asset_name': obj.get('key', ''),
                    'asset_path': obj.get('key', ''),
                    'size_bytes': obj.get('size', 0),
                    'has_vietnamese_data': False,  # Would need content analysis
                    'pdpl_sensitive': False
                }
                discovered_assets.append(asset)
        
        elif 'files' in results:
            # Filesystem results
            for file_info in results.get('files', []):
                asset = {
                    'asset_type': 'file',
                    'asset_name': file_info.get('filename', ''),
                    'asset_path': file_info.get('path', ''),
                    'size_bytes': file_info.get('size', 0),
                    'has_vietnamese_data': False,  # Would need content analysis
                    'pdpl_sensitive': False
                }
                discovered_assets.append(asset)
        
        # Limit results using config
        return discovered_assets[:APIConfig.MAX_ASSETS_PER_RESPONSE]
    
    def _is_pdpl_sensitive(self, table_info: Dict[str, Any]) -> bool:
        """Determine if table contains PDPL-sensitive data"""
        # Simple heuristic - check for common personal data column patterns
        pdpl_patterns = [
            'ho_ten', 'email', 'so_dien_thoai', 'cmnd', 'cccd',
            'dia_chi', 'ngay_sinh', 'phone', 'address', 'name'
        ]
        
        columns = table_info.get('columns', [])
        if isinstance(columns, list):
            column_names = [str(col).lower() for col in columns]
            return any(pattern in ' '.join(column_names) for pattern in pdpl_patterns)
        
        return False


# Global service instance (for development/prototype)
_scan_service_instance = None


def get_scan_service() -> ScanService:
    """Get or create global ScanService instance"""
    global _scan_service_instance
    
    if _scan_service_instance is None:
        _scan_service_instance = ScanService()
    
    return _scan_service_instance
