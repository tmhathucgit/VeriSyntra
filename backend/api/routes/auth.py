"""
Authentication Routes
Vietnamese Business Context: User authentication with multi-tenant support
PDPL 2025 Compliance: Secure authentication with bilingual error messages
"""

from datetime import datetime
from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_token_payload,
    InvalidTokenError
)
from auth.password_utils import validate_password_strength
from auth.schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserLoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    LogoutResponse,
    CurrentUserResponse
)
from auth.token_blacklist import token_blacklist
from database.crud.user_crud import UserCRUD
from database.session import get_db

# Create router
router = APIRouter()

# OAuth2 scheme for bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register new user - Đăng ký người dùng mới
    
    Vietnamese Business Context:
    - Multi-tenant: Requires valid tenant_id
    - Regional preferences: Supports north/central/south Vietnam
    - Vietnamese names: Supports full_name_vi with diacritics
    - Phone numbers: Vietnamese format
    
    PDPL 2025 Compliance:
    - Password strength validation
    - Bilingual error messages
    - Audit trail (created_at)
    
    Phase 2 Schema: Email-based authentication (no username)
    """
    # Check if email exists within tenant - Kiểm tra email đã tồn tại
    existing_email = UserCRUD.get_user_by_email(db, request.email, request.tenant_id)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Email already exists",
                "message_vi": "Email đã tồn tại",
                "error_code": "EMAIL_EXISTS"
            }
        )
    
    # Validate password strength - Xác thực độ mạnh mật khẩu
    is_valid, error = validate_password_strength(request.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": error,
                "message_vi": error.split(" | ")[0] if " | " in error else error,
                "error_code": "WEAK_PASSWORD"
            }
        )
    
    # Create user using Phase 2 signature - Tạo người dùng
    user = UserCRUD.create_user(
        db=db,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        full_name_vi=request.full_name_vi,
        phone_number=request.phone_number,
        tenant_id=request.tenant_id,
        regional_location=request.regional_location
    )
    
    return UserRegisterResponse(
        user_id=user.user_id,
        email=user.email,
        full_name=user.full_name,
        tenant_id=user.tenant_id,
        role=user.role,
        created_at=user.created_at
    )


@router.post("/login", response_model=UserLoginResponse)
async def login_user(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    User login - Đăng nhập người dùng
    
    Returns: Access token (30 min) + Refresh token (7 days)
    
    Security:
    - Password verification with bcrypt
    - JWT token generation
    
    Vietnamese Context:
    - Email-based authentication (Phase 2)
    - Bilingual error messages
    """
    # Verify credentials using email - Xác thực thông tin đăng nhập
    user = UserCRUD.verify_user_password(db, request.email, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid email or password",
                "message_vi": "Email hoặc mật khẩu không đúng",
                "error_code": "INVALID_CREDENTIALS"
            }
        )
    
    # Check if account is active - Kiểm tra tài khoản hoạt động
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Account is inactive",
                "message_vi": "Tài khoản không hoạt động",
                "error_code": "ACCOUNT_INACTIVE"
            }
        )
    
    # Create JWT tokens - Tạo JWT tokens
    access_token = create_access_token(
        data={
            "user_id": str(user.user_id),
            "email": user.email,  # Use email as username for Phase 2
            "tenant_id": str(user.tenant_id),
            "role": user.role
        }
    )
    
    refresh_token = create_refresh_token(
        data={
            "user_id": str(user.user_id),
            "email": user.email  # Use email as username for Phase 2
        }
    )
    
    # Update last login - Cập nhật lần đăng nhập cuối
    UserCRUD.update_last_login(db, user.user_id)
    
    return UserLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user.to_dict(include_sensitive=False)
    )


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_access_token(
    request: TokenRefreshRequest
):
    """
    Refresh access token using refresh token - Làm mới access token
    
    Security:
    - Checks token blacklist for revoked tokens
    - Verifies refresh token signature and expiration
    - Generates new access token with same claims
    
    Vietnamese Context:
    - Bilingual error messages
    """
    # Check if refresh token is blacklisted - Kiểm tra token bị thu hồi
    if token_blacklist.is_blacklisted(request.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Refresh token has been revoked",
                "message_vi": "Refresh token đã bị thu hồi",
                "error_code": "TOKEN_REVOKED"
            }
        )
    
    # Verify refresh token - Xác thực refresh token
    try:
        payload = verify_token(request.refresh_token, expected_type="refresh")
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": str(e),
                "message_vi": "Refresh token không hợp lệ hoặc hết hạn",
                "error_code": "INVALID_REFRESH_TOKEN"
            }
        )
    
    # Create new access token - Tạo access token mới
    access_token = create_access_token(
        data={
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "tenant_id": payload.get("tenant_id"),
            "role": payload.get("role")
        }
    )
    
    return TokenRefreshResponse(
        access_token=access_token
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout_user(
    access_token: str = Depends(oauth2_scheme),
    refresh_token: str = Body(..., embed=True)
):
    """
    User logout - blacklist both tokens - Đăng xuất người dùng
    
    Security:
    - Adds both access and refresh tokens to Redis blacklist
    - Tokens remain blacklisted until their natural expiration
    - TTL prevents indefinite blacklist growth
    
    Vietnamese Context:
    - Bilingual success message
    """
    # Get token expiration times - Lấy thời gian hết hạn của token
    access_payload = get_token_payload(access_token)
    refresh_payload = get_token_payload(refresh_token)
    
    access_exp = access_payload.get("exp")
    refresh_exp = refresh_payload.get("exp")
    
    # Calculate TTL (time until expiration) - Tính thời gian còn lại
    now = datetime.utcnow().timestamp()
    
    access_ttl = int(access_exp - now) if access_exp > now else 0
    refresh_ttl = int(refresh_exp - now) if refresh_exp > now else 0
    
    # Add tokens to blacklist - Thêm token vào danh sách đen
    if access_ttl > 0:
        token_blacklist.add_token(access_token, expires_in_minutes=access_ttl // 60)
    
    if refresh_ttl > 0:
        token_blacklist.add_token(refresh_token, expires_in_minutes=refresh_ttl // 60)
    
    return LogoutResponse()


@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user_endpoint(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information - Lấy thông tin người dùng hiện tại
    
    Protected endpoint: Requires valid access token
    
    Vietnamese Context:
    - Returns user with Vietnamese name (full_name_vi with diacritics)
    - Multi-tenant: Returns tenant_id
    - Phase 2 schema: No regional_location field
    """
    return CurrentUserResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        full_name=current_user.full_name,
        tenant_id=current_user.tenant_id,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        last_login=current_user.last_login,
        created_at=current_user.created_at
    )
