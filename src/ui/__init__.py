"""
User Interface components for St Mary's Fitness Management System.
This module provides views for interacting with various system services.
"""

from .appointment_view import AppointmentView
from .attendance_view import AttendanceView
from .main_window import MainWindow
from .member_view import MemberView

__all__ = [
    "AppointmentView",
    "AttendanceView",
    "MainWindow",
    "MemberView",
]
