"""
Repository for managing members' data storage and retrieval.
"""

import json
from typing import List, Optional
from ..models.member import Member
from ..models.common import Address
from ..models.member import MembershipType, HealthInformation
from pathlib import Path


class MemberRepository:
    """
    Repository class for managing Member data.
    """

    def __init__(self, data_file: str = "data/members.json"):
        self.data_file = Path(data_file)
        self.members: List[Member] = []
        self.load_data()

    def load_data(self):
        """
        Load members' data from the JSON file into memory.
        """
        if not self.data_file.exists():
            self.data_file.write_text("[]")  # Create an empty JSON file if it doesn't exist

        with self.data_file.open("r") as file:
            data = json.load(file)
            self.members = [self._deserialize(member) for member in data]

    def save_data(self):
        """
        Save members' data to the JSON file.
        """
        with self.data_file.open("w") as file:
            json.dump([self._serialize(member) for member in self.members], file, indent=4)

    def add(self, member: Member) -> None:
        """
        Add a new member to the repository.
        """
        self.members.append(member)
        self.save_data()

    def get_all(self) -> List[Member]:
        """
        Retrieve all members from the repository.
        """
        return self.members

    def get_by_id(self, member_id: str) -> Optional[Member]:
        """
        Retrieve a member by their unique ID.
        """
        return next((member for member in self.members if member.id == member_id), None)

    def update(self, updated_member: Member) -> bool:
        """
        Update an existing member's details.
        """
        for i, member in enumerate(self.members):
            if member.id == updated_member.id:
                self.members[i] = updated_member
                self.save_data()
                return True
        return False

    def delete(self, member_id: str) -> bool:
        """
        Delete a member by their unique ID.
        """
        for i, member in enumerate(self.members):
            if member.id == member_id:
                del self.members[i]
                self.save_data()
                return True
        return False

    def _serialize(self, member: Member) -> dict:
        """
        Serialize a Member object into a dictionary.
        """
        return {
            "id": member.id,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "phone": member.phone,
            "address": {
                "street": member.address.street,
                "city": member.address.city,
                "state": member.address.state,
                "postal_code": member.address.postal_code
            },
            "membership_type": member.membership_type.value,
            "health_info": {
                "height": member.health_info.height,
                "weight": member.health_info.weight,
                "medical_conditions": member.health_info.medical_conditions,
                "emergency_contact_name": member.health_info.emergency_contact_name,
                "emergency_contact_phone": member.health_info.emergency_contact_phone,
                "last_health_check": member.health_info.last_health_check.isoformat() if member.health_info.last_health_check else None,
                "notes": member.health_info.notes
            },
            "home_location_id": member.home_location_id,
            "is_active": member.is_active
        }

    def _deserialize(self, data: dict) -> Member:
        """
        Deserialize a dictionary into a Member object.
        """
        return Member(
            id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            address=Address(
                street=data["address"]["street"],
                city=data["address"]["city"],
                state=data["address"]["state"],
                postal_code=data["address"]["postal_code"]
            ),
            membership_type=MembershipType(data["membership_type"]),
            health_info=HealthInformation(
                height=data["health_info"]["height"],
                weight=data["health_info"]["weight"],
                medical_conditions=data["health_info"]["medical_conditions"],
                emergency_contact_name=data["health_info"]["emergency_contact_name"],
                emergency_contact_phone=data["health_info"]["emergency_contact_phone"],
                last_health_check=datetime.fromisoformat(data["health_info"]["last_health_check"]) if data["health_info"]["last_health_check"] else None,
                notes=data["health_info"]["notes"]
            ),
            home_location_id=data.get("home_location_id"),
            is_active=data["is_active"]
        )
