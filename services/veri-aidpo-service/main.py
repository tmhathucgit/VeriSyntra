"""
VeriAIDPO Classification Service
Main FastAPI application entry point

Vietnamese PDPL 2025 AI-powered data classification microservice
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from loguru import logger

from app.config import settings
from app.api.v1.endpoints import classification
from app.auth.jwt_validator import validate_token
from app.auth.permissions import require_permission

app = FastAPI(
    title=settings.service_name,
    version=settings.service_version,
    description="Vietnamese PDPL 2025 AI-powered data classification microservice with JWT authentication"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(classification.router, tags=["Classification"])

# Custom OpenAPI schema with JWT Bearer authentication
def custom_openapi():
    """Custom OpenAPI schema with JWT Bearer security"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.service_name,
        version=settings.service_version,
        description="Vietnamese PDPL 2025 AI-powered data classification microservice with JWT authentication",
        routes=app.routes,
    )
    
    # Add JWT Bearer security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token from main backend authentication"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    """Root endpoint - Service information"""
    return {
        "service": settings.service_name,
        "version": settings.service_version,
        "status": "running",
        "description": "Vietnamese PDPL 2025 AI-powered data classification"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.service_name,
        "version": settings.service_version
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.service_name} on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)
