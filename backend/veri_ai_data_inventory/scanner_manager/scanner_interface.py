"""
VeriSyntra Scanner Interface Protocol

Defines the standard interface that all scanners must implement.
This ensures consistent behavior across database, cloud, and filesystem scanners.
"""

from typing import Protocol, Dict, Any, Optional


class ScannerInterface(Protocol):
    """
    Protocol defining the standard interface for all VeriSyntra scanners.
    
    All scanner implementations (database, cloud, filesystem) must implement
    these methods to ensure consistent lifecycle management and error handling.
    """
    
    def connect(self) -> Dict[str, Any]:
        """
        Establish connection to the data source.
        
        Returns:
            {
                'status': 'success' | 'error',
                'message': str,
                'connection_info': dict (optional)
            }
        """
        ...
    
    def discover(self, **kwargs) -> Dict[str, Any]:
        """
        Discover data assets in the connected source.
        
        For databases: Discover tables and columns
        For cloud storage: Discover objects/blobs/files
        For filesystems: Discover files and directories
        
        Args:
            **kwargs: Scanner-specific discovery parameters
            
        Returns:
            {
                'status': 'success' | 'error',
                'message': str,
                'data': dict,  # Scanner-specific discovery results
                'count': int,  # Number of items discovered
                'metadata': dict (optional)
            }
        """
        ...
    
    def get_metadata(self, resource_id: str) -> Dict[str, Any]:
        """
        Get detailed metadata for a specific resource.
        
        Args:
            resource_id: Identifier for the resource
                         (table name, object key, file path, etc.)
        
        Returns:
            {
                'status': 'success' | 'error',
                'message': str,
                'metadata': dict
            }
        """
        ...
    
    def close(self) -> None:
        """
        Close connection and cleanup resources.
        
        Should handle cleanup gracefully even if connection was never established.
        """
        ...


class BaseScannerAdapter:
    """
    Base adapter to help existing scanners conform to ScannerInterface.
    
    Existing scanners from Steps 2, 4, 5 can use this adapter to ensure
    they return consistent response formats.
    """
    
    @staticmethod
    def create_success_response(
        message: str,
        data: Any = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create standardized success response"""
        response = {
            'status': 'success',
            'message': message
        }
        if data is not None:
            response['data'] = data
        response.update(kwargs)
        return response
    
    @staticmethod
    def create_error_response(
        message: str,
        error_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create standardized error response"""
        response = {
            'status': 'error',
            'message': message
        }
        if error_details:
            response['error_details'] = error_details
        return response
    
    @staticmethod
    def normalize_connection_response(connected: bool, details: str = '') -> Dict[str, Any]:
        """
        Normalize connection responses from existing scanners.
        
        Args:
            connected: Whether connection succeeded
            details: Connection details or error message
            
        Returns:
            Standardized connection response
        """
        if connected:
            return BaseScannerAdapter.create_success_response(
                message='Connected successfully',
                connection_info={'details': details}
            )
        else:
            return BaseScannerAdapter.create_error_response(
                message='Connection failed',
                error_details={'details': details}
            )
