"""
JWT Token Handler for VeriSyntra Authentication

Handles JWT access token and refresh token generation and validation for
Vietnamese PDPL 2025 compliance platform with bilingual support.

Coding Standards:
- No hard-coded values (all from settings)
- Type hints on all functions
- Bilingual error messages (Vietnamese + English)
- ASCII-only status indicators
- Comprehensive logging

Vietnamese: Xử lý mã thông báo JWT cho xác thực VeriSyntra
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from loguru import logger

from config.settings import settings


# Token type constants - Hằng số loại mã thông báo
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

# Token issuer - Tổ chức phát hành mã thông báo
TOKEN_ISSUER = "verisyntra-api"


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token for Vietnamese business user.
    
    Generates a short-lived access token for API authentication with
    Vietnamese business context (tenant_id, regional_location, etc.).
    
    Args:
        data: Token payload dictionary containing:
            - user_id (str): User unique identifier
            - tenant_id (str): Vietnamese business tenant ID
            - email (str): User email address
            - role (str): User role (dpo, admin, viewer, etc.)
            - veri_regional_location (str, optional): north, central, south
        expires_delta: Custom expiration timedelta (default: from settings)
    
    Returns:
        Encoded JWT access token string
    
    Example:
        >>> token = create_access_token({
        ...     "user_id": "user_123",
        ...     "tenant_id": "tenant_vn_001",
        ...     "email": "dpo@company.vn",
        ...     "role": "dpo",
        ...     "veri_regional_location": "south"
        ... })
    
    Vietnamese:
        Tạo mã thông báo truy cập JWT cho người dùng doanh nghiệp Việt Nam.
    """
    to_encode = data.copy()
    
    # Calculate expiration time - Tính toán thời gian hết hạn
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Add standard JWT claims - Thêm các yêu cầu JWT tiêu chuẩn
    to_encode.update({
        "exp": expire,  # Expiration time - Thời gian hết hạn
        "iat": datetime.utcnow(),  # Issued at - Thời gian phát hành
        "type": TOKEN_TYPE_ACCESS,  # Token type - Loại mã thông báo
        "iss": TOKEN_ISSUER,  # Issuer - Tổ chức phát hành
        "sub": data.get("user_id")  # Subject (user_id) - JWT standard claim
    })
    
    # Encode token - Mã hóa mã thông báo
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    user_id = data.get("user_id", "unknown")
    tenant_id = data.get("tenant_id", "unknown")
    logger.info(
        f"[OK] Access token created -> "
        f"User: {user_id}, Tenant: {tenant_id}, "
        f"Expires: {settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES} minutes"
    )
    
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token for Vietnamese business user.
    
    Generates a long-lived refresh token for obtaining new access tokens
    without re-authentication. Contains minimal data for security.
    
    Args:
        data: Token payload dictionary containing:
            - user_id (str): User unique identifier
            - tenant_id (str): Vietnamese business tenant ID
        expires_delta: Custom expiration timedelta (default: from settings)
    
    Returns:
        Encoded JWT refresh token string
    
    Example:
        >>> token = create_refresh_token({
        ...     "user_id": "user_123",
        ...     "tenant_id": "tenant_vn_001"
        ... })
    
    Vietnamese:
        Tạo mã thông báo làm mới JWT cho người dùng doanh nghiệp Việt Nam.
    """
    to_encode = data.copy()
    
    # Calculate expiration time - Tính toán thời gian hết hạn
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    # Add standard JWT claims - Thêm các yêu cầu JWT tiêu chuẩn
    to_encode.update({
        "exp": expire,  # Expiration time - Thời gian hết hạn
        "iat": datetime.utcnow(),  # Issued at - Thời gian phát hành
        "type": TOKEN_TYPE_REFRESH,  # Token type - Loại mã thông báo
        "iss": TOKEN_ISSUER,  # Issuer - Tổ chức phát hành
        "sub": data.get("user_id")  # Subject (user_id) - JWT standard claim
    })
    
    # Encode token - Mã hóa mã thông báo
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    user_id = data.get("user_id", "unknown")
    tenant_id = data.get("tenant_id", "unknown")
    logger.info(
        f"[OK] Refresh token created -> "
        f"User: {user_id}, Tenant: {tenant_id}, "
        f"Expires: {settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS} days"
    )
    
    return encoded_jwt


def verify_token(
    token: str,
    expected_type: str = TOKEN_TYPE_ACCESS
) -> Dict[str, Any]:
    """
    Verify and decode JWT token with Vietnamese bilingual error messages.
    
    Validates token signature, expiration, and type. Raises exceptions
    with bilingual error messages for Vietnamese business users.
    
    Args:
        token: JWT token string to verify
        expected_type: Expected token type ('access' or 'refresh')
    
    Returns:
        Decoded token payload dictionary
    
    Raises:
        InvalidTokenError: If token is invalid, expired, or wrong type
            (with bilingual Vietnamese + English error message)
    
    Example:
        >>> payload = verify_token(access_token, TOKEN_TYPE_ACCESS)
        >>> user_id = payload["user_id"]
        >>> tenant_id = payload["tenant_id"]
    
    Vietnamese:
        Xác minh và giải mã mã thông báo JWT với thông báo lỗi song ngữ.
    """
    try:
        # Decode and verify token signature - Giải mã và xác minh chữ ký
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verify token type - Xác minh loại mã thông báo
        token_type = payload.get("type")
        if token_type != expected_type:
            error_msg = (
                f"Wrong token type. Expected: {expected_type}, Got: {token_type} | "
                f"Loại mã thông báo sai. Mong đợi: {expected_type}, Nhận: {token_type}"
            )
            logger.warning(f"[ERROR] {error_msg}")
            raise InvalidTokenError(error_msg)
        
        # Verify issuer - Xác minh tổ chức phát hành
        issuer = payload.get("iss")
        if issuer != TOKEN_ISSUER:
            error_msg = (
                f"Invalid token issuer. Expected: {TOKEN_ISSUER}, Got: {issuer} | "
                f"Tổ chức phát hành không hợp lệ. Mong đợi: {TOKEN_ISSUER}, Nhận: {issuer}"
            )
            logger.warning(f"[ERROR] {error_msg}")
            raise InvalidTokenError(error_msg)
        
        user_id = payload.get("user_id", "unknown")
        logger.info(f"[OK] Token verified -> User: {user_id}, Type: {token_type}")
        return payload
        
    except ExpiredSignatureError:
        error_msg = (
            "Token expired. Please login again | "
            "Mã thông báo đã hết hạn. Vui lòng đăng nhập lại"
        )
        logger.warning(f"[ERROR] {error_msg}")
        raise InvalidTokenError(error_msg)
    
    except jwt.InvalidSignatureError:
        error_msg = (
            "Invalid token signature. Token may be tampered | "
            "Chữ ký mã thông báo không hợp lệ. Mã thông báo có thể bị giả mạo"
        )
        logger.warning(f"[ERROR] {error_msg}")
        raise InvalidTokenError(error_msg)
    
    except jwt.DecodeError:
        error_msg = (
            "Malformed token. Cannot decode | "
            "Mã thông báo không đúng định dạng. Không thể giải mã"
        )
        logger.warning(f"[ERROR] {error_msg}")
        raise InvalidTokenError(error_msg)
    
    except jwt.InvalidTokenError as e:
        error_msg = (
            f"Invalid token: {str(e)} | "
            f"Mã thông báo không hợp lệ: {str(e)}"
        )
        logger.warning(f"[ERROR] {error_msg}")
        raise InvalidTokenError(error_msg)


def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Extract payload from token without verification (for debugging only).
    
    WARNING: This function does NOT verify the token signature.
    Use only for debugging, logging, or inspection purposes.
    For authentication, always use verify_token().
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dictionary or None if token is malformed
    
    Example:
        >>> payload = get_token_payload(token)
        >>> if payload:
        ...     print(f"Token for user: {payload.get('user_id')}")
    
    Vietnamese:
        Trích xuất nội dung mã thông báo mà không xác minh (chỉ để gỡ lỗi).
    """
    try:
        # Decode without signature verification - Giải mã không xác minh chữ ký
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        
        user_id = payload.get("user_id", "unknown")
        token_type = payload.get("type", "unknown")
        logger.debug(
            f"[OK] Token payload extracted (unverified) -> "
            f"User: {user_id}, Type: {token_type}"
        )
        
        return payload
        
    except jwt.DecodeError as e:
        logger.error(
            f"[ERROR] Failed to decode token payload: {str(e)} | "
            f"Không thể giải mã nội dung mã thông báo: {str(e)}"
        )
        return None
    
    except Exception as e:
        logger.error(
            f"[ERROR] Unexpected error decoding token: {str(e)} | "
            f"Lỗi không mong đợi khi giải mã mã thông báo: {str(e)}"
        )
        return None


def decode_token_header(token: str) -> Optional[Dict[str, Any]]:
    """
    Extract JWT header without verification (for debugging).
    
    Useful for inspecting token algorithm, key ID, or other header claims.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded header dictionary or None if token is malformed
    
    Example:
        >>> header = decode_token_header(token)
        >>> if header:
        ...     print(f"Algorithm: {header.get('alg')}")
    
    Vietnamese:
        Trích xuất tiêu đề JWT mà không xác minh (để gỡ lỗi).
    """
    try:
        # Decode header without verification - Giải mã tiêu đề không xác minh
        header = jwt.get_unverified_header(token)
        
        algorithm = header.get("alg", "unknown")
        logger.debug(f"[OK] Token header extracted -> Algorithm: {algorithm}")
        
        return header
        
    except jwt.DecodeError as e:
        logger.error(
            f"[ERROR] Failed to decode token header: {str(e)} | "
            f"Không thể giải mã tiêu đề mã thông báo: {str(e)}"
        )
        return None
    
    except Exception as e:
        logger.error(
            f"[ERROR] Unexpected error decoding header: {str(e)} | "
            f"Lỗi không mong đợi khi giải mã tiêu đề: {str(e)}"
        )
        return None
