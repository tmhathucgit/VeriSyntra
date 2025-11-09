"""
S3Scanner for AWS S3 bucket scanning
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


class S3Scanner:
    """AWS S3 bucket scanner with Vietnamese filename support and dynamic configuration"""
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Initialize S3 scanner with dynamic configuration
        
        Args:
            connection_config: {
                'aws_access_key_id': str,
                'aws_secret_access_key': str,
                'region_name': str (optional, defaults to CloudConfig.DEFAULT_AWS_REGION),
                'bucket_name': str
            }
        """
        self.config = connection_config
        self.s3_client = None
        self.s3_resource = None
        self.utf8_validator = UTF8Validator()
    
    def connect(self) -> bool:
        """
        Connect to AWS S3 using dynamic configuration
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Lazy import to avoid requiring boto3 if not used
            import boto3
            from botocore.exceptions import ClientError, NoCredentialsError
            
            # Use dynamic config for region default
            region = self.config.get('region_name', CloudConfig.DEFAULT_AWS_REGION)
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.config['aws_access_key_id'],
                aws_secret_access_key=self.config['aws_secret_access_key'],
                region_name=region
            )
            
            self.s3_resource = boto3.resource(
                's3',
                aws_access_key_id=self.config['aws_access_key_id'],
                aws_secret_access_key=self.config['aws_secret_access_key'],
                region_name=region
            )
            
            # Test connection
            bucket_name = self.config['bucket_name']
            self.s3_client.head_bucket(Bucket=bucket_name)
            
            logger.info(f"[OK] Connected to S3 bucket: {bucket_name} (region: {region})")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] S3 connection failed: {str(e)}")
            return False
    
    def discover_objects(
        self,
        prefix: str = '',
        max_keys: int = None  # Will use CloudConfig.DEFAULT_MAX_KEYS if None
    ) -> Dict[str, Any]:
        """
        Discover S3 objects (files) with Vietnamese filename support
        
        Args:
            prefix: S3 prefix (folder path)
            max_keys: Maximum objects to scan (uses CloudConfig.DEFAULT_MAX_KEYS if None)
            
        Returns:
            {
                'objects': [
                    {
                        'key': str,  # Full path (UTF-8 Vietnamese filenames)
                        'size': int,
                        'last_modified': datetime,
                        'storage_class': str,
                        'file_extension': str,
                        'is_vietnamese_filename': bool
                    }
                ],
                'total_size': int,
                'total_count': int,
                'vietnamese_filename_count': int
            }
        """
        if not self.s3_client:
            raise RuntimeError("S3 not connected. Call connect() first.")
        
        # Use dynamic config for max_keys default
        if max_keys is None:
            max_keys = CloudConfig.DEFAULT_MAX_KEYS
        
        bucket_name = self.config['bucket_name']
        objects_info = {
            'objects': [],
            'total_size': 0,
            'total_count': 0,
            'vietnamese_filename_count': 0
        }
        
        try:
            # Import here to avoid circular import and allow mocking
            import boto3
            from botocore.exceptions import ClientError
            
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(
                Bucket=bucket_name,
                Prefix=prefix,
                PaginationConfig={'MaxItems': max_keys}
            )
            
            for page in pages:
                if 'Contents' not in page:
                    continue
                
                for obj in page['Contents']:
                    key = obj['Key']
                    size = obj['Size']
                    
                    # Skip folders (keys ending with /)
                    if key.endswith('/'):
                        continue
                    
                    # Validate UTF-8 in key (Vietnamese filenames)
                    validation = self.utf8_validator.validate(key)
                    if not validation['is_valid']:
                        logger.warning(f"[WARNING] Invalid UTF-8 in S3 key: {key}")
                        continue
                    
                    # Check for Vietnamese characters in filename
                    is_vietnamese = validation['has_vietnamese']
                    if is_vietnamese:
                        objects_info['vietnamese_filename_count'] += 1
                    
                    # Extract file extension
                    file_extension = key.split('.')[-1] if '.' in key else ''
                    
                    objects_info['objects'].append({
                        'key': key,
                        'size': size,
                        'last_modified': obj['LastModified'],
                        'storage_class': obj.get('StorageClass', 'STANDARD'),
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
            logger.error(f"[ERROR] S3 object discovery failed: {str(e)}")
            raise
    
    def get_object_metadata(self, key: str) -> Dict[str, Any]:
        """
        Get S3 object metadata with Vietnamese filename validation
        
        Args:
            key: S3 object key (Vietnamese filename supported)
            
        Returns:
            Object metadata dictionary with UTF-8 validation
        """
        if not self.s3_client:
            raise RuntimeError("S3 not connected. Call connect() first.")
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(key)
        if not validation['is_valid']:
            raise ValueError(f"Invalid UTF-8 in S3 key: {key}")
        
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            bucket_name = self.config['bucket_name']
            response = self.s3_client.head_object(Bucket=bucket_name, Key=key)
            
            metadata = {
                'key': key,
                'content_type': response.get('ContentType'),
                'content_length': response.get('ContentLength'),
                'last_modified': response.get('LastModified'),
                'etag': response.get('ETag'),
                'metadata': response.get('Metadata', {}),
                'has_vietnamese_filename': validation['has_vietnamese'],
                'vietnamese_char_count': validation['vietnamese_char_count']
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to get metadata for {key}: {str(e)}")
            raise
    
    def download_sample_content(
        self,
        key: str,
        max_bytes: int = None  # Will use CloudConfig.DEFAULT_MAX_BYTES if None
    ) -> Optional[bytes]:
        """
        Download first N bytes of S3 object for sampling
        
        Args:
            key: S3 object key
            max_bytes: Maximum bytes to download (uses CloudConfig.DEFAULT_MAX_BYTES if None)
            
        Returns:
            First N bytes of object content
        """
        if not self.s3_client:
            raise RuntimeError("S3 not connected. Call connect() first.")
        
        # Use dynamic config for max_bytes default
        if max_bytes is None:
            max_bytes = CloudConfig.DEFAULT_MAX_BYTES
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(key)
        if not validation['is_valid']:
            logger.error(f"[ERROR] Invalid UTF-8 in S3 key: {key}")
            return None
        
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            bucket_name = self.config['bucket_name']
            
            # Use Range header to download only first N bytes
            response = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=key,
                Range=f'bytes=0-{max_bytes-1}'
            )
            
            content = response['Body'].read()
            
            logger.info(
                f"[OK] Downloaded {len(content)} bytes from {key} "
                f"(Vietnamese: {validation['has_vietnamese']})"
            )
            
            return content
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to download sample from {key}: {str(e)}")
            return None
    
    def close(self):
        """Close S3 connection and cleanup resources"""
        if self.s3_client:
            # boto3 clients are automatically managed, no explicit close needed
            self.s3_client = None
            self.s3_resource = None
            logger.info("[OK] S3 scanner closed")
