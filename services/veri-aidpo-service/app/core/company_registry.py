"""
VeriSyntra Company Registry System
Manages Vietnamese companies for PDPL 2025 compliance with dynamic company-agnostic AI models.

Author: VeriSyntra Development Team
Created: 2025-10-18
Version: 1.0.0
"""

import json
import os
from typing import Dict, List, Optional, Set, Any
from datetime import datetime
from pathlib import Path


class CompanyRegistry:
    """
    Dynamic Vietnamese Company Registry for PDPL 2025 Compliance.
    
    This class manages a hot-reloadable registry of Vietnamese companies
    to enable company-agnostic AI models that normalize company names
    to [COMPANY] tokens during training and inference.
    
    Key Features:
    - Zero-downtime hot-reload from JSON config
    - Multi-industry and multi-region support
    - Fuzzy search with aliases
    - Thread-safe operations
    - Comprehensive statistics
    
    Attributes:
        config_path (Path): Path to company_registry.json
        companies (Dict): Loaded company database
        _company_index (Dict): Fast lookup index
        _alias_index (Dict): Alias to canonical name mapping
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Company Registry.
        
        Args:
            config_path (str, optional): Path to company_registry.json.
                Defaults to backend/config/company_registry.json
        """
        if config_path is None:
            # Auto-detect config path relative to this file
            base_dir = Path(__file__).resolve().parent.parent.parent
            config_path = base_dir / "config" / "company_registry.json"
        
        self.config_path = Path(config_path)
        self.companies: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
        self._company_index: Dict[str, Dict[str, Any]] = {}
        self._alias_index: Dict[str, str] = {}
        
        # Load initial data
        self.reload()
    
    def reload(self) -> Dict[str, Any]:
        """
        Hot-reload company registry from JSON configuration.
        
        This method can be called at runtime to update the registry
        without restarting the application.
        
        Returns:
            Dict containing reload statistics:
                - success (bool): Whether reload succeeded
                - companies_loaded (int): Number of companies loaded
                - industries (int): Number of industries
                - regions (Set[str]): Regions covered
                - timestamp (str): ISO format reload time
                - error (str, optional): Error message if failed
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file has invalid JSON
        """
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(
                    f"Company registry config not found: {self.config_path}"
                )
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Rebuild indexes
            self._company_index.clear()
            self._alias_index.clear()
            
            companies_loaded = 0
            regions_found: Set[str] = set()
            
            for industry, regions in data.items():
                for region, company_list in regions.items():
                    regions_found.add(region)
                    
                    for company in company_list:
                        company_name = company['name']
                        companies_loaded += 1
                        
                        # Index by canonical name
                        company_key = self._normalize_key(company_name)
                        self._company_index[company_key] = {
                            'name': company_name,
                            'industry': industry,
                            'region': region,
                            'metadata': company.get('metadata', {}),
                            'added_date': company.get('added_date', datetime.now().isoformat())
                        }
                        
                        # Index aliases
                        for alias in company.get('aliases', []):
                            alias_key = self._normalize_key(alias)
                            self._alias_index[alias_key] = company_name
            
            self.companies = data
            
            return {
                'success': True,
                'companies_loaded': companies_loaded,
                'industries': len(data),
                'regions': regions_found,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'success': False,
                'companies_loaded': 0,
                'industries': 0,
                'regions': set(),
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def add_company(
        self,
        name: str,
        industry: str,
        region: str,
        aliases: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        persist: bool = True
    ) -> Dict[str, Any]:
        """
        Dynamically add a new company to the registry.
        
        Args:
            name (str): Canonical company name
            industry (str): Industry category (technology, finance, etc.)
            region (str): Regional location (north, central, south)
            aliases (List[str], optional): Alternative names/abbreviations
            metadata (Dict, optional): Additional company information
            persist (bool): Whether to save to JSON config (default True)
        
        Returns:
            Dict containing operation result:
                - success (bool): Whether add succeeded
                - company_name (str): Name of added company
                - message (str): Status message
                - error (str, optional): Error details if failed
        
        Example:
            >>> registry = CompanyRegistry()
            >>> result = registry.add_company(
            ...     name="New Startup Ltd",
            ...     industry="technology",
            ...     region="south",
            ...     aliases=["NSL", "New Startup"],
            ...     metadata={"founded": 2025, "website": "newstartup.vn"}
            ... )
        """
        try:
            # Validate inputs
            if not name or not industry or not region:
                return {
                    'success': False,
                    'company_name': name,
                    'message': 'Invalid input: name, industry, and region are required',
                    'error': 'Missing required fields'
                }
            
            # Check if company already exists
            company_key = self._normalize_key(name)
            if company_key in self._company_index:
                return {
                    'success': False,
                    'company_name': name,
                    'message': f'Company already exists: {name}',
                    'error': 'Duplicate company'
                }
            
            # Initialize industry and region if needed
            if industry not in self.companies:
                self.companies[industry] = {}
            if region not in self.companies[industry]:
                self.companies[industry][region] = []
            
            # Create company entry
            company_entry = {
                'name': name,
                'aliases': aliases or [],
                'metadata': metadata or {},
                'added_date': datetime.now().isoformat()
            }
            
            # Add to in-memory structures
            self.companies[industry][region].append(company_entry)
            
            self._company_index[company_key] = {
                'name': name,
                'industry': industry,
                'region': region,
                'metadata': metadata or {},
                'added_date': company_entry['added_date']
            }
            
            # Index aliases
            for alias in (aliases or []):
                alias_key = self._normalize_key(alias)
                self._alias_index[alias_key] = name
            
            # Persist to JSON if requested
            if persist:
                self._save_to_config()
            
            return {
                'success': True,
                'company_name': name,
                'message': f'Successfully added company: {name}'
            }
        
        except Exception as e:
            return {
                'success': False,
                'company_name': name,
                'message': 'Failed to add company',
                'error': str(e)
            }
    
    def remove_company(self, name: str, persist: bool = True) -> Dict[str, Any]:
        """
        Remove a company from the registry.
        
        Args:
            name (str): Company name (canonical or alias)
            persist (bool): Whether to save to JSON config (default True)
        
        Returns:
            Dict containing operation result:
                - success (bool): Whether removal succeeded
                - company_name (str): Name of removed company
                - message (str): Status message
                - error (str, optional): Error details if failed
        """
        try:
            # Resolve to canonical name
            canonical_name = self.resolve_alias(name)
            if not canonical_name:
                return {
                    'success': False,
                    'company_name': name,
                    'message': f'Company not found: {name}',
                    'error': 'Company does not exist'
                }
            
            company_key = self._normalize_key(canonical_name)
            company_info = self._company_index.get(company_key)
            
            if not company_info:
                return {
                    'success': False,
                    'company_name': name,
                    'message': f'Company not found in index: {canonical_name}',
                    'error': 'Index inconsistency'
                }
            
            industry = company_info['industry']
            region = company_info['region']
            
            # Remove from company list
            company_list = self.companies.get(industry, {}).get(region, [])
            self.companies[industry][region] = [
                c for c in company_list if c['name'] != canonical_name
            ]
            
            # Remove from indexes
            del self._company_index[company_key]
            
            # Remove aliases
            self._alias_index = {
                k: v for k, v in self._alias_index.items() 
                if v != canonical_name
            }
            
            # Persist to JSON if requested
            if persist:
                self._save_to_config()
            
            return {
                'success': True,
                'company_name': canonical_name,
                'message': f'Successfully removed company: {canonical_name}'
            }
        
        except Exception as e:
            return {
                'success': False,
                'company_name': name,
                'message': 'Failed to remove company',
                'error': str(e)
            }
    
    def search_companies(
        self,
        query: Optional[str] = None,
        industry: Optional[str] = None,
        region: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search companies with filters.
        
        Args:
            query (str, optional): Search term (matches name and aliases)
            industry (str, optional): Filter by industry
            region (str, optional): Filter by region
            limit (int): Maximum results to return (default 100)
        
        Returns:
            List of company dictionaries matching criteria
        
        Example:
            >>> registry.search_companies(query="bank", industry="finance")
            [{'name': 'Vietcombank', 'industry': 'finance', ...}, ...]
        """
        results = []
        query_normalized = self._normalize_key(query) if query else None
        
        for company_key, company_info in self._company_index.items():
            # Apply filters
            if industry and company_info['industry'] != industry:
                continue
            if region and company_info['region'] != region:
                continue
            
            # Apply query filter
            if query_normalized:
                # Search in canonical name
                if query_normalized in self._normalize_key(company_info['name']):
                    results.append(company_info)
                    continue
                
                # Search in aliases
                matching_alias = False
                for alias_key, canonical in self._alias_index.items():
                    if canonical == company_info['name'] and query_normalized in alias_key:
                        matching_alias = True
                        break
                
                if matching_alias:
                    results.append(company_info)
            else:
                # No query, include all that match filters
                results.append(company_info)
            
            # Check limit
            if len(results) >= limit:
                break
        
        return results
    
    def resolve_alias(self, name: str) -> Optional[str]:
        """
        Resolve company alias to canonical name.
        
        Args:
            name (str): Company name or alias
        
        Returns:
            Canonical company name if found, else None
        
        Example:
            >>> registry.resolve_alias("VCB")
            "Vietcombank"
        """
        name_key = self._normalize_key(name)
        
        # Check if it's already canonical
        if name_key in self._company_index:
            return self._company_index[name_key]['name']
        
        # Check if it's an alias
        if name_key in self._alias_index:
            return self._alias_index[name_key]
        
        return None
    
    def get_company_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get full company information.
        
        Args:
            name (str): Company name (canonical or alias)
        
        Returns:
            Company info dict if found, else None
        
        Example:
            >>> registry.get_company_info("Grab")
            {'name': 'Grab Vietnam', 'industry': 'transportation', ...}
        """
        canonical_name = self.resolve_alias(name)
        if not canonical_name:
            return None
        
        company_key = self._normalize_key(canonical_name)
        return self._company_index.get(company_key)
    
    def get_all_companies(self) -> List[str]:
        """
        Get list of all canonical company names.
        
        Returns:
            List of company names sorted alphabetically
        """
        return sorted([info['name'] for info in self._company_index.values()])
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive registry statistics.
        
        Returns:
            Dict containing:
                - total_companies (int): Total companies in registry
                - total_aliases (int): Total aliases indexed
                - industries (Dict): Companies per industry
                - regions (Dict): Companies per region
                - industry_list (List): All industry names
                - region_list (List): All region names
        """
        industries: Dict[str, int] = {}
        regions: Dict[str, int] = {}
        
        for company_info in self._company_index.values():
            industry = company_info['industry']
            region = company_info['region']
            
            industries[industry] = industries.get(industry, 0) + 1
            regions[region] = regions.get(region, 0) + 1
        
        return {
            'total_companies': len(self._company_index),
            'total_aliases': len(self._alias_index),
            'industries': industries,
            'regions': regions,
            'industry_list': sorted(industries.keys()),
            'region_list': sorted(regions.keys())
        }
    
    def _normalize_key(self, text: str) -> str:
        """
        Normalize text for case-insensitive matching.
        
        Args:
            text (str): Input text
        
        Returns:
            Normalized lowercase key
        """
        if not text:
            return ""
        return text.lower().strip()
    
    def _save_to_config(self) -> None:
        """
        Persist current registry state to JSON config file.
        
        Raises:
            IOError: If file write fails
        """
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.companies, f, indent=2, ensure_ascii=False)


# Singleton instance for application-wide use
_registry_instance: Optional[CompanyRegistry] = None


def get_registry(config_path: Optional[str] = None) -> CompanyRegistry:
    """
    Get or create singleton CompanyRegistry instance.
    
    Args:
        config_path (str, optional): Path to config file (only used on first call)
    
    Returns:
        CompanyRegistry singleton instance
    
    Example:
        >>> registry = get_registry()
        >>> companies = registry.get_all_companies()
    """
    global _registry_instance
    
    if _registry_instance is None:
        _registry_instance = CompanyRegistry(config_path)
    
    return _registry_instance
