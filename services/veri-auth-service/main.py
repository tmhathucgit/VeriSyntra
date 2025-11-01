# ============================================
# VeriSyntra Authentication Service
# ============================================
# Vietnamese PDPL 2025 Compliance Platform
# Multi-tenant authentication microservice
# Port: 8001
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import os

from app.api import auth

# Initialize FastAPI app
app = FastAPI(
    title="VeriSyntra Authentication Service",
    description="Multi-tenant authentication for Vietnamese PDPL 2025 compliance platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",  # Main monolith
        os.getenv("FRONTEND_URL", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

# Root endpoint
@app.get("/")
async def root():
    """Vietnamese auth service welcome"""
    vn_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    return {
        "service": "veri-auth-service",
        "message": "Dich vu xac thuc VeriSyntra - Vietnamese PDPL 2025",
        "english": "VeriSyntra Authentication Service - Vietnamese PDPL 2025",
        "status": "operational",
        "vietnam_time": vn_time.isoformat(),
        "api_docs": "/docs",
        "endpoints": {
            "register": "POST /api/v1/auth/register",
            "login": "POST /api/v1/auth/login",
            "refresh": "POST /api/v1/auth/refresh",
            "me": "GET /api/v1/auth/me",
            "change_password": "POST /api/v1/auth/change-password",
            "health": "GET /api/v1/auth/health"
        }
    }

# Global health check
@app.get("/health")
async def global_health():
    """Service health monitoring"""
    return {
        "status": "healthy",
        "service": "veri-auth-service",
        "timestamp": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat(),
        "components": {
            "api": "operational",
            "vietnamese_locale": "configured",
            "jwt_auth": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
