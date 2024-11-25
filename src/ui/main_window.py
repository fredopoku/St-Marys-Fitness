"""
Main window for St Mary's Fitness Management System.
Integrates all views and provides the primary user interface.
"""

from ui.appointment_view import AppointmentView
from ui.attendance_view import AttendanceView
from ui.member_view import MemberView
from ui.location_view import LocationView
from services.appointment_service import AppointmentService
from services.attendance_service import AttendanceService
from services.member_service import MemberService
from services.location_service import LocationService

class MainWindow:
    """Main user interface for the fitness management system"""

    def __init__(self, 
                 appointment_service: AppointmentService, 
                 attendance_service: AttendanceService, 
                 member_service: MemberService, 
                 location_service: LocationService):
        self.appointment_view = AppointmentView(appointment_service)
        self.attendance_view = AttendanceView(attendance_service)
        self.member_view = MemberView(member_service)
        self.location_view = LocationView(location_service)

    def display_menu(self):
        """Display the main menu"""
        print("\n=== St Mary's Fitness Management System ===")
        print("1. Manage Appointments")
        print("2. Manage Attendance")
        print("3. Manage Members")
        print("4. Manage Locations")
        print("0. Exit")

    def handle_choice(self, choice: str):
        """Handle user's menu choice"""
        if choice == "1":
            self.manage_appointments()
        elif choice == "2":
            self.manage_attendance()
        elif choice == "3":
            self.manage_members()
        elif choice == "4":
            self.manage_locations()
        elif choice == "0":
            print("Exiting... Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")

    def manage_appointments(self):
        """Manage appointments"""
        print("\n=== Manage Appointments ===")
        self.appointment_view.display_menu()

    def manage_attendance(self):
        """Manage attendance"""
        print("\n=== Manage Attendance ===")
        self.attendance_view.display_attendance_records(
            self.attendance_view.attendance_service.get_all_attendance_records()
        )
        print("\n1. Log Check-In")
        print("2. Log Check-Out")
        print("3. View Attendance Details")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == "1":
            self.attendance_view.log_check_in()
        elif choice == "2":
            self.attendance_view.log_check_out()
        elif choice == "3":
            self.attendance_view.view_attendance_details()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please try again.")

    def manage_members(self):
        """Manage members"""
        print("\n=== Manage Members ===")
        self.member_view.display_menu()

    def manage_locations(self):
        """Manage locations"""
        print("\n=== Manage Locations ===")
        self.location_view.display_menu()

    def run(self):
        """Run the main program loop"""
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            self.handle_choice(choice)
