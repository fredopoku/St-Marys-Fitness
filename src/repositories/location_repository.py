"""
Repository for managing gym location and workout zone data.
"""

import json
from typing import List, Optional
from ..models.location import GymLocation, WorkoutZone
from ..models.common import Address
from pathlib import Path


class LocationRepository:
    """
    Repository class for managing GymLocation and WorkoutZone data.
    """

    def __init__(self, data_file: str = "data/locations.json"):
        self.data_file = Path(data_file)
        self.locations: List[GymLocation] = []
        self.load_data()

    def load_data(self):
        """
        Load gym locations' data from the JSON file into memory.
        """
        if not self.data_file.exists():
            self.data_file.write_text("[]")  # Create an empty JSON file if it doesn't exist

        with self.data_file.open("r") as file:
            data = json.load(file)
            self.locations = [self._deserialize(location) for location in data]

    def save_data(self):
        """
        Save gym locations' data to the JSON file.
        """
        with self.data_file.open("w") as file:
            json.dump([self._serialize(location) for location in self.locations], file, indent=4)

    def add_location(self, location: GymLocation) -> None:
        """
        Add a new gym location to the repository.
        """
        self.locations.append(location)
        self.save_data()

    def get_all_locations(self) -> List[GymLocation]:
        """
        Retrieve all gym locations.
        """
        return self.locations

    def get_location_by_id(self, location_id: str) -> Optional[GymLocation]:
        """
        Retrieve a gym location by its unique ID.
        """
        return next((location for location in self.locations if location.id == location_id), None)

    def update_location(self, updated_location: GymLocation) -> bool:
        """
        Update an existing gym location's details.
        """
        for i, location in enumerate(self.locations):
            if location.id == updated_location.id:
                self.locations[i] = updated_location
                self.save_data()
                return True
        return False

    def delete_location(self, location_id: str) -> bool:
        """
        Delete a gym location by its unique ID.
        """
        for i, location in enumerate(self.locations):
            if location.id == location_id:
                del self.locations[i]
                self.save_data()
                return True
        return False

    def add_workout_zone(self, location_id: str, zone: WorkoutZone) -> bool:
        """
        Add a workout zone to a specific gym location.
        """
        location = self.get_location_by_id(location_id)
        if location:
            location.workout_zones.append(zone)
            self.update_location(location)
            return True
        return False

    def remove_workout_zone(self, location_id: str, zone_id: str) -> bool:
        """
        Remove a workout zone from a specific gym location by ID.
        """
        location = self.get_location_by_id(location_id)
        if location:
            if location.remove_workout_zone(zone_id):
                self.update_location(location)
                return True
        return False

    def _serialize(self, location: GymLocation) -> dict:
        """
        Serialize a GymLocation object into a dictionary.
        """
        return {
            "id": location.id,
            "name": location.name,
            "address": {
                "street": location.address.street,
                "city": location.address.city,
                "state": location.address.state,
                "postal_code": location.address.postal_code
            },
            "manager_id": location.manager_id,
            "workout_zones": [self._serialize_zone(zone) for zone in location.workout_zones],
            "amenities": location.amenities,
            "total_capacity": location.total_capacity,
            "contact_phone": location.contact_phone,
            "contact_email": location.contact_email,
            "opening_hours": location.opening_hours,
            "is_active": location.is_active
        }

    def _serialize_zone(self, zone: WorkoutZone) -> dict:
        """
        Serialize a WorkoutZone object into a dictionary.
        """
        return {
            "id": zone.id,
            "name": zone.name,
            "type": zone.type,
            "capacity": zone.capacity,
            "equipment": zone.equipment,
            "attendant_id": zone.attendant_id,
            "description": zone.description,
            "is_active": zone.is_active,
            "schedule": zone.schedule
        }

    def _deserialize(self, data: dict) -> GymLocation:
        """
        Deserialize a dictionary into a GymLocation object.
        """
        return GymLocation(
            id=data["id"],
            name=data["name"],
            address=Address(
                street=data["address"]["street"],
                city=data["address"]["city"],
                state=data["address"]["state"],
                postal_code=data["address"]["postal_code"]
            ),
            manager_id=data["manager_id"],
            workout_zones=[self._deserialize_zone(zone) for zone in data["workout_zones"]],
            amenities=data["amenities"],
            total_capacity=data["total_capacity"],
            contact_phone=data["contact_phone"],
            contact_email=data["contact_email"],
            opening_hours=data["opening_hours"],
            is_active=data["is_active"]
        )

    def _deserialize_zone(self, data: dict) -> WorkoutZone:
        """
        Deserialize a dictionary into a WorkoutZone object.
        """
        return WorkoutZone(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            capacity=data["capacity"],
            equipment=data["equipment"],
            attendant_id=data.get("attendant_id"),
            description=data.get("description"),
            is_active=data["is_active"],
            schedule=data.get("schedule", {})
        )
