"""
VietnamesePatternDetector implementation for veri-ai-data-inventory
Uses dynamic configuration from ScanConfig for thresholds
Domain knowledge patterns for Vietnamese PDPL compliance
"""
try:
    from .config import ScanConfig
except ImportError:
    from config.constants import ScanConfig

from typing import List

class VietnamesePatternDetector:
    def __init__(self, confidence_threshold: float = ScanConfig.CONFIDENCE_THRESHOLD):
        self.confidence_threshold = confidence_threshold
        # Example: distinctive Vietnamese PDPL patterns
        self.patterns = [
            r"\bHọ và tên\b", r"\bSố CMND\b", r"\bSố CCCD\b", r"\bĐịa chỉ\b", r"\bSố điện thoại\b", r"\bEmail\b"
        ]

    def detect_patterns(self, text: str) -> List[str]:
        """Detects Vietnamese PDPL patterns in text."""
        import re
        found = []
        for pattern in self.patterns:
            if re.search(pattern, text):
                found.append(pattern)
        return found

    def is_confident(self, score: float) -> bool:
        """Checks if detection score meets dynamic threshold."""
        return score >= self.confidence_threshold
