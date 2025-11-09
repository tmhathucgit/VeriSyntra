"""
VeriSyntra Data Inventory API Endpoints

FastAPI REST endpoints for data discovery and scanning with Vietnamese business context support.
All endpoints use dynamic configuration - zero hard-coded values.

Endpoints:
- POST /api/v1/data-inventory/scan - Start new scan job
- GET /api/v1/data-inventory/scans/{scan_job_id} - Get scan status
- DELETE /api/v1/data-inventory/scans/{scan_job_id} - Cancel scan
- GET /api/v1/data-inventory/filter-templates - List filter templates
"""

import logging
from uuid import UUID, uuid4
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, HTTPException, Path, status
from typing import List

# Import dynamic configuration
try:
    from ..config.constants import APIConfig, ScanConfig
    from ..api.models import (
        ScanRequest,
        ScanResponse,
        ScanStatusResponse,
        FilterTemplateResponse,
        FilterTemplateListResponse,
    )
    from ..services.scan_service import get_scan_service
except ImportError:
    from config.constants import APIConfig, ScanConfig
    from api.models import (
        ScanRequest,
        ScanResponse,
        ScanStatusResponse,
        FilterTemplateResponse,
        FilterTemplateListResponse,
    )
    from services.scan_service import get_scan_service

logger = logging.getLogger(__name__)

# Create router with dynamic configuration - NOT hard-coded
router = APIRouter(
    prefix=APIConfig.API_PREFIX,  # Use config, not "/api/v1/data-inventory"
    tags=APIConfig.API_TAGS,  # Use config, not ["Data Discovery"]
)

# Get service instance
scan_service = get_scan_service()


@router.post(
    "/scan",
    response_model=ScanResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start data discovery scan",
    description="Initiate asynchronous scan of database, cloud storage, or filesystem with Vietnamese business context support"
)
async def start_data_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks
):
    """
    Start data source scan for Vietnamese business with column filtering
    
    - Scans databases, cloud storage, or filesystems
    - UTF-8 encoding for Vietnamese text
    - Optional column filtering for cost and performance optimization
    - Asynchronous job processing with status tracking
    - Vietnamese regional business context awareness
    """
    try:
        # Generate unique job ID
        scan_job_id = uuid4()
        
        logger.info(
            f"[OK] Starting {request.source_type} scan for tenant {request.tenant_id}"
        )
        
        # Create job in state manager
        job_state = await scan_service.create_scan_job(
            scan_job_id=scan_job_id,
            tenant_id=request.tenant_id,
            source_type=request.source_type,
            connection_config=request.connection_config,
            column_filter=request.column_filter.dict() if request.column_filter else None,
            veri_business_context=request.veri_business_context.dict() if request.veri_business_context else None
        )
        
        # Add scan job to background tasks
        background_tasks.add_task(
            scan_service.execute_scan,
            scan_job_id=scan_job_id,
            tenant_id=request.tenant_id,
            source_type=request.source_type,
            connection_config=request.connection_config,
            column_filter=request.column_filter.dict() if request.column_filter else None,
            veri_business_context=request.veri_business_context.dict() if request.veri_business_context else None
        )
        
        # Return response with dynamic status - NOT hard-coded "pending"
        return ScanResponse(
            scan_job_id=scan_job_id,
            tenant_id=request.tenant_id,
            status=APIConfig.STATUS_PENDING,  # Use config
            estimated_time=ScanConfig.ESTIMATED_SCAN_TIME_SECONDS,  # Use config
            created_at=datetime.utcnow(),
            message="Scan job created successfully"
        )
        
    except ValueError as e:
        logger.error(f"[ERROR] Invalid request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]  # Use config limit
        )
    except Exception as e:
        logger.error(f"[ERROR] Failed to start scan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]  # Use config limit
        )


