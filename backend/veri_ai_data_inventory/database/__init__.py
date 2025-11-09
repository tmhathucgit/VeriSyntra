"""
VeriSyntra Data Inventory Database Package
PostgreSQL Database Integration for PDPL 2025 Compliance

This package provides database schema, connections, and session management
for the Data Inventory microservice.

Vietnamese-First Architecture:
- _vi fields: NOT NULL (Vietnamese primary)
- _en fields: Nullable (English fallback)
- Database identifiers: May omit diacritics for ASCII compatibility

PDPL 2025 Compliance:
- Implements Decree 13/2023/ND-CP Article 12 requirements
- Multi-tenant row-level isolation
- Complete audit trail per Article 43
- Vietnamese timezone support (Asia/Ho_Chi_Minh)

Database Schema:
- 9 core tables for ROPA generation
- TEXT[] arrays for bilingual string lists
- JSONB for flexible business context
- UUID foreign keys for tenant isolation

Usage:
    from database import get_db
    
    @router.get("/endpoint")
    async def endpoint(db: AsyncSession = Depends(get_db)):
        # Database session available
        ...
"""

__version__ = "1.0.0"
__author__ = "VeriSyntra Development Team"

# Phase 2 imports - NOW AVAILABLE
from .connection import engine, async_session_maker, get_db, check_database_connection, close_database_connections
from .base import Base

__all__ = [
    "__version__",
    # Connection
    "engine",
    "async_session_maker",
    "get_db",
    "check_database_connection",
    "close_database_connections",
    # Base
    "Base"
]
