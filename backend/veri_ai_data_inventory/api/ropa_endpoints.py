"""
ROPA API Endpoints - RESTful API for ROPA Generation
Vietnamese PDPL 2025 Compliance - Document #3 Section 7

This module provides FastAPI endpoints for ROPA document management:
- POST /generate - Generate ROPA document
- GET /{ropa_id} - Retrieve ROPA metadata
- GET /{ropa_id}/download - Download ROPA file
- GET /list - List all ROPA documents
- DELETE /{ropa_id} - Delete ROPA document
- GET /preview - Preview ROPA metadata

Document #3 Section 7: API Endpoints
"""

from fastapi import APIRouter, HTTPException, Query, Path as PathParam, Depends
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
from uuid import UUID
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from models.api_models import (
    ROPAGenerateRequest,
    ROPAGenerateResponse,
    ROPAListResponse,
    ROPAPreviewResponse,
    ROPADeleteResponse,
    ErrorResponse
)
from models.ropa_models import ROPADocument, ROPALanguage, ROPAOutputFormat
from services.ropa_service import ROPAService
from database.connection import get_db


# Create router with OpenAPI metadata for Swagger UI
router = APIRouter(
    prefix="/api/v1/data-inventory/{tenant_id}/ropa",
    tags=["ROPA Generation - Vietnamese PDPL 2025"],
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Resource not found / Không tìm thấy tài nguyên"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error / Lỗi máy chủ nội bộ"
        },
        501: {
            "model": ErrorResponse,
            "description": "Not implemented - Database integration required / Chưa triển khai - Cần tích hợp cơ sở dữ liệu"
        }
    }
)


# Initialize service (can be dependency-injected in production)
ropa_service = ROPAService()


