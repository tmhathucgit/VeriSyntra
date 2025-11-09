# Database Integration Phase 1 - Schema Design Complete

**Date:** 2025-01-27  
**Document Reference:** docs/Veri_Intelligent_Data/11_Database_Integration_Implementation.md  
**Status:** [OK] Phase 1 Completed Successfully

## Phase 1 Summary

Phase 1 implemented the complete PostgreSQL database schema for VeriSyntra Data Inventory microservice, implementing PDPL 2025 (Law 91/2025/QH15) compliance requirements per Decree 13/2023/ND-CP Article 12.

## Deliverables Completed

### 1. Database Schema File
**File:** `backend/veri_ai_data_inventory/database/schema.sql`  
**Lines:** 520+ lines of SQL  
**Status:** [OK] Complete

**Contents:**
- UUID extension enablement
- 9 core tables with proper relationships
- 15+ indexes for query performance
- 20+ foreign key constraints
- Database functions and triggers
- Comprehensive SQL comments

### 2. Database Package Initialization
**File:** `backend/veri_ai_data_inventory/database/__init__.py`  
**Status:** [OK] Complete

**Contents:**
- Package documentation
- Version information
- Vietnamese-first architecture notes
- PDPL compliance notes
- Future imports preparation for Phase 2

## Database Schema Overview

### Core Tables (2 tables)

#### Table 1: processing_activities
- **Purpose:** Processing activities per Article 12.1.c
- **Primary Key:** activity_id (UUID)
- **Foreign Keys:** tenant_id
- **Key Fields:**
  - activity_name_vi (NOT NULL) / activity_name_en (nullable)
  - processing_purpose_vi (NOT NULL) / processing_purpose_en (nullable)
  - legal_basis (CHECK constraint: consent, contract, legal_obligation, etc.)
  - Compliance flags: has_sensitive_data, has_cross_border_transfer, requires_dpia
  - Vietnamese context: veri_regional_location (north/central/south)
- **Indexes:** 6 indexes (tenant, status, updated_at, sensitive, cross_border)
- **Relationships:** One-to-many with all other tables

