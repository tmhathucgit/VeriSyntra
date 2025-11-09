"""
VeriSyntra Data Inventory API Models

Pydantic models for request/response validation with Vietnamese business context support.
All models follow VeriSyntra's dynamic coding principles - zero hard-coded values.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

# Import column filter model from existing module
try:
    from ..models.column_filter import ColumnFilterConfig
except ImportError:
    # Fallback if column_filter module doesn't exist yet
    from enum import Enum
    
    class FilterMode(str, Enum):
        """Column filtering modes"""
        INCLUDE = "include"
        EXCLUDE = "exclude"
        ALL = "all"
    
    class ColumnFilterConfig(BaseModel):
        """Column filter configuration"""
        mode: FilterMode = Field(default=FilterMode.ALL)
        column_patterns: List[str] = Field(default=[])
        use_regex: bool = Field(default=False)
        case_sensitive: bool = Field(default=False)


class VeriBusinessContext(BaseModel):
    """Vietnamese business context for culturally-aware scanning"""
    
    veri_regional_location: Optional[str] = Field(
        default=None,
        description="Vietnamese regional location: 'north' | 'central' | 'south'"
    )
    veri_industry_type: Optional[str] = Field(
        default=None,
        description="Industry: 'technology' | 'manufacturing' | 'finance' | 'retail' | 'healthcare'"
    )
    veri_company_size: Optional[str] = Field(
        default=None,
        description="Company size: 'small' | 'medium' | 'large' | 'enterprise'"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "veri_regional_location": "south",
                "veri_industry_type": "finance",
                "veri_company_size": "medium"
            }
        }


class ScanRequest(BaseModel):
    """Request to start data discovery scan with Vietnamese business context"""
    
    tenant_id: UUID = Field(..., description="Unique tenant identifier")
    
    source_type: str = Field(
        ...,
        description="Data source type: 'database' | 'cloud' | 'filesystem'"
    )
    
    connection_config: Dict[str, Any] = Field(
        ...,
        description="Connection configuration specific to source type"
    )
    
    column_filter: Optional[ColumnFilterConfig] = Field(
        default=None,
        description="Column filtering configuration (for database scans)"
    )
    
    veri_business_context: Optional[VeriBusinessContext] = Field(
        default=None,
        description="Vietnamese business context for culturally-aware scanning"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tenant_id": "123e4567-e89b-12d3-a456-426614174000",
                "source_type": "database",
                "connection_config": {
                    "scanner_type": "postgresql",
                    "host": "localhost",
                    "port": 5432,
                    "database": "customer_db",
                    "username": "scanner",
                    "password": "********",
                    "schema": "public"
                },
                "column_filter": {
                    "mode": "include",
                    "column_patterns": [
                        "ho_ten", "email", "so_dien_thoai", "dia_chi"
                    ],
                    "use_regex": False,
                    "case_sensitive": False
                },
                "veri_business_context": {
                    "veri_regional_location": "south",
                    "veri_industry_type": "finance",
                    "veri_company_size": "medium"
                }
            }
        }


class ScanResponse(BaseModel):
    """Response after initiating scan job"""
    
    scan_job_id: UUID = Field(..., description="Unique scan job identifier")
    tenant_id: UUID = Field(..., description="Tenant identifier")
    status: str = Field(..., description="Initial job status (typically 'pending')")
    estimated_time: int = Field(..., description="Estimated completion time in seconds")
    created_at: datetime = Field(..., description="Job creation timestamp")
    message: str = Field(default="Scan job created successfully")
    
    class Config:
        json_schema_extra = {
            "example": {
                "scan_job_id": "987fcdeb-51a2-43f7-8d9e-123456789abc",
                "tenant_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "pending",
                "estimated_time": 300,
                "created_at": "2025-11-04T10:30:00Z",
                "message": "Scan job created successfully"
            }
        }


class DiscoveredAsset(BaseModel):
    """Single discovered data asset"""
    
    asset_type: str = Field(..., description="Type: 'table' | 'collection' | 'file' | 'object'")
    asset_name: str = Field(..., description="Asset name")
    asset_path: Optional[str] = Field(default=None, description="Full path or identifier")
    column_count: Optional[int] = Field(default=None, description="Number of columns/fields")
    row_count: Optional[int] = Field(default=None, description="Estimated row count")
    size_bytes: Optional[int] = Field(default=None, description="Size in bytes")
    has_vietnamese_data: bool = Field(default=False, description="Contains Vietnamese text")
    pdpl_sensitive: bool = Field(default=False, description="Potentially PDPL-sensitive")
    
    class Config:
        json_schema_extra = {
            "example": {
                "asset_type": "table",
                "asset_name": "customers",
                "asset_path": "public.customers",
                "column_count": 12,
                "row_count": 15430,
                "size_bytes": 2048000,
                "has_vietnamese_data": True,
                "pdpl_sensitive": True
            }
        }


class FilterStatistics(BaseModel):
    """Column filter statistics"""
    
    filter_applied: bool = Field(..., description="Whether filtering was applied")
    filter_mode: Optional[str] = Field(default=None, description="Filter mode used")
    total_columns: int = Field(..., description="Total columns discovered")
    filtered_columns: int = Field(..., description="Columns after filtering")
    excluded_columns: int = Field(..., description="Columns excluded by filter")
    reduction_percentage: float = Field(..., description="Percentage of columns excluded")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filter_applied": True,
                "filter_mode": "include",
                "total_columns": 45,
                "filtered_columns": 8,
                "excluded_columns": 37,
                "reduction_percentage": 82.22
            }
        }


class ScanStatusResponse(BaseModel):
    """Detailed scan job status response"""
    
    scan_job_id: UUID = Field(..., description="Scan job identifier")
    tenant_id: UUID = Field(..., description="Tenant identifier")
    status: str = Field(..., description="Current job status")
    progress: int = Field(..., description="Progress percentage (0-100)", ge=0, le=100)
    
    discovered_assets: List[DiscoveredAsset] = Field(
        default=[],
        description="List of discovered data assets"
    )
    
    filter_statistics: Optional[FilterStatistics] = Field(
        default=None,
        description="Column filter statistics if filtering was applied"
    )
    
    errors: List[str] = Field(
        default=[],
        description="Error messages if any"
    )
    
    started_at: Optional[datetime] = Field(
        default=None,
        description="Scan start timestamp"
    )
    
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Scan completion timestamp"
    )
    
    duration_seconds: Optional[int] = Field(
        default=None,
        description="Total execution time in seconds"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scan_job_id": "987fcdeb-51a2-43f7-8d9e-123456789abc",
                "tenant_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "completed",
                "progress": 100,
                "discovered_assets": [
                    {
                        "asset_type": "table",
                        "asset_name": "customers",
                        "asset_path": "public.customers",
                        "column_count": 12,
                        "row_count": 15430,
                        "has_vietnamese_data": True,
                        "pdpl_sensitive": True
                    }
                ],
                "filter_statistics": {
                    "filter_applied": True,
                    "filter_mode": "include",
                    "total_columns": 45,
                    "filtered_columns": 8,
                    "excluded_columns": 37,
                    "reduction_percentage": 82.22
                },
                "errors": [],
                "started_at": "2025-11-04T10:30:05Z",
                "completed_at": "2025-11-04T10:35:20Z",
                "duration_seconds": 315
            }
        }


class FilterTemplateResponse(BaseModel):
    """Single filter template details"""
    
    template_name: str = Field(..., description="Template identifier")
    description: str = Field(..., description="Human-readable description")
    filter_config: ColumnFilterConfig = Field(..., description="Filter configuration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "template_name": "personal_data_only",
                "description": "Vietnamese personal data fields (PDPL sensitive)",
                "filter_config": {
                    "mode": "include",
                    "column_patterns": [
                        "ho_ten", "so_cmnd", "so_cccd", "email", 
                        "so_dien_thoai", "dia_chi"
                    ],
                    "use_regex": False,
                    "case_sensitive": False
                }
            }
        }


class FilterTemplateListResponse(BaseModel):
    """List of available filter templates"""
    
    templates: List[FilterTemplateResponse] = Field(
        ...,
        description="Available filter templates"
    )
    total_count: int = Field(..., description="Total number of templates")
    
    class Config:
        json_schema_extra = {
            "example": {
                "templates": [
                    {
                        "template_name": "personal_data_only",
                        "description": "Vietnamese personal data fields (PDPL sensitive)",
                        "filter_config": {
                            "mode": "include",
                            "column_patterns": ["ho_ten", "email"],
                            "use_regex": False,
                            "case_sensitive": False
                        }
                    }
                ],
                "total_count": 5
            }
        }
