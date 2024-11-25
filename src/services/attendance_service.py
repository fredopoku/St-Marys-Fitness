"""
Service layer for handling Attendance-related operations.
"""

from datetime import datetime
from typing import List, Optional
from repositories.attendance_repository import AttendanceRepository
from models.attendance import AttendanceRecord


class AttendanceService:
    """Handles operations related to gym attendance."""

    def __init__(self, attendance_repository: AttendanceRepository):
        self.attendance_repository = attendance_repository

    def check_in(
        self,
        member_id: str,
        location_id: str,
        zone_id: Optional[str] = None
    ) -> AttendanceRecord:
        """
        Create a check-in record for a member.
        """
        active_attendance = self.get_active_attendance(member_id)
        if active_attendance:
            raise ValueError("Member already has an active attendance record.")

        new_attendance = AttendanceRecord(
            member_id=member_id,
            location_id=location_id,
            check_in_time=datetime.now(),
            zone_id=zone_id
        )
        return self.attendance_repository.save(new_attendance)

    def check_out(self, attendance_id: str) -> bool:
        """
        Check out a member by updating their attendance record.
        """
        attendance = self.attendance_repository.find_by_id(attendance_id)
        if not attendance:
            return False
        if attendance.check_out_time is not None:
            return False  # Already checked out
        attendance.check_out()
        self.attendance_repository.save(attendance)
        return True

    def get_active_attendance(self, member_id: str) -> Optional[AttendanceRecord]:
        """
        Retrieve an active attendance record for a specific member.
        """
        records = self.attendance_repository.find_all(
            filters={"member_id": member_id, "check_out_time__isnull": True}
        )
        return records[0] if records else None

    def get_attendance_by_id(self, attendance_id: str) -> Optional[AttendanceRecord]:
        """
        Retrieve a specific attendance record by its ID.
        """
        return self.attendance_repository.find_by_id(attendance_id)

    def list_attendance_for_member(
        self,
        member_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AttendanceRecord]:
        """
        Retrieve all attendance records for a member within an optional date range.
        """
        filters = {"member_id": member_id}
        if start_date:
            filters["check_in_time__gte"] = start_date
        if end_date:
            filters["check_in_time__lte"] = end_date
        return self.attendance_repository.find_all(filters=filters)

    def list_all_attendance(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AttendanceRecord]:
        """
        Retrieve all attendance records, optionally filtered by date range.
        """
        filters = {}
        if start_date:
            filters["check_in_time__gte"] = start_date
        if end_date:
            filters["check_in_time__lte"] = end_date
        return self.attendance_repository.find_all(filters=filters)