@router.get(
    "/scans/{scan_job_id}",
    response_model=ScanStatusResponse,
    summary="Get scan job status",
    description="Retrieve current status and results of a scan job"
)
async def get_scan_status(
    scan_job_id: UUID = Path(..., description="Unique scan job identifier")
):
    """
    Get Vietnamese data scan job status
    
    - Returns real-time progress (0-100%)
    - Discovered assets list with Vietnamese data indicators
    - Column filter statistics if filtering was applied
    - Error messages if any occurred
    - Duration and timestamp information
    """
    try:
        job_status = await scan_service.get_scan_status(scan_job_id)
        
        if not job_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scan job {scan_job_id} not found"
            )
        
        return ScanStatusResponse(**job_status)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Failed to get scan status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]  # Use config limit
        )


@router.delete(
    "/scans/{scan_job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel scan job",
    description="Cancel a running or pending scan job"
)
async def cancel_scan(
    scan_job_id: UUID = Path(..., description="Unique scan job identifier")
):
    """
    Cancel Vietnamese data scan job
    
    - Cancels pending or running scan jobs
    - Cannot cancel completed/failed/already cancelled jobs
    - Returns 204 No Content on success
    - Returns 404 if job not found
    - Returns 400 if job cannot be cancelled (already terminal state)
    """
    try:
        cancelled = await scan_service.cancel_scan(scan_job_id)
        
        if not cancelled:
            # Check if job exists
            job_status = await scan_service.get_scan_status(scan_job_id)
            if not job_status:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Scan job {scan_job_id} not found"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot cancel job in state: {job_status['status']}"
                )
        
        logger.info(f"[OK] Scan job {scan_job_id} cancelled")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Failed to cancel scan: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]  # Use config limit
        )


@router.get(
    "/filter-templates",
    response_model=FilterTemplateListResponse,
    summary="List filter templates",
    description="Get list of predefined column filter templates for Vietnamese PDPL compliance"
)
async def list_filter_templates():
    """
    List available filter templates
    
    Returns predefined column filter templates for common use cases:
    - personal_data_only: Vietnamese personal data fields (PDPL sensitive)
    - exclude_system_columns: Exclude technical/system columns
    - financial_data_only: Financial and banking data only
    - contact_info_only: Contact information only
    - all_columns: Scan all columns (no filtering)
    """
    try:
        # Import filter templates
        try:
            from ..presets.filter_templates import ColumnFilterTemplates
        except ImportError:
            from presets.filter_templates import ColumnFilterTemplates
        
        # Get all available templates
        template_names = ColumnFilterTemplates.list_templates()
        
        templates = []
        for name, description in template_names.items():
            filter_config = ColumnFilterTemplates.get_template(name)
            templates.append(
                FilterTemplateResponse(
                    template_name=name,
                    description=description,
                    filter_config=filter_config
                )
            )
        
        return FilterTemplateListResponse(
            templates=templates,
            total_count=len(templates)
        )
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to list filter templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]  # Use config limit
        )


# Health check endpoint (not in spec but useful)
@router.get(
    "/health",
    summary="Health check",
    description="Check API health and statistics"
)
async def health_check():
    """
    API health check
    
    Returns:
    - API version
    - Job statistics
    - Configuration summary
    """
    try:
        from ..services.job_state_manager import get_job_state_manager
        
        job_manager = get_job_state_manager()
        stats = job_manager.get_statistics()
        
        return {
            'status': 'healthy',
            'api_version': APIConfig.API_VERSION,
            'job_statistics': stats,
            'config': {
                'max_concurrent_requests': APIConfig.MAX_CONCURRENT_REQUESTS,
                'max_background_tasks': APIConfig.MAX_BACKGROUND_TASKS,
                'task_retention_hours': APIConfig.TASK_RETENTION_HOURS,
            }
        }
        
    except Exception as e:
        logger.error(f"[ERROR] Health check failed: {str(e)}")
        return {
            'status': 'degraded',
            'error': str(e)[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]
        }
