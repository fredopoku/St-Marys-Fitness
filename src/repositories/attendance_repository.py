"""
Repository for managing attendance records.
"""

from datetime import datetime
from typing import List, Optional
from src.models.attendance import AttendanceRecord
from src.repositories.base_repository import BaseRepository

class AttendanceRepository(BaseRepository[AttendanceRecord]):
    """Repository for attendance records"""

    def get_active_attendance(self, member_id: str) -> Optional[AttendanceRecord]:
        """
        Get the active attendance record for a member.

        :param member_id: ID of the member.
        :return: Active attendance record or None if no active record exists.
        """
        for record in self.data:
            if record.member_id == member_id and record.is_active():
                return record
        return None

    def get_attendance_by_date(self, date: datetime, location_id: Optional[str] = None) -> List[AttendanceRecord]:
        """
        Get attendance records for a specific date, optionally filtered by location.

        :param date: The date to filter attendance records.
        :param location_id: Optional location ID to further filter records.
        :return: List of attendance records.
        """
        date_str = date.strftime("%Y-%m-%d")
        return [
            record for record in self.data
            if record.check_in_time.strftime("%Y-%m-%d") == date_str
            and (location_id is None or record.location_id == location_id)
        ]

    def check_in(self, attendance: AttendanceRecord) -> AttendanceRecord:
        """
        Add a new check-in record.

        :param attendance: Attendance record to add.
        :return: The added attendance record.
        """
        self.add(attendance)
        return attendance

    def check_out(self, member_id: str) -> bool:
        """
        Record a member's check-out.

        :param member_id: ID of the member checking out.
        :return: True if check-out was successful, False otherwise.
        """
        active_record = self.get_active_attendance(member_id)
        if active_record:
            active_record.check_out()
            self.update(active_record)
            return True
        return False

    def get_attendance_history(self, member_id: str) -> List[AttendanceRecord]:
        """
        Get the full attendance history for a member.

        :param member_id: ID of the member.
        :return: List of attendance records for the member.
        """
        return [record for record in self.data if record.member_id == member_id]
