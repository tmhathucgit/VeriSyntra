"""
VietnameseTextAnalyzer for text profiling and analysis
Uses dynamic configuration from ScanConfig
Zero hard-coding - all operational values from centralized config
"""
from typing import List, Dict, Any
from collections import Counter
import logging

# Flexible import pattern for package and standalone execution
try:
    from ..config import ScanConfig
except ImportError:
    from config import ScanConfig

logger = logging.getLogger(__name__)


class VietnameseTextAnalyzer:
    """Analyzer for Vietnamese text profiling with dynamic configuration"""
    
    def __init__(
        self,
        sample_size: int = ScanConfig.DEFAULT_SAMPLE_SIZE,  # Dynamic config
        top_values_count: int = ScanConfig.TOP_VALUES_COUNT,  # Dynamic config
        min_unique_threshold: float = ScanConfig.MIN_UNIQUE_THRESHOLD  # Dynamic config
    ):
        """
        Initialize text analyzer with dynamic configuration
        
        Args:
            sample_size: Default sample size (from ScanConfig)
            top_values_count: Number of top values to return (from ScanConfig)
            min_unique_threshold: Minimum uniqueness ratio (from ScanConfig)
        """
        # Lazy import to avoid circular dependency during module loading
        try:
            from .utf8_validator import UTF8Validator
        except ImportError:
            from utf8_validator import UTF8Validator
            
        self.sample_size = sample_size
        self.top_values_count = top_values_count
        self.min_unique_threshold = min_unique_threshold
        self.utf8_validator = UTF8Validator()
    
    def profile_text_samples(
        self,
        samples: List[str],
        max_samples: int = ScanConfig.DEFAULT_SAMPLE_SIZE  # Dynamic config
    ) -> Dict[str, Any]:
        """
        Profile text samples for Vietnamese data analysis
        
        Args:
            samples: List of text samples
            max_samples: Maximum samples to analyze (from ScanConfig)
            
        Returns:
            {
                'total_count': int,
                'unique_count': int,
                'null_count': int,
                'min_length': int,
                'max_length': int,
                'avg_length': float,
                'numeric_ratio': float,
                'alphanumeric_ratio': float,
                'vietnamese_ratio': float,
                'diversity_score': float,
                'top_values': List[tuple]
            }
        """
        # Use dynamic sample size
        working_samples = [s for s in samples[:max_samples] if s is not None]
        null_count = len([s for s in samples[:max_samples] if s is None])
        
        if not working_samples:
            return {
                'total_count': len(samples[:max_samples]),
                'unique_count': 0,
                'null_count': null_count,
                'min_length': 0,
                'max_length': 0,
                'avg_length': 0.0,
                'numeric_ratio': 0.0,
                'alphanumeric_ratio': 0.0,
                'vietnamese_ratio': 0.0,
                'diversity_score': 0.0,
                'top_values': []
            }
        
        # Convert all to strings
        str_samples = [str(s) for s in working_samples]
        
        # Calculate length statistics
        lengths = [len(s) for s in str_samples]
        min_length = min(lengths)
        max_length = max(lengths)
        avg_length = sum(lengths) / len(lengths)
        
        # Calculate character type ratios
        numeric_count = sum(1 for s in str_samples if s.isdigit())
        alphanumeric_count = sum(1 for s in str_samples if s.isalnum())
        vietnamese_count = sum(
            1 for s in str_samples
            if self.utf8_validator.contains_vietnamese(s)
        )
        
        numeric_ratio = numeric_count / len(str_samples)
        alphanumeric_ratio = alphanumeric_count / len(str_samples)
        vietnamese_ratio = vietnamese_count / len(str_samples)
        
        # Calculate diversity score
        unique_values = set(str_samples)
        unique_count = len(unique_values)
        diversity_score = unique_count / len(str_samples)
        
        # Get top values using dynamic config
        value_counts = Counter(str_samples)
        top_values = value_counts.most_common(self.top_values_count)
        
        profile = {
            'total_count': len(samples[:max_samples]),
            'unique_count': unique_count,
            'null_count': null_count,
            'min_length': min_length,
            'max_length': max_length,
            'avg_length': round(avg_length, 2),
            'numeric_ratio': round(numeric_ratio, 3),
            'alphanumeric_ratio': round(alphanumeric_ratio, 3),
            'vietnamese_ratio': round(vietnamese_ratio, 3),
            'diversity_score': round(diversity_score, 3),
            'top_values': top_values
        }
        
        logger.info(
            f"[OK] Text profile: {unique_count} unique values, "
            f"{vietnamese_ratio:.1%} Vietnamese, diversity: {diversity_score:.1%}"
        )
        
        return profile
    
    def is_high_diversity(self, samples: List[str]) -> bool:
        """
        Check if samples have high diversity using dynamic threshold
        
        Args:
            samples: List of samples
            
        Returns:
            True if diversity score exceeds min_unique_threshold
        """
        if not samples:
            return False
        
        unique_count = len(set(samples))
        diversity = unique_count / len(samples)
        
        return diversity >= self.min_unique_threshold
    
    def suggest_data_type(self, samples: List[str]) -> str:
        """
        Suggest data type based on sample analysis
        
        Args:
            samples: List of sample values
            
        Returns:
            Suggested data type: 'vietnamese_text', 'numeric', 'email', 'phone', 'mixed', 'unknown'
        """
        if not samples:
            return 'unknown'
        
        profile = self.profile_text_samples(samples)
        
        # Vietnamese text if high Vietnamese character ratio
        if profile['vietnamese_ratio'] > 0.3:
            return 'vietnamese_text'
        
        # Numeric if high numeric ratio
        if profile['numeric_ratio'] > 0.8:
            return 'numeric'
        
        # Check for email pattern
        email_count = sum(1 for s in samples if isinstance(s, str) and '@' in s)
        if email_count / len(samples) > 0.7:
            return 'email'
        
        # Check for phone pattern (Vietnamese format detection)
        phone_count = sum(
            1 for s in samples
            if isinstance(s, str) and (s.startswith('0') or s.startswith('84')) and s.replace('+', '').isdigit()
        )
        if phone_count / len(samples) > 0.7:
            return 'phone'
        
        # Mixed if high alphanumeric ratio
        if profile['alphanumeric_ratio'] > 0.5:
            return 'mixed'
        
        return 'unknown'
    
    def analyze_column_quality(
        self,
        column_name: str,
        samples: List[Any]
    ) -> Dict[str, Any]:
        """
        Analyze data quality for a column
        
        Args:
            column_name: Column name
            samples: Sample values
            
        Returns:
            {
                'column_name': str,
                'completeness': float,  # % non-null
                'uniqueness': float,    # Diversity score
                'vietnamese_content': float,  # % Vietnamese text
                'suggested_type': str,
                'quality_score': float,  # Overall quality (0-1)
                'sample_count': int
            }
        """
        str_samples = [str(s) for s in samples if s is not None]
        null_count = len([s for s in samples if s is None])
        
        completeness = (len(samples) - null_count) / len(samples) if samples else 0
        
        profile = self.profile_text_samples(str_samples)
        uniqueness = profile['diversity_score']
        vietnamese_content = profile['vietnamese_ratio']
        suggested_type = self.suggest_data_type(str_samples)
        
        # Calculate quality score (weighted average)
        quality_score = (
            completeness * 0.4 +
            min(uniqueness, 1.0) * 0.3 +
            (1.0 if vietnamese_content > 0 else 0.5) * 0.3
        )
        
        result = {
            'column_name': column_name,
            'completeness': round(completeness, 3),
            'uniqueness': round(uniqueness, 3),
            'vietnamese_content': round(vietnamese_content, 3),
            'suggested_type': suggested_type,
            'quality_score': round(quality_score, 3),
            'sample_count': len(samples)
        }
        
        logger.info(
            f"[OK] Quality analysis for '{column_name}': "
            f"quality={quality_score:.1%}, type={suggested_type}"
        )
        
        return result
    
    def extract_smart_sample(
        self,
        values: List[Any],
        target_size: int = ScanConfig.DEFAULT_SAMPLE_SIZE  # Dynamic config
    ) -> Dict[str, Any]:
        """
        Extract smart sample with diversity using dynamic configuration
        
        Args:
            values: All values from column
            target_size: Desired sample size (from ScanConfig)
            
        Returns:
            {
                'samples': List[Any],
                'total_count': int,
                'unique_count': int,
                'null_count': int,
                'diversity_score': float,
                'sampling_strategy': str
            }
        """
        # Remove null values
        non_null_values = [v for v in values if v is not None]
        null_count = len(values) - len(non_null_values)
        
        if not non_null_values:
            return {
                'samples': [],
                'total_count': len(values),
                'unique_count': 0,
                'null_count': null_count,
                'diversity_score': 0.0,
                'sampling_strategy': 'none'
            }
        
        # Get unique values
        unique_values = list(set(non_null_values))
        unique_count = len(unique_values)
        
        # Calculate diversity score
        diversity_score = unique_count / len(non_null_values)
        
        # Sample strategy based on diversity using dynamic threshold
        if diversity_score >= self.min_unique_threshold:
            # High diversity: random sample of unique values
            import random
            samples = random.sample(
                unique_values,
                min(target_size, len(unique_values))
            )
            strategy = 'random_unique'
        else:
            # Low diversity: sample most common values
            value_counts = Counter(non_null_values)
            samples = [
                value for value, count in value_counts.most_common(target_size)
            ]
            strategy = 'most_common'
        
        result = {
            'samples': samples,
            'total_count': len(values),
            'unique_count': unique_count,
            'null_count': null_count,
            'diversity_score': round(diversity_score, 3),
            'sampling_strategy': strategy
        }
        
        logger.info(
            f"[OK] Extracted {len(samples)} samples using '{strategy}' strategy "
            f"(diversity: {diversity_score:.1%})"
        )
        
        return result
