"""
Location-related models including GymLocation and WorkoutZone.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from .common import BaseModel, Address

@dataclass
class WorkoutZone(BaseModel):
    """Represents a specific zone within a gym"""
    name: str
    type: str
    capacity: int
    equipment: List[str]
    attendant_id: Optional[str]
    description: Optional[str] = None
    is_active: bool = True
    schedule: Dict[str, List[str]] = None  # Day -> List of class times

    def __post_init__(self):
        """Initialize schedule if not provided"""
        super().__post_init__()
        if self.schedule is None:
            self.schedule = {}

    def update_schedule(self, day: str, times: List[str]):
        """Update schedule for a specific day"""
        self.schedule[day] = times
        self.update()

    def is_available(self, day: str, time: str) -> bool:
        """Check if zone is available at specific time"""
        return day in self.schedule and time in self.schedule[day]

@dataclass
class GymLocation(BaseModel):
    """Represents a physical gym location"""
    name: str
    address: Address
    manager_id: str
    workout_zones: List[WorkoutZone]
    amenities: List[str]
    total_capacity: int
    contact_phone: str
    contact_email: str
    opening_hours: Dict[str, str]  # Day -> "HH:MM-HH:MM"
    is_active: bool = True

    def add_workout_zone(self, zone: WorkoutZone):
        """Add a new workout zone"""
        self.workout_zones.append(zone)
        self.update()

    def remove_workout_zone(self, zone_id: str) -> bool:
        """Remove a workout zone by ID"""
        initial_length = len(self.workout_zones)
        self.workout_zones = [z for z in self.workout_zones if z.id != zone_id]
        if len(self.workout_zones) < initial_length:
            self.update()
            return True
        return False

    def get_zone(self, zone_id: str) -> Optional[WorkoutZone]:
        """Get a specific workout zone by ID"""
        for zone in self.workout_zones:
            if zone.id == zone_id:
                return zone
        return None