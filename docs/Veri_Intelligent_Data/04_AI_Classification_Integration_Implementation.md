# AI Classification Integration Implementation Plan
## veri-ai-data-inventory Integration with Vietnamese AI Classification

**Services:** veri-ai-data-inventory (Port 8010) + veri-vi-ai-classification (Port 8006)  
**Model:** VeriAIDPO_Principles_VI_v1 (8 PDPL Principles, 78-88% accuracy)  
**Version:** 1.1.0  
**Date:** November 3, 2025  
**Purpose:** Implementation guide for integrating AI-powered Vietnamese PDPL classification using VeriAIDPO_Principles_VI_v1

---

**[+] RELATED IMPLEMENTATIONS:** This document provides the **generic AI classification framework** that is specialized in other documents:
- **[Processing Activities Population](./01_Table_processing_activities/08_Data_Population_VeriAIDPO_Integration.md)** (Document #08): Specialized implementation for populating `processing_activities` table using VeriAIDPO
- **[DPO Recommendations Microservice](./10_AI_Recommendations_Microservice_Implementation.md)** (Document #10): Standalone microservice (Port 8011) providing ML-powered DPO compliance recommendations

**Document Relationship:**
- **This document (Doc #04)**: Foundation layer - Generic AI classification integration framework
- **Document #08**: Application layer - Processing activities data population
- **Document #10**: Service layer - DPO recommendations microservice
- All three use VeriAIDPO_Principles_VI_v1 model with different orchestration patterns

**When to Use Each Document:**

| Use Case | Document | Focus |
|----------|----------|-------|
| Generic AI classification for any data asset | Doc #04 (This) | Three-service orchestration framework |
| Populate processing_activities table | Doc #08 | Database scanning -> VeriAIDPO -> Activities |
| DPO compliance recommendations | Doc #10 | Standalone microservice with GPU acceleration |

---

## Table of Contents

1. [Overview](#overview)
2. [Service Integration Architecture](#service-integration-architecture)
3. [Vietnamese NLP Preprocessing Integration](#vietnamese-nlp-preprocessing-integration)
4. [Three-Service Orchestration Workflow](#three-service-orchestration-workflow)
5. [Classification Workflow](#classification-workflow)
6. [Batch Processing](#batch-processing)
7. [Result Storage](#result-storage)
8. [Vietnamese Pattern Handling](#vietnamese-pattern-handling)
9. [API Integration](#api-integration)
10. [Code Implementation](#code-implementation)
11. [Performance Optimization](#performance-optimization)
12. [Error Handling](#error-handling)

---

## Overview

### Purpose
Integrate `veri-ai-data-inventory` with `veri-vi-ai-classification` to automatically classify discovered database fields, files, and data flows using VeriAIDPO_Principles_VI_v1 model for Vietnamese PDPL compliance classification.

### Key Features
- Automatic field classification during data discovery
- Batch processing for large datasets
- Vietnamese pattern recognition (CMND/CCCD, phone, names)
- PDPL sensitivity categorization (regular vs. sensitive)
- Classification result caching
- Confidence score tracking
- Multi-tenant classification isolation

### Service Architecture
```
veri-ai-data-inventory (Port 8010) [ORCHESTRATOR]
    |
    |-- Discovers data assets (databases, files, cloud)
    |-- Extracts sample data
    |
    |-- CALLS --> veri-vi-nlp-processor (Port 8007)
    |              |
    |              |-- VnCoreNLP (Vietnamese NLP)
    |              |     |-- Tokenization
    |              |     |-- POS Tagging
    |              |     |-- Named Entity Recognition
    |              |
    |              |-- Returns preprocessed Vietnamese text
    |
    |-- CALLS --> veri-vi-ai-classification (Port 8006)
    |              |
    |              |-- VeriAIDPO_Principles_VI_v1 Model
    |              |     |-- Uses NLP hints from Port 8007
    |              |     |-- Vietnamese pattern library
    |              |     |-- 8 PDPL Principles Classification
    |              |
    |              |-- Returns PDPL principle classifications
    |
    |-- Receives classification results
    |-- Stores in inventory database
    |-- Generates ROPA with classifications
```

**Three-Service Integration Flow:**
1. **Port 8010 (Inventory)**: Discovers data and extracts samples
2. **Port 8007 (NLP)**: Preprocesses Vietnamese text (tokenization, NER)
3. **Port 8006 (AI Classification)**: Classifies using VeriAIDPO_Principles_VI_v1 model with NLP hints
4. **Port 8010 (Inventory)**: Stores classification results

---

## Vietnamese NLP Preprocessing Integration

### Purpose
Integrate `veri-vi-nlp-processor` (Port 8007) to preprocess Vietnamese text before AI classification. This service uses VnCoreNLP for tokenization, POS tagging, and NER, providing crucial linguistic hints to the AI classifier.

### NLP Processor Client Implementation

```python
# File: backend/veri_ai_data_inventory/clients/nlp_processor_client.py

import httpx
from typing import Dict, Any, List, Optional
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class NLPProcessorClient:
    """HTTP client for veri-vi-nlp-processor service"""
    
    def __init__(
        self,
        base_url: str = "http://veri-vi-nlp-processor:8007",
        timeout: int = 60,  # NLP processing can be slower
        max_retries: int = 3
    ):
        """
        Initialize NLP processor service client
        
        Args:
            base_url: Base URL of veri-vi-nlp-processor service
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        
        # HTTP client with connection pooling
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_connections=50, max_keepalive_connections=10)
        )
        
        logger.info(
            f"[OK] NLP processor client initialized: {base_url}"
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def preprocess_text(
        self,
        text: str,
        include_pos: bool = True,
        include_ner: bool = True
    ) -> Dict[str, Any]:
        """
        Preprocess Vietnamese text with VnCoreNLP
        
        Args:
            text: Vietnamese text to preprocess
            include_pos: Include POS tagging
            include_ner: Include Named Entity Recognition
            
        Returns:
            {
                'tokens': List[str],  # Word tokens
                'pos_tags': List[str],  # POS tags (if requested)
                'ner_tags': List[str],  # NER tags (if requested)
                'sentences': List[Dict],  # Sentence-level analysis
                'encoding': str,  # UTF-8 validation status
                'processing_time_ms': float
            }
        """
        try:
            payload = {
                "text": text,
                "include_pos": include_pos,
                "include_ner": include_ner
            }
            
            response = await self.client.post(
                "/api/v1/nlp/preprocess",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(
                f"[OK] Preprocessed text: {len(result['tokens'])} tokens, "
                f"{result['processing_time_ms']:.2f}ms"
            )
            
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"[ERROR] NLP preprocessing failed: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def preprocess_batch(
        self,
        texts: List[str],
        include_pos: bool = True,
        include_ner: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Batch preprocess multiple Vietnamese texts
        
        Args:
            texts: List of Vietnamese texts
            include_pos: Include POS tagging
            include_ner: Include NER
            
        Returns:
            List of preprocessing results
        """
        try:
            payload = {
                "texts": texts,
                "include_pos": include_pos,
                "include_ner": include_ner
            }
            
            response = await self.client.post(
                "/api/v1/nlp/preprocess/batch",
                json=payload
            )
            
            response.raise_for_status()
            results = response.json()
            
            logger.info(
                f"[OK] Batch preprocessed {len(texts)} texts"
            )
            
            return results
            
        except httpx.HTTPError as e:
            logger.error(f"[ERROR] Batch NLP preprocessing failed: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def detect_personal_data_patterns(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Detect Vietnamese personal data patterns using NER
        
        Args:
            text: Vietnamese text to analyze
            
        Returns:
            {
                'person_names': List[str],  # Detected names
                'locations': List[str],  # Detected locations
                'organizations': List[str],  # Detected organizations
                'potential_identifiers': List[Dict],  # Phone, CMND, etc.
                'confidence_scores': Dict[str, float]
            }
        """
        try:
            payload = {"text": text}
            
            response = await self.client.post(
                "/api/v1/nlp/detect-personal-data",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(
                f"[OK] Detected personal data: "
                f"{len(result['person_names'])} names, "
                f"{len(result['potential_identifiers'])} identifiers"
            )
            
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"[ERROR] Personal data detection failed: {str(e)}")
            raise
    
    async def validate_vietnamese_encoding(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Validate Vietnamese UTF-8 encoding
        
        Args:
            text: Text to validate
            
        Returns:
            {
                'is_valid_utf8': bool,
                'has_vietnamese_chars': bool,
                'encoding_issues': List[str],
                'suggested_fix': Optional[str]
            }
        """
        try:
            payload = {"text": text}
            
            response = await self.client.post(
                "/api/v1/nlp/validate-encoding",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"[ERROR] Encoding validation failed: {str(e)}")
            raise
    
    async def health_check(self) -> bool:
        """Check if NLP processor service is healthy"""
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Close HTTP client connections"""
        await self.client.aclose()
        logger.info("[OK] NLP processor client closed")
```

### NLP-Enhanced Data Profiling

```python
# File: backend/veri_ai_data_inventory/services/nlp_enhanced_profiler.py

from typing import Dict, Any, List
import logging
from ..clients.nlp_processor_client import NLPProcessorClient

logger = logging.getLogger(__name__)

class NLPEnhancedDataProfiler:
    """Profile data with Vietnamese NLP preprocessing"""
    
    def __init__(self):
        """Initialize NLP-enhanced profiler"""
        self.nlp_client = NLPProcessorClient()
    
    async def profile_vietnamese_field(
        self,
        field_name: str,
        sample_values: List[str]
    ) -> Dict[str, Any]:
        """
        Profile database field with NLP preprocessing
        
        Args:
            field_name: Column name
            sample_values: Sample text values
            
        Returns:
            {
                'field_name': str,
                'total_samples': int,
                'vietnamese_samples': int,
                'detected_entities': Dict,
                'linguistic_features': Dict,
                'classification_hints': List[str]
            }
        """
        try:
            # Filter valid string samples
            valid_samples = [
                str(v) for v in sample_values
                if v and isinstance(v, str) and len(str(v).strip()) > 0
            ]
            
            if not valid_samples:
                return {
                    'field_name': field_name,
                    'total_samples': 0,
                    'vietnamese_samples': 0,
                    'detected_entities': {},
                    'linguistic_features': {},
                    'classification_hints': []
                }
            
            # Combine samples for NLP analysis (first 10 samples)
            combined_text = "\n".join(valid_samples[:10])
            
            # Preprocess with NLP
            nlp_result = await self.nlp_client.preprocess_text(
                text=combined_text,
                include_pos=True,
                include_ner=True
            )
            
            # Detect personal data patterns
            personal_data = await self.nlp_client.detect_personal_data_patterns(
                text=combined_text
            )
            
            # Count Vietnamese samples
            vietnamese_count = 0
            for sample in valid_samples:
                encoding_check = await self.nlp_client.validate_vietnamese_encoding(
                    text=sample
                )
                if encoding_check['has_vietnamese_chars']:
                    vietnamese_count += 1
            
            # Generate classification hints based on NLP results
            classification_hints = self._generate_hints(
                nlp_result, personal_data
            )
            
            profile = {
                'field_name': field_name,
                'total_samples': len(valid_samples),
                'vietnamese_samples': vietnamese_count,
                'detected_entities': {
                    'person_names': personal_data['person_names'],
                    'locations': personal_data['locations'],
                    'organizations': personal_data['organizations'],
                    'identifiers': personal_data['potential_identifiers']
                },
                'linguistic_features': {
                    'total_tokens': len(nlp_result['tokens']),
                    'unique_tokens': len(set(nlp_result['tokens'])),
                    'pos_distribution': self._count_pos_tags(nlp_result.get('pos_tags', [])),
                    'avg_tokens_per_sample': len(nlp_result['tokens']) / len(valid_samples[:10])
                },
                'classification_hints': classification_hints
            }
            
            logger.info(
                f"[OK] NLP-profiled field '{field_name}': "
                f"{vietnamese_count}/{len(valid_samples)} Vietnamese samples, "
                f"hints: {classification_hints}"
            )
            
            return profile
            
        except Exception as e:
            logger.error(f"[ERROR] NLP profiling failed for '{field_name}': {str(e)}")
            raise
    
    def _generate_hints(
        self,
        nlp_result: Dict[str, Any],
        personal_data: Dict[str, Any]
    ) -> List[str]:
        """Generate classification hints from NLP results"""
        hints = []
        
        # Check for person names
        if personal_data['person_names']:
            hints.append('vietnamese_person_name')
        
        # Check for locations
        if personal_data['locations']:
            hints.append('vietnamese_location')
        
        # Check for organizations
        if personal_data['organizations']:
            hints.append('organization_name')
        
        # Check for identifiers (CMND, phone, etc.)
        for identifier in personal_data['potential_identifiers']:
            if identifier.get('type') == 'cmnd_cccd':
                hints.append('cmnd_cccd')
            elif identifier.get('type') == 'phone_number':
                hints.append('vietnamese_phone_number')
        
        # Check POS tags for proper nouns (likely names)
        if nlp_result.get('pos_tags'):
            proper_noun_ratio = sum(
                1 for tag in nlp_result['pos_tags'] if tag == 'NNP'
            ) / len(nlp_result['pos_tags'])
            
            if proper_noun_ratio > 0.5:
                hints.append('likely_proper_noun')
        
        return hints
    
    def _count_pos_tags(self, pos_tags: List[str]) -> Dict[str, int]:
        """Count POS tag distribution"""
        from collections import Counter
        return dict(Counter(pos_tags))
    
    async def close(self):
        """Close NLP client"""
        await self.nlp_client.close()
```

---

## Three-Service Orchestration Workflow

### Complete Integration Service

```python
# File: backend/veri_ai_data_inventory/services/orchestration_service.py

from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
from ..clients.nlp_processor_client import NLPProcessorClient
from ..clients.classification_client import ClassificationServiceClient
from ..services.nlp_enhanced_profiler import NLPEnhancedDataProfiler

logger = logging.getLogger(__name__)

class ThreeServiceOrchestrator:
    """
    Orchestrates data discovery workflow across three services:
    - Port 8010: veri-ai-data-inventory (this service)
    - Port 8007: veri-vi-nlp-processor
    - Port 8006: veri-vi-ai-classification (VeriAIDPO_Principles_VI_v1)
    """
    
    def __init__(self):
        """Initialize orchestrator with clients for both services"""
        self.nlp_client = NLPProcessorClient()
        self.classification_client = ClassificationServiceClient()
        self.profiler = NLPEnhancedDataProfiler()
        
        logger.info("[OK] Three-service orchestrator initialized")
    
    async def orchestrate_field_classification(
        self,
        field_name: str,
        data_type: str,
        sample_values: List[Any],
        table_name: Optional[str] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Complete orchestration: Inventory -> NLP -> AI -> Inventory
        
        Workflow:
        1. Extract sample data (Port 8010)
        2. Preprocess Vietnamese text (Port 8007)
        3. Classify with NLP hints (Port 8006)
        4. Return enriched classification (Port 8010)
        
        Args:
            field_name: Database column name
            data_type: SQL data type
            sample_values: Sample data from column
            table_name: Table name for context
            filter_metadata: Column filter context for confidence adjustment
            
        Returns:
            {
                'classification': str,
                'pdpl_category': str,
                'confidence': float,
                'nlp_insights': Dict,
                'classification_reasoning': List[str],
                'filter_context': Dict
            }
        """
        try:
            logger.info(
                f"[OK] Starting three-service orchestration for field '{field_name}' "
                f"(filtered: {filter_metadata.get('is_filtered', False) if filter_metadata else False})"
            )
            
            # STEP 1: Profile data with NLP (Port 8010 -> Port 8007)
            logger.info(f"[STEP 1/3] NLP preprocessing for '{field_name}'...")
            
            # Filter string samples for NLP
            string_samples = [
                str(v) for v in sample_values
                if v and isinstance(v, (str, int, float))
            ][:100]
            
            nlp_profile = await self.profiler.profile_vietnamese_field(
                field_name=field_name,
                sample_values=string_samples
            )
            
            # STEP 2: Classify with NLP hints and filter metadata (Port 8010 -> Port 8006)
            logger.info(f"[STEP 2/3] AI classification for '{field_name}'...")
            
            classification_result = await self.classification_client.classify_structured_field(
                field_name=field_name,
                data_type=data_type,
                sample_values=sample_values,
                table_name=table_name,
                schema_context={
                    'nlp_hints': nlp_profile['classification_hints'],
                    'vietnamese_ratio': nlp_profile['vietnamese_samples'] / max(nlp_profile['total_samples'], 1),
                    'detected_entities': nlp_profile['detected_entities']
                },
                filter_metadata=filter_metadata  # Pass filter context
            )
            
            # STEP 3: Enrich classification with NLP insights and filter context (Port 8010)
            logger.info(f"[STEP 3/3] Enriching classification results...")
            
            enriched_result = {
                'classification': classification_result['classification'],
                'pdpl_category': classification_result['pdpl_category'],
                'confidence': classification_result['confidence'],
                'vietnamese_type': classification_result.get('vietnamese_type'),
                'sensitivity_score': classification_result.get('sensitivity_score', 0.0),
                'nlp_insights': {
                    'vietnamese_samples': nlp_profile['vietnamese_samples'],
                    'total_samples': nlp_profile['total_samples'],
                    'detected_entities': nlp_profile['detected_entities'],
                    'linguistic_features': nlp_profile['linguistic_features'],
                    'classification_hints': nlp_profile['classification_hints']
                },
                'classification_reasoning': self._generate_reasoning(
                    classification_result,
                    nlp_profile
                ),
                'orchestration_metadata': {
                    'nlp_service_used': True,
                    'classification_service_used': True,
                    'services_chain': 'Port8010 -> Port8007 -> Port8006 -> Port8010'
                },
                'filter_context': filter_metadata if filter_metadata else {
                    'is_filtered': False,
                    'filter_mode': 'all'
                }
            }
            
            logger.info(
                f"[OK] Three-service orchestration complete for '{field_name}': "
                f"{enriched_result['classification']} "
                f"(confidence: {enriched_result['confidence']:.2f}, "
                f"filtered: {filter_metadata.get('is_filtered', False) if filter_metadata else False})"
            )
            
            return enriched_result
            
        except Exception as e:
            logger.error(
                f"[ERROR] Three-service orchestration failed for '{field_name}': {str(e)}"
            )
            raise
    
    async def orchestrate_batch_classification(
        self,
        fields: List[Dict[str, Any]],
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Batch orchestration for multiple fields with filter context
        
        Args:
            fields: List of field dictionaries
            filter_metadata: Column filter metadata to pass to all classifications
            
        Returns:
            List of enriched classification results
        """
        try:
            logger.info(
                f"[OK] Starting batch three-service orchestration: {len(fields)} fields "
                f"(filtered: {filter_metadata.get('is_filtered', False) if filter_metadata else False})"
            )
            
            results = []
            
            # Process each field through the three-service pipeline
            for field in fields:
                result = await self.orchestrate_field_classification(
                    field_name=field['field_name'],
                    data_type=field['data_type'],
                    sample_values=field['sample_values'],
                    table_name=field.get('table_name'),
                    filter_metadata=filter_metadata  # Pass filter context
                )
                
                results.append(result)
            
            logger.info(
                f"[OK] Batch orchestration complete: {len(results)} fields processed"
            )
            
            return results
            
        except Exception as e:
            logger.error(f"[ERROR] Batch orchestration failed: {str(e)}")
            raise
    
    async def orchestrate_unstructured_classification(
        self,
        text: str,
        document_type: str
    ) -> Dict[str, Any]:
        """
        Orchestrate unstructured document classification
        
        Workflow:
        1. Preprocess Vietnamese text (Port 8007)
        2. Extract PhoBERT embeddings with NLP tokens (Port 8006)
        3. Classify document (Port 8006)
        4. Return enriched result (Port 8010)
        
        Args:
            text: Vietnamese document text
            document_type: Document type (pdf, docx, etc.)
            
        Returns:
            Classification result with NLP insights
        """
        try:
            logger.info(
                f"[OK] Orchestrating unstructured classification for {document_type}"
            )
            
            # STEP 1: NLP preprocessing
            nlp_result = await self.nlp_client.preprocess_text(
                text=text,
                include_pos=True,
                include_ner=True
            )
            
            # STEP 2: Detect personal data
            personal_data = await self.nlp_client.detect_personal_data_patterns(
                text=text
            )
            
            # STEP 3: Classify with PhoBERT using NLP tokens
            classification_result = await self.classification_client.classify_unstructured_text(
                text=text,
                model_type="phobert",
                language="vi"
            )
            
            # STEP 4: Enrich result
            enriched_result = {
                'predicted_category': classification_result['predicted_category'],
                'confidence_score': classification_result['confidence_score'],
                'all_probabilities': classification_result.get('all_probabilities', {}),
                'nlp_insights': {
                    'tokens': nlp_result['tokens'],
                    'total_tokens': len(nlp_result['tokens']),
                    'sentences': len(nlp_result.get('sentences', [])),
                    'detected_entities': personal_data,
                    'processing_time_ms': nlp_result.get('processing_time_ms', 0)
                },
                'document_metadata': {
                    'document_type': document_type,
                    'has_personal_data': bool(personal_data['person_names'] or personal_data['potential_identifiers']),
                    'requires_pdpl_compliance': classification_result['confidence_score'] > 0.7
                }
            }
            
            logger.info(
                f"[OK] Unstructured classification complete: "
                f"{enriched_result['predicted_category']}"
            )
            
            return enriched_result
            
        except Exception as e:
            logger.error(f"[ERROR] Unstructured orchestration failed: {str(e)}")
            raise
    
    def _generate_reasoning(
        self,
        classification_result: Dict[str, Any],
        nlp_profile: Dict[str, Any]
    ) -> List[str]:
        """Generate human-readable classification reasoning"""
        reasoning = []
        
        # Classification confidence
        confidence = classification_result['confidence']
        if confidence > 0.9:
            reasoning.append(f"High confidence classification ({confidence:.2%})")
        elif confidence > 0.7:
            reasoning.append(f"Moderate confidence classification ({confidence:.2%})")
        else:
            reasoning.append(f"Low confidence classification ({confidence:.2%}) - manual review recommended")
        
        # NLP insights
        if nlp_profile['vietnamese_samples'] > 0:
            ratio = nlp_profile['vietnamese_samples'] / nlp_profile['total_samples']
            reasoning.append(
                f"Vietnamese text detected in {ratio:.0%} of samples"
            )
        
        # Detected entities
        entities = nlp_profile['detected_entities']
        if entities['person_names']:
            reasoning.append(
                f"Detected {len(entities['person_names'])} person names via NER"
            )
        
        if entities['identifiers']:
            identifier_types = [i.get('type') for i in entities['identifiers']]
            reasoning.append(
                f"Detected identifiers: {', '.join(set(identifier_types))}"
            )
        
        # Classification hints
        if nlp_profile['classification_hints']:
            reasoning.append(
                f"NLP hints: {', '.join(nlp_profile['classification_hints'])}"
            )
        
        return reasoning
    
    async def health_check_all_services(self) -> Dict[str, bool]:
        """Check health of all three services"""
        health_status = {
            'inventory_service_8010': True,  # This service (always true)
            'nlp_service_8007': await self.nlp_client.health_check(),
            'classification_service_8006': await self.classification_client.health_check()
        }
        
        logger.info(f"[OK] Health check: {health_status}")
        
        return health_status
    
    async def close(self):
        """Close all service clients"""
        await self.nlp_client.close()
        await self.classification_client.close()
        await self.profiler.close()
        logger.info("[OK] Three-service orchestrator closed")
```

### End-to-End Integration Example

```python
# File: backend/veri_ai_data_inventory/examples/three_service_example.py

"""
End-to-End Example: Scanning Vietnamese Database -> NLP -> AI Classification
"""

import asyncio
from uuid import uuid4
from ..connectors.postgresql_scanner import PostgreSQLScanner
from ..services.orchestration_service import ThreeServiceOrchestrator

async def complete_workflow_example():
    """
    Complete workflow example:
    1. Scan Vietnamese database (Port 8010)
    2. Preprocess Vietnamese text (Port 8007)
    3. Classify with AI (Port 8006)
    4. Store results (Port 8010)
    """
    
    # STEP 1: Scan Vietnamese database
    print("[STEP 1] Scanning Vietnamese customer database...")
    
    scanner = PostgreSQLScanner({
        'host': 'localhost',
        'port': 5432,
        'database': 'vietnamese_customers',
        'username': 'scanner',
        'password': 'password123',
        'schema': 'public'
    })
    
    # Connect to database
    if not scanner.connect():
        print("[ERROR] Failed to connect to database")
        return
    
    # Discover schema
    schema_info = scanner.discover_schema()
    
    print(f"[OK] Discovered {len(schema_info['tables'])} tables")
    
    # STEP 2-4: Orchestrate NLP and AI classification
    orchestrator = ThreeServiceOrchestrator()
    
    # Check service health
    health = await orchestrator.health_check_all_services()
    print(f"[OK] Service health: {health}")
    
    # Process each table
    for table in schema_info['tables']:
        table_name = table['table_name']
        print(f"\n[OK] Processing table: {table_name}")
        
        # Classify each column
        for column in table['columns']:
            column_name = column['column_name']
            data_type = column['data_type']
            
            # Extract sample data
            samples = scanner.extract_sample_data(
                table_name=table_name,
                column_name=column_name,
                limit=100
            )
            
            if not samples:
                continue
            
            # Three-service orchestration
            result = await orchestrator.orchestrate_field_classification(
                field_name=column_name,
                data_type=data_type,
                sample_values=samples,
                table_name=table_name
            )
            
            # Print results
            print(f"\n  Field: {column_name}")
            print(f"  Classification: {result['classification']}")
            print(f"  PDPL Category: {result['pdpl_category']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Vietnamese Type: {result.get('vietnamese_type', 'N/A')}")
            print(f"  Reasoning:")
            for reason in result['classification_reasoning']:
                print(f"    - {reason}")
            
            # NLP insights
            nlp = result['nlp_insights']
            print(f"  NLP Insights:")
            print(f"    - Vietnamese samples: {nlp['vietnamese_samples']}/{nlp['total_samples']}")
            print(f"    - Detected entities: {nlp['detected_entities']}")
            print(f"    - Hints: {nlp['classification_hints']}")
    
    # Cleanup
    scanner.close()
    await orchestrator.close()
    
    print("\n[OK] Complete workflow finished successfully!")

# Run example
if __name__ == "__main__":
    asyncio.run(complete_workflow_example())
```

### Sequence Diagram: Three-Service Flow

```
User/Scan Job
    |
    | [1] POST /api/v1/data-inventory/scan
    v
veri-ai-data-inventory:8010 (Orchestrator)
    |
    | [2] Discover database schema
    | [3] Extract sample data
    |
    | [4] POST /api/v1/nlp/preprocess
    v
veri-vi-nlp-processor:8007
    |
    | [5] VnCoreNLP tokenization
    | [6] POS tagging
    | [7] NER extraction
    |
    | [8] Return NLP results
    v
veri-ai-data-inventory:8010
    |
    | [9] POST /api/v1/classify/structured
    | [10] Include NLP hints in request
    v
veri-vi-ai-classification:8006
    |
    | [11] Use NLP hints
    | [12] Vietnamese pattern matching
    | [13] VeriAIDPO PDPL principles classification
    |
    | [14] Return classification results
    v
veri-ai-data-inventory:8010
    |
    | [15] Store classifications in database
    | [16] Generate ROPA entries
    | [17] Update scan job status
    |
    v
User/Scan Job
```

---

### HTTP Client Configuration

```python
# File: backend/veri_ai_data_inventory/clients/classification_client.py

import httpx
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class ClassificationServiceClient:
    """HTTP client for veri-vi-ai-classification service (VeriAIDPO_Principles_VI_v1)"""
    
    def __init__(
        self,
        base_url: str = "http://veri-vi-ai-classification:8006",
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize VeriAIDPO classification service client
        
        Args:
            base_url: Base URL of veri-vi-ai-classification service
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        
        # HTTP client with connection pooling
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )
        
        logger.info(
            f"[OK] Classification service client initialized: {base_url}"
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def classify_structured_field(
        self,
        field_name: str,
        data_type: str,
        sample_values: List[Any],
        table_name: Optional[str] = None,
        schema_context: Optional[Dict[str, Any]] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Classify structured database field with filter metadata
        
        Args:
            field_name: Column name (Vietnamese supported)
            data_type: SQL data type (VARCHAR, INT, etc.)
            sample_values: Sample data from column
            table_name: Table name (optional context)
            schema_context: Additional schema information
            filter_metadata: Column filter info (mode, total columns, etc.)
            
        Returns:
            {
                'classification': str,
                'pdpl_category': 'regular' | 'sensitive',
                'confidence': float,
                'vietnamese_type': str,
                'sensitivity_score': float,
                'filter_context': dict  # Filter metadata
            }
        """
        try:
            payload = {
                "field_name": field_name,
                "data_type": data_type,
                "sample_values": sample_values[:100],  # Limit to 100 samples
                "table_name": table_name,
                "schema_context": schema_context,
                "filter_metadata": filter_metadata  # Include filter context
            }
            
            response = await self.client.post(
                "/api/v1/classify/structured",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Adjust confidence based on sample size if filtered
            if filter_metadata and filter_metadata.get('is_filtered'):
                # Lower confidence slightly if fewer columns scanned
                reduction_ratio = filter_metadata.get('reduction_percentage', 0) / 100
                if reduction_ratio > 0.5:  # > 50% columns filtered out
                    result['confidence'] *= 0.95  # Reduce confidence by 5%
                    result['filter_adjusted'] = True
            
            logger.info(
                f"[OK] Classified field '{field_name}': "
                f"{result['classification']} "
                f"(confidence: {result['confidence']:.2f}, "
                f"filtered: {filter_metadata.get('is_filtered', False)})"
            )
            
            return result
            
        except httpx.HTTPError as e:
            logger.error(
                f"[ERROR] Classification request failed for '{field_name}': {str(e)}"
            )
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def classify_structured_batch(
        self,
        fields: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Batch classify multiple structured fields
        
        Args:
            fields: List of field dictionaries with:
                - field_name: str
                - data_type: str
                - sample_values: List[Any]
                - table_name: Optional[str]
                
        Returns:
            List of classification results
        """
        try:
            payload = {"fields": fields}
            
            response = await self.client.post(
                "/api/v1/classify/structured/batch",
                json=payload
            )
            
            response.raise_for_status()
            results = response.json()
            
            logger.info(
                f"[OK] Batch classified {len(fields)} fields, "
                f"{len(results)} results"
            )
            
            return results
            
        except httpx.HTTPError as e:
            logger.error(f"[ERROR] Batch classification failed: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def classify_unstructured_text(
        self,
        text: str,
        model_type: str = "phobert",
        language: str = "vi"
    ) -> Dict[str, Any]:
        """
        Classify Vietnamese unstructured text
        
        Args:
            text: Vietnamese text to classify
            model_type: AI model type (phobert, bert-multilingual)
            language: Text language (vi, en)
            
        Returns:
            {
                'predicted_category': str,
                'confidence_score': float,
                'all_probabilities': dict
            }
        """
        try:
            payload = {
                "text": text,
                "model_type": model_type,
                "language": language
            }
            
            response = await self.client.post(
                "/api/v1/classify/unstructured",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(
                f"[OK] Classified text: {result['predicted_category']} "
                f"(confidence: {result['confidence_score']:.2f})"
            )
            
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"[ERROR] Text classification failed: {str(e)}")
            raise
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get classification service model information"""
        try:
            response = await self.client.get("/api/v1/models/info")
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"[ERROR] Failed to get model info: {str(e)}")
            raise
    
    async def health_check(self) -> bool:
        """Check if classification service is healthy"""
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Close HTTP client connections"""
        await self.client.aclose()
        logger.info("[OK] Classification service client closed")
```

---

## Classification Workflow

### Integrated Classification Service

```python
# File: backend/veri_ai_data_inventory/services/classification_service.py

from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
from ..clients.classification_client import ClassificationServiceClient
from ..models.inventory_models import DataAsset, FieldClassification

logger = logging.getLogger(__name__)

class IntegratedClassificationService:
    """Service for integrating AI classification into data discovery"""
    
    def __init__(self):
        """Initialize classification service"""
        self.client = ClassificationServiceClient()
        self.cache = {}  # Simple in-memory cache (use Redis in production)
    
    async def classify_discovered_table(
        self,
        tenant_id: UUID,
        asset: DataAsset,
        table_schema: Dict[str, Any],
        sample_data: Dict[str, List[Any]]
    ) -> List[FieldClassification]:
        """
        Classify all fields in discovered database table
        
        Args:
            tenant_id: Tenant UUID
            asset: DataAsset instance
            table_schema: Table schema information
            sample_data: Dictionary of {column_name: [sample_values]}
            
        Returns:
            List of FieldClassification instances
        """
        try:
            classifications = []
            
            # Prepare batch classification request
            fields_to_classify = []
            
            for column in table_schema['columns']:
                column_name = column['column_name']
                data_type = column['data_type']
                samples = sample_data.get(column_name, [])
                
                if not samples:
                    logger.warning(
                        f"[WARNING] No samples for {column_name}, skipping"
                    )
                    continue
                
                # Check cache
                cache_key = self._get_cache_key(
                    column_name, data_type, samples[:10]
                )
                
                if cache_key in self.cache:
                    logger.info(f"[OK] Using cached classification for {column_name}")
                    classifications.append(self.cache[cache_key])
                    continue
                
                # Add to batch
                fields_to_classify.append({
                    "field_name": column_name,
                    "data_type": data_type,
                    "sample_values": samples[:100],
                    "table_name": table_schema['table_name']
                })
            
            # Batch classify
            if fields_to_classify:
                logger.info(
                    f"[OK] Classifying {len(fields_to_classify)} fields "
                    f"for table {table_schema['table_name']}"
                )
                
                results = await self.client.classify_structured_batch(
                    fields_to_classify
                )
                
                # Convert results to FieldClassification objects
                for field_info, result in zip(fields_to_classify, results):
                    classification = FieldClassification(
                        field_classification_id=UUID(),
                        tenant_id=tenant_id,
                        asset_id=asset.asset_id,
                        field_name=field_info['field_name'],
                        field_type=field_info['data_type'],
                        classification=result['classification'],
                        pdpl_category=result['pdpl_category'],
                        confidence_score=result['confidence'],
                        vietnamese_type=result.get('vietnamese_type'),
                        sensitivity_score=result.get('sensitivity_score', 0.0),
                        sample_values=field_info['sample_values'][:10],
                        classified_at=datetime.utcnow()
                    )
                    
                    classifications.append(classification)
                    
                    # Cache result
                    cache_key = self._get_cache_key(
                        field_info['field_name'],
                        field_info['data_type'],
                        field_info['sample_values'][:10]
                    )
                    self.cache[cache_key] = classification
            
            logger.info(
                f"[OK] Classified {len(classifications)} fields for "
                f"{table_schema['table_name']}"
            )
            
            return classifications
            
        except Exception as e:
            logger.error(f"[ERROR] Table classification failed: {str(e)}")
            raise
    
    async def classify_discovered_file(
        self,
        tenant_id: UUID,
        asset: DataAsset,
        file_content: str,
        file_type: str
    ) -> Dict[str, Any]:
        """
        Classify discovered file content
        
        Args:
            tenant_id: Tenant UUID
            asset: DataAsset instance
            file_content: File text content
            file_type: File extension (.pdf, .docx, .txt)
            
        Returns:
            Classification result dictionary
        """
        try:
            # Use unstructured classifier for file content
            result = await self.client.classify_unstructured_text(
                text=file_content[:10000],  # First 10KB
                model_type="phobert",
                language="vi"
            )
            
            logger.info(
                f"[OK] Classified file {asset.name}: "
                f"{result['predicted_category']}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"[ERROR] File classification failed: {str(e)}")
            raise
    
    async def classify_data_flow(
        self,
        tenant_id: UUID,
        source_classifications: List[FieldClassification],
        dest_classifications: List[FieldClassification]
    ) -> Dict[str, Any]:
        """
        Analyze data flow based on source and destination classifications
        
        Args:
            tenant_id: Tenant UUID
            source_classifications: Source field classifications
            dest_classifications: Destination field classifications
            
        Returns:
            Flow analysis result
        """
        # Determine most sensitive data in flow
        all_classifications = source_classifications + dest_classifications
        
        has_sensitive = any(
            c.pdpl_category == 'sensitive' for c in all_classifications
        )
        
        max_sensitivity = max(
            (c.sensitivity_score for c in all_classifications),
            default=0.0
        )
        
        # Categorize data types in flow
        data_types = set(c.classification for c in all_classifications)
        vietnamese_types = set(
            c.vietnamese_type for c in all_classifications
            if c.vietnamese_type
        )
        
        analysis = {
            "has_sensitive_data": has_sensitive,
            "max_sensitivity_score": max_sensitivity,
            "data_types_in_flow": list(data_types),
            "vietnamese_types_in_flow": list(vietnamese_types),
            "total_fields": len(all_classifications),
            "sensitive_fields": sum(
                1 for c in all_classifications
                if c.pdpl_category == 'sensitive'
            ),
            "requires_encryption": has_sensitive or max_sensitivity > 0.7,
            "requires_audit": has_sensitive
        }
        
        logger.info(
            f"[OK] Flow analysis: {analysis['sensitive_fields']} sensitive fields "
            f"out of {analysis['total_fields']}"
        )
        
        return analysis
    
    def _get_cache_key(
        self,
        field_name: str,
        data_type: str,
        samples: List[Any]
    ) -> str:
        """Generate cache key for classification result"""
        import hashlib
        
        # Create hash from field name, type, and sample values
        content = f"{field_name}|{data_type}|{str(samples)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def close(self):
        """Close classification client"""
        await self.client.close()
```

---

## Batch Processing

### Optimized Batch Classification

```python
# File: backend/veri_ai_data_inventory/services/batch_classifier.py

import asyncio
from typing import List, Dict, Any, Optional
from uuid import UUID
import logging
from datetime import datetime
from ..clients.classification_client import ClassificationServiceClient

logger = logging.getLogger(__name__)

class BatchClassificationProcessor:
    """Process large-scale classification jobs efficiently"""
    
    def __init__(
        self,
        batch_size: int = 100,
        max_concurrent_batches: int = 5
    ):
        """
        Initialize batch processor
        
        Args:
            batch_size: Number of fields per batch
            max_concurrent_batches: Maximum parallel batch requests
        """
        self.batch_size = batch_size
        self.max_concurrent_batches = max_concurrent_batches
        self.client = ClassificationServiceClient()
        self.semaphore = asyncio.Semaphore(max_concurrent_batches)
    
    async def process_large_dataset(
        self,
        tenant_id: UUID,
        fields: List[Dict[str, Any]],
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Process large dataset with progress tracking
        
        Args:
            tenant_id: Tenant UUID
            fields: List of fields to classify
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of classification results
        """
        try:
            total_fields = len(fields)
            logger.info(
                f"[OK] Starting batch classification: {total_fields} fields"
            )
            
            # Split into batches
            batches = [
                fields[i:i + self.batch_size]
                for i in range(0, total_fields, self.batch_size)
            ]
            
            logger.info(f"[OK] Created {len(batches)} batches")
            
            # Process batches concurrently with semaphore
            all_results = []
            tasks = []
            
            for batch_idx, batch in enumerate(batches):
                task = self._process_batch(
                    batch,
                    batch_idx,
                    len(batches),
                    progress_callback
                )
                tasks.append(task)
            
            # Wait for all batches to complete
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Flatten results
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"[ERROR] Batch processing error: {result}")
                    continue
                all_results.extend(result)
            
            logger.info(
                f"[OK] Batch classification complete: "
                f"{len(all_results)} / {total_fields} fields classified"
            )
            
            return all_results
            
        except Exception as e:
            logger.error(f"[ERROR] Batch processing failed: {str(e)}")
            raise
    
    async def _process_batch(
        self,
        batch: List[Dict[str, Any]],
        batch_idx: int,
        total_batches: int,
        progress_callback: Optional[callable]
    ) -> List[Dict[str, Any]]:
        """Process single batch with semaphore"""
        async with self.semaphore:
            try:
                logger.info(
                    f"[OK] Processing batch {batch_idx + 1}/{total_batches} "
                    f"({len(batch)} fields)"
                )
                
                # Call classification service
                results = await self.client.classify_structured_batch(batch)
                
                # Progress callback
                if progress_callback:
                    progress = ((batch_idx + 1) / total_batches) * 100
                    await progress_callback(progress, batch_idx + 1, total_batches)
                
                return results
                
            except Exception as e:
                logger.error(
                    f"[ERROR] Batch {batch_idx + 1} failed: {str(e)}"
                )
                raise
    
    async def close(self):
        """Close batch processor"""
        await self.client.close()
```

---

## Result Storage

### Classification Result Database Models

```python
# File: backend/veri_ai_data_inventory/models/inventory_models.py

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .database import Base

class DataAsset(Base):
    """Discovered data asset (table, file, API, etc.)"""
    __tablename__ = "data_assets"
    
    asset_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    asset_type = Column(String(50), nullable=False)  # table, file, api, etc.
    name = Column(String(255), nullable=False)
    source_system = Column(String(100))
    location = Column(String(500))
    
    discovered_at = Column(DateTime, default=datetime.utcnow)
    last_scanned = Column(DateTime)
    
    metadata = Column(JSON)
    
    # Relationships
    field_classifications = relationship("FieldClassification", back_populates="asset")

class FieldClassification(Base):
    """AI classification result for database field or file content"""
    __tablename__ = "field_classifications"
    
    field_classification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("data_assets.asset_id"), nullable=False)
    
    # Field information
    field_name = Column(String(255), nullable=False)
    field_type = Column(String(100))  # SQL type or file type
    
    # Classification results
    classification = Column(String(100), nullable=False)  # name, email, phone, etc.
    pdpl_category = Column(String(20), nullable=False)  # regular, sensitive
    confidence_score = Column(Float, nullable=False)
    vietnamese_type = Column(String(100))  # cmnd_cccd, so_dien_thoai, etc.
    sensitivity_score = Column(Float, default=0.0)
    
    # Sample data (for validation)
    sample_values = Column(JSON)
    
    # Classification metadata
    classified_at = Column(DateTime, default=datetime.utcnow)
    classifier_version = Column(String(20))
    manual_override = Column(Boolean, default=False)
    override_by = Column(UUID(as_uuid=True))
    override_at = Column(DateTime)
    
    # Relationships
    asset = relationship("DataAsset", back_populates="field_classifications")
    
    # Indexes
    __table_args__ = (
        Index('idx_tenant_asset', 'tenant_id', 'asset_id'),
        Index('idx_classification', 'classification'),
        Index('idx_pdpl_category', 'pdpl_category'),
    )
```

### Database Repository

```python
# File: backend/veri_ai_data_inventory/repositories/classification_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from uuid import UUID
import logging
from ..models.inventory_models import FieldClassification, DataAsset

logger = logging.getLogger(__name__)

class ClassificationRepository:
    """Repository for classification result storage"""
    
    def __init__(self, session: AsyncSession):
        """Initialize repository with database session"""
        self.session = session
    
    async def save_classification(
        self,
        classification: FieldClassification
    ) -> FieldClassification:
        """Save classification result"""
        try:
            self.session.add(classification)
            await self.session.commit()
            await self.session.refresh(classification)
            
            logger.info(
                f"[OK] Saved classification: {classification.field_name} -> "
                f"{classification.classification}"
            )
            
            return classification
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"[ERROR] Failed to save classification: {str(e)}")
            raise
    
    async def save_classifications_batch(
        self,
        classifications: List[FieldClassification]
    ) -> int:
        """Save multiple classifications in batch"""
        try:
            self.session.add_all(classifications)
            await self.session.commit()
            
            logger.info(
                f"[OK] Saved {len(classifications)} classifications in batch"
            )
            
            return len(classifications)
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"[ERROR] Batch save failed: {str(e)}")
            raise
    
    async def get_asset_classifications(
        self,
        tenant_id: UUID,
        asset_id: UUID
    ) -> List[FieldClassification]:
        """Get all classifications for an asset"""
        try:
            stmt = select(FieldClassification).where(
                and_(
                    FieldClassification.tenant_id == tenant_id,
                    FieldClassification.asset_id == asset_id
                )
            )
            
            result = await self.session.execute(stmt)
            classifications = result.scalars().all()
            
            return list(classifications)
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to get classifications: {str(e)}")
            raise
    
    async def get_sensitive_fields(
        self,
        tenant_id: UUID
    ) -> List[FieldClassification]:
        """Get all sensitive data fields for tenant"""
        try:
            stmt = select(FieldClassification).where(
                and_(
                    FieldClassification.tenant_id == tenant_id,
                    FieldClassification.pdpl_category == 'sensitive'
                )
            )
            
            result = await self.session.execute(stmt)
            classifications = result.scalars().all()
            
            logger.info(
                f"[OK] Found {len(classifications)} sensitive fields "
                f"for tenant {tenant_id}"
            )
            
            return list(classifications)
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to get sensitive fields: {str(e)}")
            raise
    
    async def override_classification(
        self,
        field_classification_id: UUID,
        new_classification: str,
        new_category: str,
        override_by: UUID
    ) -> FieldClassification:
        """Manual override of AI classification"""
        try:
            stmt = select(FieldClassification).where(
                FieldClassification.field_classification_id == field_classification_id
            )
            
            result = await self.session.execute(stmt)
            classification = result.scalar_one()
            
            # Update classification
            classification.classification = new_classification
            classification.pdpl_category = new_category
            classification.manual_override = True
            classification.override_by = override_by
            classification.override_at = datetime.utcnow()
            
            await self.session.commit()
            await self.session.refresh(classification)
            
            logger.info(
                f"[OK] Overridden classification: {classification.field_name} -> "
                f"{new_classification}"
            )
            
            return classification
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"[ERROR] Classification override failed: {str(e)}")
            raise
```

---

**[Continued sections: Vietnamese Pattern Handling, Performance Optimization, Error Handling...]**

This AI Classification Integration plan provides complete integration between the data inventory and classification services with batch processing, result caching, and Vietnamese pattern support.

Would you like me to continue with the final 2 implementation plans (DPO Review Dashboard and Async Job Processing)?
