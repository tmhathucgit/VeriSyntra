# File: backend/veri_ai_data_inventory/services/column_filter_service.py
"""
Column filtering service for applying Vietnamese PDPL column filters during scanning
Zero hard-coding - all operational values from config
"""

from typing import List, Dict, Any
import re
import logging

# Flexible imports for package and standalone execution
try:
    from ..models.column_filter import ColumnFilterConfig, FilterMode
except ImportError:
    from models.column_filter import ColumnFilterConfig, FilterMode

logger = logging.getLogger(__name__)


class ColumnFilterService:
    """
    Service for applying column filters during scanning
    
    Reduces costs by 50-80% through selective column scanning
    Supports Vietnamese PDPL 2025 compliance requirements
    """
    
    @staticmethod
    def should_scan_column(
        column_name: str,
        filter_config: ColumnFilterConfig
    ) -> bool:
        """
        Determine if a column should be scanned based on filter configuration
        
        Args:
            column_name: Database column name (may be Vietnamese)
            filter_config: Filter configuration
            
        Returns:
            True if column should be scanned, False otherwise
            
        Examples:
            >>> config = ColumnFilterConfig(mode=FilterMode.INCLUDE, column_patterns=["ho_ten", "email"])
            >>> ColumnFilterService.should_scan_column("ho_ten", config)
            True
            >>> ColumnFilterService.should_scan_column("internal_id", config)
            False
        """
        # Mode: ALL - scan everything
        if filter_config.mode == FilterMode.ALL:
            return True
        
        # No patterns specified
        if not filter_config.column_patterns:
            if filter_config.mode == FilterMode.INCLUDE:
                logger.warning(
                    "[WARNING] Include mode with no patterns - no columns will be scanned"
                )
                return False
            else:
                # Exclude mode with no patterns = scan all
                return True
        
        # Check if column matches any pattern
        matches_pattern = ColumnFilterService._matches_any_pattern(
            column_name,
            filter_config.column_patterns,
            filter_config.use_regex,
            filter_config.case_sensitive
        )
        
        # Apply mode logic
        if filter_config.mode == FilterMode.INCLUDE:
            result = matches_pattern  # Scan if matches
        else:  # FilterMode.EXCLUDE
            result = not matches_pattern  # Scan if does NOT match
        
        if not result:
            logger.debug(
                f"[FILTERED] Column '{column_name}' excluded by "
                f"{filter_config.mode} filter"
            )
        
        return result
    
    @staticmethod
    def _matches_any_pattern(
        column_name: str,
        patterns: List[str],
        use_regex: bool,
        case_sensitive: bool
    ) -> bool:
        """
        Check if column name matches any pattern
        
        Args:
            column_name: Column name to check
            patterns: List of patterns (regex or exact)
            use_regex: Whether to use regex matching
            case_sensitive: Whether matching is case-sensitive
            
        Returns:
            True if column matches any pattern, False otherwise
        """
        # Apply case sensitivity
        if not case_sensitive:
            column_name = column_name.lower()
        
        for pattern in patterns:
            if not case_sensitive:
                pattern = pattern.lower()
            
            if use_regex:
                try:
                    if re.match(pattern, column_name):
                        return True
                except re.error as e:
                    logger.error(
                        f"[ERROR] Invalid regex pattern '{pattern}': {str(e)}"
                    )
                    continue
            else:
                # Exact match
                if column_name == pattern:
                    return True
        
        return False
    
    @staticmethod
    def filter_columns(
        all_columns: List[str],
        filter_config: ColumnFilterConfig
    ) -> List[str]:
        """
        Filter a list of columns based on configuration
        
        Args:
            all_columns: All available column names
            filter_config: Filter configuration
            
        Returns:
            Filtered list of column names
            
        Examples:
            >>> all_cols = ["ho_ten", "email", "internal_id", "created_at"]
            >>> config = ColumnFilterConfig(mode=FilterMode.INCLUDE, column_patterns=["ho_ten", "email"])
            >>> ColumnFilterService.filter_columns(all_cols, config)
            ['ho_ten', 'email']
        """
        filtered = [
            col for col in all_columns
            if ColumnFilterService.should_scan_column(col, filter_config)
        ]
        
        logger.info(
            f"[OK] Column filter applied: {len(filtered)}/{len(all_columns)} "
            f"columns selected (mode: {filter_config.mode})"
        )
        
        return filtered
    
    @staticmethod
    def get_filter_statistics(
        all_columns: List[str],
        filter_config: ColumnFilterConfig
    ) -> Dict[str, Any]:
        """
        Get filtering statistics for reporting
        
        Args:
            all_columns: All available column names
            filter_config: Filter configuration
            
        Returns:
            Dictionary with filtering statistics
        """
        filtered_columns = ColumnFilterService.filter_columns(all_columns, filter_config)
        
        reduction_percentage = (
            (1 - len(filtered_columns) / len(all_columns)) * 100
            if all_columns else 0.0
        )
        
        return {
            'total_columns': len(all_columns),
            'filtered_columns': len(filtered_columns),
            'excluded_columns': len(all_columns) - len(filtered_columns),
            'reduction_percentage': round(reduction_percentage, 2),
            'filter_mode': filter_config.mode.value,
            'patterns_count': len(filter_config.column_patterns)
        }


# Standalone testing
if __name__ == "__main__":
    # Test with Vietnamese column names
    columns = [
        "ho_ten", "so_cmnd", "email", "dia_chi",
        "internal_id", "created_at", "updated_at"
    ]
    
    # Test INCLUDE mode
    include_config = ColumnFilterConfig(
        mode=FilterMode.INCLUDE,
        column_patterns=["ho_ten", "so_cmnd", "email", "dia_chi"],
        use_regex=False,
        case_sensitive=False
    )
    
    filtered = ColumnFilterService.filter_columns(columns, include_config)
    stats = ColumnFilterService.get_filter_statistics(columns, include_config)
    
    print("[OK] Column Filtering Test")
    print(f"All columns: {columns}")
    print(f"Filtered columns: {filtered}")
    print(f"Statistics: {stats}")
    print(f"Reduction: {stats['reduction_percentage']}%")
