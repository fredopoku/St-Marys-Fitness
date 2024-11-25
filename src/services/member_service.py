"""
Service layer for handling Member-related operations.
"""

from typing import List, Optional
from repositories.member_repository import MemberRepository
from models.member import Member, MembershipType, HealthInformation


class MemberService:
    """Handles operations related to gym members."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def create_member(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        membership_type: MembershipType,
        health_info: dict,
        home_location_id: Optional[str] = None,
    ) -> Member:
        """
        Register a new gym member.
        """
        health_data = HealthInformation(
            height=health_info["height"],
            weight=health_info["weight"],
            medical_conditions=health_info.get("medical_conditions", []),
            emergency_contact_name=health_info["emergency_contact_name"],
            emergency_contact_phone=health_info["emergency_contact_phone"],
            last_health_check=health_info.get("last_health_check"),
            notes=health_info.get("notes"),
        )
        new_member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            membership_type=membership_type,
            health_info=health_data,
            home_location_id=home_location_id,
        )
        return self.member_repository.save(new_member)

    def update_member(self, member_id: str, updates: dict) -> Optional[Member]:
        """
        Update details of an existing gym member.
        """
        member = self.member_repository.find_by_id(member_id)
        if not member:
            return None

        for key, value in updates.items():
            if hasattr(member, key):
                setattr(member, key, value)
        return self.member_repository.save(member)

    def deactivate_member(self, member_id: str) -> bool:
        """
        Deactivate a member's account.
        """
        member = self.member_repository.find_by_id(member_id)
        if not member:
            return False
        member.deactivate()
        self.member_repository.save(member)
        return True

    def activate_member(self, member_id: str) -> bool:
        """
        Reactivate a member's account.
        """
        member = self.member_repository.find_by_id(member_id)
        if not member:
            return False
        member.activate()
        self.member_repository.save(member)
        return True

    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        """
        Retrieve a specific member by their ID.
        """
        return self.member_repository.find_by_id(member_id)

    def list_all_members(self, active_only: bool = True) -> List[Member]:
        """
        List all members, optionally filtering by active status.
        """
        filters = {"is_active": True} if active_only else {}
        return self.member_repository.find_all(filters=filters)

    def update_health_information(
        self, member_id: str, health_info: dict
    ) -> Optional[Member]:
        """
        Update a member's health-related information.
        """
        member = self.member_repository.find_by_id(member_id)
        if not member:
            return None
        updated_health_info = HealthInformation(
            height=health_info["height"],
            weight=health_info["weight"],
            medical_conditions=health_info.get("medical_conditions", []),
            emergency_contact_name=health_info["emergency_contact_name"],
            emergency_contact_phone=health_info["emergency_contact_phone"],
            last_health_check=health_info.get("last_health_check"),
            notes=health_info.get("notes"),
        )
        member.update_health_info(updated_health_info)
        return self.member_repository.save(member)