#### Table 2: data_categories
- **Purpose:** Data categories per Article 12.1.d
- **Primary Key:** category_id (UUID)
- **Foreign Keys:** activity_id, tenant_id (CASCADE DELETE)
- **Key Fields:**
  - category_name_vi (NOT NULL) / category_name_en (nullable)
  - category_type (CHECK: personal_identifiers, contact_information, health_information, etc.)
  - data_fields_vi (TEXT[] array) / data_fields_en (TEXT[] array)
  - is_sensitive (BOOLEAN) - Article 4.8 PDPL
  - filter_scope_statement_vi / filter_scope_statement_en (Document #3 integration)
- **Indexes:** 4 indexes (activity, tenant, type, sensitive)

### Relationship Tables (3 tables)

#### Table 3: data_subjects
- **Purpose:** Data subject categories per Article 12.1.e
- **Foreign Keys:** activity_id, tenant_id (CASCADE DELETE)
- **Key Fields:** subject_category (customers, employees, children, etc.), includes_children (BOOLEAN)
- **Indexes:** 3 indexes

#### Table 4: data_recipients
- **Purpose:** Data recipients (12.1.f) and cross-border transfers (12.1.g)
- **Foreign Keys:** activity_id, tenant_id (CASCADE DELETE)
- **Key Fields:**
  - recipient_name_vi (NOT NULL) / recipient_name_en (nullable)
  - country_code, is_cross_border (BOOLEAN)
  - transfer_mechanism (Article 20: adequacy_decision, scc, bcr, consent, mps_approval)
  - safeguards_vi / safeguards_en (TEXT[] arrays)
- **Indexes:** 4 indexes (includes cross_border, country)

#### Table 5: data_retention
- **Purpose:** Retention periods per Article 12.1.h
- **Foreign Keys:** activity_id, tenant_id (CASCADE DELETE)
- **Key Fields:**
  - retention_period_vi (NOT NULL) / retention_period_en (nullable)
  - retention_period_days (INTEGER) - normalized for calculations
  - deletion_method (secure_deletion, anonymization, archival)
  - next_review_date (DATE)
- **Constraint:** One retention per activity (UNIQUE)
- **Indexes:** 3 indexes

### Supporting Tables (4 tables)

#### Table 6: security_measures
- **Purpose:** Security measures per Article 12.1.i
- **Key Fields:** measure_type (encryption, access_control, monitoring, etc.)
- **Indexes:** 3 indexes

#### Table 7: processing_locations
- **Purpose:** Processing locations per Article 12.1.j
- **Key Fields:** location_type (on_premise, cloud, hybrid), data_center_region (north/central/south)
- **Indexes:** 3 indexes

#### Table 8: ropa_documents
- **Purpose:** Generated ROPA documents tracking
- **Key Fields:**
  - document_format (json, csv, pdf, mps_format)
  - mps_compliant, mps_submitted, mps_reference_number
  - veri_business_context (JSONB)
- **Indexes:** 4 indexes

#### Table 9: data_inventory_audit
- **Purpose:** Audit trail per Article 43 PDPL
- **Key Fields:**
  - action_type, entity_type, entity_id
  - old_values / new_values (JSONB)
  - audit_message_vi / audit_message_en
  - vietnam_time (Asia/Ho_Chi_Minh timezone)
- **Indexes:** 5 indexes

## Database Functions

### Function 1: update_updated_at_column()
- **Purpose:** Automatic timestamp updates on UPDATE
- **Trigger:** Processing_activities table
- **Language:** PL/pgSQL

### Function 2: get_vietnam_time()
- **Purpose:** UTC to Vietnamese time conversion
- **Input:** TIMESTAMP (UTC)
- **Output:** TIMESTAMP (Asia/Ho_Chi_Minh)
- **Language:** PL/pgSQL

## Vietnamese-First Architecture Compliance

[OK] All bilingual fields follow Vietnamese-first pattern:
- `*_vi` fields: NOT NULL (Vietnamese primary)
- `*_en` fields: Nullable (English fallback)
- Database identifiers: ASCII-safe (diacritics omitted for compatibility)

**Examples:**
```sql
activity_name_vi VARCHAR(200) NOT NULL,  -- Vietnamese primary
activity_name_en VARCHAR(200),           -- English fallback

processing_purpose_vi TEXT NOT NULL,  -- Vietnamese primary
processing_purpose_en TEXT,           -- English fallback

data_fields_vi TEXT[] DEFAULT '{}',  -- Vietnamese primary (PostgreSQL TEXT[])
data_fields_en TEXT[] DEFAULT '{}',  -- English fallback (PostgreSQL TEXT[])
```

## PDPL 2025 Compliance Coverage

[OK] All Decree 13/2023/ND-CP Article 12 mandatory fields implemented:

- **Article 12.1.a:** Processing purpose (processing_purpose_vi/en)
- **Article 12.1.b:** Legal basis (legal_basis with CHECK constraint)
- **Article 12.1.c:** Activity details (activity_name_vi/en, description)
- **Article 12.1.d:** Data categories (data_categories table)
- **Article 12.1.e:** Data subjects (data_subjects table)
- **Article 12.1.f:** Data recipients (data_recipients table)
- **Article 12.1.g:** Cross-border transfers (is_cross_border, transfer_mechanism)
- **Article 12.1.h:** Retention periods (data_retention table)
- **Article 12.1.i:** Security measures (security_measures table)
- **Article 12.1.j:** Processing locations (processing_locations table)
- **Article 43:** Audit trail (data_inventory_audit table)

## Multi-Tenant Isolation

[OK] All tables enforce row-level tenant isolation:
- Every table has `tenant_id UUID NOT NULL REFERENCES tenants(tenant_id)`
- Foreign key constraints: `ON DELETE CASCADE`
- Indexes on tenant_id for query performance
- Application-level queries MUST filter by tenant_id

## Performance Optimization

**Total Indexes:** 30+ indexes across 9 tables

**Index Strategy:**
- Primary keys: UUID (11 indexes)
- Foreign keys: tenant_id, activity_id (18 indexes)
- Filtering columns: status, is_sensitive, is_cross_border (7 indexes)
- Sorting columns: timestamp DESC, generated_at DESC (3 indexes)

**Expected Query Performance:**
- Single activity lookup: O(1) via UUID primary key
- Tenant activity list: O(log n) via tenant_id index
- Filtered queries: O(log n) via composite indexes
- Audit trail: O(log n) via timestamp DESC index

## Data Type Decisions

### TEXT[] vs JSONB

**TEXT[] Arrays Used For:**
- `data_fields_vi` / `data_fields_en` - Bilingual field name lists
- `safeguards_vi` / `safeguards_en` - Bilingual safeguard measure lists

**Rationale:**
- Simple string lists with no nested structure
- Easier to query with PostgreSQL array operators
- Better performance for simple lists
- Natural mapping to Python lists

**JSONB Used For:**
- `generation_parameters` - Flexible ROPA generation config
- `veri_business_context` - Vietnamese business context object
- `old_values` / `new_values` - Audit trail change tracking

**Rationale:**
- Complex nested objects
- Flexible schema requirements
- Need for key-value access patterns

## Constraints and Data Integrity

**CHECK Constraints:** 15+ constraints across tables
- legal_basis values (6 options)
- recipient_type values (5 options)
- transfer_mechanism values (5 options)
- deletion_method values (3 options)
- Action_type values (7 options)
- Entity_type values (8 options)

**UNIQUE Constraints:** 5 constraints
- processing_activities: (tenant_id, activity_name_vi)
- data_categories: (activity_id, category_name_vi)
- data_subjects: (activity_id, subject_category)
- data_recipients: (activity_id, recipient_name_vi, country_code)
- data_retention: (activity_id) - one retention per activity

**Foreign Key Constraints:** 18+ CASCADE DELETE relationships
- Ensures referential integrity
- Automatic cleanup when parent records deleted
- Multi-tenant isolation enforcement

## Testing Requirements for Phase 2

When implementing Phase 2 (ORM models), verify:

1. **Schema Creation:**
   - Run schema.sql against PostgreSQL database
   - Verify all tables created successfully
   - Check all indexes exist
   - Verify triggers and functions work

2. **Data Integrity:**
   - Test CASCADE DELETE behavior
   - Verify UNIQUE constraints prevent duplicates
   - Test CHECK constraints reject invalid values
   - Confirm foreign key constraints enforce relationships

3. **Vietnamese-First Validation:**
   - Confirm _vi fields are NOT NULL
   - Confirm _en fields allow NULL
   - Test bilingual data insertion and retrieval

4. **Multi-Tenant Isolation:**
   - Create data for tenant A
   - Verify tenant B cannot access tenant A's data
   - Test CASCADE DELETE when tenant deleted

## Phase 1 Completion Checklist

- [OK] 9 tables defined with proper structure
- [OK] All PDPL Article 12 fields covered (12.1.a through 12.1.j)
- [OK] Multi-tenant isolation with tenant_id foreign keys
- [OK] Vietnamese-first bilingual architecture (_vi NOT NULL, _en nullable)
- [OK] Database identifiers use ASCII-safe names (no diacritics)
- [OK] Performance indexes on all query patterns
- [OK] CASCADE DELETE for referential integrity
- [OK] CHECK constraints for data validation
- [OK] UNIQUE constraints prevent duplicates
- [OK] Database functions for timestamps and Vietnamese time
- [OK] Triggers for automatic updated_at
- [OK] Comprehensive SQL comments
- [OK] TEXT[] arrays for bilingual string lists
- [OK] JSONB for flexible business context
- [OK] Audit trail with old/new values tracking

## Next Phase: Phase 2 - ORM Models

**Estimated Duration:** 3-4 hours

**Deliverables:**
1. `database/connection.py` - Async SQLAlchemy engine + session factory
2. `database/base.py` - Declarative base class
3. `models/db_models.py` - 9 SQLAlchemy ORM classes
4. Relationships with back_populates and cascade deletes
5. UUID type mapping for PostgreSQL
6. TEXT[] and JSONB type handling

**Key Patterns:**
- AsyncSession for all database operations
- relationship() with back_populates for bidirectional access
- CASCADE delete in both SQL schema and ORM relationships
- Vietnamese-first field validation in ORM layer

## Files Created

1. `backend/veri_ai_data_inventory/database/schema.sql` (520+ lines)
2. `backend/veri_ai_data_inventory/database/__init__.py` (50 lines)

**Total:** 2 files, 570+ lines of code

---

**Phase 1 Status:** [OK] COMPLETE  
**Phase 2 Status:** Ready to begin  
**Next Action:** Proceed to Phase 2 - ORM Models creation

---

*Vietnamese-First Compliance Platform*  
*PDPL 2025 (Law 91/2025/QH15)*  
*Decree 13/2023/ND-CP Article 12*
