"""
Service layer for handling Gym Location-related operations.
"""

from typing import List, Optional
from repositories.location_repository import LocationRepository
from models.location import GymLocation, WorkoutZone


class LocationService:
    """Handles operations related to gym locations and workout zones."""

    def __init__(self, location_repository: LocationRepository):
        self.location_repository = location_repository

    def create_location(
        self,
        name: str,
        address: str,
        manager_id: str,
        amenities: List[str],
        total_capacity: int,
        contact_phone: str,
        contact_email: str,
        opening_hours: dict
    ) -> GymLocation:
        """
        Add a new gym location.
        """
        new_location = GymLocation(
            name=name,
            address=address,
            manager_id=manager_id,
            workout_zones=[],
            amenities=amenities,
            total_capacity=total_capacity,
            contact_phone=contact_phone,
            contact_email=contact_email,
            opening_hours=opening_hours,
        )
        return self.location_repository.save(new_location)

    def update_location(self, location_id: str, updates: dict) -> Optional[GymLocation]:
        """
        Update details of an existing gym location.
        """
        location = self.location_repository.find_by_id(location_id)
        if not location:
            return None

        for key, value in updates.items():
            if hasattr(location, key):
                setattr(location, key, value)
        return self.location_repository.save(location)

    def deactivate_location(self, location_id: str) -> bool:
        """
        Deactivate a gym location.
        """
        location = self.location_repository.find_by_id(location_id)
        if not location:
            return False
        location.is_active = False
        self.location_repository.save(location)
        return True

    def get_location_by_id(self, location_id: str) -> Optional[GymLocation]:
        """
        Retrieve a specific gym location by its ID.
        """
        return self.location_repository.find_by_id(location_id)

    def list_all_locations(self, active_only: bool = True) -> List[GymLocation]:
        """
        List all gym locations, optionally filtering by active status.
        """
        filters = {"is_active": True} if active_only else {}
        return self.location_repository.find_all(filters=filters)

    def add_workout_zone(
        self, location_id: str, zone_data: dict
    ) -> Optional[WorkoutZone]:
        """
        Add a workout zone to a specific location.
        """
        location = self.location_repository.find_by_id(location_id)
        if not location:
            return None

        new_zone = WorkoutZone(
            name=zone_data["name"],
            type=zone_data["type"],
            capacity=zone_data["capacity"],
            equipment=zone_data.get("equipment", []),
            attendant_id=zone_data.get("attendant_id"),
            description=zone_data.get("description"),
        )
        location.add_workout_zone(new_zone)
        self.location_repository.save(location)
        return new_zone

    def remove_workout_zone(self, location_id: str, zone_id: str) -> bool:
        """
        Remove a workout zone from a specific location by its ID.
        """
        location = self.location_repository.find_by_id(location_id)
        if not location:
            return False
        success = location.remove_workout_zone(zone_id)
        if success:
            self.location_repository.save(location)
        return success

    def get_workout_zone(self, location_id: str, zone_id: str) -> Optional[WorkoutZone]:
        """
        Retrieve a specific workout zone by its ID within a gym location.
        """
        location = self.location_repository.find_by_id(location_id)
        if not location:
            return None
        return location.get_zone(zone_id)
