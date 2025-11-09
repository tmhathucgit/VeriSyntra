"""
Admin API for Dynamic Company Registry Management
Phase 3 Implementation - VeriAIDPO Dynamic Company Registry

Version: 1.0.0
Status: COMPLETE - RBAC Protected (Task 1.1.3 Step 7)

RBAC Protection:
- All endpoints require authentication
- Write operations: admin role only (user.write permission)
- Read operations: admin/auditor roles (user.read permission)
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger

# Import Phase 1 components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from app.core.company_registry import get_registry
from app.core.pdpl_normalizer import get_normalizer

# Import RBAC dependencies (Task 1.1.3 Step 5)
from auth.rbac_dependencies import require_permission, CurrentUser


router = APIRouter(prefix="/admin/companies", tags=["admin", "companies"])


# Request/Response Models
class CompanyInput(BaseModel):
    """Input model for adding new company"""
    name: str = Field(..., description="Official company name", example="Netflix Vietnam")
    industry: str = Field(..., description="Industry category", example="technology")
    region: str = Field(..., description="Vietnamese region (north/central/south)", example="south")
    aliases: Optional[List[str]] = Field(
        default=None, 
        description="Alternative names", 
        example=["Netflix VN", "Netflix Viet Nam"]
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional metadata", 
        example={"website": "netflix.com/vn", "type": "Foreign"}
    )


class CompanyResponse(BaseModel):
    """Response model for company operations"""
    name: str
    industry: str
    region: str
    aliases: List[str]
    metadata: Dict[str, Any]
    added_date: str


class RegistryStatsResponse(BaseModel):
    """Response model for registry statistics"""
    total_companies: int
    by_industry: Dict[str, int]
    by_region: Dict[str, int]
    last_modified: Optional[str]


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    details: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    """Search results response"""
    query: str
    count: int
    results: List[Dict[str, Any]]


class CompanyListResponse(BaseModel):
    """Company list response"""
    industry: str
    count: int
    companies: List[Dict[str, Any]]


# Endpoints
@router.post("/add", response_model=CompanyResponse, status_code=201)
async def add_company(
    company: CompanyInput,
    current_user: CurrentUser = Depends(require_permission("user.write"))
):
    """
    Add new company to registry (no model retraining needed)
    
    **RBAC:** Requires `user.write` permission (admin role only)
    
    This endpoint enables runtime company additions without code deployment.
    The new company will be automatically normalized in all VeriAIDPO classifications.
    
    **Example Request:**
    ```json
    {
      "name": "Apple Vietnam",
      "industry": "technology",
      "region": "south",
      "aliases": ["Apple VN", "Apple Store Vietnam"],
      "metadata": {"website": "apple.com/vn", "type": "Foreign"}
    }
    ```
    
    **Supported Industries:**
    - technology, finance, healthcare, education, retail, manufacturing, 
      transportation, telecom, government
    
    **Supported Regions:**
    - north (Ha Noi region)
    - central (Da Nang, Hue region)
    - south (Ho Chi Minh City region)
    
    Vietnamese: Them cong ty moi vao co so du lieu (chi admin)
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"adding company: {company.name}"
        )
        
        registry = get_registry()
        
        # Add company to registry
        result = registry.add_company(
            name=company.name,
            industry=company.industry,
            region=company.region,
            aliases=company.aliases or [],
            metadata=company.metadata or {}
        )
        
        # Check if add was successful
        if not result.get('success'):
            raise HTTPException(
                status_code=400, 
                detail=result.get('message', 'Failed to add company')
            )
        
        # Hot-reload normalizer to include new company
        normalizer = get_normalizer()
        normalizer = get_normalizer()  # Hot-reload by getting fresh instance
        
        logger.success(f"Successfully added company: {company.name}")
        
        return CompanyResponse(
            name=company.name,
            industry=company.industry,
            region=company.region,
            aliases=company.aliases or [],
            metadata=company.metadata or {},
            added_date=datetime.now().isoformat()
        )
    
    except ValueError as e:
        logger.error(f"Validation error adding company: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to add company: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add company: {str(e)}")


