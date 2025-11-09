"""
VeriSyntra Data Inventory Configuration Constants

Centralized configuration for veri-ai-data-inventory microservice.
This module follows VeriSyntra's dynamic coding principles:
- Single source of truth for all configuration values
- DRY (Don't Repeat Yourself) compliance
- Easy maintenance and environment-specific overrides
- Vietnamese business context support

Usage:
    from backend.veri_ai_data_inventory.config.constants import ScanConfig, DatabaseConfig
    
    limit = ScanConfig.DEFAULT_SAMPLE_SIZE
    port = DatabaseConfig.POSTGRESQL_DEFAULT_PORT
"""

from typing import Dict, List


class ScanConfig:
    """Data scanning operation configuration"""
    
    # Sample extraction settings
    DEFAULT_SAMPLE_SIZE: int = 100
    """Default number of rows to sample from database columns"""
    
    MAX_SAMPLE_PREVIEW: int = 10
    """Maximum number of samples to include in preview/response"""
    
    ERROR_PREVIEW_LENGTH: int = 50
    """Maximum characters to show in error messages for data samples"""
    
    # Pattern detection settings
    CONFIDENCE_THRESHOLD: float = 0.7
    """Minimum confidence score (0.0-1.0) for pattern detection (70%)"""
    
    MIN_UNIQUE_THRESHOLD: float = 0.1
    """Minimum ratio of unique values for diverse sampling (10%)"""
    
    # Statistics and reporting
    TOP_VALUES_COUNT: int = 10
    """Number of top values to include in distribution statistics"""
    
    # Job estimation
    ESTIMATED_SCAN_TIME_SECONDS: int = 300
    """Default estimated time for scan job completion (5 minutes)"""


class DatabaseConfig:
    """Database connection default values"""
    
    # Port numbers
    POSTGRESQL_DEFAULT_PORT: int = 5432
    """Default PostgreSQL port"""
    
    MYSQL_DEFAULT_PORT: int = 3306
    """Default MySQL port"""
    
    MONGODB_DEFAULT_PORT: int = 27017
    """Default MongoDB port"""
    
    # Schema and authentication defaults
    DEFAULT_SCHEMA: str = 'public'
    """Default PostgreSQL schema name"""
    
    MONGODB_DEFAULT_AUTH_SOURCE: str = 'admin'
    """Default MongoDB authentication database"""


class EncodingConfig:
    """UTF-8 encoding constants for Vietnamese text support"""
    
    # PostgreSQL encoding
    POSTGRESQL_CLIENT_ENCODING: str = 'utf8'
    """PostgreSQL client encoding for Vietnamese diacritics"""
    
    POSTGRESQL_OPTIONS: str = '-c client_encoding=utf8'
    """PostgreSQL connection options for UTF-8"""
    
    # MySQL encoding
    MYSQL_CHARSET: str = 'utf8mb4'
    """MySQL character set for full Unicode support including Vietnamese"""
    
    MYSQL_SET_NAMES: str = 'SET NAMES utf8mb4'
    """MySQL command to set connection character set"""
    
    MYSQL_SET_CHARSET: str = 'SET CHARACTER SET utf8mb4'
    """MySQL command to set client character set"""
    
    # Python encoding
    PYTHON_IO_ENCODING: str = 'utf-8'
    """Python I/O encoding for filesystem operations"""
    
    # MongoDB encoding
    MONGODB_UNICODE_ERROR_HANDLER: str = 'strict'
    """MongoDB Unicode error handling (fail on invalid UTF-8)"""


class CloudConfig:
    """Cloud storage scanning configuration"""
    
    # AWS S3 settings
    DEFAULT_AWS_REGION: str = 'ap-southeast-1'
    """Default AWS region (Southeast Asia - Singapore) for Vietnamese market"""
    
    DEFAULT_MAX_KEYS: int = 1000
    """Maximum number of S3 objects to scan per request"""
    
    DEFAULT_MAX_BYTES: int = 10240
    """Maximum bytes to download for content sampling (10KB)"""
    
    S3_DEFAULT_STORAGE_CLASS: str = 'STANDARD'
    """Default S3 storage class"""
    
    # Azure Blob settings
    AZURE_DEFAULT_MAX_BLOBS: int = 1000
    """Maximum number of Azure blobs to scan per request"""
    
    # Google Cloud Storage settings
    GCS_DEFAULT_MAX_OBJECTS: int = 1000
    """Maximum number of GCS objects to scan per request"""


