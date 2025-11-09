"""
Health check endpoint for VeriAIDPO service
"""
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for VeriAIDPO service"""
    return {
        "status": "healthy",
        "service": "VeriAIDPO Classification Service"
    }
