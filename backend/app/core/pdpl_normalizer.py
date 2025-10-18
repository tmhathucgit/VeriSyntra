"""
VeriSyntra PDPL Text Normalization System
Normalizes Vietnamese company names and personal names for company-agnostic AI models.

Author: VeriSyntra Development Team
Created: 2025-10-18
Version: 1.0.0
"""

import re
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass

from .company_registry import get_registry, CompanyRegistry


@dataclass
class NormalizationResult:
    """
    Result of text normalization operation.
    
    Attributes:
        original_text (str): Original input text
        normalized_text (str): Text with entities replaced by tokens
        entities_found (List[Dict]): List of detected entities with metadata
        company_count (int): Number of company names normalized
        person_count (int): Number of person names normalized
    """
    original_text: str
    normalized_text: str
    entities_found: List[Dict[str, Any]]
    company_count: int
    person_count: int


class PDPLTextNormalizer:
    """
    PDPL 2025 Text Normalization System.
    
    This class normalizes Vietnamese company names and personal names
    to enable company-agnostic AI models. It replaces specific company
    names with [COMPANY] tokens and person names with [PERSON] tokens.
    
    Key Features:
    - Dynamic company registry integration
    - Vietnamese name pattern recognition
    - Case-insensitive matching
    - Preserves text structure
    - Tracks normalization metadata
    
    Attributes:
        company_registry (CompanyRegistry): Registry for company lookups
        person_patterns (List[re.Pattern]): Regex patterns for Vietnamese names
        company_patterns (List[re.Pattern]): Patterns for company structures
    """
    
    # Vietnamese common titles and prefixes
    VIETNAMESE_TITLES = [
        'ông', 'bà', 'anh', 'chị', 'em',
        'ông', 'ba', 'cô', 'chu', 'bác',
        'mr', 'mrs', 'ms', 'dr', 'prof'
    ]
    
    # Vietnamese company suffixes
    COMPANY_SUFFIXES = [
        'corporation', 'corp', 'company', 'co', 'ltd',
        'limited', 'inc', 'joint stock', 'jsc',
        'công ty', 'cong ty', 'tổng công ty', 'tong cong ty',
        'tập đoàn', 'tap doan', 'ngân hàng', 'ngan hang',
        'bank', 'group', 'holdings', 'international'
    ]
    
    def __init__(self, company_registry: Optional[CompanyRegistry] = None):
        """
        Initialize PDPL Text Normalizer.
        
        Args:
            company_registry (CompanyRegistry, optional): Company registry instance.
                If None, uses singleton from get_registry()
        """
        self.company_registry = company_registry or get_registry()
        
        # Compile regex patterns for efficiency
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """
        Compile regex patterns for Vietnamese name and company detection.
        """
        # Vietnamese person name patterns
        # Format: Title + Given Name + Family Name
        title_pattern = '|'.join(self.VIETNAMESE_TITLES)
        
        self.person_patterns = [
            # With title: "ông Nguyễn Văn A", "Mrs. Trần Thị B"
            re.compile(
                rf'\b(?:{title_pattern})\.?\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+){1,3})\b',
                re.IGNORECASE | re.UNICODE
            ),
            # Without title: "Nguyễn Văn A", "Trần Thị B"
            re.compile(
                r'\b([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+\s+(?:[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+\s+){1,2}[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)\b',
                re.UNICODE
            )
        ]
        
        # Company structure patterns
        suffix_pattern = '|'.join(re.escape(s) for s in self.COMPANY_SUFFIXES)
        
        self.company_patterns = [
            # Company name with suffix
            re.compile(
                rf'\b([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][\w\s]+?)\s+(?:{suffix_pattern})\b',
                re.IGNORECASE | re.UNICODE
            )
        ]
    
    def normalize_text(
        self,
        text: str,
        normalize_companies: bool = True,
        normalize_persons: bool = False
    ) -> NormalizationResult:
        """
        Normalize text by replacing entities with tokens.
        
        Args:
            text (str): Input text to normalize
            normalize_companies (bool): Replace company names with [COMPANY] (default True)
            normalize_persons (bool): Replace person names with [PERSON] (default False)
        
        Returns:
            NormalizationResult with normalized text and metadata
        
        Example:
            >>> normalizer = PDPLTextNormalizer()
            >>> result = normalizer.normalize_text(
            ...     "Vietcombank và FPT hợp tác với ông Nguyễn Văn A"
            ... )
            >>> print(result.normalized_text)
            "[COMPANY] và [COMPANY] hợp tác với ông Nguyễn Văn A"
        """
        normalized_text = text
        entities_found = []
        company_count = 0
        person_count = 0
        
        # Normalize companies
        if normalize_companies:
            normalized_text, company_entities, company_count = self._normalize_companies(
                normalized_text
            )
            entities_found.extend(company_entities)
        
        # Normalize persons
        if normalize_persons:
            normalized_text, person_entities, person_count = self._normalize_persons(
                normalized_text
            )
            entities_found.extend(person_entities)
        
        return NormalizationResult(
            original_text=text,
            normalized_text=normalized_text,
            entities_found=entities_found,
            company_count=company_count,
            person_count=person_count
        )
    
    def normalize_for_inference(self, text: str) -> str:
        """
        Normalize text for AI model inference (companies only).
        
        This is the primary method used for preparing text before
        sending to AI models for classification.
        
        Args:
            text (str): Input text
        
        Returns:
            Normalized text with [COMPANY] tokens
        
        Example:
            >>> normalizer = PDPLTextNormalizer()
            >>> normalized = normalizer.normalize_for_inference(
            ...     "Grab Vietnam thu thập dữ liệu vị trí"
            ... )
            >>> print(normalized)
            "[COMPANY] thu thập dữ liệu vị trí"
        """
        result = self.normalize_text(
            text,
            normalize_companies=True,
            normalize_persons=False
        )
        return result.normalized_text
    
    def denormalize_text(
        self,
        normalized_text: str,
        entity_map: Dict[str, str]
    ) -> str:
        """
        Reverse normalization by replacing tokens with original entities.
        
        This is used for displaying AI model outputs with actual company names.
        
        Args:
            normalized_text (str): Text with [COMPANY] or [PERSON] tokens
            entity_map (Dict[str, str]): Mapping of tokens to original values
                Example: {'[COMPANY]_0': 'Vietcombank', '[COMPANY]_1': 'FPT'}
        
        Returns:
            Text with tokens replaced by original entity names
        
        Example:
            >>> denormalized = normalizer.denormalize_text(
            ...     "[COMPANY] processes personal data",
            ...     {'[COMPANY]': 'Grab Vietnam'}
            ... )
            >>> print(denormalized)
            "Grab Vietnam processes personal data"
        """
        denormalized_text = normalized_text
        
        # Replace tokens with original entities
        for token, original_value in entity_map.items():
            denormalized_text = denormalized_text.replace(token, original_value)
        
        return denormalized_text
    
    def _normalize_companies(self, text: str) -> Tuple[str, List[Dict[str, Any]], int]:
        """
        Normalize company names in text.
        
        Args:
            text (str): Input text
        
        Returns:
            Tuple of (normalized_text, entities_list, company_count)
        """
        normalized_text = text
        entities = []
        companies_replaced: Set[str] = set()  # Track canonical company names
        
        # Build list of all searchable terms (companies + aliases)
        search_terms = []
        
        for company_name in self.company_registry.get_all_companies():
            # Add canonical name
            search_terms.append((company_name, company_name))
            
            # Add aliases
            company_info = self.company_registry.get_company_info(company_name)
            if company_info and 'metadata' in company_info:
                # Search in original companies dict for aliases
                for industry, regions in self.company_registry.companies.items():
                    for region, company_list in regions.items():
                        for company in company_list:
                            if company['name'] == company_name:
                                for alias in company.get('aliases', []):
                                    search_terms.append((alias, company_name))
        
        # Sort by length (longest first) to handle overlapping names
        search_terms.sort(key=lambda x: len(x[0]), reverse=True)
        
        # Track already replaced canonical companies
        for search_term, canonical_name in search_terms:
            # Skip if this company already replaced
            if canonical_name.lower() in companies_replaced:
                continue
            
            # Case-insensitive search
            pattern = re.compile(re.escape(search_term), re.IGNORECASE)
            
            match = pattern.search(normalized_text)
            if match:
                matched_text = match.group()
                
                # Get company info
                company_info = self.company_registry.get_company_info(canonical_name)
                
                entities.append({
                    'type': 'company',
                    'original': matched_text,
                    'token': '[COMPANY]',
                    'position': match.span(),
                    'metadata': company_info
                })
                
                # Replace with token
                normalized_text = normalized_text[:match.start()] + '[COMPANY]' + normalized_text[match.end():]
                
                # Mark canonical company as replaced
                companies_replaced.add(canonical_name.lower())
        
        return normalized_text, entities, len(entities)
    
    def _normalize_persons(self, text: str) -> Tuple[str, List[Dict[str, Any]], int]:
        """
        Normalize Vietnamese person names in text.
        
        Args:
            text (str): Input text
        
        Returns:
            Tuple of (normalized_text, entities_list, person_count)
        """
        normalized_text = text
        entities = []
        replacements_made: Set[str] = set()
        
        # Apply person name patterns
        for pattern in self.person_patterns:
            matches = list(pattern.finditer(normalized_text))
            
            for match in matches:
                matched_text = match.group()
                
                # Avoid duplicate replacements
                if matched_text.lower() not in replacements_made:
                    # Check if this might be a company (has company suffix)
                    is_company = any(
                        suffix.lower() in matched_text.lower()
                        for suffix in self.COMPANY_SUFFIXES
                    )
                    
                    if not is_company:
                        entities.append({
                            'type': 'person',
                            'original': matched_text,
                            'token': '[PERSON]',
                            'position': match.span()
                        })
                        
                        # Replace with token
                        normalized_text = normalized_text[:match.start()] + '[PERSON]' + normalized_text[match.end():]
                        
                        replacements_made.add(matched_text.lower())
        
        return normalized_text, entities, len(replacements_made)
    
    def get_company_mentions(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all company mentions from text without normalization.
        
        Args:
            text (str): Input text
        
        Returns:
            List of company mention dictionaries
        
        Example:
            >>> mentions = normalizer.get_company_mentions(
            ...     "Vietcombank và FPT hợp tác"
            ... )
            >>> print(mentions)
            [{'name': 'Vietcombank', 'industry': 'finance', ...},
             {'name': 'FPT Corporation', 'industry': 'technology', ...}]
        """
        mentions = []
        all_companies = self.company_registry.get_all_companies()
        
        for company_name in all_companies:
            pattern = re.compile(re.escape(company_name), re.IGNORECASE)
            matches = list(pattern.finditer(text))
            
            if matches:
                company_info = self.company_registry.get_company_info(company_name)
                mentions.append({
                    'name': company_name,
                    'occurrences': len(matches),
                    'positions': [m.span() for m in matches],
                    'metadata': company_info
                })
        
        return mentions
    
    def validate_normalization(self, original: str, normalized: str) -> Dict[str, Any]:
        """
        Validate that normalization preserved text structure.
        
        Args:
            original (str): Original text
            normalized (str): Normalized text
        
        Returns:
            Dict with validation results:
                - is_valid (bool): Whether normalization is valid
                - token_count (int): Number of tokens added
                - length_ratio (float): Ratio of normalized to original length
                - issues (List[str]): Any validation issues found
        """
        issues = []
        
        # Count tokens
        company_tokens = normalized.count('[COMPANY]')
        person_tokens = normalized.count('[PERSON]')
        total_tokens = company_tokens + person_tokens
        
        # Check for structural issues
        if '[COMPANY]' in normalized and '[COMPANY]' in original:
            issues.append('Original text already contains [COMPANY] token')
        
        if '[PERSON]' in normalized and '[PERSON]' in original:
            issues.append('Original text already contains [PERSON] token')
        
        # Length comparison
        length_ratio = len(normalized) / len(original) if len(original) > 0 else 0
        
        # Extreme length changes might indicate issues
        if length_ratio < 0.3 or length_ratio > 3.0:
            issues.append(f'Unusual length ratio: {length_ratio:.2f}')
        
        is_valid = len(issues) == 0
        
        return {
            'is_valid': is_valid,
            'token_count': total_tokens,
            'company_tokens': company_tokens,
            'person_tokens': person_tokens,
            'length_ratio': length_ratio,
            'issues': issues
        }


# Singleton instance for application-wide use
_normalizer_instance: Optional[PDPLTextNormalizer] = None


def get_normalizer(company_registry: Optional[CompanyRegistry] = None) -> PDPLTextNormalizer:
    """
    Get or create singleton PDPLTextNormalizer instance.
    
    Args:
        company_registry (CompanyRegistry, optional): Registry instance
    
    Returns:
        PDPLTextNormalizer singleton instance
    
    Example:
        >>> normalizer = get_normalizer()
        >>> normalized = normalizer.normalize_for_inference("Grab thu thập dữ liệu")
    """
    global _normalizer_instance
    
    if _normalizer_instance is None:
        _normalizer_instance = PDPLTextNormalizer(company_registry)
    
    return _normalizer_instance
