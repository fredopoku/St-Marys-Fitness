"""
St Mary's Fitness Management System Core Module.
This package initializes and provides access to all core components of the application.
"""

from .models import (
    Member, MembershipType, HealthInformation,
    GymLocation, WorkoutZone,
    Appointment, AppointmentType,
    Subscription, PaymentFrequency,
    AttendanceRecord,
    Address, BaseModel,
)
from .repositories import (
    MemberRepository, LocationRepository,
    AppointmentRepository, AttendanceRepository,
)
from .services import (
    AppointmentService, AttendanceService,
    LocationService, MemberService,
)
from .ui import (
    AppointmentView, AttendanceView,
    MainWindow, MemberView,
)
from .utils import Config

__all__ = [
    # Models
    "Member", "MembershipType", "HealthInformation",
    "GymLocation", "WorkoutZone",
    "Appointment", "AppointmentType",
    "Subscription", "PaymentFrequency",
    "AttendanceRecord", "Address", "BaseModel",

    # Repositories
    "MemberRepository", "LocationRepository",
    "AppointmentRepository", "AttendanceRepository",

    # Services
    "AppointmentService", "AttendanceService",
    "LocationService", "MemberService",

    # UI
    "AppointmentView", "AttendanceView",
    "MainWindow", "MemberView",

    # Utils
    "Config",
]