class FilesystemConfig:
    """Filesystem scanning configuration"""
    
    DEFAULT_MAX_DEPTH: int = 5
    """Maximum directory depth for recursive scanning"""
    
    DEFAULT_MAX_FILES: int = 10000
    """Maximum number of files to discover per scan"""
    
    DEFAULT_FOLLOW_SYMLINKS: bool = False
    """Whether to follow symbolic links during scanning"""
    
    DEFAULT_MIN_FILE_SIZE: int = 0
    """Minimum file size in bytes (0 = no minimum)"""
    
    EXCLUDED_EXTENSIONS: List[str] = ['.tmp', '.log', '.cache', '.bak', '.swp']
    """File extensions to exclude from scanning"""


class ScanManagerConfig:
    """Scanner Manager orchestration configuration"""
    
    MAX_CONCURRENT_SCANS: int = 5
    """Maximum number of concurrent scanner instances"""
    
    DEFAULT_RETRY_ATTEMPTS: int = 3
    """Number of retry attempts for failed scanner connections"""
    
    RETRY_DELAY_SECONDS: int = 5
    """Delay in seconds between retry attempts"""
    
    SCANNER_TIMEOUT_SECONDS: int = 600
    """Maximum time in seconds for single scanner operation (10 minutes)"""
    
    MAX_RESULTS_PER_SCANNER: int = 10000
    """Maximum number of results to collect per scanner instance"""
    
    ENABLE_PARALLEL_SCANNING: bool = True
    """Enable parallel scanning across multiple data sources"""
    
    PROGRESS_UPDATE_INTERVAL_SECONDS: int = 10
    """Interval for progress updates during long-running scans"""


class VietnameseRegionalConfig:
    """
    Vietnamese business context configuration
    
    VeriSyntra supports regional variations in Vietnamese business practices:
    - North (Hanoi): More formal, government-focused, thorough documentation
    - South (HCMC): Entrepreneurial, faster decisions, international exposure
    - Central (Da Nang/Hue): Traditional values, consensus-building
    
    Future enhancement: Region-specific sample sizes and thresholds
    """
    
    # Regional sample size preferences (future implementation)
    NORTH_SAMPLE_SIZE: int = 100  # Hanoi: thorough, formal approach
    SOUTH_SAMPLE_SIZE: int = 50   # HCMC: faster, efficiency-focused
    CENTRAL_SAMPLE_SIZE: int = 75  # Da Nang/Hue: balanced approach
    
    # Regional confidence thresholds (future implementation)
    NORTH_CONFIDENCE_THRESHOLD: float = 0.8  # Higher precision requirement
    SOUTH_CONFIDENCE_THRESHOLD: float = 0.6  # More flexible
    CENTRAL_CONFIDENCE_THRESHOLD: float = 0.7  # Standard


