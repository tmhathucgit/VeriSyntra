"""
VeriSyntra Authentication Module

JWT-based authentication for Vietnamese PDPL 2025 compliance platform.
Provides token generation, validation, password hashing, and blacklist management.

Vietnamese: Module xác thực VeriSyntra
"""

from .jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_token_payload,
    decode_token_header,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
    TOKEN_ISSUER
)

from .password_utils import (
    hash_password,
    verify_password,
    needs_rehash,
    validate_password_strength
)

from .token_blacklist import (
    token_blacklist,
    TokenBlacklist
)

__all__ = [
    # Token creation functions - Hàm tạo mã thông báo
    "create_access_token",
    "create_refresh_token",
    
    # Token validation functions - Hàm xác thực mã thông báo
    "verify_token",
    "get_token_payload",
    "decode_token_header",
    
    # Password utilities - Tiện ích mật khẩu
    "hash_password",
    "verify_password",
    "needs_rehash",
    "validate_password_strength",
    
    # Token blacklist - Danh sách đen mã thông báo
    "token_blacklist",
    "TokenBlacklist",
    
    # Token type constants - Hằng số loại mã thông báo
    "TOKEN_TYPE_ACCESS",
    "TOKEN_TYPE_REFRESH",
    "TOKEN_ISSUER"
]