@router.post(
    "/generate",
    response_model=dict,
    status_code=201,
    summary="Generate ROPA Document / Tạo tài liệu ROPA",
    description="""
    Generate Vietnamese PDPL 2025 compliant Record of Processing Activities (ROPA).
    
    **Supported Formats:**
    - `json` - Standard JSON export with complete structure
    - `csv` - 20-column CSV for Excel (UTF-8 BOM)
    - `pdf` - PDF with Vietnamese font support (Noto Sans)
    - `mps_format` - MPS JSON format per Circular 09/2024/TT-BCA
    
    **Languages:**
    - `vi` (Vietnamese) - Default, PDPL-compliant Vietnamese
    - `en` (English) - English translation
    
    **Vietnamese Business Context:**
    Include regional and industry context for culturally-appropriate generation:
    - **Region:** `north` (Hanoi), `central` (Da Nang), `south` (HCMC)
    - **Industry:** `technology`, `finance`, `manufacturing`, `healthcare`, etc.
    - **Size:** `startup`, `sme`, `enterprise`
    
    **[OK] Status:** FULLY IMPLEMENTED with database integration
    """,
    responses={
        201: {
            "description": "ROPA generated successfully / ROPA được tạo thành công",
            "content": {
                "application/json": {
                    "example": {
                        "ropa_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                        "download_url": "/api/v1/data-inventory/550e8400-e29b-41d4-a716-446655440000/ropa/7c9e6679-7425-40de-944b-e07fc1f90ae7/download",
                        "mps_compliant": True,
                        "generated_at": "2025-11-05T22:00:00+07:00",
                        "file_size_bytes": 26209,
                        "entry_count": 5,
                        "format": "pdf",
                        "language": "vi"
                    }
                }
            }
        },
        400: {"description": "Invalid request / Yêu cầu không hợp lệ"},
        500: {"description": "Internal server error / Lỗi máy chủ nội bộ"}
    }
)
async def generate_ropa(
    tenant_id: UUID = PathParam(
        ...,
        description="Tenant UUID for multi-tenancy / UUID của tenant",
        example="550e8400-e29b-41d4-a716-446655440000"
    ),
    request: ROPAGenerateRequest = None,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    **Generate Vietnamese PDPL 2025 ROPA Document**
    
    Creates a Record of Processing Activities compliant with:
    - Decree 13/2023/ND-CP Article 12 (ROPA requirements)
    - PDPL 2025 Article 17 (Record keeping obligations)
    - MPS Circular 09/2024/TT-BCA (Reporting format)
    
    **Zero Hard-Coding Architecture:**
    - Dictionary routing for format selection (no if/else)
    - Enum-based language and format validation
    - Vietnamese cultural intelligence integration
    
    **Example Request:**
    ```json
    {
      "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
      "format": "pdf",
      "language": "vi",
      "include_sensitive": true,
      "include_cross_border": true,
      "veri_business_context": {
        "region": "south",
        "industry": "technology",
        "business_size": "enterprise"
      }
    }
    ```
    
    **Vietnamese Context Impact:**
    - **South (HCMC):** Entrepreneurial tone, international business focus
    - **North (Hanoi):** Formal structure, government compliance emphasis
    - **Central (Da Nang):** Traditional values, consensus-building language
    """
    try:
        # Validate tenant_id matches request
        if request.tenant_id != tenant_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "TenantMismatch",
                    "message": "Tenant ID in path does not match request body",
                    "message_vi": "Tenant ID trong đường dẫn không khớp với yêu cầu"
                }
            )
        
        # Generate ROPA from database
        response = await ropa_service.generate_ropa_from_database(
            db=db,
            tenant_id=tenant_id,
            format=request.format,
            language=request.language,
            user_id=None,  # TODO: Add authentication to get current user
            veri_business_context=request.veri_business_context
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "GenerationFailed",
                "message": f"ROPA generation failed: {str(e)}",
                "message_vi": f"Tạo ROPA thất bại: {str(e)}"
            }
        )


@router.get(
    "/{ropa_id}",
    response_model=dict,
    summary="Get ROPA Metadata / Lấy thông tin ROPA",
    description="""
    Retrieve metadata for a specific ROPA document without downloading the full file.
    
    **Returns:**
    - Document ID, format, language
    - File size and entry count  
    - Generation timestamp (Vietnamese timezone)
    - MPS compliance status (Bộ Công an)
    - Download URL for file retrieval
    - Sensitive data and cross-border transfer flags
    
    **Use Cases:**
    - Display ROPA list in UI
    - Check document properties before download
    - Verify MPS compliance status
    - Monitor ROPA generation history
    """,
    responses={
        200: {
            "description": "Metadata retrieved successfully / Lấy thông tin thành công",
            "content": {
                "application/json": {
                    "example": {
                        "ropa_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                        "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
                        "format": "pdf",
                        "language": "vi",
                        "generated_at": "2025-11-05T22:00:00+07:00",
                        "file_size_bytes": 26209,
                        "download_url": "/api/v1/data-inventory/.../download",
                        "entry_count": 5,
                        "mps_compliant": True,
                        "has_sensitive_data": False,
                        "has_cross_border_transfers": True
                    }
                }
            }
        },
        404: {"description": "ROPA document not found / Không tìm thấy tài liệu ROPA"}
    }
)
async def get_ropa_metadata(
    tenant_id: UUID = PathParam(
        ...,
        description="Tenant UUID / UUID của tenant",
        example="550e8400-e29b-41d4-a716-446655440000"
    ),
    ropa_id: UUID = PathParam(
        ...,
        description="ROPA document UUID / UUID của tài liệu ROPA",
        example="7c9e6679-7425-40de-944b-e07fc1f90ae7"
    )
) -> dict:
    """
    **Get ROPA Document Metadata**
    
    Returns comprehensive metadata without downloading the full file.
    Useful for UI display and validation checks.
    
    **Metadata Fields:**
    - **ropa_id:** Unique document identifier
    - **format:** Generated format (json, csv, pdf, mps_format)
    - **language:** Document language (vi, en)
    - **mps_compliant:** MPS (Bộ Công an) compliance status
    - **has_sensitive_data:** Sensitive personal data presence
    - **has_cross_border_transfers:** Cross-border transfer flag
    - **generated_at:** Asia/Ho_Chi_Minh timezone
    """
    try:
        metadata = ropa_service.get_ropa_metadata(tenant_id, ropa_id)
        
        if not metadata:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ROPANotFound",
                    "message": f"ROPA document not found: {ropa_id}",
                    "message_vi": f"Không tìm thấy tài liệu ROPA: {ropa_id}"
                }
            )
        
        return metadata.model_dump()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "MetadataRetrievalFailed",
                "message": f"Failed to retrieve metadata: {str(e)}",
                "message_vi": f"Lấy metadata thất bại: {str(e)}"
            }
        )


@router.get(
    "/{ropa_id}/download",
    response_class=FileResponse,
    summary="Download ROPA File / Tải xuống file ROPA",
    description="""
    Download the generated ROPA file in the specified format.
    
    **Supported Formats:**
    - **JSON** (`application/json`) - Complete structured data
    - **CSV** (`text/csv`) - Excel-compatible with UTF-8 BOM
    - **PDF** (`application/pdf`) - Vietnamese font support
    - **MPS Format** (`application/json`) - MPS Circular 09/2024/TT-BCA
    
    **File Streaming:**
    - Efficient streaming for large PDFs
    - Proper Content-Type headers
    - Filename in response headers
    - Support for download managers
    
    **Vietnamese Fonts:**
    - PDF uses Noto Sans Vietnamese
    - Proper diacritics (á à ả ã ạ ă â ê ô ơ ư đ)
    - No font substitution issues
    """,
    responses={
        200: {
            "description": "File downloaded successfully / Tải file thành công",
            "content": {
                "application/pdf": {},
                "application/json": {},
                "text/csv": {}
            }
        },
        404: {"description": "File not found / Không tìm thấy file"}
    }
)
async def download_ropa(
    tenant_id: UUID = PathParam(
        ...,
        description="Tenant UUID / UUID của tenant",
        example="550e8400-e29b-41d4-a716-446655440000"
    ),
    ropa_id: UUID = PathParam(
        ...,
        description="ROPA document UUID / UUID của tài liệu ROPA",
        example="7c9e6679-7425-40de-944b-e07fc1f90ae7"
    ),
    format: ROPAOutputFormat = Query(
        ROPAOutputFormat.PDF,
        description="File format: json, csv, pdf, or mps_format / Định dạng file"
    )
) -> FileResponse:
    """
    **Download ROPA File with Streaming**
    
    Streams the generated ROPA file to client with appropriate Content-Type.
    
    **Format-Specific Headers:**
    - **PDF:** `Content-Type: application/pdf`
    - **JSON:** `Content-Type: application/json`
    - **CSV:** `Content-Type: text/csv; charset=utf-8`
    - **MPS:** `Content-Type: application/json`
    
    **Vietnamese Character Support:**
    - All formats use UTF-8 encoding
    - CSV includes BOM for Excel compatibility
    - PDF embeds Vietnamese fonts
    """
    try:
        file_path = ropa_service.get_ropa_file(tenant_id, ropa_id, format)
        
        if not file_path or not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "FileNotFound",
                    "message": f"ROPA file not found: {ropa_id} (format: {format.value})",
                    "message_vi": f"Không tìm thấy file ROPA: {ropa_id} (định dạng: {format.value})"
                }
            )
        
        # Content type mapping - ZERO HARD-CODING
        content_type_map = {
            ROPAOutputFormat.JSON: "application/json",
            ROPAOutputFormat.CSV: "text/csv",
            ROPAOutputFormat.PDF: "application/pdf",
            ROPAOutputFormat.MPS_FORMAT: "application/json"
        }
        
        media_type = content_type_map.get(format, "application/octet-stream")
        
        return FileResponse(
            path=str(file_path),
            media_type=media_type,
            filename=file_path.name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "DownloadFailed",
                "message": f"File download failed: {str(e)}",
                "message_vi": f"Tải file thất bại: {str(e)}"
            }
        )


@router.get(
    "/list",
    response_model=ROPAListResponse,
    summary="List ROPA Documents / Danh sách tài liệu ROPA",
    description="""
    List all ROPA documents for a tenant with pagination support.
    
    **Pagination:**
    - Default: 20 items per page
    - Maximum: 100 items per page
    - 1-indexed page numbers
    - Returns `has_next` flag for pagination UI
    
    **Sorting:**
    - Sorted by generation time (newest first)
    - Vietnamese timezone (Asia/Ho_Chi_Minh)
    
    **Response includes:**
    - Total count across all pages
    - Current page metadata
    - Array of ROPA metadata objects
    - Download URLs for each document
    """,
    responses={
        200: {
            "description": "List retrieved successfully / Lấy danh sách thành công",
            "content": {
                "application/json": {
                    "example": {
                        "total": 25,
                        "items": [
                            {
                                "ropa_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                                "format": "pdf",
                                "language": "vi",
                                "generated_at": "2025-11-05T22:00:00+07:00",
                                "file_size_bytes": 26209,
                                "entry_count": 5
                            }
                        ],
                        "page": 1,
                        "page_size": 20,
                        "has_next": True
                    }
                }
            }
        }
    }
)
async def list_ropa_documents(
    tenant_id: UUID = PathParam(
        ...,
        description="Tenant UUID / UUID của tenant",
        example="550e8400-e29b-41d4-a716-446655440000"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Page number (1-indexed) / Số trang (bắt đầu từ 1)",
        example=1
    ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
        description="Items per page (max 100) / Số mục mỗi trang (tối đa 100)",
        example=20
    )
) -> ROPAListResponse:
    """
    **List ROPA Documents with Pagination**
    
    Returns paginated list of all ROPA documents for a tenant.
    
    **Pagination Example:**
    - Page 1: Items 1-20 (if page_size=20)
    - Page 2: Items 21-40
    - Page 3: Items 41-60
    
    **Filtering:** (Future enhancement)
    - By format (JSON, CSV, PDF, MPS)
    - By language (Vietnamese, English)
    - By date range
    - By MPS compliance status
    """
    try:
        items, total = ropa_service.list_ropa_documents(
            tenant_id=tenant_id,
            page=page,
            page_size=page_size
        )
        
        has_next = (page * page_size) < total
        
        return ROPAListResponse(
            total=total,
            items=items,
            page=page,
            page_size=page_size,
            has_next=has_next
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "ListFailed",
                "message": f"Failed to list ROPA documents: {str(e)}",
                "message_vi": f"Liệt kê tài liệu ROPA thất bại: {str(e)}"
            }
        )


@router.delete(
    "/{ropa_id}",
    response_model=ROPADeleteResponse,
    summary="Delete ROPA Document / Xóa tài liệu ROPA",
    description="""
    Delete a ROPA document and all associated files.
    
    **Deletion Scope:**
    - Removes all format variations (JSON, CSV, PDF, MPS)
    - Deletes metadata file
    - Permanent deletion (no soft delete)
    - Cannot be undone
    
    **Use Cases:**
    - Remove outdated ROPA versions
    - Clean up test data
    - GDPR right to erasure compliance
    - Storage optimization
    
    **[WARNING] Warning:** This action cannot be undone. Ensure you have backups if needed.
    """,
    responses={
        200: {
            "description": "Document deleted successfully / Xóa tài liệu thành công",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "ROPA document deleted successfully",
                        "deleted_at": "2025-11-05T22:05:00+07:00"
                    }
                }
            }
        },
        404: {"description": "ROPA document not found / Không tìm thấy tài liệu ROPA"}
    }
)
async def delete_ropa(
    tenant_id: UUID = PathParam(
        ...,
        description="Tenant UUID / UUID của tenant",
        example="550e8400-e29b-41d4-a716-446655440000"
    ),
    ropa_id: UUID = PathParam(
        ...,
        description="ROPA document UUID to delete / UUID của tài liệu ROPA cần xóa",
        example="7c9e6679-7425-40de-944b-e07fc1f90ae7"
    )
) -> ROPADeleteResponse:
    """
    **Delete ROPA Document Permanently**
    
    Deletes ROPA document file, all format variations, and metadata.
    
    **Vietnamese Timezone:**
    Deletion timestamp returned in Asia/Ho_Chi_Minh timezone.
    
    **Audit Trail:**
    Consider logging deletion events for compliance purposes
    before calling this endpoint.
    """
    try:
        deleted = ropa_service.delete_ropa(tenant_id, ropa_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ROPANotFound",
                    "message": f"ROPA document not found: {ropa_id}",
                    "message_vi": f"Không tìm thấy tài liệu ROPA: {ropa_id}"
                }
            )
        
        return ROPADeleteResponse(
            success=True,
            message="ROPA document deleted successfully",
            deleted_at=ropa_service._get_vietnam_time()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "DeletionFailed",
                "message": f"Failed to delete ROPA: {str(e)}",
                "message_vi": f"Xóa ROPA thất bại: {str(e)}"
            }
        )


@router.get(
    "/preview",
    response_model=dict,
    summary="Preview ROPA Metadata / Xem trước thông tin ROPA",
    description="""
    Preview what will be included in a ROPA document **without generating it**.
    
    **Returns Preview Information:**
    - **entry_count:** Number of processing activities
    - **data_categories:** Unique data categories found
    - **has_sensitive_data:** Sensitive personal data detection
    - **has_cross_border_transfers:** Cross-border transfer presence
    - **compliance_checklist:** Vietnamese PDPL compliance status
    - **estimated_file_size_kb:** Approximate file size
    
    **Vietnamese PDPL Compliance Checklist:**
    - [OK] Controller information (Decree 13/2023/ND-CP Article 12.1.a)
    - [OK] DPO information (Article 12.1.b)
    - [OK] Legal basis for all processing
    - [OK] Retention periods defined
    - [OK] Security measures documented
    
    **Use Cases:**
    - Validate data before generation
    - Check compliance status
    - Estimate file size
    - Verify data categories included
    
    **[OK] Status:** FULLY IMPLEMENTED with database integration
    """,
    responses={
        200: {
            "description": "Preview generated successfully / Tạo preview thành công",
            "content": {
                "application/json": {
                    "example": {
                        "entry_count": 5,
                        "data_categories": ["Họ và tên", "Email", "Số điện thoại", "Địa chỉ"],
                        "has_sensitive_data": False,
                        "has_cross_border_transfers": True,
                        "compliance_checklist": {
                            "has_controller_info": True,
                            "has_dpo": True,
                            "has_legal_basis": True,
                            "has_retention_period": True,
                            "has_security_measures": True
                        },
                        "estimated_file_size_kb": 25
                    }
                }
            }
        },
        500: {"description": "Internal server error / Lỗi máy chủ nội bộ"}
    }
)
async def preview_ropa(
    tenant_id: UUID = PathParam(
        ...,
        description="Tenant UUID / UUID của tenant",
        example="550e8400-e29b-41d4-a716-446655440000"
    ),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    **Preview ROPA Metadata Without Generation**
    
    Check what will be included in the ROPA before generating the full document.
    
    **Compliance Validation:**
    - Controller information completeness
    - DPO (Data Protection Officer) presence
    - Legal basis for all activities
    - Retention periods defined
    - Security measures documented
    
    **Sensitive Data Detection:**
    Scans for keywords indicating sensitive personal data:
    - Health data (sức khỏe, y tế)
    - Biometric data (sinh trắc học)
    - Genetic data (di truyền)
    
    **Cross-Border Transfer Detection:**
    Identifies processing activities involving data transfers outside Vietnam.
    """
    try:
        # Get preview from database
        preview = await ropa_service.preview_ropa_from_database(
            db=db,
            tenant_id=tenant_id
        )
        
        return preview
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "PreviewFailed",
                "message": f"Preview generation failed: {str(e)}",
                "message_vi": f"Tạo preview thất bại: {str(e)}"
            }
        )


# Export router
__all__ = ['router']
