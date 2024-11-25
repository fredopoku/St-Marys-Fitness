"""
Repositories for St Mary's Fitness Management System.
This module exports all repository classes for easy access.
"""

from .member_repository import MemberRepository
from .location_repository import LocationRepository
from .appointment_repository import AppointmentRepository
from .subscription_repository import SubscriptionRepository
from .attendance_repository import AttendanceRepository
from .base_repository import BaseRepository

__all__ = [
    'MemberRepository',
    'LocationRepository',
    'AppointmentRepository',
    'SubscriptionRepository',
    'AttendanceRepository',
    'BaseRepository'
]