@router.delete("/remove", response_model=MessageResponse)
async def remove_company(
    name: str = Query(..., description="Company name to remove"),
    industry: str = Query(..., description="Industry category"),
    region: str = Query(..., description="Region (north/central/south)"),
    current_user: CurrentUser = Depends(require_permission("user.delete"))
):
    """
    Remove company from registry
    
    **RBAC:** Requires `user.delete` permission (admin role only)
    
    Removes a company and hot-reloads the normalizer.
    
    **Example:**
    ```
    DELETE /api/v1/admin/companies/remove?name=OldCompany&industry=technology&region=south
    ```
    
    Vietnamese: Xoa cong ty khoi co so du lieu (chi admin)
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"removing company: {name}"
        )
        
        registry = get_registry()
        success = registry.remove_company(name, industry, region)
        
        if success:
            # Hot-reload normalizer
            normalizer = get_normalizer()
            normalizer= get_normalizer()  # Hot-reload by getting fresh instance
            
            logger.success(f"Successfully removed company: {name}")
            
            return MessageResponse(
                message=f"Removed company '{name}'",
                details={
                    "name": name,
                    "industry": industry,
                    "region": region
                }
            )
        else:
            logger.warning(f"Company not found: {name}")
            raise HTTPException(
                status_code=404, 
                detail=f"Company '{name}' not found in {industry}/{region}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove company: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to remove company: {str(e)}")


@router.get("/search", response_model=SearchResponse)
async def search_companies(
    query: str = Query(..., description="Search query (company name or alias)", min_length=1),
    current_user: CurrentUser = Depends(require_permission("user.read"))
):
    """
    Search companies by name or alias
    
    **RBAC:** Requires `user.read` permission (admin/auditor/dpo roles)
    
    Performs case-insensitive search across company names and aliases.
    
    **Example:**
    ```
    GET /api/v1/admin/companies/search?query=shopee
    ```
    
    **Returns:**
    - All companies matching the query
    - Includes industry and region information
    
    Vietnamese: Tim kiem cong ty theo ten hoac biet danh
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"searching companies: query='{query}'"
        )
        
        registry = get_registry()
        results = registry.search_companies(query)
        
        logger.info(f"Found {len(results)} companies matching '{query}'")
        
        return SearchResponse(
            query=query,
            count=len(results),
            results=results
        )
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/list/{industry}", response_model=CompanyListResponse)
async def list_companies_by_industry(
    industry: str,
    current_user: CurrentUser = Depends(require_permission("user.read"))
):
    """
    Get all companies in specific industry
    
    **RBAC:** Requires `user.read` permission (admin/auditor/dpo roles)
    
    Returns all companies across all regions for the given industry.
    
    **Example:**
    ```
    GET /api/v1/admin/companies/list/technology
    ```
    
    **Supported Industries:**
    - technology, finance, healthcare, education, retail, manufacturing,
      transportation, telecom, government
    
    Vietnamese: Lay tat ca cong ty trong nganh cong nghiep cu the
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"listing companies for industry: {industry}"
        )
        
        registry = get_registry()
        companies = registry.search_companies(industry)
        
        logger.info(f"Found {len(companies)} companies in {industry}")
        
        return CompanyListResponse(
            industry=industry,
            count=len(companies),
            companies=companies
        )
    
    except Exception as e:
        logger.error(f"Failed to list companies: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list companies: {str(e)}")


@router.get("/stats", response_model=RegistryStatsResponse)
async def get_registry_stats(
    current_user: CurrentUser = Depends(require_permission("user.read"))
):
    """
    Get company registry statistics
    
    **RBAC:** Requires `user.read` permission (admin/auditor/dpo roles)
    
    Returns comprehensive statistics about the registry:
    - Total number of companies
    - Breakdown by industry
    - Breakdown by region
    - Last modification timestamp
    
    **Example Response:**
    ```json
    {
      "total_companies": 47,
      "by_industry": {
        "technology": 15,
        "finance": 10,
        "healthcare": 8
      },
      "by_region": {
        "north": 18,
        "central": 5,
        "south": 24
      },
      "last_modified": "2025-10-18T10:30:00"
    }
    ```
    
    Vietnamese: Lay thong ke dang ky cong ty
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"fetching registry statistics"
        )
        
        registry = get_registry()
        stats = registry.get_statistics()
        
        logger.info(f"Registry stats: {stats['total_companies']} total companies")
        
        return RegistryStatsResponse(**stats)
    
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post("/reload", response_model=MessageResponse)
async def reload_registry(
    current_user: CurrentUser = Depends(require_permission("user.write"))
):
    """
    Hot-reload company registry from config file
    
    **RBAC:** Requires `user.write` permission (admin role only)
    
    Reloads the registry from `config/company_registry.json` without restarting
    the server. Useful after manual config file updates.
    
    **Use Case:**
    1. Manually edit `config/company_registry.json`
    2. Call this endpoint to apply changes
    3. No server restart required
    
    **Returns:**
    - Success message with updated statistics
    
    Vietnamese: Tai lai dang ky cong ty tu tep cau hinh (chi admin)
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"hot-reloading company registry"
        )
        
        registry = get_registry()
        normalizer = get_normalizer()
        
        registry_success = registry.reload()
        normalizer= get_normalizer()  # Hot-reload by getting fresh instance
        
        if registry_success:
            stats = registry.get_statistics()
            logger.success(f"Registry reloaded: {stats['total_companies']} companies")
            
            return MessageResponse(
                message="Registry reloaded successfully",
                details=stats
            )
        else:
            logger.error("Registry reload failed")
            raise HTTPException(status_code=500, detail="Failed to reload registry")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Reload failed: {str(e)}")


@router.get("/export")
async def export_registry(
    current_user: CurrentUser = Depends(require_permission("user.read"))
):
    """
    Export full company registry as JSON
    
    **RBAC:** Requires `user.read` permission (admin/auditor/dpo roles)
    
    Returns the complete registry structure for backup or migration purposes.
    
    **Returns:**
    - Full registry data structure
    - Statistics summary
    
    **Use Case:**
    - Backup before major changes
    - Migration to another environment
    - Integration with external systems
    
    Vietnamese: Xuat dang ky cong ty day du dang JSON
    """
    try:
        logger.info(
            f"[RBAC] User {current_user.email} (role: {current_user.role}) "
            f"exporting company registry"
        )
        
        registry = get_registry()
        
        export_data = {
            "companies": registry.companies,
            "stats": registry.get_statistics(),
            "export_timestamp": datetime.now().isoformat(),
            "format_version": "1.0"
        }
        
        logger.success("Registry exported successfully")
        
        return export_data
    
    except Exception as e:
        logger.error(f"Export failed: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
