"""
VeriSyntra Job State Manager

In-memory state management for scan jobs using dynamic configuration.
This implementation uses a simple dictionary-based approach suitable for
prototype/development. Production should use Redis or database-backed storage.

Key Features:
- Dynamic configuration from APIConfig (zero hard-coding)
- Thread-safe operations for concurrent access
- Automatic cleanup of expired jobs
- Vietnamese business context preservation
"""

import logging
from datetime import datetime, timedelta
from threading import Lock
from typing import Any, Dict, List, Optional
from uuid import UUID

# Import dynamic configuration
try:
    from ..config.constants import APIConfig
except ImportError:
    from config.constants import APIConfig

logger = logging.getLogger(__name__)


class JobState:
    """
    Single scan job state container
    
    Stores all information about a scan job using dynamic configuration
    for status values and retention policies.
    """
    
    def __init__(
        self,
        scan_job_id: UUID,
        tenant_id: UUID,
        source_type: str,
        connection_config: Dict[str, Any],
        column_filter: Optional[Dict[str, Any]] = None,
        veri_business_context: Optional[Dict[str, Any]] = None
    ):
        """Initialize job state with dynamic status from APIConfig"""
        self.scan_job_id = scan_job_id
        self.tenant_id = tenant_id
        self.source_type = source_type
        self.connection_config = connection_config
        self.column_filter = column_filter
        self.veri_business_context = veri_business_context or {}
        
        # Use dynamic config for status - NOT hard-coded
        self.status = APIConfig.STATUS_PENDING
        self.progress = 0
        self.discovered_assets = []
        self.filter_statistics = None
        self.errors = []
        
        self.created_at = datetime.utcnow()
        self.started_at = None
        self.completed_at = None
        self.duration_seconds = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job state to dictionary"""
        return {
            'scan_job_id': str(self.scan_job_id),
            'tenant_id': str(self.tenant_id),
            'source_type': self.source_type,
            'status': self.status,
            'progress': self.progress,
            'discovered_assets': self.discovered_assets,
            'filter_statistics': self.filter_statistics,
            'errors': self.errors[:APIConfig.MAX_ERRORS_PER_RESPONSE],  # Use config limit
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_seconds': self.duration_seconds,
            'veri_business_context': self.veri_business_context
        }
    
    def start(self):
        """Mark job as started using dynamic status"""
        self.status = APIConfig.STATUS_RUNNING
        self.started_at = datetime.utcnow()
        logger.info(f"[OK] Scan job {self.scan_job_id} started")
    
    def update_progress(self, progress: int):
        """Update job progress (0-100)"""
        self.progress = max(0, min(100, progress))
    
    def complete(self, discovered_assets: List[Dict[str, Any]], filter_statistics: Optional[Dict[str, Any]] = None):
        """Mark job as completed using dynamic status"""
        self.status = APIConfig.STATUS_COMPLETED
        self.progress = 100
        self.discovered_assets = discovered_assets[:APIConfig.MAX_ASSETS_PER_RESPONSE]  # Use config limit
        self.filter_statistics = filter_statistics
        self.completed_at = datetime.utcnow()
        
        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())
        
        logger.info(
            f"[OK] Scan job {self.scan_job_id} completed: "
            f"{len(self.discovered_assets)} assets discovered in {self.duration_seconds}s"
        )
    
    def fail(self, error_message: str):
        """Mark job as failed using dynamic status"""
        self.status = APIConfig.STATUS_FAILED
        self.completed_at = datetime.utcnow()
        
        # Truncate error message using config
        truncated_error = error_message[:APIConfig.MAX_ERROR_MESSAGE_LENGTH]
        self.errors.append(truncated_error)
        
        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())
        
        logger.error(f"[ERROR] Scan job {self.scan_job_id} failed: {truncated_error}")
    
    def cancel(self):
        """Mark job as cancelled using dynamic status"""
        self.status = APIConfig.STATUS_CANCELLED
        self.completed_at = datetime.utcnow()
        
        if self.started_at:
            self.duration_seconds = int((self.completed_at - self.started_at).total_seconds())
        
        logger.info(f"[OK] Scan job {self.scan_job_id} cancelled")
    
    def is_terminal(self) -> bool:
        """Check if job is in terminal state"""
        terminal_statuses = [
            APIConfig.STATUS_COMPLETED,
            APIConfig.STATUS_FAILED,
            APIConfig.STATUS_CANCELLED
        ]
        return self.status in terminal_statuses
    
    def is_expired(self) -> bool:
        """Check if job retention period has expired"""
        if not self.completed_at:
            return False
        
        # Use dynamic retention period from config
        retention_period = timedelta(hours=APIConfig.TASK_RETENTION_HOURS)
        expiry_time = self.completed_at + retention_period
        
        return datetime.utcnow() > expiry_time


class JobStateManager:
    """
    Thread-safe in-memory job state manager
    
    Manages scan job lifecycle using dynamic configuration.
    Suitable for development/prototype. Production should use Redis/database.
    """
    
    def __init__(self):
        """Initialize job state manager"""
        self._jobs: Dict[UUID, JobState] = {}
        self._lock = Lock()
        logger.info("[OK] JobStateManager initialized (in-memory storage)")
    
    def create_job(
        self,
        scan_job_id: UUID,
        tenant_id: UUID,
        source_type: str,
        connection_config: Dict[str, Any],
        column_filter: Optional[Dict[str, Any]] = None,
        veri_business_context: Optional[Dict[str, Any]] = None
    ) -> JobState:
        """Create new job state"""
        with self._lock:
            job_state = JobState(
                scan_job_id=scan_job_id,
                tenant_id=tenant_id,
                source_type=source_type,
                connection_config=connection_config,
                column_filter=column_filter,
                veri_business_context=veri_business_context
            )
            self._jobs[scan_job_id] = job_state
            
            logger.info(
                f"[OK] Created job {scan_job_id} for tenant {tenant_id} "
                f"(source: {source_type})"
            )
            
            return job_state
    
    def get_job(self, scan_job_id: UUID) -> Optional[JobState]:
        """Get job state by ID"""
        with self._lock:
            return self._jobs.get(scan_job_id)
    
    def update_job(self, scan_job_id: UUID, **kwargs) -> bool:
        """Update job state fields"""
        with self._lock:
            job = self._jobs.get(scan_job_id)
            if not job:
                logger.warning(f"[WARNING] Job {scan_job_id} not found for update")
                return False
            
            for key, value in kwargs.items():
                if hasattr(job, key):
                    setattr(job, key, value)
            
            return True
    
    def delete_job(self, scan_job_id: UUID) -> bool:
        """Delete job state (for cancellation)"""
        with self._lock:
            if scan_job_id in self._jobs:
                job = self._jobs[scan_job_id]
                job.cancel()
                del self._jobs[scan_job_id]
                logger.info(f"[OK] Job {scan_job_id} deleted")
                return True
            
            logger.warning(f"[WARNING] Job {scan_job_id} not found for deletion")
            return False
    
    def list_jobs(
        self,
        tenant_id: Optional[UUID] = None,
        status: Optional[str] = None
    ) -> List[JobState]:
        """List jobs with optional filtering"""
        with self._lock:
            jobs = list(self._jobs.values())
            
            if tenant_id:
                jobs = [j for j in jobs if j.tenant_id == tenant_id]
            
            if status:
                jobs = [j for j in jobs if j.status == status]
            
            return jobs
    
    def cleanup_expired_jobs(self) -> int:
        """
        Remove expired completed jobs using dynamic retention period
        
        Returns:
            Number of jobs cleaned up
        """
        with self._lock:
            expired_job_ids = [
                job_id for job_id, job in self._jobs.items()
                if job.is_terminal() and job.is_expired()
            ]
            
            for job_id in expired_job_ids:
                del self._jobs[job_id]
            
            if expired_job_ids:
                logger.info(
                    f"[OK] Cleaned up {len(expired_job_ids)} expired jobs "
                    f"(retention: {APIConfig.TASK_RETENTION_HOURS}h)"
                )
            
            return len(expired_job_ids)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get job state manager statistics"""
        with self._lock:
            total_jobs = len(self._jobs)
            status_counts = {}
            
            for status in APIConfig.VALID_STATUSES:
                status_counts[status] = sum(
                    1 for job in self._jobs.values() if job.status == status
                )
            
            return {
                'total_jobs': total_jobs,
                'status_counts': status_counts,
                'retention_hours': APIConfig.TASK_RETENTION_HOURS,
                'max_background_tasks': APIConfig.MAX_BACKGROUND_TASKS
            }


# Global singleton instance (for development/prototype)
# Production should use dependency injection
_job_state_manager_instance = None


def get_job_state_manager() -> JobStateManager:
    """Get or create global JobStateManager instance"""
    global _job_state_manager_instance
    
    if _job_state_manager_instance is None:
        _job_state_manager_instance = JobStateManager()
    
    return _job_state_manager_instance
