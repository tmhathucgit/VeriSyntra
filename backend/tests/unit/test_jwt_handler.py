"""
VeriSyntra JWT Handler Unit Tests
Vietnamese PDPL 2025 Compliance Platform

Comprehensive unit tests for JWT token creation and validation.
"""

import pytest
from datetime import timedelta
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError
from auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_token_payload,
    decode_token_header,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
    TOKEN_ISSUER
)


class TestCreateAccessToken:
    """Test suite for access token creation."""

    def test_create_access_token_with_defaults(self, sample_user_data):
        """Test creating access token with default expiration."""
        token = create_access_token(data=sample_user_data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token contains correct data
        payload = get_token_payload(token)
        assert payload["user_id"] == sample_user_data["user_id"]
        assert payload["email"] == sample_user_data["email"]
        assert payload["tenant_id"] == sample_user_data["tenant_id"]
        assert payload["regional_location"] == sample_user_data["regional_location"]
        assert payload["type"] == TOKEN_TYPE_ACCESS
        assert payload["iss"] == TOKEN_ISSUER

    def test_create_access_token_with_custom_expiry(self, sample_user_data):
        """Test creating access token with custom expiration time."""
        custom_expiry = timedelta(minutes=60)
        token = create_access_token(data=sample_user_data, expires_delta=custom_expiry)
        
        assert token is not None
        payload = get_token_payload(token)
        assert payload["type"] == TOKEN_TYPE_ACCESS
        
        # Verify expiration is approximately 60 minutes from now
        import time
        exp_time = payload["exp"]
        current_time = time.time()
        time_diff = exp_time - current_time
        assert 3500 < time_diff < 3700  # Allow 100 second margin

    def test_create_access_token_with_minimal_data(self):
        """Test creating access token with minimal required data."""
        minimal_data = {"user_id": "user456"}
        token = create_access_token(data=minimal_data)
        
        assert token is not None
        payload = get_token_payload(token)
        assert payload["user_id"] == "user456"
        assert payload["type"] == TOKEN_TYPE_ACCESS

    def test_create_access_token_preserves_vietnamese_data(self):
        """Test that Vietnamese characters are preserved in tokens."""
        vietnamese_data = {
            "user_id": "user789",
            "full_name": "Nguyễn Văn A",
            "company": "Công ty TNHH ABC",
            "city": "Thành phố Hồ Chí Minh"
        }
        token = create_access_token(data=vietnamese_data)
        
        payload = get_token_payload(token)
        assert payload["full_name"] == "Nguyễn Văn A"
        assert payload["company"] == "Công ty TNHH ABC"
        assert payload["city"] == "Thành phố Hồ Chí Minh"


class TestCreateRefreshToken:
    """Test suite for refresh token creation."""

    def test_create_refresh_token_with_defaults(self, sample_user_data):
        """Test creating refresh token with default expiration."""
        token = create_refresh_token(data=sample_user_data)
        
        assert token is not None
        assert isinstance(token, str)
        
        payload = get_token_payload(token)
        assert payload["user_id"] == sample_user_data["user_id"]
        assert payload["type"] == TOKEN_TYPE_REFRESH
        assert payload["iss"] == TOKEN_ISSUER

    def test_create_refresh_token_with_custom_expiry(self, sample_user_data):
        """Test creating refresh token with custom expiration time."""
        custom_expiry = timedelta(days=30)
        token = create_refresh_token(data=sample_user_data, expires_delta=custom_expiry)
        
        payload = get_token_payload(token)
        assert payload["type"] == TOKEN_TYPE_REFRESH
        
        # Verify expiration is approximately 30 days from now
        import time
        exp_time = payload["exp"]
        current_time = time.time()
        time_diff = exp_time - current_time
        assert 2590000 < time_diff < 2594000  # Allow margin for 30 days


class TestVerifyToken:
    """Test suite for token verification."""

    def test_verify_valid_access_token(self, sample_user_data):
        """Test verifying a valid access token."""
        token = create_access_token(data=sample_user_data)
        payload = verify_token(token, expected_type=TOKEN_TYPE_ACCESS)
        
        assert payload is not None
        assert payload["user_id"] == sample_user_data["user_id"]
        assert payload["type"] == TOKEN_TYPE_ACCESS

    def test_verify_valid_refresh_token(self, sample_user_data):
        """Test verifying a valid refresh token."""
        token = create_refresh_token(data=sample_user_data)
        payload = verify_token(token, expected_type=TOKEN_TYPE_REFRESH)
        
        assert payload is not None
        assert payload["user_id"] == sample_user_data["user_id"]
        assert payload["type"] == TOKEN_TYPE_REFRESH

    def test_verify_token_with_wrong_type(self, sample_user_data):
        """Test that verification fails when token type doesn't match."""
        access_token = create_access_token(data=sample_user_data)
        
        with pytest.raises(InvalidTokenError) as exc_info:
            verify_token(access_token, expected_type=TOKEN_TYPE_REFRESH)
        
        # Check bilingual error message
        error_message = str(exc_info.value)
        assert "Wrong token type" in error_message or "Loại mã thông báo sai" in error_message

    def test_verify_expired_token(self, sample_user_data):
        """Test that verification fails for expired tokens."""
        # Create token that expires immediately
        expired_token = create_access_token(
            data=sample_user_data,
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        with pytest.raises(InvalidTokenError) as exc_info:
            verify_token(expired_token, expected_type=TOKEN_TYPE_ACCESS)
        
        # Check bilingual error message
        error_message = str(exc_info.value)
        assert "expired" in error_message.lower() or "hết hạn" in error_message.lower()

    def test_verify_invalid_signature(self, sample_user_data):
        """Test that verification fails for tokens with invalid signature."""
        token = create_access_token(data=sample_user_data)
        
        # Tamper with token (change last character)
        tampered_token = token[:-1] + ("A" if token[-1] != "A" else "B")
        
        with pytest.raises(InvalidTokenError):
            verify_token(tampered_token, expected_type=TOKEN_TYPE_ACCESS)

    def test_verify_malformed_token(self):
        """Test that verification fails for malformed tokens."""
        malformed_tokens = [
            "not.a.token",
            "invalid",
            "",
            "a.b",  # Only 2 parts instead of 3
            "a.b.c.d",  # Too many parts
        ]
        
        for malformed_token in malformed_tokens:
            with pytest.raises(InvalidTokenError):
                verify_token(malformed_token, expected_type=TOKEN_TYPE_ACCESS)

    def test_verify_token_without_type(self, sample_user_data):
        """Test verifying token without specifying expected type."""
        token = create_access_token(data=sample_user_data)
        payload = verify_token(token)  # No expected_type
        
        assert payload is not None
        assert payload["user_id"] == sample_user_data["user_id"]


class TestGetTokenPayload:
    """Test suite for token payload extraction (debug only)."""

    def test_get_payload_from_valid_token(self, sample_user_data):
        """Test extracting payload from valid token."""
        token = create_access_token(data=sample_user_data)
        payload = get_token_payload(token)
        
        assert payload is not None
        assert payload["user_id"] == sample_user_data["user_id"]
        assert "exp" in payload
        assert "iat" in payload
        assert "type" in payload

    def test_get_payload_from_expired_token(self, sample_user_data):
        """Test that get_token_payload works even for expired tokens."""
        expired_token = create_access_token(
            data=sample_user_data,
            expires_delta=timedelta(seconds=-1)
        )
        
        # Should still extract payload (no verification)
        payload = get_token_payload(expired_token)
        assert payload is not None
        assert payload["user_id"] == sample_user_data["user_id"]

    def test_get_payload_from_invalid_token(self):
        """Test that get_token_payload returns None for invalid tokens."""
        invalid_tokens = [
            "not.a.token",
            "invalid",
            "",
        ]
        
        for invalid_token in invalid_tokens:
            payload = get_token_payload(invalid_token)
            assert payload is None


class TestDecodeTokenHeader:
    """Test suite for token header decoding."""

    def test_decode_header_from_valid_token(self, sample_user_data):
        """Test decoding header from valid token."""
        token = create_access_token(data=sample_user_data)
        header = decode_token_header(token)
        
        assert header is not None
        assert header["alg"] == "HS256"  # Our configured algorithm
        assert header["typ"] == "JWT"

    def test_decode_header_from_invalid_token(self):
        """Test that decode_token_header returns None for invalid tokens."""
        invalid_tokens = [
            "not.a.token",
            "invalid",
            "",
        ]
        
        for invalid_token in invalid_tokens:
            header = decode_token_header(invalid_token)
            assert header is None


class TestTokenConstants:
    """Test suite for token-related constants."""

    def test_token_type_constants(self):
        """Test that token type constants are defined correctly."""
        assert TOKEN_TYPE_ACCESS == "access"
        assert TOKEN_TYPE_REFRESH == "refresh"

    def test_token_issuer_constant(self):
        """Test that token issuer constant is defined."""
        assert TOKEN_ISSUER == "verisyntra-api"
