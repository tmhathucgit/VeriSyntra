"""
EnhancedPatternDetector for Vietnamese PDPL compliance
Uses dynamic configuration from ScanConfig and VietnameseRegionalConfig
Zero hard-coding - all operational values from centralized config
"""
from typing import List, Dict, Any, Optional
import re
import logging

# Flexible import pattern for package and standalone execution
try:
    from ..config import ScanConfig, VietnameseRegionalConfig
except ImportError:
    from config.constants import ScanConfig, VietnameseRegionalConfig

logger = logging.getLogger(__name__)


class EnhancedPatternDetector:
    """Enhanced Vietnamese pattern detection with dynamic configuration"""
    
    # DOMAIN KNOWLEDGE - PDPL 2025 legal standard (acceptable as constant)
    # Source: Vietnamese PDPL 2025 personal data field definitions
    PDPL_FIELD_PATTERNS = {
        'ho_ten': r'^ho[_\s-]?ten$',
        'ten': r'^ten$',
        'ho': r'^ho$',
        'so_cmnd': r'^so[_\s-]?(cmnd|cccd)$',
        'so_dien_thoai': r'^(so[_\s-]?)?(dien[_\s-]?thoai|dt|phone)$',
        'dia_chi': r'^dia[_\s-]?chi$',
        'email': r'^email$',
        'ngay_sinh': r'^ngay[_\s-]?sinh$',
        'gioi_tinh': r'^gioi[_\s-]?tinh$',
        'so_tai_khoan': r'^so[_\s-]?tai[_\s-]?khoan$',
        'ma_so_thue': r'^ma[_\s-]?so[_\s-]?thue$',
        'dan_toc': r'^dan[_\s-]?toc$',
        'ton_giao': r'^ton[_\s-]?giao$',
        'quoc_tich': r'^quoc[_\s-]?tich$'
    }
    
    # DOMAIN KNOWLEDGE - Vietnamese telecom/government standards (acceptable as constant)
    DATA_PATTERNS = {
        'cmnd_cccd': re.compile(r'^\d{9,12}$'),  # Vietnamese ID card format
        'phone_vn_mobile': re.compile(r'^(84|0)(3|5|7|8|9)\d{8}$'),  # Vietnamese mobile
        'phone_vn_landline': re.compile(r'^(84|0)(2)\d{9}$'),  # Vietnamese landline
        'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        'tax_code': re.compile(r'^\d{10}(-\d{3})?$'),  # Vietnamese tax ID
        'bank_account': re.compile(r'^\d{10,16}$'),  # Vietnamese bank account
        'vietnamese_name': re.compile(
            r'^[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]'
            r'[a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+'
            r'(\s[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]'
            r'[a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+)+$'
        )
    }
    
    def __init__(
        self,
        confidence_threshold: float = ScanConfig.CONFIDENCE_THRESHOLD,  # Dynamic config
        min_unique_threshold: float = ScanConfig.MIN_UNIQUE_THRESHOLD,  # Dynamic config
        sample_size: int = ScanConfig.DEFAULT_SAMPLE_SIZE  # Dynamic config
    ):
        """
        Initialize detector with dynamic configuration
        
        Args:
            confidence_threshold: Minimum confidence for pattern match (from ScanConfig)
            min_unique_threshold: Minimum uniqueness ratio (from ScanConfig)
            sample_size: Default sample size (from ScanConfig)
        """
        self.confidence_threshold = confidence_threshold
        self.min_unique_threshold = min_unique_threshold
        self.sample_size = sample_size
    
    def detect_field_pattern(self, field_name: str) -> Optional[str]:
        """
        Detect Vietnamese PDPL field name pattern
        
        Args:
            field_name: Database column name (may be Vietnamese)
            
        Returns:
            Pattern type or None
        """
        field_lower = field_name.lower()
        
        for pattern_type, regex in self.PDPL_FIELD_PATTERNS.items():
            if re.match(regex, field_lower, re.IGNORECASE):
                logger.debug(f"[OK] Detected field pattern '{pattern_type}' for '{field_name}'")
                return pattern_type
        
        return None
    
    def detect_data_pattern(
        self,
        sample_values: List[str],
        max_samples: int = ScanConfig.DEFAULT_SAMPLE_SIZE  # Dynamic config
    ) -> Dict[str, float]:
        """
        Detect Vietnamese data patterns in sample values
        
        Args:
            sample_values: List of sample data
            max_samples: Maximum samples to analyze (from ScanConfig)
            
        Returns:
            {pattern_type: confidence_score}
        """
        if not sample_values:
            return {}
        
        # Use dynamic sample size
        samples = sample_values[:max_samples]
        pattern_scores = {}
        
        for pattern_type, regex in self.DATA_PATTERNS.items():
            matches = sum(
                1 for val in samples
                if isinstance(val, str) and regex.match(val)
            )
            
            if matches > 0:
                confidence = matches / len(samples)
                # Use dynamic confidence threshold
                if confidence >= self.confidence_threshold:
                    pattern_scores[pattern_type] = confidence
        
        logger.info(
            f"[OK] Detected {len(pattern_scores)} patterns with confidence >= "
            f"{self.confidence_threshold} (sample size: {len(samples)})"
        )
        
        return pattern_scores
    
    def detect_with_regional_context(
        self,
        samples: List[str],
        region: str = 'central'
    ) -> Dict[str, Any]:
        """
        Detect patterns with Vietnamese regional business context
        
        Args:
            samples: Sample data values
            region: Vietnamese region ('north', 'south', 'central')
            
        Returns:
            {
                'patterns': Dict[str, float],
                'region': str,
                'confidence_threshold': float,
                'sample_size': int
            }
        """
        # CORRECT: Use regional config, not hard-coded values
        if region == 'north':
            confidence = VietnameseRegionalConfig.NORTH_CONFIDENCE_THRESHOLD
            sample_count = VietnameseRegionalConfig.NORTH_SAMPLE_SIZE
        elif region == 'south':
            confidence = VietnameseRegionalConfig.SOUTH_CONFIDENCE_THRESHOLD
            sample_count = VietnameseRegionalConfig.SOUTH_SAMPLE_SIZE
        else:
            confidence = VietnameseRegionalConfig.CENTRAL_CONFIDENCE_THRESHOLD
            sample_count = VietnameseRegionalConfig.CENTRAL_SAMPLE_SIZE
        
        # Use dynamic values throughout
        working_samples = samples[:sample_count]
        
        # Temporarily adjust confidence threshold for regional context
        original_threshold = self.confidence_threshold
        self.confidence_threshold = confidence
        
        patterns = self.detect_data_pattern(working_samples, max_samples=sample_count)
        
        # Restore original threshold
        self.confidence_threshold = original_threshold
        
        result = {
            'patterns': patterns,
            'region': region,
            'confidence_threshold': confidence,
            'sample_size': len(working_samples)
        }
        
        logger.info(
            f"[OK] Regional detection ({region}): {len(patterns)} patterns found "
            f"(confidence: {confidence}, samples: {len(working_samples)})"
        )
        
        return result
    
    def is_pdpl_sensitive_field(self, field_name: str) -> bool:
        """
        Check if field name matches PDPL sensitive data patterns
        
        Args:
            field_name: Database column name
            
        Returns:
            True if matches PDPL sensitive field pattern
        """
        pattern = self.detect_field_pattern(field_name)
        return pattern is not None
    
    def analyze_column(
        self,
        column_name: str,
        sample_values: List[str]
    ) -> Dict[str, Any]:
        """
        Comprehensive column analysis for PDPL compliance
        
        Args:
            column_name: Database column name
            sample_values: Sample data values
            
        Returns:
            {
                'column_name': str,
                'field_pattern': Optional[str],
                'data_patterns': Dict[str, float],
                'is_pdpl_sensitive': bool,
                'confidence_threshold': float,
                'sample_count': int
            }
        """
        field_pattern = self.detect_field_pattern(column_name)
        data_patterns = self.detect_data_pattern(sample_values)
        
        result = {
            'column_name': column_name,
            'field_pattern': field_pattern,
            'data_patterns': data_patterns,
            'is_pdpl_sensitive': field_pattern is not None or len(data_patterns) > 0,
            'confidence_threshold': self.confidence_threshold,
            'sample_count': min(len(sample_values), self.sample_size)
        }
        
        return result
    
    @classmethod
    def get_pdpl_field_types(cls) -> List[str]:
        """
        Get list of all PDPL sensitive field types
        
        Returns:
            List of PDPL field pattern types
        """
        return list(cls.PDPL_FIELD_PATTERNS.keys())
    
    @classmethod
    def get_data_pattern_types(cls) -> List[str]:
        """
        Get list of all data pattern types
        
        Returns:
            List of data pattern types
        """
        return list(cls.DATA_PATTERNS.keys())
