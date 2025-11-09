"""
VeriSyntra Error Handler

Provides retry logic and error handling for scanner operations.
Uses dynamic configuration for retry attempts and delays.
"""

import time
import logging
from typing import Callable, Any, Dict, Optional
from functools import wraps

# Flexible import pattern
try:
    from ..config import ScanManagerConfig
except ImportError:
    from config.constants import ScanManagerConfig

logger = logging.getLogger(__name__)


class ScanErrorHandler:
    """
    Error handler with retry logic for scanner operations.
    
    Uses dynamic configuration from ScanManagerConfig for all retry parameters.
    """
    
    def __init__(
        self,
        max_retries: int = ScanManagerConfig.DEFAULT_RETRY_ATTEMPTS,
        retry_delay: int = ScanManagerConfig.RETRY_DELAY_SECONDS
    ):
        """
        Initialize error handler with dynamic configuration.
        
        Args:
            max_retries: Maximum retry attempts (default from ScanManagerConfig)
            retry_delay: Delay between retries in seconds (default from ScanManagerConfig)
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.error_log: list[Dict[str, Any]] = []
    
    def retry_on_failure(
        self,
        operation: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute operation with retry logic.
        
        Args:
            operation: Function to execute
            *args: Positional arguments for operation
            **kwargs: Keyword arguments for operation
            
        Returns:
            Operation result or error response
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                logger.info(
                    f"[INFO] Executing operation (attempt {attempt + 1}/{self.max_retries})"
                )
                
                result = operation(*args, **kwargs)
                
                # Success
                if attempt > 0:
                    logger.info(
                        f"[OK] Operation succeeded after {attempt + 1} attempts"
                    )
                
                return result
                
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # Log the error
                error_entry = {
                    'attempt': attempt + 1,
                    'error': error_msg,
                    'timestamp': time.time()
                }
                self.error_log.append(error_entry)
                
                logger.warning(
                    f"[WARNING] Operation failed (attempt {attempt + 1}/{self.max_retries}): "
                    f"{error_msg}"
                )
                
                # Don't sleep on the last attempt
                if attempt < self.max_retries - 1:
                    logger.info(f"[INFO] Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
        
        # All retries exhausted
        logger.error(
            f"[ERROR] Operation failed after {self.max_retries} attempts. "
            f"Last error: {str(last_error)}"
        )
        
        return {
            'status': 'error',
            'message': f'Operation failed after {self.max_retries} attempts',
            'last_error': str(last_error),
            'error_history': self.error_log
        }
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get summary of all errors encountered.
        
        Returns:
            Error summary statistics
        """
        return {
            'total_errors': len(self.error_log),
            'errors': self.error_log
        }
    
    def clear_error_log(self):
        """Clear the error log"""
        self.error_log.clear()
    
    @staticmethod
    def is_retryable_error(error: Exception) -> bool:
        """
        Determine if an error is retryable.
        
        Args:
            error: Exception to check
            
        Returns:
            True if error should trigger retry, False otherwise
        """
        # Network/connection errors are retryable
        retryable_error_types = [
            'ConnectionError',
            'TimeoutError',
            'ConnectionRefusedError',
            'ConnectionResetError',
        ]
        
        error_type = type(error).__name__
        return error_type in retryable_error_types
    
    @staticmethod
    def create_error_response(
        message: str,
        error: Optional[Exception] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create standardized error response.
        
        Args:
            message: Error message
            error: Original exception (optional)
            **kwargs: Additional error details
            
        Returns:
            Standardized error response dictionary
        """
        response = {
            'status': 'error',
            'message': message
        }
        
        if error:
            response['error_type'] = type(error).__name__
            response['error_details'] = str(error)
        
        response.update(kwargs)
        return response


def with_retry(max_retries: int = ScanManagerConfig.DEFAULT_RETRY_ATTEMPTS):
    """
    Decorator for adding retry logic to scanner methods.
    
    Args:
        max_retries: Maximum retry attempts (default from ScanManagerConfig)
        
    Usage:
        @with_retry(max_retries=3)
        def my_scanner_method(self):
            # Method implementation
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            error_handler = ScanErrorHandler(max_retries=max_retries)
            return error_handler.retry_on_failure(func, *args, **kwargs)
        return wrapper
    return decorator
