"""
VeriSyntra Scan Progress Tracker

Tracks progress of multi-source scans with status updates.
Uses dynamic configuration for update intervals.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Flexible import pattern
try:
    from ..config import ScanManagerConfig
except ImportError:
    from config.constants import ScanManagerConfig

logger = logging.getLogger(__name__)


class ScanStatus(str, Enum):
    """Enumeration of scan statuses"""
    PENDING = 'pending'
    CONNECTING = 'connecting'
    DISCOVERING = 'discovering'
    EXTRACTING = 'extracting'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class ScanProgressTracker:
    """
    Track progress of scanner operations.
    
    Provides real-time progress updates with configurable update intervals.
    """
    
    def __init__(
        self,
        update_interval: int = ScanManagerConfig.PROGRESS_UPDATE_INTERVAL_SECONDS
    ):
        """
        Initialize progress tracker with dynamic configuration.
        
        Args:
            update_interval: Seconds between progress updates (default from ScanManagerConfig)
        """
        self.update_interval = update_interval
        self.scans: Dict[str, Dict[str, Any]] = {}
        self.last_update_time: Dict[str, float] = {}
    
    def start_scan(
        self,
        scan_id: str,
        scanner_type: str,
        description: str = ''
    ) -> None:
        """
        Register a new scan operation.
        
        Args:
            scan_id: Unique identifier for this scan
            scanner_type: Type of scanner (postgresql, s3, etc.)
            description: Optional description of the scan
        """
        self.scans[scan_id] = {
            'scan_id': scan_id,
            'scanner_type': scanner_type,
            'description': description,
            'status': ScanStatus.PENDING,
            'progress_percent': 0.0,
            'items_discovered': 0,
            'items_processed': 0,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'duration_seconds': 0,
            'current_operation': None,
            'error_message': None
        }
        
        self.last_update_time[scan_id] = time.time()
        
        logger.info(f"[OK] Started tracking scan: {scan_id} ({scanner_type})")
    
    def update_progress(
        self,
        scan_id: str,
        status: Optional[ScanStatus] = None,
        progress_percent: Optional[float] = None,
        items_discovered: Optional[int] = None,
        items_processed: Optional[int] = None,
        current_operation: Optional[str] = None,
        force_update: bool = False
    ) -> bool:
        """
        Update scan progress.
        
        Args:
            scan_id: Scan identifier
            status: New status (optional)
            progress_percent: Progress percentage 0-100 (optional)
            items_discovered: Number of items discovered (optional)
            items_processed: Number of items processed (optional)
            current_operation: Current operation description (optional)
            force_update: Force update even if interval hasn't elapsed
            
        Returns:
            True if update was recorded, False if skipped due to interval
        """
        if scan_id not in self.scans:
            logger.warning(f"[WARNING] Unknown scan ID: {scan_id}")
            return False
        
        # Check if update interval has elapsed
        current_time = time.time()
        time_since_last = current_time - self.last_update_time.get(scan_id, 0)
        
        if not force_update and time_since_last < self.update_interval:
            return False  # Skip update, too soon
        
        # Update fields
        if status is not None:
            self.scans[scan_id]['status'] = status
        if progress_percent is not None:
            self.scans[scan_id]['progress_percent'] = min(100.0, max(0.0, progress_percent))
        if items_discovered is not None:
            self.scans[scan_id]['items_discovered'] = items_discovered
        if items_processed is not None:
            self.scans[scan_id]['items_processed'] = items_processed
        if current_operation is not None:
            self.scans[scan_id]['current_operation'] = current_operation
        
        # Update duration
        start_time = datetime.fromisoformat(self.scans[scan_id]['start_time'])
        duration = (datetime.now() - start_time).total_seconds()
        self.scans[scan_id]['duration_seconds'] = duration
        
        self.last_update_time[scan_id] = current_time
        
        logger.debug(
            f"[INFO] Scan {scan_id}: {self.scans[scan_id]['status']} - "
            f"{self.scans[scan_id]['progress_percent']:.1f}% "
            f"({items_discovered or 0} items)"
        )
        
        return True
    
    def complete_scan(
        self,
        scan_id: str,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """
        Mark scan as completed.
        
        Args:
            scan_id: Scan identifier
            success: Whether scan completed successfully
            error_message: Error message if failed
        """
        if scan_id not in self.scans:
            logger.warning(f"[WARNING] Unknown scan ID: {scan_id}")
            return
        
        self.scans[scan_id]['status'] = ScanStatus.COMPLETED if success else ScanStatus.FAILED
        self.scans[scan_id]['progress_percent'] = 100.0 if success else self.scans[scan_id]['progress_percent']
        self.scans[scan_id]['end_time'] = datetime.now().isoformat()
        
        if error_message:
            self.scans[scan_id]['error_message'] = error_message
        
        # Calculate final duration
        start_time = datetime.fromisoformat(self.scans[scan_id]['start_time'])
        end_time = datetime.fromisoformat(self.scans[scan_id]['end_time'])
        duration = (end_time - start_time).total_seconds()
        self.scans[scan_id]['duration_seconds'] = duration
        
        status_text = 'completed' if success else 'failed'
        logger.info(
            f"[OK] Scan {scan_id} {status_text} in {duration:.1f}s "
            f"({self.scans[scan_id]['items_discovered']} items)"
        )
    
    def get_scan_status(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current status of a scan.
        
        Args:
            scan_id: Scan identifier
            
        Returns:
            Scan status dictionary or None if not found
        """
        return self.scans.get(scan_id)
    
    def get_all_scans(self) -> List[Dict[str, Any]]:
        """
        Get status of all tracked scans.
        
        Returns:
            List of all scan status dictionaries
        """
        return list(self.scans.values())
    
    def get_active_scans(self) -> List[Dict[str, Any]]:
        """
        Get all active (non-completed) scans.
        
        Returns:
            List of active scan status dictionaries
        """
        active_statuses = [
            ScanStatus.PENDING,
            ScanStatus.CONNECTING,
            ScanStatus.DISCOVERING,
            ScanStatus.EXTRACTING
        ]
        
        return [
            scan for scan in self.scans.values()
            if scan['status'] in active_statuses
        ]
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for all scans.
        
        Returns:
            Summary statistics dictionary
        """
        total_scans = len(self.scans)
        completed = sum(1 for s in self.scans.values() if s['status'] == ScanStatus.COMPLETED)
        failed = sum(1 for s in self.scans.values() if s['status'] == ScanStatus.FAILED)
        active = sum(1 for s in self.scans.values() if s['status'] not in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED])
        
        total_items = sum(s['items_discovered'] for s in self.scans.values())
        total_duration = sum(s['duration_seconds'] for s in self.scans.values())
        
        return {
            'total_scans': total_scans,
            'completed': completed,
            'failed': failed,
            'active': active,
            'total_items_discovered': total_items,
            'total_duration_seconds': total_duration,
            'success_rate': (completed / total_scans * 100) if total_scans > 0 else 0.0
        }
    
    def clear_completed(self) -> int:
        """
        Clear completed scans from tracker.
        
        Returns:
            Number of scans removed
        """
        completed_ids = [
            scan_id for scan_id, scan in self.scans.items()
            if scan['status'] in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED]
        ]
        
        for scan_id in completed_ids:
            del self.scans[scan_id]
            if scan_id in self.last_update_time:
                del self.last_update_time[scan_id]
        
        logger.info(f"[OK] Cleared {len(completed_ids)} completed scans")
        return len(completed_ids)
    
    def cancel_scan(self, scan_id: str) -> bool:
        """
        Mark a scan as cancelled.
        
        Args:
            scan_id: Scan identifier
            
        Returns:
            True if scan was cancelled, False if not found
        """
        if scan_id not in self.scans:
            return False
        
        self.scans[scan_id]['status'] = ScanStatus.CANCELLED
        self.scans[scan_id]['end_time'] = datetime.now().isoformat()
        
        logger.info(f"[OK] Scan {scan_id} cancelled")
        return True
