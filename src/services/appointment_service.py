"""
Service layer for handling Appointment-related operations.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from repositories.appointment_repository import AppointmentRepository
from models.appointment import Appointment, AppointmentType, AppointmentStatus


class AppointmentService:
    """Handles operations related to appointments."""

    def __init__(self, appointment_repository: AppointmentRepository):
        self.appointment_repository = appointment_repository

    def create_appointment(
        self,
        member_id: str,
        trainer_id: str,
        location_id: str,
        appointment_type: AppointmentType,
        start_time: datetime,
        duration: int,
        zone_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Appointment:
        """
        Create a new appointment.
        """
        new_appointment = Appointment(
            member_id=member_id,
            trainer_id=trainer_id,
            location_id=location_id,
            appointment_type=appointment_type,
            start_time=start_time,
            duration=duration,
            zone_id=zone_id,
            notes=notes
        )
        return self.appointment_repository.save(new_appointment)

    def get_appointment_by_id(self, appointment_id: str) -> Optional[Appointment]:
        """
        Retrieve an appointment by its ID.
        """
        return self.appointment_repository.find_by_id(appointment_id)

    def list_upcoming_appointments(self, member_id: str) -> List[Appointment]:
        """
        Get a list of upcoming appointments for a specific member.
        """
        return self.appointment_repository.find_all(
            filters={
                "member_id": member_id,
                "start_time__gte": datetime.now(),
                "status": AppointmentStatus.SCHEDULED
            }
        )

    def cancel_appointment(self, appointment_id: str, cancellation_note: Optional[str] = None) -> bool:
        """
        Cancel an appointment by ID.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return False
        if appointment.status not in [AppointmentStatus.SCHEDULED, AppointmentStatus.IN_PROGRESS]:
            return False
        appointment.cancel(cancellation_note)
        self.appointment_repository.save(appointment)
        return True

    def complete_appointment(self, appointment_id: str, completion_note: Optional[str] = None) -> bool:
        """
        Mark an appointment as completed.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return False
        if appointment.status != AppointmentStatus.IN_PROGRESS:
            return False
        appointment.complete(completion_note)
        self.appointment_repository.save(appointment)
        return True

    def reschedule_appointment(
        self,
        appointment_id: str,
        new_start_time: datetime,
        new_duration: Optional[int] = None
    ) -> bool:
        """
        Reschedule an existing appointment.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return False
        if appointment.status != AppointmentStatus.SCHEDULED:
            return False
        appointment.start_time = new_start_time
        if new_duration:
            appointment.duration = new_duration
        self.appointment_repository.save(appointment)
        return True
