from fastapi import APIRouter, HTTPException
from datetime import datetime
import pytz

router = APIRouter()

@router.get("/")
async def veriportal_info():
    """VeriPortal user management information"""
    return {
        "module": "VeriPortal",
        "description": "Quản lý người dùng và quyền truy cập cho doanh nghiệp Việt Nam",
        "english": "User management and access control for Vietnamese enterprises",
        "features": [
            "Vietnamese business user authentication",
            "Role-based access control with cultural context",
            "PDPL 2025 compliant user data handling",
            "Regional business practice integration"
        ],
        "status": "active",
        "vietnam_time": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()
    }

@router.get("/dashboard")
async def vietnamese_business_dashboard():
    """Vietnamese business dashboard data"""
    return {
        "dashboard": "Vietnamese Business Dashboard",
        "vietnamese": "Bảng điều khiển doanh nghiệp Việt Nam",
        "data": {
            "total_users": 150,
            "active_sessions": 23,
            "compliance_status": "Đang tuân thủ PDPL 2025",
            "last_assessment": "2024-10-03",
            "regional_distribution": {
                "northern_vietnam": 45,
                "southern_vietnam": 78,
                "central_vietnam": 27
            }
        },
        "cultural_insights": {
            "primary_business_regions": ["Hà Nội", "Thành phố Hồ Chí Minh", "Đà Nẵng"],
            "business_hours": "08:00 - 17:30 (GMT+7)",
            "preferred_communication": "Vietnamese language"
        },
        "timestamp": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()
    }