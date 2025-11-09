"""
FastAPI Security Dependencies
Vietnamese Business Context: Multi-tenant user authentication
PDPL 2025 Compliance: Secure token verification with bilingual error messages
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.jwt_handler import verify_token, InvalidTokenError
from auth.token_blacklist import TokenBlacklist, token_blacklist
from database.crud.user_crud import UserCRUD
from database.session import get_db

# OAuth2 scheme for bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_token_blacklist() -> TokenBlacklist:
    """Dependency to get global token blacklist instance"""
    return token_blacklist


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    blacklist: TokenBlacklist = Depends(get_token_blacklist)
):
    """
    Get current authenticated user from access token - Lấy người dùng hiện tại từ token
    
    Security checks:
    1. Token is not blacklisted (not revoked during logout)
    2. Token is valid and not expired
    3. Token type is 'access' (not refresh token)
    4. User exists in database
    5. User is active
    
    Vietnamese Context:
    - Returns user with tenant_id for multi-tenant filtering
    - Returns regional_location for business context
    - Bilingual error messages
    
    PDPL 2025 Compliance:
    - Secure token verification
    - Audit trail (last_login_at in user object)
    
    Args:
        token: Bearer token from Authorization header
        db: Database session
        blacklist: Token blacklist for revoked tokens
        
    Returns:
        User object from database
        
    Raises:
        HTTPException: 401 if token invalid/revoked, 403 if user inactive
    """
    # Check if token is blacklisted - Kiểm tra token bị thu hồi
    if blacklist.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token has been revoked",
                "message_vi": "Token đã bị thu hồi",
                "error_code": "TOKEN_REVOKED"
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verify token - Xác thực token
    try:
        payload = verify_token(token, expected_type="access")
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": str(e),
                "message_vi": "Token không hợp lệ hoặc hết hạn",
                "error_code": "INVALID_TOKEN"
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user from database - Lấy người dùng từ cơ sở dữ liệu
    user_id = payload.get("user_id")
    user = UserCRUD.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "User not found",
                "message_vi": "Người dùng không tồn tại",
                "error_code": "USER_NOT_FOUND"
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Check if user is active - Kiểm tra người dùng hoạt động
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "User account is inactive",
                "message_vi": "Tài khoản người dùng không hoạt động",
                "error_code": "USER_INACTIVE"
            }
        )
    
    return user
