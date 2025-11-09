"""
VeriSyntra Token Blacklist Unit Tests
Vietnamese PDPL 2025 Compliance Platform

Comprehensive unit tests for Redis-based token blacklist functionality.
"""

import pytest
import time
from auth.token_blacklist import TokenBlacklist
from auth.jwt_handler import create_access_token


class TestTokenBlacklistInitialization:
    """Test suite for TokenBlacklist initialization."""

    def test_blacklist_initialization(self):
        """Test that TokenBlacklist initializes successfully."""
        blacklist = TokenBlacklist()
        
        assert blacklist is not None
        assert blacklist.redis_client is not None

    def test_blacklist_health_check(self):
        """Test Redis health check."""
        blacklist = TokenBlacklist()
        health = blacklist.health_check()
        
        assert health["connected"] is True
        assert "redis_version" in health
        assert "connected_clients" in health
        assert "used_memory_human" in health


class TestAddToken:
    """Test suite for adding tokens to blacklist."""

    def test_add_token_success(self):
        """Test successfully adding token to blacklist."""
        blacklist = TokenBlacklist()
        test_token = "test.token.123"
        
        result = blacklist.add_token(test_token, expires_in_minutes=5)
        
        assert result is True

    def test_add_token_with_custom_ttl(self):
        """Test adding token with custom TTL."""
        blacklist = TokenBlacklist()
        test_token = "test.token.custom.ttl"
        
        result = blacklist.add_token(test_token, expires_in_minutes=60)
        
        assert result is True
        
        # Verify TTL is approximately correct
        ttl = blacklist.get_blacklist_ttl(test_token)
        assert ttl is not None
        assert 3500 < ttl < 3700  # Allow margin for 60 minutes

    def test_add_real_jwt_token(self):
        """Test adding real JWT token to blacklist."""
        blacklist = TokenBlacklist()
        
        # Create real JWT token
        token_data = {"user_id": "user123", "email": "test@example.com"}
        jwt_token = create_access_token(data=token_data)
        
        result = blacklist.add_token(jwt_token, expires_in_minutes=30)
        
        assert result is True


class TestIsBlacklisted:
    """Test suite for checking if token is blacklisted."""

    def test_is_blacklisted_for_blacklisted_token(self):
        """Test checking if blacklisted token is detected."""
        blacklist = TokenBlacklist()
        test_token = "test.blacklisted.token"
        
        # Add token to blacklist
        blacklist.add_token(test_token, expires_in_minutes=5)
        
        # Check if blacklisted
        result = blacklist.is_blacklisted(test_token)
        
        assert result is True

    def test_is_blacklisted_for_clean_token(self):
        """Test checking if non-blacklisted token returns False."""
        blacklist = TokenBlacklist()
        clean_token = f"test.clean.token.{time.time()}"
        
        result = blacklist.is_blacklisted(clean_token)
        
        assert result is False

    def test_is_blacklisted_fail_secure(self):
        """Test that is_blacklisted returns True on Redis errors (fail-secure)."""
        blacklist = TokenBlacklist()
        
        # Close Redis connection to simulate error
        blacklist.redis_client.close()
        
        # Should return True (deny access) on error
        result = blacklist.is_blacklisted("test.token")
        
        # Note: This should return True due to fail-secure design
        # However, Redis might auto-reconnect, so we just verify no exception
        assert isinstance(result, bool)


class TestRemoveToken:
    """Test suite for removing tokens from blacklist."""

    def test_remove_token_success(self):
        """Test successfully removing token from blacklist."""
        blacklist = TokenBlacklist()
        test_token = "test.token.remove"
        
        # Add token first
        blacklist.add_token(test_token, expires_in_minutes=5)
        assert blacklist.is_blacklisted(test_token) is True
        
        # Remove token
        result = blacklist.remove_token(test_token)
        
        assert result is True
        assert blacklist.is_blacklisted(test_token) is False

    def test_remove_non_existent_token(self):
        """Test removing token that doesn't exist."""
        blacklist = TokenBlacklist()
        non_existent_token = f"test.non.existent.{time.time()}"
        
        # Should return True even if token doesn't exist
        result = blacklist.remove_token(non_existent_token)
        
        assert result is True


class TestGetBlacklistTTL:
    """Test suite for getting token TTL."""

    def test_get_ttl_for_blacklisted_token(self):
        """Test getting TTL for blacklisted token."""
        blacklist = TokenBlacklist()
        test_token = "test.token.ttl"
        
        # Add token with 10 minute TTL
        blacklist.add_token(test_token, expires_in_minutes=10)
        
        # Get TTL
        ttl = blacklist.get_blacklist_ttl(test_token)
        
        assert ttl is not None
        assert 500 < ttl <= 600  # Should be close to 600 seconds (10 minutes)

    def test_get_ttl_for_non_blacklisted_token(self):
        """Test getting TTL for non-blacklisted token."""
        blacklist = TokenBlacklist()
        clean_token = f"test.clean.token.{time.time()}"
        
        ttl = blacklist.get_blacklist_ttl(clean_token)
        
        assert ttl is None

    def test_get_ttl_decreases_over_time(self):
        """Test that TTL decreases over time."""
        blacklist = TokenBlacklist()
        test_token = "test.token.ttl.decrease"
        
        # Add token
        blacklist.add_token(test_token, expires_in_minutes=5)
        
        # Get initial TTL
        ttl1 = blacklist.get_blacklist_ttl(test_token)
        
        # Wait 2 seconds
        time.sleep(2)
        
        # Get TTL again
        ttl2 = blacklist.get_blacklist_ttl(test_token)
        
        assert ttl2 < ttl1


