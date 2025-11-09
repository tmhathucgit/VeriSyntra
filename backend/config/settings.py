"""
VeriSyntra Backend Configuration Settings

This module handles all environment variable configuration for the VeriSyntra
Vietnamese PDPL 2025 compliance platform backend services.

Coding Standards:
- No hard-coded values (all from environment variables)
- Type hints on all fields
- Validation through Pydantic
- Vietnamese comments where applicable
- Bilingual error messages
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings use environment variables to avoid hard-coding.
    Supports both development and production environments.
    """
    
    # Application Settings
    APP_NAME: str = Field(
        default="VeriSyntra Vietnamese DPO Compliance Platform",
        description="Application name"
    )
    VERSION: str = Field(
        default="1.0.0-prototype",
        description="Application version"
    )
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )
    
    # Server Configuration
    HOST: str = Field(
        default="127.0.0.1",
        description="Server host address"
    )
    PORT: int = Field(
        default=8000,
        description="Server port number"
    )
    RELOAD: bool = Field(
        default=True,
        description="Enable auto-reload in development"
    )
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://verisyntra:password@localhost:5432/verisyntra_db",
        description="PostgreSQL database connection URL"
    )
    
    # Redis Configuration (Token Blacklist & Session Management)
    REDIS_HOST: str = Field(
        default="localhost",
        description="Redis server host"
    )
    REDIS_PORT: int = Field(
        default=6379,
        description="Redis server port"
    )
    REDIS_DB: int = Field(
        default=1,
        description="Redis database number (0-15)"
    )
    REDIS_PASSWORD: str = Field(
        default="",
        description="Redis password (empty if no auth)"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL (legacy)"
    )
    
    # JWT Authentication Configuration
    JWT_SECRET_KEY: str = Field(
        ...,  # Required field
        description="Secret key for JWT token signing (min 32 characters)"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    
    # Security Settings
    BCRYPT_ROUNDS: int = Field(
        default=12,
        description="Bcrypt hashing rounds (10-15 recommended)"
    )
    SECRET_KEY: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Legacy secret key (use JWT_SECRET_KEY instead)"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="Legacy algorithm (use JWT_ALGORITHM instead)"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Legacy token expiration (use JWT_ACCESS_TOKEN_EXPIRE_MINUTES)"
    )
    
    # Vietnamese Cultural Settings
    VIETNAM_TIMEZONE: str = Field(
        default="Asia/Ho_Chi_Minh",
        description="Vietnamese timezone for all datetime operations"
    )
    DEFAULT_LANGUAGE: str = Field(
        default="vi",
        description="Default language (vi=Vietnamese)"
    )
    SUPPORTED_LANGUAGES: str = Field(
        default="vi,en",
        description="Comma-separated supported languages"
    )
    
    # PDPL 2025 Configuration
    PDPL_VERSION: int = Field(
        default=2025,
        description="PDPL compliance version year"
    )
    COMPLIANCE_FRAMEWORK: str = Field(
        default="Vietnam_PDPL_2025",
        description="Compliance framework identifier"
    )
    
    # Logging Configuration
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    LOG_FORMAT: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>VeriSyntra</cyan> | {message}",
        description="Loguru log format string"
    )
    
    # CORS Configuration
    CORS_ORIGINS: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        description="Comma-separated allowed CORS origins"
    )
    
    @validator("JWT_SECRET_KEY")
    def validate_jwt_secret_key(cls, v: str) -> str:
        """
        Validate JWT secret key has minimum security requirements.
        
        Vietnamese: Xác thực khóa bí mật JWT đáp ứng yêu cầu bảo mật tối thiểu.
        """
        if len(v) < 32:
            raise ValueError(
                f"JWT_SECRET_KEY must be at least 32 characters long (current: {len(v)}). "
                f"JWT_SECRET_KEY phải có ít nhất 32 ký tự (hiện tại: {len(v)})."
            )
        return v
    
    @validator("BCRYPT_ROUNDS")
    def validate_bcrypt_rounds(cls, v: int) -> int:
        """
        Validate bcrypt rounds are within secure range.
        
        Vietnamese: Xác thực số vòng bcrypt nằm trong phạm vi bảo mật.
        """
        if not (10 <= v <= 15):
            raise ValueError(
                f"BCRYPT_ROUNDS must be between 10 and 15 (current: {v}). "
                f"BCRYPT_ROUNDS phải từ 10 đến 15 (hiện tại: {v})."
            )
        return v
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v: str) -> str:
        """
        Validate environment is one of allowed values.
        
        Vietnamese: Xác thực môi trường là một trong các giá trị được phép.
        """
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(
                f"ENVIRONMENT must be one of {allowed} (current: {v}). "
                f"ENVIRONMENT phải là một trong {allowed} (hiện tại: {v})."
            )
        return v
    
    def get_cors_origins_list(self) -> List[str]:
        """
        Get CORS origins as a list.
        
        Returns:
            List of allowed CORS origin URLs
            
        Vietnamese:
            Lấy danh sách nguồn CORS được phép.
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    def get_supported_languages_list(self) -> List[str]:
        """
        Get supported languages as a list.
        
        Returns:
            List of supported language codes
            
        Vietnamese:
            Lấy danh sách mã ngôn ngữ được hỗ trợ.
        """
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    def get_redis_url(self) -> str:
        """
        Construct Redis connection URL from components.
        
        Returns:
            Redis connection URL string
            
        Vietnamese:
            Xây dựng URL kết nối Redis từ các thành phần.
        """
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        """Pydantic configuration class."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env
        # Make .env file optional
        env_ignore_empty = True


# Global settings instance
# Vietnamese: Thể hiện cài đặt toàn cục
settings = Settings()
