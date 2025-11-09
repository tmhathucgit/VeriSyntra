"""
Test Swagger UI Documentation for ROPA API Endpoints

Run this to verify the enhanced OpenAPI documentation at /docs

Usage:
    python test_swagger_ui.py
    Then open: http://localhost:8000/docs
"""

from fastapi import FastAPI
from api.ropa_endpoints import router

# Create FastAPI app
app = FastAPI(
    title="VeriSyntra ROPA Generation API",
    description="""
    Vietnamese PDPL 2025 Compliance - Record of Processing Activities (ROPA) Generation
    
    [OK] All endpoints enhanced with bilingual Swagger UI documentation
    [OK] Supports 4 export formats: JSON, CSV, PDF, MPS
    [OK] Vietnamese business context integration
    
    Legal Framework:
    - Personal Data Protection Law (PDPL) 2025
    - Decree 13/2023/ND-CP
    - MPS Circular 09/2024/TT-BCA
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount ROPA router
app.include_router(router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "VeriSyntra ROPA API - Visit /docs for Swagger UI",
        "version": "1.0.0",
        "endpoints": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "ropa_api": "/api/v1/data-inventory/{tenant_id}/ropa"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("[OK] Starting Swagger UI test server...")
    print("[OK] Swagger UI: http://localhost:8000/docs")
    print("[OK] ReDoc: http://localhost:8000/redoc")
    print("[OK] Health check: http://localhost:8000/")
    print("")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
