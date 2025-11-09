"""
Database Connection Configuration
Async SQLAlchemy with PostgreSQL for VeriSyntra Data Inventory

This module provides async database connection setup using SQLAlchemy 2.0+
with asyncpg driver for PostgreSQL.

Vietnamese-First Architecture:
- Supports bilingual data (_vi NOT NULL, _en nullable)
- Multi-tenant row-level isolation via tenant_id
- Vietnamese timezone support (Asia/Ho_Chi_Minh)

PDPL 2025 Compliance:
- Secure connection pooling
- Transaction management for data integrity
- Audit trail support via session tracking

Usage:
    from database.connection import get_db
    
    @router.get("/endpoint")
    async def endpoint(db: AsyncSession = Depends(get_db)):
        # Database session available
        result = await db.execute(select(ProcessingActivityDB))
        activities = result.scalars().all()
        return activities
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
import os
import logging

logger = logging.getLogger(__name__)

# ============================================
# Database Configuration
# ============================================

# Database URL from environment
# Default: postgresql+asyncpg://verisyntra:verisyntra@localhost:5432/verisyntra
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://verisyntra:verisyntra@localhost:5432/verisyntra"
)

# SQL Echo for debugging (set SQL_ECHO=true in environment)
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"

# Connection pool settings
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))

# ============================================
# Async Engine Configuration
# ============================================

# Create async engine with asyncpg driver
engine = create_async_engine(
    DATABASE_URL,
    echo=SQL_ECHO,  # Log all SQL statements when true
    poolclass=NullPool,  # Use NullPool for async operations (recommended)
    future=True,  # Use SQLAlchemy 2.0 style
    pool_pre_ping=True,  # Verify connections before using
    connect_args={
        "server_settings": {
            "application_name": "verisyntra_data_inventory",
            "timezone": "Asia/Ho_Chi_Minh"  # Vietnamese timezone
        }
    }
)

logger.info(f"[OK] Database engine created for Data Inventory service")
logger.info(f"Database URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Not configured'}")

# ============================================
# Async Session Factory
# ============================================

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy-loading issues after commit
    autocommit=False,
    autoflush=False
)

logger.info("[OK] Async session factory created")

# ============================================
# FastAPI Dependency
# ============================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions
    
    Provides async database session with automatic:
    - Transaction management (commit/rollback)
    - Connection cleanup
    - Error handling
    
    Usage:
        @router.get("/activities")
        async def get_activities(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(ProcessingActivityDB))
            return result.scalars().all()
    
    Yields:
        AsyncSession: Active database session
        
    Note:
        Session is automatically committed on success and rolled back on error.
        Connection is closed in finally block.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
            logger.debug("[OK] Database session committed")
        except Exception as e:
            await session.rollback()
            logger.error(f"[ERROR] Database session rollback: {str(e)}")
            raise
        finally:
            await session.close()
            logger.debug("[OK] Database session closed")

# ============================================
# Database Health Check
# ============================================

async def check_database_connection() -> bool:
    """
    Check if database connection is healthy
    
    Returns:
        bool: True if connection successful, False otherwise
        
    Usage:
        is_healthy = await check_database_connection()
        if not is_healthy:
            raise Exception("Database connection failed")
    """
    try:
        async with async_session_maker() as session:
            await session.execute("SELECT 1")
            logger.info("[OK] Database connection healthy")
            return True
    except Exception as e:
        logger.error(f"[ERROR] Database connection failed: {str(e)}")
        return False

# ============================================
# Database Cleanup
# ============================================

async def close_database_connections():
    """
    Close all database connections gracefully
    
    Call this during application shutdown to ensure clean exit.
    
    Usage:
        @app.on_event("shutdown")
        async def shutdown():
            await close_database_connections()
    """
    try:
        await engine.dispose()
        logger.info("[OK] Database connections closed")
    except Exception as e:
        logger.error(f"[ERROR] Error closing database connections: {str(e)}")

# ============================================
# Exports
# ============================================

__all__ = [
    "engine",
    "async_session_maker",
    "get_db",
    "check_database_connection",
    "close_database_connections"
]
