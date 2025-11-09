"""
Password Hashing Utilities for VeriSyntra Authentication

Provides secure password hashing and verification using bcrypt algorithm
with Vietnamese business context support.

Coding Standards:
- No hard-coded values (bcrypt rounds from settings)
- Type hints on all functions
- Bilingual error messages
- ASCII-only status indicators
- Comprehensive logging

Vietnamese: Tiện ích băm mật khẩu cho xác thực VeriSyntra
"""

from typing import Optional
from passlib.context import CryptContext
from loguru import logger

from config.settings import settings


# Passlib context with bcrypt - Ngữ cảnh Passlib với bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS
)


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt algorithm.
    
    Uses bcrypt with configurable rounds from settings (default: 12).
    Suitable for Vietnamese business user passwords with proper security.
    
    Args:
        password: Plaintext password to hash
    
    Returns:
        Hashed password string (bcrypt format)
    
    Example:
        >>> hashed = hash_password("MySecurePassword123!")
        >>> # Returns: $2b$12$... (bcrypt hash)
    
    Vietnamese:
        Băm mật khẩu văn bản thuần túy bằng thuật toán bcrypt.
    """
    try:
        hashed = pwd_context.hash(password)
        logger.info(
            f"[OK] Password hashed successfully -> "
            f"Bcrypt rounds: {settings.BCRYPT_ROUNDS}"
        )
        return hashed
        
    except Exception as e:
        error_msg = (
            f"Failed to hash password: {str(e)} | "
            f"Không thể băm mật khẩu: {str(e)}"
        )
        logger.error(f"[ERROR] {error_msg}")
        raise ValueError(error_msg)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.
    
    Constant-time comparison to prevent timing attacks.
    Used for Vietnamese business user login authentication.
    
    Args:
        plain_password: Plaintext password to verify
        hashed_password: Bcrypt hashed password from database
    
    Returns:
        True if password matches, False otherwise
    
    Example:
        >>> is_valid = verify_password("MyPassword123!", hashed_from_db)
        >>> if is_valid:
        ...     # Password correct - proceed with login
    
    Vietnamese:
        Xác minh mật khẩu văn bản thuần túy với băm bcrypt.
    """
    try:
        is_valid = pwd_context.verify(plain_password, hashed_password)
        
        if is_valid:
            logger.info("[OK] Password verification successful")
        else:
            logger.warning("[WARNING] Password verification failed - incorrect password")
        
        return is_valid
        
    except Exception as e:
        error_msg = (
            f"Failed to verify password: {str(e)} | "
            f"Không thể xác minh mật khẩu: {str(e)}"
        )
        logger.error(f"[ERROR] {error_msg}")
        return False


def needs_rehash(hashed_password: str) -> bool:
    """
    Check if a hashed password needs to be rehashed.
    
    Returns True if the hash uses deprecated algorithm or different
    bcrypt rounds than current settings. Useful for password upgrade
    on user login.
    
    Args:
        hashed_password: Bcrypt hashed password to check
    
    Returns:
        True if password should be rehashed with current settings
    
    Example:
        >>> if verify_password(plain, hashed) and needs_rehash(hashed):
        ...     new_hash = hash_password(plain)
        ...     # Update database with new_hash
    
    Vietnamese:
        Kiểm tra xem mật khẩu đã băm có cần băm lại không.
    """
    try:
        needs_upgrade = pwd_context.needs_update(hashed_password)
        
        if needs_upgrade:
            logger.info(
                "[WARNING] Password hash needs upgrade -> "
                f"Current bcrypt rounds: {settings.BCRYPT_ROUNDS}"
            )
        
        return needs_upgrade
        
    except Exception as e:
        logger.error(
            f"[ERROR] Failed to check password rehash: {str(e)} | "
            f"Không thể kiểm tra băm lại mật khẩu: {str(e)}"
        )
        return False


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength for Vietnamese business users.
    
    Password requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - At least 1 special character
    
    Args:
        password: Plaintext password to validate
    
    Returns:
        Tuple of (is_valid, error_message_vi_en)
        - is_valid: True if password meets requirements
        - error_message: Bilingual error message or None
    
    Example:
        >>> is_valid, error = validate_password_strength("weak")
        >>> if not is_valid:
        ...     print(error)  # "Password too short | Mật khẩu quá ngắn"
    
    Vietnamese:
        Xác thực độ mạnh mật khẩu cho người dùng doanh nghiệp Việt Nam.
    """
    # Check minimum length - Kiểm tra độ dài tối thiểu
    if len(password) < 8:
        return False, (
            "Password must be at least 8 characters long | "
            "Mật khẩu phải có ít nhất 8 ký tự"
        )
    
    # Check for uppercase letter - Kiểm tra chữ hoa
    if not any(c.isupper() for c in password):
        return False, (
            "Password must contain at least 1 uppercase letter | "
            "Mật khẩu phải chứa ít nhất 1 chữ hoa"
        )
    
    # Check for lowercase letter - Kiểm tra chữ thường
    if not any(c.islower() for c in password):
        return False, (
            "Password must contain at least 1 lowercase letter | "
            "Mật khẩu phải chứa ít nhất 1 chữ thường"
        )
    
    # Check for digit - Kiểm tra chữ số
    if not any(c.isdigit() for c in password):
        return False, (
            "Password must contain at least 1 digit | "
            "Mật khẩu phải chứa ít nhất 1 chữ số"
        )
    
    # Check for special character - Kiểm tra ký tự đặc biệt
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, (
            "Password must contain at least 1 special character (!@#$%^&*...) | "
            "Mật khẩu phải chứa ít nhất 1 ký tự đặc biệt (!@#$%^&*...)"
        )
    
    logger.info("[OK] Password strength validation passed")
    return True, None
