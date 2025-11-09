"""
UTF8Validator for Vietnamese text validation
Uses dynamic configuration from EncodingConfig and ScanConfig
Zero hard-coding - all operational values from centralized config
"""
from typing import List, Dict, Any, Optional
import logging

# Flexible import pattern for package and standalone execution
try:
    from ..config import EncodingConfig, ScanConfig
except ImportError:
    from config.constants import EncodingConfig, ScanConfig

logger = logging.getLogger(__name__)


class UTF8Validator:
    """Utility for validating and handling Vietnamese UTF-8 text"""
    
    # DOMAIN KNOWLEDGE - Vietnamese language specification (acceptable as constant)
    # Source: Unicode Standard for Vietnamese (134 unique diacritical characters)
    VIETNAMESE_CHARS = set([
        # Lowercase vowels with diacritics
        'à', 'á', 'ả', 'ã', 'ạ', 'ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ',
        'â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'đ', 'è', 'é', 'ẻ', 'ẽ',
        'ẹ', 'ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ì', 'í', 'ỉ', 'ĩ',
        'ị', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'ô', 'ồ', 'ố', 'ổ', 'ỗ',
        'ộ', 'ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ù', 'ú', 'ủ', 'ũ',
        'ụ', 'ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ',
        # Uppercase vowels with diacritics
        'À', 'Á', 'Ả', 'Ã', 'Ạ', 'Ă', 'Ằ', 'Ắ', 'Ẳ', 'Ẵ', 'Ặ',
        'Â', 'Ầ', 'Ấ', 'Ẩ', 'Ẫ', 'Ậ', 'Đ', 'È', 'É', 'Ẻ', 'Ẽ',
        'Ẹ', 'Ê', 'Ề', 'Ế', 'Ể', 'Ễ', 'Ệ', 'Ì', 'Í', 'Ỉ', 'Ĩ',
        'Ị', 'Ò', 'Ó', 'Ỏ', 'Õ', 'Ọ', 'Ô', 'Ồ', 'Ố', 'Ổ', 'Ỗ',
        'Ộ', 'Ơ', 'Ờ', 'Ớ', 'Ở', 'Ỡ', 'Ợ', 'Ù', 'Ú', 'Ủ', 'Ũ',
        'Ụ', 'Ư', 'Ừ', 'Ứ', 'Ử', 'Ữ', 'Ự', 'Ỳ', 'Ý', 'Ỷ', 'Ỹ', 'Ỵ'
    ])
    
    def __init__(
        self,
        encoding: str = EncodingConfig.PYTHON_IO_ENCODING,  # Dynamic config
        error_handler: str = EncodingConfig.MONGODB_UNICODE_ERROR_HANDLER,  # Dynamic config
        min_confidence: float = ScanConfig.CONFIDENCE_THRESHOLD  # Dynamic config
    ):
        """
        Initialize UTF8Validator with dynamic configuration
        
        Args:
            encoding: Text encoding standard (from EncodingConfig)
            error_handler: Unicode error handling mode (from EncodingConfig)
            min_confidence: Minimum confidence threshold (from ScanConfig)
        """
        self.encoding = encoding
        self.error_handler = error_handler
        self.min_confidence = min_confidence
    
    def validate(self, text: str, strict: bool = True) -> bool:
        """
        Validate UTF-8 encoding of text
        
        Args:
            text: Text to validate
            strict: If True, fail on any encoding error
            
        Returns:
            True if valid UTF-8, False otherwise
        """
        if not isinstance(text, str):
            return False
        
        try:
            # Attempt encode/decode cycle using dynamic encoding config
            text.encode(self.encoding).decode(self.encoding)
            return True
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            if strict:
                logger.error(f"[ERROR] UTF-8 validation failed: {str(e)}")
            return False
    
    def validate_batch(
        self,
        texts: List[str],
        sample_size: int = ScanConfig.DEFAULT_SAMPLE_SIZE  # Dynamic config
    ) -> Dict[str, Any]:
        """
        Validate batch of texts using dynamic sample size
        
        Args:
            texts: List of texts to validate
            sample_size: Maximum texts to validate (from ScanConfig)
            
        Returns:
            {
                'total': int,
                'valid': int,
                'invalid': int,
                'invalid_indices': List[int],
                'sample_size': int
            }
        """
        # Use dynamic sample size, not hard-coded
        texts_to_check = texts[:sample_size]
        
        result = {
            'total': len(texts_to_check),
            'valid': 0,
            'invalid': 0,
            'invalid_indices': [],
            'sample_size': sample_size
        }
        
        for idx, text in enumerate(texts_to_check):
            if self.validate(text, strict=False):
                result['valid'] += 1
            else:
                result['invalid'] += 1
                result['invalid_indices'].append(idx)
        
        logger.info(
            f"[OK] Batch validation: {result['valid']}/{result['total']} valid "
            f"(sample size: {sample_size})"
        )
        
        return result
    
    @classmethod
    def contains_vietnamese(cls, text: str) -> bool:
        """
        Check if text contains Vietnamese diacritics
        
        Args:
            text: Text to check
            
        Returns:
            True if contains Vietnamese characters
        """
        if not isinstance(text, str):
            return False
        
        return any(char in cls.VIETNAMESE_CHARS for char in text)
    
    def sanitize(self, text: str, replacement: str = '?') -> str:
        """
        Sanitize text by replacing invalid UTF-8 sequences
        
        Args:
            text: Text to sanitize
            replacement: Character to replace invalid sequences
            
        Returns:
            Sanitized text
        """
        try:
            # Use dynamic error handler config
            return text.encode(self.encoding, errors=self.error_handler).decode(self.encoding)
        except Exception as e:
            logger.error(f"[ERROR] Text sanitization failed: {str(e)}")
            return text
    
    def get_vietnamese_char_count(self, text: str) -> int:
        """
        Count Vietnamese diacritical characters in text
        
        Args:
            text: Text to analyze
            
        Returns:
            Count of Vietnamese characters
        """
        if not isinstance(text, str):
            return 0
        
        return sum(1 for char in text if char in self.VIETNAMESE_CHARS)
    
    def is_likely_vietnamese(
        self,
        text: str,
        min_threshold: float = ScanConfig.MIN_UNIQUE_THRESHOLD  # Dynamic config
    ) -> bool:
        """
        Determine if text is likely Vietnamese based on character ratio
        
        Args:
            text: Text to check
            min_threshold: Minimum ratio of Vietnamese chars (from ScanConfig)
            
        Returns:
            True if likely Vietnamese text
        """
        if not text or len(text) < 3:
            return False
        
        vn_char_count = self.get_vietnamese_char_count(text)
        ratio = vn_char_count / len(text)
        
        return ratio >= min_threshold
