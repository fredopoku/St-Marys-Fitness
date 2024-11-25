"""
Repository for managing appointments.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from src.models.appointment import Appointment, AppointmentStatus, AppointmentType
from src.repositories.base_repository import BaseRepository

class AppointmentRepository(BaseRepository[Appointment]):
    """Repository for managing appointments"""

    def get_upcoming_appointments(self, member_id: Optional[str] = None) -> List[Appointment]:
        """
        Get all upcoming appointments, optionally filtered by member ID.

        :param member_id: Optional ID of the member to filter.
        :return: List of upcoming appointments.
        """
        now = datetime.now()
        return [
            appointment for appointment in self.data
            if appointment.start_time > now
            and (member_id is None or appointment.member_id == member_id)
        ]

    def get_appointments_by_date(self, date: datetime, location_id: Optional[str] = None) -> List[Appointment]:
        """
        Get appointments for a specific date, optionally filtered by location.

        :param date: Date to filter appointments.
        :param location_id: Optional location ID to filter appointments.
        :return: List of appointments for the date.
        """
        date_str = date.strftime("%Y-%m-%d")
        return [
            appointment for appointment in self.data
            if appointment.start_time.strftime("%Y-%m-%d") == date_str
            and (location_id is None or appointment.location_id == location_id)
        ]

    def schedule_appointment(self, appointment: Appointment) -> Appointment:
        """
        Schedule a new appointment.

        :param appointment: Appointment to schedule.
        :return: The scheduled appointment.
        """
        self.add(appointment)
        return appointment

    def cancel_appointment(self, appointment_id: str, note: Optional[str] = None) -> bool:
        """
        Cancel an appointment.

        :param appointment_id: ID of the appointment to cancel.
        :param note: Optional cancellation note.
        :return: True if cancellation was successful, False otherwise.
        """
        appointment = self.get_by_id(appointment_id)
        if appointment and appointment.status not in [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED]:
            appointment.cancel(note)
            self.update(appointment)
            return True
        return False

    def complete_appointment(self, appointment_id: str, note: Optional[str] = None) -> bool:
        """
        Mark an appointment as completed.

        :param appointment_id: ID of the appointment to complete.
        :param note: Optional completion note.
        :return: True if completion was successful, False otherwise.
        """
        appointment = self.get_by_id(appointment_id)
        if appointment and appointment.status == AppointmentStatus.IN_PROGRESS:
            appointment.complete(note)
            self.update(appointment)
            return True
        return False

    def get_member_appointment_history(self, member_id: str) -> List[Appointment]:
        """
        Get the full appointment history for a member.

        :param member_id: ID of the member.
        :return: List of appointments for the member.
        """
        return [appointment for appointment in self.data if appointment.member_id == member_id]

    def get_trainer_schedule(self, trainer_id: str, date: datetime) -> List[Appointment]:
        """
        Get a trainer's schedule for a specific date.

        :param trainer_id: ID of the trainer.
        :param date: Date to filter appointments.
        :return: List of appointments for the trainer on the date.
        """
        date_str = date.strftime("%Y-%m-%d")
        return [
            appointment for appointment in self.data
            if appointment.trainer_id == trainer_id
            and appointment.start_time.strftime("%Y-%m-%d") == date_str
        ]
