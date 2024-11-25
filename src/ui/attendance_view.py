"""
User interface components for managing attendance records.
Provides views and controls for logging, updating, and viewing attendance.
"""

from typing import List
from services.attendance_service import AttendanceService
from models.attendance import AttendanceRecord
from datetime import datetime

class AttendanceView:
    """UI class for managing attendance"""

    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service

    def display_attendance_records(self, records: List[AttendanceRecord]):
        """Display a list of attendance records"""
        print("Attendance Records:")
        for record in records:
            duration = f"{record.duration} minutes" if record.duration else "In progress"
            print(f"ID: {record.id}, Member ID: {record.member_id}, Location ID: {record.location_id}, "
                  f"Check-in: {record.check_in_time}, Check-out: {record.check_out_time or 'N/A'}, "
                  f"Duration: {duration}")

    def log_check_in(self):
        """Prompt user to log a new check-in"""
        try:
            member_id = input("Enter Member ID: ")
            location_id = input("Enter Location ID: ")
            zone_id = input("Enter Zone ID (optional): ") or None

            new_record = self.attendance_service.log_check_in(
                member_id=member_id,
                location_id=location_id,
                zone_id=zone_id
            )
            print(f"Check-in successfully logged with ID: {new_record.id}")
        except Exception as e:
            print(f"Error logging check-in: {e}")

    def log_check_out(self):
        """Prompt user to log a check-out"""
        try:
            record_id = input("Enter Attendance Record ID: ")
            self.attendance_service.log_check_out(record_id)
            print("Check-out successfully logged.")
        except Exception as e:
            print(f"Error logging check-out: {e}")

    def view_attendance_details(self):
        """Prompt user to view details of a specific attendance record"""
        try:
            record_id = input("Enter Attendance Record ID: ")
            record = self.attendance_service.get_attendance_record(record_id)
            if record:
                duration = f"{record.duration} minutes" if record.duration else "In progress"
                print(f"Attendance Details:\n"
                      f"ID: {record.id}\n"
                      f"Member ID: {record.member_id}\n"
                      f"Location ID: {record.location_id}\n"
                      f"Check-in: {record.check_in_time}\n"
                      f"Check-out: {record.check_out_time or 'N/A'}\n"
                      f"Zone ID: {record.zone_id or 'N/A'}\n"
                      f"Duration: {duration}")
            else:
                print("Attendance record not found.")
        except Exception as e:
            print(f"Error fetching attendance details: {e}")
