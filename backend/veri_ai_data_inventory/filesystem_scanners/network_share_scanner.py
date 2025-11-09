"""
NetworkShareScanner for Windows/SMB network share scanning
Uses dynamic configuration from FilesystemConfig
Zero hard-coding - all operational values from centralized config
Vietnamese UTF-8 filename support
"""
from typing import Dict, Any, List, Optional
from pathlib import Path, WindowsPath
from datetime import datetime
import os
import logging

# Flexible import pattern for package and standalone execution
try:
    from ..config import FilesystemConfig, EncodingConfig, ScanConfig
    from ..utils import UTF8Validator
except ImportError:
    from config import FilesystemConfig, EncodingConfig, ScanConfig
    from utils import UTF8Validator

logger = logging.getLogger(__name__)


class NetworkShareScanner:
    """Network share scanner with Vietnamese filename support and dynamic configuration"""
    
    def __init__(self, connection_config: Dict[str, Any]):
        """
        Initialize network share scanner with dynamic configuration
        
        Args:
            connection_config: {
                'share_path': str,  # UNC path (e.g., '\\\\server\\share')
                'username': str (optional),
                'password': str (optional),
                'domain': str (optional)
            }
        """
        self.config = connection_config
        self.share_path = Path(connection_config['share_path'])
        self.utf8_validator = UTF8Validator()
        self.connected = False
        
        # Set UTF-8 encoding for filesystem operations using dynamic config
        os.environ['PYTHONIOENCODING'] = EncodingConfig.PYTHON_IO_ENCODING
    
    def connect(self) -> bool:
        """
        Connect to network share and validate accessibility
        
        Returns:
            True if share is accessible, False otherwise
        """
        try:
            # For Windows UNC paths, we don't need explicit connection
            # The OS handles authentication through Windows credentials
            # or explicit credentials if provided
            
            if not self.share_path.exists():
                logger.error(f"[ERROR] Network share does not exist or is not accessible: {self.share_path}")
                return False
            
            if not self.share_path.is_dir():
                logger.error(f"[ERROR] Network share path is not a directory: {self.share_path}")
                return False
            
            self.connected = True
            logger.info(f"[OK] Connected to network share: {self.share_path}")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Network share connection failed: {str(e)}")
            return False
    
    def discover_files(
        self,
        max_depth: int = None,  # Uses FilesystemConfig.DEFAULT_MAX_DEPTH if None
        max_files: int = None,  # Uses FilesystemConfig.DEFAULT_MAX_FILES if None
        min_file_size: int = None,  # Uses FilesystemConfig.DEFAULT_MIN_FILE_SIZE if None
        follow_symlinks: bool = None,  # Uses FilesystemConfig.DEFAULT_FOLLOW_SYMLINKS if None
        file_extensions: List[str] = None  # Optional filter
    ) -> Dict[str, Any]:
        """
        Discover files on network share with Vietnamese filename support
        
        Args:
            max_depth: Maximum directory depth (uses FilesystemConfig.DEFAULT_MAX_DEPTH if None)
            max_files: Maximum files to discover (uses FilesystemConfig.DEFAULT_MAX_FILES if None)
            min_file_size: Minimum file size in bytes (uses FilesystemConfig.DEFAULT_MIN_FILE_SIZE if None)
            follow_symlinks: Follow symbolic links (uses FilesystemConfig.DEFAULT_FOLLOW_SYMLINKS if None)
            file_extensions: Filter by extensions (e.g., ['.pdf', '.docx'])
            
        Returns:
            {
                'files': [
                    {
                        'path': str,  # Full UNC path (UTF-8 Vietnamese filenames)
                        'name': str,  # Filename
                        'size': int,
                        'created': datetime,
                        'modified': datetime,
                        'extension': str,
                        'is_vietnamese_filename': bool
                    }
                ],
                'total_size': int,
                'total_count': int,
                'vietnamese_filename_count': int
            }
        """
        if not self.connected:
            raise RuntimeError("Network share not connected. Call connect() first.")
        
        # Use dynamic config for defaults
        if max_depth is None:
            max_depth = FilesystemConfig.DEFAULT_MAX_DEPTH
        if max_files is None:
            max_files = FilesystemConfig.DEFAULT_MAX_FILES
        if min_file_size is None:
            min_file_size = FilesystemConfig.DEFAULT_MIN_FILE_SIZE
        if follow_symlinks is None:
            follow_symlinks = FilesystemConfig.DEFAULT_FOLLOW_SYMLINKS
        
        files_info = {
            'files': [],
            'total_size': 0,
            'total_count': 0,
            'vietnamese_filename_count': 0
        }
        
        try:
            for root, dirs, files in os.walk(
                self.share_path,
                followlinks=follow_symlinks
            ):
                # Stop if max files reached
                if files_info['total_count'] >= max_files:
                    break
                
                # Calculate depth
                try:
                    depth = len(Path(root).relative_to(self.share_path).parts)
                except ValueError:
                    depth = 0
                
                if depth > max_depth:
                    continue
                
                for filename in files:
                    # Stop if max files reached
                    if files_info['total_count'] >= max_files:
                        break
                    
                    file_path = Path(root) / filename
                    
                    # Validate UTF-8 in filename
                    validation = self.utf8_validator.validate(filename)
                    if not validation['is_valid']:
                        logger.warning(f"[WARNING] Invalid UTF-8 in filename: {filename}")
                        continue
                    
                    # Check for Vietnamese characters
                    is_vietnamese = validation['has_vietnamese']
                    if is_vietnamese:
                        files_info['vietnamese_filename_count'] += 1
                    
                    # Get file stats
                    try:
                        stat = file_path.stat()
                        file_size = stat.st_size
                        
                        # Filter by size
                        if file_size < min_file_size:
                            continue
                        
                        # Get extension
                        extension = file_path.suffix.lower()
                        
                        # Filter by extension
                        if file_extensions and extension not in file_extensions:
                            continue
                        
                        # Skip excluded extensions from config
                        if extension in FilesystemConfig.EXCLUDED_EXTENSIONS:
                            continue
                        
                        files_info['files'].append({
                            'path': str(file_path),
                            'name': filename,
                            'size': file_size,
                            'created': datetime.fromtimestamp(stat.st_ctime),
                            'modified': datetime.fromtimestamp(stat.st_mtime),
                            'extension': extension,
                            'is_vietnamese_filename': is_vietnamese
                        })
                        
                        files_info['total_size'] += file_size
                        files_info['total_count'] += 1
                        
                    except (OSError, PermissionError) as e:
                        logger.warning(f"[WARNING] Cannot access {file_path}: {str(e)}")
                        continue
            
            logger.info(
                f"[OK] Discovered {files_info['total_count']} files on network share "
                f"({files_info['total_size'] / (1024**2):.2f} MB), "
                f"{files_info['vietnamese_filename_count']} with Vietnamese names"
            )
            
            return files_info
            
        except Exception as e:
            logger.error(f"[ERROR] Network share discovery failed: {str(e)}")
            raise
    
    def read_sample_content(
        self,
        file_path: str,
        max_bytes: int = None  # Uses ScanConfig.DEFAULT_SAMPLE_SIZE * 100 if None
    ) -> Optional[bytes]:
        """
        Read first N bytes of file from network share for content sampling
        
        Args:
            file_path: Full UNC path to file
            max_bytes: Maximum bytes to read (uses ScanConfig.DEFAULT_SAMPLE_SIZE * 100 if None)
            
        Returns:
            First N bytes of file content
        """
        if not self.connected:
            raise RuntimeError("Network share not connected. Call connect() first.")
        
        # Use dynamic config for max_bytes default
        if max_bytes is None:
            max_bytes = ScanConfig.DEFAULT_SAMPLE_SIZE * 100  # 10KB for text files
        
        path = Path(file_path)
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(path.name)
        if not validation['is_valid']:
            logger.error(f"[ERROR] Invalid UTF-8 in filename: {path.name}")
            return None
        
        try:
            with open(path, 'rb') as f:
                content = f.read(max_bytes)
            
            logger.info(
                f"[OK] Read {len(content)} bytes from network share file {path.name} "
                f"(Vietnamese: {validation['has_vietnamese']})"
            )
            
            return content
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to read {file_path}: {str(e)}")
            return None
    
    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Get file metadata from network share with Vietnamese filename validation
        
        Args:
            file_path: Full UNC path to file
            
        Returns:
            File metadata dictionary with UTF-8 validation
        """
        if not self.connected:
            raise RuntimeError("Network share not connected. Call connect() first.")
        
        path = Path(file_path)
        
        # Validate Vietnamese filename
        validation = self.utf8_validator.validate(path.name)
        if not validation['is_valid']:
            raise ValueError(f"Invalid UTF-8 in filename: {path.name}")
        
        try:
            stat = path.stat()
            
            metadata = {
                'path': str(path),
                'name': path.name,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'extension': path.suffix.lower(),
                'has_vietnamese_filename': validation['has_vietnamese'],
                'vietnamese_char_count': validation['vietnamese_char_count']
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to get metadata for {file_path}: {str(e)}")
            raise
    
    def close(self):
        """Close network share connection and cleanup resources"""
        # No persistent connections for Windows UNC paths
        self.connected = False
        logger.info("[OK] Network share scanner closed")