class APIConfig:
    """API endpoint configuration - zero hard-coding"""
    
    # API Versioning
    API_VERSION: str = "v1"
    """API version string"""
    
    API_PREFIX: str = "/api/v1/data-inventory"
    """API route prefix for all data inventory endpoints"""
    
    API_TAGS: List[str] = ["Data Discovery", "Scan Management"]
    """OpenAPI tags for endpoint documentation"""
    
    # Job Status Enums (not hard-coded strings)
    STATUS_PENDING: str = "pending"
    """Scan job is queued but not started"""
    
    STATUS_RUNNING: str = "running"
    """Scan job is currently executing"""
    
    STATUS_COMPLETED: str = "completed"
    """Scan job finished successfully"""
    
    STATUS_FAILED: str = "failed"
    """Scan job encountered an error"""
    
    STATUS_CANCELLED: str = "cancelled"
    """Scan job was cancelled by user"""
    
    VALID_STATUSES: List[str] = [
        "pending", "running", "completed", "failed", "cancelled"
    ]
    """All valid job status values"""
    
    # HTTP Configuration
    MAX_REQUEST_SIZE_MB: int = 10
    """Maximum request body size in megabytes"""
    
    REQUEST_TIMEOUT_SECONDS: int = 30
    """Default HTTP request timeout in seconds"""
    
    LONG_RUNNING_TIMEOUT_SECONDS: int = 300
    """Timeout for long-running scan operations (5 minutes)"""
    
    MAX_CONCURRENT_REQUESTS: int = 100
    """Maximum number of concurrent API requests"""
    
    # Background Task Configuration
    BACKGROUND_TASK_CHECK_INTERVAL_SECONDS: int = 5
    """How often to check background task status"""
    
    MAX_BACKGROUND_TASKS: int = 50
    """Maximum number of background tasks in queue"""
    
    TASK_RETENTION_HOURS: int = 24
    """How long to retain completed task results (hours)"""
    
    # Response Configuration
    MAX_ASSETS_PER_RESPONSE: int = 1000
    """Maximum number of discovered assets in single response"""
    
    MAX_ERROR_MESSAGE_LENGTH: int = 500
    """Maximum characters in error messages"""
    
    MAX_ERRORS_PER_RESPONSE: int = 10
    """Maximum number of error messages in response"""
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    """Default number of items per page in API responses"""
    
    MAX_PAGE_SIZE: int = 200
    """Maximum allowed page size"""
    
    # CORS Configuration
    CORS_ALLOW_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    """Allowed CORS origins for frontend"""
    
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    """Allowed HTTP methods for CORS"""
    
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    """Allowed headers for CORS"""
    
    # Legacy compatibility (deprecated - use new names)
    DEFAULT_REQUEST_TIMEOUT: int = REQUEST_TIMEOUT_SECONDS
    """@deprecated Use REQUEST_TIMEOUT_SECONDS instead"""
    
    LONG_RUNNING_TIMEOUT: int = LONG_RUNNING_TIMEOUT_SECONDS
    """@deprecated Use LONG_RUNNING_TIMEOUT_SECONDS instead"""


# Configuration export for convenient imports
__all__ = [
    'ScanConfig',
    'DatabaseConfig',
    'EncodingConfig',
    'CloudConfig',
    'FilesystemConfig',
    'VietnameseRegionalConfig',
    'APIConfig',
]


# Validation function for configuration integrity
def validate_config() -> Dict[str, bool]:
    """
    Validate configuration constants for consistency
    
    Returns:
        Dictionary of validation results
    """
    validations = {
        'sample_size_positive': ScanConfig.DEFAULT_SAMPLE_SIZE > 0,
        'preview_smaller_than_sample': (
            ScanConfig.MAX_SAMPLE_PREVIEW <= ScanConfig.DEFAULT_SAMPLE_SIZE
        ),
        'confidence_in_range': (
            0.0 <= ScanConfig.CONFIDENCE_THRESHOLD <= 1.0
        ),
        'ports_valid': all([
            1024 <= DatabaseConfig.POSTGRESQL_DEFAULT_PORT <= 65535,
            1024 <= DatabaseConfig.MYSQL_DEFAULT_PORT <= 65535,
            1024 <= DatabaseConfig.MONGODB_DEFAULT_PORT <= 65535,
        ]),
        'max_depth_positive': FilesystemConfig.DEFAULT_MAX_DEPTH > 0,
    }
    
    return validations


if __name__ == '__main__':
    # Run validation when module is executed directly
    print("[OK] VeriSyntra Configuration Constants")
    print(f"[OK] Default sample size: {ScanConfig.DEFAULT_SAMPLE_SIZE}")
    print(f"[OK] PostgreSQL port: {DatabaseConfig.POSTGRESQL_DEFAULT_PORT}")
    print(f"[OK] AWS region: {CloudConfig.DEFAULT_AWS_REGION}")
    
    validations = validate_config()
    all_valid = all(validations.values())
    
    print(f"\n[OK] Configuration validation: {'PASSED' if all_valid else 'FAILED'}")
    for check, result in validations.items():
        status = '[OK]' if result else '[ERROR]'
        print(f"{status} {check}: {result}")
