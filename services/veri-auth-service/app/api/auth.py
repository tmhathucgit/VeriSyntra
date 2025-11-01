# ============================================
# VeriSyntra Auth Service - Authentication API
# ============================================
# Vietnamese PDPL 2025 Compliance Platform
# Authentication endpoints: login, register, refresh, verify
# ============================================

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from uuid import UUID
from datetime import datetime
import pytz
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import (
    VeriUserCreate,
    VeriUserLogin,
    VeriUserResponse,
    VeriPasswordChange
)
from app.models.tenant import VeriTenantCreate, VeriRegionalLocation
from app.core.security import (
    verify_password,
    create_token_response,
    verify_token,
    get_current_user
)
from app.core.database import get_db
from app.core import crud

router = APIRouter()


# ============================================
# Registration Endpoint
# ============================================

@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def register_user(user_data: VeriUserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register new Vietnamese business user
    
    Creates new user account and tenant (if not exists)
    Supports Vietnamese company registration
    """
    # Check if email already exists
    existing_user = await crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Email da ton tai / Email already exists",
                "english": "Email already exists"
            }
        )
    
    # Create or get tenant
    tenant_id = user_data.tenant_id
    if not tenant_id:
        # Create new tenant
        tenant_create = VeriTenantCreate(
            company_name=user_data.company_name or f"Company of {user_data.full_name}",
            company_name_vi=user_data.company_name or f"Cong ty cua {user_data.full_name_vi or user_data.full_name}",
            veri_regional_location=user_data.veri_regional_location or VeriRegionalLocation.SOUTH,
            veri_industry_type="technology",
            subscription_tier="starter"
        )
        tenant = await crud.create_tenant(db, tenant_create)
        tenant_id = tenant.tenant_id
    else:
        # Verify tenant exists
        tenant = await crud.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Doanh nghiep khong ton tai / Tenant not found",
                    "english": "Tenant not found"
                }
            )
    
    # Create user (first user is admin)
    user_count = await crud.count_tenant_users(db, tenant_id)
    role = "admin" if user_count == 0 else "staff"
    
    user = await crud.create_user(db, user_data, tenant_id, role)
    
    await db.commit()
    
    return {
        "message": "Dang ky thanh cong / Registration successful",
        "english": "Registration successful",
        "user_id": str(user.user_id),
        "tenant_id": str(tenant_id),
        "email": user.email,
        "verification_required": True,
        "next_steps": {
            "vi": "Vui long xac thuc email de kich hoat tai khoan",
            "en": "Please verify your email to activate your account"
        }
    }


# ============================================
# Login Endpoint
# ============================================

@router.post("/login", response_model=Dict[str, Any])
async def login_user(login_data: VeriUserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate Vietnamese user with multi-tenant context
    
    Returns JWT access token and refresh token
    """
    # Find user by email
    user = await crud.get_user_by_email(db, login_data.email, login_data.tenant_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Email hoac mat khau khong dung / Invalid email or password",
                "english": "Invalid email or password"
            }
        )
    
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Email hoac mat khau khong dung / Invalid email or password",
                "english": "Invalid email or password"
            }
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Tai khoan da bi vo hieu hoa / Account is inactive",
                "english": "Account is inactive"
            }
        )
    
    # Update last login
    await crud.update_user_last_login(db, user.user_id)
    await db.commit()
    
    # Get tenant information for business context
    tenant = await crud.get_tenant_by_id(db, user.tenant_id)
    veri_business_context = {
        "veriBusinessId": str(tenant.tenant_id) if tenant else None,
        "veriRegionalLocation": tenant.veri_regional_location if tenant else "south",
        "veriIndustryType": tenant.veri_industry_type if tenant else "technology",
        "veriSubscriptionTier": tenant.subscription_tier if tenant else "starter"
    }
    
    # Create tokens
    token_response = create_token_response(
        user_id=user.user_id,
        email=user.email,
        tenant_id=user.tenant_id,
        role=user.role,
        full_name=user.full_name,
        is_active=user.is_active,
        veri_business_context=veri_business_context
    )
    
    return {
        **token_response,
        "message": "Dang nhap thanh cong / Login successful",
        "english": "Login successful",
        "vietnam_time": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()
    }


