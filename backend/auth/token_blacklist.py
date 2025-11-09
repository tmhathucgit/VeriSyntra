"""
Token Blacklist using Redis for VeriSyntra Authentication

Manages revoked JWT tokens for logout functionality and token invalidation.
Uses Redis for fast lookups and automatic expiration.

Coding Standards:
- No hard-coded values (all from settings)
- Type hints on all methods
- Bilingual error messages
- ASCII-only status indicators
- Comprehensive logging
- Fail-secure on errors

Vietnamese: Danh sách đen mã thông báo sử dụng Redis
"""

from typing import Optional
from datetime import timedelta
import redis
from redis.exceptions import ConnectionError as RedisConnectionError, RedisError
from loguru import logger

from config.settings import settings


class TokenBlacklist:
    """
    Redis-based token blacklist for revoked JWT tokens.
    
    Manages logout functionality by tracking invalidated tokens.
    Tokens automatically expire from blacklist when their TTL expires.
    
    Vietnamese: Danh sách đen mã thông báo dựa trên Redis.
    """
    
    def __init__(self):
        """
        Initialize Redis connection for token blacklist.
        
        Connects to Redis using configuration from settings.
        Tests connection on initialization.
        
        Raises:
            RedisConnectionError: If cannot connect to Redis server
            
        Vietnamese:
            Khởi tạo kết nối Redis cho danh sách đen mã thông báo.
        """
        try:
            # Build Redis connection - Xây dựng kết nối Redis
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=True,  # Return strings instead of bytes
                socket_connect_timeout=5,  # 5 second timeout
                socket_timeout=5,
                retry_on_timeout=True
            )
            
            # Test connection - Kiểm tra kết nối
            self.redis_client.ping()
            
            logger.info(
                f"[OK] Token blacklist Redis connection established -> "
                f"Host: {settings.REDIS_HOST}:{settings.REDIS_PORT}, "
                f"DB: {settings.REDIS_DB}"
            )
            
        except RedisConnectionError as e:
            error_msg = (
                f"Redis connection failed: {str(e)} | "
                f"Không thể kết nối Redis: {str(e)}"
            )
            logger.error(f"[ERROR] {error_msg}")
            raise RedisConnectionError(error_msg)
        
        except Exception as e:
            error_msg = (
                f"Unexpected error initializing Redis: {str(e)} | "
                f"Lỗi không mong đợi khi khởi tạo Redis: {str(e)}"
            )
            logger.error(f"[ERROR] {error_msg}")
            raise
    
    def add_token(
        self,
        token: str,
        expires_in_minutes: Optional[int] = None
    ) -> bool:
        """
        Add token to blacklist (logout/revoke functionality).
        
        Token will automatically expire from blacklist after TTL.
        TTL should match the token's expiration time.
        
        Args:
            token: JWT token string to blacklist
            expires_in_minutes: Token TTL in minutes (default: access token expiry)
        
        Returns:
            True if token successfully blacklisted, False on error
        
        Example:
            >>> blacklist.add_token(access_token, expires_in_minutes=30)
            True
        
        Vietnamese:
            Thêm mã thông báo vào danh sách đen (chức năng đăng xuất/thu hồi).
        """
        try:
            # Use default expiration if not provided - Sử dụng hết hạn mặc định
            if expires_in_minutes is None:
                expires_in_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
            
            # Store token with expiration - Lưu trữ mã thông báo với thời gian hết hạn
            key = f"blacklist:{token}"
            self.redis_client.setex(
                key,
                timedelta(minutes=expires_in_minutes),
                "revoked"  # Value doesn't matter, key existence is the check
            )
            
            logger.info(
                f"[OK] Token added to blacklist -> "
                f"TTL: {expires_in_minutes} minutes"
            )
            return True
            
        except RedisError as e:
            logger.error(
                f"[ERROR] Failed to blacklist token: {str(e)} | "
                f"Không thể thêm mã thông báo vào danh sách đen: {str(e)}"
            )
            return False
        
        except Exception as e:
            logger.error(
                f"[ERROR] Unexpected error blacklisting token: {str(e)} | "
                f"Lỗi không mong đợi khi thêm vào danh sách đen: {str(e)}"
            )
            return False
    
    def is_blacklisted(self, token: str) -> bool:
        """
        Check if token is blacklisted (revoked).
        
        FAIL-SECURE: Returns True (blacklisted) on Redis errors to deny access
        when blacklist check fails.
        
        Args:
            token: JWT token string to check
        
        Returns:
            True if token is blacklisted or on error (fail-secure)
            False if token is valid (not blacklisted)
        
        Example:
            >>> if blacklist.is_blacklisted(token):
            ...     raise HTTPException(401, "Token has been revoked")
        
        Vietnamese:
            Kiểm tra xem mã thông báo có bị đưa vào danh sách đen không.
        """
        try:
            key = f"blacklist:{token}"
            exists = self.redis_client.exists(key) > 0
            
            if exists:
                logger.warning("[WARNING] Token is blacklisted (revoked)")
            else:
                logger.debug("[OK] Token not blacklisted (valid)")
            
            return exists
            
        except RedisError as e:
            # FAIL-SECURE: Treat as blacklisted on error
            # Fail-secure: Coi như bị đưa vào danh sách đen khi có lỗi
            logger.error(
                f"[ERROR] Failed to check blacklist (fail-secure: deny): {str(e)} | "
                f"Không thể kiểm tra danh sách đen (fail-secure: từ chối): {str(e)}"
            )
            return True  # Deny access on error
        
        except Exception as e:
            # FAIL-SECURE: Treat as blacklisted on error
            logger.error(
                f"[ERROR] Unexpected error checking blacklist (fail-secure: deny): {str(e)} | "
                f"Lỗi không mong đợi (fail-secure: từ chối): {str(e)}"
            )
            return True  # Deny access on error
    
    def remove_token(self, token: str) -> bool:
        """
        Remove token from blacklist (rare use case).
        
        Typically not needed as tokens expire automatically.
        May be used for token un-revocation in special cases.
        
        Args:
            token: JWT token string to remove from blacklist
        
        Returns:
            True if successfully removed, False on error
        
        Example:
            >>> blacklist.remove_token(token)  # Un-revoke token
            True
        
        Vietnamese:
            Xóa mã thông báo khỏi danh sách đen (trường hợp hiếm).
        """
        try:
            key = f"blacklist:{token}"
            deleted = self.redis_client.delete(key)
            
            if deleted > 0:
                logger.info("[OK] Token removed from blacklist")
            else:
                logger.warning("[WARNING] Token not found in blacklist (already removed or expired)")
            
            return True
            
        except RedisError as e:
            logger.error(
                f"[ERROR] Failed to remove token from blacklist: {str(e)} | "
                f"Không thể xóa mã thông báo khỏi danh sách đen: {str(e)}"
            )
            return False
        
        except Exception as e:
            logger.error(
                f"[ERROR] Unexpected error removing token: {str(e)} | "
                f"Lỗi không mong đợi khi xóa mã thông báo: {str(e)}"
            )
            return False
    
    def get_blacklist_ttl(self, token: str) -> Optional[int]:
        """
        Get remaining TTL (time-to-live) for blacklisted token.
        
        Returns how many seconds until token expires from blacklist.
        Useful for debugging or administrative purposes.
        
        Args:
            token: JWT token string to check
        
        Returns:
            TTL in seconds, or None if token not blacklisted or on error
        
        Example:
            >>> ttl = blacklist.get_blacklist_ttl(token)
            >>> print(f"Token expires from blacklist in {ttl} seconds")
        
        Vietnamese:
            Lấy TTL (thời gian tồn tại) còn lại cho mã thông báo trong danh sách đen.
        """
        try:
            key = f"blacklist:{token}"
            ttl = self.redis_client.ttl(key)
            
            # TTL returns -2 if key doesn't exist, -1 if no expiration
            if ttl == -2:
                logger.debug("[OK] Token not in blacklist (TTL: -2)")
                return None
            elif ttl == -1:
                logger.warning("[WARNING] Token in blacklist with no expiration (TTL: -1)")
                return None
            else:
                logger.debug(f"[OK] Token blacklist TTL: {ttl} seconds")
                return ttl
            
        except RedisError as e:
            logger.error(
                f"[ERROR] Failed to get blacklist TTL: {str(e)} | "
                f"Không thể lấy TTL danh sách đen: {str(e)}"
            )
            return None
        
        except Exception as e:
            logger.error(
                f"[ERROR] Unexpected error getting TTL: {str(e)} | "
                f"Lỗi không mong đợi khi lấy TTL: {str(e)}"
            )
            return None
    
    def clear_all_blacklisted_tokens(self) -> int:
        """
        Clear all blacklisted tokens (administrative use only).
        
        WARNING: This will un-revoke ALL tokens. Use with extreme caution.
        Typically only used in testing or emergency situations.
        
        Returns:
            Number of tokens cleared, or -1 on error
        
        Example:
            >>> cleared = blacklist.clear_all_blacklisted_tokens()
            >>> print(f"Cleared {cleared} tokens from blacklist")
        
        Vietnamese:
            Xóa tất cả mã thông báo trong danh sách đen (chỉ dành cho quản trị).
        """
        try:
            # Find all blacklist keys - Tìm tất cả các khóa danh sách đen
            pattern = "blacklist:*"
            keys = list(self.redis_client.scan_iter(match=pattern))
            
            if not keys:
                logger.info("[OK] No blacklisted tokens to clear")
                return 0
            
            # Delete all keys - Xóa tất cả các khóa
            deleted = self.redis_client.delete(*keys)
            
            logger.warning(
                f"[WARNING] Cleared {deleted} tokens from blacklist (ADMINISTRATIVE ACTION)"
            )
            return deleted
            
        except RedisError as e:
            logger.error(
                f"[ERROR] Failed to clear blacklist: {str(e)} | "
                f"Không thể xóa danh sách đen: {str(e)}"
            )
            return -1
        
        except Exception as e:
            logger.error(
                f"[ERROR] Unexpected error clearing blacklist: {str(e)} | "
                f"Lỗi không mong đợi khi xóa danh sách đen: {str(e)}"
            )
            return -1
    
    def health_check(self) -> dict:
        """
        Check Redis connection health.
        
        Returns connection status and basic metrics.
        Useful for health check endpoints.
        
        Returns:
            Dictionary with health status and metrics
        
        Example:
            >>> health = blacklist.health_check()
            >>> if health['connected']:
            ...     print("Redis is healthy")
        
        Vietnamese:
            Kiểm tra sức khỏe kết nối Redis.
        """
        try:
            # Test connection - Kiểm tra kết nối
            ping_result = self.redis_client.ping()
            
            # Get info - Lấy thông tin
            info = self.redis_client.info()
            
            return {
                "connected": ping_result,
                "redis_version": info.get("redis_version", "unknown"),
                "used_memory_human": info.get("used_memory_human", "unknown"),
                "connected_clients": info.get("connected_clients", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0)
            }
            
        except RedisError as e:
            logger.error(f"[ERROR] Redis health check failed: {str(e)}")
            return {
                "connected": False,
                "error": str(e)
            }
        
        except Exception as e:
            logger.error(f"[ERROR] Unexpected error in health check: {str(e)}")
            return {
                "connected": False,
                "error": str(e)
            }


# Global singleton instance - Thể hiện singleton toàn cục
# Initialize once and reuse throughout application
try:
    token_blacklist = TokenBlacklist()
except Exception as e:
    logger.error(
        f"[ERROR] Failed to initialize global token blacklist: {str(e)} | "
        f"Không thể khởi tạo danh sách đen mã thông báo toàn cục: {str(e)}"
    )
    # Re-raise to prevent application from starting with broken blacklist
    raise
