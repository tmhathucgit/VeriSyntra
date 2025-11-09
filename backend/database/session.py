"""
Database Session Management
PostgreSQL connection with SQLAlchemy
Vietnamese business context: Database session for multi-tenant isolation
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Database URL from environment settings
DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,        # Maximum number of permanent connections
    max_overflow=20      # Maximum overflow connections
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Database session dependency for FastAPI - Phụ thuộc session cơ sở dữ liệu
    
    Usage:
        db: Session = Depends(get_db)
    
    Vietnamese Context:
    - Provides database session for multi-tenant queries
    - Automatic session cleanup after request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
