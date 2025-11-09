"""
SQLAlchemy Declarative Base
ORM Base Class for VeriSyntra Data Inventory Models

This module provides the declarative base class that all ORM models
inherit from. It enables SQLAlchemy's declarative mapping system.

Vietnamese-First Architecture:
- All ORM models inherit from this Base
- Supports bilingual fields (_vi NOT NULL, _en nullable)
- UUID primary keys throughout

PDPL 2025 Compliance:
- Multi-tenant isolation via tenant_id in all models
- Audit trail support
- Vietnamese timezone awareness

Usage:
    from database.base import Base
    
    class ProcessingActivityDB(Base):
        __tablename__ = "processing_activities"
        
        activity_id = Column(UUID(as_uuid=True), primary_key=True)
        # ... other columns
"""

from sqlalchemy.orm import declarative_base

# ============================================
# Declarative Base
# ============================================

# All ORM models will inherit from this Base class
Base = declarative_base()

# ============================================
# Base Class Metadata
# ============================================

# Metadata provides schema information and table management
# Used for:
# - Generating CREATE TABLE statements
# - Managing database migrations
# - Introspection and reflection

__all__ = ["Base"]
