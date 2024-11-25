"""
User interface components for managing appointments.
Provides views and controls for scheduling, updating, and viewing appointments.
"""

from datetime import datetime
from typing import List
from services.appointment_service import AppointmentService
from models.appointment import Appointment, AppointmentType

class AppointmentView:
    """UI class for managing appointments"""

    def __init__(self, appointment_service: AppointmentService):
        self.appointment_service = appointment_service

    def display_appointments(self, appointments: List[Appointment]):
        """Display a list of appointments"""
        print("Appointments:")
        for appt in appointments:
            print(f"ID: {appt.id}, Type: {appt.appointment_type.name}, "
                  f"Member ID: {appt.member_id}, Start: {appt.start_time}, "
                  f"Status: {appt.status.name}")

    def schedule_appointment(self):
        """Prompt user to schedule a new appointment"""
        try:
            member_id = input("Enter Member ID: ")
            trainer_id = input("Enter Trainer ID: ")
            location_id = input("Enter Location ID: ")
            appointment_type = AppointmentType[input("Enter Appointment Type (e.g., PERSONAL_TRAINING): ").upper()]
            start_time = datetime.strptime(input("Enter Start Time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
            duration = int(input("Enter Duration (minutes): "))
            zone_id = input("Enter Zone ID (optional): ") or None
            notes = input("Enter Notes (optional): ") or None

            new_appt = self.appointment_service.create_appointment(
                member_id=member_id,
                trainer_id=trainer_id,
                location_id=location_id,
                appointment_type=appointment_type,
                start_time=start_time,
                duration=duration,
                zone_id=zone_id,
                notes=notes
            )
            print(f"Appointment successfully created with ID: {new_appt.id}")
        except Exception as e:
            print(f"Error scheduling appointment: {e}")

    def update_appointment_status(self):
        """Prompt user to update the status of an appointment"""
        try:
            appointment_id = input("Enter Appointment ID: ")
            new_status = input("Enter New Status (e.g., COMPLETED, CANCELLED): ").upper()
            self.appointment_service.update_appointment_status(appointment_id, new_status)
            print("Appointment status updated successfully.")
        except Exception as e:
            print(f"Error updating appointment status: {e}")

    def view_appointment_details(self):
        """Prompt user to view details of a specific appointment"""
        try:
            appointment_id = input("Enter Appointment ID: ")
            appointment = self.appointment_service.get_appointment(appointment_id)
            if appointment:
                print(f"Appointment Details:\n"
                      f"ID: {appointment.id}\n"
                      f"Type: {appointment.appointment_type.name}\n"
                      f"Member ID: {appointment.member_id}\n"
                      f"Trainer ID: {appointment.trainer_id}\n"
                      f"Start Time: {appointment.start_time}\n"
                      f"Duration: {appointment.duration} minutes\n"
                      f"Status: {appointment.status.name}\n"
                      f"Notes: {appointment.notes or 'N/A'}")
            else:
                print("Appointment not found.")
        except Exception as e:
            print(f"Error fetching appointment details: {e}")
