"""
VeriSyntra Data Inventory Main Application

FastAPI application initialization with Vietnamese business context support.
All configuration uses dynamic values - zero hard-coding.

Features:
- CORS support for frontend integration
- API versioning
- OpenAPI documentation
- Background task management
- Startup/shutdown event handlers
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import dynamic configuration
try:
    from .config.constants import APIConfig
    from .api.scan_endpoints import router as scan_router
    from .services.job_state_manager import get_job_state_manager
except ImportError:
    from config.constants import APIConfig
    from api.scan_endpoints import router as scan_router
    from services.job_state_manager import get_job_state_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    
    Startup:
    - Initialize job state manager
    - Log configuration summary
    
    Shutdown:
    - Cleanup expired jobs
    - Log shutdown status
    """
    # Startup
    logger.info("[OK] VeriSyntra Data Inventory API starting...")
    logger.info(f"[OK] API Version: {APIConfig.API_VERSION}")
    logger.info(f"[OK] API Prefix: {APIConfig.API_PREFIX}")
    logger.info(f"[OK] Max concurrent requests: {APIConfig.MAX_CONCURRENT_REQUESTS}")
    logger.info(f"[OK] Task retention: {APIConfig.TASK_RETENTION_HOURS}h")
    
    # Initialize job state manager
    job_manager = get_job_state_manager()
    stats = job_manager.get_statistics()
    logger.info(f"[OK] Job state manager initialized: {stats['total_jobs']} jobs")
    
    yield
    
    # Shutdown
    logger.info("[OK] VeriSyntra Data Inventory API shutting down...")
    
    # Cleanup expired jobs
    cleaned_count = job_manager.cleanup_expired_jobs()
    logger.info(f"[OK] Cleaned up {cleaned_count} expired jobs")
    logger.info("[OK] Shutdown complete")


# Create FastAPI application with dynamic configuration
app = FastAPI(
    title="VeriSyntra Data Inventory API",
    description="""
    Vietnamese PDPL 2025 Compliance Platform - Data Discovery & Scanning API
    
    Features:
    - Multi-source data discovery (databases, cloud storage, filesystems)
    - Vietnamese UTF-8 text support
    - Column filtering for cost optimization
    - Vietnamese regional business context awareness
    - PDPL 2025 compliance scanning
    
    Regional Support:
    - North Vietnam (Hanoi): Formal, thorough documentation
    - South Vietnam (HCMC): Entrepreneurial, efficiency-focused
    - Central Vietnam (Da Nang/Hue): Traditional, consensus-building
    """,
    version=APIConfig.API_VERSION,  # Use config, not "1.0.0"
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware with dynamic configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=APIConfig.CORS_ALLOW_ORIGINS,  # Use config
    allow_credentials=True,
    allow_methods=APIConfig.CORS_ALLOW_METHODS,  # Use config
    allow_headers=APIConfig.CORS_ALLOW_HEADERS,  # Use config
)

# Include routers
app.include_router(scan_router)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    API root endpoint
    
    Returns basic API information and links to documentation.
    """
    return {
        "name": "VeriSyntra Data Inventory API",
        "version": APIConfig.API_VERSION,
        "description": "Vietnamese PDPL 2025 Compliance Platform - Data Discovery & Scanning",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_spec": "/openapi.json"
        },
        "endpoints": {
            "scan": f"{APIConfig.API_PREFIX}/scan",
            "status": f"{APIConfig.API_PREFIX}/scans/{{scan_job_id}}",
            "cancel": f"{APIConfig.API_PREFIX}/scans/{{scan_job_id}}",
            "filter_templates": f"{APIConfig.API_PREFIX}/filter-templates",
            "health": f"{APIConfig.API_PREFIX}/health"
        },
        "regional_support": [
            "North Vietnam (Hanoi): Formal, government-focused",
            "South Vietnam (HCMC): Entrepreneurial, international",
            "Central Vietnam (Da Nang/Hue): Traditional, consensus-driven"
        ]
    }


# Development server entry point
if __name__ == "__main__":
    import uvicorn
    
    logger.info("[OK] Starting development server...")
    logger.info(f"[OK] API will be available at: http://localhost:8000{APIConfig.API_PREFIX}")
    logger.info(f"[OK] Swagger UI: http://localhost:8000/docs")
    logger.info(f"[OK] ReDoc: http://localhost:8000/redoc")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
