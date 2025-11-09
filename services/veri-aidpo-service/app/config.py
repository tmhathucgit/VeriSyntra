"""
VeriAIDPO Service Configuration
Pydantic settings for microservice configuration
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Service info
    service_name: str = "VeriAIDPO Classification Service"
    service_version: str = "1.0.0"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    
    # JWT Authentication (Phase 2)
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    
    # Database
    database_url: str = ""
    
    # Redis
    redis_url: str = "redis://redis:6379/1"
    
    # ML Models
    model_cache_dir: str = "/app/models"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
