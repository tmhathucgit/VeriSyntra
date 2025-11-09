"""
CRUD Operations Package for VeriSyntra Data Inventory
Vietnamese PDPL 2025 Compliance

This package provides async CRUD (Create, Read, Update, Delete) operations
for all database entities in the Data Inventory microservice.

Vietnamese-First Architecture:
- All operations validate Vietnamese primary fields (_vi NOT NULL)
- English fields (_en) are optional fallbacks
- Bilingual error messages for all operations

PDPL 2025 Compliance:
- Multi-tenant isolation enforced in all queries
- Audit trail creation for all mutations
- Tenant ownership verification before updates/deletes

Module Structure:
- processing_activity.py - Processing activity operations
- data_category.py - Data category operations
- data_subject.py - Data subject operations
- data_recipient.py - Data recipient operations
- data_retention.py - Data retention operations
- security_measure.py - Security measure operations
- processing_location.py - Processing location operations
- ropa_document.py - ROPA document operations
- audit.py - Audit trail operations

Usage:
    from crud.processing_activity import create_processing_activity
    from database import get_db
    
    @router.post("/activities")
    async def create_activity(
        request: ActivityCreate,
        db: AsyncSession = Depends(get_db)
    ):
        activity = await create_processing_activity(db, request)
        return activity
"""

__version__ = "1.0.0"

# Phase 3 imports - NOW AVAILABLE
from .processing_activity import *
from .data_category import *
from .data_subject import *
from .data_recipient import *
from .data_retention import *
from .security_measure import *
from .processing_location import *
from .ropa_document import *
from .audit import *

__all__ = [
    "__version__"
    # All module exports are re-exported via wildcard imports
]
