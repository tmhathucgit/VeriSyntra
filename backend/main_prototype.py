from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import pytz
from app.core.vietnamese_cultural_intelligence import VietnameseCulturalIntelligence
from app.api.v1.endpoints import veriportal, vericompliance
from loguru import logger
import sys

# Configure logging with Vietnam timezone
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>VeriSyntra</cyan> | {message}",
    level="INFO"
)

# Initialize FastAPI app
app = FastAPI(
    title="VeriSyntra Vietnamese DPO Compliance Platform",
    description="Professional Vietnamese PDPL 2025 Compliance Solution",
    version="1.0.0-prototype",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Vietnamese Cultural Intelligence
cultural_ai = VietnameseCulturalIntelligence()

# Root endpoint with Vietnamese welcome
@app.get("/")
async def root():
    """Vietnamese welcome endpoint with cultural context"""
    vn_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    return {
        "message": "Chào mừng đến với VeriSyntra - Nền tảng tuân thủ PDPL 2025 cho doanh nghiệp Việt Nam",
        "english": "Welcome to VeriSyntra - Vietnamese PDPL 2025 Compliance Platform",
        "status": "operational",
        "vietnam_time": vn_time.isoformat(),
        "cultural_context": "vietnamese_business_platform",
        "api_docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health monitoring"""
    return {
        "status": "healthy",
        "service": "VeriSyntra Vietnamese DPO Platform",
        "timestamp": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat(),
        "components": {
            "cultural_ai": "active",
            "api_endpoints": "operational",
            "vietnamese_locale": "configured"
        }
    }

# Include API routes
app.include_router(veriportal.router, prefix="/api/v1/veriportal", tags=["VeriPortal"])
app.include_router(vericompliance.router, prefix="/api/v1/vericompliance", tags=["VeriCompliance"])

# Global exception handler with Vietnamese context
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Vietnamese platform error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Lỗi hệ thống VeriSyntra",
            "english": "VeriSyntra system error",
            "error_type": type(exc).__name__,
            "support": "Vui lòng liên hệ hỗ trợ kỹ thuật"
        }
    )

if __name__ == "__main__":
    logger.info("🚀 Starting VeriSyntra Vietnamese DPO Compliance Platform")
    logger.info("🇻🇳 Vietnamese Cultural Intelligence: Active")
    logger.info("📊 API Documentation: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        "main_prototype:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )