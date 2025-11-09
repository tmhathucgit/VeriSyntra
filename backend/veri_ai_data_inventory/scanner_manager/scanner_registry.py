"""
VeriSyntra Scanner Registry

Central registry of all available scanner types with lazy import support.
Maps scanner type identifiers to their implementation classes.
"""

from typing import Dict, Type, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ScannerRegistry:
    """
    Central registry for all VeriSyntra scanner implementations.
    
    Provides lazy loading of scanner classes to avoid import errors
    when optional dependencies are not installed.
    """
    
    # Scanner type mappings
    # Format: 'scanner_type': ('module_path', 'ClassName')
    _SCANNER_MAPPINGS: Dict[str, tuple] = {
        # Database scanners (Step 2)
        'postgresql': ('database_scanners.postgresql_scanner', 'PostgreSQLScanner'),
        'mysql': ('database_scanners.mysql_scanner', 'MySQLScanner'),
        'mongodb': ('database_scanners.mongodb_scanner', 'MongoDBScanner'),
        'mssql': ('database_scanners.mssql_scanner', 'MSSQLScanner'),
        
        # Cloud scanners (Step 4)
        's3': ('cloud_scanners.s3_scanner', 'S3Scanner'),
        'azure_blob': ('cloud_scanners.azure_blob_scanner', 'AzureBlobScanner'),
        'gcs': ('cloud_scanners.gcs_scanner', 'GCSScanner'),
        
        # Filesystem scanners (Step 5)
        'local_filesystem': ('filesystem_scanners.local_filesystem_scanner', 'LocalFilesystemScanner'),
        'network_share': ('filesystem_scanners.network_share_scanner', 'NetworkShareScanner'),
    }
    
    # Cache for loaded scanner classes
    _loaded_scanners: Dict[str, Type] = {}
    
    @classmethod
    def get_scanner_class(cls, scanner_type: str) -> Optional[Type]:
        """
        Get scanner class by type identifier with lazy loading.
        
        Args:
            scanner_type: Scanner type identifier (e.g., 'postgresql', 's3')
            
        Returns:
            Scanner class or None if not found/cannot load
        """
        # Check cache first
        if scanner_type in cls._loaded_scanners:
            return cls._loaded_scanners[scanner_type]
        
        # Check if scanner type is registered
        if scanner_type not in cls._SCANNER_MAPPINGS:
            logger.error(f"[ERROR] Unknown scanner type: {scanner_type}")
            return None
        
        # Lazy load the scanner class
        module_path, class_name = cls._SCANNER_MAPPINGS[scanner_type]
        
        try:
            # Flexible import: try package import first, then standalone
            try:
                # Package import (when used as part of microservice)
                module = __import__(
                    f'..{module_path}',
                    fromlist=[class_name],
                    level=1
                )
            except ImportError:
                # Standalone import (when running tests/scripts)
                module = __import__(
                    module_path,
                    fromlist=[class_name]
                )
            
            scanner_class = getattr(module, class_name)
            
            # Cache the loaded class
            cls._loaded_scanners[scanner_type] = scanner_class
            
            logger.info(f"[OK] Loaded scanner class: {scanner_type} -> {class_name}")
            return scanner_class
            
        except (ImportError, AttributeError) as e:
            logger.error(
                f"[ERROR] Failed to load scanner '{scanner_type}' "
                f"from {module_path}.{class_name}: {str(e)}"
            )
            return None
    
    @classmethod
    def list_available_scanners(cls) -> Dict[str, str]:
        """
        List all registered scanner types with descriptions.
        
        Returns:
            {scanner_type: description}
        """
        descriptions = {
            # Database scanners
            'postgresql': 'PostgreSQL database scanner',
            'mysql': 'MySQL database scanner',
            'mongodb': 'MongoDB database scanner',
            'mssql': 'Microsoft SQL Server scanner',
            
            # Cloud scanners
            's3': 'AWS S3 bucket scanner',
            'azure_blob': 'Azure Blob Storage scanner',
            'gcs': 'Google Cloud Storage scanner',
            
            # Filesystem scanners
            'local_filesystem': 'Local filesystem scanner',
            'network_share': 'Network share (UNC) scanner',
        }
        
        return descriptions
    
    @classmethod
    def get_scanner_category(cls, scanner_type: str) -> Optional[str]:
        """
        Get the category of a scanner type.
        
        Args:
            scanner_type: Scanner type identifier
            
        Returns:
            'database', 'cloud', 'filesystem', or None if unknown
        """
        database_scanners = ['postgresql', 'mysql', 'mongodb', 'mssql']
        cloud_scanners = ['s3', 'azure_blob', 'gcs']
        filesystem_scanners = ['local_filesystem', 'network_share']
        
        if scanner_type in database_scanners:
            return 'database'
        elif scanner_type in cloud_scanners:
            return 'cloud'
        elif scanner_type in filesystem_scanners:
            return 'filesystem'
        else:
            return None
    
    @classmethod
    def validate_scanner_type(cls, scanner_type: str) -> bool:
        """
        Validate if a scanner type is registered.
        
        Args:
            scanner_type: Scanner type to validate
            
        Returns:
            True if registered, False otherwise
        """
        return scanner_type in cls._SCANNER_MAPPINGS
    
    @classmethod
    def get_scanners_by_category(cls, category: str) -> list[str]:
        """
        Get all scanner types in a category.
        
        Args:
            category: 'database', 'cloud', or 'filesystem'
            
        Returns:
            List of scanner type identifiers
        """
        scanners = []
        for scanner_type in cls._SCANNER_MAPPINGS.keys():
            if cls.get_scanner_category(scanner_type) == category:
                scanners.append(scanner_type)
        return scanners
    
    @classmethod
    def clear_cache(cls):
        """Clear the loaded scanner class cache"""
        cls._loaded_scanners.clear()
        logger.info("[OK] Scanner registry cache cleared")
