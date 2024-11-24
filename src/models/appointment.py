"""
Appointment-related models including Appointment and AppointmentType.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from .common import BaseModel

class AppointmentType(Enum):
    """Types of appointments available"""
    PERSONAL_TRAINING = "personal_training"
    GROUP_CLASS = "group_class"
    CONSULTATION = "consultation"
    ASSESSMENT = "assessment"

class AppointmentStatus(Enum):
    """Status of appointments"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

@dataclass
class Appointment(BaseModel):
    """Represents a scheduled appointment"""
    member_id: str
    trainer_id: str
    location_id: str
    appointment_type: AppointmentType
    start_time: datetime
    duration: int  # in minutes
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    zone_id: Optional[str] = None
    notes: Optional[str] = None

    @property
    def end_time(self) -> datetime:
        """Calculate appointment end time"""
        return self.start_time + timedelta(minutes=self.duration)

    def cancel(self, cancellation_note: Optional[str] = None):
        """Cancel the appointment"""
        self.status = AppointmentStatus.CANCELLED
        if cancellation_note:
            self.notes = f"Cancelled: {cancellation_note}"
        self.update()

    def complete(self, completion_note: Optional[str] = None):
        """Mark appointment as completed"""
        self.status = AppointmentStatus.COMPLETED
        if completion_note:
            self.notes = completion_note
        self.update()

    def is_upcoming(self) -> bool:
        """Check if appointment is in the future"""
        return self.start_time > datetime.now()