"""
GCSScanner for Google Cloud Storage scanning
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


class GCSScanner:
    """Google Cloud Storage scanner with Vietnamese filename support and dynamic configuration"""
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Initialize GCS scanner with dynamic configuration
        
        Args:
            connection_config: {
                'project_id': str,
                'credentials_path': str (optional, uses default credentials if not provided),
                'bucket_name': str
            }
        """
        self.config = connection_config
        self.storage_client = None
        self.bucket = None
        self.utf8_validator = UTF8Validator()
    
    def connect(self) -> bool:
        """
        Connect to Google Cloud Storage using dynamic configuration
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Lazy import to avoid requiring google-cloud-storage if not used
            from google.cloud import storage
            from google.api_core.exceptions import GoogleAPIError
            
            # Initialize client with credentials if provided
            if 'credentials_path' in self.config:
                self.storage_client = storage.Client.from_service_account_json(
                    self.config['credentials_path'],
                    project=self.config['project_id']
                )
            else:
                # Use default credentials
                self.storage_client = storage.Client(
                    project=self.config['project_id']
                )
            
            # Get bucket
            bucket_name = self.config['bucket_name']
            self.bucket = self.storage_client.bucket(bucket_name)
            
            # Test connection by checking if bucket exists
            if not self.bucket.exists():
                raise ValueError(f"Bucket {bucket_name} does not exist")
            
            logger.info(f"[OK] Connected to GCS bucket: {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] GCS connection failed: {str(e)}")
            return False
    
    def discover_objects(
        self,
        prefix: str = '',
        max_objects: int = None  # Will use CloudConfig.GCS_DEFAULT_MAX_OBJECTS if None
    ) -> Dict[str, Any]:
        """
        Discover GCS objects (files) with Vietnamese filename support
        
        Args:
            prefix: GCS prefix (folder path)
            max_objects: Maximum objects to scan (uses CloudConfig.GCS_DEFAULT_MAX_OBJECTS if None)
            
        Returns:
            {
                'objects': [
                    {
                        'name': str,  # Object name (UTF-8 Vietnamese filenames)
                        'size': int,
                        'updated': datetime,
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
        if not self.bucket:
            raise RuntimeError("GCS not connected. Call connect() first.")
        
        # Use dynamic config for max_objects default
        if max_objects is None:
            max_objects = CloudConfig.GCS_DEFAULT_MAX_OBJECTS
        
        objects_info = {
            'objects': [],
            'total_size': 0,
            'total_count': 0,
            'vietnamese_filename_count': 0
        }
        
        try:
            # List blobs with prefix
            blobs = self.bucket.list_blobs(prefix=prefix, max_results=max_objects)
            
            for blob in blobs:
                name = blob.name
                size = blob.size
                
                # Skip directories (blobs with name ending in /)
                if name.endswith('/'):
                    continue
                
                # Validate UTF-8 in object name (Vietnamese filenames)
                validation = self.utf8_validator.validate(name)
                if not validation['is_valid']:
                    logger.warning(f"[WARNING] Invalid UTF-8 in GCS object name: {name}")
                    continue
                
                # Check for Vietnamese characters in filename
                is_vietnamese = validation['has_vietnamese']
                if is_vietnamese:
                    objects_info['vietnamese_filename_count'] += 1
                
                # Extract file extension
                file_extension = name.split('.')[-1] if '.' in name else ''
                
                objects_info['objects'].append({
                    'name': name,
                    'size': size,
                    'updated': blob.updated,
                    'content_type': blob.content_type,
                    'file_extension': file_extension,
                    'is_vietnamese_filename': is_vietnamese
                })
                
                objects_info['total_size'] += size
                objects_info['total_count'] += 1
            
            logger.info(
                f"[OK] Discovered {objects_info['total_count']} objects "
                f"({objects_info['total_size'] / (1024**2):.2f} MB), "
                f"{objects_info['vietnamese_filename_count']} with Vietnamese names"
            )
            
            return objects_info
            
        except Exception as e:
            logger.error(f"[ERROR] GCS object discovery failed: {str(e)}")
            raise
    
    def get_object_metadata(self, object_name: str) -> Dict[str, Any]:
        """
        Get GCS object metadata with Vietnamese filename validation
        
        Args:
            object_name: GCS object name (Vietnamese filename supported)
            
        Returns:
            Object metadata dictionary with UTF-8 validation
        """
        if not self.bucket:
            raise RuntimeError("GCS not connected. Call connect() first.")
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(object_name)
        if not validation['is_valid']:
            raise ValueError(f"Invalid UTF-8 in GCS object name: {object_name}")
        
        try:
            blob = self.bucket.blob(object_name)
            blob.reload()  # Fetch metadata from GCS
            
            metadata = {
                'name': object_name,
                'content_type': blob.content_type,
                'size': blob.size,
                'updated': blob.updated,
                'created': blob.time_created,
                'md5_hash': blob.md5_hash,
                'metadata': blob.metadata or {},
                'has_vietnamese_filename': validation['has_vietnamese'],
                'vietnamese_char_count': validation['vietnamese_char_count']
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to get metadata for {object_name}: {str(e)}")
            raise
    
    def download_sample_content(
        self,
        object_name: str,
        max_bytes: int = None  # Will use CloudConfig.DEFAULT_MAX_BYTES if None
    ) -> Optional[bytes]:
        """
        Download first N bytes of GCS object for sampling
        
        Args:
            object_name: GCS object name
            max_bytes: Maximum bytes to download (uses CloudConfig.DEFAULT_MAX_BYTES if None)
            
        Returns:
            First N bytes of object content
        """
        if not self.bucket:
            raise RuntimeError("GCS not connected. Call connect() first.")
        
        # Use dynamic config for max_bytes default
        if max_bytes is None:
            max_bytes = CloudConfig.DEFAULT_MAX_BYTES
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(object_name)
        if not validation['is_valid']:
            logger.error(f"[ERROR] Invalid UTF-8 in GCS object name: {object_name}")
            return None
        
        try:
            blob = self.bucket.blob(object_name)
            
            # Download only first N bytes using start and end parameters
            content = blob.download_as_bytes(start=0, end=max_bytes)
            
            logger.info(
                f"[OK] Downloaded {len(content)} bytes from {object_name} "
                f"(Vietnamese: {validation['has_vietnamese']})"
            )
            
            return content
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to download sample from {object_name}: {str(e)}")
            return None
    
    def close(self):
        """Close GCS connection and cleanup resources"""
        if self.storage_client:
            # GCS client is automatically managed, no explicit close needed
            self.storage_client = None
            self.bucket = None
            logger.info("[OK] GCS scanner closed")