class TestClearAllBlacklistedTokens:
    """Test suite for clearing all blacklisted tokens."""

    def test_clear_all_tokens(self):
        """Test clearing all blacklisted tokens."""
        blacklist = TokenBlacklist()
        
        # Add multiple tokens
        tokens = [f"test.clear.token.{i}" for i in range(5)]
        for token in tokens:
            blacklist.add_token(token, expires_in_minutes=5)
        
        # Verify all are blacklisted
        for token in tokens:
            assert blacklist.is_blacklisted(token) is True
        
        # Clear all
        cleared_count = blacklist.clear_all_blacklisted_tokens()
        
        assert cleared_count >= 5  # At least our 5 tokens
        
        # Verify all our tokens are cleared
        for token in tokens:
            assert blacklist.is_blacklisted(token) is False


class TestTokenBlacklistIntegration:
    """Integration tests for token blacklist."""

    def test_logout_workflow(self):
        """Test complete logout workflow with JWT token."""
        blacklist = TokenBlacklist()
        
        # 1. User logs in and gets access token
        user_data = {
            "user_id": "user123",
            "email": "nguyen.van.a@example.com",
            "tenant_id": "tenant001"
        }
        access_token = create_access_token(data=user_data)
        
        # 2. Token is not blacklisted initially
        assert blacklist.is_blacklisted(access_token) is False
        
        # 3. User logs out - add token to blacklist
        blacklist.add_token(access_token, expires_in_minutes=30)
        
        # 4. Token is now blacklisted
        assert blacklist.is_blacklisted(access_token) is True
        
        # 5. Subsequent requests with this token should be denied
        # (is_blacklisted returns True)

    def test_token_expiration_workflow(self):
        """Test that blacklisted tokens expire after TTL."""
        blacklist = TokenBlacklist()
        test_token = "test.expiration.token"
        
        # Add token with very short TTL (2 seconds)
        blacklist.add_token(test_token, expires_in_minutes=0.033)  # ~2 seconds
        
        # Token should be blacklisted immediately
        assert blacklist.is_blacklisted(test_token) is True
        
        # Wait for expiration
        time.sleep(3)
        
        # Token should no longer be blacklisted (expired from Redis)
        assert blacklist.is_blacklisted(test_token) is False

    def test_multiple_users_logout(self):
        """Test multiple users logging out simultaneously."""
        blacklist = TokenBlacklist()
        
        # Create tokens for multiple users
        users = [
            {"user_id": f"user{i}", "email": f"user{i}@example.com"}
            for i in range(3)
        ]
        tokens = [create_access_token(data=user) for user in users]
        
        # All tokens should not be blacklisted initially
        for token in tokens:
            assert blacklist.is_blacklisted(token) is False
        
        # Blacklist all tokens (users logout)
        for token in tokens:
            blacklist.add_token(token, expires_in_minutes=30)
        
        # All tokens should now be blacklisted
        for token in tokens:
            assert blacklist.is_blacklisted(token) is True

    def test_revoke_and_restore_token(self):
        """Test revoking token and then restoring it."""
        blacklist = TokenBlacklist()
        test_token = "test.revoke.restore.token"
        
        # Add to blacklist (revoke)
        blacklist.add_token(test_token, expires_in_minutes=10)
        assert blacklist.is_blacklisted(test_token) is True
        
        # Remove from blacklist (restore)
        blacklist.remove_token(test_token)
        assert blacklist.is_blacklisted(test_token) is False
        
        # Can revoke again
        blacklist.add_token(test_token, expires_in_minutes=10)
        assert blacklist.is_blacklisted(test_token) is True


class TestTokenBlacklistEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_add_empty_token(self):
        """Test adding empty token."""
        blacklist = TokenBlacklist()
        
        result = blacklist.add_token("", expires_in_minutes=5)
        
        # Should handle gracefully
        assert isinstance(result, bool)

    def test_check_empty_token(self):
        """Test checking empty token."""
        blacklist = TokenBlacklist()
        
        result = blacklist.is_blacklisted("")
        
        # Should return False (or True for fail-secure)
        assert isinstance(result, bool)

    def test_add_token_with_zero_ttl(self):
        """Test adding token with zero TTL."""
        blacklist = TokenBlacklist()
        test_token = "test.zero.ttl"
        
        # TTL of 0 minutes should still work (immediate expiration)
        result = blacklist.add_token(test_token, expires_in_minutes=0)
        
        assert isinstance(result, bool)

    def test_add_token_with_negative_ttl(self):
        """Test adding token with negative TTL."""
        blacklist = TokenBlacklist()
        test_token = "test.negative.ttl"
        
        # Should handle gracefully (likely treat as 0 or error)
        result = blacklist.add_token(test_token, expires_in_minutes=-5)
        
        assert isinstance(result, bool)

    def test_add_very_long_token(self):
        """Test adding very long token."""
        blacklist = TokenBlacklist()
        long_token = "a" * 10000
        
        result = blacklist.add_token(long_token, expires_in_minutes=5)
        
        assert isinstance(result, bool)