# ============================================
# Refresh Token Endpoint
# ============================================

@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_access_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Refresh JWT access token using refresh token
    """
    try:
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        user_id = payload.get("sub")
        
        # Get user from database
        user = await crud.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "Nguoi dung khong ton tai / User not found",
                    "english": "User not found"
                }
            )
        
        # Get tenant information
        tenant = await crud.get_tenant_by_id(db, user.tenant_id)
        veri_business_context = {
            "veriBusinessId": str(tenant.tenant_id) if tenant else None,
            "veriRegionalLocation": tenant.veri_regional_location if tenant else "south",
            "veriIndustryType": tenant.veri_industry_type if tenant else "technology"
        }
        
        # Create new tokens
        token_response = create_token_response(
            user_id=user.user_id,
            email=user.email,
            tenant_id=user.tenant_id,
            role=user.role,
            full_name=user.full_name,
            is_active=user.is_active,
            veri_business_context=veri_business_context
        )
        
        return {
            **token_response,
            "message": "Token da duoc cap nhat / Token refreshed",
            "english": "Token refreshed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Khong the cap nhat token / Could not refresh token",
                "english": "Could not refresh token",
                "error": str(e)
            }
        )


# ============================================
# Get Current User Profile
# ============================================

@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_profile(current_user: Dict[str, Any] = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Get current authenticated user profile with Vietnamese business context
    """
    user_id = current_user.get("user_id")
    user = await crud.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Nguoi dung khong ton tai / User not found",
                "english": "User not found"
            }
        )
    
    # Get tenant information
    tenant = await crud.get_tenant_by_id(db, user.tenant_id)
    
    return {
        "user": {
            "user_id": str(user.user_id),
            "email": user.email,
            "full_name": user.full_name,
            "full_name_vi": user.full_name_vi,
            "phone_number": user.phone_number,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "preferred_language": user.preferred_language,
            "timezone": user.timezone,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None
        },
        "tenant": {
            "tenant_id": str(tenant.tenant_id) if tenant else None,
            "company_name": tenant.company_name if tenant else None,
            "company_name_vi": tenant.company_name_vi if tenant else None,
            "veri_regional_location": tenant.veri_regional_location if tenant else None,
            "veri_industry_type": tenant.veri_industry_type if tenant else None,
            "subscription_tier": tenant.subscription_tier if tenant else None
        },
        "veri_business_context": {
            "veriBusinessId": str(tenant.tenant_id) if tenant else None,
            "veriRegionalLocation": tenant.veri_regional_location if tenant else None,
            "veriIndustryType": tenant.veri_industry_type if tenant else None
        }
    }


# ============================================
# Change Password Endpoint
# ============================================

@router.post("/change-password", response_model=Dict[str, Any])
async def change_user_password(
    password_data: VeriPasswordChange,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change user password (Vietnamese language support)
    """
    user_id = current_user.get("user_id")
    user = await crud.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Nguoi dung khong ton tai / User not found",
                "english": "User not found"
            }
        )
    
    # Verify old password
    if not verify_password(password_data.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Mat khau hien tai khong dung / Current password is incorrect",
                "english": "Current password is incorrect"
            }
        )
    
    # Update new password in database
    await crud.update_user_password(db, user_id, password_data.new_password)
    await db.commit()
    
    return {
        "message": "Mat khau da duoc thay doi thanh cong / Password changed successfully",
        "english": "Password changed successfully",
        "success": True
    }


# ============================================
# Health Check
# ============================================

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Vietnamese auth service health check"""
    # Count users and tenants from database
    from sqlalchemy import select, func
    from app.core.db_models import UserDB, TenantDB
    
    users_count = await db.scalar(select(func.count()).select_from(UserDB))
    tenants_count = await db.scalar(select(func.count()).select_from(TenantDB))
    
    return {
        "status": "healthy",
        "service": "veri-auth-service",
        "message": "Dich vu xac thuc VeriSyntra hoat dong binh thuong",
        "english": "VeriSyntra auth service operational",
        "users_count": users_count or 0,
        "tenants_count": tenants_count or 0,
        "vietnam_time": datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat()
    }
