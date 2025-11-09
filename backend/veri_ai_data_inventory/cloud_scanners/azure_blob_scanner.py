"""
AzureBlobScanner for Azure Blob Storage scanning
Uses dynamic configuration from CloudConfig
Zero hard-coding - all operational values from centralized config
Vietnamese UTF-8 filename support
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Flexible import pattern for package and standalone execution
try:
    from ..config import CloudConfig, ScanConfig
    from ..utils import UTF8Validator
except ImportError:
    from config import CloudConfig, ScanConfig
    from utils import UTF8Validator

logger = logging.getLogger(__name__)


class AzureBlobScanner:
    """Azure Blob Storage scanner with Vietnamese filename support and dynamic configuration"""
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Initialize Azure Blob scanner with dynamic configuration
        
        Args:
            connection_config: {
                'connection_string': str,
                'container_name': str
            }
        """
        self.config = connection_config
        self.blob_service_client = None
        self.container_client = None
        self.utf8_validator = UTF8Validator()
    
    def connect(self) -> bool:
        """
        Connect to Azure Blob Storage using dynamic configuration
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Lazy import to avoid requiring azure-storage-blob if not used
            from azure.storage.blob import BlobServiceClient
            from azure.core.exceptions import AzureError
            
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.config['connection_string']
            )
            
            container_name = self.config['container_name']
            self.container_client = self.blob_service_client.get_container_client(
                container_name
            )
            
            # Test connection by getting container properties
            self.container_client.get_container_properties()
            
            logger.info(f"[OK] Connected to Azure Blob container: {container_name}")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Azure Blob connection failed: {str(e)}")
            return False
    
    def discover_blobs(
        self,
        name_starts_with: str = '',
        max_blobs: int = None  # Will use CloudConfig.AZURE_DEFAULT_MAX_BLOBS if None
    ) -> Dict[str, Any]:
        """
        Discover Azure blobs with Vietnamese filename support
        
        Args:
            name_starts_with: Filter blobs by name prefix
            max_blobs: Maximum blobs to scan (uses CloudConfig.AZURE_DEFAULT_MAX_BLOBS if None)
            
        Returns:
            {
                'blobs': [
                    {
                        'name': str,  # Blob name (UTF-8 Vietnamese filenames)
                        'size': int,
                        'last_modified': datetime,
                        'content_type': str,
                        'file_extension': str,
                        'is_vietnamese_filename': bool
                    }
                ],
                'total_size': int,
                'total_count': int,
                'vietnamese_filename_count': int
            }
        """
        if not self.container_client:
            raise RuntimeError("Azure Blob not connected. Call connect() first.")
        
        # Use dynamic config for max_blobs default
        if max_blobs is None:
            max_blobs = CloudConfig.AZURE_DEFAULT_MAX_BLOBS
        
        blobs_info = {
            'blobs': [],
            'total_size': 0,
            'total_count': 0,
            'vietnamese_filename_count': 0
        }
        
        try:
            # List blobs with name filter
            blob_list = self.container_client.list_blobs(
                name_starts_with=name_starts_with
            )
            
            for blob in blob_list:
                # Limit to max_blobs
                if blobs_info['total_count'] >= max_blobs:
                    break
                
                name = blob.name
                size = blob.size
                
                # Skip directories (blobs with name ending in /)
                if name.endswith('/'):
                    continue
                
                # Validate UTF-8 in blob name (Vietnamese filenames)
                validation = self.utf8_validator.validate(name)
                if not validation['is_valid']:
                    logger.warning(f"[WARNING] Invalid UTF-8 in blob name: {name}")
                    continue
                
                # Check for Vietnamese characters in filename
                is_vietnamese = validation['has_vietnamese']
                if is_vietnamese:
                    blobs_info['vietnamese_filename_count'] += 1
                
                # Extract file extension
                file_extension = name.split('.')[-1] if '.' in name else ''
                
                blobs_info['blobs'].append({
                    'name': name,
                    'size': size,
                    'last_modified': blob.last_modified,
                    'content_type': blob.content_settings.content_type if blob.content_settings else None,
                    'file_extension': file_extension,
                    'is_vietnamese_filename': is_vietnamese
                })
                
                blobs_info['total_size'] += size
                blobs_info['total_count'] += 1
            
            logger.info(
                f"[OK] Discovered {blobs_info['total_count']} blobs "
                f"({blobs_info['total_size'] / (1024**2):.2f} MB), "
                f"{blobs_info['vietnamese_filename_count']} with Vietnamese names"
            )
            
            return blobs_info
            
        except Exception as e:
            logger.error(f"[ERROR] Azure Blob discovery failed: {str(e)}")
            raise
    
    def get_blob_metadata(self, blob_name: str) -> Dict[str, Any]:
        """
        Get Azure blob metadata with Vietnamese filename validation
        
        Args:
            blob_name: Blob name (Vietnamese filename supported)
            
        Returns:
            Blob metadata dictionary with UTF-8 validation
        """
        if not self.container_client:
            raise RuntimeError("Azure Blob not connected. Call connect() first.")
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(blob_name)
        if not validation['is_valid']:
            raise ValueError(f"Invalid UTF-8 in blob name: {blob_name}")
        
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            properties = blob_client.get_blob_properties()
            
            metadata = {
                'name': blob_name,
                'content_type': properties.content_settings.content_type if properties.content_settings else None,
                'content_length': properties.size,
                'last_modified': properties.last_modified,
                'etag': properties.etag,
                'metadata': properties.metadata,
                'has_vietnamese_filename': validation['has_vietnamese'],
                'vietnamese_char_count': validation['vietnamese_char_count']
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to get metadata for {blob_name}: {str(e)}")
            raise
    
    def download_sample_content(
        self,
        blob_name: str,
        max_bytes: int = None  # Will use CloudConfig.DEFAULT_MAX_BYTES if None
    ) -> Optional[bytes]:
        """
        Download first N bytes of Azure blob for sampling
        
        Args:
            blob_name: Blob name
            max_bytes: Maximum bytes to download (uses CloudConfig.DEFAULT_MAX_BYTES if None)
            
        Returns:
            First N bytes of blob content
        """
        if not self.container_client:
            raise RuntimeError("Azure Blob not connected. Call connect() first.")
        
        # Use dynamic config for max_bytes default
        if max_bytes is None:
            max_bytes = CloudConfig.DEFAULT_MAX_BYTES
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(blob_name)
        if not validation['is_valid']:
            logger.error(f"[ERROR] Invalid UTF-8 in blob name: {blob_name}")
            return None
        
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            
            # Download only first N bytes using offset and length
            download_stream = blob_client.download_blob(offset=0, length=max_bytes)
            content = download_stream.readall()
            
            logger.info(
                f"[OK] Downloaded {len(content)} bytes from {blob_name} "
                f"(Vietnamese: {validation['has_vietnamese']})"
            )
            
            return content
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to download sample from {blob_name}: {str(e)}")
            return None
    
    def close(self):
        """Close Azure Blob connection and cleanup resources"""
        if self.blob_service_client:
            # Azure SDK handles cleanup automatically
            self.blob_service_client = None
            self.container_client = None
            logger.info("[OK] Azure Blob scanner closed")
