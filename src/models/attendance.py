"""
Attendance-related models for tracking member visits.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .common import BaseModel

@dataclass
class AttendanceRecord(BaseModel):
    """Records a member's attendance at the gym"""
    member_id: str
    location_id: str
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    zone_id: Optional[str] = None

    def check_out(self):
        """Record check-out time"""
        self.check_out_time = datetime.now()
        self.update()

    @property
    def duration(self) -> Optional[int]:
        """Calculate duration of visit in minutes"""
        if not self.check_out_time:
            return None
        duration = self.check_out_time - self.check_in_time
        return int(duration.total_seconds() / 60)

    def is_active(self) -> bool:
        """Check if this is an active visit (no checkout)"""
        return self.check_out_time is None