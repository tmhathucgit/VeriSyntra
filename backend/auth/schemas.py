"""
Authentication Pydantic Schemas
Vietnamese Business Context: Bilingual validation messages
PDPL 2025 Compliance: Secure data validation
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# User Registration Schemas

class UserRegisterRequest(BaseModel):
    """User registration request - Yêu cầu đăng ký người dùng"""
    email: EmailStr = Field(..., description="Địa chỉ email | Email address")
    password: str = Field(..., min_length=8, description="Mật khẩu | Password")
    full_name: str = Field(..., min_length=2, max_length=255, description="Họ tên | Full name")
    full_name_vi: Optional[str] = Field(None, min_length=2, max_length=255, description="Họ tên tiếng Việt | Vietnamese name")
    phone_number: Optional[str] = Field(None, description="Số điện thoại | Phone number")
    tenant_id: UUID = Field(..., description="Mã tổ chức | Tenant ID")
    regional_location: Optional[str] = Field(None, description="Khu vực | Regional location")
    
    @field_validator('regional_location')
    @classmethod
    def validate_regional_location(cls, v):
        """Validate regional location - Xác thực khu vực"""
        if v and v not in ['north', 'central', 'south']:
            raise ValueError(
                "Khu vực không hợp lệ. Chỉ chấp nhận: north, central, south | "
                "Invalid regional location. Only accepts: north, central, south"
            )
        return v


class UserRegisterResponse(BaseModel):
    """User registration response - Phản hồi đăng ký người dùng"""
    user_id: UUID
    email: str
    full_name: str
    tenant_id: UUID
    role: str
    created_at: datetime
    message: str = "Đăng ký thành công | Registration successful"
    message_vi: str = "Đăng ký thành công"


# User Login Schemas

class UserLoginRequest(BaseModel):
    """User login request - Yêu cầu đăng nhập"""
    email: EmailStr = Field(..., description="Địa chỉ email | Email address")
    password: str = Field(..., description="Mật khẩu | Password")


class UserLoginResponse(BaseModel):
    """User login response with tokens - Phản hồi đăng nhập với token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds
    user: dict
    message: str = "Đăng nhập thành công | Login successful"
    message_vi: str = "Đăng nhập thành công"


# Token Refresh Schemas

class TokenRefreshRequest(BaseModel):
    """Token refresh request - Yêu cầu làm mới token"""
    refresh_token: str = Field(..., description="Mã refresh token | Refresh token")


class TokenRefreshResponse(BaseModel):
    """Token refresh response - Phản hồi làm mới token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800
    message: str = "Làm mới token thành công | Token refreshed successfully"
    message_vi: str = "Làm mới token thành công"


# Logout Schema

class LogoutResponse(BaseModel):
    """Logout response - Phản hồi đăng xuất"""
    message: str = "Đăng xuất thành công | Logout successful"
    message_vi: str = "Đăng xuất thành công"


# Current User Schema

class CurrentUserResponse(BaseModel):
    """Current user information - Thông tin người dùng hiện tại"""
    user_id: UUID
    email: str
    full_name: str
    tenant_id: UUID
    role: str
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime


# Error Response Schema

class ErrorResponse(BaseModel):
    """Standard error response (bilingual) - Phản hồi lỗi chuẩn (song ngữ)"""
    message: str
    message_vi: str
    error_code: str
    details: Optional[dict] = None
