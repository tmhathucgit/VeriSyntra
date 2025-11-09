from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import pytz
from app.core.vietnamese_cultural_intelligence import VietnameseCulturalIntelligence
from app.api.v1.endpoints import veriportal, vericompliance, admin_companies, veriaidpo_classification
from api.routes.auth import router as auth_router
from database.base import Base
from database.session import engine
from loguru import logger
import sys

# Configure logging with Vietnam timezone
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>VeriSyntra</cyan> | {message}",
    level="INFO"
)

# Initialize FastAPI app with enhanced Vietnamese business metadata
app = FastAPI(
    title="VeriSyntra Vietnamese DPO Compliance Platform",
    description="""
    ## Nền tảng tuân thủ PDPL 2025 cho doanh nghiệp Việt Nam | Vietnamese PDPL 2025 Compliance Platform
    
    Professional data protection compliance solution with Vietnamese cultural intelligence.
    
    **Tính năng chính | Key Features:**
    - Xác thực người dùng đa thuê bao | Multi-tenant user authentication
    - Quản lý tuân thủ PDPL 2025 | PDPL 2025 compliance management
    - Trí tuệ văn hóa Việt Nam | Vietnamese cultural intelligence
    - Phân loại dữ liệu AI | AI-powered data classification
    
    **Bảo mật | Security:**
    - JWT token authentication (OAuth2 Password Bearer)
    - Mã hóa mật khẩu bcrypt | Bcrypt password hashing
    - Khóa tài khoản tự động | Automatic account lockout
    - Danh sách đen token | Token blacklist
    """,
    version="1.0.0-prototype",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Xác thực người dùng | User authentication endpoints with JWT tokens"
        },
        {
            "name": "VeriPortal",
            "description": "Cổng thông tin VeriPortal | VeriPortal compliance modules"
        },
        {
            "name": "VeriCompliance",
            "description": "Tuân thủ PDPL | PDPL compliance management"
        },
        {
            "name": "Admin - Company Registry",
            "description": "Quản lý công ty | Company registry administration"
        },
        {
            "name": "VeriAIDPO Classification",
            "description": "Phân loại dữ liệu AI | AI-powered data classification"
        }
    ]
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

# Startup event: Create database tables
@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on startup - Khởi tạo bảng cơ sở dữ liệu khi khởi động
    
    Creates all tables defined in SQLAlchemy models if they don't exist.
    Uses Base metadata from database.base module.
    """
    logger.info("Database initialization: Creating tables if not exist")
    logger.info("Khởi tạo cơ sở dữ liệu: Tạo bảng nếu chưa tồn tại")
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("[OK] Database tables created successfully")
        logger.info("[OK] Các bảng cơ sở dữ liệu đã được tạo thành công")
    except Exception as e:
        logger.error(f"[ERROR] Database initialization failed: {e}")
        logger.error(f"[ERROR] Khởi tạo cơ sở dữ liệu thất bại: {e}")
        logger.warning("[WARNING] Server starting without database - some endpoints may not work")
        logger.warning("[WARNING] Máy chủ khởi động mà không có cơ sở dữ liệu - một số endpoint có thể không hoạt động")

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

# Include API routes with authentication first
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(veriportal.router, prefix="/api/v1/veriportal", tags=["VeriPortal"])
app.include_router(vericompliance.router, prefix="/api/v1/vericompliance", tags=["VeriCompliance"])
app.include_router(admin_companies.router, prefix="/api/v1", tags=["Admin - Company Registry"])
app.include_router(veriaidpo_classification.router, prefix="/api/v1", tags=["VeriAIDPO Classification"])

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
    logger.info("Starting VeriSyntra Vietnamese DPO Compliance Platform")
    logger.info("Vietnamese Cultural Intelligence: Active")
    logger.info("Authentication System: JWT OAuth2 Password Bearer")
    logger.info("API Documentation: http://127.0.0.1:8000/docs")
    logger.info("Khởi động VeriSyntra - Nền tảng tuân thủ PDPL 2025")
    
    uvicorn.run(
        "main_prototype:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )