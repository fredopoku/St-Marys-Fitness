"""
Member-related models including Member, MembershipType, and HealthInformation.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List
from .common import BaseModel, Address

class MembershipType(Enum):
    """Types of membership available"""
    REGULAR = "regular"
    PREMIUM = "premium"
    TRIAL = "trial"

@dataclass
class HealthInformation:
    """Health-related information for a member"""
    height: float  # in centimeters
    weight: float  # in kilograms
    medical_conditions: List[str]
    emergency_contact_name: str
    emergency_contact_phone: str
    last_health_check: Optional[datetime] = None
    notes: Optional[str] = None

@dataclass
class Member(BaseModel):
    """Represents a gym member"""
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Address
    membership_type: MembershipType
    health_info: HealthInformation
    home_location_id: Optional[str] = None
    is_active: bool = True

    @property
    def full_name(self) -> str:
        """Get member's full name"""
        return f"{self.first_name} {self.last_name}"

    def deactivate(self):
        """Deactivate member's membership"""
        self.is_active = False
        self.update()

    def activate(self):
        """Activate member's membership"""
        self.is_active = True
        self.update()

    def update_health_info(self, health_info: HealthInformation):
        """Update member's health information"""
        self.health_info = health_info
        self.update()