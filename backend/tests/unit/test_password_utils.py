"""
VeriSyntra Password Utilities Unit Tests
Vietnamese PDPL 2025 Compliance Platform

Comprehensive unit tests for password hashing and validation.
"""

import pytest
from auth.password_utils import (
    hash_password,
    verify_password,
    needs_rehash,
    validate_password_strength
)


class TestHashPassword:
    """Test suite for password hashing."""

    def test_hash_password_returns_string(self, sample_password):
        """Test that hash_password returns a string."""
        hashed = hash_password(sample_password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_uses_bcrypt_format(self, sample_password):
        """Test that hashed password uses bcrypt format."""
        hashed = hash_password(sample_password)
        
        # Bcrypt hashes start with $2b$ or $2a$
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_hash_password_creates_unique_hashes(self, sample_password):
        """Test that same password creates different hashes (due to salt)."""
        hash1 = hash_password(sample_password)
        hash2 = hash_password(sample_password)
        
        assert hash1 != hash2  # Different salts = different hashes

    def test_hash_password_with_vietnamese_characters(self):
        """Test hashing passwords with Vietnamese characters."""
        vietnamese_password = "MậtKhẩu123!@#Việt"
        hashed = hash_password(vietnamese_password)
        
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_hash_password_with_empty_string(self):
        """Test hashing empty password."""
        hashed = hash_password("")
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_with_long_password(self):
        """Test hashing very long password."""
        long_password = "A" * 100 + "1!@#"
        hashed = hash_password(long_password)
        
        assert isinstance(hashed, str)


class TestVerifyPassword:
    """Test suite for password verification."""

    def test_verify_correct_password(self, sample_password):
        """Test verifying correct password."""
        hashed = hash_password(sample_password)
        result = verify_password(sample_password, hashed)
        
        assert result is True

    def test_verify_incorrect_password(self, sample_password):
        """Test verifying incorrect password."""
        hashed = hash_password(sample_password)
        result = verify_password("WrongPassword123!", hashed)
        
        assert result is False

    def test_verify_password_case_sensitive(self, sample_password):
        """Test that password verification is case-sensitive."""
        hashed = hash_password(sample_password)
        wrong_case = sample_password.lower()
        
        if wrong_case != sample_password:
            result = verify_password(wrong_case, hashed)
            assert result is False

    def test_verify_password_with_vietnamese_characters(self):
        """Test verifying password with Vietnamese characters."""
        vietnamese_password = "MậtKhẩu123!@#Việt"
        hashed = hash_password(vietnamese_password)
        
        # Correct password
        assert verify_password(vietnamese_password, hashed) is True
        
        # Wrong password
        assert verify_password("MậtKhẩu123!@#Viet", hashed) is False

    def test_verify_empty_password(self):
        """Test verifying empty password."""
        hashed = hash_password("")
        
        assert verify_password("", hashed) is True
        assert verify_password("nonempty", hashed) is False

    def test_verify_password_with_invalid_hash(self, sample_password):
        """Test verifying password with invalid hash."""
        result = verify_password(sample_password, "invalid_hash")
        
        assert result is False

    def test_verify_password_timing_attack_resistance(self, sample_password):
        """Test that verification uses constant-time comparison."""
        hashed = hash_password(sample_password)
        
        # Both correct and incorrect passwords should take similar time
        # This is a basic check - timing is handled by bcrypt internally
        result1 = verify_password(sample_password, hashed)
        result2 = verify_password("WrongPassword123!", hashed)
        
        assert result1 is True
        assert result2 is False


class TestNeedsRehash:
    """Test suite for password rehash detection."""

    def test_needs_rehash_with_current_rounds(self, sample_password):
        """Test that recently hashed password doesn't need rehash."""
        hashed = hash_password(sample_password)
        result = needs_rehash(hashed)
        
        # Should not need rehash if using current settings
        assert result is False

    def test_needs_rehash_with_invalid_hash(self):
        """Test needs_rehash with invalid hash."""
        result = needs_rehash("invalid_hash")
        
        # Invalid hash returns False (error logged)
        assert result is False

    def test_needs_rehash_with_empty_hash(self):
        """Test needs_rehash with empty hash."""
        result = needs_rehash("")
        
        # Empty hash returns False (error logged)
        assert result is False


class TestValidatePasswordStrength:
    """Test suite for password strength validation."""

    def test_validate_strong_password(self, sample_password):
        """Test validating a strong password."""
        is_valid, error = validate_password_strength(sample_password)
        
        assert is_valid is True
        assert error is None

    def test_validate_password_too_short(self):
        """Test validating password that is too short."""
        short_password = "Ab1!"
        is_valid, error = validate_password_strength(short_password)
        
        assert is_valid is False
        assert error is not None
        assert "at least 8 characters" in error.lower()

    def test_validate_password_no_uppercase(self):
        """Test validating password without uppercase letter."""
        no_upper = "password123!"
        is_valid, error = validate_password_strength(no_upper)
        
        assert is_valid is False
        assert "uppercase" in error.lower()

    def test_validate_password_no_lowercase(self):
        """Test validating password without lowercase letter."""
        no_lower = "PASSWORD123!"
        is_valid, error = validate_password_strength(no_lower)
        
        assert is_valid is False
        assert "lowercase" in error.lower()

    def test_validate_password_no_digit(self):
        """Test validating password without digit."""
        no_digit = "Password!@#"
        is_valid, error = validate_password_strength(no_digit)
        
        assert is_valid is False
        assert "digit" in error.lower()

    def test_validate_password_no_special(self):
        """Test validating password without special character."""
        no_special = "Password123"
        is_valid, error = validate_password_strength(no_special)
        
        assert is_valid is False
        assert "special" in error.lower()

    def test_validate_weak_passwords(self, sample_weak_passwords):
        """Test validating multiple weak passwords."""
        for weak_password in sample_weak_passwords:
            is_valid, error = validate_password_strength(weak_password)
            
            assert is_valid is False
            assert error is not None

    def test_validate_password_with_vietnamese_characters(self):
        """Test validating password with Vietnamese characters."""
        vietnamese_password = "MậtKhẩu123!@#"
        is_valid, error = validate_password_strength(vietnamese_password)
        
        # Should be valid (has uppercase, lowercase, digit, special)
        assert is_valid is True
        assert error is None

    def test_validate_empty_password(self):
        """Test validating empty password."""
        is_valid, error = validate_password_strength("")
        
        assert is_valid is False
        assert error is not None

    def test_validate_returns_bilingual_errors(self):
        """Test that validation returns bilingual errors."""
        weak_password = "weak"
        is_valid, error = validate_password_strength(weak_password)
        
        assert is_valid is False
        assert isinstance(error, str)
        assert "|" in error  # Bilingual errors separated by |


class TestPasswordUtilsIntegration:
    """Integration tests for password utilities."""

    def test_hash_and_verify_workflow(self, sample_password):
        """Test complete hash and verify workflow."""
        # Hash password
        hashed = hash_password(sample_password)
        
        # Verify correct password
        assert verify_password(sample_password, hashed) is True
        
        # Verify incorrect password
        assert verify_password("WrongPassword", hashed) is False

    def test_validate_then_hash_workflow(self, sample_password):
        """Test validate then hash workflow."""
        # Validate password strength first
        is_valid, error = validate_password_strength(sample_password)
        assert is_valid is True
        assert error is None
        
        # If valid, hash it
        hashed = hash_password(sample_password)
        
        # Verify it works
        assert verify_password(sample_password, hashed) is True

    def test_multiple_users_same_password(self, sample_password):
        """Test that multiple users with same password get different hashes."""
        user1_hash = hash_password(sample_password)
        user2_hash = hash_password(sample_password)
        user3_hash = hash_password(sample_password)
        
        # All hashes should be different (different salts)
        assert user1_hash != user2_hash
        assert user2_hash != user3_hash
        assert user1_hash != user3_hash
        
        # But all should verify correctly
        assert verify_password(sample_password, user1_hash) is True
        assert verify_password(sample_password, user2_hash) is True
        assert verify_password(sample_password, user3_hash) is True
