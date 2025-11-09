"""
Service Layer Constants - Vietnamese PDPL Compliance Platform
Defines named constants to avoid hard-coded magic values throughout service layer.

Follows VeriSyntra zero hard-coding architecture:
- All magic values replaced with descriptive constants
- Vietnamese-first with bilingual support
- Single source of truth for system defaults
"""

from uuid import UUID

# ==============================================================================
# System User Constants
# ==============================================================================

# System user for automated operations (ROPA generation, scheduled tasks)
# Used when no specific user context exists
SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

# ==============================================================================
# File Size Estimation Constants
# ==============================================================================

# Average kilobytes per processing activity in ROPA document
# Used for preview file size estimation before actual generation
AVG_KB_PER_ACTIVITY = 5

# Minimum estimated file size in KB (empty document overhead)
MIN_ESTIMATED_FILE_SIZE_KB = 10

# ==============================================================================
# Audit Log Constants
# ==============================================================================

# Audit action types for ROPA operations
AUDIT_ACTION_ROPA_GENERATED = "ropa_generated"
AUDIT_ACTION_ROPA_DELETED = "ropa_deleted"
AUDIT_ACTION_ROPA_DOWNLOADED = "ropa_downloaded"

# Audit entity types
AUDIT_ENTITY_ROPA_DOCUMENT = "ropa_document"
AUDIT_ENTITY_PROCESSING_ACTIVITY = "processing_activity"

# ==============================================================================
# Vietnamese Time Zone
# ==============================================================================

# Vietnamese timezone for all datetime operations
VIETNAM_TIMEZONE = 'Asia/Ho_Chi_Minh'

# ==============================================================================
# Exports
# ==============================================================================

__all__ = [
    'SYSTEM_USER_ID',
    'AVG_KB_PER_ACTIVITY',
    'MIN_ESTIMATED_FILE_SIZE_KB',
    'AUDIT_ACTION_ROPA_GENERATED',
    'AUDIT_ACTION_ROPA_DELETED',
    'AUDIT_ACTION_ROPA_DOWNLOADED',
    'AUDIT_ENTITY_ROPA_DOCUMENT',
    'AUDIT_ENTITY_PROCESSING_ACTIVITY',
    'VIETNAM_TIMEZONE'
]
